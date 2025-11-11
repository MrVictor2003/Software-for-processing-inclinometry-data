import math
import matplotlib.pyplot as plt

class RawDataCollectorSevenMeasurements:
    "Класс для импорта файла с сырыми данными измерений"
    def __init__(self, filename: str):
        self.filename = filename
        self.raw_data = []

    def read_data(self):
        with open(self.filename, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                if len(values) == 7:
                    data_measure = {
                        'depth': float(values[0]),
                        'x_accel': float(values[1]),
                        'y_accel': float(values[2]),
                        'z_accel': float(values[3]),
                        'x_magn': float(values[4]),
                        'y_magn': float(values[5]),
                        'z_magn': float(values[6])
                    }
                    self.raw_data.append(data_measure)

        return self.raw_data

class ConverterRawDataToDepthDangleZangle:
    "Класс для расчета азимутов и зенитных углов по сырым данным"
    def __init__(self, lst_raw_data):
        self.lst_raw_data = lst_raw_data
        self.lst_azimuths = []
        self.lst_adjusted_azimuths = []
        self.lst_zangles = []
        self.lst_depths = []
        self.lst_lenght = []
        self.lst_avg_azimuths = []
        self.lst_avg_zangles = []
        self.lst_lenght_azimuths_zangles = []

    def get_depth(self):
        self.lst_depths = []
        for i in self.lst_raw_data:
            self.lst_depths.append(i.get('depth'))
        return self.lst_depths

    def calculate_lenght(self):
        for i in range(len(self.lst_depths)-1):
            self.lst_lenght.append(round(self.lst_depths[i+1]-self.lst_depths[i],3))
        return self.lst_lenght

    def calculate_azimuths(self):
        self.lst_azimuths = []
        for i in self.lst_raw_data:

            accel_x = i.get('x_accel')
            accel_y = i.get('y_accel')
            accel_z = i.get('z_accel')

            accel_norm = math.sqrt(accel_x**2+accel_y**2+accel_z**2)
            if accel_norm < 0.001:
                continue

            magn_x = i.get('x_magn')
            magn_y = i.get('y_magn')
            magn_z = i.get('z_magn')

            # Азимут
            azimuth = math.atan2(accel_norm*(magn_y*accel_x-magn_x*accel_y),
                                magn_z*(accel_x**2+accel_y**2)-accel_z*\
                                (accel_x*magn_x+accel_y*magn_y))

            # Нормализация
            if azimuth < 0:
                azimuth += 2 * math.pi

            self.lst_azimuths.append(azimuth)
        return self.lst_azimuths

    def calculate_delta_azimuth(self, b, l, magnetic_declination, n, lst_azimuths):
        self.lst_azimuths = lst_azimuths
        self.b = b
        self.l = l
        self.magnetic_declination = magnetic_declination
        self.n = n
        self.lst_adjusted_azimuths = []

        l_0 = 6 * self.n - 3
        b_rad = math.radians(self.b)
        l_rad = math.radians(self.l)
        l_0_rad = math.radians(l_0)
        convergence_of_the_meridians = (l_rad - l_0_rad) * math.sin(b_rad)

        for i in self.lst_azimuths:
            adjusted_azimuth = i + self.magnetic_declination - convergence_of_the_meridians
            self.lst_adjusted_azimuths.append(adjusted_azimuth)
        return self.lst_adjusted_azimuths

    def calculate_avg_azimuths(self):
        for i in range(len(self.lst_adjusted_azimuths)-1):
            self.lst_avg_azimuths.append((self.lst_adjusted_azimuths[i+1]+
                                                self.lst_adjusted_azimuths[i])/2)
        return self.lst_avg_azimuths

    def calculate_zangles(self):
        self.lst_zangles = []
        for i in self.lst_raw_data:

            accel_x = i.get('x_accel')
            accel_y = i.get('y_accel')
            accel_z = i.get('z_accel')

            accel_norm = math.sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)
            if accel_norm < 0.001:
                continue

            self.lst_zangles.append(math.acos(accel_z/accel_norm))

        return self.lst_zangles

    def calculate_avg_zangles(self):
        for i in range(len(self.lst_zangles)-1):
            self.lst_avg_zangles.append((self.lst_zangles[i+1]+
                                                self.lst_zangles[i])/2)
        return self.lst_avg_zangles

    #поменять метод ниже на список с вложенными словарями СРЕДНИХ ЗНАЧЕНИЙ

    def get_lenght_azimuths_zangles(self):
        for i in range(len(self.lst_lenght)):
            data_lenght_azimuths_zangles = {
                'lenght': float(self.lst_lenght[i]),
                'avg_azimuth': float(self.lst_avg_azimuths[i]),
                'avg_zangle': float(self.lst_avg_zangles[i])
            }
            self.lst_lenght_azimuths_zangles.append(data_lenght_azimuths_zangles)

        return self.lst_lenght_azimuths_zangles

