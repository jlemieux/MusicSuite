from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from bs4 import BeautifulSoup


class AudioConverter(Worker):
    song_converted = pyqtSignal()
    def __init__(self):
        super().__init__()

    @pyqtSlot(PandoraSong)
    def convert(self, song):
        output = song.temp_dl_path.with_suffix(".mp3")
        cmd = ('ffmpeg -i "{0}" -y -acodec libmp3lame -ab 192k "{1}"'
               .format(song.temp_dl_path, output))
        subprocess.call(shlex.split(cmd))
        os.remove(song.temp_dl_path)
        song.temp_dl_path = output
        self.song_converted.emit()
        self.thread.quit()

class Downloader(Worker):
    song_downloaded = pyqtSignal()
    def __init__(self):
        super().__init__()

    @pyqtSlot(PandoraSong)
    def download(self, song):
        response = requests.get(song.download_url)
        self._check_audio_format(song, response)

        with open(song.temp_dl_path, "wb") as downloaded_song:
            downloaded_song.write(response.content)
        self.song_downloaded.emit()
        self.thread.quit()

    def _check_audio_format(self, song, response):
        if response.headers['Content-Type'] == 'audio/mp4':
            song.temp_dl_path = temp_dl_path.with_suffix(".mp4")

class Authenticator(object):
    MAX_FILENAME_LENGTH = 40
    SYMBOLS = ['.', '_', "'", '-', '&', ')', '(', '@', '#', '$', '!', '%', '~']

    def __init__(self):
        pass

    def is_safe(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

        if not self._auth_empty():
            return False
        if not self._auth_length():
            return False
        if not self._auth_chars():
            return False

        return True

    def _auth_empty(self):
        error_title = "Empty field"
        error_text = "Field <{0}> is empty!"

        if len(''.join(self.title.split())) == 0:
            self._report_error(error_title, error_text.format('Title'))
            return False
        if len(''.join(self.artist.split())) == 0:
            self._report_error(error_title, error_text.format('Artist'))
            return False
        if len(''.join(self.album.split())) == 0:
            self._report_error(error_title, error_text.format('Album'))
            return False

        return True

    def _auth_length(self):
        error_title = "Excess length"
        error_text = "Field <{0}> is {1} characters. Max filename length " \
                     "is " + self.MAX_FILENAME_LENGTH + "!"

        example_track = "01 "
        example_extension = ".mp3"
        final_title = example_track + self.title + example_extension
        title_len = len(final_title)
        artist_len = len(artist)
        album_len = len(album)

        if title_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Title', title_len))
            return False
        if artist_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Artist', artist_len))
            return False
        if album_len > self.MAX_FILENAME_LENGTH:
            self._report_error(error_title, error_text.format('Album', album_len))
            return False

        return True

    def _auth_chars(self):
        error_title = "Forbidden characters"
        error_text = self._create_chars_error_text()

        pattern = self._create_regex_pattern()

        if not re.match(pattern, self.title):
            self._report_error(error_title, error_text.format('Title'))
            return False
        if not re.match(pattern, self.artist):
            self._report_error(error_title, error_text.format('Artist'))
            return False
        if not re.match(pattern, self.album):
            self._report_error(error_title, error_text.format('Album'))
            return False

        return True

    def _create_regex_pattern(self):
        pattern = r"^([^\S\n\t]|[a-zA-Z0-9"
        for symbol in self.symbols:
            pattern += "\{0}".format(symbol)
        pattern += "])+$"
        return pattern

    def _create_chars_error_text(self):
        error_text = "Field <{0}> contains forbidden characters!\n" \
             "Valid characters are:\n" \
             "\t> a-z, A-Z, 0-9\n" \
             "\t> Spaces and commas\n" \
             "\t> Additional:\n"
        for symbol in symbols:
            error_text += "\t\t> {0}\n".format(symbol)
        error_text = error_text[:-2]  # remove last '\n'
        return error_text

    def _report_error(self, error_title, error_text):
        msg = QMessageBox(QMessageBox.Information,
                          error_title,
                          error_text,
                          QMessageBox.Ok)
        msg.exec_()

class Worker(QObject):
    def __init__(self):
        super().__init__()
        self.thread = None

class PandoraSong(object):
    def __init__(self, title, artist, album, time, download_url):
        self.title = title
        self.artist = artist
        self.album = album
        self.time = time
        self.download_url = download_url
        self.temp_dl_path = None
        self.mb_album = None
        self.itunes_path = None
        self.itunes_add_path = None

class PandoraDownloadPanel(object):
    def __init__(self, gui):
        self.gui = gui
        self.btn_download = self.gui.pb_download
        self.btn_find_album = self.gui.pb_findAlbum
        self.title = self.gui.lbl_title
        self.artist = self.gui.lbl_artist
        self.album = self.gui.lbl_album

    def enable(self):
        self.btn_download.setText("Download")
        self.btn_download.setEnabled(True)
        self.btn_find_album.setEnabled(True)
        self.title.setEnabled(True)
        self.artist.setEnabled(True)
        self.album.setEnabled(True)

    def disable(self):
        self.btn_download.setDisabled(True)
        self.btn_find_album.setDisabled(True)
        self.title.setDisabled(True)
        self.artist.setDisabled(True)
        self.album.setDisabled(True)

    def fill_labels(self, song):
        self.title.setText(song.title)
        self.artist.setText(song.artist)
        self.album.setText(song.album)

    def confirm_download(self):
        self.btn_download.setText("Downloaded!")

class PandoraSongFactory(Worker):
    song_created = pyqtSignal(PandoraSong)
    song_missing = pyqtSignal(str)

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.song_missing.connect(self._post_html)

    @pyqtSlot(str)
    def create_song(self, download_url):
        self._post_html(download_url)

    @pyqtSlot(str)
    def _post_html(self, download_url):
        print("Trying to create song...")
        self.page.toHtml(lambda html: self._create_song(html, download_url))

    def _create_song(self, html, download_url):
        soup = BeautifulSoup(html, "html.parser")
        try:
            title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
            artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
            album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
            time = soup.find("span", {"data-qa": "remaining_time"}).contents[0]
        except AttributeError:
            print("Could not find song info on current screen.")
            time.sleep(1)
            self.song_missing.emit(download_url)
        else:
            print("Song created.")
            song = PandoraSong(title, artist, album, time, download_url)
            self.song_created.emit(song)
            self.thread.quit()

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
