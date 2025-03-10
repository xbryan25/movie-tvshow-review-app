from os.path import split

from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import QSize, Qt

# from about_title.about_title_tv_show_design import Ui_MainWindow as AboutTitleTvShowDesignUI
from about_title.tv_show_review import TvShowReview
from about_title.movie_review import MovieReview

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests
import sqlite3
import json


class AboutSpecificMediaPageControls:
    def __init__(self, widgets, application_window):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZ"
                             "iI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYX"
                             "BpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.widgets = widgets
        self.application_window = application_window

        self.media_id = None
        self.media_type = None
        self.account_id = None
        self.requests_session_tmdb = None
        self.requests_session_images = None

        # To be overwritten later
        self.media_title = ""

        # For TV Shows
        self.seasons = []
        self.clicked_season = 'Series'
        self.seasons_directors = {}

        self.add_to_liked_state = "not clicked"
        self.add_to_watchlist_state = "not clicked"

        self.load_widgets()

        self.add_signals()

    def add_signals(self):
        self.star_slider.valueChanged.connect(lambda: self.change_own_rating_slider())
        self.add_to_liked_button.clicked.connect(self.add_to_liked)
        self.add_to_watchlist_button.clicked.connect(self.add_to_watchlist)
        self.add_review_button.clicked.connect(self.add_review_to_media)
        self.save_rating_button.clicked.connect(self.save_rating)

    def set_media_type_and_id(self, media_type, media_id):
        self.media_type = media_type
        self.media_id = str(media_id)

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_requests_session(self, requests_session_tmdb, requests_session_images):
        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

    def set_liked_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if self.media_type == "tv":

            liked_tv_shows = json.loads(
                cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

            if self.media_id in liked_tv_shows:
                self.add_to_liked_button.setText("Remove from Liked")

                self.add_to_liked_state = "clicked"
            else:
                self.add_to_liked_button.setText("Add to Liked")

                self.add_to_liked_state = "not clicked"

        elif self.media_type == "movie":
            liked_movies = json.loads(
                cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])
            if self.media_id in liked_movies:
                self.add_to_liked_button.setText("Remove from Liked")

                self.add_to_liked_state = "clicked"
            else:
                self.add_to_liked_button.setText("Add to Liked")

                self.add_to_liked_state = "not clicked"

            # print(self.add_to_liked_button.text())

        connection.commit()
        connection.close()

    def set_watchlist_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if self.media_type == "tv":

            tv_shows_to_watch = json.loads(
                cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

            if self.media_id in tv_shows_to_watch:
                self.add_to_watchlist_button.setText("Remove from Watchlist")

                self.add_to_watchlist_state = "clicked"

            else:
                self.add_to_watchlist_button.setText("Add to Watchlist")

                self.add_to_watchlist_state = "not clicked"

        elif self.media_type == "movie":
            movies_to_watch = json.loads(
                cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

            if self.media_id in movies_to_watch:
                self.add_to_watchlist_button.setText("Remove from Watchlist")

                self.add_to_watchlist_state = "clicked"

            else:
                self.add_to_watchlist_button.setText("Add to Watchlist")

                self.add_to_watchlist_state = "not clicked"

        connection.commit()
        connection.close()

    def set_review_button_state(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if self.media_type == "movie":
            movie_reviews = json.loads(
                cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

            movie_ids = movie_reviews.keys()

            if str(self.media_id) in movie_ids:
                self.add_review_button.setText("Edit Review")

        connection.commit()
        connection.close()

    def get_directors(self):

        if self.media_type == "tv":
            # Make a copy of self.seasons but without the series, which is the first element

            seasons_list_without_series = list(self.seasons[1:])
            for season in seasons_list_without_series:
                season_directors = []

                tv_show_season_credit_url = f"https://api.themoviedb.org/3/tv/{self.media_id}/season/{season['season_number']}"
                tv_credit_response = self.requests_session_tmdb.get(tv_show_season_credit_url,
                                                                       headers=self.api_headers).json()

                for episode_credits in tv_credit_response['episodes']:

                    # Check if episode_credits['crew'] (a list) is empty or not
                    if episode_credits['crew']:
                        for crew in episode_credits['crew']:

                            if crew['job'] == 'Director':
                                episode_director_name = crew['name']

                                if episode_director_name not in season_directors:
                                    season_directors.append(episode_director_name)

                self.seasons_directors.update({season['name']: season_directors})

        elif self.media_type == "movie":
            movie_credits_url = f"https://api.themoviedb.org/3/movie/{self.media_id}/credits?language=en-US"

            movie_credits_response = self.requests_session_tmdb.get(movie_credits_url, headers=self.api_headers).json()

            movie_directors = []

            for crew_member in movie_credits_response['crew']:
                if crew_member['job'] == 'Director':
                    movie_directors.append(crew_member['name'])

            if len(movie_directors) >= 3:
                # Only get the two first directors then add ", etc."
                self.director_label.setText(
                    f"Directed by: {", ".join(movie_directors[:2])}, etc.")
            else:
                self.director_label.setText(f"Directed by: {", ".join(movie_directors)}")

    def get_genres(self, genres_list):
        genres = []

        for genre_dictionary in genres_list:
            genres.append(genre_dictionary['name'])

        return ', '.join(genres)

    def load_widgets(self):
        self.director_label = self.widgets[0]
        self.general_stars_label = self.widgets[1]
        self.genres_label = self.widgets[2]
        self.media_title_label = self.widgets[3]
        self.poster_label = self.widgets[4]
        self.synopsis_label = self.widgets[5]
        self.year_label = self.widgets[6]
        self.add_review_button = self.widgets[7]
        self.add_to_liked_button = self.widgets[8]
        self.add_to_watchlist_button = self.widgets[9]
        self.save_rating_button = self.widgets[10]
        self.star_label = self.widgets[11]
        self.star_slider = self.widgets[12]
        self.season_buttons_scroll_area = self.widgets[13]
        self.season_buttons_scroll_area_widget_contents = self.widgets[14]
        self.seasons_buttons_grid_layout = self.widgets[15]
        self.gridLayout_2 = self.widgets[16]

    # TODO: Rename to something such as load_posters
    def start_process(self):
        self.load_contents()

        self.load_old_rating()

        self.set_liked_button_state()
        self.set_watchlist_button_state()
        self.set_review_button_state()

        if self.media_type == "tv":
            self.load_season_buttons()
            self.attach_connection_to_change_season()

    def load_contents(self):
        media_url = f"https://api.themoviedb.org/3/{self.media_type}/{self.media_id}"
        media_release_year = ""

        media_response = self.requests_session_tmdb.get(media_url, headers=self.api_headers).json()

        if self.media_type == "tv":
            self.media_title = media_response['name']
        if self.media_type == "movie":
            self.media_title = media_response['title']

        # To be used in the class
        media_overview = media_response['overview']
        media_vote_average = media_response['vote_average']
        media_genres = self.get_genres(media_response['genres'])

        if self.media_type == "tv":
            media_release_year = (media_response['first_air_date'].split('-'))[0]

            self.seasons = media_response['seasons']

            self.add_series_dictionary(media_response['number_of_episodes'], media_response['vote_average'],
                                       media_response['overview'], media_response['id'])
        if self.media_type == "movie":
            media_release_year = (media_response['release_date'].split('-'))[0]

        self.media_title_label.setText(self.media_title)
        self.year_label.setText(str(media_release_year))
        self.general_stars_label.setText(str(media_vote_average/2))
        self.synopsis_label.setText(media_overview)
        self.director_label.setText("-")
        self.genres_label.setText("Genres: " + media_genres)

        self.get_directors()

        if not media_response['poster_path']:
            question_mark_image = QPixmap("../images/question_mark.jpg")

            self.poster_label.setPixmap(question_mark_image)
            self.poster_label.setScaledContents(True)
        else:
            media_img_url = 'https://image.tmdb.org/t/p/w500' + media_response['poster_path']

            media_image = QImage()
            media_image.loadFromData(self.requests_session_images.get(media_img_url).content)

            self.poster_label.setPixmap(QPixmap(media_image))
            self.poster_label.setScaledContents(True)

        if self.media_type == "movie":
            self.gridLayout_2.removeWidget(self.season_buttons_scroll_area)

            # Remove synopsis_label then re-add with now row span
            self.gridLayout_2.removeWidget(self.synopsis_label)
            self.gridLayout_2.addWidget(self.synopsis_label, 4, 1, 2, 3)
            self.gridLayout_2.update()

    def add_series_dictionary(self, number_of_episodes, vote_average, overview, series_id):
        # Shallow copies (meaning nested entries are not read) the first season of the show
        series_dictionary = dict(self.seasons[0])

        series_dictionary['name'] = 'Series'

        series_dictionary['episode_count'] = number_of_episodes
        series_dictionary['vote_average'] = vote_average
        series_dictionary['overview'] = overview
        series_dictionary['id'] = series_id

        self.seasons.insert(0, series_dictionary)

    def change_own_rating_slider(self, old_rating=None):
        if not old_rating:
            star_slider_value = round(self.star_slider.value() / 2, 1)

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

        liked_media_type = []
        liked_media_type_json = ""

        # Read from database
        if self.media_type == "tv":
            liked_media_type = json.loads(
                cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

        elif self.media_type == "movie":
            liked_media_type = json.loads(
                cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

        # Manipulate values
        if self.add_to_liked_state == "not clicked":
            self.add_to_liked_button.setText("Remove from Liked")
            liked_media_type.append(self.media_id)

            # Converts the list into a json
            liked_media_type_json = json.dumps(liked_media_type)

            self.add_to_liked_state = "clicked"
        elif self.add_to_liked_state == "clicked":
            self.add_to_liked_button.setText("Add to Liked")

            liked_media_type.pop(liked_media_type.index(self.media_id))

            # Converts the list into a json
            liked_media_type_json = json.dumps(liked_media_type)

            self.add_to_liked_state = "not clicked"

        # Update database
        if self.media_type == "tv":
            cursor.execute(
                """UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                {"liked_tv_shows": liked_media_type_json, "account_id": self.account_id})

        elif self.media_type == "movie":
            cursor.execute(
                """UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                {"liked_movies": liked_media_type_json, "account_id": self.account_id})

        connection.commit()
        connection.close()

    def add_to_watchlist(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        media_to_watch_type = []
        media_to_watch_type_json = ""

        # Read from database
        if self.media_type == "tv":
            media_to_watch_type = json.loads(
                cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

        elif self.media_type == "movie":
            media_to_watch_type = json.loads(
                cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {"account_id": self.account_id}).fetchone()[0])

        # Manipulate values
        if self.add_to_watchlist_state == "not clicked":
            self.add_to_watchlist_button.setText("Remove from Watchlist")
            media_to_watch_type.append(self.media_id)

            # Converts the list into a json
            media_to_watch_type_json = json.dumps(media_to_watch_type)

            self.add_to_watchlist_state = "clicked"
        elif self.add_to_liked_state == "clicked":
            self.add_to_watchlist_button.setText("Add to Watchlist")

            media_to_watch_type.pop(media_to_watch_type.index(self.media_id))

            # Converts the list into a json
            media_to_watch_type_json = json.dumps(media_to_watch_type)

            self.add_to_watchlist_state = "not clicked"

        # Update database
        if self.media_type == "tv":
            cursor.execute(
                """UPDATE media_to_watch SET tv_shows_to_watch=(:tv_shows_to_watch) WHERE account_id=(:account_id)""",
                {"tv_shows_to_watch": media_to_watch_type_json, "account_id": self.account_id})

        elif self.media_type == "movie":
            cursor.execute(
                """UPDATE media_to_watch SET movies_to_watch=(:movies_to_watch) WHERE account_id=(:account_id)""",
                {"movies_to_watch": media_to_watch_type_json, "account_id": self.account_id})

        connection.commit()
        connection.close()

    def add_review_to_media(self):

        if self.media_type == "tv":
            self.tv_show_review = TvShowReview(self.account_id, self.media_id, self.clicked_season)
            self.tv_show_review.title_label.setText(f"{self.media_title} | {self.clicked_season}")

            self.tv_show_review.show()
        elif self.media_type == "movie":
            self.movie_review = MovieReview(self.account_id, self.media_id)

            self.movie_review.title_label.setText(self.media_title)

            self.movie_review.show()

    def load_season_buttons(self):
        for season in self.seasons:
            # Don't forget to change QLabel to Poster

            self.season_button = QPushButton(parent=self.season_buttons_scroll_area_widget_contents)
            self.season_button.setMinimumSize(QSize(200, 25))
            self.season_button.setMaximumSize(QSize(200, 25))

            self.season_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.season_button.setFont(font)

            self.season_button.setText(season['name'])
            self.season_button.setObjectName(f'{(season['name'].replace(" ", "_")).lower()}_button')

            self.seasons_buttons_grid_layout.addWidget(self.season_button, 0, self.seasons.index(season), 1, 1)

    def attach_connection_to_change_season(self):
        season_buttons = self.season_buttons_scroll_area_widget_contents.findChildren(QPushButton)

        for i in range(len(season_buttons)):
            # Used tip from
            # https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
            # magamig's comment

            season_buttons[i].clicked.connect(lambda state, j=i: self.change_season(j))

    def change_season(self, season_index):
        get_season_synopsis = self.seasons[season_index]['overview']

        get_air_date = self.seasons[season_index]['air_date']
        get_vote_average = self.seasons[season_index]['vote_average']

        if get_season_synopsis == "" and not get_air_date and get_vote_average == 0.0:
            self.synopsis_label.setText("Not yet released.")
            self.year_label.setText("Unknown")

        elif get_season_synopsis == "":
            self.synopsis_label.setText("No information available.")
        else:
            self.synopsis_label.setText(get_season_synopsis)

        if get_air_date:
            get_air_date = (get_air_date.split('-'))[0]
            self.year_label.setText(get_air_date)

        if season_index == 0:
            self.director_label.setText("-")
        elif not self.seasons_directors[self.seasons[season_index]['name']]:
            # If director list is empty
            self.director_label.setText("Unknown")
        elif len(self.seasons_directors[self.seasons[season_index]['name']]) >= 3:
            # Only get the two first directors then add ", etc."
            self.director_label.setText(
                    f"Directed by: {", ".join(self.seasons_directors[self.seasons[season_index]['name']][:2])}, etc.")
        else:
            self.director_label.setText(f"Directed by: {", ".join(self.seasons_directors[self.seasons[season_index]['name']])}")

        # Overwrite self.clicked_season in __init__
        self.clicked_season = self.seasons[season_index]['name']

        self.load_old_rating()
        print(self.clicked_season)

        # print(self.seasons[season_index])
        #
        # season_button.synopsis_label.setText((self.seasons[season_index])['overview'])

    # def add_connection_from_review_button_to_seasons(self):
    #     for season in self.seasons:
    #         # _season is just another name of season, I just can't think of any word other than season
    #         self.add_review_button.clicked.connect(lambda state, _season=season: self.add_review_season(_season))

    def save_rating(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        media_and_ratings = {}

        if self.media_type == "tv":
            media_and_ratings = json.loads(cursor.execute("""SELECT tv_show_own_ratings FROM own_ratings_for_media 
                                                        WHERE account_id=(:account_id)""",
                                                             {"account_id": self.account_id}).fetchone()[0])
        elif self.media_type == "movie":
            media_and_ratings = json.loads(cursor.execute("""SELECT movie_own_ratings FROM own_ratings_for_media 
                                                                WHERE account_id=(:account_id)""",
                                                           {"account_id": self.account_id}).fetchone()[0])

        rated_media = media_and_ratings.keys()

        if self.media_id not in rated_media and self.media_type == "movie":
            media_and_ratings.update({self.media_id: round(self.star_slider.value() / 2, 1)})
        elif self.media_id in rated_media and self.media_type == "movie":
            media_and_ratings[self.media_id] = round(self.star_slider.value() / 2, 1)

        elif self.media_id not in rated_media and self.media_type == "tv":
            media_and_ratings.update({self.media_id: {self.clicked_season: round(self.star_slider.value()/2, 1)}})
        else:
            rated_seasons = media_and_ratings[self.media_id].keys()

            if self.clicked_season not in rated_seasons:
                media_and_ratings[self.media_id].update({self.clicked_season: round(self.star_slider.value()/2, 1)})
            else:
                media_and_ratings[self.media_id][self.clicked_season] = round(self.star_slider.value()/2, 1)

        media_and_ratings_json = json.dumps(media_and_ratings)

        if self.media_type == "tv":
            cursor.execute("""UPDATE own_ratings_for_media SET tv_show_own_ratings=(:tv_show_own_ratings) WHERE
                                                      account_id=(:account_id)""",
                           {"tv_show_own_ratings": media_and_ratings_json, "account_id": self.account_id})

        elif self.media_type == "movie":
            cursor.execute("""UPDATE own_ratings_for_media SET movie_own_ratings=(:movie_own_ratings) WHERE
                                                              account_id=(:account_id)""",
                           {"movie_own_ratings": media_and_ratings_json, "account_id": self.account_id})

        connection.commit()
        connection.close()

    def load_old_rating(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        media_and_ratings = {}

        if self.media_type == "tv":
            media_and_ratings = json.loads(cursor.execute("""SELECT tv_show_own_ratings FROM 
                                                                    own_ratings_for_media WHERE 
                                                                    account_id=(:account_id)""",
                                                             {"account_id": self.account_id}).fetchone()[0])
        elif self.media_type == "movie":
            media_and_ratings = json.loads(cursor.execute("""SELECT movie_own_ratings FROM own_ratings_for_media 
                                                            WHERE account_id=(:account_id)""",
                                                           {"account_id": self.account_id}).fetchone()[0])

        rated_media = media_and_ratings.keys()

        if self.media_id in rated_media and self.media_type == "tv":
            rated_seasons = media_and_ratings[self.media_id].keys()

            if self.clicked_season in rated_seasons:
                self.change_own_rating_slider(old_rating=media_and_ratings[self.media_id][self.clicked_season])

        if self.media_id in rated_media and self.media_type == "movie":
            self.change_own_rating_slider(old_rating=media_and_ratings[self.media_id])

        connection.commit()
        connection.close()

    def split_title(self):
        return '+'.join(self.title.split())
