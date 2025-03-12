from PyQt6.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy, QFrame
from PyQt6.QtGui import QImage, QPixmap

from search_results.media_result import MediaResult


class SearchResultsPageControls:
    def __init__(self, widgets, application_window):
        super().__init__()

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.widgets = widgets
        self.application_window = application_window

        self.media_title_to_search = None
        self.account_id = None
        self.requests_session_tmdb = None
        self.requests_session_images = None

        self.load_widgets()

        # self.show_search_results()

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

    def set_requests_session(self, requests_session_tmdb, requests_session_images):
        self.requests_session_tmdb = requests_session_tmdb
        self.requests_session_images = requests_session_images

    def remove_old_search_results(self):
        self.movie_results_scroll_area.verticalScrollBar().setValue(0)
        self.tv_show_results_scroll_area.verticalScrollBar().setValue(0)

        movie_results_scroll_area_children = self.movie_results_scroll_area.widget().findChildren(MediaResult)
        tv_show_results_scroll_area_children = self.tv_show_results_scroll_area.widget().findChildren(MediaResult)

        # Delete the MediaResult frames
        for movie_results_scroll_area_child in movie_results_scroll_area_children:
            movie_results_scroll_area_child.deleteLater()

        for tv_show_results_scroll_area_child in tv_show_results_scroll_area_children:
            tv_show_results_scroll_area_child.deleteLater()

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


    def show_search_results(self):
        self.showing_results_label.setText(f"Showing results for '{self.media_title_to_search}'")

        movie_search_url = f"https://api.themoviedb.org/3/search/movie?query={self.media_title_to_search_url}"
        movie_search_results = self.requests_session_tmdb.get(movie_search_url, headers=self.api_headers).json()

        count = 0

        # Only the top 5 movies will be shown as search results
        for count, movie in enumerate(movie_search_results['results']):
            self.movie_result_frame = MediaResult(self.movie_results_scroll_area.widget(), movie['id'], "movie",
                                                  self.account_id, self.requests_session_tmdb,
                                                  self.requests_session_images, self.application_window)

            self.movie_result_frame.media_title.setText(movie['title'])

            if not movie['poster_path']:
                # Crab and Squid Save the Ocean

                question_mark_image = QPixmap("../images/question_mark.jpg")
                self.movie_result_frame.media_poster.setPixmap(question_mark_image)

            else:
                media_img_url = f'https://image.tmdb.org/t/p/w154/{movie['poster_path']}'

                media_image = QImage()
                media_image.loadFromData(self.requests_session_images.get(media_img_url,
                                                                          headers=self.api_headers).content)

                self.movie_result_frame.media_poster.setPixmap(QPixmap(media_image))

            if movie['release_date'] == '':
                self.movie_result_frame.media_release_year.setText("Unknown")
            else:
                self.movie_result_frame.media_release_year.setText((movie['release_date'].split('-'))[0])

            self.movie_result_frame.media_short_info.setText("???")

            self.movie_results_scroll_area_grid_layout.addWidget(self.movie_result_frame, count, 0, 1, 1)

            if count + 1 == 5:
                break

        vertical_spacer_for_movie_results = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                                        QSizePolicy.Policy.Expanding)

        self.movie_results_scroll_area_grid_layout.addItem(vertical_spacer_for_movie_results, count + 1, 0, 1, 1)

        # --------------------------------------------------------------------------------------------

        tv_show_search_url = f"https://api.themoviedb.org/3/search/tv?query={self.media_title_to_search_url}"
        tv_show_search_results = self.requests_session_tmdb.get(tv_show_search_url, headers=self.api_headers).json()

        count = 0

        # Only the top 5 tv shows will be shown as search results
        for count, tv_show in enumerate(tv_show_search_results['results']):

            self.tv_show_result_frame = MediaResult(self.tv_show_results_scroll_area.widget(), tv_show['id'], "tv",
                                                    self.account_id, self.requests_session_tmdb,
                                                    self.requests_session_images, self.application_window)

            self.tv_show_result_frame.media_title.setText(tv_show['name'])

            if not tv_show['poster_path']:
                # Crab and Squid Save the Ocean

                question_mark_image = QPixmap("../images/question_mark.jpg")

                self.tv_show_result_frame.media_poster.setPixmap(question_mark_image)
            else:
                media_img_url = f'https://image.tmdb.org/t/p/w154/{tv_show['poster_path']}'

                media_image = QImage()
                media_image.loadFromData(self.requests_session_images.get(media_img_url,
                                                                          headers=self.api_headers).content)

                self.tv_show_result_frame.media_poster.setPixmap(QPixmap(media_image))

            if tv_show['first_air_date'] == '':
                self.tv_show_result_frame.media_release_year.setText("Unknown")
            else:
                self.tv_show_result_frame.media_release_year.setText((tv_show['first_air_date'].split('-'))[0])

            self.tv_show_result_frame.media_short_info.setText("???")

            self.tv_show_results_scroll_area_grid_layout.addWidget(self.tv_show_result_frame, count, 0, 1, 1)

            if count + 1 == 5:
                break

        vertical_spacer_for_tv_show_results = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                                          QSizePolicy.Policy.Expanding)


        self.tv_show_results_scroll_area_grid_layout.addItem(vertical_spacer_for_tv_show_results, count + 1, 0, 1,
                                                             1)