class ConverterToXYH:
    "Класс для расчета координат по расстояниям, дирекционным и зенитным углам"
    def __init__(self, lst_lenght_azimuths_zangles, x=7602075.49, y=457761.31, z=-9.69):
        self.lst_lenght_azimuths_zangles = lst_lenght_azimuths_zangles
        self.x = x
        self.y = y
        self.z = z
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []
        self.lst_xyz = []

    def calculate_x(self):
        self.lst_x.append(self.x)
        for i in self.lst_lenght_azimuths_zangles:
            self.x += i.get('lenght')*math.sin(i.get('avg_zangle'))*math.cos(i.get('avg_azimuth'))

            self.lst_x.append(self.x)

        return self.lst_x

    def calculate_y(self):
        self.lst_y.append(self.y)
        for i in self.lst_lenght_azimuths_zangles:
            self.y += i.get('lenght')*math.sin(i.get('avg_zangle'))*\
            math.sin(i.get('avg_azimuth'))

            self.lst_y.append(self.y)

        return self.lst_y

    def calculate_z(self):
        self.lst_z.append(self.z)
        for i in self.lst_lenght_azimuths_zangles:
            self.z += -i.get('lenght')*math.cos(i.get('avg_zangle'))

            self.lst_z.append(self.z)

        return self.lst_z

    def get_coords(self):
        for i in range(len(self.lst_x)):
            self.lst_xyz.append({'x': self.lst_x[i],
                                 'y': self.lst_y[i],
                                 'z': self.lst_z[i]})
        return self.lst_xyz

class WellDeviation:
    def __init__(self, lst_xyz):
        self.lst_xyz = lst_xyz
        self.lst_lateral_deviation = []
        self.index_max_lateral_deviation = 0
        self.max_lateral_deviation = 0
        self.deviation_x = 0
        self.deviation_y = 0

    def get_max_lateral_deviation(self):
        for i in self.lst_xyz:
            self.lst_lateral_deviation.append(math.sqrt(i.get('x')**2 + i.get('y')**2))

        self.index_max_lateral_deviation = self.lst_lateral_deviation.index(max(
            self.lst_lateral_deviation))

        self.deviation_x = (self.lst_xyz[self.index_max_lateral_deviation].get('x') -
                            self.lst_xyz[0].get('x'))

        self.deviation_y = (self.lst_xyz[self.index_max_lateral_deviation].get('y') -
                            self.lst_xyz[0].get('y'))

        self.max_lateral_deviation = math.sqrt(self.deviation_x**2 + self.deviation_y**2)

        return self.max_lateral_deviation

class Visualizer:
    "Класс для визуализации траектории скважины"
    def __init__(self, lst_x, lst_y, lst_z):
        self.lst_x = lst_x
        self.lst_y = lst_y
        self.lst_z = lst_z

    def show_x_z(self):
        plt.plot(self.lst_x, self.lst_z)
        plt.show()

    def show_2d_trajectory(self, first_axis, second_axis):
        self.first_axis = first_axis
        self.second_axis = second_axis
        plt.plot(self.first_axis, self.second_axis,
                 label='Траектория скважины')
        plt.axis('equal')
        plt.title('График траектории скважины')
        plt.legend()
        plt.show()

    def show_3d_trajectory(self, first_axis, second_axis, third_axis):
        self.first_axis = first_axis
        self.second_axis = second_axis
        self.third_axis = third_axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(self.first_axis, self.second_axis, self.third_axis)
        ax.axis('equal')
        plt.show()

