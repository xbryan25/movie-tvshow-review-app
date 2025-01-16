from main.search_results.search_results_design import Ui_MainWindow as SearchResultsPageUI
from main.search_results.media_result import MediaResult

from PyQt6.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap

import requests


class SearchResultsPage(QMainWindow, SearchResultsPageUI):
    def __init__(self, media_title):
        super().__init__()

        self.setupUi(self)

        self.api_headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y0OWMyYmEyNmUxN2ZjMDkyY2VkYmQ2M2ZiZWIzNiIsIm5iZiI6MTczMjE2NjEzOS4wNDMzNTc0LCJzdWIiOiI2NzNlYzE5NzQ2NTQxYmJjZDM3OWNmZTYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.j9GlO1y5TXH6iexR69tp03m39ScK9-CoKdjbkfVBqJY"
        }

        self.media_title = media_title
        self.account_id = 1

        self.show_search_results()

    def show_search_results(self):
        self.show_results_label.setText(f"Showing results for {self.media_title}")

        tv_show_search_url = f"https://api.themoviedb.org/3/search/tv?query={self.media_title}"


        tv_show_search_results = requests.get(tv_show_search_url, headers=self.api_headers).json()

        print(tv_show_search_results)

        for tv_show in tv_show_search_results['results']:
            self.media_result_frame = MediaResult(self.results_scroll_area_contents, "tv", self.account_id)

            media_img_url = f'https://image.tmdb.org/t/p/w92/{tv_show['poster_path']}'

            media_image = QImage()
            media_image.loadFromData(requests.get(media_img_url, headers=self.api_headers).content)

            self.media_result_frame.media_poster.setPixmap(QPixmap(media_image))
            self.media_result_frame.media_title.setText(tv_show['name'])
            self.media_result_frame.media_release_year.setText((tv_show['first_air_date'].split('-'))[0])

            self.media_result_frame.media_type.setText("TV Show")
            self.media_result_frame.media_short_info.setText("???")

            self.verticalLayout_2.addWidget(self.media_result_frame)

        vertical_spacer_for_search_results = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(vertical_spacer_for_search_results)
