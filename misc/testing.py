from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
import PyQt5
import sys, os

os.environ['QT_DEBUG_PLUGINS'] = "1"

pyqt = os.path.dirname(PyQt5.__file__)
QtWidgets.QApplication.addLibraryPath(os.path.join(pyqt, "mediaservice"))

app = QtGui.QGuiApplication(sys.argv)

player = QtMultimedia.QMediaPlayer()
music = os.path.join(pyqt, "mysong.mp3")
sound = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(music))
player.setMedia(sound)
player.setVolume(100)
player.play()

sys.exit(app.exec_())
