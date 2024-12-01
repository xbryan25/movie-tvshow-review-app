from main.login.signup_dialog_design import Ui_Dialog as SignupDialogUI
from PyQt6.QtWidgets import QDialog

class SignupDialog(QDialog, SignupDialogUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
