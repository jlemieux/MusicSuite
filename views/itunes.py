from models.tab import Tab
from models.library import Library
from controller.player import Player

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

from pathlib import Path
#import os


class iTunes(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.media_path = None
        self.auto_add_path = None

        self.library = Library(self.parent.library)
        self.player = Player()

        self.library.table.itemDoubleClicked.connect(self.play_song)

        self.parent.pb_dir.clicked.connect(self.set_media_path)

    def play_song(self, cell):
        self.player.play_song(self.get_clicked_song_path(cell))
        self.parent.tb_playPause.setIcon(QIcon(":/icons/pause.png"))
        try:
            self.parent.tb_playPause.clicked.disconnect()
        except TypeError:
            # No slots are connected
            pass
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
        name_cell_col = self.library.headers["Name"]
        name_cell = self.library.table.item(cell.row(), name_cell_col)
        song_path = name_cell.toolTip()
        return song_path

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
        self.media_path = Path(selected_path)
        self.auto_add_path = self.media_path / "Automatically Add to iTunes"
        music_path = self.media_path / "Music"
        if music_path.exists():
            self.library.populate_table(music_path)

