# Form implementation generated from reading ui file 'operation-confirmation-dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(425, 100)
        Dialog.setMinimumSize(QtCore.QSize(425, 100))
        Dialog.setMaximumSize(QtCore.QSize(425, 100))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.header_label = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(16)
        self.header_label.setFont(font)
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.gridLayout.addWidget(self.header_label, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Oswald")
        font.setPointSize(10)
        self.button_box.setFont(font)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.header_label.setText(_translate("Dialog", "Placeholder text"))
