from PyQt5.QtWidgets import QTableWidgetItem
from models.itunes_song import iTunesSong

from mutagen.mp3 import EasyMP3, HeaderNotFoundError
from mutagen import MutagenError

from pathlib import Path
import os
import time


class Library(object):
    def __init__(self, table):
        self.table = table
        self.music_path = None
        self.auto_add_path_dir = None
        self.temp_path_dir = None
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
        self.auto_add_path_dir = music_path.parents[0] / Path("Automatically Add to iTunes")
        self.temp_path_dir = music_path.parents[0] / Path("temp")
        self.temp_path_dir.mkdir(exist_ok=True)
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

        return iTunesSong(self.n_rows, info['title'], info['artist'],
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
        track_cell = self._add_cell(track_text, self.header["Track"])
        year_cell = self._add_cell(song.year, self.header["Year"])

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
