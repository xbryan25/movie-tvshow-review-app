from PyQt6.QtWidgets import QLabel


class Poster(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):
        print("clicked")
