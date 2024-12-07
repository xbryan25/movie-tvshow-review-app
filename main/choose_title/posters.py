from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation

from main.about_title.about_title import AboutTitlePage


# TODO: Finish pulsing animation whenever a poster gets hovered by the mouse

class Poster(QLabel):
    def __init__(self, parent, media_type):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = ""
        self.media_type = media_type

    def setTitle(self, title):
        self.title = title

    def setMediaId(self, media_id):
        self.media_id = media_id

    def mousePressEvent(self, event):
        print(self.title)
        self.about_title_page = AboutTitlePage(self.media_id, self.media_type)
        self.about_title_page.show()

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

