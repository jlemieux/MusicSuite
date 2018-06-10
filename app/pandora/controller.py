import os
from pathlib import Path
from functools import partial
from urllib.request import urlopen

from app.workers import MBAlbumAPI
from app.models import Authenticator, WebView, Tab
from app.pandora.models import PandoraDownloadPanel, PandoraSong
from app.pandora.workers import PandoraSongFactory, Downloader, AudioConverter

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QUrl, QThread, pyqtSlot
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from mutagen.id3 import ID3, TRCK, TYER, APIC, TIT2, TPE1, TALB

class Pandora(Tab):
    def __init__(self, gui, library):
        super().__init__(gui)
        self.threads = {}

        self.library = library
        self.webView = WebView(self.gui.pd_webView)
        self.dl_panel = PandoraDownloadPanel(self.gui)
        self.auth = Authenticator()

        # Workers
        self.pdsf = PandoraSongFactory(self.webView.page)
        self.downloader = Downloader()
        self.converter = AudioConverter()
        self.album_api = MBAlbumAPI()

        self._setup_nonworker_signals()

    def _report_error(self, error_title, error_text, block=True):
        msg = QMessageBox(QMessageBox.Information,
                          error_title,
                          error_text,
                          QMessageBox.Ok)
        if block:
            msg.exec_()
        else:
            msg.show()
            msg.raise_()
            msg.activateWindow()

    def _duplicate_song_error(self):
        error_title = "Duplicate song"
        error_text = "Song already in library!"
        self._report_error(error_title, error_text)

    def _setup_nonworker_signals(self):
        #Load Pandora
        self.gui.pb_loadPandora.clicked.connect(self._load_pandora)

        #WebView.WebUrlRequestInterceptor
        self.webView.interceptor.url_received.connect(self._receieve_url)

        #PandoraDownloadPanel
        self.dl_panel.btn_download.clicked.connect(self._pb_download_clicked)
        self.dl_panel.btn_find_album.clicked.connect(self._pb_find_album_clicked)

    def _threaded_call(self, worker, fn, *args, signals=None, slots=None):
        thread = QThread()
        thread.setObjectName('thread_' + worker.__class__.__name__)

        # store because garbage collection
        self.threads[worker] = thread

        # give worker thread so it can be quit()
        worker.thread = thread

        # objects stay on threads after thread.quit()
        # need to move back to main thread to recycle the same Worker.
        # Error is thrown about Worker having thread (0x0) if you don't do this
        worker.moveToThread(QThread.currentThread())

        # move to newly created thread
        worker.moveToThread(thread)

        # Can now apply cross-thread signals/slots

        #worker.signals.connect(self.slots)
        if signals:
            for signal, slot in signals.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)

        #self.signals.connect(worker.slots)
        if slots:
            for slot, signal in slots.items():
                try:
                    signal.disconnect()
                except TypeError:  # Signal has no slots to disconnect
                    pass
                signal.connect(slot)

        thread.started.connect(partial(fn, *args)) # fn needs to be slot
        thread.start()

    @pyqtSlot(str)
    def _receieve_url(self, download_url):
        signals = {self.pdsf.song_created: self._receieve_song}
        self._threaded_call(self.pdsf, self.pdsf.create_song, download_url,
                            signals=signals)

    @pyqtSlot(PandoraSong)
    def _receieve_song(self, song):
        self.current_song = song
        self.dl_panel.fill_labels(self.current_song)
        self.dl_panel.enable()

    @pyqtSlot()
    def _pb_download_clicked(self):
        self.dl_panel.disable()
        title = self.dl_panel.title.text()
        artist = self.dl_panel.artist.text()
        album = self.dl_panel.album.text()

        if not self.auth.is_safe(title, artist, album):
            self.dl_panel.enable()
            return

        if not self.library.song_is_unique(title, artist):
            self._duplicate_song_error()
            self.dl_panel.enable()
            return

        self._start_download()

    def _start_download(self):
        self._update_song_info()
        signals = {self.downloader.song_downloaded: self._download_finished}
        self._threaded_call(self.downloader, self.downloader.download,
                            self.current_song, signals=signals)

    @pyqtSlot()
    def _download_finished(self):
        convert = self.current_song.temp_dl_path.suffix == ".mp4"
        if convert:
            signals = {self.converter.song_converted: self._conversion_finished}
            self._threaded_call(self.converter, self.converter.convert,
                                self.current_song, signals=signals)
        else:
            self._conversion_finished()

    @pyqtSlot()
    def _conversion_finished(self):
        signals = {self.album_api.album_created: self._set_song_itunes_paths}
        self._threaded_call(self.album_api, self.album_api.set_mb_album,
                            self.current_song, signals=signals)

    @pyqtSlot(bool)
    def _set_song_itunes_paths(self, album_exists):
        title = self.current_song.title
        artist = self.current_song.artist
        album = self.current_song.album

        temp_name = self.current_song.temp_dl_path.parts[-1]
        self.current_song.itunes_add_path = (self.library.auto_add_dir /
                                             temp_name)
        if album_exists:
            track = self.current_song.mb_album.nth_track
            final_name = "{0} {1}".format(track, temp_name)
        else:
            self._missing_album_error()
            final_name = temp_name

        base = Path(artist) / Path(album) / Path(final_name)
        self.current_song.itunes_path = self.library.music_path / base

        self._set_metadata(album_exists)

    def _set_metadata(self, album_exists):
        audio = ID3(self.current_song.temp_dl_path)
        if album_exists:
            track = "{0}/{1}".format(self.current_song.mb_album.nth_track,
                                     self.current_song.mb_album.n_tracks)
            year = self.current_song.mb_album.get_year()
            audio['TRCK'] = TRCK(encoding=3, text=track)
            audio['TYER'] = TYER(encoding=3, text=year)
            art_url = self.current_song.mb_album.art_url
            if art_url is not None:
                album_art_stream = urlopen(art_url)
                audio['APIC'] = APIC(
                                  encoding=3,
                                  mime='image/jpeg',
                                  type=3, desc=u'Cover',
                                  data=album_art_stream.read()
                                )
                album_art_stream.close()

        audio['TIT2'] = TIT2(encoding=3, text=self.current_song.title)
        audio['TPE1'] = TPE1(encoding=3, text=self.current_song.artist)
        audio['TALB'] = TALB(encoding=3, text=self.current_song.album)
        audio.save()

        self._move_to_itunes()

    def _move_to_itunes(self):
        os.rename(self.current_song.temp_dl_path,
                  self.current_song.itunes_add_path)
        self.library.add_song(self.current_song.itunes_path,
                              pandora_song=self.current_song)
        self.dl_panel.confirm_download()

    def _update_song_info(self):
        '''current_song.title, artist, and album are always
           going to be whatever was set in the labels by
           the user. Paths may change due to album availability,
           but these are permanently set from the start.'''
        self.current_song.title = self.dl_panel.title.text()
        self.current_song.artist = self.dl_panel.artist.text()
        self.current_song.album = self.dl_panel.album.text()
        base = Path(self.current_song.title).with_suffix(".mp3")
        self.current_song.temp_dl_path = self.library.temp_dir / base

    @pyqtSlot()
    def _pb_find_album_clicked(self):
        self.dl_panel.disable()
        self.current_song.title = self.dl_panel.title.text()
        self.current_song.artist = self.dl_panel.artist.text()
        signals = {self.album_api.album_created: self._auto_set_album_text}
        self._threaded_call(self.album_api, self.album_api.set_mb_album,
                            self.current_song, signals=signals)

    @pyqtSlot(bool)
    def _auto_set_album_text(self, album_exists=False):
        if album_exists:
            self.dl_panel.album.setText(self.current_song.mb_album.title)
        else:
            self._missing_album_error()
        self.dl_panel.enable()

    def _missing_album_error(self):
        error_title = "Could not find album data"
        error_text = ("Could not find automatic online album metadata "
                      "for <'{0}' by '{1}'>!".format(self.current_song.title,
                      self.current_song.artist))
        self._report_error(error_title, error_text, block=False)

    @pyqtSlot()
    def _load_pandora(self):
        url = "https://www.pandora.com"
        r = QWebEngineHttpRequest()
        r.setUrl(QUrl(url))
        r.setMethod(QWebEngineHttpRequest.Get)
        self.webView.view.load(r)
