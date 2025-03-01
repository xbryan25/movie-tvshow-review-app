from PyQt6.QtCore import QFileInfo

from search_results.search_results_design import Ui_MainWindow as SearchResultsPageUI
from search_results.media_result import MediaResult

from PyQt6.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap

import requests


class SearchResultsPage(QMainWindow, SearchResultsPageUI):
    def __init__(self, media_title, account_id, requests_session_tmdb, requests_session_images):
        super().__init__()

        self.setupUi(self)

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

        self.media_title = media_title
        self.media_title_for_url = (self.media_title.lower()).replace(" ", "+")
        self.account_id = account_id

        self.show_search_results()

    def show_search_results(self):
        self.show_results_label.setText(f"Showing results for '{self.media_title}'")

        movie_search_url = f"https://api.themoviedb.org/3/search/movie?query={self.media_title_for_url}"
        movie_search_results = self.requests_session_tmdb.get(movie_search_url, headers=self.api_headers).json()

        # Only the top 5 movies will be shown as search results
        for count, movie in enumerate(movie_search_results['results']):
            self.media_result_frame = MediaResult(self.results_scroll_area_contents, movie['id'], "movie",
                                                  self.account_id, self.requests_session_tmdb,
                                                  self.requests_session_tmdb)

            self.media_result_frame.media_title.setText(movie['title'])

            if not movie['poster_path']:
                # Crab and Squid Save the Ocean

                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.media_result_frame.media_poster.setPixmap(question_mark_image)

            else:
                media_img_url = f'https://image.tmdb.org/t/p/w154/{movie['poster_path']}'

                media_image = QImage()
                media_image.loadFromData(self.requests_session_images.get(media_img_url,
                                                                          headers=self.api_headers).content)

                self.media_result_frame.media_poster.setPixmap(QPixmap(media_image))

            if movie['release_date'] == '':
                self.media_result_frame.media_release_year.setText("Unknown")
            else:
                self.media_result_frame.media_release_year.setText((movie['release_date'].split('-'))[0])

            self.media_result_frame.media_type_label.setText("Movie")
            self.media_result_frame.media_short_info.setText("???")

            self.verticalLayout_2.addWidget(self.media_result_frame)

            print(f"{((count + 1) / 10) * 100:.2f}")

            if count + 1 == 5:
                print("Broke free")
                break

        tv_show_search_url = f"https://api.themoviedb.org/3/search/tv?query={self.media_title_for_url}"
        tv_show_search_results = self.requests_session_tmdb.get(tv_show_search_url, headers=self.api_headers).json()

        # print(tv_show_search_results)

        # Only the top 5 tv shows will be shown as search results
        for count, tv_show in enumerate(tv_show_search_results['results']):
            self.media_result_frame = MediaResult(self.results_scroll_area_contents, tv_show['id'], "tv",
                                                  self.account_id, self.requests_session_tmdb,
                                                  self.requests_session_images)

            self.media_result_frame.media_title.setText(tv_show['name'])

            if not tv_show['poster_path']:
                # Crab and Squid Save the Ocean

                # print(QPixmap("../../images/question_mark.jpg"))

                question_mark_image = QPixmap("../images/question_mark.jpg")
                #
                self.media_result_frame.media_poster.setPixmap(question_mark_image)
                # self.media_result_frame.media_title.setText(tv_show['name'])
            else:
                media_img_url = f'https://image.tmdb.org/t/p/w154/{tv_show['poster_path']}'

                media_image = QImage()
                media_image.loadFromData(self.requests_session_images.get(media_img_url,
                                                                          headers=self.api_headers).content)

                self.media_result_frame.media_poster.setPixmap(QPixmap(media_image))
                # self.media_result_frame.media_title.setText(tv_show['name'])

            if tv_show['first_air_date'] == '':
                self.media_result_frame.media_release_year.setText("Unknown")
            else:
                self.media_result_frame.media_release_year.setText((tv_show['first_air_date'].split('-'))[0])

            self.media_result_frame.media_type_label.setText("TV Show")
            self.media_result_frame.media_short_info.setText("???")

            self.verticalLayout_2.addWidget(self.media_result_frame)

            print(f"{((count + 6) / 10) * 100:.2f}")

            if count + 1 == 5:
                print("Broke free")
                break

        vertical_spacer_for_search_results = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(vertical_spacer_for_search_results)
