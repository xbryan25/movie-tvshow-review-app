from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QMainWindow, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize

from dialogs.operation_confirmation_dialog import OperationConfirmationDialog

from utils.clickable_frame import ClickableFrame

import sqlite3
import json
import requests


class LikedToWatchReviewedPageControls:
    def __init__(self, widgets, application_window):

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZ"
                             "iI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYX"
                             "BpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.widgets = widgets
        self.application_window = application_window

        self.account_id = None
        self.state_to_show = None
        self.requests_session_tmdb = None
        self.requests_session_images = None

        self.load_widgets()

        self.first_name = ""
        # self.get_first_name()

    def load_widgets(self):
        self.l_tw_r_header_label = self.widgets[0]
        self.l_tw_r_movies_label = self.widgets[1]
        self.l_tw_r_tv_shows_label = self.widgets[2]
        self.l_tw_r_movies_scroll_area = self.widgets[3]
        self.l_tw_r_tv_shows_scroll_area = self.widgets[4]
        self.l_tw_r_movies_scroll_area_contents = self.widgets[5]
        self.l_tw_r_tv_shows_scroll_area_contents = self.widgets[6]
        self.l_tw_r_movies_scroll_area_grid_layout = self.widgets[7]
        self.l_tw_r_tv_shows_scroll_area_grid_layout = self.widgets[8]

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_state_to_show(self, state_to_show):
        self.state_to_show = state_to_show

    def set_requests_session(self, requests_session_tmdb, requests_session_images):
        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

    def initialize_page(self):
        self.get_first_name()
        self.edit_window_title()

    def get_first_name(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        self.first_name = cursor.execute("""SELECT firstname FROM accounts WHERE account_id=(:account_id)""",
                                         {'account_id': self.account_id}).fetchone()[0]

        connection.commit()
        connection.close()

    def edit_window_title(self):

        if self.state_to_show == "liked":
            self.application_window.setWindowTitle(f"{self.first_name}'s Liked Media")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Liked Media")
        elif self.state_to_show == "to_watch":
            self.application_window.setWindowTitle(f"{self.first_name}'s Media to Watch")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Media to Watch")
        elif self.state_to_show == "reviewed":
            self.application_window.setWindowTitle(f"{self.first_name}'s Reviewed Media")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Reviewed Media")

    def clear_all_media(self):
        self.l_tw_r_movies_scroll_area.verticalScrollBar().setValue(0)
        self.l_tw_r_tv_shows_scroll_area.verticalScrollBar().setValue(0)

        l_tw_r_movies_scroll_area_children = (self.l_tw_r_movies_scroll_area.widget().
                                              findChildren(QFrame))

        l_tw_r_tv_shows_scroll_area_children = (self.l_tw_r_tv_shows_scroll_area.widget().
                                                findChildren(QFrame))

        # Delete the frames
        for l_tw_r_movies_scroll_area_child in l_tw_r_movies_scroll_area_children:
            l_tw_r_movies_scroll_area_child.deleteLater()

        for l_tw_r_tv_shows_scroll_area_child in l_tw_r_tv_shows_scroll_area_children:
            l_tw_r_tv_shows_scroll_area_child.deleteLater()

        # Delete the vertical spacers
        for i in range(self.l_tw_r_movies_scroll_area_grid_layout.count()):
            item = self.l_tw_r_movies_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.l_tw_r_movies_scroll_area_grid_layout.removeItem(item)
                break

        for i in range(self.l_tw_r_tv_shows_scroll_area_grid_layout.count()):
            item = self.l_tw_r_tv_shows_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.l_tw_r_tv_shows_scroll_area_grid_layout.removeItem(item)
                break

    def load_l_tw_r_media(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if self.state_to_show == "liked":
            l_tw_r_movies = json.loads(
                cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])
        elif self.state_to_show == "to_watch":
            l_tw_r_movies = json.loads(
                cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])
        else:
            l_tw_r_movies = json.loads(
                cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT tv_show_reviews FROM reviews WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

        # self.l_tw_r_movies_scroll_area_grid_layout.setColumnStretch(1, 1)

        # Pushes movie frames to the right
        left_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Minimum)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(left_v_spacer, 0, 0, 1, 1)

        # Pushes movie frames to the left
        right_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(right_v_spacer, 0, 2, 1, 1)

        count = 0

        for count, l_tw_r_movie in enumerate(l_tw_r_movies):
            movie_url = f"https://api.themoviedb.org/3/movie/{l_tw_r_movie}"
            movie_response = self.requests_session_tmdb.get(movie_url, headers=self.api_headers).json()

            movie_title = movie_response['title']
            movie_release_year = (movie_response['release_date'].split('-'))[0]
            movie_runtime = movie_response['runtime']
            movie_poster_path = movie_response['poster_path']

            self.l_tw_r_movie_frame = ClickableFrame(parent=self.l_tw_r_movies_scroll_area_contents)
            self.l_tw_r_movie_frame.setMinimumSize(QSize(360, 160))
            self.l_tw_r_movie_frame.setMaximumSize(QSize(550, 160))
            self.l_tw_r_movie_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.l_tw_r_movie_frame.setStyleSheet("background-color: rgb(13, 249, 249);")
            self.l_tw_r_movie_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.l_tw_r_movie_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.l_tw_r_movie_frame.setObjectName(f"l_tw_r_movie_{l_tw_r_movie}")

            self.l_tw_r_movie_frame.clicked.connect(lambda state, media_id=l_tw_r_movie:
                                                    self.application_window.change_to_about_specific_media_page("movie",
                                                                                                                media_id))

            self.l_tw_r_movie_grid_layout = QGridLayout(self.l_tw_r_movie_frame)
            self.l_tw_r_movie_grid_layout.setObjectName("l_tw_r_movie_grid_layout")

            self.movie_title_label = QLabel(parent=self.l_tw_r_movie_frame)
            self.movie_title_label.setMinimumSize(QSize(0, 30))
            self.movie_title_label.setMaximumSize(QSize(16777215, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_title_label.setFont(font)
            self.movie_title_label.setObjectName(f"movie_title_label_{l_tw_r_movie}")
            self.movie_title_label.setText(movie_title)
            self.l_tw_r_movie_grid_layout.addWidget(self.movie_title_label, 0, 2, 1, 2)

            self.movie_poster_label = QLabel(parent=self.l_tw_r_movie_frame)
            self.movie_poster_label.setMinimumSize(QSize(0, 138))
            self.movie_poster_label.setMaximumSize(QSize(92, 138))
            self.movie_poster_label.setText("")
            self.movie_poster_label.setScaledContents(True)
            self.movie_poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.movie_poster_label.setObjectName(f"movie_poster_{l_tw_r_movie}")
            self.movie_poster_label.setScaledContents(True)

            if not movie_poster_path:
                question_mark_image = QPixmap("../images/question_mark.jpg")

                self.movie_poster.setPixmap(question_mark_image)
            else:
                movie_img_url = 'https://image.tmdb.org/t/p/w92/' + movie_poster_path

                movie_image = QImage()
                movie_image.loadFromData(self.requests_session_images.get(movie_img_url).content)

                self.movie_poster_label.setPixmap(QPixmap(movie_image))

            self.movie_poster_label.setScaledContents(True)
            self.l_tw_r_movie_grid_layout.addWidget(self.movie_poster_label, 0, 0, 5, 1)

            self.movie_year_label = QLabel(parent=self.l_tw_r_movie_frame)
            self.movie_year_label.setMinimumSize(QSize(0, 30))
            self.movie_year_label.setMaximumSize(QSize(16777215, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_year_label.setFont(font)
            self.movie_year_label.setObjectName(f"movie_year_{l_tw_r_movie}")
            self.movie_year_label.setText(movie_release_year)
            self.l_tw_r_movie_grid_layout.addWidget(self.movie_year_label, 1, 2, 1, 2)

            self.movie_runtime_label = QLabel(parent=self.l_tw_r_movie_frame)
            self.movie_runtime_label.setMinimumSize(QSize(0, 30))
            self.movie_runtime_label.setMaximumSize(QSize(16777215, 30))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.movie_runtime_label.setFont(font)
            self.movie_runtime_label.setObjectName(f"movie_runtime_{l_tw_r_movie}")
            self.movie_runtime_label.setText(f"{movie_runtime} minutes")
            self.l_tw_r_movie_grid_layout.addWidget(self.movie_runtime_label, 2, 2, 1, 2)

            if self.state_to_show != "reviewed":
                self.remove_button_movie = QPushButton(parent=self.l_tw_r_movie_frame)
                font = QFont()
                font.setFamily("Oswald Medium")
                font.setPointSize(10)
                font.setBold(False)
                font.setWeight(50)
                self.remove_button_movie.setFont(font)
                self.remove_button_movie.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.remove_button_movie.setObjectName("remove_from_liked_movie")
                self.remove_button_movie.setText("Remove")

                self.remove_button_movie.clicked.connect(lambda state, frame=self.l_tw_r_movie_frame,
                                                                movie=l_tw_r_movie,
                                                                _l_tw_r_movies=l_tw_r_movies,
                                                                media_type="movie":
                                                         self.remove_media(frame, movie, _l_tw_r_movies,
                                                                           media_type))

                self.l_tw_r_movie_grid_layout.addWidget(self.remove_button_movie, 3, 2, 1, 2)

            poster_spacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Minimum)

            self.l_tw_r_movie_grid_layout.addItem(poster_spacer, 1, 1, 1, 1)

            self.l_tw_r_movies_scroll_area_grid_layout.addWidget(self.l_tw_r_movie_frame,
                                                                            count, 1, 1, 1)

        # Pushes movie frames up
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(spacerItem1,
                                                                      count + 1, 1, 1, 1)

        # -----------------------------------------------------------------------------------------------

        # Pushes tv_show frames to the right
        left_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Minimum)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(left_v_spacer,
                                                                        0, 0, 1, 1)

        # Pushes movie frames to the left
        right_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(right_v_spacer,
                                                                        0, 2, 1, 1)

        count = 0

        for count, l_tw_r_tv_show in enumerate(l_tw_r_tv_shows):
            tv_show_url = f"https://api.themoviedb.org/3/tv/{l_tw_r_tv_show}"
            tv_show_response = self.requests_session_tmdb.get(tv_show_url, headers=self.api_headers).json()

            tv_show_title = tv_show_response['name']
            tv_show_release_year = (tv_show_response['first_air_date'].split('-'))[0]
            tv_show_number_of_seasons = tv_show_response['number_of_seasons']
            tv_show_poster = tv_show_response['poster_path']

            self.l_tw_r_tv_show_frame = ClickableFrame(parent=self.l_tw_r_tv_shows_scroll_area_contents)
            self.l_tw_r_tv_show_frame.setMinimumSize(QSize(360, 160))
            self.l_tw_r_tv_show_frame.setMaximumSize(QSize(550, 160))
            self.l_tw_r_tv_show_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.l_tw_r_tv_show_frame.setStyleSheet("background-color: rgb(13, 249, 249);")
            self.l_tw_r_tv_show_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.l_tw_r_tv_show_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.l_tw_r_tv_show_frame.setObjectName(f"l_tw_r_tv_show_{l_tw_r_tv_show}")

            self.l_tw_r_tv_show_frame.clicked.connect(lambda state, media_id=l_tw_r_tv_show:
                                                      self.application_window.change_to_about_specific_media_page("tv",
                                                                                                                  media_id))

            self.l_tw_r_tv_show_grid_layout = QGridLayout(self.l_tw_r_tv_show_frame)
            self.l_tw_r_tv_show_grid_layout.setObjectName("l_tw_r_tv_show_grid_layout")

            self.tv_show_title_label = QLabel(parent=self.l_tw_r_tv_show_frame)
            self.tv_show_title_label.setMinimumSize(QSize(0, 30))
            self.tv_show_title_label.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_title_label.setFont(font)
            self.tv_show_title_label.setObjectName(f"tv_show_title_label_{l_tw_r_tv_show}")
            self.tv_show_title_label.setText(tv_show_title)
            self.l_tw_r_tv_show_grid_layout.addWidget(self.tv_show_title_label, 0, 2, 1, 2)

            self.tv_show_poster_label = QLabel(parent=self.l_tw_r_tv_show_frame)
            self.tv_show_poster_label.setMinimumSize(QSize(0, 138))
            self.tv_show_poster_label.setMaximumSize(QSize(92, 138))
            self.tv_show_poster_label.setText("")
            self.tv_show_poster_label.setScaledContents(True)
            self.tv_show_poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tv_show_poster_label.setObjectName(f"tv_show_poster_{l_tw_r_tv_show}")

            if not tv_show_poster:
                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.tv_show_poster_label.setPixmap(question_mark_image)

            else:
                tv_show_img_url = 'https://image.tmdb.org/t/p/w92' + tv_show_poster

                tv_show_image = QImage()
                tv_show_image.loadFromData(self.requests_session_images.get(tv_show_img_url).content)

                self.tv_show_poster_label.setPixmap(QPixmap(tv_show_image))
                self.tv_show_poster_label.setScaledContents(True)

            self.tv_show_poster_label.setScaledContents(True)
            self.l_tw_r_tv_show_grid_layout.addWidget(self.tv_show_poster_label, 0, 0, 5, 1)

            self.tv_show_year_label = QLabel(parent=self.l_tw_r_tv_show_frame)
            self.tv_show_year_label.setMinimumSize(QSize(0, 30))
            self.tv_show_year_label.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_year_label.setFont(font)
            self.tv_show_year_label.setObjectName("tv_show_year")
            self.tv_show_year_label.setText(tv_show_release_year)
            self.l_tw_r_tv_show_grid_layout.addWidget(self.tv_show_year_label, 1, 2, 1, 2)

            self.tv_show_seasons_label = QLabel(parent=self.l_tw_r_tv_show_frame)
            self.tv_show_seasons_label.setMinimumSize(QSize(0, 30))
            self.tv_show_seasons_label.setMaximumSize(QSize(200, 50))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.tv_show_seasons_label.setFont(font)
            self.tv_show_seasons_label.setObjectName(f"tv_show_seasons_{l_tw_r_tv_show}")
            self.tv_show_seasons_label.setText(f"{tv_show_number_of_seasons} seasons")
            self.l_tw_r_tv_show_grid_layout.addWidget(self.tv_show_seasons_label, 2, 2, 1, 2)

            if self.state_to_show != "reviewed":
                self.remove_button_tv_show = QPushButton(parent=self.l_tw_r_tv_show_frame)
                font = QFont()
                font.setFamily("Oswald Medium")
                font.setPointSize(10)
                self.remove_button_tv_show.setFont(font)
                self.remove_button_tv_show.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.remove_button_tv_show.setObjectName(f"remove_button_tv_show_{l_tw_r_tv_show}")
                self.remove_button_tv_show.setText("Remove")

                self.remove_button_tv_show.clicked.connect(lambda state, frame=self.l_tw_r_tv_show_frame,
                                                                  tv_show=l_tw_r_tv_show,
                                                                  _l_tw_r_tv_shows=l_tw_r_tv_shows,
                                                                  media_type="tv":
                                                           self.remove_media(frame, tv_show,
                                                                             _l_tw_r_tv_shows,
                                                                             media_type))

                self.l_tw_r_tv_show_grid_layout.addWidget(self.remove_button_tv_show, 3, 2, 1, 2)

            poster_spacer2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Minimum)

            self.l_tw_r_tv_show_grid_layout.addItem(poster_spacer2, 1, 1, 1, 1)

            self.l_tw_r_tv_shows_scroll_area_grid_layout.addWidget(self.l_tw_r_tv_show_frame,
                                                                              count, 1, 1, 1)

        # Pushes movie frames up
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(spacerItem2,
                                                                       count + 1, 1, 1, 1)

        connection.commit()
        connection.close()

    def remove_media(self, frame, media, media_list, media_type):
        self.confirmation_dialog = OperationConfirmationDialog(media_type, self.state_to_show)

        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_confirm_state():
            connection = sqlite3.connect('../database\\accounts.db')
            cursor = connection.cursor()

            self.rearrange_layout(frame, media_type)

            frame.hide()
            frame.deleteLater()

            media_list.remove(media)
            media_json = json.dumps(liked_media_list)

            if media_type == "movie":
                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                           {"liked_movies": media_json, "account_id": self.account_id})
            else:
                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": media_json, "account_id": self.account_id})

            connection.commit()
            connection.close()

    def rearrange_layout(self, frame, media_type):

        if media_type == "movie":
            # Make a shallow copy of the current children of the widget

            movie_frames = [child for child in
                            self.l_tw_r_movies_scroll_area.widget().findChildren(QFrame)
                            if type(child) is QFrame]

            # Remove v_spacer
            v_spacer = self.l_tw_r_movies_scroll_area_grid_layout.itemAtPosition(len(movie_frames) + 1, 1)
            self.l_tw_r_movies_scroll_area_grid_layout.removeItem(v_spacer)

            count = 0

            for movie_frame in movie_frames:
                # Transfer frames one row up
                self.l_tw_r_movies_scroll_area_grid_layout.removeWidget(movie_frame)

                if movie_frame != frame:

                    self.l_tw_r_movies_scroll_area_grid_layout.addWidget(movie_frame, count, 1, 1, 1)

                    count += 1

            # Add v_spacer again
            v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding)
            self.l_tw_r_movies_scroll_area_grid_layout.addItem(v_spacer, count + 1, 1, 1, 1)

        elif media_type == "tv":
            # Make a shallow copy of the current children of the widget

            tv_show_frames = [child for child in
                              self.l_tw_r_tv_shows_scroll_area.widget().findChildren(QFrame)
                              if type(child) is QFrame]

            # Remove v_spacer
            v_spacer = self.l_tw_r_tv_shows_scroll_area_grid_layout.itemAtPosition(len(tv_show_frames) + 1, 1)
            self.l_tw_r_tv_shows_scroll_area_grid_layout.removeItem(v_spacer)

            count = 0

            for tv_show_frame in tv_show_frames:
                # Transfer frames one row up
                self.l_tw_r_tv_shows_scroll_area_grid_layout.removeWidget(tv_show_frame)

                if tv_show_frame != frame:
                    self.l_tw_r_tv_shows_scroll_area_grid_layout.addWidget(tv_show_frame, count, 1, 1, 1)

                    count += 1

            # Add v_spacer again
            v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(v_spacer, count + 1, 1, 1, 1)

