import os
import time
import shlex
import subprocess
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

from app.models import Worker
from app.pandora.models import PandoraSong

import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class PandoraSongFactory(Worker):
    song_created = pyqtSignal(PandoraSong)
    song_missing = pyqtSignal(str)

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.song_missing.connect(self._post_html)

    @pyqtSlot(str)
    def create_song(self, download_url):
        self._post_html(download_url)

    @pyqtSlot(str)
    def _post_html(self, download_url):
        print("Trying to create song...")
        self.page.toHtml(lambda html: self._create_song(html, download_url))

    def _create_song(self, html, download_url):
        soup = BeautifulSoup(html, "html.parser")
        try:
            title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
            artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
            album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
            time_ = soup.find("span", {"data-qa": "remaining_time"}).contents[0]
        except AttributeError:
            print("Could not find song info on current screen.")
            time.sleep(1)
            self.song_missing.emit(download_url)
        else:
            print("Song created.")
            song = PandoraSong(title, artist, album, time_, download_url)
            self.song_created.emit(song)
            self.thread.quit()


class Downloader(Worker):
    song_downloaded = pyqtSignal()
    def __init__(self):
        super().__init__()

    @pyqtSlot(PandoraSong)
    def download(self, song):
        response = requests.get(song.download_url)
        self._check_audio_format(song, response)

        with open(song.temp_dl_path, "wb") as downloaded_song:
            downloaded_song.write(response.content)
        self.song_downloaded.emit()
        self.thread.quit()

    def _check_audio_format(self, song, response):
        if response.headers['Content-Type'] == 'audio/mp4':
            song.temp_dl_path = song.temp_dl_path.with_suffix(".mp4")


class AudioConverter(Worker):
    song_converted = pyqtSignal()
    def __init__(self):
        super().__init__()

    @pyqtSlot(PandoraSong)
    def convert(self, song):
        output = song.temp_dl_path.with_suffix(".mp3")
        cmd = ('ffmpeg -i "{0}" -y -acodec libmp3lame -ab 192k "{1}"'
               .format(song.temp_dl_path, output))
        subprocess.call(shlex.split(cmd), stdout=DEVNULL, stderr=subprocess.STDOUT)
        os.remove(song.temp_dl_path)
        song.temp_dl_path = output
        self.song_converted.emit()
        self.thread.quit()
