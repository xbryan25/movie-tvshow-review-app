# Form implementation generated from reading ui file 'choose-titles-page.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 775)
        MainWindow.setMinimumSize(QtCore.QSize(800, 775))
        MainWindow.setMaximumSize(QtCore.QSize(800, 769))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.header_frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.header_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.header_frame.setObjectName("header_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.header_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.search_movie_tv_show_label = QtWidgets.QLabel(parent=self.header_frame)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.search_movie_tv_show_label.setFont(font)
        self.search_movie_tv_show_label.setObjectName("search_movie_tv_show_label")
        self.horizontalLayout_3.addWidget(self.search_movie_tv_show_label)
        self.search_title_line_edit = QtWidgets.QLineEdit(parent=self.header_frame)
        self.search_title_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        self.search_title_line_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.search_title_line_edit.setFont(font)
        self.search_title_line_edit.setText("")
        self.search_title_line_edit.setObjectName("search_title_line_edit")
        self.horizontalLayout_3.addWidget(self.search_title_line_edit)
        spacerItem1 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.liked_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.liked_button.setMinimumSize(QtCore.QSize(40, 0))
        self.liked_button.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.liked_button.setFont(font)
        self.liked_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.liked_button.setStyleSheet("QPushButton{color: black; border: none; background-color: transparent;}\n"
"QPushButton:hover{color:green}")
        self.liked_button.setFlat(True)
        self.liked_button.setObjectName("liked_button")
        self.horizontalLayout_3.addWidget(self.liked_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.to_watch_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.to_watch_button.setMinimumSize(QtCore.QSize(60, 0))
        self.to_watch_button.setMaximumSize(QtCore.QSize(60, 30))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.to_watch_button.setFont(font)
        self.to_watch_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.to_watch_button.setStyleSheet("QPushButton{color: black; border: none; background-color: transparent;}\n"
"QPushButton:hover{color:green}")
        self.to_watch_button.setFlat(True)
        self.to_watch_button.setObjectName("to_watch_button")
        self.horizontalLayout_3.addWidget(self.to_watch_button)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.reviewed_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.reviewed_button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.reviewed_button.setFont(font)
        self.reviewed_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.reviewed_button.setStyleSheet("QPushButton{color: black; border: none; background-color: transparent;}\n"
"QPushButton:hover{color:green}")
        self.reviewed_button.setDefault(False)
        self.reviewed_button.setFlat(True)
        self.reviewed_button.setObjectName("reviewed_button")
        self.horizontalLayout_3.addWidget(self.reviewed_button)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.members_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.members_button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.members_button.setFont(font)
        self.members_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.members_button.setStyleSheet("QPushButton{color: black; border: none; background-color: transparent;}\n"
"QPushButton:hover{color:green}")
        self.members_button.setFlat(True)
        self.members_button.setObjectName("members_button")
        self.horizontalLayout_3.addWidget(self.members_button)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.logout_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.logout_button.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.logout_button.setFont(font)
        self.logout_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logout_button.setStyleSheet("QPushButton{color: black; border: none; background-color: transparent;}\n"
"QPushButton:hover{color:green}")
        self.logout_button.setFlat(True)
        self.logout_button.setObjectName("logout_button")
        self.horizontalLayout_3.addWidget(self.logout_button)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout.addWidget(self.header_frame)
        self.popular_movie_week_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.popular_movie_week_frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.popular_movie_week_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.popular_movie_week_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.popular_movie_week_frame.setObjectName("popular_movie_week_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.popular_movie_week_frame)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.popular_movie_week_label = QtWidgets.QLabel(parent=self.popular_movie_week_frame)
        self.popular_movie_week_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Oswald SemiBold")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.popular_movie_week_label.setFont(font)
        self.popular_movie_week_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.popular_movie_week_label.setObjectName("popular_movie_week_label")
        self.horizontalLayout.addWidget(self.popular_movie_week_label)
        self.verticalLayout.addWidget(self.popular_movie_week_frame)
        self.popular_movies_scroll_area = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.popular_movies_scroll_area.setMinimumSize(QtCore.QSize(0, 280))
        self.popular_movies_scroll_area.setMaximumSize(QtCore.QSize(880, 280))
        self.popular_movies_scroll_area.setStyleSheet("\n"
"QScrollBar:horizontal{\n"
"    border: none;\n"
"    background-color: rgb(43, 56, 138);\n"
"    height: 10px;\n"
"    margin: 0 0 0 0;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal{\n"
"    background-color: rgb(131, 207, 241);\n"
"    min-width: 30px;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal:hover{\n"
"    background-color: rgb(131, 180, 210);\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:pressed{\n"
"    background-color: rgb(120, 170, 190);\n"
"}\n"
"")
        self.popular_movies_scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.popular_movies_scroll_area.setLineWidth(1)
        self.popular_movies_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.popular_movies_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.popular_movies_scroll_area.setWidgetResizable(True)
        self.popular_movies_scroll_area.setObjectName("popular_movies_scroll_area")
        self.popular_movies_scroll_area_contents = QtWidgets.QWidget()
        self.popular_movies_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 782, 270))
        self.popular_movies_scroll_area_contents.setObjectName("popular_movies_scroll_area_contents")
        self.gridLayout = QtWidgets.QGridLayout(self.popular_movies_scroll_area_contents)
        self.gridLayout.setObjectName("gridLayout")

#         self.temp_movie_poster = QtWidgets.QLabel(parent=self.popular_movies_scroll_area_contents)
#         self.temp_movie_poster.setMinimumSize(QtCore.QSize(165, 250))
#         self.temp_movie_poster.setMaximumSize(QtCore.QSize(165, 250))
#         self.temp_movie_poster.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
#         self.temp_movie_poster.setStyleSheet("QLabel{\n"
# "background-color: orange;\n"
# "border-style: outset;\n"
# "}\n"
# "\n"
# "QLabel:hover{\n"
# "border: 4px solid blue;\n"
# "border-radius: 1px;\n"
# "}\n"
# "\n"
# "")
#         self.temp_movie_poster.setText("")
#         self.temp_movie_poster.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         self.temp_movie_poster.setObjectName("temp_movie_poster")
#         self.gridLayout.addWidget(self.temp_movie_poster, 0, 0, 1, 1)

        self.popular_movies_scroll_area.setWidget(self.popular_movies_scroll_area_contents)
        self.verticalLayout.addWidget(self.popular_movies_scroll_area)
        self.popular_tv_show_week_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.popular_tv_show_week_frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.popular_tv_show_week_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.popular_tv_show_week_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.popular_tv_show_week_frame.setObjectName("popular_tv_show_week_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.popular_tv_show_week_frame)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.popular_tv_show_week_label = QtWidgets.QLabel(parent=self.popular_tv_show_week_frame)
        self.popular_tv_show_week_label.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setFamily("Oswald SemiBold")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.popular_tv_show_week_label.setFont(font)
        self.popular_tv_show_week_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.popular_tv_show_week_label.setObjectName("popular_tv_show_week_label")
        self.horizontalLayout_2.addWidget(self.popular_tv_show_week_label)
        self.verticalLayout.addWidget(self.popular_tv_show_week_frame)
        self.popular_tv_shows_scroll_area = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.popular_tv_shows_scroll_area.setMinimumSize(QtCore.QSize(0, 280))
        self.popular_tv_shows_scroll_area.setMaximumSize(QtCore.QSize(880, 280))
        self.popular_tv_shows_scroll_area.setStyleSheet("\n"
"QScrollBar:horizontal{\n"
"    border: none;\n"
"    background-color: rgb(43, 56, 138);\n"
"    height: 10px;\n"
"    margin: 0 0 0 0;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal{\n"
"    background-color: rgb(131, 207, 241);\n"
"    min-width: 30px;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal:hover{\n"
"    background-color: rgb(131, 180, 210);\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:pressed{\n"
"    background-color: rgb(120, 170, 190);\n"
"}\n"
"")
        self.popular_tv_shows_scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.popular_tv_shows_scroll_area.setLineWidth(1)
        self.popular_tv_shows_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.popular_tv_shows_scroll_area.setWidgetResizable(True)
        self.popular_tv_shows_scroll_area.setObjectName("popular_tv_shows_scroll_area")
        self.popular_tv_shows_scroll_area_contents = QtWidgets.QWidget()
        self.popular_tv_shows_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 782, 270))
        self.popular_tv_shows_scroll_area_contents.setObjectName("popular_tv_shows_scroll_area_contents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.popular_tv_shows_scroll_area_contents)
        self.gridLayout_2.setObjectName("gridLayout_2")

#         self.temp_tv_show_poster = QtWidgets.QLabel(parent=self.popular_tv_shows_scroll_area_contents)
#         self.temp_tv_show_poster.setMinimumSize(QtCore.QSize(165, 250))
#         self.temp_tv_show_poster.setMaximumSize(QtCore.QSize(165, 250))
#         self.temp_tv_show_poster.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
#         self.temp_tv_show_poster.setStyleSheet("QLabel{\n"
# "background-color: orange;\n"
# "border-style: outset;\n"
# "}\n"
# "\n"
# "QLabel:hover{\n"
# "border: 4px solid blue;\n"
# "border-radius: 1px;\n"
# "}\n"
# "\n"
# "")
#         self.temp_tv_show_poster.setText("")
#         self.temp_tv_show_poster.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         self.temp_tv_show_poster.setObjectName("temp_tv_show_poster")
#         self.gridLayout_2.addWidget(self.temp_tv_show_poster, 0, 0, 1, 1)

        self.popular_tv_shows_scroll_area.setWidget(self.popular_tv_shows_scroll_area_contents)
        self.verticalLayout.addWidget(self.popular_tv_shows_scroll_area)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Choose a Movie or a TV Show"))
        self.search_movie_tv_show_label.setText(_translate("MainWindow", "Search Movie/TV Show "))
        self.search_title_line_edit.setPlaceholderText(_translate("MainWindow", "Input name..."))
        self.liked_button.setText(_translate("MainWindow", "Liked"))
        self.to_watch_button.setText(_translate("MainWindow", "To Watch"))
        self.reviewed_button.setText(_translate("MainWindow", "Reviewed"))
        self.members_button.setText(_translate("MainWindow", "Members"))
        self.logout_button.setText(_translate("MainWindow", "Logout?"))
        self.popular_movie_week_label.setText(_translate("MainWindow", "Popular movies for this week"))
        self.popular_tv_show_week_label.setText(_translate("MainWindow", "Popular TV shows for this week"))
