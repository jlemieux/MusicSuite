from models.tab import Tab
from models.pandora_song import PandoraSong
from models.webview import WebView
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest as qreq
from PyQt5.QtWidgets import QMessageBox

from bs4 import BeautifulSoup
import requests
from pathlib import Path

import sys
import os
import time
import subprocess
import shlex
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')
from threading import Thread


class Pandora(Tab):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.library = library
        self.webView = WebView(parent.pd_webView)
        self.webView.interceptor.subscribe(self.wait_for_DOM)
        self.current_song = None

        self.parent.html_test.clicked.connect(self.send_req)
        self.parent.pb_download.clicked.connect(self.download_song)
    def wait_for_DOM(self, event):
        '''Delay toHtml call to allow DOM to load'''
        url = event.url
        thr = Thread(target=self.get_html, args=(url,))
        thr.start()

    def get_html(self, url):
        time.sleep(2)
        self.webView.page.toHtml(lambda html: self.create_song(html, url))

    def create_song(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
        artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
        album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
        time = soup.find("span", {"data-qa": "remaining_time"}).contents[0]
        basepath = Path(artist) / Path(album) / Path(title)
        self.current_song = PandoraSong(title, artist, album, time, basepath, url)
        self.preset_labels()
        self.enable_dl_panel()

    def disable_dl_panel(self):
        self.parent.pb_download.setDisabled(True)
        self.parent.lbl_title.setDisabled(True)
        self.parent.lbl_artist.setDisabled(True)
        self.parent.lbl_album.setDisabled(True)

    def enable_dl_panel(self):
        self.parent.pb_download.setText("Download")
        self.parent.pb_download.setDisabled(False)
        self.parent.lbl_title.setDisabled(False)
        self.parent.lbl_artist.setDisabled(False)
        self.parent.lbl_album.setDisabled(False)

    def preset_labels(self):
        self.parent.lbl_title.setText(self.current_song.title)
        self.parent.lbl_artist.setText(self.current_song.artist)
        self.parent.lbl_album.setText(self.current_song.album)

    def create_artist_album_dirs(self):
        album = self.current_song.path.parents[0]
        album.mkdir(parents=True, exist_ok=True)

    def download_song(self):
        self.disable_dl_panel()

        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.parent.lbl_album.text()

        if not self.library.song_is_unique(title, artist):
            msg = QMessageBox()
            msg.setText("Song already in library!")
            msg.exec_()
            self.enable_dl_panel()
            return

        self.current_song.title = title
        self.current_song.artist = artist
        self.current_song.album = album
        self.current_song.basepath = Path(artist) / Path(album) / Path(title)
        self.current_song.path = (self.library.music_path / self.current_song.basepath).with_suffix(".mp3")

        self.create_artist_album_dirs()

        response = requests.get(self.current_song.url)
        if response.headers['Content-Type'] == 'audio/mp4':
            self.current_song.path = self.current_song.path.with_suffix(".mp4")
        with open(self.current_song.path, "wb") as song:
            song.write(response.content)

        self.ffmpeg(self.current_song)

        self.library.add_downloaded_song(self.current_song)
        self.confirm_download()

    def ffmpeg(self, song):
        convert = song.path.suffix == ".mp4"
        if convert:
            output = song.path.with_suffix(".mp3")
            cmd = ('ffmpeg -i "{0}" -y -acodec libmp3lame '
                   '-ab 192k -metadata title="{1}" '
                   '-metadata artist="{2}" -metadata album="{3}" "{4}"'
                   .format(song.path, song.title, song.artist, song.album, output))
        else:
            cmd = ('ffmpeg -i "{0}" -y -codec copy -metadata title="{1}" '
                   '-metadata artist="{2}" -metadata album="{3}" "{4}"'
                   .format(song.path, song.title, song.artist, song.album, song.path))
        subprocess.call(shlex.split(cmd), stdout=DEVNULL, stderr=subprocess.STDOUT)
        if convert:
            os.remove(song.path)
            song.path = song.path.with_suffix(".mp3")
        #time.sleep(5)  # allow song to copy to folder
        #os.remove(self.name)  # remove original file

    def confirm_download(self):
        self.parent.pb_download.setText("Downloaded!")

    def send_req(self):
        temp = "https://www.pandora.com"
        r = qreq()
        r.setUrl(QUrl(temp))
        r.setMethod(qreq.Get)
        self.webView.view.load(r)
