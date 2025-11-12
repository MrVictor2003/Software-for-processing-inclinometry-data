#Импорт классов программы
from classes.raw_data_collector import RawDataCollectorSevenMeasurements
from classes.converter_raw_data_to_depth_dangle_zangle import ConverterRawDataToDepthDangleZangle
from classes.converter_to_xyh import ConverterToXYH
from classes.well_deviation import WellDeviation
from classes.visualizer import Visualizer
from classes.creator_of_the_txt_file_for_ncad import CreatorOfTheTxtFileForNcad

#main функция, исполняющая программу
def main():
    #Чтение файла с исходными (сырыми) данными
    filename = "./data/raw_data_ishodnie.txt"
    data_collector7 = RawDataCollectorSevenMeasurements(filename)
    raw_data7 = data_collector7.read_data()
    print(raw_data7)

    #Расчет азимутов
    converter_raw_data = ConverterRawDataToDepthDangleZangle(raw_data7)
    lst_azimuths = converter_raw_data.calculate_azimuths()
    print(lst_azimuths)
    print(len(lst_azimuths))

    #Расчет дирекционных углов
    print('Расчет азимутов с поправкой')
    lst_adjusted_azimuths = converter_raw_data.calculate_delta_azimuth(
        68.527570255,
        79.964853136,
        0.40247292551,
        14,
        lst_azimuths)
    print(lst_adjusted_azimuths)
    print(len(lst_adjusted_azimuths))

    #Расчет зенитных углов
    print('Расчет зенитных углов')
    lst_zangles = converter_raw_data.calculate_zangles()
    print(lst_zangles)
    print(len(lst_zangles))

    #Формирование списка с расстояниями от устья до станций съемки
    print('Вывод глубин')
    lst_depths = converter_raw_data.get_depth()
    print(lst_depths)
    print(len(lst_depths))

    #Расчет длин интервалов между станциями съемки
    lst_lenghts = converter_raw_data.calculate_lenght()
    print(lst_lenghts)
    print(len(lst_lenghts))

    #Расчет средних дирекционных углов
    lst_avg_azimuths = converter_raw_data.calculate_avg_azimuths()
    print(lst_avg_azimuths)
    print(len(lst_avg_azimuths))

    #Расчет средних зенитных углов
    lst_avg_zangles = converter_raw_data.calculate_avg_zangles()
    print(lst_avg_zangles)
    print(len(lst_avg_zangles))

    #Формирование списка с вложенными словарями с
    #длинами, азимутами и зенитными углами
    lst_de_az_za = converter_raw_data.get_lenght_azimuths_zangles()
    print(lst_de_az_za)
    print(len(lst_de_az_za))

    #Задаются координаты устья скважины х-север, y-восток
    converter_to_xyh = ConverterToXYH(lst_de_az_za,7602075.49,457761.31,-9.69)

    #Расчет координат по оси X
    lst_x = converter_to_xyh.calculate_x()
    print(lst_x)
    print(len(lst_x))
    print(min(lst_x))

    #Расчет координат по оси Y
    lst_y = converter_to_xyh.calculate_y()
    print(lst_y)
    print(len(lst_y))
    print(min(lst_y))

    #Расчет координат по оси H
    lst_z = converter_to_xyh.calculate_z()
    print(lst_z)
    print(len(lst_z))
    print(min(lst_z))

    #Получается список с вложенными словарями координат станций съемки
    lst_xyz = converter_to_xyh.get_coords()
    print(lst_xyz)
    print(len(lst_xyz))

    #Вывод максимального горизонтального отклонения
    test_well_deviation = WellDeviation(lst_xyz)
    print('максимальное горизонтальное отклонение')
    print(test_well_deviation.get_max_lateral_deviation())

    txt_file_test = CreatorOfTheTxtFileForNcad(lst_xyz)
    #Запись файла с координатами точек для импорта в "NanoCAD"
    txt_file_test.create_txt_file_with_points('./data/txt_file_with_points_to_ncad.txt')
    #Запись файла с полилинией траектории скважины для импорта в "NanoCAD"
    txt_file_test.create_txt_file_with_plines('./data/txt_file_with_polylines_to_ncad.txt')

    vizualizer = Visualizer(lst_x, lst_y, lst_z)
    #Отображение 2d графика с траекторией скважины в плане
    plot_2d = vizualizer.show_2d_trajectory(lst_y, lst_x)
    #Отображение 3d графика с траекторией скважины
    plot_3d = vizualizer.show_3d_trajectory(lst_y, lst_x, lst_z)

#Точка входа
if __name__ == "__main__":
    main()