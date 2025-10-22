import math
import matplotlib.pyplot as plt

class RawDataCollector:
    "Класс для импорта файла с сырыми данными измерений"
    def __init__(self, filename: str):
        self.filename = filename
        self.raw_data = []

    def read_data(self):
        with open(self.filename, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                if len(values) == 11:
                    data_measure = {
                        'time': float(values[0]),
                        'x_accel': float(values[1]),
                        'y_accel': float(values[2]),
                        'z_accel': float(values[3]),
                        'x_gyro': float(values[4]),
                        'y_gyro': float(values[5]),
                        'z_gyro': float(values[6]),
                        'x_magn': float(values[7]),
                        'y_magn': float(values[8]),
                        'z_magn': float(values[9]),
                        'pulses': int(values[10])
                    }

                self.raw_data.append(data_measure)

        return self.raw_data

class ConverterRawDataToLenghtDangleZangle:
    "Класс для расчета расстояний, дирекционных углов, зенитных углов по сырым данным"
    def __init__(self, lst_raw_data):
        self.lst_raw_data = lst_raw_data
        self.lst_lenght_dangle_zangleg_zanglea = []
        self.lst_zangle_accel = []
        self.lst_roll_accel = []
        self.lst_dt = []
        self.lst_zangle_gyro = []
        self.lst_dangle = []
        self.lst_lenght_encoder = []

    def calculate_zangle_by_accel(self):
        for i in self.lst_raw_data:
            self.lst_zangle_accel.append(math.atan2(i.get('y_accel'),
                                                    math.sqrt(i.get('x_accel') ** 2 + i.get('z_accel') ** 2)))
        return self.lst_zangle_accel

    def calculate_roll_by_accel(self):
        for i in self.lst_raw_data:
            self.lst_roll_accel.append(math.atan2(-i.get('x_accel'), i.get('z_accel')))
        return self.lst_roll_accel

    def calculate_dt(self):
        for i in range(len(self.lst_raw_data)):
            if i == len(self.lst_raw_data)-1:
                break
            else:
                self.lst_dt.append(self.lst_raw_data[i+1].get('time')-
                                   self.lst_raw_data[i].get('time'))
        return self.lst_dt

    def calculate_zangle_by_gyro(self):
        self.current_zangle_gyro = self.lst_raw_data[0].get('y_gyro')*self.lst_dt[0]
        self.lst_zangle_gyro.append(self.current_zangle_gyro)
        for i in range(len(self.lst_raw_data)-1):
            self.current_zangle_gyro += self.lst_raw_data[i+1].get('y_gyro')*self.lst_dt[i]
            self.lst_zangle_gyro.append(self.current_zangle_gyro)
        return self.lst_zangle_gyro

    def calculate_lenght_by_encoder(self):
        PPR = 1000
        R = 20

        lenght_one_revolution = 2 * math.pi * R
        lenght_one_pulse = lenght_one_revolution / PPR

        for i in range(len(self.lst_raw_data)):
            if i == 0:
                continue
            else:
                current_value = self.lst_raw_data[i].get('pulses')
                previous_value = self.lst_raw_data[i - 1].get('pulses')
                delta_pulse = current_value - previous_value
                delta_lenght = delta_pulse * lenght_one_pulse
                self.lst_lenght_encoder.append(delta_lenght)

        return self.lst_lenght_encoder

    #Этот метод написал не сам, так как начал сомневаться в правильности расчета
    #roll и pitch в методах calculate_zangle_by_accel() и calculate_roll_by_accel.
    #В данном методе наклон магнитометра компенсируется с помощью акселерометра.
    def calculate_dangle(self):
        """Исправленный расчет азимута с компенсацией наклона"""
        self.lst_dangle = []
        for i in self.lst_raw_data:
            # Нормализация акселерометра
            accel_norm = math.sqrt(i.get('x_accel') ** 2 + i.get('y_accel') ** 2 + i.get('z_accel') ** 2)
            if accel_norm < 0.001:
                continue

            norm_accel_x = i.get('x_accel') / accel_norm
            norm_accel_y = i.get('y_accel') / accel_norm
            norm_accel_z = i.get('z_accel') / accel_norm

            # Углы наклона
            roll = math.atan2(norm_accel_y, norm_accel_z)
            pitch = math.atan2(-norm_accel_x, math.sqrt(norm_accel_y ** 2 + norm_accel_z ** 2))

            # Компенсация наклона магнитометра (ИСПРАВЛЕННАЯ ФОРМУЛА)
            mx = i.get('x_magn')
            my = i.get('y_magn')
            mz = i.get('z_magn')

            magn_x_compensed = mx * math.cos(pitch) + mz * math.sin(pitch)
            magn_y_compensed = (mx * math.sin(roll) * math.sin(pitch) +
                                my * math.cos(roll) -
                                mz * math.sin(roll) * math.cos(pitch))

            # Азимут
            dangle = math.atan2(magn_y_compensed, magn_x_compensed)

            # Нормализация
            if dangle < 0:
                dangle += 2 * math.pi

            self.lst_dangle.append(dangle)
        return self.lst_dangle

    def get_lenght_dangle_zangleg_zanglea(self):
        for i in range(len(self.lst_raw_data)-1):
            data_lenght_dangle_zangleg_zanglea = {
                'lenght': float(self.lst_lenght_encoder[i]),
                'dangle': float(self.lst_dangle[i]),
                'zangle_gyro': float(self.lst_zangle_gyro[i]),
                'zangle_accel': float(self.lst_zangle_accel[i])
            }
            self.lst_lenght_dangle_zangleg_zanglea.append(data_lenght_dangle_zangleg_zanglea)

        return self.lst_lenght_dangle_zangleg_zanglea

class ComplementaryFilter:
    "Класс для фильтрации зенитных углов с помощью комплиментарного фильтра"
    def __init__(self, lst_l_d_zg_za):
        self.lst_l_d_zg_za = lst_l_d_zg_za
        self.lst_lenght_dangle_zangle = []
        self.alpha = 0.9
        self.lst_zangles = []

    def filter_zangles(self):
        self.behind_zangle = 0
        for i in range(len(self.lst_l_d_zg_za)):
            if i == -1:
                continue
            else:
                zangle = (self.alpha * (self.behind_zangle
                                        + math.radians(self.lst_l_d_zg_za[i].get('zangle_gyro')))
                          + (1-self.alpha) * self.lst_l_d_zg_za[i].get('zangle_accel'))

                self.lst_zangles.append(zangle)
                self.behind_zangle = zangle

        return self.lst_zangles

    def get_lenght_dangle_zangle(self):
        for i in range(len(self.lst_l_d_zg_za)):
            self.lst_lenght_dangle_zangle.append({'lenght': self.lst_l_d_zg_za[i].get('lenght'),
                                                  'dangle': self.lst_l_d_zg_za[i].get('dangle'),
                                                  'zangle': self.lst_zangles[i]})

        return self.lst_lenght_dangle_zangle

class ConverterToXYH:
    "Класс для расчета координат по расстояниям, дирекционным и зенитным углам"
    def __init__(self, lst_lenght_dangle_zangle, x=0, y=0, z=0):
        self.lst_lenght_dangle_zangle = lst_lenght_dangle_zangle
        self.x = x
        self.y = y
        self.z = z
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []
        self.lst_xyz = []

    def calculate_x(self):
        self.lst_x.append(self.x)
        for i in self.lst_lenght_dangle_zangle:
            self.x += i.get('lenght')*math.cos(i.get('dangle'))\
                              *math.cos(i.get('zangle'))
            self.lst_x.append(self.x)

        return self.lst_x

    def calculate_y(self):
        self.lst_y.append(self.y)
        for i in self.lst_lenght_dangle_zangle:
            self.y += i.get('lenght')*math.sin(i.get('dangle'))\
                              *math.cos(i.get('zangle'))
            self.lst_y.append(self.y)

        return self.lst_y

    def calculate_z(self):
        self.lst_z.append(self.z)
        for i in self.lst_lenght_dangle_zangle:
            self.z += -i.get('lenght') * math.sin(i.get('zangle'))
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

    def get_lateral_deviations(self):
        for i in self.lst_xyz:
            self.lst_lateral_deviation.append(math.sqrt(i.get('x')**2 + i.get('y')**2))

        return self.lst_lateral_deviation

    def get_max_lateral_deviation(self):
        if abs(max(self.lst_lateral_deviation)) > abs(min(self.lst_lateral_deviation)):
            return max(self.lst_lateral_deviation)
        else:
            return min(self.lst_lateral_deviation)

class Visualizer:
    "Класс для визуализации траектории скважины"
    def __init__(self, lst_xyz):
        self.lst_xyz = lst_xyz
        self.lst_x = []
        self.lst_y = []
        self.lst_z = []

    def get_x(self):
        for i in self.lst_xyz:
            self.lst_x.append(i.get('x'))

        return self.lst_x

    def get_y(self):
        for i in self.lst_xyz:
            self.lst_y.append(i.get('y'))

        return self.lst_y

    def get_z(self):
        for i in self.lst_xyz:
            self.lst_z.append(i.get('z'))

        return self.lst_z

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

def main():
    print('Открытие файла с сырыми данными')
    test_rd_collector = RawDataCollector('./data/super_final_raw_file3.txt')
    raw_data_lst = test_rd_collector.read_data()
    print('Запуск конвертера сырых данных в длину и углы')
    test_converter_raw_data_to_angles = ConverterRawDataToLenghtDangleZangle(raw_data_lst)
    lst_zangles_accel = test_converter_raw_data_to_angles.calculate_zangle_by_accel()
    print('Вычисленные зенитные углы по акселлерометру (В РАДИАНАХ!!!):')
    print(lst_zangles_accel)
    print('Вычисление dt:')
    lst_dt = test_converter_raw_data_to_angles.calculate_dt()
    print(lst_dt)
    print('Вычисленные зенитные углы по гироскопу (В ГРАДУСАХ!!!):')
    lst_zangles_gyro = test_converter_raw_data_to_angles.calculate_zangle_by_gyro()
    print(lst_zangles_gyro)
    print('Вычисленные roll углы по акселерометру (В РАДИАНАХ!!!):')
    lst_roll_accel = test_converter_raw_data_to_angles.calculate_roll_by_accel()
    print(lst_roll_accel)
    lst_lenght_encoder = test_converter_raw_data_to_angles.calculate_lenght_by_encoder()
    print('вычисленные длины по энкодеру')
    print(lst_lenght_encoder)
    lst_dangle = test_converter_raw_data_to_angles.calculate_dangle()
    print('вычисление азимутов')
    print(lst_dangle)

    lst_lenght_dangle_zanglegyro_zangleaccel = test_converter_raw_data_to_angles\
        .get_lenght_dangle_zangleg_zanglea()
    print(lst_lenght_dangle_zanglegyro_zangleaccel)
    print(len(lst_lenght_dangle_zanglegyro_zangleaccel))

    test_complementary_filter = ComplementaryFilter(lst_lenght_dangle_zanglegyro_zangleaccel)
    lst_zangle = test_complementary_filter.filter_zangles()
    print('Отфильтрованные зенитные углы (В РАДИАНАХ!!!)')
    print(lst_zangle)
    print(len(lst_zangle))
    print('Вывод lenght,dangle,zangle:')
    lst_lenght_dangle_zangle = test_complementary_filter.get_lenght_dangle_zangle()
    print(lst_lenght_dangle_zangle)
    print(len(lst_lenght_dangle_zangle))

    test_converter_to_xyz = ConverterToXYH(lst_lenght_dangle_zangle)

    lstx = test_converter_to_xyz.calculate_x()
    lsty = test_converter_to_xyz.calculate_y()
    lstz = test_converter_to_xyz.calculate_z()
    lstxyz = test_converter_to_xyz.get_coords()

    test_well_deviation = WellDeviation(lstxyz)
    print('горизонтальные отклонения скважины')
    lst_lateral_deviations = test_well_deviation.get_lateral_deviations()
    print(lst_lateral_deviations)
    print('максимальное горизонтальное отклонение')
    print(test_well_deviation.get_max_lateral_deviation())

    viz1 = Visualizer(lstxyz)
    x1 = viz1.get_x()
    y1 = viz1.get_y()
    z1 = viz1.get_z()
    trajectory_x_z = viz1.show_2d_trajectory(x1, z1)
    trajectory_x_y = viz1.show_2d_trajectory(x1, y1)
    trajectory_y_z = viz1.show_2d_trajectory(y1, z1)
    trajectory_x_y_z = viz1.show_3d_trajectory(x1, y1, z1)


    """это проверка расчета зенитных углов (нужно будет добавить в метод calculate_zangle_by_gyro,
    если это правильно или удалить, если нет"""
    check_y_gyro = []
    for i in raw_data_lst:
        check_y_gyro.append(i.get('y_gyro'))

    print('данные с гироскопа по оси у:')
    print(check_y_gyro)

    print('dt:')
    print(lst_dt)

    check_lst_gyro_pitch = []
    for i in range(len(lst_dt)):
        if i == 0:
            behind_gyro_pitch = lst_dt[i]*check_y_gyro[i]
            check_lst_gyro_pitch.append(behind_gyro_pitch)
        else:
            current_gyro_pitch = behind_gyro_pitch + lst_dt[i]*check_y_gyro[i]
            check_lst_gyro_pitch.append(current_gyro_pitch)
            behind_gyro_pitch = current_gyro_pitch


    print('зенитные углы по гироскопу в градусах:')
    print(check_lst_gyro_pitch)
    print(len(check_lst_gyro_pitch))

    print('вычисленные зенитные углы по гироскопу в классе моем')
    print(lst_zangles_gyro)
    print(len(lst_zangles_gyro))
if __name__ == "__main__":
    main()