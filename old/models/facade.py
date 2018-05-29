import time
import sys

from views.youtube import YouTube
from views.pandora import Pandora
from views.itunes import iTunes
from models.library import Library

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget


class Facade(QObject):
    def __init__(self, gui):
        super().__init__()

        self.gui = gui

        self.library = Library(self.gui.library)

        self.pd = Pandora(self.gui, self.library)
        self.yt = YouTube(self.gui)
        self.it = iTunes(self.gui, self.library)
