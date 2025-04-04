from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QSizePolicy, QSpacerItem
from PyQt6.QtCore import QRect, QPropertyAnimation
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt, QSize


class MediaResult(QFrame):
    def __init__(self, parent, media_type, account_id, application_window):

        super().__init__()

        self.parent = parent
        self.setMouseTracking(True)
        self.title = ""
        self.media_id = None
        self.media_type = media_type
        self.account_id = account_id

        self.application_window = application_window

        self.setup_elements()

    def set_media_id(self, media_id):
        self.media_id = media_id

    def set_media_title(self, media_title):
        self.media_title.setText(media_title)

    def set_media_poster(self, media_poster):
        self.media_poster.setPixmap(media_poster)

    def set_media_release_year(self, media_release_year):
        self.media_release_year.setText(media_release_year)

    def set_short_info(self, media_short_info):
        self.media_short_info.setText(media_short_info)

    def setup_elements(self):
        self.setMinimumSize(QSize(500, 170))
        self.setMaximumSize(QSize(500, 170))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("background-color:rgb(199, 253, 255)")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.media_type_label = QLabel(parent=self)
        self.media_type_label.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_type_label.setFont(font)
        self.media_type_label.setObjectName("media_type")
        self.gridLayout.addWidget(self.media_type_label, 2, 3, 1, 1)

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)

        self.media_poster = QLabel(parent=self)
        self.media_poster.setMinimumSize(QSize(90, 140))
        self.media_poster.setMaximumSize(QSize(90, 140))
        self.media_poster.setStyleSheet("background-color: rgb(255, 208, 253)")
        self.media_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.media_poster.setObjectName("media_poster")
        self.media_poster.setScaledContents(True)
        self.gridLayout.addWidget(self.media_poster, 0, 1, 3, 1)

        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)

        self.media_short_info = QLabel(parent=self)
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_short_info.setFont(font)
        self.media_short_info.setObjectName("media_short_info")
        self.gridLayout.addWidget(self.media_short_info, 2, 3, 1, 1)

        self.media_release_year = QLabel(parent=self)
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_release_year.setFont(font)
        self.media_release_year.setObjectName("media_release_year")
        self.gridLayout.addWidget(self.media_release_year, 1, 3, 1, 2)

        self.media_title = QLabel(parent=self)
        font = QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.media_title.setFont(font)
        self.media_title.setObjectName("media_title")
        self.gridLayout.addWidget(self.media_title, 0, 3, 1, 2)

    def setTitle(self, title):
        self.title = title

    def setMediaId(self, media_id):
        self.media_id = media_id

    def mousePressEvent(self, event):
        # print(self.title)

        self.application_window.change_to_about_specific_media_page(self.media_type, self.media_id)

    def mouseMoveEvent(self, ev):
        pass

    def resize_animation(self):
        pass


