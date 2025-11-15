class CreatorOfTheTxtFileForNcad:
    """Класс для создания txt-файла для импорта в ПО NanoCAD"""
    def __init__(self, lst_xyz):
        self.lst_xyz = lst_xyz

    def create_txt_file_with_points(self, filename):
        self.filename = filename

        with open(filename, 'w') as file:
            file.write('POINT\n')
            for i in self.lst_xyz:
                file.write(f'{round(i.get('y'),3)},{round(i.get('x'),3)},'
                           f'{round(i.get('z'),3)}\n')

    def create_txt_file_with_plines(self, filename):
        self.filename = filename

        with open(filename, 'w') as file:
            file.write('3DPOLY\n')
            for i in self.lst_xyz:
                file.write(f'{round(i.get('y'),3)},{round(i.get('x'),3)},'
                           f'{round(i.get('z'),3)}\n')
