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

    def calculate_avg_azimuths(self):
        for i in range(len(self.lst_azimuths)-1):
            self.lst_avg_azimuths.append((self.lst_azimuths[i+1]+\
                                                self.lst_azimuths[i])/2)
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
            self.lst_avg_zangles.append((self.lst_zangles[i+1]+\
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
    def __init__(self, lst_lenght_azimuths_zangles, x=0, y=0, z=0):
        self.lst_lenght_azimuths_zangles = lst_lenght_azimuths_zangles
        self.x = x
        self.y = y
        self.z = z
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []

    def calculate_x(self):
        for i in self.lst_lenght_azimuths_zangles:
            self.x += i.get('lenght')*math.sin(i.get('avg_azimuth'))*\
            math.sin(i.get('avg_zangle'))

            self.lst_x.append(self.x)

        return self.lst_x

    def calculate_y(self):
        for i in self.lst_lenght_azimuths_zangles:
            self.y += i.get('lenght')*math.sin(i.get('avg_azimuth'))*\
            math.cos(i.get('avg_zangle'))

            self.lst_y.append(self.y)

        return self.lst_y

    def calculate_z(self):
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


def main():
    #Чтение файла с сырыми данными
    filename = "./data/raw_data_ishodnie.txt"
    data_collector7 = RawDataCollectorSevenMeasurements(filename)
    raw_data7 = data_collector7.read_data()
    print(raw_data7)

    #Расчет азимутов
    converter_raw_data = ConverterRawDataToDepthDangleZangle(raw_data7)
    lst_azimuths = converter_raw_data.calculate_azimuths()
    print(lst_azimuths)
    print(len(lst_azimuths))

    #Расчет зенитных углов
    lst_zangles = converter_raw_data.calculate_zangles()
    print(lst_zangles)
    print(len(lst_zangles))

    lst_depths = converter_raw_data.get_depth()
    print(lst_depths)
    print(len(lst_depths))

    lst_lenghts = converter_raw_data.calculate_lenght()
    print(lst_lenghts)
    print(len(lst_lenghts))

    lst_avg_azimuths = converter_raw_data.calculate_avg_azimuths()
    print(lst_avg_azimuths)
    print(len(lst_avg_azimuths))

    lst_avg_zangles = converter_raw_data.calculate_avg_zangles()
    print(lst_avg_zangles)
    print(len(lst_avg_zangles))

    lst_de_az_za = converter_raw_data.get_lenght_azimuths_zangles()
    print(lst_de_az_za)
    print(len(lst_de_az_za))

    converter_to_xyh = ConverterToXYH(lst_de_az_za)
    lst_x = converter_to_xyh.calculate_x()
    print(lst_x)
    print(len(lst_x))

    lst_y = converter_to_xyh.calculate_y()
    print(lst_y)
    print(len(lst_y))

    lst_z = converter_to_xyh.calculate_z()
    print(lst_z)
    print(len(lst_z))

if __name__ == "__main__":
    main()