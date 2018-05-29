import os
import re
from pathlib import Path

from app.pandora.models import WebUrlRequestInterceptor

from mutagen.mp3 import EasyMP3
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineProfile


class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None


class Tab(QObject):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui


class Album(object):
    def __init__(self, id, title, date, nth_track, n_tracks, art_url):
        self.id = id
        self.title = title
        self.date = date
        self.nth_track = nth_track
        self.n_tracks = n_tracks
        self.art_url = art_url

    def get_year(self):
        # date: YYYY-MM-DD
        return self.date.split('-')[0]


class Authenticator(object):
    MAX_FILENAME_LENGTH = 40
    SYMBOLS = ['.', '_', "'", '-', '&', ')', '(', '@', '#', '$', '!', '%']

    def __init__(self):
        pass

    def is_safe(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

        if not self._auth_empty():
            return False
        if not self._auth_length():
            return False
        if not self._auth_chars():
            return False

        return True

    def _auth_empty(self):
        error_title = "Empty field"
        error_text = "Field <{0}> is empty!"

        if len(''.join(self.title.split())) == 0:
            self._report_error(error_title, error_text.format('Title'))
            return False
        if len(''.join(self.artist.split())) == 0:
            self._report_error(error_title, error_text.format('Artist'))
            return False
        if len(''.join(self.album.split())) == 0:
            self._report_error(error_title, error_text.format('Album'))
            return False

        return True

    def _auth_length(self):
        error_title = "Excess length"
        error_text = "Field <{0}> is {1} characters. Max filename length " \
                     "is " + str(self.MAX_FILENAME_LENGTH) + "!"

        example_track = "01 "
        example_extension = ".mp3"
        final_title = example_track + self.title + example_extension
        title_len = len(final_title)
        artist_len = len(self.artist)
        album_len = len(self.album)

        if title_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Title', title_len))
            return False
        if artist_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Artist', artist_len))
            return False
        if album_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Album', album_len))
            return False

        return True

    def _auth_chars(self):
        error_title = "Forbidden characters"
        error_text = self._create_chars_error_text()

        pattern = self._create_regex_pattern()

        if not re.match(pattern, self.title):
            self._report_error(error_title, error_text.format('Title'))
            return False
        if not re.match(pattern, self.artist):
            self._report_error(error_title, error_text.format('Artist'))
            return False
        if not re.match(pattern, self.album):
            self._report_error(error_title, error_text.format('Album'))
            return False

        return True

    def _create_regex_pattern(self):
        pattern = r"^([^\S\n\t]|[a-zA-Z0-9"
        for symbol in self.SYMBOLS:
            pattern += "\{0}".format(symbol)
        pattern += "])+$"
        return pattern

    def _create_chars_error_text(self):
        error_text = "Field <{0}> contains forbidden characters!\n" \
             "Valid characters are:\n" \
             "\t> a-z, A-Z, 0-9\n" \
             "\t> Spaces and commas\n" \
             "\t> Additional:\n"
        for symbol in self.SYMBOLS:
            error_text += "\t\t> {0}\n".format(symbol)
        error_text = error_text[:-2]  # remove last '\n'
        return error_text

    def _report_error(self, error_title, error_text):
        msg = QMessageBox(QMessageBox.Information,
                          error_title,
                          error_text,
                          QMessageBox.Ok)
        msg.exec_()


class WebView(object):
    def __init__(self, view):
        self.view = view

        self.create_profile()
        self.set_page()
        self.set_interceptor()

        self.enable_plugins()
        self.enable_fullscreen()

    def enable_plugins(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.PluginsEnabled, True)
        self.view.settings().setAttribute(
          QWebEngineSettings.AllowRunningInsecureContent, True)

    def enable_fullscreen(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.FullScreenSupportEnabled, True)
        self.view.page().fullScreenRequested.connect(
          lambda request: request.accept())

    def create_profile(self):
        self.profile = QWebEngineProfile(self.view)

    def set_page(self):
        self.page = QWebEnginePage(self.profile, self.view)
        self.view.setPage(self.page)

    def set_interceptor(self):
        self.interceptor = WebUrlRequestInterceptor(self.view)
        self.profile.setRequestInterceptor(self.interceptor)


class LibrarySong(object):
    def __init__(self, row, title, artist, album,
                 time, n_tracks, nth_track, year, path):
        self.row = row
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.n_tracks = n_tracks
        self.nth_track = nth_track
        self.year = year
        self.path = path


class Library(object):
    def __init__(self, table):
        self.table = table
        self.music_path = None
        self.auto_add_dir = None
        self.temp_dir = None
        self.formats = ['.mp3', '.ogg']
        self.ignore = ['Automatically Add to iTunes']
        self.n_rows = 0
        self.songs = {}

    def _get_headers(self):
        self.headers = {}
        for i in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(i).text()
            self.headers[header] = i

    def populate_table(self, music_path):
        self.music_path = music_path
        self.auto_add_dir = music_path.parents[0] / Path("Automatically Add to iTunes")
        self.temp_dir = music_path.parents[0] / Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        self._get_headers()
        self._recurse(music_path)

    def _add_cell(self, text, col):
        cell = QTableWidgetItem(text, 0)
        self.table.setItem(self.n_rows, col, cell)
        return cell

    def _create_song(self, path, pandora_song):
        if pandora_song is None:
            info = self._get_info_from_metadata(path)
        else:
            info = self._get_info_from_song(pandora_song)

        return LibrarySong(self.n_rows, info['title'], info['artist'],
                           info['album'], info['time'], info['n_tracks'],
                           info['nth_track'], info['year'], info['path'])

    def _add_row(self, song):
        self.table.insertRow(self.n_rows)

        title_cell = self._add_cell(song.title, self.headers["Title"])
        title_cell.setToolTip(str(song.path))
        artist_cell = self._add_cell(song.artist, self.headers["Artist"])
        album_cell = self._add_cell(song.album, self.headers["Album"])
        time_cell = self._add_cell(song.time, self.headers["Time"])
        # album, nth_track, n_tracks, and year can also be '' here,
        # which means no info was found for that field
        if song.n_tracks == '':
            track_text = song.nth_track
        else:
            track_text = "{0} of {1}".format(song.nth_track, song.n_tracks)
        track_cell = self._add_cell(track_text, self.headers["Track"])
        year_cell = self._add_cell(song.year, self.headers["Year"])

    def add_song(self, path, pandora_song=None):
        song = self._create_song(path, pandora_song)
        self._add_row(song)
        self.songs[self.n_rows] = song
        self.n_rows += 1

    def _get_info_from_metadata(self, path):
        info = {}
        audiofile = EasyMP3(str(path))
        title = audiofile['title'][0]
        artist = audiofile['artist'][0]
        seconds = int(round(audiofile.info.length))
        minutes = seconds // 60
        remainder = seconds - (minutes * 60)
        time = "{0}:{1:0>2d}".format(minutes, remainder)
        album = ''
        n_tracks = ''
        nth_track = ''
        year = ''
        if 'album' in audiofile.keys():
            album = audiofile['album'][0]
        if 'tracknumber' in audiofile.keys():
            track = audiofile['tracknumber'][0]
            if len(track) == 2:  # e.g. 11
                nth_track = track
            elif len(track) == 5:  # e.g. 11/20
                nth_track, n_tracks = track.split('/')
        if 'date' in audiofile.keys():
            year = audiofile['date'][0]

        info['title'] = title
        info['artist'] = artist
        info['album'] = album
        info['time'] = time
        info['n_tracks'] = n_tracks
        info['nth_track'] = nth_track
        info['year'] = year
        info['path'] = path

        return info

    def _get_info_from_song(self, song):
        info = {}
        info['title'] = song.title
        info['artist'] = song.artist
        info['album'] = song.album
        info['time'] = song.time
        info['n_tracks'] = song.mb_album.n_tracks
        info['nth_track'] = song.mb_album.nth_track
        info['year'] = song.mb_album.get_year()
        info['path'] = song.itunes_path

        return info

    def song_is_unique(self, title, artist):
        for song in self.songs.values():
            #print("Comparing '{0}' to '{1}'".format(title, song.title))
            if title == song.title:
                #print("Comparing '{0}' to '{1}'".format(artist, song.artist))
                if artist == song.artist:
                    return False
        return True

    def _recurse(self, parent_path):
        for name in os.listdir(str(parent_path)):
            if name in self.ignore or name.startswith("._"):
                continue
            cur_path = parent_path / name
            if cur_path.is_dir():
                self._recurse(cur_path)
            if cur_path.suffix in self.formats:
                self.add_song(cur_path)

    '''
    Tree View functionality
    
    def update_tree(self, music_path):
        root = QTreeWidgetItem(self.tree)
        root.setText(0, os.path.basename(music_path))
        root.setToolTip(0, music_path)
        self._recurse(root, music_path)

    def _recurse(self, parent, parent_path):
        for name in os.listdir(parent_path):
            if name in self.ignore:
                continue
            cur = QTreeWidgetItem(parent)
            cur.setText(0, name)
            cur_path = os.path.join(parent_path, name)
            cur.setToolTip(0, cur_path)
            if os.path.isdir(cur_path):
                self._recurse(cur, cur_path)
        return
    '''
