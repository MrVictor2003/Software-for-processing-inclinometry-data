from classes.raw_data_collector import RawDataCollectorSevenMeasurements
from classes.converter_raw_data_to_depth_dangle_zangle import ConverterRawDataToDepthDangleZangle
from classes.converter_to_xyh import ConverterToXYH
from classes.well_deviation import WellDeviation
from classes.visualizer import Visualizer
from classes.creator_of_the_txt_file_for_ncad import CreatorOfTheTxtFileForNcad

def main():
    #Чтение файла с сырыми данными
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
    plot_2d = vizualizer.show_2d_trajectory(lst_x, lst_y)
    plot_3d = vizualizer.show_3d_trajectory(lst_x, lst_y, lst_z)

if __name__ == "__main__":
    main()