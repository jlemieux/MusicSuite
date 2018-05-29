from pygame import mixer


class iTunesControlPanel(object):
    def __init__(self, gui):
        self.gui = gui
        self.btn_play_pause = self.gui.tb_playPause
        self.btn_set_dir = self.gui.pb_dir

    def enable(self):
        self.btn_play_pause.setEnabled(True)
        self.btn_set_dir.setEnabled(True)

    def disable(self):
        self.btn_play_pause.setDisabled(True)
        self.btn_set_dir.setDisabled(True)


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
