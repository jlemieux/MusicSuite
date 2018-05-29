from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class PandoraDownloadPanel(object):
    def __init__(self, gui):
        self.gui = gui
        self.btn_download = self.gui.pb_download
        self.btn_find_album = self.gui.pb_findAlbum
        self.title = self.gui.lbl_title
        self.artist = self.gui.lbl_artist
        self.album = self.gui.lbl_album

    def enable(self):
        self.btn_download.setText("Download")
        self.btn_download.setEnabled(True)
        self.btn_find_album.setEnabled(True)
        self.title.setEnabled(True)
        self.artist.setEnabled(True)
        self.album.setEnabled(True)

    def disable(self):
        self.btn_download.setDisabled(True)
        self.btn_find_album.setDisabled(True)
        self.title.setDisabled(True)
        self.artist.setDisabled(True)
        self.album.setDisabled(True)

    def fill_labels(self, song):
        self.title.setText(song.title)
        self.artist.setText(song.artist)
        self.album.setText(song.album)

    def confirm_download(self):
        self.btn_download.setText("Downloaded!")


class PandoraSong(object):
    def __init__(self, title, artist, album, time, download_url):
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.download_url = download_url
        self.temp_dl_path = None
        self.mb_album = None
        self.itunes_path = None
        self.itunes_add_path = None


class WebUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    url_received = pyqtSignal(str)

    def __init__(self, webView):
        super().__init__()

    def interceptRequest(self, info):
        if info.resourceType() == 8:  # media type
            download_url = info.requestUrl().toString()
            self.url_received.emit(download_url)
