import matplotlib.pyplot as plt

class Visualizer:
    "Класс для визуализации траектории скважины"
    def __init__(self, lst_x, lst_y, lst_z):
        self.lst_x = lst_x
        self.lst_y = lst_y
        self.lst_z = lst_z

    def show_x_z(self):
        plt.plot(self.lst_x, self.lst_z)
        plt.show()

    def show_2d_trajectory(self, first_axis, second_axis):
        self.first_axis = first_axis
        self.second_axis = second_axis
        plt.plot(self.first_axis, self.second_axis,
                 label='Траектория скважины')
        plt.axis('equal')
        plt.xlabel('Восток')
        plt.ylabel('Север')
        plt.title('График траектории скважины')
        plt.legend()
        plt.show()

    def show_3d_trajectory(self, first_axis, second_axis, third_axis):
        self.first_axis = first_axis
        self.second_axis = second_axis
        self.third_axis = third_axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.xlabel('Восток')
        plt.ylabel('Север')
        ax.set_zlabel('Глубина')
        ax.plot(self.first_axis, self.second_axis, self.third_axis,
                label='Траектория скважины')
        ax.axis('equal')
        plt.title('График траектории скважины')
        plt.legend()
        plt.show()