# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_CONFIRM_WIN.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Confirm_Window(object):
    def setupUi(self, Confirm_Window):
        Confirm_Window.setObjectName("Confirm_Window")
        Confirm_Window.resize(640, 261)
        self.PROMPT = QtWidgets.QTextEdit(Confirm_Window)
        self.PROMPT.setGeometry(QtCore.QRect(40, 40, 551, 151))
        self.PROMPT.setObjectName("PROMPT")
        self.label = QtWidgets.QLabel(Confirm_Window)
        self.label.setGeometry(QtCore.QRect(40, 20, 47, 13))
        self.label.setObjectName("label")
        self.PROCEED = QtWidgets.QPushButton(Confirm_Window)
        self.PROCEED.setGeometry(QtCore.QRect(50, 210, 75, 23))
        self.PROCEED.setObjectName("PROCEED")
        self.CANCEL = QtWidgets.QPushButton(Confirm_Window)
        self.CANCEL.setGeometry(QtCore.QRect(160, 210, 75, 23))
        self.CANCEL.setObjectName("CANCEL")

        self.retranslateUi(Confirm_Window)
        QtCore.QMetaObject.connectSlotsByName(Confirm_Window)

    def retranslateUi(self, Confirm_Window):
        _translate = QtCore.QCoreApplication.translate
        Confirm_Window.setWindowTitle(_translate("Confirm_Window", "Confirm Window"))
        self.label.setText(_translate("Confirm_Window", "Prompt"))
        self.PROCEED.setText(_translate("Confirm_Window", "Proceed"))
        self.CANCEL.setText(_translate("Confirm_Window", "Cancel"))

