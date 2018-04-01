from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import sys, os
os.environ['QT_DEBUG_PLUGINS'] = "0"

import browser


class Browser(QtWidgets.QMainWindow, browser.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(
          QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(
          QtWebEngineWidgets.QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webView.page().fullScreenRequested.connect(
          lambda request: request.accept())
        #self.player = QtMultimedia.QMediaPlayer(self)
        #url = QtCore.QUrl.fromLocalFile("F:\\Users\\JimmyGtr11\\Music\\iTunes\\iTunes Media\\Music\\Smash Mouth\\Unknown Album\\All Star.mp3")
        #self.player.setMedia(QtMultimedia.QMediaContent(url))
        #self.player.setVolume(50)
        
        self.tb_search.clicked.connect(self.search)
        self.tb_back.clicked.connect(self.embed)

    def search(self):
        text = self.address_bar.text()
        url = QtCore.QUrl(text)
        self.webView.load(url)
    
    def embed(self):
        #allow="autoplay; encrypted-media"
        html = '<iframe width="560" height="315" \
        src="https://www.youtube.com/embed/3_eQbg8tuns" \
        frameborder="0" allowfullscreen></iframe>'

        self.webView.setHtml(html, QtCore.QUrl(''))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    ui = Browser()
    ui.show()

    sys.exit(app.exec_())
