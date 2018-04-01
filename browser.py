# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tb_back = QtWidgets.QToolButton(self.centralwidget)
        self.tb_back.setGeometry(QtCore.QRect(20, 25, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/back.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_back.setIcon(icon)
        self.tb_back.setObjectName("tb_back")
        self.tb_forward = QtWidgets.QToolButton(self.centralwidget)
        self.tb_forward.setGeometry(QtCore.QRect(70, 25, 30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/forward.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_forward.setIcon(icon1)
        self.tb_forward.setObjectName("tb_forward")
        self.tb_refresh = QtWidgets.QToolButton(self.centralwidget)
        self.tb_refresh.setGeometry(QtCore.QRect(120, 25, 30, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_refresh.setIcon(icon2)
        self.tb_refresh.setObjectName("tb_refresh")
        self.tb_home = QtWidgets.QToolButton(self.centralwidget)
        self.tb_home.setGeometry(QtCore.QRect(170, 25, 30, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/home.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_home.setIcon(icon3)
        self.tb_home.setObjectName("tb_home")
        self.tb_search = QtWidgets.QToolButton(self.centralwidget)
        self.tb_search.setGeometry(QtCore.QRect(670, 25, 30, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/search.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_search.setIcon(icon4)
        self.tb_search.setObjectName("tb_search")
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webView.setEnabled(True)
        self.webView.setGeometry(QtCore.QRect(0, 80, 800, 479))
        self.webView.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.webView.setAutoFillBackground(True)
        self.webView.setProperty("url", QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.address_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.address_bar.setGeometry(QtCore.QRect(220, 25, 451, 30))
        self.address_bar.setObjectName("address_bar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tb_back.setText(_translate("MainWindow", "..."))
        self.tb_forward.setText(_translate("MainWindow", "..."))
        self.tb_refresh.setText(_translate("MainWindow", "..."))
        self.tb_home.setText(_translate("MainWindow", "..."))
        self.tb_search.setText(_translate("MainWindow", "..."))

from PyQt5 import QtWebEngineWidgets
import resource_rc