class CreatorOfTheTxtFileForNcad:
    def __init__(self, lst_xyz):
        self.lst_xyz = lst_xyz

    def create_txt_file_with_points(self, filename):
        self.filename = filename

        with open(filename, 'w') as file:
            file.write('POINT\n')
            for i in self.lst_xyz:
                file.write(f'{round(i.get('x'),3)},{round(i.get('y'),3)},{round(i.get('z'),3)}\n')

    def create_txt_file_with_plines(self, filename):
        self.filename = filename

        with open(filename, 'w') as file:
            file.write('3DPOLY\n')
            for i in self.lst_xyz:
                file.write(f'{round(i.get('x'),3)},{round(i.get('y'),3)},{round(i.get('z'),3)}\n')



def main():
    print('Чтение файла с сырыми данными')
    filename = "./data/raw_data_ishodnie.txt"
    data_collector7 = RawDataCollectorSevenMeasurements(filename)
    raw_data7 = data_collector7.read_data()
    print(raw_data7)

    print('Расчет азимутов')
    converter_raw_data = ConverterRawDataToDepthDangleZangle(raw_data7)
    lst_azimuths = converter_raw_data.calculate_azimuths()
    print(lst_azimuths)
    print(len(lst_azimuths))

    print('Расчет азимутов с поправкой')
    lst_adjusted_azimuths = converter_raw_data.calculate_delta_azimuth(
        68.527570255,
        79.964853136,
        0.40247292551,
        14,
        lst_azimuths)
    print(lst_adjusted_azimuths)
    print(len(lst_adjusted_azimuths))

    print('Расчет зенитных углов')
    lst_zangles = converter_raw_data.calculate_zangles()
    print(lst_zangles)
    print(len(lst_zangles))

    print('Вывод глубин')
    lst_depths = converter_raw_data.get_depth()
    print(lst_depths)
    print(len(lst_depths))

    print('Расчет длин отрезков')
    lst_lenghts = converter_raw_data.calculate_lenght()
    print(lst_lenghts)
    print(len(lst_lenghts))
    print('Расчет средних азимутов')
    lst_avg_azimuths = converter_raw_data.calculate_avg_azimuths()
    print(lst_avg_azimuths)
    print(len(lst_avg_azimuths))
    print('Расчет средних зенитных углов')
    lst_avg_zangles = converter_raw_data.calculate_avg_zangles()
    print(lst_avg_zangles)
    print(len(lst_avg_zangles))

    print('Вывод списка с длинами, азимутами и зенитными углами')
    lst_de_az_za = converter_raw_data.get_lenght_azimuths_zangles()
    print(lst_de_az_za)
    print(len(lst_de_az_za))

    converter_to_xyh = ConverterToXYH(lst_de_az_za)
    print('расчет координат по оси X')
    lst_x = converter_to_xyh.calculate_x()
    print(lst_x)
    print(len(lst_x))
    print(min(lst_x))
    print('расчет координат по оси Y')
    lst_y = converter_to_xyh.calculate_y()
    print(lst_y)
    print(len(lst_y))
    print(min(lst_y))
    print('расчет координат по оси H')
    lst_z = converter_to_xyh.calculate_z()
    print(lst_z)
    print(len(lst_z))
    print(min(lst_z))

    lst_xyz = converter_to_xyh.get_coords()
    print(lst_xyz)
    print(len(lst_xyz))

    test_well_deviation = WellDeviation(lst_xyz)
    print('максимальное горизонтальное отклонение')
    print(test_well_deviation.get_max_lateral_deviation())

    txt_file_test = CreatorOfTheTxtFileForNcad(lst_xyz)
    txt_file_test.create_txt_file_with_points('./data/txt_file_with_points_to_ncad.txt')
    txt_file_test.create_txt_file_with_plines('./data/txt_file_with_polylines_to_ncad.txt')

    vizualizer = Visualizer(lst_x, lst_y, lst_z)
    # plot_2d = vizualizer.show_2d_trajectory(lst_x, lst_y)
    # plot_3d = vizualizer.show_3d_trajectory(lst_x, lst_y, lst_z)


if __name__ == "__main__":
    main()