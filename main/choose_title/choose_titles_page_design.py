# Form implementation generated from reading ui file 'choose-titles-page.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

from main.choose_title.posters import Poster


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(889, 664)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 321))
        self.widget_2.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label_0 = Poster(parent=self.widget_2)
        self.label_0.setMinimumSize(QtCore.QSize(211, 0))
        self.label_0.setMaximumSize(QtCore.QSize(211, 16777215))
        self.label_0.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.label_0.setPixmap(QtGui.QPixmap(":/newPrefix/1.jpg"))
        self.label_0.setScaledContents(True)
        self.label_0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_0.setObjectName("label_0")
        self.horizontalLayout.addWidget(self.label_0)

        self.label_1 = Poster(parent=self.widget_2)
        self.label_1.setMinimumSize(QtCore.QSize(211, 0))
        self.label_1.setMaximumSize(QtCore.QSize(211, 16777215))
        self.label_1.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.label_1.setPixmap(QtGui.QPixmap(":/newPrefix/1.jpg"))
        self.label_1.setScaledContents(True)
        self.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout.addWidget(self.label_1)

        self.label_4 = Poster(parent=self.widget_2)
        self.label_4.setMinimumSize(QtCore.QSize(211, 0))
        self.label_4.setMaximumSize(QtCore.QSize(211, 16777215))
        self.label_4.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.label_4.setPixmap(QtGui.QPixmap(":/newPrefix/1.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)

        self.label_3 = Poster(parent=self.widget_2)
        self.label_3.setMinimumSize(QtCore.QSize(211, 0))
        self.label_3.setMaximumSize(QtCore.QSize(211, 16777215))
        self.label_3.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.label_3.setPixmap(QtGui.QPixmap(":/newPrefix/1.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 331))
        self.widget.setStyleSheet("border-width: 1px;\n"
"border-color: black;\n"
"border-style: outset;")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Choose a Movie or a TV Show"))
        self.label_0.setText(_translate("MainWindow", "temp"))
        self.label_1.setText(_translate("MainWindow", "temp"))
        self.label_4.setText(_translate("MainWindow", "temp"))
        self.label_3.setText(_translate("MainWindow", "temp"))
        self.label_2.setText(_translate("MainWindow", "test"))
