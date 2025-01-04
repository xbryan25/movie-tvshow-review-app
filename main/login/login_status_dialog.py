from main.login.login_status_dialog_design import Ui_Dialog as LoginStatusDialogUI
from PyQt6.QtWidgets import QDialog


class LoginStatusDialog(QDialog, LoginStatusDialogUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
