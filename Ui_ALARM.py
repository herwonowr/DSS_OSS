# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ALARM.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ALARM(object):
    def setupUi(self, ALARM):
        ALARM.setObjectName("ALARM")
        ALARM.resize(1333, 689)
        self.centralwidget = QtWidgets.QWidget(ALARM)
        self.centralwidget.setObjectName("centralwidget")
        self.ALARM_LIST = QtWidgets.QComboBox(self.centralwidget)
        self.ALARM_LIST.setGeometry(QtCore.QRect(60, 30, 151, 21))
        self.ALARM_LIST.setObjectName("ALARM_LIST")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(60, 10, 131, 21))
        self.label_17.setObjectName("label_17")
        self.GUIDE = QtWidgets.QTextEdit(self.centralwidget)
        self.GUIDE.setGeometry(QtCore.QRect(250, 30, 431, 151))
        self.GUIDE.setObjectName("GUIDE")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(250, 10, 131, 21))
        self.label_20.setObjectName("label_20")
        self.INPUT_BOX = QtWidgets.QTextEdit(self.centralwidget)
        self.INPUT_BOX.setGeometry(QtCore.QRect(730, 30, 431, 151))
        self.INPUT_BOX.setObjectName("INPUT_BOX")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(730, 10, 131, 21))
        self.label_21.setObjectName("label_21")
        self.SUMBIT_ALARM = QtWidgets.QPushButton(self.centralwidget)
        self.SUMBIT_ALARM.setGeometry(QtCore.QRect(730, 200, 75, 23))
        self.SUMBIT_ALARM.setObjectName("SUMBIT_ALARM")
        ALARM.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ALARM)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1333, 21))
        self.menubar.setObjectName("menubar")
        ALARM.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ALARM)
        self.statusbar.setObjectName("statusbar")
        ALARM.setStatusBar(self.statusbar)

        self.retranslateUi(ALARM)
        QtCore.QMetaObject.connectSlotsByName(ALARM)

    def retranslateUi(self, ALARM):
        _translate = QtCore.QCoreApplication.translate
        ALARM.setWindowTitle(_translate("ALARM", "MainWindow"))
        self.label_17.setText(_translate("ALARM", "Alarm"))
        self.label_20.setText(_translate("ALARM", "Guide"))
        self.label_21.setText(_translate("ALARM", "Input Box"))
        self.SUMBIT_ALARM.setText(_translate("ALARM", "Submit Alarm"))

