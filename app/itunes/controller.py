#import os
import random
from pathlib import Path

from app.models import Tab
from app.itunes.models import iTunesControlPanel, Player

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem


class iTunes(Tab):
    def __init__(self, gui, library):
        super().__init__(gui)

        self.library = library
        self.music_path = None
        self.last_song_played = None

        self.control_panel = iTunesControlPanel(self.gui)
        self.player = Player()

        self._setup_nonworker_signals()

    def _setup_nonworker_signals(self):
        #Library
        self.library.table.itemDoubleClicked.connect(self._cell_double_clicked)

        #iTunesControlPanel
        self.control_panel.btn_play_pause.clicked.connect(self._first_random_play)
        self.control_panel.btn_set_dir.clicked.connect(self.set_media_path)

    @pyqtSlot(bool)
    def _first_random_play(self):
        song = self._get_random_song()
        self.play_song(song)

    @pyqtSlot(QTableWidgetItem)
    def _cell_double_clicked(self, cell):
        song = self._get_clicked_song(cell)
        self.play_song(song)

    def play_song(self, song):
        self.last_song_played = song
        self.player.play_song(song.path)
        self.control_panel.btn_play_pause.setIcon(QIcon(":/icons/pause.png"))
        self.control_panel.btn_play_pause.clicked.disconnect()
        self.control_panel.btn_play_pause.clicked.connect(self.pause_song)

    @pyqtSlot(bool)
    def unpause_song(self):
        self.player.unpause_song()
        self.control_panel.btn_play_pause.setIcon(QIcon(":/icons/pause.png"))
        self.control_panel.btn_play_pause.clicked.disconnect(self.unpause_song)
        self.control_panel.btn_play_pause.clicked.connect(self.pause_song)

    @pyqtSlot(bool)
    def pause_song(self):
        self.player.pause_song()
        self.control_panel.btn_play_pause.setIcon(QIcon(":/icons/play.png"))
        self.control_panel.btn_play_pause.clicked.disconnect(self.pause_song)
        self.control_panel.btn_play_pause.clicked.connect(self.unpause_song)

    def _get_clicked_song(self, cell):
        print("Clicked row: {0}".format(cell.row()))
        song = self.library.songs[cell.row()]
        return song

    def get_random_song(self):
        numRows = self.library.table.rowCount()
        random_row = random.randint(0, numRows-1)
        random_song = self.library.songs[random_row]
        while random_song is self.last_song_played:
            random_row = random.randint(0, numRows-1)
            random_song = self.library.songs[random_row]
        return random_song

    @pyqtSlot(bool)
    def set_media_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.ReadOnly
        #opening_path = os.path.abspath(os.sep)  # cross platform safe
        opening_path = "F:\\Users\\JimmyGtr11\\Music\\iTunes"
        selected_path = QFileDialog.getExistingDirectory(self.gui,
          'Select directory...', opening_path, options)
        if selected_path is None:
            return
        self.music_path = Path(selected_path) / "Music"
        if self.music_path.exists():
            temp_dir = Path(selected_path) / "temp"
            temp_dir.mkdir(exist_ok=True)
            self.library.populate_table(self.music_path)
