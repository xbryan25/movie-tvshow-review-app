from main.about_title.movie_review_design import Ui_MainWindow as MovieReviewUI

from PyQt6.QtWidgets import QMainWindow


class MovieReview(QMainWindow, MovieReviewUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
