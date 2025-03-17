
from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QMainWindow, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize, QDate

import sqlite3
import json


class MembersPageControls:
    def __init__(self, widgets, application_window):
        self.widgets = widgets
        self.application_window = application_window

        self.account_id = None

        self.current_date = QDate.currentDate().toString('MMMM d, yyyy')

        self.load_widgets()

    def load_widgets(self):
        self.members_label = self.widgets[0]
        self.total_member_count_label = self.widgets[1]
        self.members_scroll_area = self.widgets[2]
        self.members_scroll_area_contents = self.widgets[3]
        self.members_scroll_area_contents_grid_layout = self.widgets[4]

    def load_members(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        members_info = {}

        members_tuples_list = cursor.execute("""SELECT account_id, username, firstname, lastname FROM accounts""").fetchall()

        for member_tuple in members_tuples_list:
            members_info.update({member_tuple[0]: {'username': member_tuple[1],
                                                   'fullname': f"{member_tuple[2]} {member_tuple[3]}",
                                                   'liked_media':  self.get_number_of_liked_media(cursor,
                                                                                                  member_tuple[0]),
                                                   'media_to_watch': self.get_number_of_to_watch_media(cursor,
                                                                                                       member_tuple[0]),
                                                   'reviewed_media': self.get_number_of_reviewed_media(cursor,
                                                                                                       member_tuple[0])
                                                   }})

        member_count = len(members_info)

        self.total_member_count_label.setText(f"Total member count as of {self.current_date}: {member_count}")

        # Pushes movie frames to the right
        left_h_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Minimum)

        self.members_scroll_area_contents_grid_layout.addItem(left_h_spacer, 0, 0, 1, 1)

        # Pushes movie frames to the left
        right_h_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self.members_scroll_area_contents_grid_layout.addItem(right_h_spacer, 0, 2, 1, 1)

        count = 0

        for count, member_info in enumerate(members_info.values()):
            self.member_frame = QFrame(parent=self.members_scroll_area_contents)
            self.member_frame.setMinimumSize(QSize(650, 180))
            self.member_frame.setMaximumSize(QSize(650, 180))
            self.member_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.member_frame.setStyleSheet("background-color: rgb(170, 255, 255);")
            self.member_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.member_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.member_frame.setObjectName(f"member_frame_{member_info['username']}")

            self.gridLayout = QGridLayout(self.member_frame)
            self.gridLayout.setVerticalSpacing(6)
            self.gridLayout.setObjectName("gridLayout")

            self.profile_picture = QLabel(parent=self.member_frame)
            self.profile_picture.setMinimumSize(QSize(160, 160))
            self.profile_picture.setMaximumSize(QSize(160, 160))
            self.profile_picture.setStyleSheet("background-color: red;\n"
                                               "border-radius: 80px;")
            self.profile_picture.setText("")
            self.profile_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.profile_picture.setObjectName("profile_picture")
            self.gridLayout.addWidget(self.profile_picture, 0, 0, 6, 1)

            self.username = QLabel(parent=self.member_frame)
            self.username.setMinimumHeight(66)
            font = QFont()
            font.setFamily("Oswald Medium")
            font.setPointSize(28)
            self.username.setFont(font)
            self.username.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.username.setToolTip("")
            self.username.setToolTipDuration(-1)
            self.username.setAutoFillBackground(False)
            self.username.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.username.setWordWrap(False)
            self.username.setObjectName("username")
            self.username.setText(f"{member_info['username']}")
            # self.username.setStyleSheet("background-color: rgb(170, 0, 255);")
            self.gridLayout.addWidget(self.username, 0, 2, 2, 8)

            self.firstname_lastname = QLabel(parent=self.member_frame)
            self.firstname_lastname.setMaximumHeight(30)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(15)
            self.firstname_lastname.setFont(font)
            self.firstname_lastname.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.firstname_lastname.setObjectName("firstname_lastname")
            self.firstname_lastname.setText(f"{member_info['fullname']}")
            # self.firstname_lastname.setStyleSheet("background-color: rgb(170, 50, 255);")
            self.gridLayout.addWidget(self.firstname_lastname, 2, 2, 2, 8)

            self.num_of_likes = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_likes.setFont(font)
            self.num_of_likes.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_likes.setObjectName("num_of_likes")
            self.num_of_likes.setText(f"{member_info['liked_media'][0] + member_info['liked_media'][1]} likes")
            self.gridLayout.addWidget(self.num_of_likes, 4, 2, 1, 2)

            self.num_of_likes_movie = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_likes_movie.setFont(font)
            self.num_of_likes_movie.setObjectName("num_of_likes_movie")
            self.num_of_likes_movie.setText(f"Movies: {member_info['liked_media'][0]}")
            self.gridLayout.addWidget(self.num_of_likes_movie, 5, 2, 1, 1)

            self.num_of_likes_tv_show = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_likes_tv_show.setFont(font)
            self.num_of_likes_tv_show.setObjectName("num_of_likes_tv_show")
            self.num_of_likes_tv_show.setText(f"TV shows: {member_info['liked_media'][1]}")
            self.gridLayout.addWidget(self.num_of_likes_tv_show, 5, 3, 1, 1)

            self.line = QFrame(parent=self.member_frame)
            self.line.setFrameShadow(QFrame.Shadow.Plain)
            self.line.setLineWidth(1)
            self.line.setMidLineWidth(0)
            self.line.setFrameShape(QFrame.Shape.VLine)
            self.line.setObjectName("line")
            self.gridLayout.addWidget(self.line, 4, 4, 2, 1)

            self.num_of_media_to_watch = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_media_to_watch.setFont(font)
            self.num_of_media_to_watch.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_media_to_watch.setObjectName("num_of_media_to_watch")
            self.num_of_media_to_watch.setText(f"{member_info['media_to_watch'][0] + member_info['media_to_watch'][1]} "
                                               f"media to watch")
            self.gridLayout.addWidget(self.num_of_media_to_watch, 4, 5, 1, 2)

            self.num_of_media_to_watch_movie = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_media_to_watch_movie.setFont(font)
            self.num_of_media_to_watch_movie.setObjectName("num_of_media_to_watch_movie")
            self.num_of_media_to_watch_movie.setText(f"Movies: {member_info['media_to_watch'][0]}")
            self.gridLayout.addWidget(self.num_of_media_to_watch_movie, 5, 5, 1, 1)

            self.num_of_media_to_watch_tv_show = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_media_to_watch_tv_show.setFont(font)
            self.num_of_media_to_watch_tv_show.setObjectName("num_of_media_to_watch_tv_show")
            self.num_of_media_to_watch_tv_show.setText(f"TV Shows: {member_info['media_to_watch'][1]}")
            self.gridLayout.addWidget(self.num_of_media_to_watch_tv_show, 5, 6, 1, 1)

            self.line_2 = QFrame(parent=self.member_frame)
            self.line_2.setFrameShadow(QFrame.Shadow.Plain)
            self.line_2.setLineWidth(1)
            self.line_2.setMidLineWidth(0)
            self.line_2.setFrameShape(QFrame.Shape.VLine)
            self.line_2.setObjectName("line_2")
            self.gridLayout.addWidget(self.line_2, 4, 7, 2, 1)

            self.num_of_reviews = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_reviews.setFont(font)
            self.num_of_reviews.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_reviews.setObjectName("num_of_reviews")
            self.num_of_reviews.setText(f"{member_info['reviewed_media'][0] + member_info['reviewed_media'][1]} "
                                        f"reviews")

            self.gridLayout.addWidget(self.num_of_reviews, 4, 8, 1, 2)

            self.num_of_reviews_movie = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_reviews_movie.setFont(font)
            self.num_of_reviews_movie.setObjectName("num_of_reviews_movie")
            self.num_of_reviews_movie.setText(f"Movies: {member_info['reviewed_media'][0]}")
            self.gridLayout.addWidget(self.num_of_reviews_movie, 5, 8, 1, 1)

            self.num_of_reviews_tv_show = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.num_of_reviews_tv_show.setFont(font)
            self.num_of_reviews_tv_show.setObjectName("num_of_reviews_tv_show")
            self.num_of_reviews_tv_show.setText(f"TV Shows: {member_info['reviewed_media'][1]}")
            self.gridLayout.addWidget(self.num_of_reviews_tv_show, 5, 9, 1, 1)

            profile_pic_h_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed,
                                               QSizePolicy.Policy.Minimum)
            self.gridLayout.addItem(profile_pic_h_spacer, 4, 1, 1, 1)

            self.members_scroll_area_contents_grid_layout.addWidget(self.member_frame, count, 1, 1, 1)

        # Pushes movie frames up
        bottom_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.members_scroll_area_contents_grid_layout.addItem(bottom_v_spacer, count + 1, 1, 1, 1)

        connection.commit()
        connection.close()

    @staticmethod
    def get_number_of_liked_media(cursor, account_id):
        num_of_liked_movies = len(
            json.loads(cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        num_of_liked_tv_shows = len(
            json.loads(cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return [num_of_liked_movies, num_of_liked_tv_shows]

    @staticmethod
    def get_number_of_to_watch_media(cursor, account_id):
        num_of_movies_to_watch = len(
            json.loads(cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                                       {"account_id": account_id}).fetchone()[0]))

        num_of_tv_shows_to_watch = len(
            json.loads(cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return [num_of_movies_to_watch, num_of_tv_shows_to_watch]

    @staticmethod
    def get_number_of_reviewed_media(cursor, account_id):
        num_of_reviewed_movies = len(
            json.loads(cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        num_of_reviewed_tv_shows = len(
            json.loads(cursor.execute("""SELECT tv_show_reviews FROM reviews WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return [num_of_reviewed_movies, num_of_reviewed_tv_shows]
