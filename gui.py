# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 741)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/search.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_yt = QtWidgets.QWidget()
        self.tab_yt.setObjectName("tab_yt")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_yt)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.yt_webView = QtWebEngineWidgets.QWebEngineView(self.tab_yt)
        self.yt_webView.setUrl(QtCore.QUrl("https://www.youtube.com/"))
        self.yt_webView.setObjectName("yt_webView")
        self.verticalLayout_2.addWidget(self.yt_webView)
        self.tabWidget.addTab(self.tab_yt, "")
        self.tab_pd = QtWidgets.QWidget()
        self.tab_pd.setObjectName("tab_pd")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_pd)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pd_webView = QtWebEngineWidgets.QWebEngineView(self.tab_pd)
        self.pd_webView.setUrl(QtCore.QUrl("https://www.pandora.com/"))
        self.pd_webView.setObjectName("pd_webView")
        self.verticalLayout_3.addWidget(self.pd_webView)
        self.tabWidget.addTab(self.tab_pd, "")
        self.tab_it = QtWidgets.QWidget()
        self.tab_it.setObjectName("tab_it")
        self.pb_dir = QtWidgets.QPushButton(self.tab_it)
        self.pb_dir.setGeometry(QtCore.QRect(380, 250, 161, 61))
        self.pb_dir.setAutoDefault(False)
        self.pb_dir.setDefault(False)
        self.pb_dir.setFlat(False)
        self.pb_dir.setObjectName("pb_dir")
        self.tabWidget.addTab(self.tab_it, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MusicSuite"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_yt), _translate("MainWindow", "YouTube"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_yt), _translate("MainWindow", "YouTube"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pd), _translate("MainWindow", "Pandora"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_pd), _translate("MainWindow", "Pandora"))
        self.pb_dir.setText(_translate("MainWindow", "Choose a file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_it), _translate("MainWindow", "iTunes"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_it), _translate("MainWindow", "iTunes"))

from PyQt5 import QtWebEngineWidgets
import resource_rc
