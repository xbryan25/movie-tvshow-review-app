

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

        self.movie_posters = []
        self.tv_show_posters = []

        self.movie_posters_contents = {}
        self.tv_show_posters_contents = {}

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_api_client(self, api_client):
        self.api_client = api_client
        # self.api_client.progress_updated.connect(lambda: print("Yo"))

    def update_progress_bar(self, percentage):
        self.loading_screen.loading_progress_bar.setValue(percentage)

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
        self.logout_button.clicked.connect(self.logout_account)

    def start_process(self):
        for i in range(20):
            self.make_more_movie_posters(i)
            self.make_more_tv_show_posters(i)

        self.loading_screen = LoadingScreen()
        self.loading_screen.show()

        self.threadpool = QThreadPool()
        self.start_load_pictures_thread()

    def logout_account(self):
        self.logout_confirmation_dialog = LogoutConfirmationDialog(self.application_window)
        self.logout_confirmation_dialog.exec()

    def start_load_pictures_thread(self):
        self.application_window.hide()

        load_pictures_worker = LoadPicturesWorker(self.load_pictures, self.api_client)

        load_pictures_worker.signals.finished.connect(self.show_posters)

        load_pictures_worker.signals.finished.connect(self.show_choose_titles_page)

        self.threadpool.start(load_pictures_worker)

    def show_posters(self):
        for i, (key, value) in enumerate(self.movie_posters_contents.items()):
            self.movie_posters[i].setMediaId(key)

            if value != '':
                movie_image = QImage()
                movie_image.loadFromData(value)

                self.movie_posters[i].setPixmap(QPixmap(movie_image))
            else:
                question_mark_image = QPixmap("../assets/images/question_mark.jpg")
                self.movie_posters[i].setPixmap(QPixmap(question_mark_image))

        for i, (key, value) in enumerate(self.tv_show_posters_contents.items()):
            self.tv_show_posters[i].setMediaId(key)

            if value != '':
                tv_show_image = QImage()
                tv_show_image.loadFromData(value)

                self.tv_show_posters[i].setPixmap(QPixmap(tv_show_image))
            else:
                question_mark_image = QPixmap("../assets/images/question_mark.jpg")
                self.tv_show_posters[i].setPixmap(QPixmap(question_mark_image))

    async def load_pictures(self):
        popular_movies_api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        popular_movies_api_response = await self.api_client.fetch(popular_movies_api_url)

        popular_tv_shows_api_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
        popular_tv_shows_api_response = await self.api_client.fetch(popular_tv_shows_api_url)

        movie_ids = []
        movie_img_urls = []

        tv_show_ids = []
        tv_show_img_urls = []

        # Get Poster details
        for i in range(20):
            movie_img_url = ""

            if popular_movies_api_response['results'][i]['poster_path']:
                movie_img_url = 'https://image.tmdb.org/t/p/w342/' + popular_movies_api_response['results'][i][
                    'poster_path']

            movie_img_urls.append(movie_img_url)

            movie_ids.append(popular_movies_api_response['results'][i]['id'])

            # TMDB poster download sizes
            # https://www.themoviedb.org/talk/5ee4ba52a217c0001fd0cb83

            tv_show_img_url = ""

            if popular_tv_shows_api_response['results'][i]['poster_path']:
                tv_show_img_url = ('https://image.tmdb.org/t/p/w342/' +
                                   popular_tv_shows_api_response['results'][i]['poster_path'])

            tv_show_img_urls.append(tv_show_img_url)

            tv_show_ids.append(popular_tv_shows_api_response['results'][i]['id'])

        # Fetch data from TMDB
        movie_img_data = await self.api_client.fetch_all_images(movie_img_urls, self.loading_screen.loading_progress_bar, 0, 40)
        tv_show_img_data = await self.api_client.fetch_all_images(tv_show_img_urls, self.loading_screen.loading_progress_bar, 21, 40)

        # Load image data to Posters
        for j in range(20):
            self.movie_posters_contents.update({movie_ids[j]: movie_img_data[j]})
            self.tv_show_posters_contents.update({tv_show_ids[j]: tv_show_img_data[j]})



    def show_choose_titles_page(self):
        self.loading_screen.close()
        self.application_window.show()

    def make_more_movie_posters(self, column):
        frame_name = "movie_frame_" + str(column + 1)

        self.movie_poster = Poster(parent=self.popular_movies_scroll_area_contents, media_type="movie",
                                   application_window=self.application_window, frame_name=frame_name)

        self.popular_movies_scroll_area_grid_layout.addWidget(self.movie_poster, 0, column, 1, 1)

        self.movie_posters.append(self.movie_poster)

    def make_more_tv_show_posters(self, column):
        frame_name = "tv_show_frame_" + str(column + 1)

        self.tv_show_poster = Poster(parent=self.popular_tv_shows_scroll_area_contents, media_type="tv",
                                     application_window=self.application_window, frame_name=frame_name)

        self.popular_tv_shows_scroll_area_grid_layout.addWidget(self.tv_show_poster, 0, column, 1, 1)

        self.tv_show_posters.append(self.tv_show_poster)
