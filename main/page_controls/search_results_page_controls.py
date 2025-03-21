from PyQt6.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy, QFrame, QApplication
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import (QSize, Qt, QPropertyAnimation, QRect, QEvent, QThread, QObject, pyqtSignal, QRunnable,
                          pyqtSlot, QThreadPool, QMetaObject, Q_ARG, QTimer)

from search_results.media_result import MediaResult

from loading_screen.loading_screen import LoadingScreen
from utils.load_pictures_worker import LoadPicturesWorker

import aiohttp
import asyncio
import json


class SearchResultsPageControls:
    def __init__(self, widgets, application_window):

        self.widgets = widgets
        self.application_window = application_window

        self.media_title_to_search = None
        self.account_id = None
        self.api_client = None

        self.num_of_movie_results = 0
        self.num_of_tv_show_results = 0

        self.movie_result_frames = []
        self.tv_show_result_frames = []

        self.load_widgets()

    def load_widgets(self):
        self.showing_results_label = self.widgets[0]

        self.movie_results_label = self.widgets[1]
        self.tv_show_results_label = self.widgets[2]

        self.movie_results_scroll_area = self.widgets[3]
        self.tv_show_results_scroll_area = self.widgets[4]

        self.movie_results_scroll_area_grid_layout = self.widgets[5]
        self.tv_show_results_scroll_area_grid_layout = self.widgets[6]

    def set_media_title_to_search(self, media_title_to_search):
        self.media_title_to_search = media_title_to_search
        self.media_title_to_search_url = (self.media_title_to_search.lower()).replace(" ", "+")

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_api_client(self, api_client):
        self.api_client = api_client

    def set_num_of_media(self, num_of_movie_results, num_of_tv_show_results):
        self.num_of_movie_results = num_of_movie_results
        self.num_of_tv_show_results = num_of_tv_show_results

    def remove_old_search_results(self):
        self.movie_results_scroll_area.verticalScrollBar().setValue(0)
        self.tv_show_results_scroll_area.verticalScrollBar().setValue(0)

        # Delete the MediaResult frames
        for i in range(len(self.movie_result_frames)):
            self.movie_result_frames[i].deleteLater()

        self.movie_result_frames.clear()

        for j in range(len(self.tv_show_result_frames)):
            self.tv_show_result_frames[j].deleteLater()

        self.tv_show_result_frames.clear()

        # Delete the vertical spacers
        for i in range(self.movie_results_scroll_area_grid_layout.count()):
            item = self.movie_results_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.movie_results_scroll_area_grid_layout.removeItem(item)
                break

        for i in range(self.tv_show_results_scroll_area_grid_layout.count()):
            item = self.tv_show_results_scroll_area_grid_layout.itemAt(i)

            if isinstance(item, QSpacerItem):
                self.tv_show_results_scroll_area_grid_layout.removeItem(item)
                break

    async def get_num_of_media(self):
        movie_search_url = f"https://api.themoviedb.org/3/search/movie?query={self.media_title_to_search_url}"
        movie_search_results = await self.api_client.fetch(movie_search_url)

        tv_show_search_url = f"https://api.themoviedb.org/3/search/tv?query={self.media_title_to_search_url}"
        tv_show_search_results = await self.api_client.fetch(tv_show_search_url)

        self.set_num_of_media(len(movie_search_results['results']), len(tv_show_search_results['results']))

    def start_process(self):
        self.remove_old_search_results()

        self.loading_screen = LoadingScreen()
        self.loading_screen.show()

        self.threadpool = QThreadPool()
        self.start_get_num_of_media_results_thread()

    def make_media_result_frames(self, media_type, num):
        self.showing_results_label.setText(f"Showing results for '{self.media_title_to_search}'")

        count = 0

        for count in range(num):
            if media_type == "movie":
                self.movie_result_frame = MediaResult(self.movie_results_scroll_area.widget(), "movie",
                                                      self.account_id, self.application_window)

                self.movie_results_scroll_area_grid_layout.addWidget(self.movie_result_frame, count, 0, 1, 1)

                self.movie_result_frames.append(self.movie_result_frame)

            elif media_type == "tv":
                self.tv_show_result_frame = MediaResult(self.tv_show_results_scroll_area.widget(), "tv",
                                                      self.account_id, self.application_window)

                self.tv_show_results_scroll_area_grid_layout.addWidget(self.tv_show_result_frame, count, 0, 1, 1)

                self.tv_show_result_frames.append(self.tv_show_result_frame)

        vertical_spacer_for_media_results = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        if media_type == "movie":
            self.movie_results_scroll_area_grid_layout.addItem(vertical_spacer_for_media_results, count + 1, 0, 1, 1)
        elif media_type == "tv":
            self.tv_show_results_scroll_area_grid_layout.addItem(vertical_spacer_for_media_results, count + 1, 0, 1, 1)

    def start_get_num_of_media_results_thread(self):
        self.load_search_media_worker = LoadPicturesWorker(self.get_num_of_media, self.api_client)

        self.load_search_media_worker.signals.finished.connect(
            lambda: self.make_media_result_frames("movie", self.num_of_movie_results))

        self.load_search_media_worker.signals.finished.connect(
            lambda: self.make_media_result_frames("tv", self.num_of_tv_show_results))

        self.load_search_media_worker.signals.finished.connect(lambda: self.start_show_search_results_thread())

        self.threadpool.start(self.load_search_media_worker)

    def start_show_search_results_thread(self):
        self.load_pictures_worker = LoadPicturesWorker(self.show_search_results, self.api_client)

        self.load_pictures_worker.signals.finished.connect(self.loading_screen.close)

        self.load_pictures_worker.signals.finished.connect(lambda: self.application_window.
                                                           subpage_stacked_widget.
                                                           setCurrentWidget(self.application_window.search_results_subpage))

        self.threadpool.start(self.load_pictures_worker)

    async def show_search_results(self):
        movie_search_url = f"https://api.themoviedb.org/3/search/movie?query={self.media_title_to_search_url}"
        movie_search_results = await self.api_client.fetch(movie_search_url)

        tv_show_search_url = f"https://api.themoviedb.org/3/search/tv?query={self.media_title_to_search_url}"
        tv_show_search_results = await self.api_client.fetch(tv_show_search_url)

        total_search_results_count = len(movie_search_results['results']) + len(tv_show_search_results['results'])

        # -------------------------------------------------------------------------------------------------

        movie_search_result_img_urls = []

        for count, movie_search_result in enumerate(movie_search_results['results']):
            self.movie_result_frames[count].set_media_id(movie_search_result['id'])
            self.movie_result_frames[count].set_media_title(movie_search_result['title'])
            self.movie_result_frames[count].set_short_info("???")

            if movie_search_result['release_date'] == '':
                self.movie_result_frames[count].set_media_release_year("Unknown")
            else:
                self.movie_result_frames[count].set_media_release_year((movie_search_result['release_date'].split('-'))[0])

            if not movie_search_result['poster_path']:
                movie_search_result_img_urls.append("")
            else:
                movie_search_result_img_urls.append(f'https://image.tmdb.org/t/p/w154/{movie_search_result['poster_path']}')

        movie_search_result_img_contents = await self.api_client.fetch_all_images(movie_search_result_img_urls,
                                                                                  self.loading_screen.loading_progress_bar,
                                                                                  0,
                                                                                  total_search_results_count)

        for i in range(len(movie_search_result_img_contents)):
            if movie_search_result_img_contents[i] != "":
                media_image = QImage()
                media_image.loadFromData(movie_search_result_img_contents[i])

                self.movie_result_frames[i].set_media_poster(QPixmap(media_image))
            else:
                question_mark_image = QPixmap("../assets/images/question_mark.jpg")
                self.movie_result_frames[i].set_media_poster(question_mark_image)

        # --------------------------------------------------------------------------------------------

        tv_show_search_result_img_urls = []

        for count, tv_show_search_result in enumerate(tv_show_search_results['results']):
            self.tv_show_result_frames[count].set_media_id(tv_show_search_result['id'])
            self.tv_show_result_frames[count].set_media_title(tv_show_search_result['name'])
            self.tv_show_result_frames[count].set_short_info("???")

            if tv_show_search_result['first_air_date'] == '':
                self.tv_show_result_frames[count].set_media_release_year("Unknown")
            else:
                self.tv_show_result_frames[count].set_media_release_year(
                    (tv_show_search_result['first_air_date'].split('-'))[0])

            if not tv_show_search_result['poster_path']:
                tv_show_search_result_img_urls.append("")
            else:
                tv_show_search_result_img_urls.append(
                    f'https://image.tmdb.org/t/p/w154/{tv_show_search_result['poster_path']}')

        tv_show_search_result_img_contents = await self.api_client.fetch_all_images(tv_show_search_result_img_urls,
                                                                                    self.loading_screen.loading_progress_bar,
                                                                                    self.num_of_movie_results,
                                                                                    total_search_results_count)

        for i in range(len(tv_show_search_result_img_contents)):
            if tv_show_search_result_img_contents[i] != "":
                media_image = QImage()
                media_image.loadFromData(tv_show_search_result_img_contents[i])

                self.tv_show_result_frames[i].set_media_poster(QPixmap(media_image))
            else:
                question_mark_image = QPixmap("../assets/images/question_mark.jpg")
                self.tv_show_result_frames[i].set_media_poster(question_mark_image)
