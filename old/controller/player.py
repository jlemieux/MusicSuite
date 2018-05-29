from pygame import mixer

import os


class Player(object):
    def __init__(self):
        mixer.init()

    def play_song(self, path):
        mixer.music.load(str(path))
        mixer.music.play()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

#self.player = QtMultimedia.QMediaPlayer(self)
#url = QUrl.fromLocalFile("F:\\Users\\JimmyGtr11\\Music\\iTunes\\iTunes Media\\Music\\Smash Mouth\\Unknown Album\\All Star.mp3")
#self.player.setMedia(QtMultimedia.QMediaContent(url))
#self.player.setVolume(50)