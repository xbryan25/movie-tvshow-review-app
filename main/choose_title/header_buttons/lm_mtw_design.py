# Form implementation generated from reading ui file 'liked-media-and-media-to-watch.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.header_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.header_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(20)
        self.header_label.setFont(font)
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.verticalLayout_2.addWidget(self.header_label)
        self.h_line = QtWidgets.QFrame(parent=self.centralwidget)
        self.h_line.setStyleSheet("color: rgb(186, 188, 180)")
        self.h_line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.h_line.setLineWidth(5)
        self.h_line.setMidLineWidth(5)
        self.h_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.h_line.setObjectName("h_line")
        self.verticalLayout_2.addWidget(self.h_line)
        self.outer_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.outer_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.outer_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.outer_frame.setObjectName("outer_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.outer_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.movie_frame = QtWidgets.QFrame(parent=self.outer_frame)
        self.movie_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.movie_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.movie_frame.setObjectName("movie_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.movie_frame)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.movie_label = QtWidgets.QLabel(parent=self.movie_frame)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        self.movie_label.setFont(font)
        self.movie_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.movie_label.setObjectName("movie_label")
        self.verticalLayout.addWidget(self.movie_label)
        self.movie_scroll_area = QtWidgets.QScrollArea(parent=self.movie_frame)
        self.movie_scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.movie_scroll_area.setWidgetResizable(True)
        self.movie_scroll_area.setObjectName("movie_scroll_area")
        self.movie_scroll_area_contents = QtWidgets.QWidget()
        self.movie_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 352, 439))
        self.movie_scroll_area_contents.setObjectName("movie_scroll_area_contents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.movie_scroll_area_contents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # self.liked_movie_frame = QtWidgets.QFrame(parent=self.movie_scroll_area_contents)
        # self.liked_movie_frame.setMinimumSize(QtCore.QSize(0, 160))
        # self.liked_movie_frame.setMaximumSize(QtCore.QSize(16777215, 160))
        # self.liked_movie_frame.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.liked_movie_frame.setStyleSheet("background-color: rgb(13, 249, 249);")
        # self.liked_movie_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.liked_movie_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        # self.liked_movie_frame.setObjectName("liked_movie_frame")
        # self.gridLayout = QtWidgets.QGridLayout(self.liked_movie_frame)
        # self.gridLayout.setObjectName("gridLayout")
        # self.temp_movie_poster = QtWidgets.QLabel(parent=self.liked_movie_frame)
        # self.temp_movie_poster.setMinimumSize(QtCore.QSize(0, 138))
        # self.temp_movie_poster.setMaximumSize(QtCore.QSize(92, 138))
        # self.temp_movie_poster.setText("")
        # self.temp_movie_poster.setScaledContents(True)
        # self.temp_movie_poster.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_movie_poster.setObjectName("temp_movie_poster")
        # self.gridLayout.addWidget(self.temp_movie_poster, 0, 0, 5, 1)
        # spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        # self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        # self.temp_movie_title = QtWidgets.QLabel(parent=self.liked_movie_frame)
        # self.temp_movie_title.setMinimumSize(QtCore.QSize(0, 30))
        # self.temp_movie_title.setMaximumSize(QtCore.QSize(200, 50))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_movie_title.setFont(font)
        # self.temp_movie_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_movie_title.setObjectName("temp_movie_title")
        # self.gridLayout.addWidget(self.temp_movie_title, 0, 2, 1, 2)
        # self.remove_from_liked_movie = QtWidgets.QPushButton(parent=self.liked_movie_frame)
        # font = QtGui.QFont()
        # font.setFamily("Oswald Medium")
        # font.setPointSize(10)
        # font.setBold(False)
        # font.setWeight(50)
        # self.remove_from_liked_movie.setFont(font)
        # self.remove_from_liked_movie.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.remove_from_liked_movie.setObjectName("remove_from_liked_movie")
        # self.gridLayout.addWidget(self.remove_from_liked_movie, 3, 2, 1, 2)
        # self.temp_movie_runtime = QtWidgets.QLabel(parent=self.liked_movie_frame)
        # self.temp_movie_runtime.setMinimumSize(QtCore.QSize(0, 30))
        # self.temp_movie_runtime.setMaximumSize(QtCore.QSize(16777215, 30))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_movie_runtime.setFont(font)
        # self.temp_movie_runtime.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_movie_runtime.setObjectName("temp_movie_runtime")
        # self.gridLayout.addWidget(self.temp_movie_runtime, 2, 2, 1, 2)
        # self.temp_movie_year = QtWidgets.QLabel(parent=self.liked_movie_frame)
        # self.temp_movie_year.setMinimumSize(QtCore.QSize(0, 30))
        # self.temp_movie_year.setMaximumSize(QtCore.QSize(16777215, 50))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_movie_year.setFont(font)
        # self.temp_movie_year.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_movie_year.setObjectName("temp_movie_year")
        # self.gridLayout.addWidget(self.temp_movie_year, 1, 2, 1, 2)
        # self.verticalLayout_4.addWidget(self.liked_movie_frame)

        # spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.verticalLayout_4.addItem(spacerItem1)

        self.movie_scroll_area.setWidget(self.movie_scroll_area_contents)
        self.verticalLayout.addWidget(self.movie_scroll_area)
        self.horizontalLayout.addWidget(self.movie_frame)
        self.v_line = QtWidgets.QFrame(parent=self.outer_frame)
        self.v_line.setStyleSheet("color: rgb(186, 188, 180)")
        self.v_line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.v_line.setLineWidth(5)
        self.v_line.setMidLineWidth(5)
        self.v_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.v_line.setObjectName("v_line")
        self.horizontalLayout.addWidget(self.v_line)

        # self.tv_show_frame = QtWidgets.QFrame(parent=self.outer_frame)
        # self.tv_show_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.tv_show_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        # self.tv_show_frame.setObjectName("tv_show_frame")
        # self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tv_show_frame)
        # self.verticalLayout_3.setObjectName("verticalLayout_3")
        # self.tv_show_label = QtWidgets.QLabel(parent=self.tv_show_frame)
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(16)
        # self.tv_show_label.setFont(font)
        # self.tv_show_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.tv_show_label.setObjectName("tv_show_label")
        # self.verticalLayout_3.addWidget(self.tv_show_label)
        # self.tv_show_scroll_area = QtWidgets.QScrollArea(parent=self.tv_show_frame)
        # self.tv_show_scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # self.tv_show_scroll_area.setWidgetResizable(True)
        # self.tv_show_scroll_area.setObjectName("tv_show_scroll_area")
        # self.tv_show_scroll_area_contents = QtWidgets.QWidget()
        # self.tv_show_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 352, 439))
        # self.tv_show_scroll_area_contents.setObjectName("tv_show_scroll_area_contents")
        # self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tv_show_scroll_area_contents)
        # self.verticalLayout_5.setObjectName("verticalLayout_5")
        # self.liked_tv_show_frame = QtWidgets.QFrame(parent=self.tv_show_scroll_area_contents)
        # self.liked_tv_show_frame.setMinimumSize(QtCore.QSize(0, 160))
        # self.liked_tv_show_frame.setMaximumSize(QtCore.QSize(16777215, 160))
        # self.liked_tv_show_frame.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.liked_tv_show_frame.setStyleSheet("background-color: rgb(255, 85, 0)")
        # self.liked_tv_show_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.liked_tv_show_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        # self.liked_tv_show_frame.setObjectName("liked_tv_show_frame")
        # self.gridLayout_2 = QtWidgets.QGridLayout(self.liked_tv_show_frame)
        # self.gridLayout_2.setObjectName("gridLayout_2")
        # self.temp_tv_show_poster = QtWidgets.QLabel(parent=self.liked_tv_show_frame)
        # self.temp_tv_show_poster.setMaximumSize(QtCore.QSize(92, 138))
        # self.temp_tv_show_poster.setText("")
        # self.temp_tv_show_poster.setScaledContents(True)
        # self.temp_tv_show_poster.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_tv_show_poster.setObjectName("temp_tv_show_poster")
        # self.gridLayout_2.addWidget(self.temp_tv_show_poster, 0, 0, 5, 1)
        # spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        # self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        # self.temp_tv_show_title = QtWidgets.QLabel(parent=self.liked_tv_show_frame)
        # self.temp_tv_show_title.setMinimumSize(QtCore.QSize(0, 30))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_tv_show_title.setFont(font)
        # self.temp_tv_show_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_tv_show_title.setObjectName("temp_tv_show_title")
        # self.gridLayout_2.addWidget(self.temp_tv_show_title, 0, 2, 1, 2)
        # self.remove_from_liked_tv_show = QtWidgets.QPushButton(parent=self.liked_tv_show_frame)
        # font = QtGui.QFont()
        # font.setFamily("Oswald Medium")
        # font.setPointSize(10)
        # self.remove_from_liked_tv_show.setFont(font)
        # self.remove_from_liked_tv_show.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.remove_from_liked_tv_show.setObjectName("remove_from_liked_tv_show")
        # self.gridLayout_2.addWidget(self.remove_from_liked_tv_show, 3, 2, 1, 2)
        # self.temp_tv_show_year = QtWidgets.QLabel(parent=self.liked_tv_show_frame)
        # self.temp_tv_show_year.setMinimumSize(QtCore.QSize(0, 30))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_tv_show_year.setFont(font)
        # self.temp_tv_show_year.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_tv_show_year.setObjectName("temp_tv_show_year")
        # self.gridLayout_2.addWidget(self.temp_tv_show_year, 1, 2, 1, 2)
        # self.temp_tv_show_seasons = QtWidgets.QLabel(parent=self.liked_tv_show_frame)
        # self.temp_tv_show_seasons.setMinimumSize(QtCore.QSize(0, 30))
        # font = QtGui.QFont()
        # font.setFamily("Oswald")
        # font.setPointSize(10)
        # self.temp_tv_show_seasons.setFont(font)
        # self.temp_tv_show_seasons.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.temp_tv_show_seasons.setObjectName("temp_tv_show_seasons")
        # self.gridLayout_2.addWidget(self.temp_tv_show_seasons, 2, 2, 1, 2)
        # self.verticalLayout_5.addWidget(self.liked_tv_show_frame)

        # spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.verticalLayout_5.addItem(spacerItem3)

        self.tv_show_scroll_area.setWidget(self.tv_show_scroll_area_contents)
        self.verticalLayout_3.addWidget(self.tv_show_scroll_area)
        self.horizontalLayout.addWidget(self.tv_show_frame)
        self.verticalLayout_2.addWidget(self.outer_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "[name]\'s"))
        self.header_label.setText(_translate("MainWindow", "[name]\'s"))
        self.movie_label.setText(_translate("MainWindow", "Movies"))
        self.tv_show_label.setText(_translate("MainWindow", "TV Shows"))

        # self.temp_movie_title.setText(_translate("MainWindow", "Avengers: Infinity War Of the Universe"))
        self.remove_from_liked_movie.setText(_translate("MainWindow", "Remove"))
        # self.temp_movie_runtime.setText(_translate("MainWindow", "1 hr and 50 mins"))
        # self.temp_movie_year.setText(_translate("MainWindow", "2012"))
        #
        # self.temp_tv_show_title.setText(_translate("MainWindow", "Avengers: Infinity War Of the Universe"))
        self.remove_from_liked_tv_show.setText(_translate("MainWindow", "Remove"))
        # self.temp_tv_show_year.setText(_translate("MainWindow", "2012"))
        # self.temp_tv_show_seasons.setText(_translate("MainWindow", "12 seasons + 1 special"))
