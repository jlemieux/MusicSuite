from PyQt5.QtWidgets import QTableWidgetItem

from mutagen.mp3 import EasyMP3, HeaderNotFoundError

from pathlib import Path
import os


class Song(object):
    def __init__(self, library, row):
        self.library = library
        self.row = row
        self.get_info()

    def get_info(self):
        self.info = {}
        for col in range(self.library.columnCount()):
            header = self.library.table.horizontalHeaderItem(col).text()
            cell = self.library.table.item(self.row, col)
            if header == "Name":  # TODO: store path in separate column
                self.info["Path"] = cell.toolTip()
            self.info[header] = cell.text()
