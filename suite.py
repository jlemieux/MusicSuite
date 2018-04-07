from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import sys, os

os.environ['QT_DEBUG_PLUGINS'] = "0"

from gui import Ui_MainWindow

from views.youtube import YouTube
from views.pandora import Pandora
from views.itunes import iTunes


class Suite(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.yt = YouTube(self)
        self.pd = Pandora(self)
        self.it = iTunes(self)

        #self.player = QtMultimedia.QMediaPlayer(self)
        #url = QUrl.fromLocalFile("F:\\Users\\JimmyGtr11\\Music\\iTunes\\iTunes Media\\Music\\Smash Mouth\\Unknown Album\\All Star.mp3")
        #self.player.setMedia(QtMultimedia.QMediaContent(url))
        #self.player.setVolume(50)

    '''
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
    '''

if __name__ == '__main__':
    app = QApplication(sys.argv)

    suite = Suite()
    suite.show()

    sys.exit(app.exec_())
