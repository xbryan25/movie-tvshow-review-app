from main.choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI

from main.choose_title.posters import Poster

from PyQt6.QtWidgets import QMainWindow, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import (QSize, Qt, QPropertyAnimation, QRect, QEvent, QThread, QObject, pyqtSignal, QRunnable,
                          pyqtSlot, QThreadPool)
from main.loading_screen.loading_screen import LoadingScreen
import requests
import sqlite3
import re
import urllib
import asyncio
import threading
import sys
import traceback

import time

# Multithreading credits: https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/#qrunnable-and-the-qthreadpool
# https://realpython.com/python-pyqt-qthread/


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


# For QThread
class LoadPicturesWorker(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.fn()
        self.signals.finished.emit()


class ChooseTitlesPage(QMainWindow, ChooseTitlesPageUI):
    def __init__(self, account_id):
        super().__init__()

        self.setupUi(self)
        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.account_id = account_id

        for i in range(12):
            self.make_more_movie_posters(i)
            self.make_more_tv_show_posters(i)

        self.loading_screen = LoadingScreen()
        self.loading_screen.show()

        self.threadpool = QThreadPool()
        self.start_load_pictures_thread()

        print("Yo")

    def start_load_pictures_thread(self):
        load_pictures_worker = LoadPicturesWorker(self.load_pictures)

        load_pictures_worker.signals.finished.connect(self.show_choose_titles_page)

        self.threadpool.start(load_pictures_worker)

    def load_pictures(self):

        popular_movies_api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        popular_movies_api_response = requests.get(popular_movies_api_url, headers=self.api_headers)

        popular_tv_shows_api_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
        popular_tv_shows_api_response = requests.get(popular_tv_shows_api_url, headers=self.api_headers)

        # Find the children of the Poster class
        movie_poster_containers = self.popular_movies_scroll_area_contents.findChildren(Poster)
        tv_show_poster_containers = self.popular_tv_shows_scroll_area_contents.findChildren(Poster)

        # TODO: Add loading screen

        for i in range(12):
            movie_img_url = 'https://image.tmdb.org/t/p/w342/' + popular_movies_api_response.json()['results'][i][
                'poster_path']

            movie_id = popular_movies_api_response.json()['results'][i][
                'id']

            movie_image = QImage()
            movie_image.loadFromData(requests.get(movie_img_url).content)

            movie_poster_containers[i].setMediaId(movie_id)
            movie_poster_containers[i].setPixmap(QPixmap(movie_image))
            movie_poster_containers[i].show()

            # TMDB poster download sizes
            # https://www.themoviedb.org/talk/5ee4ba52a217c0001fd0cb83

            tv_show_img_url = 'https://image.tmdb.org/t/p/w342/' + \
                              popular_tv_shows_api_response.json()['results'][i]['poster_path']

            tv_show_id = popular_tv_shows_api_response.json()['results'][i]['id']

            tv_show_image = QImage()
            tv_show_image.loadFromData(requests.get(tv_show_img_url).content)

            tv_show_poster_containers[i].setMediaId(tv_show_id)
            tv_show_poster_containers[i].setPixmap(QPixmap(tv_show_image))
            tv_show_poster_containers[i].show()

            print(f"{((i + 1) / 12) * 100:.2f}")
            self.loading_screen.loading_progress_bar.setValue(int(((i + 1) / 12) * 100))

        print("Done!")

    def show_choose_titles_page(self):
        self.loading_screen.hide()
        self.show()


    def make_more_movie_posters(self, column):
        frame_name = "movie_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label = Poster(parent=self.popular_movies_scroll_area_contents, media_type="movie", account_id=self.account_id)
        self.label.setMinimumSize(QSize(165, 250))
        self.label.setMaximumSize(QSize(165, 250))

        self.label.setText("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName(frame_name)
        self.label.setScaledContents(True)

        self.label.setStyleSheet("QLabel{\n"
                                 "padding: 3px 3px 3px 3px;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel:hover{\n"
                                 "border: 4px solid blue;\n"
                                 "border-radius: 1px;\n"
                                 "}\n"
                                 "\n"
                                 "")

        # movie_poster_containers = self.scrollAreaWidgetContents.findChildren(Poster)

        self.gridLayout.addWidget(self.label, 0, column, 1, 1)

    def make_more_tv_show_posters(self, column):
        frame_name = "tv_show_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label_2 = Poster(parent=self.popular_tv_shows_scroll_area_contents, media_type="tv", account_id=self.account_id)
        self.label_2.setMinimumSize(QSize(165, 250))
        self.label_2.setMaximumSize(QSize(165, 250))

        self.label_2.setText("")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName(frame_name)
        self.label_2.setScaledContents(True)

        self.label_2.setStyleSheet("QLabel{\n"
                                 "padding: 3px 3px 3px 3px;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel:hover{\n"
                                 "border: 4px solid blue;\n"
                                 "border-radius: 1px;\n"
                                 "}\n"
                                 "\n"
                                 "")

        self.gridLayout_2.addWidget(self.label_2, 0, column, 1, 1)



