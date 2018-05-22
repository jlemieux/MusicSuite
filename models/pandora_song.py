

class PandoraSong(object):
    def __init__(self, title, artist, album, time, basepath, url):
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.basepath = basepath
        self.path = None
        self.url = url
