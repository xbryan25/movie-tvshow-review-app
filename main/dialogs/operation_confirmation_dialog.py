from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from dialogs.operation_confirmation_dialog_design import Ui_Dialog as OperationConfirmationDialogUI


class OperationConfirmationDialog(QDialog, OperationConfirmationDialogUI):
    def __init__(self, media_type, state_to_show):
        super().__init__()

        self.setupUi(self)

        self.show()

        self.confirm_state = False

        self.media_type = media_type
        self.state_to_show = state_to_show

        ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        cancel_button = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)

        ok_button.clicked.connect(self.set_confirm_state)
        cancel_button.clicked.connect(self.close)

        self.set_texts()

    def set_texts(self):
        media_type_text = ""

        if self.media_type == "tv":
            media_type_text = "TV show"
        elif self.media_type == "movie":
            media_type_text = "movie"

        if self.state_to_show == "liked":
            self.header_label.setText(f"Remove {media_type_text} from liked media?")
        elif self.state_to_show == "to_watch":
            self.header_label.setText(f"Remove {media_type_text} from media to watch?")

    def set_confirm_state(self):
        self.confirm_state = True
        self.close()

    def get_confirm_state(self):
        return self.confirm_state
