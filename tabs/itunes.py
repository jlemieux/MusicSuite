from PyQt5.QtWidgets import *


class iTunes(object):
    def __init__(self):
        pass
    def set_auto_add_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.ReadOnly
        self.dir = QFileDialog.getExistingDirectory(self,
          'Select directory...', 'C:/', options)
        print(self.dir)