import sys
import math
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QLabel,
    QWidget,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPainter, QColor, QPen


class Point:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.setMinimumSize(400, 400)
        self.axis_points = [Point(0, 0, 0), Point(0, 0, 0)]
        self.intersection_point = Point(0, 0, 0)

    def add_point(self, x, y):
        now = QTime.currentTime().msecsSinceStartOfDay()
        self.points.append(Point(x, y, now))

    def update_axis_points(self, x, y):
        self.axis_points = [Point(self.width(), y, 0), Point(x, self.height(), 0)]
        self.intersection_point = Point(x, y, 0)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        now = QTime.currentTime().msecsSinceStartOfDay()
        self.points = [point for point in self.points if now - point.time <= 5000]

        for point in self.points:
            color = QColor(255, 255, 255)  # сделать точки белыми
            qp.setPen(color)
            qp.setBrush(color)
            qp.drawEllipse(int(point.x), int(point.y), 3, 3)  # Уменьшение размера точек

        color = QColor(20, 20, 20)  # сделать точки оси красными
        qp.setPen(color)
        qp.setBrush(color)
        for point in self.axis_points:
            qp.drawEllipse(int(point.x), int(point.y), 5, 5)

        qp.setPen(QPen(color, 1, Qt.PenStyle.DotLine))  # Отрисовка пунктирных линий для осей
        qp.drawLine(int(self.axis_points[0].x), int(self.axis_points[0].y), int(self.intersection_point.x), int(self.intersection_point.y))
        qp.drawLine(int(self.axis_points[1].x), int(self.axis_points[1].y), int(self.intersection_point.x), int(self.intersection_point.y))

        color = QColor(255, 255, 0)  # сделать точку пересечения желтой
        qp.setPen(color)
        qp.setBrush(color)
        qp.drawEllipse(int(self.intersection_point.x), int(self.intersection_point.y), 5, 5)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slider_freq_x = QSlider(Qt.Orientation.Horizontal)
        self.slider_freq_x.setMinimum(0)
        self.slider_freq_x.setMaximum(20)  # Изменил максимальное значение на 20, чтобы разрешить половинные значения
        self.slider_freq_x.setTickInterval(1)
        self.slider_freq_x.valueChanged.connect(self.freq_changed)

        self.slider_freq_y = QSlider(Qt.Orientation.Vertical)
        self.slider_freq_y.setMinimum(0)
        self.slider_freq_y.setMaximum(20)  # Изменил максимальное значение на 20, чтобы разрешить половинные значения
        self.slider_freq_y.setTickInterval(1)
        self.slider_freq_y.valueChanged.connect(self.freq_changed)

        self.label_freq_x = QLabel()
        self.label_freq_y = QLabel()

        self.canvas = Canvas()

        self.layout = QGridLayout()
        self.layout.addWidget(self.slider_freq_x, 0, 0)
        self.layout.addWidget(self.label_freq_x, 1, 0)
        self.layout.addWidget(self.canvas, 2, 0)
        self.layout.addWidget(self.slider_freq_y, 2, 1)
        self.layout.addWidget(self.label_freq_y, 2, 2)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.x = 0
        self.y = 0

        self.timer = QTimer()
        self.timer.setInterval(1000 // 60)  # обновление со скоростью ~60 кадров в секунду
        self.timer.start()
        self.timer.timeout.connect(self.on_new_frame)

    def freq_changed(self):
        self.label_freq_x.setText(str(self.slider_freq_x.value() / 2.0))
        self.label_freq_y.setText(str(self.slider_freq_y.value() / 2.0))

    def on_new_frame(self):
        value_x = self.slider_freq_x.value() / 240.0  # Скорректированное значение деления для плавности
        value_y = self.slider_freq_y.value() / 240.0  # Скорректированное значение деления для плавности

        self.x += value_x
        self.y += value_y

        pos_x = 200 + 100 * math.sin(self.x)
        pos_y = 200 + 100 * math.cos(self.y)

        for _ in range(5):  # Теперь точки будут добавляться в более плотные кластеры
            self.canvas.add_point(pos_x, pos_y)

        self.canvas.update_axis_points(pos_x, pos_y)
        self.canvas.update()


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
