from models.tab import Tab
from models.pandora_song import PandoraSong
from models.webview import WebView
from models.album_api import AlbumAPI
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
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
import re
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')
from threading import Thread

MAX_LENGTH = 40

class Pandora(Tab):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.parent = parent
        self.library = library
        self.albumAPI = AlbumAPI()
        self.webView = WebView(parent.pd_webView)
        self.webView.interceptor.subscribe(self.wait_for_DOM)
        self.current_song = None
        self.current_album = None
        self.last_event = None

        self.webView.view.loadFinished.connect(self._load_finished)
        self.parent.pb_loadPandora.clicked.connect(self.load_pandora)
        self.parent.pb_download.clicked.connect(self.dl_btn_clicked)
        self.parent.pb_findAlbum.clicked.connect(self.auto_set_album_text)

    def threaded(fn):
        def wrapper(*args, **kwargs):
            thread = Thread(target=fn, args=args, kwargs=kwargs)
            thread.start()
            return thread
        return wrapper

    def wait_for_DOM(self, event):
        '''Delay toHtml call to allow DOM to load'''
        print("setting last event now")
        self.last_event = event
        self.webView.view.loadFinished.emit(True)
        #self.webView.page.toHtml(self._get_html)

    def _load_finished(self, result):
        print("_load_finished: checking last event none")
        self.webView.page.toHtml(self._get_html)

    def _get_html(self, html):
        print("in _get_html")
        soup = BeautifulSoup(html, "html.parser")
        try:
            title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
            artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
            album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
            r_time = soup.find("span", {"data-qa": "remaining_time"}).contents[0]
        except AttributeError:
            print("excepting attrerr")
            self.wait_for_nowPlaying_page()
            return
        self.create_song(title, artist, album, r_time)

    @threaded
    def wait_for_nowPlaying_page(self):
        time.sleep(1)
        print("emitting sig")
        self.webView.view.loadFinished.emit(True)

    def create_song(self, title, artist, album, r_time):
        basepath = Path(artist) / Path(album) / Path(title)
        self.current_song = PandoraSong(title, artist, album, r_time, basepath, self.last_event.url)
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
        text = "Song already in library!"
        msg = QMessageBox(QMessageBox.Information, "Duplicate song error", text, QMessageBox.Ok)
        msg.exec_()

    def too_long_alert(self, info):
        text = "'{0}' is '{1}' characters - 40 character max!".format(info, len(info))
        msg = QMessageBox(QMessageBox.Information, "Too long error", text, QMessageBox.Ok)
        msg.exec_()

    def too_short_alert(self, info):
        text = "Cannot leave {0} empty!".format(info)
        msg = QMessageBox(QMessageBox.Information, "Too short error", text, QMessageBox.Ok)
        msg.exec_()

    def forbidden_character(self, info):
        text = ("{0} contains forbidden characters!\nValid characters " +
                "are:\n\t- Any letter or number\n\t- Underscores, periods, " +
                "dashes\n\t- Spaces").format(info)
        msg = QMessageBox(QMessageBox.Information, "Forbidden character error", text, QMessageBox.Ok)
        msg.exec_()

    def safe_filenames(self, title, artist, album):
        title_total = "01 " + title + ".mp3"
        title_len = len(title_total)
        artist_len = len(artist)
        album_len  = len(album)
        print("about to do max lens")
        if title_len > MAX_LENGTH:
        
            self.too_long_alert('Title')
            
            return False
        if artist_len > MAX_LENGTH:
            self.too_long_alert('Artist')
            return False
        if album_len> MAX_LENGTH:
            self.too_long_alert('Album')
            return False
            
        print("about to do zeroes")
        
        if title_len <= 0:
            self.too_short_alert('Title')
            return False
        if artist_len <= 0:
            self.too_short_alert('Artist')
            return False
        if album_len <= 0:
            self.too_short_alert('Album')
            return False
            
        print("about to do patterns")
        
        pattern = r"^([a-zA-Z0-9_\.'\-\&\(\)]|[^\S\n\t])+$"
        print("title pattern")
        if not re.match(pattern, title):
            print("not match")
            self.forbidden_character('Title')
            return False
        print("artist pattern")
        if not re.match(pattern, artist):
            print("not match")
            self.forbidden_character('Artist')
            return False
        print("album pattern")
        if not re.match(pattern, album):
            print("not match")
            self.forbidden_character('Album')
            return False
        
        print("returning True")
        
        return True

    def dl_btn_clicked(self):
        print("clicked")
        self.disable_dl_panel()
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.parent.lbl_album.text()

        print("about to do safe_filenames(title, artist, album)")
        if not self.safe_filenames(title, artist, album):
            self.enable_dl_panel()
            return

        print("entering song_is_unique(title,artist)")
        if not self.library.song_is_unique(title, artist):
            print("inside if not condition, about to alert")
            self.duplicate_song_alert()
            print("done alert, enabling panel")
            self.enable_dl_panel()
            return

        thr = Thread(target=self.download_song)
        #thr = DownloadThread()
        #thr.run(self, self.download_song)
        print("starting thread")
        thr.start()
        print("after thread start")

    def auto_set_album_text(self):
        self.disable_dl_panel()
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.albumAPI.get_album_info(title, artist) #TODO: x2 api calls
        if album is None:
            text = "Could not find album information!"
            msg = QMessageBox(QMessageBox.Information, "Missing album error", text, QMessageBox.Ok)
            msg.exec_()
        else:
            self.parent.lbl_album.setText(album.title)
        self.enable_dl_panel()

    def download_song(self):
        print("entering download_song(self)")
        title = self.parent.lbl_title.text()
        artist = self.parent.lbl_artist.text()
        album = self.parent.lbl_album.text()

        #print("about to do safe_filenames(title, artist, album)")
        #if not self.safe_filenames(title, artist, album):
        #    print("returning....")
        #    return
        '''
        print("entering song_is_unique(title,artist)")
        if not self.library.song_is_unique(title, artist):
            print("inside if not condition, about to alert")
            self.duplicate_song_alert()
            print("done alert, enabling panel")
            self.enable_dl_panel()
            return
        '''

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
            audio['TYER'] = TYER(encoding=3, text=year)
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

    def load_pandora(self):
        temp = "https://www.pandora.com"
        r = qreq()
        r.setUrl(QUrl(temp))
        r.setMethod(qreq.Get)
        self.webView.view.load(r)


class DownloadThread(QThread):
    def __init__(self):
        super().__init__(self)

    def run(self, cls, fn):
        cls.fn()