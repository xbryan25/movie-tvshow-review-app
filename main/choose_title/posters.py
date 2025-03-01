from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation

from about_title.about_title_movie import AboutTitleMoviePage
from about_title.about_title_tv_show import AboutTitleTvShowPage

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests

# TODO: Finish pulsing animation whenever a poster gets hovered by the mouse

class Poster(QLabel):
    def __init__(self, parent, media_type, account_id, requests_session_tmdb, requests_session_images):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = ""
        self.media_type = media_type
        self.account_id = account_id

        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setTitle(self, title):
        self.title = title

    def setMediaId(self, media_id):
        self.media_id = media_id

    def mousePressEvent(self, event):
        # print(self.title)

        if self.media_type == "movie":
            self.about_title_movie_page = AboutTitleMoviePage(self.media_id, self.account_id,
                                                              self.requests_session_tmdb,
                                                              self.requests_session_images)
            self.about_title_movie_page.show()
        else:
            self.about_title_tv_show_page = AboutTitleTvShowPage(self.media_id, self.account_id,
                                                                 self.requests_session_tmdb,
                                                                 self.requests_session_images)
            self.about_title_tv_show_page.show()

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

