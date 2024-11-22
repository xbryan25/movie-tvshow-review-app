from main.choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI

from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage
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

        self.load_pictures()

    def load_pictures(self):

        popular_movies_api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        response = requests.get(popular_movies_api_url, headers=self.api_headers)

        # for i in range(4):
        #     url = 'https://image.tmdb.org/t/p/original/' + response.json()['results'][i]['poster_path']
        #
        #     image = QImage()
        #     image.loadFromData(requests.get(url).content)
        #
        #     image_label.setPixmap(QPixmap(image))
        #     image_label.show()

        labels = self.widget_2.findChildren(QLabel)

        # TODO: Add loading screen

        for i in range(4):
            url = 'https://image.tmdb.org/t/p/original/' + response.json()['results'][i]['poster_path']

            image = QImage()
            image.loadFromData(requests.get(url).content)

            labels[i].setPixmap(QPixmap(image))
            labels[i].show()
