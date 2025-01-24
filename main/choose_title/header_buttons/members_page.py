from main.choose_title.header_buttons.members_design import Ui_MainWindow as MembersPageUI

from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QMainWindow, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize, QDate

import sqlite3
import json


class MembersPage(QMainWindow, MembersPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.current_date = QDate.currentDate().toString('MMMM d, yyyy')

        self.load_members()


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

        for member_info in members_info.values():
            self.member_frame = QFrame(parent=self.members_scroll_area_contents)
            self.member_frame.setMinimumSize(QSize(340, 135))
            self.member_frame.setMaximumSize(QSize(360, 135))
            self.member_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.member_frame.setStyleSheet("background-color: rgb(170, 255, 255);")
            self.member_frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.member_frame.setFrameShadow(QFrame.Shadow.Raised)
            self.member_frame.setObjectName("member_frame")

            self.gridLayout = QGridLayout(self.member_frame)
            self.gridLayout.setVerticalSpacing(6)
            self.gridLayout.setObjectName("gridLayout")

            self.num_of_likes = QLabel(parent=self.member_frame)
            self.num_of_likes.setMaximumSize(QSize(100, 16777215))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_likes.setFont(font)
            self.num_of_likes.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_likes.setObjectName("num_of_likes")
            self.num_of_likes.setText(f"{member_info['liked_media']} likes")
            self.gridLayout.addWidget(self.num_of_likes, 3, 0, 1, 1)

            self.num_of_media_to_watch = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_media_to_watch.setFont(font)
            self.num_of_media_to_watch.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_media_to_watch.setObjectName("num_of_media_to_watch")
            self.num_of_media_to_watch.setText(f"{member_info['media_to_watch']} media to watch")
            self.gridLayout.addWidget(self.num_of_media_to_watch, 3, 1, 1, 1)

            self.num_of_reviews = QLabel(parent=self.member_frame)
            self.num_of_reviews.setMaximumSize(QSize(100, 16777215))
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(11)
            self.num_of_reviews.setFont(font)
            self.num_of_reviews.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.num_of_reviews.setObjectName("num_of_reviews")
            self.num_of_reviews.setText(f"{member_info['reviewed_media']} reviews")
            self.gridLayout.addWidget(self.num_of_reviews, 3, 2, 1, 1)

            self.firstname_lastname = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(14)
            self.firstname_lastname.setFont(font)
            self.firstname_lastname.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.firstname_lastname.setObjectName("firstname_lastname")
            self.firstname_lastname.setText(f"{member_info['fullname']}")
            self.gridLayout.addWidget(self.firstname_lastname, 1, 0, 1, 3)

            self.username = QLabel(parent=self.member_frame)
            font = QFont()
            font.setFamily("Oswald Medium")
            font.setPointSize(20)
            self.username.setFont(font)
            self.username.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.username.setToolTip("")
            self.username.setToolTipDuration(-1)
            self.username.setAutoFillBackground(False)
            self.username.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.username.setWordWrap(False)
            self.username.setObjectName("username")
            self.username.setText(f"{member_info['username']}")
            self.gridLayout.addWidget(self.username, 0, 0, 1, 3)

            self.verticalLayout_3.addWidget(self.member_frame)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

    @staticmethod
    def get_number_of_liked_media(cursor, account_id):
        num_of_liked_movies = len(
            json.loads(cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        num_of_liked_tv_shows = len(
            json.loads(cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return num_of_liked_tv_shows + num_of_liked_movies

    @staticmethod
    def get_number_of_to_watch_media(cursor, account_id):
        num_of_movies_to_watch = len(
            json.loads(cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                                       {"account_id": account_id}).fetchone()[0]))

        num_of_tv_shows_to_watch = len(
            json.loads(cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return num_of_movies_to_watch + num_of_tv_shows_to_watch

    @staticmethod
    def get_number_of_reviewed_media(cursor, account_id):
        num_of_reviewed_movies = len(
            json.loads(cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        num_of_reviewed_tv_shows = len(
            json.loads(cursor.execute("""SELECT tv_show_reviews FROM reviews WHERE account_id=(:account_id)""",
                                      {"account_id": account_id}).fetchone()[0]))

        return num_of_reviewed_movies + num_of_reviewed_tv_shows
