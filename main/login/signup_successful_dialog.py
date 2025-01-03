from main.login.signup_successful_dialog_design import Ui_Dialog as SignupSuccessfulDialogUI
from PyQt6.QtWidgets import QDialog


class SignupSuccessfulDialog(QDialog, SignupSuccessfulDialogUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
