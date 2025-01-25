from PyQt6.QtWidgets import QDialog
from choose_title.logout_confirmation_dialog_design import Ui_Dialog as LogoutConfirmationUI


class LogoutConfirmationDialog(QDialog, LogoutConfirmationUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

