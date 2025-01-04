from main.login.signup_fail_dialog_design import Ui_Dialog as SignupFailDialogUI
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt


class SignupFailDialog(QDialog, SignupFailDialogUI):
    def __init__(self, issues_found):
        super().__init__()

        self.issues_found = issues_found

        self.setupUi(self)

        self.add_issues()

    def add_issues(self):
        extra_space = (len(self.issues_found) - 1) * 12

        text_to_add = ""

        for issue in self.issues_found:
            text_to_add += "•" + issue + "\n"

        self.issues_list_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.issues_list_label.setText(text_to_add)
        self.setMinimumSize(250, 150 + extra_space)
        self.setMaximumSize(250, 150 + extra_space)
        #
        self.issues_list_label.setMinimumHeight(self.issues_list_label.height() + extra_space)
        self.issues_list_label.setMaximumHeight(self.issues_list_label.height() + extra_space)

        print(self.issues_list_label.height())

        print(150 + extra_space)