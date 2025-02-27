# Form implementation generated from reading ui file 'signup-fail.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 150)
        Dialog.setMinimumSize(QtCore.QSize(250, 150))
        Dialog.setMaximumSize(QtCore.QSize(250, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.issues_found_label = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        self.issues_found_label.setFont(font)
        self.issues_found_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.issues_found_label.setObjectName("issues_found_label")
        self.verticalLayout.addWidget(self.issues_found_label)

        self.issues_list_label = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.issues_list_label.setFont(font)
        self.issues_list_label.setObjectName("issues_list_label")
        # self.issues_list_label.setStyleSheet("background-color: rgb(183, 196, 255)")
        self.verticalLayout.addWidget(self.issues_list_label)

        self.proceed_button = QtWidgets.QPushButton(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(11)
        self.proceed_button.setFont(font)
        self.proceed_button.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.proceed_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Signup failed."))
        self.issues_found_label.setText(_translate("Dialog", "Issues found:"))
        self.issues_list_label.setText(_translate("Dialog", "• Sample"))
        self.proceed_button.setText(_translate("Dialog", "Proceed"))
