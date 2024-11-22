from main.choose_title.choose_titles_page_design import Ui_MainWindow as ChooseTitlesPageUI

from PyQt6.QtWidgets import QMainWindow
import sqlite3
import re


class ChooseTitlesPage(QMainWindow, ChooseTitlesPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        print("Reach here")
