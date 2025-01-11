from main.login.signup_successful_dialog_design import Ui_Dialog as SignupSuccessfulDialogUI
from PyQt6.QtWidgets import QDialog

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class SignupSuccessfulDialog(QDialog, SignupSuccessfulDialogUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_pointing_hand_cursor_to_interactables()

    def set_pointing_hand_cursor_to_interactables(self):
        self.proceed_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))