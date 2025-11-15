import math

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
        self.lst_xyz = []

    def calculate_x(self):
        self.lst_x.append(self.x)
        for i in self.lst_lenght_azimuths_zangles:
            self.x += (i.get('lenght')*math.sin(i.get('avg_zangle'))
                       *math.cos(i.get('avg_azimuth')))

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