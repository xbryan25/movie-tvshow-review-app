from os.path import split

from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import QSize, Qt

from main.about_title.about_title_tv_show_design import Ui_MainWindow as AboutTitleTvShowDesignUI
from main.about_title.tv_show_review import TvShowReview

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import requests
import sqlite3
import json


class AboutTitleTvShowPage(QMainWindow, AboutTitleTvShowDesignUI):
    def __init__(self, media_id, account_id):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.media_id = media_id
        self.account_id = account_id

        # To be overwritten later
        self.media_title = ""
        self.seasons = []
        self.clicked_season = 'Series'

        self.directors = {}


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

        self.load_season_buttons()

        self.star_slider.valueChanged.connect(self.change_own_rating_slider)

        self.add_to_liked_button.clicked.connect(self.add_to_liked)

        self.add_to_watchlist_button.clicked.connect(self.add_to_watchlist)

        self.add_review_button.clicked.connect(self.add_review_season)

        self.set_pointing_hand_cursor_to_interactables()

    def set_pointing_hand_cursor_to_interactables(self):
        self.add_to_liked_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_to_watchlist_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.star_slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_review_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.season_buttons_scroll_area.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        season_buttons = self.season_buttons_scroll_area_widget_contents.findChildren(QPushButton)

        for season_button in season_buttons:
            season_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def load_contents(self):
        tv_show_url = f"https://api.themoviedb.org/3/tv/{self.media_id}"
        tv_show_response = requests.get(tv_show_url, headers=self.api_headers).json()

        # To be used in the class
        self.media_title = tv_show_response['name']
        tv_show_overview = tv_show_response['overview']
        tv_show_vote_average = tv_show_response['vote_average']
        tv_show_release_year = (tv_show_response['first_air_date'].split('-'))[0]
        tv_show_img_url = 'https://image.tmdb.org/t/p/original' + tv_show_response['poster_path']
        tv_show_genres = self.get_genres(tv_show_response['genres'])

        self.seasons = tv_show_response['seasons']

        self.add_series_dictionary(tv_show_response['number_of_episodes'], tv_show_response['vote_average'],
                                   tv_show_response['overview'], tv_show_response['id'])
        # print(movie_overview)
        # print(movie_vote_average)
        # print(movie_release_year)
        #
        self.title_label.setText(self.media_title)
        self.year_label.setText(str(tv_show_release_year))
        self.general_stars_label.setText(str(tv_show_vote_average))
        self.synopsis_label.setText(tv_show_overview)
        self.director_label.setText("-")
        self.genres_label.setText("Genres: " + tv_show_genres)

        self.get_directors()

        tv_show_image = QImage()
        tv_show_image.loadFromData(requests.get(tv_show_img_url).content)

        self.poster_label.setPixmap(QPixmap(tv_show_image))
        self.poster_label.setScaledContents(True)

    def add_series_dictionary(self, number_of_episodes, vote_average, overview, id):
        # Shallow copies (meaning nested entries are not read) the first season of the show
        series_dictionary = dict(self.seasons[0])

        series_dictionary['name'] = 'Series'

        series_dictionary['episode_count'] = number_of_episodes
        series_dictionary['vote_average'] = vote_average
        series_dictionary['overview'] = overview
        series_dictionary['id'] = id

        self.seasons.insert(0, series_dictionary)

    def set_liked_button_state(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        liked_tv_shows = json.loads(
            cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        if self.media_id in liked_tv_shows:
            self.add_to_liked_button.setText("Remove from Liked")

            self.add_to_liked_state = "clicked"

    def set_watchlist_button_state(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        tv_shows_to_watch = json.loads(
            cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        if self.media_id in tv_shows_to_watch:
            self.add_to_watchlist_button.setText("Remove from Watchlist")

            self.add_to_watchlist_state = "clicked"

        connection.commit()
        connection.close()

    def set_review_button_state(self):
        pass
        # connection = sqlite3.connect('database\\accounts.db')
        # cursor = connection.cursor()
        #
        # movie_reviews = json.loads(
        #     cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
        #                    {"account_id": self.account_id}).fetchone()[0])
        #
        # movie_ids = movie_reviews.keys()
        #
        # if str(self.media_id) in movie_ids:
        #     self.add_review_button.setText("Edit Review")
        #
        # connection.commit()
        # connection.close()

    def get_directors(self):
        # Make a copy of self.seasons but without the series, which is the first element

        seasons_without_series = list(self.seasons[1:])
        print("\n---------START----------\n")
        for season in seasons_without_series:
            season_directors = []

            tv_show_season_credit_url = f"https://api.themoviedb.org/3/tv/{self.media_id}/season/{season['season_number']}"
            tv_credit_response = requests.get(tv_show_season_credit_url, headers=self.api_headers).json()

            for episode_credits in tv_credit_response['episodes']:

                # Check if episode_credits['crew'] (a list) is empty or not
                if episode_credits['crew']:
                    for crew in episode_credits['crew']:

                        if crew['job'] == 'Director':
                            episode_director_name = crew['name']

                            if episode_director_name not in season_directors:
                                season_directors.append(episode_director_name)

            self.directors.update({season['name']: season_directors})

        print(self.directors)


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

        # Same thing with the liked_tv_shows_column
        liked_tv_shows = json.loads(cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                                      {"account_id": self.account_id}).fetchone()[0])

        if self.add_to_liked_state == "not clicked":
            self.add_to_liked_button.setText("Remove from Liked")

            if self.media_id not in liked_tv_shows:
                liked_tv_shows.append(self.media_id)

                # Converts the list into a json
                liked_tv_shows_json = json.dumps(liked_tv_shows)

                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": liked_tv_shows_json, "account_id": self.account_id})

            self.add_to_liked_state = "clicked"
        else:
            self.add_to_liked_button.setText("Add to Liked")

            if self.media_id in liked_tv_shows:
                liked_tv_shows.pop(liked_tv_shows.index(self.media_id))

                # Converts the list into a json
                liked_tv_shows_json = json.dumps(liked_tv_shows)

                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": liked_tv_shows_json, "account_id": self.account_id})

            self.add_to_liked_state = "not clicked"

        connection.commit()
        connection.close()

    def add_to_watchlist(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        tv_shows_to_watch = json.loads(
            cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        if self.add_to_watchlist_state == "not clicked":
            self.add_to_watchlist_button.setText("Remove from Watchlist")

            if self.media_id not in tv_shows_to_watch:
                tv_shows_to_watch.append(self.media_id)

                # Converts the list into a json
                tv_shows_to_watch_json = json.dumps(tv_shows_to_watch)

                cursor.execute(
                    """UPDATE media_to_watch SET tv_shows_to_watch=(:tv_shows_to_watch) WHERE account_id=(:account_id)""",
                    {"tv_shows_to_watch": tv_shows_to_watch_json, "account_id": self.account_id})

            self.add_to_watchlist_state = "clicked"
        else:
            self.add_to_watchlist_button.setText("Add to Watchlist")

            if self.media_id in tv_shows_to_watch:
                tv_shows_to_watch.pop(tv_shows_to_watch.index(self.media_id))

                # Converts the list into a json
                tv_shows_to_watch_json = json.dumps(tv_shows_to_watch)

                cursor.execute(
                    """UPDATE media_to_watch SET tv_shows_to_watch=(:tv_shows_to_watch) WHERE account_id=(:account_id)""",
                    {"tv_shows_to_watch": tv_shows_to_watch_json, "account_id": self.account_id})

            self.add_to_watchlist_state = "not clicked"

        connection.commit()
        connection.close()

    def load_season_buttons(self):
        for season in self.seasons:
            # Don't forget to change QLabel to Poster

            self.season_button = QPushButton(parent=self.season_buttons_scroll_area_widget_contents)
            self.season_button.setMinimumSize(QSize(250, 25))
            self.season_button.setMaximumSize(QSize(250, 25))

            font = QFont()
            font.setFamily("Oswald")
            font.setPointSize(10)
            self.season_button.setFont(font)

            self.season_button.setText(season['name'])
            self.season_button.setObjectName(f'{(season['name'].replace(" ", "_")).lower()}_button')
            print(f'{(season['name'].replace(" ", "_")).lower()}_button')

            self.seasons_buttons_grid.addWidget(self.season_button, 0, self.seasons.index(season), 1, 1)

        self.attach_connection_to_change_season()

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
        elif not self.directors[self.seasons[season_index]['name']]:
            # If director list is empty
            self.director_label.setText("Unknown")
        else:
            self.director_label.setText(f"Directed by: {", ".join(self.directors[self.seasons[season_index]['name']])}")

        # Overwrite self.clicked_season in __init__
        self.clicked_season = self.seasons[season_index]['name']
        print(self.clicked_season)

        # print(self.seasons[season_index])
        #
        # season_button.synopsis_label.setText((self.seasons[season_index])['overview'])

    # def add_connection_from_review_button_to_seasons(self):
    #     for season in self.seasons:
    #         # _season is just another name of season, I just can't think of any word other than season
    #         self.add_review_button.clicked.connect(lambda state, _season=season: self.add_review_season(_season))

    def add_review_season(self):
        self.tv_show_review = TvShowReview(self.account_id, self.media_id, self.clicked_season)
        self.tv_show_review.title_label.setText(f"{self.media_title} | {self.clicked_season}")

        self.tv_show_review.show()
    def split_title(self):
        return '+'.join(self.title.split())
