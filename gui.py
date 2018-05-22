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
        MainWindow.resize(805, 524)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/search.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
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
        self.yt_webView.setUrl(QtCore.QUrl("about:blank"))
        self.yt_webView.setObjectName("yt_webView")
        self.verticalLayout_2.addWidget(self.yt_webView)
        self.url_test = QtWidgets.QPushButton(self.tab_yt)
        self.url_test.setObjectName("url_test")
        self.verticalLayout_2.addWidget(self.url_test)
        self.tabWidget.addTab(self.tab_yt, "")
        self.tab_pd = QtWidgets.QWidget()
        self.tab_pd.setObjectName("tab_pd")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_pd)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pd_webView = QtWebEngineWidgets.QWebEngineView(self.tab_pd)
        self.pd_webView.setUrl(QtCore.QUrl("about:blank"))
        self.pd_webView.setObjectName("pd_webView")
        self.verticalLayout_3.addWidget(self.pd_webView)
        self.html_test = QtWidgets.QPushButton(self.tab_pd)
        self.html_test.setObjectName("html_test")
        self.verticalLayout_3.addWidget(self.html_test)
        self.layout_dl = QtWidgets.QHBoxLayout()
        self.layout_dl.setContentsMargins(-1, 0, -1, -1)
        self.layout_dl.setObjectName("layout_dl")
        self.layout_trackInfo = QtWidgets.QVBoxLayout()
        self.layout_trackInfo.setContentsMargins(0, -1, -1, -1)
        self.layout_trackInfo.setObjectName("layout_trackInfo")
        self.layout_headers = QtWidgets.QHBoxLayout()
        self.layout_headers.setObjectName("layout_headers")
        self.hdr_title = QtWidgets.QLabel(self.tab_pd)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hdr_title.setFont(font)
        self.hdr_title.setAlignment(QtCore.Qt.AlignCenter)
        self.hdr_title.setObjectName("hdr_title")
        self.layout_headers.addWidget(self.hdr_title)
        self.hdr_artist = QtWidgets.QLabel(self.tab_pd)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hdr_artist.setFont(font)
        self.hdr_artist.setAlignment(QtCore.Qt.AlignCenter)
        self.hdr_artist.setObjectName("hdr_artist")
        self.layout_headers.addWidget(self.hdr_artist)
        self.hdr_album = QtWidgets.QLabel(self.tab_pd)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hdr_album.setFont(font)
        self.hdr_album.setAlignment(QtCore.Qt.AlignCenter)
        self.hdr_album.setObjectName("hdr_album")
        self.layout_headers.addWidget(self.hdr_album)
        self.layout_headers.setStretch(0, 1)
        self.layout_headers.setStretch(1, 1)
        self.layout_headers.setStretch(2, 1)
        self.layout_trackInfo.addLayout(self.layout_headers)
        self.layout_inputs = QtWidgets.QHBoxLayout()
        self.layout_inputs.setContentsMargins(-1, 0, -1, -1)
        self.layout_inputs.setObjectName("layout_inputs")
        self.lbl_title = QtWidgets.QLineEdit(self.tab_pd)
        self.lbl_title.setObjectName("lbl_title")
        self.layout_inputs.addWidget(self.lbl_title)
        self.lbl_artist = QtWidgets.QLineEdit(self.tab_pd)
        self.lbl_artist.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_artist.sizePolicy().hasHeightForWidth())
        self.lbl_artist.setSizePolicy(sizePolicy)
        self.lbl_artist.setMinimumSize(QtCore.QSize(0, 0))
        self.lbl_artist.setObjectName("lbl_artist")
        self.layout_inputs.addWidget(self.lbl_artist)
        self.lbl_album = QtWidgets.QLineEdit(self.tab_pd)
        self.lbl_album.setObjectName("lbl_album")
        self.layout_inputs.addWidget(self.lbl_album)
        self.layout_inputs.setStretch(0, 1)
        self.layout_inputs.setStretch(1, 1)
        self.layout_inputs.setStretch(2, 1)
        self.layout_trackInfo.addLayout(self.layout_inputs)
        self.layout_dl.addLayout(self.layout_trackInfo)
        self.pb_download = QtWidgets.QPushButton(self.tab_pd)
        self.pb_download.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_download.sizePolicy().hasHeightForWidth())
        self.pb_download.setSizePolicy(sizePolicy)
        self.pb_download.setMinimumSize(QtCore.QSize(0, 50))
        self.pb_download.setObjectName("pb_download")
        self.layout_dl.addWidget(self.pb_download)
        self.layout_dl.setStretch(0, 4)
        self.layout_dl.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.layout_dl)
        self.tabWidget.addTab(self.tab_pd, "")
        self.tab_it = QtWidgets.QWidget()
        self.tab_it.setObjectName("tab_it")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_it)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.layout_controls = QtWidgets.QHBoxLayout()
        self.layout_controls.setContentsMargins(-1, 0, -1, 0)
        self.layout_controls.setSpacing(15)
        self.layout_controls.setObjectName("layout_controls")
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_buttons.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layout_buttons.setContentsMargins(-1, 0, -1, 0)
        self.layout_buttons.setSpacing(10)
        self.layout_buttons.setObjectName("layout_buttons")
        self.tb_back = QtWidgets.QToolButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back.sizePolicy().hasHeightForWidth())
        self.tb_back.setSizePolicy(sizePolicy)
        self.tb_back.setMinimumSize(QtCore.QSize(30, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_back.setIcon(icon1)
        self.tb_back.setObjectName("tb_back")
        self.layout_buttons.addWidget(self.tb_back)
        self.tb_playPause = QtWidgets.QToolButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_playPause.sizePolicy().hasHeightForWidth())
        self.tb_playPause.setSizePolicy(sizePolicy)
        self.tb_playPause.setMinimumSize(QtCore.QSize(30, 30))
        self.tb_playPause.setFocusPolicy(QtCore.Qt.NoFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_playPause.setIcon(icon2)
        self.tb_playPause.setCheckable(False)
        self.tb_playPause.setChecked(False)
        self.tb_playPause.setObjectName("tb_playPause")
        self.layout_buttons.addWidget(self.tb_playPause)
        self.tb_forward = QtWidgets.QToolButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_forward.sizePolicy().hasHeightForWidth())
        self.tb_forward.setSizePolicy(sizePolicy)
        self.tb_forward.setMinimumSize(QtCore.QSize(30, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_forward.setIcon(icon3)
        self.tb_forward.setObjectName("tb_forward")
        self.layout_buttons.addWidget(self.tb_forward)
        self.slider_volume = QtWidgets.QSlider(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider_volume.sizePolicy().hasHeightForWidth())
        self.slider_volume.setSizePolicy(sizePolicy)
        self.slider_volume.setMinimumSize(QtCore.QSize(84, 22))
        self.slider_volume.setOrientation(QtCore.Qt.Horizontal)
        self.slider_volume.setObjectName("slider_volume")
        self.layout_buttons.addWidget(self.slider_volume)
        self.layout_controls.addLayout(self.layout_buttons)
        self.layout_info = QtWidgets.QVBoxLayout()
        self.layout_info.setContentsMargins(-1, 0, -1, -1)
        self.layout_info.setSpacing(1)
        self.layout_info.setObjectName("layout_info")
        self.layout_song = QtWidgets.QHBoxLayout()
        self.layout_song.setSpacing(6)
        self.layout_song.setObjectName("layout_song")
        self.tb_shuffle = QtWidgets.QToolButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_shuffle.sizePolicy().hasHeightForWidth())
        self.tb_shuffle.setSizePolicy(sizePolicy)
        self.tb_shuffle.setMinimumSize(QtCore.QSize(30, 20))
        self.tb_shuffle.setObjectName("tb_shuffle")
        self.layout_song.addWidget(self.tb_shuffle)
        self.song_name = QtWidgets.QLabel(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.song_name.sizePolicy().hasHeightForWidth())
        self.song_name.setSizePolicy(sizePolicy)
        self.song_name.setMinimumSize(QtCore.QSize(200, 20))
        self.song_name.setAlignment(QtCore.Qt.AlignCenter)
        self.song_name.setObjectName("song_name")
        self.layout_song.addWidget(self.song_name)
        self.tb_repeat = QtWidgets.QToolButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_repeat.sizePolicy().hasHeightForWidth())
        self.tb_repeat.setSizePolicy(sizePolicy)
        self.tb_repeat.setMinimumSize(QtCore.QSize(30, 20))
        self.tb_repeat.setObjectName("tb_repeat")
        self.layout_song.addWidget(self.tb_repeat)
        self.layout_info.addLayout(self.layout_song)
        self.layout_artist = QtWidgets.QHBoxLayout()
        self.layout_artist.setContentsMargins(-1, 0, -1, -1)
        self.layout_artist.setObjectName("layout_artist")
        self.time_elapsed = QtWidgets.QLabel(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_elapsed.sizePolicy().hasHeightForWidth())
        self.time_elapsed.setSizePolicy(sizePolicy)
        self.time_elapsed.setMinimumSize(QtCore.QSize(0, 10))
        self.time_elapsed.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.time_elapsed.setFont(font)
        self.time_elapsed.setObjectName("time_elapsed")
        self.layout_artist.addWidget(self.time_elapsed)
        self.artist = QtWidgets.QLabel(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.artist.sizePolicy().hasHeightForWidth())
        self.artist.setSizePolicy(sizePolicy)
        self.artist.setMinimumSize(QtCore.QSize(0, 10))
        self.artist.setMaximumSize(QtCore.QSize(16777215, 10))
        self.artist.setAlignment(QtCore.Qt.AlignCenter)
        self.artist.setObjectName("artist")
        self.layout_artist.addWidget(self.artist)
        self.time_remaining = QtWidgets.QLabel(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_remaining.sizePolicy().hasHeightForWidth())
        self.time_remaining.setSizePolicy(sizePolicy)
        self.time_remaining.setMinimumSize(QtCore.QSize(0, 10))
        self.time_remaining.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(7)
        font.setKerning(True)
        self.time_remaining.setFont(font)
        self.time_remaining.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_remaining.setObjectName("time_remaining")
        self.layout_artist.addWidget(self.time_remaining)
        self.layout_info.addLayout(self.layout_artist)
        self.layout_seek = QtWidgets.QHBoxLayout()
        self.layout_seek.setContentsMargins(-1, 0, -1, -1)
        self.layout_seek.setObjectName("layout_seek")
        self.slider_seek = QtWidgets.QSlider(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider_seek.sizePolicy().hasHeightForWidth())
        self.slider_seek.setSizePolicy(sizePolicy)
        self.slider_seek.setMinimumSize(QtCore.QSize(282, 15))
        self.slider_seek.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_seek.setOrientation(QtCore.Qt.Horizontal)
        self.slider_seek.setObjectName("slider_seek")
        self.layout_seek.addWidget(self.slider_seek)
        self.layout_info.addLayout(self.layout_seek)
        self.layout_controls.addLayout(self.layout_info)
        self.layout_search = QtWidgets.QHBoxLayout()
        self.layout_search.setContentsMargins(-1, 0, -1, 0)
        self.layout_search.setObjectName("layout_search")
        self.search = QtWidgets.QLineEdit(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search.sizePolicy().hasHeightForWidth())
        self.search.setSizePolicy(sizePolicy)
        self.search.setMinimumSize(QtCore.QSize(135, 22))
        self.search.setFrame(True)
        self.search.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.search.setClearButtonEnabled(False)
        self.search.setObjectName("search")
        self.layout_search.addWidget(self.search)
        self.layout_controls.addLayout(self.layout_search)
        self.layout_controls.setStretch(1, 3)
        self.layout_controls.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.layout_controls)
        self.library = QtWidgets.QTableWidget(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.library.sizePolicy().hasHeightForWidth())
        self.library.setSizePolicy(sizePolicy)
        self.library.setFocusPolicy(QtCore.Qt.NoFocus)
        self.library.setAutoFillBackground(False)
        self.library.setMidLineWidth(0)
        self.library.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.library.setAlternatingRowColors(False)
        self.library.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.library.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.library.setShowGrid(False)
        self.library.setWordWrap(True)
        self.library.setCornerButtonEnabled(True)
        self.library.setRowCount(0)
        self.library.setObjectName("library")
        self.library.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.library.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.library.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.library.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.library.setHorizontalHeaderItem(3, item)
        self.library.horizontalHeader().setCascadingSectionResizes(False)
        self.library.horizontalHeader().setStretchLastSection(True)
        self.library.verticalHeader().setVisible(False)
        self.verticalLayout_4.addWidget(self.library)
        self.pb_dir = QtWidgets.QPushButton(self.tab_it)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_dir.sizePolicy().hasHeightForWidth())
        self.pb_dir.setSizePolicy(sizePolicy)
        self.pb_dir.setAutoDefault(False)
        self.pb_dir.setDefault(False)
        self.pb_dir.setFlat(False)
        self.pb_dir.setObjectName("pb_dir")
        self.verticalLayout_4.addWidget(self.pb_dir)
        self.tabWidget.addTab(self.tab_it, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 21))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MusicSuite"))
        self.url_test.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_yt), _translate("MainWindow", "YouTube"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_yt), _translate("MainWindow", "YouTube"))
        self.html_test.setText(_translate("MainWindow", "PushButton"))
        self.hdr_title.setText(_translate("MainWindow", "Title"))
        self.hdr_artist.setText(_translate("MainWindow", "Artist"))
        self.hdr_album.setText(_translate("MainWindow", "Album"))
        self.lbl_title.setText(_translate("MainWindow", "fdsadfdsf"))
        self.lbl_artist.setText(_translate("MainWindow", "aswdefa"))
        self.lbl_album.setText(_translate("MainWindow", "asdfasdf"))
        self.pb_download.setText(_translate("MainWindow", "Download"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pd), _translate("MainWindow", "Pandora"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_pd), _translate("MainWindow", "Pandora"))
        self.tb_back.setText(_translate("MainWindow", "..."))
        self.tb_playPause.setText(_translate("MainWindow", "..."))
        self.tb_forward.setText(_translate("MainWindow", "..."))
        self.tb_shuffle.setText(_translate("MainWindow", "..."))
        self.song_name.setText(_translate("MainWindow", "TextLabel"))
        self.tb_repeat.setText(_translate("MainWindow", "..."))
        self.time_elapsed.setText(_translate("MainWindow", "TextLabel"))
        self.artist.setText(_translate("MainWindow", "TextLabel"))
        self.time_remaining.setText(_translate("MainWindow", "TextLabel"))
        self.library.setSortingEnabled(True)
        item = self.library.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Title"))
        item = self.library.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Time"))
        item = self.library.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Artist"))
        item = self.library.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Album"))
        self.pb_dir.setText(_translate("MainWindow", "Choose a file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_it), _translate("MainWindow", "iTunes"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_it), _translate("MainWindow", "iTunes"))

from PyQt5 import QtWebEngineWidgets
import resource_rc
