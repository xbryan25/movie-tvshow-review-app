from os import supports_effective_ids

from PyQt6.QtWidgets import QDialog, QMainWindow
from PyQt6.QtCore import Qt
from loading_screen.loading_screen_design import Ui_MainWindow as LoadingScreenUI


class LoadingScreen(QMainWindow, LoadingScreenUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.show()
        # self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
