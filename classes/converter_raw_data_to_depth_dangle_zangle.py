import math

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

    def get_lenght_azimuths_zangles(self):
        for i in range(len(self.lst_lenght)):
            data_lenght_azimuths_zangles = {
                'lenght': float(self.lst_lenght[i]),
                'avg_azimuth': float(self.lst_avg_azimuths[i]),
                'avg_zangle': float(self.lst_avg_zangles[i])
            }
            self.lst_lenght_azimuths_zangles.append(data_lenght_azimuths_zangles)

        return self.lst_lenght_azimuths_zangles