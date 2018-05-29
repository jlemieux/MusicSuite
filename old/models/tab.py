from PyQt5.QtCore import QObject


class Tab(QObject):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
