

class iTunesSong(object):
    def __init__(self, row, title, artist, album,
                 time, n_tracks, nth_track, year, path):
        self.row = row
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.n_tracks = n_tracks
        self.nth_track = nth_track
        self.year = year
        self.path = path
