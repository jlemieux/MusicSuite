from PyQt5.QtWidgets import QTableWidgetItem
from itunes_song import iTunesSong

from mutagen.mp3 import EasyMP3, HeaderNotFoundError

from pathlib import Path
import os


class Library(object):
    def __init__(self, table):
        self.table = table
        self.formats = ['.mp3', '.ogg']
        self.ignore = ['Automatically Add to iTunes']
        self.songs = {}

    def get_headers(self):
        self.headers = {}
        for i in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(i).text()
            self.headers[header] = i

    def get_song_length(self, mp3):
        audiofile = EasyMP3(mp3)
        seconds = int(round(audiofile.info.length))
        minutes = seconds // 60
        remainder = seconds - (minutes * 60)
        formatted = "{0}:{1:0>2d}".format(minutes, remainder)
        return formatted

    def populate_table(self, music_path):
        self.get_headers()
        self.n_rows = 0
        self._recurse(music_path)

    def add_cell(self, text, col):
        cell = QTableWidgetItem(text, 0)
        self.table.setItem(self.n_rows, col, cell)
        return cell

    def add_row(self, song_path):
        '''
        Path("/Music/Artist/Album/song.mp3").parts = 
        ("Music", "Artist", "Album", "song.mp3")
        '''

        self.table.insertRow(self.n_rows)

        #song_name = os.path.basename(path)
        song_name = song_path.parts[-1]
        song_cell = self.add_cell(song_name, self.headers["Name"])
        song_cell.setToolTip(str(song_path))

        #artist_name = os.path.basename(os.path.dirname(parent))
        artist_name = song_path.parts[-3]
        artist_cell = self.add_cell(artist_name, self.headers["Artist"])

        song_length = self.get_song_length(str(song_path))
        time_cell = self.add_cell(song_length, self.headers["Time"])

        album_name = song_path.parts[-2]
        album_cell = self.add_cell(album_name, self.headers["Album"])

        self.add_song(self.n_rows)

        self.n_rows += 1

    def add_song(self, row):
        song = iTunesSong(row)
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            cell = self.table.item(row, col)
            if header == "Name":  # TODO: store path in separate column
                setattr(song, "path", cell.toolTip())
            setattr(song, header.lower(), cell.text())
        self.songs[row] = song

    def _recurse(self, parent_path):
        for name in os.listdir(str(parent_path)):
            if name in self.ignore or name.startswith("._"):
                continue
            cur_path = parent_path / name
            if cur_path.is_dir():
                self._recurse(cur_path)
            if cur_path.suffix in self.formats:
                self.add_row(cur_path)

    '''
    def edit_metadata(self, mp3):
        audiofile = eyed3.load(mp3)
        audiofile.tag.artist = u"{0}".format(os.path.basename(
          os.path.dirname(parent))
        audiofile.tag.album = u"{0}".format(os.path.basename(parent))
        audiofile.tag.album_artist = u"Integrity"
        audiofile.tag.title = u"Hollow"
        audiofile.tag.track_num = 2

        audiofile.tag.save()
    '''

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
