from main.about_title.media_review_design import Ui_MainWindow as MediaReviewUI

import sqlite3
import json

from PyQt6.QtWidgets import QMainWindow


class TvShowReview(QMainWindow, MediaReviewUI):
    def __init__(self, account_id, media_id, clicked_season):
        super().__init__()

        self.setupUi(self)

        self.account_id = account_id
        self.media_id = str(media_id)
        self.clicked_season = clicked_season

        # self.show_old_review()

        self.save_button.clicked.connect(self.add_review)

    def show_old_review(self, season):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        movie_reviews = json.loads(
            cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                           {"account_id": self.account_id}).fetchone()[0])

        movie_ids = movie_reviews.keys()

        if self.media_id in movie_ids:
            self.review_plain_text.setPlainText(movie_reviews[self.media_id])

    def add_review(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        current_season = f'Season {self.clicked_season + 1}'

        tv_show_reviews = json.loads(cursor.execute("""SELECT tv_show_reviews FROM reviews WHERE account_id=(:account_id)""",
                                              {"account_id": self.account_id}).fetchone()[0])

        tv_show_ids = tv_show_reviews.keys()

        # tv_show_reviews.update({self.media_id: {season: self.review_plain_text.toPlainText()}})

        if self.media_id in tv_show_ids:
            # Dictionary ni siya
            tv_show_season_reviews = tv_show_reviews[self.media_id]

            reviewed_seasons = tv_show_season_reviews.keys()

            if current_season in reviewed_seasons:
                tv_show_season_reviews[current_season] = self.review_plain_text.toPlainText()
            else:
                tv_show_season_reviews.update({current_season: self.review_plain_text.toPlainText()})

            # tv_show_reviews[self.media_id] = tv_show_season_reviews

        else:
            tv_show_reviews.update({self.media_id: {current_season: self.review_plain_text.toPlainText()}})

        tv_show_reviews_json = json.dumps(tv_show_reviews)

        cursor.execute("""UPDATE reviews SET tv_show_reviews=(:tv_show_reviews) WHERE account_id=(:account_id)""",
                       {"tv_show_reviews": tv_show_reviews_json, "account_id": self.account_id})

        connection.commit()
        connection.close()
