from choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI
from choose_title.choose_titles_page import ChooseTitlesPage

from login.login_page_design import Ui_MainWindow as LoginPageUI
from login.signup_dialog import SignupDialog

from login.login_status_dialog import LoginStatusDialog

from login.signup_fail_dialog import SignupFailDialog
from login.signup_successful_dialog import SignupSuccessfulDialog

from login.initialize_account import InitializeAccount

from PyQt6.QtWidgets import QMainWindow, QLineEdit
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import sqlite3
import re

# from main.choose_title.choose_titles_page


class LoginPage(QMainWindow, LoginPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.sign_up_button.clicked.connect(self.signup_clicked)
        self.login_button.clicked.connect(self.check_if_account_exists)
        self.show_password_checkbox.stateChanged.connect(self.show_password_text_login)

        self.username_lineedit.returnPressed.connect(self.check_if_account_exists)
        self.password_lineedit.returnPressed.connect(self.check_if_account_exists)

        # Temporary account_id; to be overwritten
        self.account_id = 0

        self.choose_titles_page = None

        # self.set_pointing_hand_cursor_to_interactables()

    # def set_pointing_hand_cursor_to_interactables(self):
    #     self.sign_up_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    #     self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    #     self.show_password_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def show_password_text_login(self):
        if self.show_password_checkbox.isChecked():
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)

    def signup_clicked(self):
        signup_dialog = SignupDialog()

        signup_dialog.sign_up_button.clicked.connect(lambda: self.make_new_account(signup_dialog))
        signup_dialog.show_password_checkbox.stateChanged.connect(lambda: self.show_password_text_signup(signup_dialog))
        signup_dialog.exec()

    def make_new_account(self, signup_dialog):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        # TODO: Trim the leading and trailing spaces before checking each field

        # The no_issues variable checks if all the input fields in the signup dialog are correct
        # If no_issues stays True, then the account will be inserted into the database
        no_issues = True

        all_usernames = cursor.execute("SELECT username FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_usernames]

        issues_found = []

        if not self.is_valid_name(signup_dialog.firstname_lineedit.text()):
            issues_found.append("First name format is invalid")
            no_issues = False

        if not self.is_valid_name(signup_dialog.lastname_lineedit.text()):
            issues_found.append("Last name format is invalid")
            no_issues = False

        if signup_dialog.email_lineedit.text() == "":
            issues_found.append("Email is blank")
        elif not self.is_valid_email(signup_dialog.email_lineedit.text()):
            issues_found.append("Email format is invalid")
            no_issues = False

        if signup_dialog.username_lineedit.text() in all_username:
            issues_found.append("Username already exists")
            no_issues = False
        elif signup_dialog.username_lineedit.text() == "":
            issues_found.append("Username is blank")
            no_issues = False

        if signup_dialog.password_lineedit.text() == "":
            issues_found.append("Password is blank")
            no_issues = False
        elif signup_dialog.confirm_password_lineedit.text() == "":
            issues_found.append("Confirm password is blank")
            no_issues = False
        elif signup_dialog.password_lineedit.text() != signup_dialog.confirm_password_lineedit.text():
            issues_found.append("Password and confirm password is not equal")
            no_issues = False

        if no_issues:
            cursor.execute("INSERT INTO accounts (username, password, firstname, lastname, email, age, gender) VALUES "
                           "(:username, :password, :firstname, :lastname, :email, :age, :gender)",
                           {"username": signup_dialog.username_lineedit.text(),
                            "password": signup_dialog.password_lineedit.text(),
                            "firstname": signup_dialog.firstname_lineedit.text(),
                            "lastname": signup_dialog.lastname_lineedit.text(),
                            "email": signup_dialog.email_lineedit.text(),
                            "age": signup_dialog.age_spinbox.value(),
                            "gender": signup_dialog.gender_combobox.currentText()})

            print("Account created!")

            # Overwrite self.account_id
            self.account_id = cursor.execute("SELECT account_id FROM accounts WHERE username=(:username)",
                                            {"username": signup_dialog.username_lineedit.text()}).fetchone()[0]

        else:
            signup_fail_dialog = SignupFailDialog(issues_found)

            signup_fail_dialog.proceed_button.clicked.connect(lambda: self.close_signup_fail_dialog(signup_fail_dialog))

            signup_fail_dialog.exec()

        connection.commit()
        connection.close()

        # The reason that this is at the bottom is to avoid OperationalError: database is locked
        # where more than one cursor is active, the previous cursor has to be closed first
        if no_issues:
            initialize_account = InitializeAccount(self.account_id)
            initialize_account.initialize()

            signup_successful_dialog = SignupSuccessfulDialog()
            signup_successful_dialog.proceed_button.clicked.connect(
                lambda: self.close_signup_dialogs(signup_dialog, signup_successful_dialog))
            signup_successful_dialog.exec()

    @staticmethod
    def close_signup_fail_dialog(signup_fail_dialog):
        signup_fail_dialog.close()

    @staticmethod
    def close_signup_dialogs(signup_dialog, signup_successful_dialog):
        signup_dialog.close()
        signup_successful_dialog.close()

    @staticmethod
    def is_valid_email(email):
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        return True if valid_email else False

    @staticmethod
    def is_valid_name(name):
        valid_name = re.match(r'^[a-zA-Z ]+$', name)

        return True if valid_name else False

    @staticmethod
    def show_password_text_signup(signup_dialog):
        if signup_dialog.show_password_checkbox.isChecked():
            signup_dialog.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            signup_dialog.confirm_password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            signup_dialog.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            signup_dialog.confirm_password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)

    # TODO: Rename this function
    def check_if_account_exists(self):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        all_accounts_username_password = cursor.execute("SELECT username, password FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_accounts_username_password]
        all_password = [str(account[1]) for account in all_accounts_username_password]

        no_issues = True
        issue_message = ""

        # TODO: Trim the leading and trailing spaces before checking each field

        if self.username_lineedit.text() in all_username:
            password_index = all_username.index(self.username_lineedit.text())

            if self.password_lineedit.text() == all_password[password_index]:

                username = self.username_lineedit.text()
                account_id = cursor.execute("SELECT account_id FROM accounts WHERE username=(:username)",
                                            {"username": username}).fetchone()[0]
                # self.change_to_choose_title_page(account_id)

                self.login_successful(account_id)

            elif self.password_lineedit.text() == "":
                issue_message = "Password is blank."
                no_issues = False
            else:
                issue_message = "Password is wrong."
                no_issues = False

        elif self.username_lineedit.text() == "":
            issue_message = "Username is blank."
            no_issues = False
        else:
            issue_message = "Account doesn't exist."
            no_issues = False

        if not no_issues:
            login_failure_dialog = LoginStatusDialog()
            login_failure_dialog.text_label.setText(issue_message)
            login_failure_dialog.setWindowTitle("Login failure.")
            login_failure_dialog.proceed_button.clicked.connect(lambda: self.close_login_failure_dialog(login_failure_dialog))
            login_failure_dialog.exec()

        connection.commit()
        connection.close()

    @staticmethod
    def close_login_failure_dialog(login_failure_dialog):
        login_failure_dialog.close()

    def login_successful(self, account_id):
        login_successful_dialog = LoginStatusDialog()
        login_successful_dialog.setWindowTitle("Login successful.")
        login_successful_dialog.text_label.setText("No issues logging in!")
        # Put a timer here?

        login_successful_dialog.proceed_button.clicked.connect(lambda: self.change_to_choose_title_page(account_id, login_successful_dialog))

        login_successful_dialog.exec()

    def change_to_choose_title_page(self, account_id, login_successful_dialog):
        self.username_lineedit.setText("")
        self.password_lineedit.setText("")

        login_successful_dialog.close()

        self.hide()

        self.choose_titles_page = ChooseTitlesPage(account_id, self)

        # self.choose_titles_page.show()

