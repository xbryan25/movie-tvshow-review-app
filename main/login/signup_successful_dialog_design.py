# Form implementation generated from reading ui file 'signup-successful.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 100)
        Dialog.setMinimumSize(QtCore.QSize(250, 100))
        Dialog.setMaximumSize(QtCore.QSize(250, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.no_issues_label = QtWidgets.QLabel(parent=Dialog)
        self.no_issues_label.setMaximumSize(QtCore.QSize(227, 36))
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        self.no_issues_label.setFont(font)
        self.no_issues_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.no_issues_label.setObjectName("no_issues_label")
        self.verticalLayout.addWidget(self.no_issues_label)
        
        self.proceed_button = QtWidgets.QPushButton(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(11)
        self.proceed_button.setFont(font)
        self.proceed_button.setObjectName("proceed_button")
        self.verticalLayout.addWidget(self.proceed_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Signup successful!"))
        self.no_issues_label.setText(_translate("Dialog", "No issues signing up!"))
        self.proceed_button.setText(_translate("Dialog", "Click here to proceed"))
