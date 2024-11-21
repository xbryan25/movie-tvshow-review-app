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

        signup_dialog.sign_up_button.clicked.connect(lambda: self.make_new_account(signup_dialog))
        signup_dialog.exec()


    def make_new_account(self, signup_dialog):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        all_usernames = cursor.execute("SELECT username FROM accounts").fetchall()

        # Convert each tuple to string
        all_username = [str(account[0]) for account in all_usernames]

        if signup_dialog.username_lineedit.text() in all_username:
            print("Username already exists")
        elif signup_dialog.username_lineedit.text() == "":
            print("Username is blank")
        else:
            if signup_dialog.password_lineedit.text() == "":
                print("Password is blank")
            elif signup_dialog.confirm_password_lineedit.text() == "":
                print("Confirm password is blank")
            elif signup_dialog.password_lineedit.text() != signup_dialog.confirm_password_lineedit.text():
                print("Password and confirm password is not equal")
            else:
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

