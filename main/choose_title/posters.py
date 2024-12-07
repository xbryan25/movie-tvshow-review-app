from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation

# TODO: Finish pulsing animation whenever a poster gets hovered by the mouse

class Poster(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""

    def setTitle(self, title):
        self.title = title

    def mousePressEvent(self, event):
        print(self.title)

    def mouseMoveEvent(self, ev):
        pass

    def resize_animation(self):
        pass
        # self.animation = QPropertyAnimation(self, b'geometry')
        # self.animation.setDuration(100)
        #
        # if self.width() == 150:
        #     self.animation.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
        #     self.animation.setEndValue(QRect(self.x(), self.y(), 200, self.height()))
        #     self.animation.start()
        #
        # elif self.width() == 200:
        #     self.animation.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
        #     self.animation.setEndValue(QRect(self.x(), self.y(), 150, self.height()))
        #     self.animation.start()
        #
        #
        #
        # print(self.width())

