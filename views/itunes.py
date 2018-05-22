from models.tab import Tab
from controller.player import Player

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

from pathlib import Path
#import os
import random

class iTunes(Tab):
    def __init__(self, parent, library):
        super().__init__(parent)
        self.parent = parent
        self.music_path = None
        self.current_song = None

        #self.library = Library(self.parent.library)
        self.library = library
        self.player = Player()

        self.library.table.itemDoubleClicked.connect(self.play_song)
        self.parent.tb_playPause.clicked.connect(self.play_song)
        self.parent.pb_dir.clicked.connect(self.set_media_path)

    def play_song(self, cell=None):
        if cell is None:
            song = self.get_random_song_path()
        else:
            song = self.get_clicked_song_path(cell)
        self.player.play_song(song)
        self.parent.tb_playPause.setIcon(QIcon(":/icons/pause.png"))
        self.parent.tb_playPause.clicked.disconnect()
        self.parent.tb_playPause.clicked.connect(self.pause_song)

    def unpause_song(self):
        self.player.unpause_song()
        self.parent.tb_playPause.setIcon(QIcon(":/icons/pause.png"))
        self.parent.tb_playPause.clicked.disconnect(self.unpause_song)
        self.parent.tb_playPause.clicked.connect(self.pause_song)

    def pause_song(self):
        self.player.pause_song()
        self.parent.tb_playPause.setIcon(QIcon(":/icons/play.png"))
        self.parent.tb_playPause.clicked.disconnect(self.pause_song)
        self.parent.tb_playPause.clicked.connect(self.unpause_song)

    def get_clicked_song_path(self, cell):
        song = self.library.songs[cell.row()]
        return song.path
        '''
        name_cell_col = self.library.headers["Name"]
        name_cell = self.library.table.item(cell.row(), name_cell_col)
        song_path = name_cell.toolTip()
        return song_path
        '''

    def get_random_song(self):
        numRows = self.library.table.rowCount()
        random_row = random.randint(0, numRows-1)
        random_song = self.library.songs[random_row]
        while random_song is self.current_song:
            random_song = self.library.songs[random_row]
        return random_song.path
        '''
        numRows = self.library.table.rowCount()
        name_cell_col = self.library.headers["Name"]
        random_row = random.randint(0, numRows-1)
        if self.current_song_row is not None:
            while random_row == self.current_song_row:
                random_row = random.randint(0, numRows-1)
        name_cell = self.library.table.item(random_row, name_cell_col)
        song_path = name_cell.toolTip()
        return song_path
        '''

    def set_media_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.ReadOnly
        #opening_path = os.path.abspath(os.sep)  # cross platform safe
        opening_path = "F:\\Users\\JimmyGtr11\\Music\\iTunes"
        selected_path = QFileDialog.getExistingDirectory(self.parent,
          'Select directory...', opening_path, options)
        if selected_path is None:
            return
        self.music_path = Path(selected_path) / "Music"
        if self.music_path.exists():
            self.library.populate_table(self.music_path)

