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
        self.songs = {}

    def get_headers(self):
        self.headers = {}
        for i in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(i).text()
            self.headers[header] = i

    def get_song_length(self, mp3):
        print("getting {0} length...".format(mp3.parts[-1]))
        try:
            audiofile = EasyMP3(str(mp3))
        except MutagenError:
            for _ in range(5):
                time.sleep(1)
                if mp3.is_file():
                    audiofile = EasyMP3(str(mp3))
                    break
            else:
                raise OSError(2, 'No such file or directory', str(mp3))

        seconds = int(round(audiofile.info.length))
        minutes = seconds // 60
        remainder = seconds - (minutes * 60)
        formatted = "{0}:{1:0>2d}".format(minutes, remainder)
        return formatted

    def populate_table(self, music_path):
        self.music_path = music_path
        self.auto_add_path_dir = music_path.parents[0] / Path("Automatically Add to iTunes")
        self.temp_path_dir = music_path.parents[0] / Path("temp")
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
        song_title = song_path.parts[-1]
        song_cell = self.add_cell(song_title, self.headers["Title"])
        song_cell.setToolTip(str(song_path))

        #artist_name = os.path.basename(os.path.dirname(parent))
        artist_name = song_path.parts[-3]
        artist_cell = self.add_cell(artist_name, self.headers["Artist"])

        song_length = self.get_song_length(song_path)
        time_cell = self.add_cell(song_length, self.headers["Time"])

        album_name = song_path.parts[-2]
        album_cell = self.add_cell(album_name, self.headers["Album"])

    def add_library_song(self):
        song = iTunesSong(self.n_rows)
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            cell = self.table.item(self.n_rows, col)
            if header == "Title":  # TODO: store `path` in separate column
                setattr(song, "path", cell.toolTip())
            setattr(song, header.lower(), cell.text())
        self.songs[self.n_rows] = song

    def song_is_unique(self, title, artist):
        for song in self.songs.values():
            #print("Comparing '{0}' to '{1}'".format(title, song.title))
            compare = ''.join(song.title.split()[1:-4])
            if title == compare:
                #print("Comparing '{0}' to '{1}'".format(artist, song.artist))
                if artist == song.artist:
                    return False
        return True

    def add_downloaded_song(self, pandora_song):
        self.add_row(pandora_song.path)
        itunes_song = iTunesSong(self.n_rows)
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text()
            attr = getattr(pandora_song, header.lower())
            setattr(itunes_song, header.lower(), attr)
        setattr(itunes_song, "path", pandora_song.path)
        self.songs[self.n_rows] = itunes_song
        self.n_rows += 1

    def _recurse(self, parent_path):
        for name in os.listdir(str(parent_path)):
            if name in self.ignore or name.startswith("._"):
                continue
            cur_path = parent_path / name
            if cur_path.is_dir():
                self._recurse(cur_path)
            if cur_path.suffix in self.formats:
                self.add_row(cur_path)
                self.add_library_song()
                self.n_rows += 1

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
