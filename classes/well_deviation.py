import math

class WellDeviation:
    """Класс, рассчитывающий отклонение скважины"""
    def __init__(self, lst_xyz):
        self.lst_xyz = lst_xyz
        self.lst_lateral_deviation = []
        self.index_max_lateral_deviation = 0
        self.max_lateral_deviation = 0
        self.deviation_x = 0
        self.deviation_y = 0

    def get_max_lateral_deviation(self):
        for i in self.lst_xyz:
            self.lst_lateral_deviation.append(
                math.sqrt(i.get('x')**2+i.get('y')**2))

        self.index_max_lateral_deviation = (
            self.lst_lateral_deviation.index(
                max(self.lst_lateral_deviation)))

        self.deviation_x = (
                self.lst_xyz[self.index_max_lateral_deviation].get('x')
                -self.lst_xyz[0].get('x'))

        self.deviation_y = (
                self.lst_xyz[self.index_max_lateral_deviation].get('y')
                -self.lst_xyz[0].get('y'))

        self.max_lateral_deviation = round(
            math.sqrt(self.deviation_x**2+self.deviation_y**2),3)

        return self.max_lateral_deviation