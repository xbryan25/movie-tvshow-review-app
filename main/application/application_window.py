from PyQt6.QtWidgets import QMainWindow, QLineEdit

from login.signup_dialog import SignupDialog
from login.login_status_dialog import LoginStatusDialog

from application.application_window_design import Ui_MainWindow as ApplicationWindowUI
from application.choose_titles_page_controls import ChooseTitlesPageControls
from application.login_page_controls import LoginPageControls

from utils.user_input_validators import UserInputValidators

import sqlite3


class ApplicationWindow(QMainWindow, ApplicationWindowUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.load_controls()

        self.change_to_login_page()

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

    def change_to_login_page(self):
        self.page_stacked_widget.setCurrentWidget(self.login_page)

    def change_to_choose_title_page(self, account_id):
        login_successful_dialog = LoginStatusDialog()
        login_successful_dialog.setWindowTitle("Login successful.")
        login_successful_dialog.text_label.setText("No issues logging in!")

        login_successful_dialog.exec()

        self.username_lineedit.setText("")
        self.password_lineedit.setText("")

        self.page_stacked_widget.setCurrentWidget(self.main_page)

        self.choose_titles_page_controls.set_account_id(account_id)
        self.choose_titles_page_controls.start_process()
