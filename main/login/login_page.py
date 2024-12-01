from main.choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI
from main.choose_title.choose_titles_page import ChooseTitlesPage

from main.login.login_page_design import Ui_MainWindow as LoginPageUI
from main.login.signup_dialog import SignupDialog
from PyQt6.QtWidgets import QMainWindow, QLineEdit
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
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # The no_issues variable checks if all the input fields in the signup dialog are correct
        # If no_issues stays True, then the account will be inserted into the database
        no_issues = True

        all_usernames = cursor.execute("SELECT username FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_usernames]

        if not self.is_valid_name(signup_dialog.firstname_lineedit.text()):
            print("First name format is invalid")
            no_issues = False

        if not self.is_valid_name(signup_dialog.lastname_lineedit.text()):
            print("Last name format is invalid")
            no_issues = False

        if not self.is_valid_email(signup_dialog.email_lineedit.text()):
            print("Email format is invalid")
            no_issues = False

        if signup_dialog.username_lineedit.text() in all_username:
            print("Username already exists")
            no_issues = False
        elif signup_dialog.username_lineedit.text() == "":
            print("Username is blank")
            no_issues = False

        if signup_dialog.password_lineedit.text() == "":
            print("Password is blank")
            no_issues = False
        elif signup_dialog.confirm_password_lineedit.text() == "":
            print("Confirm password is blank")
            no_issues = False
        elif signup_dialog.password_lineedit.text() != signup_dialog.confirm_password_lineedit.text():
            print("Password and confirm password is not equal")
            no_issues = False

        if no_issues:
            cursor.execute("INSERT INTO accounts VALUES "
                           "(:username, :password, :firstname, :lastname, :email, :age, :gender)",
                           {"username": signup_dialog.username_lineedit.text(),
                            "password": signup_dialog.password_lineedit.text(),
                            "firstname": signup_dialog.firstname_lineedit.text(),
                            "lastname": signup_dialog.lastname_lineedit.text(),
                            "email": signup_dialog.email_lineedit.text(),
                            "age": signup_dialog.age_spinbox.value(),
                            "gender": signup_dialog.gender_combobox.currentText()})

            print("Account created!")

        connection.commit()
        connection.close()

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
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        all_accounts_username_password = cursor.execute("SELECT username, password FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_accounts_username_password]
        all_password = [str(account[1]) for account in all_accounts_username_password]

        if self.username_lineedit.text() in all_username:
            print("Username exists,", end="")

            password_index = all_username.index(self.username_lineedit.text())

            if self.password_lineedit.text() == all_password[password_index]:
                print(" password is correct")
                print("\nWelcome!")

                self.change_to_choose_title_page()

            elif self.password_lineedit.text() == "":
                print(" password is blank")
            else:
                print(" wrong password")

        elif self.username_lineedit.text() == "":
            print("Username is blank")
        else:
            print("Account doesn't exist, kindly sign up")

        connection.commit()
        connection.close()


    def change_to_choose_title_page(self):
        self.hide()

        self.choose_titles_page = ChooseTitlesPage()

        # self.choose_titles_page.show()
