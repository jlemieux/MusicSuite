from models.tab import Tab
from models.pandora_song import PandoraSong
from models.webview import WebView
from models.album_api import AlbumAPI
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest as qreq
from PyQt5.QtWidgets import QMessageBox

from bs4 import BeautifulSoup
import requests
from pathlib import Path

from urllib.request import urlopen
from mutagen.id3 import ID3, TRCK, TALB, TORY, APIC
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
        self.albumAPI = AlbumAPI()
        self.webView = WebView(parent.pd_webView)
        self.webView.interceptor.subscribe(self.wait_for_DOM)
        self.current_song = None
        self.current_album = None

        self.parent.html_test.clicked.connect(self.send_req)
        self.parent.pb_download.clicked.connect(self.dl_btn_clicked)
        self.parent.pb_findAlbum.clicked.connect(self.auto_set_album_text)
    def wait_for_DOM(self, event):
        '''Delay toHtml call to allow DOM to load'''
        url = event.url
        thr = Thread(target=self.get_html, args=(url,))
        thr.start()

    def get_html(self, url):
        time.sleep(5)
        self.webView.page.toHtml(lambda html: self.create_song(html, url))

    def create_song(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        info = soup.find("div", {"class": "nowPlayingTopInfo__current"})
        title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
        artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
        album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
        r_time = soup.find("span", {"data-qa": "remaining_time"}).contents[0]
        basepath = Path(artist) / Path(album) / Path(title)
        self.current_song = PandoraSong(title, artist, album, r_time, basepath, url)
        self.preset_labels()
        self.enable_dl_panel()

    def disable_dl_panel(self):
        self.parent.pb_download.setDisabled(True)
        self.parent.lbl_title.setDisabled(True)
        self.parent.lbl_artist.setDisabled(True)
        self.parent.lbl_album.setDisabled(True)
        self.parent.pb_findAlbum.setDisabled(True)

    def enable_dl_panel(self):
        self.parent.pb_download.setText("Download")
        self.parent.pb_download.setDisabled(False)
        self.parent.lbl_title.setDisabled(False)
        self.parent.lbl_artist.setDisabled(False)
        self.parent.lbl_album.setDisabled(False)
        self.parent.pb_findAlbum.setDisabled(False)

    def preset_labels(self):
        self.parent.lbl_title.setText(self.current_song.title)
        self.parent.lbl_artist.setText(self.current_song.artist)
        self.parent.lbl_album.setText(self.current_song.album)

    def set_current_album(self):
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        self.current_album = self.albumAPI.get_album_info(title, artist)#TODO: x2 api calls

    '''
    def create_artist_album_dirs(self):
        album = self.current_song.path.parents[0]
        album.mkdir(parents=True, exist_ok=True)
    '''

    def duplicate_song_alert(self):
        msg = QMessageBox()
        msg.setText("Song already in library!")
        msg.exec_()

    def dl_btn_clicked(self):
        self.disable_dl_panel()
        thr = Thread(target=self.download_song)
        thr.start()

    def auto_set_album_text(self):
        self.disable_dl_panel()
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.albumAPI.get_album_info(title, artist) #TODO: x2 api calls
        if album is None:
            msg = QMessageBox()
            msg.setText("Could not find album information!")
            msg.exec_()
        else:
            self.parent.lbl_album.setText(album.title)
        self.enable_dl_panel()

    def download_song(self):
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.parent.lbl_album.text()

        if not self.library.song_is_unique(title, artist):
            self.duplicate_song_alert()
            self.enable_dl_panel()
            return

        self.current_song.title = title
        self.current_song.artist = artist
        self.current_song.album = album
        self.current_song.basepath = Path(artist) / Path(album) / Path(title)
        self.current_song.path = (self.library.music_path / self.current_song.basepath).with_suffix(".mp3")

        temp_path = self.library.temp_path_dir / self.current_song.path.parts[-1]
        auto_add_path = self.library.auto_add_path_dir / self.current_song.path.parts[-1]

        response = requests.get(self.current_song.url)
        if response.headers['Content-Type'] == 'audio/mp4':
            temp_path = temp_path.with_suffix(".mp4")
        with open(temp_path, "wb") as song:
            song.write(response.content)

        temp_output = self.ffmpeg(self.current_song, temp_path)
        self.add_album_info(temp_output)
        self.move_to_itunes(temp_path, temp_output, auto_add_path)
        self.library.add_downloaded_song(self.current_song)
        self.confirm_download()

    def ffmpeg(self, song, temp_path):
        convert = temp_path.suffix == ".mp4"
        output = temp_path.with_suffix(".mp3")
        if convert:
            cmd = ('ffmpeg -i "{0}" -y -acodec libmp3lame '
                   '-ab 192k -metadata title="{1}" '
                   '-metadata artist="{2}" "{3}"'
                   .format(temp_path, song.title, song.artist, output))
        else:
            cmd = ('ffmpeg -i "{0}" -y -codec copy -metadata title="{1}" '
                   '-metadata artist="{2}" "{3}"'
                   .format(temp_path, song.title, song.artist, output))
        subprocess.call(shlex.split(cmd), stdout=DEVNULL, stderr=subprocess.STDOUT)
        return output
        #os.remove(temp_path)

    def move_to_itunes(self, temp_path, temp_output, output):
        os.rename(temp_output, output)
        os.remove(temp_path)

    def update_song_name(self, track):
        new_base = Path("{0} {1}".format(track, self.current_song.path.name))
        self.current_song.basepath = self.current_song.basepath.parent / new_base
        self.current_song.path = self.current_song.path.parent / new_base
        print("Current song path: ")
        print(self.current_song.path)

    def add_album_info(self, temp_output):
        self.set_current_album()
        audio = ID3(temp_output)
        if self.current_album is not None:
            album_art = urlopen(self.current_album.art_url)
            track = "{0}/{1}".format(self.current_album.nth_track,
                                     self.current_album.n_tracks)
            self.update_song_name(self.current_album.nth_track)
            year = self.current_album.get_date_year()
            audio['TRCK'] = TRCK(encoding=3, text=track)
            audio['TORY'] = TORY(encoding=3, text=year)
            audio['APIC'] = APIC(
                              encoding=3,
                              mime='image/jpeg',
                              type=3, desc=u'Cover',
                              data=album_art.read()
                            )
            album_art.close()

        album = self.current_song.album
        audio['TALB'] = TALB(encoding=3, text=album)
        audio.save()

    def confirm_download(self):
        self.parent.pb_download.setText("Downloaded!")

    def send_req(self):
        temp = "https://www.pandora.com"
        r = qreq()
        r.setUrl(QUrl(temp))
        r.setMethod(qreq.Get)
        self.webView.view.load(r)
