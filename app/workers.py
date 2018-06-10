import time
import sys
from xml.etree import ElementTree

from app.models import Album, Worker
from app.pandora.models import PandoraSong

import requests
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class MBAlbumAPI(Worker):
    album_created = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.info_base = "http://musicbrainz.org/ws/2/recording/?query={0}"
        self.art_base = "http://coverartarchive.org/release/{0}"

    @pyqtSlot(PandoraSong)
    def set_mb_album(self, song):
        queries = self._build_queries(song.title, song.artist)
        for query in queries:
            url = self.info_base.format(query)
            response = requests.get(url)
            xml_root = ElementTree.fromstring(response.content)
            album = self._create_album(xml_root)
            if album is not None:
                song.mb_album = album
                self.album_created.emit(True)
                break
        else:
            self.album_created.emit(False)

        self.thread.quit()

    '''
    @pyqtSlot(YoutubeSong)
    def set_mb_album(self, song):
        queries = self._build_queries(song.title, song.artist)
        for query in queries:
            url = self.info_base.format(query)
            response = requests.get(url)
            xml_root = ElementTree.fromstring(response.content)
            album = self._create_album(xml_root)
            if album is not None:
                song.mb_album = album
                self.album_created.emit(album_exists=True)
                break
        else:
            self.album_create.emit(album_exists=False)

        self.thread.quit()
    '''

    def _create_album(self, root):
        recording_list = self._namespace_find(root, 'recording-list')
        if len(recording_list) == 0:
            return None
        for recording in recording_list:
            release_list = self._namespace_find(recording, 'release-list')
            for release in release_list:
                medium_list = self._namespace_find(release, 'medium-list')
                medium = self._namespace_find(medium_list, 'medium')
                format = self._namespace_find(medium, 'format').text
                track_list = self._namespace_find(medium, 'track-list')
                track = self._namespace_find(track_list, 'track')
                #release_group = self._namespace_find(release, 'release-group')

                album_id = release.attrib['id']
                album_title = self._namespace_find(release, 'title').text
                album_date = self._namespace_find(release, 'date').text
                album_nth_track = self._namespace_find(track, 'number').text
                try:
                    int(album_nth_track)
                except ValueError:  # inconsistent API format...
                    # Format: 'track-ntracks'
                    album_nth_track = album_nth_track.split('-')[0]
                album_n_tracks = self._namespace_find(medium_list, 'track-count').text
                #album_type = self._namespace_find(release_group, 'primary-type').text

                if format == 'CD' or format == 'Digital Media':
                    break

            if format == 'CD' or format == 'Digital Media':
                break
        else:
            # mbz.org doesn't have CD track number, only album formats
            album_nth_track = '99'

        album_nth_track = "{0:0>2d}".format(int(album_nth_track))
        art_url = self._get_album_art_url(album_id)
        album = Album(album_id, album_title, album_date, album_nth_track,
                      album_n_tracks, art_url)

        return album

    def _get_album_art_url(self, id):
        url = self.art_base.format(id)
        while True:
            response = requests.get(url)
            if response.status_code == 404:  # no album art found
                return None
            try:
                json = response.json()
                break
            except ValueError:
                print("JSON for url <{0}> value error.".format(url))
                time.sleep(1)
                continue

        default = None  # Default image url if 'front' image not found
        for image in json['images']:
            if image['front'] == 'true':
                url = image['image']
                break
            if default is None:
                default = image['image']
        else:
            url = default

        return url

    def _build_queries(self, title, artist):
        queries = []
        base = "recording:%22{0}%22%20AND%20artist:%22{1}%22"

        q1 = base.format(title.replace(' ', '%20'), artist.replace(' ', '%20'))
        queries.append(q1)

        q2 = base.format(title.replace(' ', ''), artist.replace(' ', '%20'))
        queries.append(q2)

        return queries

    def _namespace_find(self, root, tag):
        ns0 = "{http://musicbrainz.org/ns/mmd-2.0#}"
        ns1 = "{http://musicbrainz.org/ns/ext#-2.0}"
        try:
            element = root.find(ns0 + tag)
        except TypeError:  # xml namespace issue
            element = root.find(ns1 + tag)
        return element
