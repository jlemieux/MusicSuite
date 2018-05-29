from app.models import Library
from app.pandora.controller import Pandora
from app.youtube.controller import YouTube
from app.itunes.controller import iTunes

from PyQt5.QtCore import QObject


class Facade(QObject):
    def __init__(self, gui):
        super().__init__()

        self.gui = gui

        self.library = Library(self.gui.library)

        self.pd = Pandora(self.gui, self.library)
        self.yt = YouTube(self.gui)
        self.it = iTunes(self.gui, self.library)