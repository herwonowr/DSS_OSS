# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_RMTCREDENTIAL.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RMT_CREDENTIAL(object):
    def setupUi(self, RMT_CREDENTIAL):
        RMT_CREDENTIAL.setObjectName("RMT_CREDENTIAL")
        RMT_CREDENTIAL.resize(384, 189)
        self.centralwidget = QtWidgets.QWidget(RMT_CREDENTIAL)
        self.centralwidget.setObjectName("centralwidget")
        self.RMT_USER = QtWidgets.QLineEdit(self.centralwidget)
        self.RMT_USER.setGeometry(QtCore.QRect(122, 40, 161, 20))
        self.RMT_USER.setObjectName("RMT_USER")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 71, 16))
        self.label_2.setObjectName("label_2")
        self.RMT_PWD = QtWidgets.QLineEdit(self.centralwidget)
        self.RMT_PWD.setGeometry(QtCore.QRect(120, 80, 161, 20))
        self.RMT_PWD.setObjectName("RMT_PWD")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 10, 221, 16))
        self.label_3.setObjectName("label_3")
        self.confirm = QtWidgets.QPushButton(self.centralwidget)
        self.confirm.setGeometry(QtCore.QRect(210, 110, 75, 23))
        self.confirm.setObjectName("confirm")
        RMT_CREDENTIAL.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RMT_CREDENTIAL)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 384, 21))
        self.menubar.setObjectName("menubar")
        RMT_CREDENTIAL.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RMT_CREDENTIAL)
        self.statusbar.setObjectName("statusbar")
        RMT_CREDENTIAL.setStatusBar(self.statusbar)

        self.retranslateUi(RMT_CREDENTIAL)
        QtCore.QMetaObject.connectSlotsByName(RMT_CREDENTIAL)

    def retranslateUi(self, RMT_CREDENTIAL):
        _translate = QtCore.QCoreApplication.translate
        RMT_CREDENTIAL.setWindowTitle(_translate("RMT_CREDENTIAL", "MainWindow"))
        self.label.setText(_translate("RMT_CREDENTIAL", "RMT Userame"))
        self.label_2.setText(_translate("RMT_CREDENTIAL", "RMT Pwd"))
        self.label_3.setText(_translate("RMT_CREDENTIAL", "Please input your RMT credential"))
        self.confirm.setText(_translate("RMT_CREDENTIAL", "Confirm"))

