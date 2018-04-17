from pygame import mixer

import os


class Player(object):
    def __init__(self):
        mixer.init()

    def play_song(self, song):
        mixer.music.load(song)
        mixer.music.play()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()
