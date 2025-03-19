

# from choose_title.header_buttons.liked_media_page import LikedMediaPage
# from choose_title.header_buttons.media_to_watch_page import MediaToWatchPage
# from choose_title.header_buttons.members_page import MembersPage

from choose_title.logout_confirmation_dialog import LogoutConfirmationDialog

from choose_title.posters import Poster

from PyQt6.QtWidgets import QMainWindow, QLabel, QFrame, QDialogButtonBox
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import (QSize, Qt, QPropertyAnimation, QRect, QEvent, QThread, QObject, pyqtSignal, QRunnable,
                          pyqtSlot, QThreadPool)

from loading_screen.loading_screen import LoadingScreen

# from search_results.search_results_page import SearchResultsPage

from utils.load_pictures_worker import LoadPicturesWorker

import sqlite3
import re
import urllib

import threading
import sys
import traceback

import aiohttp
import asyncio

import time


class ChooseTitlesPageControls:
    def __init__(self, widgets, application_window):
        self.widgets = widgets
        self.application_window = application_window

        self.account_id = None
        self.api_client = None

        self.load_widgets()
        self.add_signals()

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_api_client(self, api_client):
        self.api_client = api_client

    def start_process(self):
        for i in range(20):
            self.make_more_movie_posters(i)
            self.make_more_tv_show_posters(i)

        self.loading_screen = LoadingScreen()
        self.loading_screen.show()

        self.threadpool = QThreadPool()
        self.start_load_pictures_thread()

    def open_liked_media_page(self):
        self.liked_media_page = LikedMediaPage(self.account_id)
        self.liked_media_page.show()

    def open_media_to_watch_page(self):
        self.media_to_watch_page = MediaToWatchPage(self.account_id)
        self.media_to_watch_page.show()

    def open_members_page(self):
        self.members_page = MembersPage()
        self.members_page.show()

    def load_widgets(self):
        self.search_title_line_edit = self.widgets[0]
        self.liked_button = self.widgets[1]
        self.to_watch_button = self.widgets[2]
        self.members_button = self.widgets[3]
        self.logout_button = self.widgets[4]
        self.popular_movies_scroll_area_contents = self.widgets[5]
        self.popular_movies_scroll_area_grid_layout = self.widgets[6]
        self.popular_tv_shows_scroll_area_contents = self.widgets[7]
        self.popular_tv_shows_scroll_area_grid_layout = self.widgets[8]

    def add_signals(self):
        # self.liked_button.clicked.connect(self.open_liked_media_page)
        # self.to_watch_button.clicked.connect(self.open_media_to_watch_page)
        # self.members_button.clicked.connect(self.open_members_page)
        self.logout_button.clicked.connect(self.logout_account)

    def logout_account(self):

        self.logout_confirmation_dialog = LogoutConfirmationDialog(self.application_window)

        print(self.logout_confirmation_dialog)

        self.logout_confirmation_dialog.exec()

    def start_load_pictures_thread(self):
        self.application_window.hide()

        load_pictures_worker = LoadPicturesWorker(self.load_pictures, self.api_client)

        load_pictures_worker.signals.finished.connect(self.show_choose_titles_page)

        self.threadpool.start(load_pictures_worker)

    async def load_pictures(self):

        # await self.api_client.start_session()
        popular_movies_api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        popular_movies_api_response = await self.api_client.fetch(popular_movies_api_url)

        popular_tv_shows_api_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
        popular_tv_shows_api_response = await self.api_client.fetch(popular_tv_shows_api_url)

        # Find the children of the Poster class
        movie_poster_containers = self.popular_movies_scroll_area_contents.findChildren(Poster)
        tv_show_poster_containers = self.popular_tv_shows_scroll_area_contents.findChildren(Poster)


        movie_img_urls = []
        tv_show_img_urls = []

        # Set up Poster details
        for i in range(20):
            movie_img_url = ""

            if popular_movies_api_response['results'][i]['poster_path']:
                movie_img_url = 'https://image.tmdb.org/t/p/w342/' + popular_movies_api_response['results'][i][
                    'poster_path']

            movie_img_urls.append(movie_img_url)

            movie_id = popular_movies_api_response['results'][i]['id']
            movie_poster_containers[i].setMediaId(movie_id)

            movie_poster_containers[i].show()

            # TMDB poster download sizes
            # https://www.themoviedb.org/talk/5ee4ba52a217c0001fd0cb83

            tv_show_img_url = ""

            if popular_tv_shows_api_response['results'][i]['poster_path']:
                tv_show_img_url = ('https://image.tmdb.org/t/p/w342/' +
                                   popular_tv_shows_api_response['results'][i]['poster_path'])

            tv_show_img_urls.append(tv_show_img_url)

            tv_show_id = popular_tv_shows_api_response['results'][i]['id']
            tv_show_poster_containers[i].setMediaId(tv_show_id)

            tv_show_poster_containers[i].show()

        # Fetch data from TMDB
        movie_img_data = await self.api_client.fetch_all_images(movie_img_urls, self.loading_screen.loading_progress_bar, 0, 40)
        tv_show_img_data = await self.api_client.fetch_all_images(tv_show_img_urls, self.loading_screen.loading_progress_bar, 21, 40)

        # Load image data to Posters
        for j in range(20):
            if movie_img_data[j] != '':

                movie_image = QImage()
                movie_image.loadFromData(movie_img_data[j])

                movie_poster_containers[j].setPixmap(QPixmap(movie_image))

            if tv_show_img_data[j] != '':

                tv_show_image = QImage()
                tv_show_image.loadFromData(tv_show_img_data[j])

                tv_show_poster_containers[j].setPixmap(QPixmap(tv_show_image))

        print("Done!")

        # await self.api_client.close_session()

    def show_choose_titles_page(self):
        self.loading_screen.close()
        self.application_window.show()

    def make_more_movie_posters(self, column):
        frame_name = "movie_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label = Poster(parent=self.popular_movies_scroll_area_contents, media_type="movie",
                            application_window=self.application_window)
        self.label.setMinimumSize(QSize(165, 225))
        self.label.setMaximumSize(QSize(165, 270))

        self.label.setText("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName(frame_name)
        self.label.setScaledContents(True)

        self.label.setStyleSheet("QLabel{\n"
                                 "padding: 3px 3px 3px 3px;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel:hover{\n"
                                 "border: 5px solid rgb(255, 166, 54);\n"
                                 "border-radius: 5px;\n"
                                 "}\n"
                                 "\n"
                                 "")

        # movie_poster_containers = self.scrollAreaWidgetContents.findChildren(Poster)

        self.popular_movies_scroll_area_grid_layout.addWidget(self.label, 0, column, 1, 1)

    def make_more_tv_show_posters(self, column):
        frame_name = "tv_show_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label_2 = Poster(parent=self.popular_tv_shows_scroll_area_contents, media_type="tv",
                              application_window=self.application_window)

        self.label_2.setMinimumSize(QSize(165, 225))
        self.label_2.setMaximumSize(QSize(165, 270))

        self.label_2.setText("")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName(frame_name)
        self.label_2.setScaledContents(True)

        self.label_2.setStyleSheet("QLabel{\n"
                                   "padding: 3px 3px 3px 3px;\n"
                                   "}\n"
                                   "\n"
                                   "QLabel:hover{\n"
                                   "border: 5px solid rgb(255, 166, 54);\n"
                                   "border-radius: 5px;\n"
                                   "}\n"
                                   "\n"
                                   "")

        self.popular_tv_shows_scroll_area_grid_layout.addWidget(self.label_2, 0, column, 1, 1)



