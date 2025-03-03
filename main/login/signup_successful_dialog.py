from login.signup_successful_dialog_design import Ui_Dialog as SignupSuccessfulDialogUI
from PyQt6.QtWidgets import QDialog

from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class SignupSuccessfulDialog(QDialog, SignupSuccessfulDialogUI):
    def __init__(self, signup_dialog):
        super().__init__()

        self.setupUi(self)

        self.signup_dialog = signup_dialog

        self.set_pointing_hand_cursor_to_interactables()

        self.proceed_button.clicked.connect(self.close_dialogs)

    def close_dialogs(self):
        self.signup_dialog.close()

        self.close()

    def set_pointing_hand_cursor_to_interactables(self):
        self.proceed_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))