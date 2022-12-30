import sys
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLineEdit
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtGui import QPainter, QColor


# Унаследуем наш класс от простейшего графического примитива QWidget
class Example(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        uic.loadUi('Ui.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)



    def run(self):
        self.repaint()
    # Метод срабатывает, когда виджету надо
    # перерисовать свое содержимое,
    # например, при создании формы
    def paintEvent(self, event):
        # Создаем объект QPainter для рисования
        qp = QPainter()
        # Начинаем процесс рисования
        qp.begin(self)
        self.draw(qp)
        # Завершаем рисование
        qp.end()

    def draw(self, qp):
        x = randint(10, 300)
        y = randint(10, 300)
        r = randint(10, 30)
        qp.setBrush(QColor(255, 255, 0))
        qp.drawEllipse(x, y, r, r)



if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = Example()
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())

