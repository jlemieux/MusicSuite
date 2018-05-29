#import os
import sys

from gui import Ui_MainWindow
from app.facade import Facade
from PyQt5.QtWidgets import QMainWindow, QApplication


#os.environ['QT_DEBUG_PLUGINS'] = "0"
#os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "8080"


class Suite(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.facade = Facade(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    suite = Suite()
    suite.show()

    sys.exit(app.exec_())
