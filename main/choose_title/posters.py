from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation

# from about_title.about_title_movie import AboutTitleMoviePage
# from about_title.about_title_tv_show import AboutTitleTvShowPage

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests

# TODO: Finish pulsing animation whenever a poster gets hovered by the mouse

class Poster(QLabel):
    def __init__(self, parent, media_type, application_window):

        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = ""
        self.media_type = media_type

        self.application_window = application_window

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setTitle(self, title):
        self.title = title

    def setMediaId(self, media_id):
        self.media_id = media_id

    def mousePressEvent(self, event):
        self.application_window.change_to_about_specific_media_page(self.media_type, self.media_id)
