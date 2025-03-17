from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from choose_title.logout_confirmation_dialog_design import Ui_Dialog as LogoutConfirmationUI


class LogoutConfirmationDialog(QDialog, LogoutConfirmationUI):
    def __init__(self, application_window):
        super().__init__()

        self.setupUi(self)

        self.application_window = application_window

        self.yes_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Yes)
        self.yes_button.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.application_window.page_stacked_widget.setCurrentWidget(self.application_window.login_page)

        self.close()

    def closeEvent(self, event):
        print(f"LogoutConfirmationDialog close: {self}")

        super().closeEvent(event)
