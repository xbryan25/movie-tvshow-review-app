from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QMainWindow, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize, QThreadPool

from dialogs.operation_confirmation_dialog import OperationConfirmationDialog

from utils.liked_to_watch_reviewed_media_result import LikedToWatchReviewedMediaResult

from loading_screen.loading_screen import LoadingScreen
from utils.load_pictures_worker import LoadPicturesWorker

import sqlite3
import json
import requests

class LikedToWatchReviewedPageControls:
    def __init__(self, widgets, application_window):

        self.widgets = widgets
        self.application_window = application_window

        self.account_id = None
        self.state_to_show = None
        self.api_client = None

        self.l_tw_r_movies = None
        self.l_tw_r_tv_shows = None

        self.l_tw_r_movies_num = None
        self.l_tw_r_tv_shows_num = None
        self.total_l_tw_r_media = None

        self.l_tw_r_movie_frames = []
        self.l_tw_r_tv_show_frames = []

        self.load_widgets()

        self.first_name = ""

    def load_widgets(self):
        self.l_tw_r_header_label = self.widgets[0]
        self.l_tw_r_movies_label = self.widgets[1]
        self.l_tw_r_tv_shows_label = self.widgets[2]
        self.l_tw_r_movies_scroll_area = self.widgets[3]
        self.l_tw_r_tv_shows_scroll_area = self.widgets[4]
        self.l_tw_r_movies_scroll_area_contents = self.widgets[5]
        self.l_tw_r_tv_shows_scroll_area_contents = self.widgets[6]
        self.l_tw_r_movies_scroll_area_grid_layout = self.widgets[7]
        self.l_tw_r_tv_shows_scroll_area_grid_layout = self.widgets[8]

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_state_to_show(self, state_to_show):
        self.state_to_show = state_to_show

    def set_api_client(self, api_client):
        self.api_client = api_client

    def initialize_page(self):
        self.get_first_name()
        self.edit_window_title()

    def get_first_name(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        self.first_name = cursor.execute("""SELECT firstname FROM accounts WHERE account_id=(:account_id)""",
                                         {'account_id': self.account_id}).fetchone()[0]

        connection.commit()
        connection.close()

    def start_process(self):
        self.initialize_page()
        self.clear_all_media()

        self.get_movies_and_tv_shows_from_database()

        self.make_media_result_frames(len(self.l_tw_r_movies), len(self.l_tw_r_tv_shows))

        self.loading_screen = LoadingScreen()

        # Don't show loading screen of there are no media
        if self.l_tw_r_movies_num != 0 and self.l_tw_r_tv_shows_num != 0:
            self.loading_screen.show()

        self.threadpool = QThreadPool()
        self.start_show_results_thread()

    def edit_window_title(self):

        if self.state_to_show == "liked":
            self.application_window.setWindowTitle(f"{self.first_name}'s Liked Media")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Liked Media")
        elif self.state_to_show == "to_watch":
            self.application_window.setWindowTitle(f"{self.first_name}'s Media to Watch")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Media to Watch")
        elif self.state_to_show == "reviewed":
            self.application_window.setWindowTitle(f"{self.first_name}'s Reviewed Media")
            self.l_tw_r_header_label.setText(f"{self.first_name}'s Reviewed Media")

    def clear_all_media(self):
        self.l_tw_r_movies_scroll_area.verticalScrollBar().setValue(0)
        self.l_tw_r_tv_shows_scroll_area.verticalScrollBar().setValue(0)

        # Delete the MediaResult frames
        for i in range(len(self.l_tw_r_movie_frames)):
            self.l_tw_r_movie_frames[i].deleteLater()

        self.l_tw_r_movie_frames.clear()

        for j in range(len(self.l_tw_r_tv_show_frames)):
            self.l_tw_r_tv_show_frames[j].deleteLater()

        self.l_tw_r_tv_show_frames.clear()

        # Delete the vertical spacers
        for i in range(self.l_tw_r_movies_scroll_area_grid_layout.count()):
            item = self.l_tw_r_movies_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.l_tw_r_movies_scroll_area_grid_layout.removeItem(item)
                break

        for i in range(self.l_tw_r_tv_shows_scroll_area_grid_layout.count()):
            item = self.l_tw_r_tv_shows_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.l_tw_r_tv_shows_scroll_area_grid_layout.removeItem(item)
                break

    def get_movies_and_tv_shows_from_database(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if self.state_to_show == "liked":
            self.l_tw_r_movies = json.loads(
                cursor.execute("""SELECT liked_movies FROM liked_media WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            self.l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT liked_tv_shows FROM liked_media WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])
        elif self.state_to_show == "to_watch":
            self.l_tw_r_movies = json.loads(
                cursor.execute("""SELECT movies_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            self.l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT tv_shows_to_watch FROM media_to_watch WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])
        else:
            self.l_tw_r_movies = json.loads(
                cursor.execute("""SELECT movie_reviews FROM reviews WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

            self.l_tw_r_tv_shows = json.loads(
                cursor.execute("""SELECT tv_show_reviews FROM reviews WHERE account_id=(:account_id)""",
                               {'account_id': self.account_id}).fetchone()[0])

        self.l_tw_r_movies_num = len(self.l_tw_r_movies)
        self.l_tw_r_tv_shows_num = len(self.l_tw_r_tv_shows)

        self.total_l_tw_r_media = self.l_tw_r_movies_num + self.l_tw_r_tv_shows_num

        connection.commit()
        connection.close()

    def make_media_result_frames(self, num_of_movies, num_of_tv_shows):
        # Pushes movie frames to the right
        left_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Minimum)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(left_v_spacer, 0, 0, 1, 1)

        # Pushes movie frames to the left
        right_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(right_v_spacer, 0, 2, 1, 1)

        count = 0

        for count in range(num_of_movies):
            self.l_tw_r_movie_frame = LikedToWatchReviewedMediaResult(self.l_tw_r_movies_scroll_area, "movie",
                                                                      self.account_id, self.application_window,
                                                                      self.state_to_show)

            self.l_tw_r_movies_scroll_area_grid_layout.addWidget(self.l_tw_r_movie_frame, count, 1, 1, 1)

            self.l_tw_r_movie_frames.append(self.l_tw_r_movie_frame)

        # Pushes movie frames up
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)

        self.l_tw_r_movies_scroll_area_grid_layout.addItem(spacerItem1,
                                                           count + 1, 1, 1, 1)

        # -----------------------------------------------------------------------------------------------

        # Pushes tv_show frames to the right
        left_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Minimum)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(left_v_spacer,
                                                             0, 0, 1, 1)

        # Pushes movie frames to the left
        right_v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(right_v_spacer,
                                                             0, 2, 1, 1)

        count = 0

        for count in range(num_of_tv_shows):
            self.l_tw_r_tv_show_frame = LikedToWatchReviewedMediaResult(self.l_tw_r_tv_shows_scroll_area, "tv",
                                                                        self.account_id, self.application_window,
                                                                        self.state_to_show)

            self.l_tw_r_tv_shows_scroll_area_grid_layout.addWidget(self.l_tw_r_tv_show_frame, count, 1, 1, 1)

            self.l_tw_r_tv_show_frames.append(self.l_tw_r_tv_show_frame)

        # Pushes tv show frames up
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)

        self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(spacerItem2,
                                                             count + 1, 1, 1, 1)

    def add_remove_button_operation_to_frames(self):
        for l_tw_r_movie_frame in self.l_tw_r_movie_frames:
            l_tw_r_movie_frame.add_remove_button_operation(self.l_tw_r_movies, self)

        for l_tw_r_tv_show_frame in self.l_tw_r_tv_show_frames:
            l_tw_r_tv_show_frame.add_remove_button_operation(self.l_tw_r_tv_shows, self)

    def start_show_results_thread(self):
        self.load_pictures_worker = LoadPicturesWorker(self.load_l_tw_r_media_contents, self.api_client)

        self.load_pictures_worker.signals.finished.connect(self.loading_screen.close)

        if self.state_to_show != 'reviewed':
            self.load_pictures_worker.signals.finished.connect(self.add_remove_button_operation_to_frames)

        self.load_pictures_worker.signals.finished.connect(lambda: self.application_window.
                                                           subpage_stacked_widget.
                                                           setCurrentWidget(self.application_window.l_tw_r_subpage))

        self.threadpool.start(self.load_pictures_worker)

    async def load_l_tw_r_media_contents(self):

        movie_img_urls = []

        for count, l_tw_r_movie in enumerate(self.l_tw_r_movies):
            movie_url = f"https://api.themoviedb.org/3/movie/{l_tw_r_movie}"

            movie_response = await self.api_client.fetch(movie_url)

            self.l_tw_r_movie_frames[count].set_media_id(l_tw_r_movie)
            self.l_tw_r_movie_frames[count].set_media_title(movie_response['title'])
            self.l_tw_r_movie_frames[count].set_media_release_year((movie_response['release_date'].split('-'))[0])
            self.l_tw_r_movie_frames[count].set_media_short_info(f"{movie_response['runtime']} minutes")

            if movie_response['poster_path']:
                movie_img_url = 'https://image.tmdb.org/t/p/w92/' + movie_response['poster_path']
                movie_img_urls.append(movie_img_url)

            else:
                movie_img_urls.append("")

        movie_img_contents = await self.api_client.fetch_all_images(movie_img_urls,
                                                                    self.loading_screen.loading_progress_bar,
                                                                    0,
                                                                    self.total_l_tw_r_media)

        for i in range(len(movie_img_contents)):
            if movie_img_contents[i]:
                movie_image = QImage()
                movie_image.loadFromData(movie_img_contents[i])

                self.l_tw_r_movie_frames[i].set_media_poster(QPixmap(movie_image))
            else:
                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.l_tw_r_movie_frames[i].setPixmap(question_mark_image)

        # -----------------------------------------------------------------------------------------------

        tv_show_img_urls = []

        for count, l_tw_r_tv_show in enumerate(self.l_tw_r_tv_shows):
            tv_show_url = f"https://api.themoviedb.org/3/tv/{l_tw_r_tv_show}"

            tv_show_response = await self.api_client.fetch(tv_show_url)

            self.l_tw_r_tv_show_frames[count].set_media_id(l_tw_r_tv_show)
            self.l_tw_r_tv_show_frames[count].set_media_title(tv_show_response['name'])
            self.l_tw_r_tv_show_frames[count].set_media_release_year((tv_show_response['first_air_date'].split('-'))[0])
            self.l_tw_r_tv_show_frames[count].set_media_short_info(f"{tv_show_response['number_of_seasons']} seasons")


            if tv_show_response['poster_path']:
                tv_show_img_url = 'https://image.tmdb.org/t/p/w92/' + tv_show_response['poster_path']
                tv_show_img_urls.append(tv_show_img_url)

            else:
                tv_show_img_urls.append("")

        tv_show_img_contents = await self.api_client.fetch_all_images(tv_show_img_urls,
                                                                      self.loading_screen.loading_progress_bar,
                                                                      len(self.l_tw_r_movies) + 1,
                                                                      self.total_l_tw_r_media)

        for i in range(len(tv_show_img_contents)):
            if tv_show_img_contents[i]:
                tv_show_image = QImage()
                tv_show_image.loadFromData(tv_show_img_contents[i])

                self.l_tw_r_tv_show_frames[i].set_media_poster(QPixmap(tv_show_image))
            else:
                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.l_tw_r_tv_show_frames[i].setPixmap(question_mark_image)

    def remove_media(self, frame, media, media_list, media_type):
        self.confirmation_dialog = OperationConfirmationDialog(media_type, self.state_to_show)
        self.confirmation_dialog.exec()

        if self.confirmation_dialog.get_confirm_state():
            self.rearrange_layout(frame, media_type)

            frame.hide()
            frame.deleteLater()

            media_list.remove(media)
            media_json = json.dumps(media_list)

            self.update_database_after_removing(media_type, media_json)

    def update_database_after_removing(self, media_type, media_json):

        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if media_type == "movie":
            if self.state_to_show == "liked":
                cursor.execute("""UPDATE liked_media SET liked_movies=(:liked_movies) WHERE account_id=(:account_id)""",
                               {"liked_movies": media_json, "account_id": self.account_id})
            elif self.state_to_show == "to_watch":
                cursor.execute("""UPDATE media_to_watch SET movies_to_watch=(:movies_to_watch) WHERE account_id=(:account_id)""",
                               {"movies_to_watch": media_json, "account_id": self.account_id})

        elif media_type == "tv":
            if self.state_to_show == "liked":
                cursor.execute("""UPDATE liked_media SET liked_tv_shows=(:liked_tv_shows) WHERE account_id=(:account_id)""",
                               {"liked_tv_shows": media_json, "account_id": self.account_id})
            elif self.state_to_show == "to_watch":
                cursor.execute(
                    """UPDATE media_to_watch SET tv_shows_to_watch=(:tv_shows_to_watch) WHERE account_id=(:account_id)""",
                    {"tv_shows_to_watch": media_json, "account_id": self.account_id})

        connection.commit()
        connection.close()

    def rearrange_layout(self, frame, media_type):
        if media_type == "movie":

            # Remove v_spacer
            v_spacer = self.l_tw_r_movies_scroll_area_grid_layout.itemAtPosition(len(self.l_tw_r_movie_frames), 1)
            self.l_tw_r_movies_scroll_area_grid_layout.removeItem(v_spacer)

            count = 0

            for movie_frame in self.l_tw_r_movie_frames:
                # Transfer frames one row up
                self.l_tw_r_movies_scroll_area_grid_layout.removeWidget(movie_frame)

                if movie_frame != frame:

                    self.l_tw_r_movies_scroll_area_grid_layout.addWidget(movie_frame, count, 1, 1, 1)

                    count += 1

            # Add v_spacer again
            v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding)
            self.l_tw_r_movies_scroll_area_grid_layout.addItem(v_spacer, count + 1, 1, 1, 1)

        elif media_type == "tv":

            # Remove v_spacer
            v_spacer = self.l_tw_r_tv_shows_scroll_area_grid_layout.itemAtPosition(len(self.l_tw_r_tv_show_frames) + 1, 1)
            self.l_tw_r_tv_shows_scroll_area_grid_layout.removeItem(v_spacer)

            count = 0

            for tv_show_frame in self.l_tw_r_tv_show_frames:
                # Transfer frames one row up
                self.l_tw_r_tv_shows_scroll_area_grid_layout.removeWidget(tv_show_frame)

                if tv_show_frame != frame:
                    self.l_tw_r_tv_shows_scroll_area_grid_layout.addWidget(tv_show_frame, count, 1, 1, 1)

                    count += 1

            # Add v_spacer again
            v_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.l_tw_r_tv_shows_scroll_area_grid_layout.addItem(v_spacer, count + 1, 1, 1, 1)

