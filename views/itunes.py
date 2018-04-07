from models.tab import Tab

from PyQt5.QtWidgets import QFileDialog


class iTunes(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.auto_add_dir = None
        self.parent.pb_dir.clicked.connect(self.set_auto_add_dir)
    def set_auto_add_dir(self):
        if self.auto_add_dir is None:
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            options |= QFileDialog.ReadOnly
            self.auto_add_dir = QFileDialog.getExistingDirectory(self.parent,
              'Select directory...', 'C:/', options)
        else:
            print(self.auto_add_dir)
