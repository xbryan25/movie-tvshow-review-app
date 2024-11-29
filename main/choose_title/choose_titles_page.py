from main.choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI

from main.choose_title.posters import Poster

from PyQt6.QtWidgets import QMainWindow, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, QRect, QEvent
import requests
import sqlite3
import re
import urllib


class ChooseTitlesPage(QMainWindow, ChooseTitlesPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        for i in range(15):
            self.make_more_movie_posters(i)
            self.make_more_tv_show_posters(i)

        self.load_pictures()

        print("Done!")

    def load_pictures(self):

        popular_movies_api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        popular_movies_api_response = requests.get(popular_movies_api_url, headers=self.api_headers)

        popular_tv_shows_api_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
        popular_tv_shows_api_response = requests.get(popular_tv_shows_api_url, headers=self.api_headers)

        # test = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1&with_original_language=en"
        # tester = requests.get(test, headers=self.api_headers)
        # print(tester.json())

        # for i in range(4):
        #     url = 'https://image.tmdb.org/t/p/original/' + response.json()['results'][i]['poster_path']
        #
        #     image = QImage()
        #     image.loadFromData(requests.get(url).content)
        #
        #     image_label.setPixmap(QPixmap(image))
        #     image_label.show()

        # Find the children of the Poster class
        movie_poster_containers = self.scrollAreaWidgetContents.findChildren(Poster)
        tv_show_poster_containers = self.scrollAreaWidgetContents_2.findChildren(Poster)

        # TODO: Add loading screen

        for i in range(15):
            movie_img_url = 'https://image.tmdb.org/t/p/original/' + popular_movies_api_response.json()['results'][i]['poster_path']

            movie_image = QImage()
            movie_image.loadFromData(requests.get(movie_img_url).content)

            movie_poster_containers[i].setPixmap(QPixmap(movie_image))
            movie_poster_containers[i].show()

            tv_show_img_url = 'https://image.tmdb.org/t/p/original/' + popular_tv_shows_api_response.json()['results'][i]['poster_path']

            tv_show_image = QImage()
            tv_show_image.loadFromData(requests.get(tv_show_img_url).content)

            tv_show_poster_containers[i].setPixmap(QPixmap(tv_show_image))
            tv_show_poster_containers[i].show()

    def make_more_movie_posters(self, column):
        frame_name = "movie_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label = Poster(parent=self.scrollAreaWidgetContents)
        self.label.setMinimumSize(QSize(200, 300))
        self.label.setMaximumSize(QSize(200, 300))

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

        movie_poster_containers = self.scrollAreaWidgetContents.findChildren(Poster)

        self.gridLayout.addWidget(self.label, 0, column, 1, 1)



    def make_more_tv_show_posters(self, column):
        frame_name = "tv_show_frame_" + str(column + 1)

        # Don't forget to change QLabel to Poster

        self.label_2 = Poster(parent=self.scrollAreaWidgetContents_2)
        self.label_2.setMinimumSize(QSize(200, 300))
        self.label_2.setMaximumSize(QSize(200, 300))

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



