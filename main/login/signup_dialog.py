from login.signup_dialog_design import Ui_Dialog as SignupDialogUI

from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class SignupDialog(QDialog, SignupDialogUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_pointing_hand_cursor_to_interactables()

    def set_pointing_hand_cursor_to_interactables(self):
        self.sign_up_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.show_password_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))