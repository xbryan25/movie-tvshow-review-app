from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect, QPropertyAnimation, QSize

# from about_title.about_title_movie import AboutTitleMoviePage
# from about_title.about_title_tv_show import AboutTitleTvShowPage

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests

# TODO: Finish pulsing animation whenever a poster gets hovered by the mouse


class Poster(QLabel):
    def __init__(self, parent, media_type, application_window, frame_name):

        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = ""
        self.media_type = media_type
        self.frame_name = frame_name

        self.application_window = application_window

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setMinimumSize(QSize(165, 225))
        self.setMaximumSize(QSize(165, 270))

        self.setText("")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(frame_name)
        self.setScaledContents(True)
        self.setObjectName(self.frame_name)

        self.setStyleSheet("QLabel{\n"
                           "padding: 3px 3px 3px 3px;\n"
                           "}\n"
                           "\n"
                           "QLabel:hover{\n"
                           "border: 5px solid rgb(255, 166, 54);\n"
                           "border-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "")


    def setTitle(self, title):
        self.title = title

    def setMediaId(self, media_id):
        self.media_id = media_id

    def mousePressEvent(self, event):
        self.application_window.change_to_about_specific_media_page(self.media_type, self.media_id)
