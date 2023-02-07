import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtCore import QSize

from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt

from api_utils import *
from map_utils import *


class myMap:
    def __init__(self):
        self.z = 11
        self.lat = 37.619585
        self.lon = 55.865172


my_map = myMap()


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(600, 600))  # Устанавливаем размеры
        self.setWindowTitle("Большая задача")  # Устанавливаем заголовок окна
        self.central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.grid_layout = QGridLayout()  # Создаём QGridLayout
        self.central_widget.setLayout(self.grid_layout)  # Устанавливаем данное размещение в центральный виджет
        # метка и кнопки
        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("Адрес:")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)  # Добавляем метку в сетку
        # карта
        self.image = QLabel()
        self.grid_layout.addWidget(self.image, 1, 3, 10, 10)
        self.pixmap = QPixmap("data//empty.png")
        self.image.setPixmap(self.pixmap)

        self.plus = QPushButton("+", self)
        self.grid_layout.addWidget(self.plus, 1, 14, 1, 1)
        self.plus.clicked.connect(self.plus_z)
        self.minus = QPushButton("-", self)
        self.grid_layout.addWidget(self.minus, 1, 0, 1, 1)
        self.minus.clicked.connect(self.minus_z)

        # поле
        self.adress = QLineEdit()
        self.adress.setFont(font)
        self.grid_layout.addWidget(self.adress, 0, 3, 1, 10)  # Добавляем поле в сетку
        self.adress.setText('Пестеля, 5')
        # поле для вывода изображения карты
        # кнопка Найти
        self.btn2 = QPushButton("Найти", self)
        self.grid_layout.addWidget(self.btn2, 0, 13, 1, 2)  # Добавляем кнопку в сетку
        self.btn2.clicked.connect(self.new_search)

    def new_search(self):
        toponym_to_find = self.adress.text()
        print(toponym_to_find)

        # Получаем координаты центра карты
        my_map.lon, my_map.lat = get_coords(toponym_to_find)
        params = {
            "ll": ",".join([str(my_map.lon), str(my_map.lat)]),
            "z": str(my_map.z),
            "l": "map",
            'pt': f"{my_map.lon},{my_map.lat}"
        }

        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)

    def minus_z(self):
        if my_map.z > 0:
            my_map.z = my_map.z - 1
        self.change_z()

    def plus_z(self):
        if my_map.z < 17:
            my_map.z = my_map.z + 1

        self.change_z()

    def change_z(self):
        params = {
            "ll": ",".join([str(my_map.lon), str(my_map.lat)]),
            "z": str(my_map.z),
            "l": "map",
            'pt': f"{my_map.lon},{my_map.lat}"
        }

        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)
        self.btn2.setEnabled(True)  # включить кнопку "Найти"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())