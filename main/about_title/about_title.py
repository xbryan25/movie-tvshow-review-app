from os.path import split

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QImage, QPixmap
from main.about_title.about_title_design import Ui_MainWindow as AboutTitleDesignUI
import requests


class AboutTitlePage(QMainWindow, AboutTitleDesignUI):
    def __init__(self, media_id, media_type):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.media_id = media_id
        self.media_type = media_type

        self.setupUi(self)

        self.load_contents()

    def load_contents(self):
        if self.media_type == "movie":
            movie_url = f"https://api.themoviedb.org/3/movie/{self.media_id}"
            movie_response = requests.get(movie_url, headers=self.api_headers).json()

            print(movie_response)

            movie_title = movie_response['title']
            movie_overview = movie_response['overview']
            movie_vote_average = movie_response['vote_average']
            movie_release_year = (movie_response['release_date'].split('-'))[0]
            movie_img_url = 'https://image.tmdb.org/t/p/original' + movie_response['poster_path']
            movie_genres = self.get_genres(movie_response['genres'])

            print(movie_overview)
            print(movie_vote_average)
            print(movie_release_year)

            self.title_label.setText(movie_title)
            self.year_label.setText(str(movie_release_year))
            self.general_stars_label.setText(str(movie_vote_average))
            self.synopsis_label.setText(movie_overview)
            self.director_label.setText("Directed by: " + self.get_directors(movie_url))
            self.genres_label.setText("Genres: " + movie_genres)

            movie_image = QImage()
            movie_image.loadFromData(requests.get(movie_img_url).content)

            self.poster_label.setPixmap(QPixmap(movie_image))
            self.poster_label.setScaledContents(True)



    def get_directors(self, movie_url):
        movie_credits_url = movie_url + "/credits?language=en-US"
        movie_credits_response = requests.get(movie_credits_url, headers=self.api_headers).json()

        directors = []

        for crew_member in movie_credits_response['crew']:
            if crew_member['job'] == 'Director':
                directors.append(crew_member['name'])

        return ', '.join(directors)

    def get_genres(self, genres_list):
        genres = []

        for genre_dictionary in genres_list:
            genres.append(genre_dictionary['name'])

        return ', '.join(genres)


    # def split_title(self):
    #     return '+'.join(self.title.split())
