from main.login.login_page_design import Ui_MainWindow as LoginPageUI
from main.login.signup_dialog import SignupDialog
from PyQt6.QtWidgets import QMainWindow
import sqlite3


class LoginPage(QMainWindow, LoginPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.sign_up_button.clicked.connect(self.signup_clicked)
        self.login_button.clicked.connect(self.check_if_account_exists)

    def signup_clicked(self):
        signup_dialog = SignupDialog()

        signup_dialog.exec()

    def check_if_account_exists(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        all_accounts_username_password = cursor.execute("SELECT username, password FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_accounts_username_password]
        all_password = [str(account[1]) for account in all_accounts_username_password]

        if self.username_lineedit.text() in all_username:
            print("Pass test 1")

            password_index = all_username.index(self.username_lineedit.text())

            if self.password_lineedit.text() == all_password[password_index]:
                print("Pass test 2")
            else:
                print("Wrong password")

        else:
            print("Account doesn't exist")


        connection.commit()
        connection.close()

