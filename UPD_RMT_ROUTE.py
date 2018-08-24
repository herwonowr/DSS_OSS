# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UPD_RMT_ROUTE.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Ui_UPD_RMT_ROUTE(object):
    def setupUi(self, Ui_UPD_RMT_ROUTE):
        Ui_UPD_RMT_ROUTE.setObjectName("Ui_UPD_RMT_ROUTE")
        Ui_UPD_RMT_ROUTE.resize(1083, 896)
        Ui_UPD_RMT_ROUTE.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.centralwidget = QtWidgets.QWidget(Ui_UPD_RMT_ROUTE)
        self.centralwidget.setObjectName("centralwidget")
        self.OP = QtWidgets.QLineEdit(self.centralwidget)
        self.OP.setGeometry(QtCore.QRect(70, 40, 211, 21))
        self.OP.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.OP.setObjectName("OP")
        self.OP_LIST = QtWidgets.QComboBox(self.centralwidget)
        self.OP_LIST.setGeometry(QtCore.QRect(70, 70, 211, 21))
        self.OP_LIST.setObjectName("OP_LIST")
        self.RMT_TABLE = QtWidgets.QTableView(self.centralwidget)
        self.RMT_TABLE.setGeometry(QtCore.QRect(70, 230, 291, 281))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RMT_TABLE.sizePolicy().hasHeightForWidth())
        self.RMT_TABLE.setSizePolicy(sizePolicy)
        self.RMT_TABLE.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.RMT_TABLE.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RMT_TABLE.setInputMethodHints(QtCore.Qt.ImhNone)
        self.RMT_TABLE.setObjectName("RMT_TABLE")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(70, 170, 181, 31))
        self.textEdit.setObjectName("textEdit")
        self.OP_LIST.raise_()
        self.OP.raise_()
        self.RMT_TABLE.raise_()
        self.textEdit.raise_()
        Ui_UPD_RMT_ROUTE.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Ui_UPD_RMT_ROUTE)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1083, 21))
        self.menubar.setObjectName("menubar")
        Ui_UPD_RMT_ROUTE.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Ui_UPD_RMT_ROUTE)
        self.statusbar.setObjectName("statusbar")
        Ui_UPD_RMT_ROUTE.setStatusBar(self.statusbar)

        self.retranslateUi(Ui_UPD_RMT_ROUTE)
        QtCore.QMetaObject.connectSlotsByName(Ui_UPD_RMT_ROUTE)

    def retranslateUi(self, Ui_UPD_RMT_ROUTE):
        _translate = QtCore.QCoreApplication.translate
        Ui_UPD_RMT_ROUTE.setWindowTitle(_translate("Ui_UPD_RMT_ROUTE", "MainWindow"))
        Ui_UPD_RMT_ROUTE.setToolTip(_translate("Ui_UPD_RMT_ROUTE", "<html><head/><body><p><br/></p></body></html>"))
        self.textEdit.setHtml(_translate("Ui_UPD_RMT_ROUTE", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">RMT ROUTE TABLE</p></body></html>"))

