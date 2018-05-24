import requests
from xml.etree import ElementTree
import sys
import traceback


class Album(object):
    def __init__(self, id, title, type, date, n_tracks, nth_track):
        self.id = id
        self.title = title
        self.type = type
        self.date = date
        self.n_tracks = n_tracks
        self.nth_track = nth_track
        self.art_url = None

    def get_date_year(self):
        # date: YYYY-MM-DD
        return self.date.split('-')[0]


class AlbumAPI(object):
    def __init__(self):
        self.info_base = "http://musicbrainz.org/ws/2/recording/?query={0}"
        self.art_base = "http://coverartarchive.org/release/{0}"

    def get_album_info(self, title, artist):
        info_query = self.build_info_query(title, artist)
        info_response = self.get_response(info_query, 'info')
        ns = "http://musicbrainz.org/ns/mmd-2.0#"
        ElementTree.register_namespace('', ns)
        xml_root = ElementTree.fromstring(info_response.content)
        album = self.create_album(xml_root)
        if album is not None:
            self.set_album_art_url(album)
        return album

    def set_album_art_url(self, album):
        art_response = self.get_response(album.id, 'art')
        try:
            json = art_response.json()
        except BaseException:
            print(traceback.format_exc())
            input("waiting...")
            sys.exit(1)
        default = None
        for image in json['images']:
            if image['front'] == 'true':
                url = image['image']
                break
            if (default is None) and ('Front' in image['types']):
                default = image
        else:
            url = default['image']
        album.art_url = url

    def build_info_query(self, title, artist):
        title = title.replace(' ', '%20')
        artist = artist.replace(' ', '%20')
        query = "recording:%22{0}%22%20AND%20artist:%22{1}%22".format(title, artist)
        return query

    def get_response(self, query, type):
        if type == 'art':
            url = self.art_base.format(query)
        else:
            url = self.info_base.format(query)
        response = requests.get(url)
        return response

    def namespace_find(self, root, tag):
        ns0 = "{http://musicbrainz.org/ns/mmd-2.0#}"
        ns1 = "{http://musicbrainz.org/ns/ext#-2.0}"
        try:
            element = root.find(ns0 + tag)
        except TypeError:  # xml namespace issue
            element = root.find(ns1 + tag)
        return element

    def create_album(self, root):
        recording_list = self.namespace_find(root, 'recording-list')
        if len(recording_list) == 0:
            return None
        for recording in recording_list:
            release_list = self.namespace_find(recording, 'release-list')
            for release in release_list:
                fr_id = release.attrib['id']
                fr_title = self.namespace_find(release, 'title').text
                release_group = self.namespace_find(release, 'release-group')
                fr_type = self.namespace_find(release_group, 'primary-type').text
                fr_date = self.namespace_find(release, 'date').text
                medium_list = self.namespace_find(release, 'medium-list')
                fr_n_tracks = self.namespace_find(medium_list, 'track-count').text
                medium = self.namespace_find(medium_list, 'medium')
                format = self.namespace_find(medium, 'format').text
                track_list = self.namespace_find(medium, 'track-list')
                track = self.namespace_find(track_list, 'track')
                fr_nth_track = self.namespace_find(track, 'number').text
                if format == 'CD' or format == 'Digital Media':
                    break
            if format == 'CD' or format == 'Digital Media':
                break
        else:
            fr_nth_track = "99"

        fr_nth_track = "{0:0>2d}".format(int(fr_nth_track))
        album = Album(fr_id, fr_title, fr_type, fr_date, fr_n_tracks, fr_nth_track)
        return album
