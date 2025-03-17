from login.signup_dialog_design import Ui_Dialog as SignupDialogUI
from login.signup_fail_dialog import SignupFailDialog
from login.signup_successful_dialog import SignupSuccessfulDialog

from login.initialize_account import InitializeAccount

from utils.user_input_validators import UserInputValidators

from PyQt6.QtWidgets import QDialog, QLineEdit
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

import sqlite3


class SignupDialog(QDialog, SignupDialogUI):
    def __init__(self):

        super().__init__()

        self.setupUi(self)

        # To be overwritten
        self.account_id = 0

        self.user_input_validators = UserInputValidators()

        self.set_pointing_hand_cursor_to_interactables()


        self.sign_up_button.clicked.connect(self.make_new_account)
        self.show_password_checkbox.stateChanged.connect(self.show_password_text_signup)

    def make_new_account(self):

        issues_found = self.user_input_validators.signup_input_validator(self.firstname_lineedit.text(),
                                                                         self.lastname_lineedit.text(),
                                                                         self.email_lineedit.text(),
                                                                         self.username_lineedit.text(),
                                                                         self.password_lineedit.text(),
                                                                         self.confirm_password_lineedit.text())
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        if not issues_found:

            cursor.execute("INSERT INTO accounts (username, password, firstname, lastname, email, age, gender) VALUES "
                           "(:username, :password, :firstname, :lastname, :email, :age, :gender)",
                           {"username": self.username_lineedit.text(),
                            "password": self.password_lineedit.text(),
                            "firstname": self.firstname_lineedit.text(),
                            "lastname": self.lastname_lineedit.text(),
                            "email": self.email_lineedit.text(),
                            "age": self.age_spinbox.value(),
                            "gender": self.gender_combobox.currentText()})

            print("Account created!")

            # Overwrite self.account_id
            self.account_id = cursor.execute("SELECT account_id FROM accounts WHERE username=(:username)",
                                             {"username": self.username_lineedit.text()}).fetchone()[0]

        else:
            signup_fail_dialog = SignupFailDialog(issues_found, self)
            signup_fail_dialog.exec()

        connection.commit()
        connection.close()

        # The reason that this is at the bottom is to avoid OperationalError: database is locked
        # where more than one cursor is active, the previous cursor has to be closed first
        if not issues_found:
            initialize_account = InitializeAccount(self.account_id)
            initialize_account.initialize()

            signup_successful_dialog = SignupSuccessfulDialog(self)
            signup_successful_dialog.exec()

    def show_password_text_signup(self):
        if self.show_password_checkbox.isChecked():
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)

    def set_pointing_hand_cursor_to_interactables(self):
        self.sign_up_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.show_password_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
