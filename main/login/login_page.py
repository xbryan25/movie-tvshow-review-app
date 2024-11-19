from main.login.login_page_design import Ui_MainWindow as LoginPageUI
from main.login.signup_dialog import SignupDialog
from PyQt6.QtWidgets import QMainWindow


class LoginPage(QMainWindow, LoginPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.sign_up_button.clicked.connect(self.signup_clicked)

    def signup_clicked(self):
        signup_dialog = SignupDialog()

        signup_dialog.exec()