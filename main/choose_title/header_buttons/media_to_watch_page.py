from choose_title.header_buttons.lm_mtw_design import Ui_MainWindow as MediaToWatchUI

from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QMainWindow, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize

import sqlite3
import json
import requests


class MediaToWatchPage(QMainWindow, MediaToWatchUI):
    def __init__(self, account_id):
        super().__init__()

        self.setupUi(self)

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.first_name = ''
        self.account_id = account_id

        self.get_first_name()
        self.edit_window_title()

        self.load_media_to_watch()

    def get_first_name(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        self.first_name = cursor.execute("""SELECT firstname FROM accounts WHERE account_id=(:account_id)""",
                                         {'account_id': self.account_id}).fetchone()[0]

        connection.commit()
        connection.close()

    def edit_window_title(self):
        self.setWindowTitle(f"{self.first_name}'s Media to Watch")
        self.header_label.setText(f"{self.first_name}'s Media to Watch")

    def load_media_to_watch(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movies_to_watch = json.loads(
            cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                                         {'account_id': self.account_id}).fetchone()[0])

        tv_shows_to_watch = json.loads(
            cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                           {'account_id': self.account_id}).fetchone()[0])

        for movie_to_watch in movies_to_watch:
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_to_watch}"
            movie_response = requests.get(movie_url, headers=self.api_headers).json()

            movie_title = movie_response['title']
            movie_release_year = (movie_response['release_date'].split('-'))[0]
            movie_poster_path = movie_response['poster_path']

            self.movie_to_watch_frame = QFrame(parent=self.movie_scroll_area_contents)
            self.movie_to_watch_frame.setMinimumSize(QSize(0, 160))
            self.movie_to_watch_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.movie_to_watch_frame.setStyleSheet("background-color: rgb(13, 249, 249);")
            self.movie_to_watch_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.movie_to_watch_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.movie_to_watch_frame.setObjectName("movie_to_watch_frame")

            self.gridLayout = QGridLayout(self.movie_to_watch_frame)
            self.gridLayout.setObjectName("gridLayout")

            self.movie_title = QLabel(parent=self.movie_to_watch_frame)
            self.movie_title.setMinimumSize(QSize(0, 30))
            self.movie_title.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_title.setFont(font)
            self.movie_title.setObjectName("movie_title")
            self.movie_title.setText(movie_title)
            self.gridLayout.addWidget(self.movie_title, 0, 2, 1, 2)

            self.movie_poster = QLabel(parent=self.movie_to_watch_frame)
            self.movie_poster.setMinimumSize(QSize(0, 138))
            self.movie_poster.setMaximumSize(QSize(92, 138))
            self.movie_poster.setText("")
            self.movie_poster.setScaledContents(True)
            self.movie_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.movie_poster.setObjectName("movie_poster")
            self.movie_poster.setScaledContents(True)

            if not movie_poster_path:
                question_mark_image = QPixmap("../images/question_mark.jpg")
                #
                self.movie_poster.setPixmap(question_mark_image)
            else:
                movie_img_url = 'https://image.tmdb.org/t/p/w92/' + movie_poster_path

                movie_image = QImage()
                movie_image.loadFromData(requests.get(movie_img_url).content)

                self.movie_poster.setPixmap(QPixmap(movie_image))

            self.movie_poster.setScaledContents(True)
            self.gridLayout.addWidget(self.movie_poster, 0, 0, 5, 1)

            self.movie_runtime = QLabel(parent=self.movie_to_watch_frame)
            self.movie_runtime.setMinimumSize(QSize(0, 30))
            self.movie_runtime.setMaximumSize(QSize(16777215, 30))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_runtime.setFont(font)
            self.movie_runtime.setObjectName("movie_runtime")
            self.gridLayout.addWidget(self.movie_runtime, 2, 2, 1, 2)

            self.movie_year = QLabel(parent=self.movie_to_watch_frame)
            self.movie_year.setMinimumSize(QSize(0, 30))
            self.movie_year.setMaximumSize(QSize(16777215, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_year.setFont(font)
            self.movie_year.setObjectName("movie_year")
            self.movie_year.setText(movie_release_year)
            self.gridLayout.addWidget(self.movie_year, 1, 2, 1, 2)

            self.remove_from_movie_to_watch = QPushButton(parent=self.movie_to_watch_frame)
            font = QFont()
            font.setFamily("Oswald Medium")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.remove_from_movie_to_watch.setFont(font)
            self.remove_from_movie_to_watch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.remove_from_movie_to_watch.setObjectName("remove_from_movie_to_watch")
            self.remove_from_movie_to_watch.setText("Remove")
            self.remove_from_movie_to_watch.clicked.connect(lambda state, frame=self.movie_to_watch_frame,
                                                            movie=movie_to_watch, _movies_to_watch=movies_to_watch,
                                                            media_type="movie":
                                                            self.remove_media_to_watch(frame, movie,
                                                                                       _movies_to_watch,
                                                                                       media_type))
            self.gridLayout.addWidget(self.remove_from_movie_to_watch, 3, 2, 1, 2)

            poster_spacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Minimum)
            self.gridLayout.addItem(poster_spacer, 1, 1, 1, 1)

            self.verticalLayout_4.addWidget(self.movie_to_watch_frame)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)

        for tv_show_to_watch in tv_shows_to_watch:
            tv_show_url = f"https://api.themoviedb.org/3/tv/{tv_show_to_watch}"
            tv_show_response = requests.get(tv_show_url, headers=self.api_headers).json()

            tv_show_title = tv_show_response['name']
            tv_show_release_year = (tv_show_response['first_air_date'].split('-'))[0]
            tv_show_poster = tv_show_response['poster_path']

            self.tv_show_to_watch_frame = QFrame(parent=self.tv_show_scroll_area_contents)
            self.tv_show_to_watch_frame.setMinimumSize(QSize(0, 160))
            self.tv_show_to_watch_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.tv_show_to_watch_frame.setStyleSheet("background-color: rgb(13, 249, 249);")
            self.tv_show_to_watch_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.tv_show_to_watch_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.tv_show_to_watch_frame.setObjectName("tv_show_to_watch_frame")

            self.gridLayout2 = QGridLayout(self.tv_show_to_watch_frame)
            self.gridLayout2.setObjectName("gridLayout2")

            self.tv_show_title = QLabel(parent=self.tv_show_to_watch_frame)
            self.tv_show_title.setMinimumSize(QSize(0, 30))
            self.tv_show_title.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_title.setFont(font)
            self.tv_show_title.setObjectName("tv_show_title")
            self.tv_show_title.setText(tv_show_title)
            self.gridLayout2.addWidget(self.tv_show_title, 0, 2, 1, 2)

            self.tv_show_poster = QLabel(parent=self.tv_show_to_watch_frame)
            self.tv_show_poster.setMinimumSize(QSize(0, 138))
            self.tv_show_poster.setMaximumSize(QSize(92, 138))
            self.tv_show_poster.setText("")
            self.tv_show_poster.setScaledContents(True)
            self.tv_show_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tv_show_poster.setObjectName("tv_show_poster")

            if not tv_show_poster:
                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.tv_show_poster.setPixmap(question_mark_image)

            else:
                tv_show_img_url = 'https://image.tmdb.org/t/p/w92' + tv_show_poster

                tv_show_image = QImage()
                tv_show_image.loadFromData(requests.get(tv_show_img_url).content)

                self.tv_show_poster.setPixmap(QPixmap(tv_show_image))
                self.tv_show_poster.setScaledContents(True)

            self.tv_show_poster.setScaledContents(True)
            self.gridLayout2.addWidget(self.tv_show_poster, 0, 0, 5, 1)

            self.tv_show_seasons = QLabel(parent=self.tv_show_to_watch_frame)
            self.tv_show_seasons.setMinimumSize(QSize(0, 30))
            self.tv_show_seasons.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_seasons.setFont(font)
            self.tv_show_seasons.setObjectName("tv_show_seasons")
            self.gridLayout2.addWidget(self.tv_show_seasons, 2, 2, 1, 2)

            self.tv_show_year = QLabel(parent=self.tv_show_to_watch_frame)
            self.tv_show_year.setMinimumSize(QSize(0, 30))
            self.tv_show_year.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_year.setFont(font)
            self.tv_show_year.setObjectName("tv_show_year")
            self.tv_show_year.setText(tv_show_release_year)
            self.gridLayout2.addWidget(self.tv_show_year, 1, 2, 1, 2)

            self.remove_from_tv_show_to_watch = QPushButton(parent=self.tv_show_to_watch_frame)
            font = QFont()
            font.setFamily("Oswald Medium")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.remove_from_tv_show_to_watch.setFont(font)
            self.remove_from_tv_show_to_watch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.remove_from_tv_show_to_watch.setObjectName("remove_from_tv_show_to_watch")
            self.remove_from_tv_show_to_watch.setText("Remove")
            self.remove_from_tv_show_to_watch.clicked.connect(lambda state, frame=self.tv_show_to_watch_frame,
                                                              tv_show=tv_show_to_watch,
                                                              _tv_shows_to_watch=tv_shows_to_watch,
                                                              media_type="tv":
                                                              self.remove_media_to_watch(frame, tv_show,
                                                                                         _tv_shows_to_watch,
                                                                                         media_type))

            # self.remove_from_tv_show_to_watch.clicked.connect(self.tv_show_to_watch_frame.close)
            self.gridLayout2.addWidget(self.remove_from_tv_show_to_watch, 3, 2, 1, 2)

            poster_spacer2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Minimum)

            self.gridLayout2.addItem(poster_spacer2, 1, 1, 1, 1)

            self.verticalLayout_5.addWidget(self.tv_show_to_watch_frame)

        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)

        connection.commit()
        connection.close()

    def remove_media_to_watch(self, frame, media, media_to_watch_list, media_type):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        frame.close()

        media_to_watch_list.remove(media)
        media_to_watch_list_json = json.dumps(media_to_watch_list)

        if media_type == "movie":
            cursor.execute("""UPDATE media_to_watch SET movies_to_watch=(:movies_to_watch) WHERE account_id=(:account_id)""",
                       {"movies_to_watch": media_to_watch_list_json, "account_id": self.account_id})
        else:
            cursor.execute("""UPDATE media_to_watch SET tv_shows_to_watch=(:tv_shows_to_watch) WHERE account_id=(:account_id)""",
                           {"tv_shows_to_watch": media_to_watch_list_json, "account_id": self.account_id})

        connection.commit()
        connection.close()
