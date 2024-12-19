from os.path import split

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QImage, QPixmap
from main.about_title.about_title_design import Ui_MainWindow as AboutTitleDesignUI
import requests
import sqlite3
import json

class AboutTitlePage(QMainWindow, AboutTitleDesignUI):
    def __init__(self, media_id, media_type, account_id):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.media_id = media_id
        self.media_type = media_type
        self.account_id = account_id

        self.add_to_liked_state = "not clicked"
        self.add_to_watchlist_state = "not clicked"

        self.setupUi(self)

        self.initialize_liked_media_table()

        self.load_contents()
        self.set_liked_button_state()

        self.star_slider.valueChanged.connect(self.change_own_rating_slider)

        self.add_to_liked_button.clicked.connect(self.add_to_liked)

        self.add_to_watchlist_button.clicked.connect(self.add_to_watchlist)


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

        elif self.media_type == "tv":
            tv_show_url = f"https://api.themoviedb.org/3/tv/{self.media_id}"
            tv_show_response = requests.get(tv_show_url, headers=self.api_headers).json()

            print(tv_show_response)

            tv_show_title = tv_show_response['name']
            tv_show_overview = tv_show_response['overview']
            tv_show_vote_average = tv_show_response['vote_average']
            tv_show_release_year = (tv_show_response['first_air_date'].split('-'))[0]
            tv_show_img_url = 'https://image.tmdb.org/t/p/original' + tv_show_response['poster_path']
            tv_show_genres = self.get_genres(tv_show_response['genres'])

            # print(movie_overview)
            # print(movie_vote_average)
            # print(movie_release_year)
            #
            self.title_label.setText(tv_show_title)
            self.year_label.setText(str(tv_show_release_year))
            self.general_stars_label.setText(str(tv_show_vote_average))
            self.synopsis_label.setText(tv_show_overview)
            self.director_label.setText("Directed by: " + self.get_directors(tv_show_url))
            self.genres_label.setText("Genres: " + tv_show_genres)

            tv_show_image = QImage()
            tv_show_image.loadFromData(requests.get(tv_show_img_url).content)

            self.poster_label.setPixmap(QPixmap(tv_show_image))
            self.poster_label.setScaledContents(True)

    # # Made add_to_liked_state a property so that it can be manipulated after __init__
    # @property
    # def add_to_liked_state(self):
    #     return self._add_to_liked_state
    #
    # @add_to_liked_state.setter
    # def add_to_liked_state(self, state):
    #     self._add_to_liked_state = state

    def set_liked_button_state(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        if self.media_type == "movie":
            liked_movies = json.loads(
                cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])
            if self.media_id in liked_movies:
                self.add_to_liked_button.setText("Remove from Liked")

                self.add_to_liked_state = "clicked"

        else:
            liked_tv_shows = json.loads(
                cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

            if self.media_id in liked_tv_shows:
                self.add_to_liked_button.setText("Remove from Liked")

                self.add_to_liked_state = "clicked"

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

    def change_own_rating_slider(self):
        star_slider_value = round(self.star_slider.value()/2, 1)

        temp = list(str(star_slider_value))

        if temp[2] == '5':
            self.star_label.setText(f"Own rating: {star_slider_value: .1f} stars")
        else:
            self.star_label.setText(f"Own rating: {star_slider_value: .0f} stars")

    def add_to_liked(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # # Check if row with account_id exists in liked_media table
        # does_row_with_account_id_exist = cursor.execute("""SELECT * FROM liked_media WHERE account_id=(:account_id)""",
        #                                        {"account_id": self.account_id}).fetchone()
        #
        # if not does_row_with_account_id_exist:
        #     liked_movies_json_placeholder = json.dumps([])
        #     liked_tv_shows_json_placeholder = json.dumps([])
        #
        #     cursor.execute("""INSERT INTO liked_media VALUES (:account_id, :liked_movies, :liked_tv_shows)""",
        #                    {"account_id": self.account_id, "liked_movies": liked_movies_json_placeholder,
        #                     "liked_tv_shows": liked_tv_shows_json_placeholder})

        # Reads the json in liked_movies column, converts it into a list
        liked_movies = json.loads(cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": self.account_id}).fetchone()[0])

        # Same thing with the liked_tv_shows_column
        liked_tv_shows = json.loads(cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": self.account_id}).fetchone()[0])

        if self.add_to_liked_state == "not clicked":
            self.add_to_liked_button.setText("Remove from Liked")

            if self.media_type == "movie" and self.media_id not in liked_movies:
                liked_movies.append(self.media_id)

                # Converts the list into a json
                liked_movies_json = json.dumps(liked_movies)

                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                               {"liked_movies": liked_movies_json, "account_id": self.account_id})

            if self.media_type == "tv" and self.media_id not in liked_tv_shows:
                liked_tv_shows.append(self.media_id)

                # Converts the list into a json
                liked_tv_shows_json = json.dumps(liked_tv_shows)

                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": liked_tv_shows_json, "account_id": self.account_id})

            self.add_to_liked_state = "clicked"
        else:
            self.add_to_liked_button.setText("Add to Liked")

            if self.media_type == "movie" and self.media_id in liked_movies:
                liked_movies.pop(liked_movies.index(self.media_id))

                # Converts the list into a json
                liked_movies_json = json.dumps(liked_movies)

                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                               {"liked_movies": liked_movies_json, "account_id": self.account_id})

            if self.media_type == "tv" and self.media_id in liked_tv_shows:
                liked_tv_shows.pop(liked_tv_shows.index(self.media_id))

                # Converts the list into a json
                liked_tv_shows_json = json.dumps(liked_tv_shows)

                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": liked_tv_shows_json, "account_id": self.account_id})

            self.add_to_liked_state = "not clicked"

        connection.commit()
        connection.close()

    def add_to_watchlist(self):
        if self.add_to_watchlist_state == "not clicked":
            self.add_to_watchlist_button.setText("Remove from Watchlist")

            self.add_to_watchlist_state = "clicked"
        else:
            self.add_to_watchlist_button.setText("Add to Watchlist")

            self.add_to_watchlist_state = "not clicked"

    def initialize_liked_media_table(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # Check if row with account_id exists in liked_media table
        does_row_with_account_id_exist = cursor.execute("""SELECT * FROM liked_media WHERE account_id=(:account_id)""",
                                               {"account_id": self.account_id}).fetchone()

        if not does_row_with_account_id_exist:
            liked_movies_json_placeholder = json.dumps([])
            liked_tv_shows_json_placeholder = json.dumps([])

            cursor.execute("""INSERT INTO liked_media VALUES (:account_id, :liked_movies, :liked_tv_shows)""",
                           {"account_id": self.account_id, "liked_movies": liked_movies_json_placeholder,
                            "liked_tv_shows": liked_tv_shows_json_placeholder})

        connection.commit()
        connection.close()

    # def split_title(self):
    #     return '+'.join(self.title.split())
