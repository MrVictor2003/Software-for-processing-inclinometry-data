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
        self.lst_depth = []

    def get_depth(self):
        self.lst_depth = []
        for i in self.lst_raw_data:
            self.lst_depth.append(i.get('depth'))
        return self.lst_depth

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


def main():
    #Чтение файла с сырыми данными
    filename = "./data/raw_data_ishodnie.txt"
    data_collector7 = RawDataCollectorSevenMeasurements(filename)
    raw_data7 = data_collector7.read_data()
    print(raw_data7)
    print(type(raw_data7))

    #Расчет азимутов
    converter_raw_data = ConverterRawDataToDepthDangleZangle(raw_data7)
    lst_azimuths = converter_raw_data.calculate_azimuths()
    print(lst_azimuths)
    print(len(lst_azimuths))

    #Расчет зенитных углов
    lst_zangles = converter_raw_data.calculate_zangles()
    print(lst_zangles)
    print(len(lst_zangles))

    lst_depth = converter_raw_data.get_depth()
    print(lst_depth)
    print(len(lst_depth))

if __name__ == "__main__":
    main()