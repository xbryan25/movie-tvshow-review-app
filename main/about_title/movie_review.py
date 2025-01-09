from main.about_title.media_review_design import Ui_MainWindow as MediaReviewUI

import sqlite3
import json

from PyQt6.QtWidgets import QMainWindow


class MovieReview(QMainWindow, MediaReviewUI):
    def __init__(self, account_id, media_id):
        super().__init__()

        self.setupUi(self)

        self.account_id = account_id
        self.media_id = str(media_id)

        self.show_old_review()

        self.save_button.clicked.connect(self.add_review)

    def show_old_review(self):
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

        movie_reviews = json.loads(cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                                              {"account_id": self.account_id}).fetchone()[0])

        movie_ids = movie_reviews.keys()

        if self.media_id in movie_ids:
            movie_reviews[self.media_id] = self.review_plain_text.toPlainText()
        else:
            movie_reviews.update({self.media_id: self.review_plain_text.toPlainText()})

        movie_reviews_json = json.dumps(movie_reviews)

        cursor.execute("""UPDATE reviews SET movie_reviews=(:movie_reviews) WHERE account_id=(:account_id)""",
                       {"movie_reviews": movie_reviews_json, "account_id": self.account_id})

        connection.commit()
        connection.close()
