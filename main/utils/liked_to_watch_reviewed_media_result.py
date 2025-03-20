from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem, QPushButton
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt, QSize


class LikedToWatchReviewedMediaResult(QFrame):
    def __init__(self, parent, media_type, account_id, application_window, state_to_show):

        super().__init__()

        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = None
        self.media_type = media_type
        self.account_id = account_id

        self.application_window = application_window

        self.state_to_show = state_to_show

        self.setup_elements()

    def set_media_id(self, media_id):
        self.media_id = media_id

    def set_media_title(self, media_title):
        self.media_title_label.setText(media_title)

    def set_media_poster(self, media_poster):
        self.media_poster_label.setPixmap(media_poster)

    def set_media_release_year(self, media_release_year):
        self.media_year_label.setText(media_release_year)

    def set_media_short_info(self, media_short_info):
        self.media_short_info_label.setText(media_short_info)

    def add_remove_button_operation(self, medias, l_tw_r_page_controls):
        self.remove_button_media.clicked.connect(
            lambda state, _frame=self,
                   _media_id=self.media_id,
                   _medias=medias,
                   _media_type=self.media_type:
            l_tw_r_page_controls.remove_media(_frame, _media_id, _medias,
                                              _media_type))

    def setup_elements(self):
        self.setMinimumSize(QSize(360, 160))
        self.setMaximumSize(QSize(550, 160))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("background-color: rgb(13, 249, 249);")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName(f"l_tw_r_movie")

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setObjectName("grid_layout")

        self.media_title_label = QLabel(parent=self)
        self.media_title_label.setMinimumSize(QSize(0, 30))
        self.media_title_label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_title_label.setFont(font)
        self.media_title_label.setObjectName(f"media_title_label")
        self.grid_layout.addWidget(self.media_title_label, 0, 2, 1, 2)

        self.media_poster_label = QLabel(parent=self)
        self.media_poster_label.setMinimumSize(QSize(0, 138))
        self.media_poster_label.setMaximumSize(QSize(92, 138))
        self.media_poster_label.setScaledContents(True)
        self.media_poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.media_poster_label.setObjectName(f"media_poster")
        self.media_poster_label.setScaledContents(True)

        self.media_poster_label.setScaledContents(True)
        self.grid_layout.addWidget(self.media_poster_label, 0, 0, 5, 1)

        self.media_year_label = QLabel(parent=self)
        self.media_year_label.setMinimumSize(QSize(0, 30))
        self.media_year_label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_year_label.setFont(font)
        self.media_year_label.setObjectName(f"media_year")
        self.grid_layout.addWidget(self.media_year_label, 1, 2, 1, 2)

        self.media_short_info_label = QLabel(parent=self)
        self.media_short_info_label.setMinimumSize(QSize(0, 30))
        self.media_short_info_label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_short_info_label.setFont(font)
        self.media_short_info_label.setObjectName(f"media_short_info_label")
        self.grid_layout.addWidget(self.media_short_info_label, 2, 2, 1, 2)

        if self.state_to_show != "reviewed":
            self.remove_button_media = QPushButton(parent=self)
            font = QFont()
            font.setFamily("Oswald Medium")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            self.remove_button_media.setFont(font)
            self.remove_button_media.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.remove_button_media.setObjectName("remove_from_liked_media")
            self.remove_button_media.setText("Remove")

            self.grid_layout.addWidget(self.remove_button_media, 3, 2, 1, 2)

        poster_spacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed,
                                    QSizePolicy.Policy.Minimum)

        self.grid_layout.addItem(poster_spacer, 1, 1, 1, 1)

    # def setTitle(self, title):
    #     self.title = title
    #
    # def setMediaId(self, media_id):
    #     self.media_id = media_id

    def mousePressEvent(self, event):
        self.application_window.change_to_about_specific_media_page(self.media_type, self.media_id)

    def mouseMoveEvent(self, ev):
        pass

    def resize_animation(self):
        pass


