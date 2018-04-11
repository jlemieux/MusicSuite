from models.tab import Tab
from models.library import Library
from controller.player import Player

from PyQt5.QtWidgets import QFileDialog

import os


class iTunes(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.media_path = None
        self.auto_add_path = None

        self.library = Library(self.parent.library)
        self.player = Player()

        self.library.table.itemDoubleClicked.connect(self.play_song)
        self.parent.pb_dir.clicked.connect(self.set_media_path)

    def play_song(self, cell):
        self.player.play_song(self.get_clicked_song_name(cell))

    def get_clicked_song_name(self, cell):
        name_cell_col = self.library.headers["Name"]
        name_cell = self.library.table.item(cell.row(), name_cell_col)
        song_name = name_cell.toolTip()
        return song_name

    def set_media_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.ReadOnly
        fp = "F:/Users/JimmyGtr11/Music/iTunes" # change back to C:/
        self.media_path = QFileDialog.getExistingDirectory(self.parent,
          'Select directory...', fp, options)
        if self.media_path is None:
            return
        print(self.media_path)
        self.auto_add_path = os.path.join(self.media_path,
          "Automatically Add to iTunes")
        music_path = os.path.join(self.media_path, "Music")
        if os.path.exists(music_path):
            self.library.populate_table(music_path)

