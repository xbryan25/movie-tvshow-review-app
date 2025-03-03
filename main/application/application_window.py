from PyQt6.QtWidgets import QMainWindow, QLineEdit

from login.signup_dialog import SignupDialog
from login.login_status_dialog import LoginStatusDialog

from application.application_window_design import Ui_MainWindow as ApplicationWindowUI

from utils.user_input_validators import UserInputValidators

import sqlite3


class ApplicationWindow(QMainWindow, ApplicationWindowUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.add_signals()

    def add_signals(self):
        self.sign_up_button.clicked.connect(self.signup_clicked)
        self.login_button.clicked.connect(self.check_if_account_exists)
        self.show_password_checkbox.stateChanged.connect(self.show_password_text_login)

        self.username_lineedit.returnPressed.connect(self.check_if_account_exists)
        self.password_lineedit.returnPressed.connect(self.check_if_account_exists)

    def show_password_text_login(self):
        if self.show_password_checkbox.isChecked():
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)

    def signup_clicked(self):
        self.signup_dialog = SignupDialog()

        self.signup_dialog.exec()

    # TODO: Rename this function
    def check_if_account_exists(self):
        connection = sqlite3.connect('..\\database\\accounts.db')
        cursor = connection.cursor()

        all_accounts_username_password = cursor.execute("SELECT username, password FROM accounts").fetchall()

        # Convert each tuple to string
        all_usernames = [str(account[0]) for account in all_accounts_username_password]
        all_passwords = [str(account[1]) for account in all_accounts_username_password]

        issue_message = UserInputValidators.login_input_validator(self.username_lineedit.text(),
                                                                  self.password_lineedit.text(),
                                                                  all_usernames,
                                                                  all_passwords)

        if issue_message == "":
            username = self.username_lineedit.text()
            account_id = cursor.execute("SELECT account_id FROM accounts WHERE username=(:username)",
                                        {"username": username}).fetchone()[0]

            self.change_to_choose_title_page(account_id)

        else:
            login_failure_dialog = LoginStatusDialog()
            login_failure_dialog.text_label.setText(issue_message)
            login_failure_dialog.setWindowTitle("Login failure.")
            login_failure_dialog.exec()

        connection.commit()
        connection.close()


    def change_to_choose_title_page(self, account_id):
        login_successful_dialog = LoginStatusDialog()
        login_successful_dialog.setWindowTitle("Login successful.")
        login_successful_dialog.text_label.setText("No issues logging in!")

        login_successful_dialog.exec()

        self.username_lineedit.setText("")
        self.password_lineedit.setText("")

        self.stackedWidget.setCurrentWidget(self.choose_titles_page)


        # self.hide()
        #
        # self.choose_titles_page = ChooseTitlesPage(account_id, self)

        # self.choose_titles_page.show()

