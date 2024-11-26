from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation

class Poster(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):
        print("clicked")

    def mouseMoveEvent(self, ev):
        pass

    def resize_animation(self):
        pass
