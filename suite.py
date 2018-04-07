from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import sys, os

os.environ['QT_DEBUG_PLUGINS'] = "0"

import browser
import itunes


class Suite(QMainWindow, browser.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(
          QWebEngineSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(
          QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webView.page().fullScreenRequested.connect(
          lambda request: request.accept())
        #self.player = QtMultimedia.QMediaPlayer(self)
        #url = QUrl.fromLocalFile("F:\\Users\\JimmyGtr11\\Music\\iTunes\\iTunes Media\\Music\\Smash Mouth\\Unknown Album\\All Star.mp3")
        #self.player.setMedia(QtMultimedia.QMediaContent(url))
        #self.player.setVolume(50)
        
        #self.tb_search.clicked.connect(self.search)
        #self.tb_back.clicked.connect(self.embed)
        self.pb_file.clicked.connect(self.get_dir)

    def search(self):
        text = self.address_bar.text()
        url = QUrl(text)
        self.webView.load(url)
    
    def embed(self):
        #allow="autoplay; encrypted-media"
        html = '<iframe width="560" height="315" \
        src="https://www.youtube.com/embed/3_eQbg8tuns" \
        frameborder="0" allowfullscreen></iframe>'

        self.webView.setHtml(html, QUrl(''))

    def get_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.ReadOnly
        self.dir = QFileDialog.getExistingDirectory(self,
          'Select directory...', 'C:/', options)
        print(self.dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Suite()
    ui.show()

    sys.exit(app.exec_())
