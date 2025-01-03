from main.login.login_successful_dialog_design import Ui_Dialog as LoginSuccessfulPopupUI
from PyQt6.QtWidgets import QDialog


class LoginSuccessfulDialog(QDialog, LoginSuccessfulPopupUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
