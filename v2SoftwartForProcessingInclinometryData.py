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
                        'Depth': float(values[0]),
                        'x_accel': float(values[1]),
                        'y_accel': float(values[2]),
                        'z_accel': float(values[3]),
                        'x_magn': float(values[4]),
                        'y_magn': float(values[5]),
                        'z_magn': float(values[6])
                    }

                self.raw_data.append(data_measure)

        return self.raw_data

class RawDataCollectorTenMeasurements:
    "Класс для импорта файла с сырыми данными измерений"
    def __init__(self, filename: str):
        self.filename = filename
        self.raw_data = []

    def read_data(self):
        with open(self.filename, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                if len(values) == 10:
                    data_measure = {
                        'Depth': float(values[0]),
                        'x_accel': float(values[1]),
                        'y_accel': float(values[2]),
                        'z_accel': float(values[3]),
                        'x_gyro': float(values[4]),
                        'y_gyro': float(values[5]),
                        'z_gyro': float(values[6]),
                        'x_magn': float(values[7]),
                        'y_magn': float(values[8]),
                        'z_magn': float(values[9])
                    }

                self.raw_data.append(data_measure)

        return self.raw_data

#тут написать класс для расчета для 7 измерений

#тут написать класс для расчета для 10 измерений

if __name__ == "__main__":
    filename = "./data/raw_data_ishodnie.txt"

    file_format = 0

    try:
        raw_data = RawDataCollectorTenMeasurements(filename).read_data()
        print("Формат 10 измерений в строке")
    except:
        try:
            raw_data = RawDataCollectorSevenMeasurements(filename).read_data()
            print("Формат 7 измерений в строке")
        except:
            ValueError ('Неправильный формат файла')
    print(raw_data)