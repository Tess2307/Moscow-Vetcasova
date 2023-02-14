import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QButtonGroup, QCheckBox, QRadioButton
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap

from api_utils import *
from map_utils import *


class myMap:
    def __init__(self):
        self.toponym = 'Москва, Пестеля, 8Г'
        self.lon = 55.865172
        self.lat = 37.619585
        self.type_map = 'map'
        self.z = 11
        self.shift = {'left': 0,
                      'up': 0 }

my_map = myMap()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(650, 750))  # Устанавливаем размеры
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
        self.label.setText("Поиск:")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)  # Добавляем метку в сетку
        # карта
        self.image = QLabel()
        self.grid_layout.addWidget(self.image, 5, 2, 10, 10)
        self.pixmap = QPixmap()
        #self.image.setPixmap(self.pixmap)

        self.plus = QPushButton("+", self)
        self.grid_layout.addWidget(self.plus, 2, 10, 1, 2)
        self.plus.clicked.connect(self.plus_z)
        self.minus = QPushButton("-", self)
        self.grid_layout.addWidget(self.minus, 2, 2, 1, 2)
        self.minus.clicked.connect(self.minus_z)

        self.left = QPushButton("W", self)
        self.grid_layout.addWidget(self.left, 2, 4, 1, 2)
        self.left.clicked.connect(self.move_left)
        self.up = QPushButton("N", self)
        self.grid_layout.addWidget(self.up, 1, 6, 1, 2)
        self.up.clicked.connect(self.move_up)
        self.right = QPushButton("O", self)
        self.grid_layout.addWidget(self.right, 2, 8, 1, 2)
        self.right.clicked.connect(self.move_right)
        self.bottom = QPushButton("S", self)
        self.grid_layout.addWidget(self.bottom, 3, 6, 1, 2)
        self.bottom.clicked.connect(self.move_bottom)
        self.reset = QPushButton(" ", self)
        self.grid_layout.addWidget(self.reset, 2, 6, 1, 2)
        self.reset.clicked.connect(self.reset_shift)
        # поле
        self.adress = QLineEdit()
        self.adress.resize(650, 40)
        self.adress.setFont(font)
        self.grid_layout.addWidget(self.adress, 0, 2, 1, 10)  # Добавляем поле в сетку
        self.adress.setText(my_map.toponym)
        # кнопка Найти
        self.btn2 = QPushButton("Найти", self)
        self.grid_layout.addWidget(self.btn2, 0, 12, 1, 2)  # Добавляем кнопку в сетку
        self.btn2.clicked.connect(self.new_search)
        self.new_search()
        #
        # Переключатели карты
        self.check_map = QRadioButton("Карта", self)
        self.grid_layout.addWidget(self.check_map, 4, 2, 1, 2)
        self.check_map.setChecked(True)
        self.check_sp = QRadioButton("Спутник", self)
        self.grid_layout.addWidget(self.check_sp, 4, 4, 1, 2)

        self.check_gybrid = QRadioButton("Гибрид", self)
        self.grid_layout.addWidget(self.check_gybrid, 4, 6, 1, 2)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.check_map)
        self.button_group.addButton(self.check_sp)
        self.button_group.addButton(self.check_gybrid)
        self.button_group.buttonClicked.connect(self.check_map_type)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.plus_z()
        elif event.key() == Qt.Key_PageDown:
            self.minus_z()

    def new_search(self):
        my_map.toponym = self.adress.text()
        my_map.lon, my_map.lat = get_coords(my_map.toponym)
        self.change_map()

    def change_map(self):
        lon = my_map.lon + my_map.shift['left'] / my_map.z
        lat = my_map.lat + my_map.shift['up'] / my_map.z
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "z": str(my_map.z),
            "l": my_map.type_map,
            'pt': f"{my_map.lon},{my_map.lat},pm2rdm"
        }
        # обновить изображение
        self.pixmap = QPixmap(get_map(params))
        self.image.setPixmap(self.pixmap)

    def minus_z(self):
        if my_map.z > 3:
            my_map.z = my_map.z - 1
        self.change_map()

    def plus_z(self):
        if my_map.z < 18:
            my_map.z = my_map.z + 1
        self.change_map()

    def move_left(self):
        my_map.shift['left'] -= 1
        self.change_map()

    def move_right(self):
        my_map.shift['left'] += 1
        self.change_map()

    def move_bottom(self):
        my_map.shift['up'] -= 1
        self.change_map()

    def move_up(self):
        my_map.shift['up'] += 1
        self.change_map()

    def reset_shift(self):
        my_map.shift['left'] = 0
        my_map.shift['up'] = 0
        my_map.z = 11
        self.change_map()

    def check_map_type(self):
        if self.check_sp.isChecked():
            my_map.type_map = 'sat'
        elif self.check_map.isChecked():
            my_map.type_map = 'map'
        elif self.check_gybrid.isChecked():
            my_map.type_map = 'sat,skl'
        self.change_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())