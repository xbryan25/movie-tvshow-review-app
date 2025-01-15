from main.search_results.search_results_design import Ui_MainWindow as SearchResultsPageUI
from PyQt6.QtWidgets import QMainWindow


class SearchResultsPage(QMainWindow, SearchResultsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

