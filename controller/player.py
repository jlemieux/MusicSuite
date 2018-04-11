from pygame import mixer

import os


class Player(object):
    def __init__(self):
        mixer.init()

    def play_song(self, song):
        if song.endswith('.mp3') or song.endswith('.ogg'):
            mixer.music.load(song)
            mixer.music.play()
        elif os.path.isfile(song):
            print("Playback only supports .mp3 and .ogg audio files!")
