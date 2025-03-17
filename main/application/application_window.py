from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton

from login.signup_dialog import SignupDialog
from login.login_status_dialog import LoginStatusDialog

from application.application_window_design import Ui_MainWindow as ApplicationWindowUI

from page_controls.choose_titles_page_controls import ChooseTitlesPageControls
from page_controls.login_page_controls import LoginPageControls
from page_controls.about_specific_media_page_controls import AboutSpecificMediaPageControls
from page_controls.search_results_page_controls import SearchResultsPageControls
from page_controls.liked_to_watch_reviewed_page_controls import LikedToWatchReviewedPageControls
from page_controls.members_page_controls import MembersPageControls

from utils.user_input_validators import UserInputValidators

import sqlite3
import requests


class ApplicationWindow(QMainWindow, ApplicationWindowUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.load_external_stylesheet()

        self.load_controls()
        self.open_requests_session()

        self.change_to_login_page()

        self.current_account_id = 0

        self.has_loaded_posters = False

        self.app_title_button.clicked.connect(self.change_to_choose_title_page)
        self.liked_button.clicked.connect(lambda: self.change_to_liked_to_watch_reviewed_page("liked"))
        self.to_watch_button.clicked.connect(lambda: self.change_to_liked_to_watch_reviewed_page("to_watch"))
        self.reviewed_button.clicked.connect(lambda: self.change_to_liked_to_watch_reviewed_page("reviewed"))
        self.members_button.clicked.connect(lambda: self.change_to_members_page())

        self.search_title_line_edit.returnPressed.connect(
            lambda: self.change_to_search_results_page(self.search_title_line_edit.text()))

        self.choose_titles_page_controls.set_requests_session(self.requests_session_tmdb,
                                                              self.requests_session_images)
        self.choose_titles_page_controls.start_process()

    def open_requests_session(self):
        self.requests_session_tmdb = requests.Session()
        self.requests_session_images = requests.Session()

    def set_current_account_id(self, account_id):
        self.current_account_id = account_id

    def load_controls(self):
        self.login_page_controls = LoginPageControls([self.sign_up_button,
                                                      self.login_button,
                                                      self.show_password_checkbox,
                                                      self.username_lineedit,
                                                      self.password_lineedit],
                                                     self)

        self.choose_titles_page_controls = ChooseTitlesPageControls([self.search_title_line_edit,
                                                                     self.liked_button,
                                                                     self.to_watch_button,
                                                                     self.members_button,
                                                                     self.logout_button,
                                                                     self.popular_movies_scroll_area_contents,
                                                                     self.popular_movies_scroll_area_grid_layout,
                                                                     self.popular_tv_shows_scroll_area_contents,
                                                                     self.popular_tv_shows_scroll_area_grid_layout],
                                                                    self)

        self.about_specific_media_page_controls = AboutSpecificMediaPageControls([self.director_label,
                                                                                  self.general_stars_label,
                                                                                  self.genres_label,
                                                                                  self.media_title_label,
                                                                                  self.poster_label,
                                                                                  self.synopsis_label,
                                                                                  self.year_label,
                                                                                  self.add_review_button,
                                                                                  self.add_to_liked_button,
                                                                                  self.add_to_watchlist_button,
                                                                                  self.save_rating_button,
                                                                                  self.star_label,
                                                                                  self.star_slider,
                                                                                  self.season_buttons_scroll_area,
                                                                                  self.season_buttons_scroll_area_widget_contents,
                                                                                  self.seasons_buttons_grid_layout,
                                                                                  self.gridLayout_2],
                                                                                 self)

        self.search_results_page_controls = SearchResultsPageControls([self.showing_results_label,
                                                                       self.movie_results_label,
                                                                       self.tv_show_results_label,
                                                                       self.movie_results_scroll_area,
                                                                       self.tv_show_results_scroll_area,
                                                                       self.movie_results_scroll_area_grid_layout,
                                                                       self.tv_show_results_scroll_area_grid_layout],
                                                                      self)

        self.liked_to_watch_reviewed_page_controls = LikedToWatchReviewedPageControls([self.l_tw_r_header_label,
                                                                                       self.l_tw_r_movies_label,
                                                                                       self.l_tw_r_tv_shows_label,
                                                                                       self.l_tw_r_movies_scroll_area,
                                                                                       self.l_tw_r_tv_shows_scroll_area,
                                                                                       self.l_tw_r_movies_scroll_area_contents,
                                                                                       self.l_tw_r_tv_shows_scroll_area_contents,
                                                                                       self.l_tw_r_movies_scroll_area_grid_layout,
                                                                                       self.l_tw_r_tv_shows_scroll_area_grid_layout],
                                                                                      self)

        self.members_page_controls = MembersPageControls([self.members_label,
                                                          self.total_member_count_label,
                                                          self.members_scroll_area,
                                                          self.members_scroll_area_contents,
                                                          self.members_scroll_area_contents_grid_layout],
                                                         self)

    def change_to_login_page(self):
        self.page_stacked_widget.setCurrentWidget(self.login_page)

    def change_to_choose_title_page(self):
        if not self.has_loaded_posters:

            login_successful_dialog = LoginStatusDialog()
            login_successful_dialog.setWindowTitle("Login successful.")
            login_successful_dialog.text_label.setText("No issues logging in!")

            login_successful_dialog.exec()

            self.username_lineedit.setText("")
            self.password_lineedit.setText("")

            self.page_stacked_widget.setCurrentWidget(self.main_page)
            self.subpage_stacked_widget.setCurrentWidget(self.popular_media_subpage)

            self.choose_titles_page_controls.set_account_id(self.current_account_id)
            # self.choose_titles_page_controls.set_requests_session(self.requests_session_tmdb,
            #                                                       self.requests_session_images)
            # self.choose_titles_page_controls.start_process()

            self.has_loaded_posters = True

        else:
            self.page_stacked_widget.setCurrentWidget(self.main_page)
            self.subpage_stacked_widget.setCurrentWidget(self.popular_media_subpage)

    def change_to_about_specific_media_page(self, media_type, media_id):
        self.page_stacked_widget.setCurrentWidget(self.main_page)
        self.subpage_stacked_widget.setCurrentWidget(self.about_specific_media_subpage)

        self.about_specific_media_page_controls.set_account_id(self.current_account_id)
        self.about_specific_media_page_controls.set_media_type_and_id(media_type, media_id)
        self.about_specific_media_page_controls.set_requests_session(self.requests_session_tmdb,
                                                                     self.requests_session_images)

        self.about_specific_media_page_controls.start_process()

    def change_to_liked_to_watch_reviewed_page(self, state_to_show):
        self.page_stacked_widget.setCurrentWidget(self.main_page)
        self.subpage_stacked_widget.setCurrentWidget(self.l_tw_r_subpage)

        self.liked_to_watch_reviewed_page_controls.set_account_id(self.current_account_id)
        self.liked_to_watch_reviewed_page_controls.set_state_to_show(state_to_show)
        self.liked_to_watch_reviewed_page_controls.set_requests_session(self.requests_session_tmdb,
                                                                        self.requests_session_images)

        self.liked_to_watch_reviewed_page_controls.initialize_page()

        self.liked_to_watch_reviewed_page_controls.clear_all_media()

        self.liked_to_watch_reviewed_page_controls.load_l_tw_r_media()

    def change_to_members_page(self):
        self.page_stacked_widget.setCurrentWidget(self.main_page)
        self.subpage_stacked_widget.setCurrentWidget(self.members_subpage)

        self.members_page_controls.load_members()

    def change_to_search_results_page(self, media_title_to_search):
        if media_title_to_search.strip() == "":
            print("The search bar is empty.")
        else:
            self.page_stacked_widget.setCurrentWidget(self.main_page)
            self.subpage_stacked_widget.setCurrentWidget(self.search_results_subpage)

            self.search_results_page_controls.set_media_title_to_search(media_title_to_search)
            self.search_results_page_controls.set_account_id(self.current_account_id)
            self.search_results_page_controls.set_requests_session(self.requests_session_tmdb,
                                                                   self.requests_session_images)

            self.search_results_page_controls.remove_old_search_results()
            self.search_results_page_controls.show_search_results()

    def load_external_stylesheet(self):
        with open("../assets/qss_files/login_page_style.qss", "r") as file:
            self.login_page.setStyleSheet(file.read())

    def resizeEvent(self, a0):
        print(self.size())
