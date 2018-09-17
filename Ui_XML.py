# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_XML.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_XML(object):
    def setupUi(self, XML):
        XML.setObjectName("XML")
        XML.resize(1333, 692)
        self.centralwidget = QtWidgets.QWidget(XML)
        self.centralwidget.setObjectName("centralwidget")
        self.ComboBox_DSC = QtWidgets.QComboBox(self.centralwidget)
        self.ComboBox_DSC.setGeometry(QtCore.QRect(230, 90, 151, 21))
        self.ComboBox_DSC.setObjectName("ComboBox_DSC")
        self.DOWN_XML = QtWidgets.QPushButton(self.centralwidget)
        self.DOWN_XML.setGeometry(QtCore.QRect(60, 90, 151, 31))
        self.DOWN_XML.setObjectName("DOWN_XML")
        self.BUILD_PEER = QtWidgets.QPushButton(self.centralwidget)
        self.BUILD_PEER.setGeometry(QtCore.QRect(60, 140, 151, 23))
        self.BUILD_PEER.setObjectName("BUILD_PEER")
        self.MERGE_IP_HOST = QtWidgets.QPushButton(self.centralwidget)
        self.MERGE_IP_HOST.setGeometry(QtCore.QRect(60, 180, 151, 23))
        self.MERGE_IP_HOST.setObjectName("MERGE_IP_HOST")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(230, 70, 131, 21))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(60, 40, 371, 21))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(230, 180, 371, 21))
        self.label_19.setObjectName("label_19")
        self.BUILD_TEST_PEER = QtWidgets.QPushButton(self.centralwidget)
        self.BUILD_TEST_PEER.setGeometry(QtCore.QRect(60, 230, 151, 23))
        self.BUILD_TEST_PEER.setObjectName("BUILD_TEST_PEER")
        self.comboBox_OPTION = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_OPTION.setGeometry(QtCore.QRect(240, 230, 141, 22))
        self.comboBox_OPTION.setObjectName("comboBox_OPTION")
        XML.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(XML)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1333, 21))
        self.menubar.setObjectName("menubar")
        XML.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(XML)
        self.statusbar.setObjectName("statusbar")
        XML.setStatusBar(self.statusbar)

        self.retranslateUi(XML)
        QtCore.QMetaObject.connectSlotsByName(XML)

    def retranslateUi(self, XML):
        _translate = QtCore.QCoreApplication.translate
        XML.setWindowTitle(_translate("XML", "MainWindow"))
        self.DOWN_XML.setText(_translate("XML", "DownLoad XML/Build host"))
        self.BUILD_PEER.setText(_translate("XML", "Build Peer Info from DSC XML"))
        self.MERGE_IP_HOST.setText(_translate("XML", "Merge IP_Host file"))
        self.label_17.setText(_translate("XML", "Select DSC"))
        self.label_18.setText(_translate("XML", "XML on DSC will be updated once at 1:00 UTC each day"))
        self.label_19.setText(_translate("XML", "Put hosts file under C:Usersg800472AppDataRoamingWireshark"))
        self.BUILD_TEST_PEER.setText(_translate("XML", "grep 10302 from no test peer"))

