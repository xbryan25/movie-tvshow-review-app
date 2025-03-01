from os.path import split

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QImage, QPixmap

from about_title.about_title_movie_design import Ui_MainWindow as AboutTitleMovieDesignUI
from about_title.movie_review import MovieReview

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests
import sqlite3
import json


class AboutTitleMoviePage(QMainWindow, AboutTitleMovieDesignUI):
    def __init__(self, media_id, account_id, requests_session_tmdb, requests_session_images):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.media_id = str(media_id)
        self.account_id = account_id

        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

        # To be overwritten later
        self.media_title = ""

        self.add_to_liked_state = "not clicked"
        self.add_to_watchlist_state = "not clicked"

        self.setupUi(self)

        # self.initialize_liked_media_table()
        # self.initialize_to_watch_media_table()
        #
        # self.initialize_reviews_table()

        self.load_contents()

        self.set_liked_button_state()
        self.set_watchlist_button_state()
        self.set_review_button_state()

        self.load_old_rating()

        self.star_slider.valueChanged.connect(lambda: self.change_own_rating_slider())

        self.add_to_liked_button.clicked.connect(self.add_to_liked)

        self.add_to_watchlist_button.clicked.connect(self.add_to_watchlist)

        self.add_review_button.clicked.connect(self.add_review_movie)

        self.save_rating_button.clicked.connect(self.save_rating)

    def load_contents(self):
        movie_url = f"https://api.themoviedb.org/3/movie/{self.media_id}"
        movie_response = self.requests_session_tmdb.get(movie_url, headers=self.api_headers).json()

        print(movie_response)

        # To be used in the class
        self.media_title = movie_response['title']
        movie_overview = movie_response['overview']
        movie_vote_average = movie_response['vote_average']
        movie_release_year = (movie_response['release_date'].split('-'))[0]

        movie_genres = self.get_genres(movie_response['genres'])

        print(movie_overview)
        print(movie_vote_average)
        print(movie_release_year)

        self.title_label.setText(self.media_title)
        self.year_label.setText(str(movie_release_year))
        self.general_stars_label.setText(str(movie_vote_average))
        self.synopsis_label.setText(movie_overview)
        self.genres_label.setText("Genres: " + movie_genres)

        movie_directors = self.get_directors(movie_url)

        if len(movie_directors) >= 3:
            # Only get the two first directors then add ", etc."
            self.director_label.setText(
                    f"Directed by: {", ".join(movie_directors[:2])}, etc.")
        else:
            self.director_label.setText(f"Directed by: {", ".join(movie_directors)}")

        if not movie_response['poster_path']:
            question_mark_image = QPixmap("../images/question_mark.jpg")
            #
            self.poster_label.setPixmap(question_mark_image)
            self.poster_label.setScaledContents(True)
        else:
            movie_img_url = 'https://image.tmdb.org/t/p/w500/' + movie_response['poster_path']

            movie_image = QImage()
            movie_image.loadFromData(self.requests_session_images.get(movie_img_url).content)

            self.poster_label.setPixmap(QPixmap(movie_image))
            self.poster_label.setScaledContents(True)


    def set_liked_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        liked_movies = json.loads(
            cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])
        if self.media_id in liked_movies:
            self.add_to_liked_button.setText("Remove from Liked")

            self.add_to_liked_state = "clicked"

    def set_watchlist_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movies_to_watch = json.loads(
            cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        if self.media_id in movies_to_watch:
            self.add_to_watchlist_button.setText("Remove from Watchlist")

            self.add_to_watchlist_state = "clicked"

    def set_review_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movie_reviews = json.loads(
            cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        movie_ids = movie_reviews.keys()

        if str(self.media_id) in movie_ids:
            self.add_review_button.setText("Edit Review")

        connection.commit()
        connection.close()

    def get_directors(self, movie_url):
        movie_credits_url = movie_url + "/credits?language=en-US"
        movie_credits_response = self.requests_session_tmdb.get(movie_credits_url, headers=self.api_headers).json()

        movie_directors = []

        for crew_member in movie_credits_response['crew']:
            if crew_member['job'] == 'Director':
                movie_directors.append(crew_member['name'])

        return movie_directors

    def get_genres(self, genres_list):
        genres = []

        for genre_dictionary in genres_list:
            genres.append(genre_dictionary['name'])

        return ', '.join(genres)

    def change_own_rating_slider(self, old_rating=None):
        if not old_rating:
            star_slider_value = round(self.star_slider.value()/2, 1)

            temp = list(str(star_slider_value))

            if temp[2] == '5':
                self.star_label.setText(f"Own rating: {star_slider_value: .1f} stars")
            else:
                self.star_label.setText(f"Own rating: {star_slider_value: .0f} stars")

        elif old_rating:
            self.star_slider.setSliderPosition(int(old_rating * 2))

            temp = list(str(old_rating))

            if temp[2] == '5':
                self.star_label.setText(f"Own rating: {old_rating: .1f} stars")
            else:
                self.star_label.setText(f"Own rating: {old_rating: .0f} stars")

    def add_to_liked(self):
        connection = sqlite3.connect('../database\\accounts.db')
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

        if self.add_to_liked_state == "not clicked":
            self.add_to_liked_button.setText("Remove from Liked")

            if self.media_id not in liked_movies:
                liked_movies.append(self.media_id)

                # Converts the list into a json
                liked_movies_json = json.dumps(liked_movies)

                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                               {"liked_movies": liked_movies_json, "account_id": self.account_id})

            self.add_to_liked_state = "clicked"
        else:
            self.add_to_liked_button.setText("Add to Liked")

            if self.media_id in liked_movies:
                liked_movies.pop(liked_movies.index(self.media_id))

                # Converts the list into a json
                liked_movies_json = json.dumps(liked_movies)

                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                               {"liked_movies": liked_movies_json, "account_id": self.account_id})

            self.add_to_liked_state = "not clicked"

        connection.commit()
        connection.close()

    def add_to_watchlist(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movies_to_watch = json.loads(
            cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        if self.add_to_watchlist_state == "not clicked":
            self.add_to_watchlist_button.setText("Remove from Watchlist")

            if self.media_id not in movies_to_watch:
                movies_to_watch.append(self.media_id)

                # Converts the list into a json
                movies_to_watch_json = json.dumps(movies_to_watch)

                cursor.execute("""UPDATE media_to_watch SET movies_to_watch=(:movies_to_watch) WHERE account_id=(:account_id)""",
                               {"movies_to_watch": movies_to_watch_json, "account_id": self.account_id})

            self.add_to_watchlist_state = "clicked"
        else:
            self.add_to_watchlist_button.setText("Add to Watchlist")

            if self.media_id in movies_to_watch:
                movies_to_watch.pop(movies_to_watch.index(self.media_id))

                # Converts the list into a json
                movies_to_watch_json = json.dumps(movies_to_watch)

                cursor.execute("""UPDATE media_to_watch SET movies_to_watch=(:movies_to_watch) WHERE account_id=(:account_id)""",
                               {"movies_to_watch": movies_to_watch_json, "account_id": self.account_id})

            self.add_to_watchlist_state = "not clicked"

        connection.commit()
        connection.close()

    def add_review_movie(self):
        self.movie_review = MovieReview(self.account_id, self.media_id)

        self.movie_review.title_label.setText(self.media_title)

        self.movie_review.show()

    def save_rating(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movies_and_ratings = json.loads(cursor.execute("""SELECT movie_own_ratings FROM own_ratings_for_media 
                                        WHERE account_id=(:account_id)""",
                                      {"account_id": self.account_id}).fetchone()[0])

        rated_movies = movies_and_ratings.keys()

        if self.media_id not in rated_movies:
            movies_and_ratings.update({self.media_id: round(self.star_slider.value()/2, 1)})
        else:
            movies_and_ratings[self.media_id] = round(self.star_slider.value()/2, 1)

        movies_and_ratings_json = json.dumps(movies_and_ratings)
        cursor.execute("""UPDATE own_ratings_for_media SET movie_own_ratings=(:movie_own_ratings) WHERE
                                      account_id=(:account_id)""",
                       {"movie_own_ratings": movies_and_ratings_json, "account_id": self.account_id})

        print("Rating saved successfully!")

        connection.commit()
        connection.close()

    def load_old_rating(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        movies_and_ratings = json.loads(cursor.execute("""SELECT movie_own_ratings FROM own_ratings_for_media 
                                                WHERE account_id=(:account_id)""",
                                                       {"account_id": self.account_id}).fetchone()[0])

        rated_movies = movies_and_ratings.keys()

        if self.media_id in rated_movies:
            self.change_own_rating_slider(old_rating=movies_and_ratings[self.media_id])

        connection.commit()
        connection.close()



    # def split_title(self):
    #     return '+'.join(self.title.split())
