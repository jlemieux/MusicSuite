from PyQt5.QtWidgets import QTableWidgetItem

from mutagen.mp3 import EasyMP3, HeaderNotFoundError

import os


class Library(object):
    def __init__(self, table):
        self.table = table
        self.formats = ['.mp3', '.ogg']
        self.ignore = ['Automatically Add to iTunes']

    def get_headers(self):
        self.headers = {}
        for i in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(i).text()
            self.headers[header] = i

    def get_song_length(self, mp3):
        audiofile = EasyMP3(mp3)
        return str(audiofile.info.length)

    def populate_table(self, music_path):
        self.get_headers()
        self.n_rows = 0
        self._recurse(music_path)

    def add_cell(self, text, col):
        cell = QTableWidgetItem(text, 0)
        self.table.setItem(self.n_rows, col, cell)
        return cell

    def add_row(self, path, parent):
        self.table.insertRow(self.n_rows)

        song_name = os.path.basename(path)
        song_cell = self.add_cell(song_name, self.headers["Name"])
        song_cell.setToolTip(path)

        artist_name = os.path.basename(os.path.dirname(parent))
        artist_cell = self.add_cell(artist_name, self.headers["Artist"])

        song_length = self.get_song_length(path)
        time_cell = self.add_cell(song_length, self.headers["Time"])

        album_name = os.path.basename(parent)
        album_cell = self.add_cell(album_name, self.headers["Album"])

        self.n_rows += 1

    def _recurse(self, parent_path):
        for name in os.listdir(parent_path):
            if name in self.ignore or name.startswith("._"):
                continue
            cur_path = os.path.join(parent_path, name)
            if os.path.isdir(cur_path):
                self._recurse(cur_path)
            good_format = False
            for format in self.formats:
                if name.endswith(format):
                    good_format = True
                    break
            if good_format:
                self.add_row(cur_path, parent_path)

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
