from models.tab import Tab
from models.pandora_song import PandoraSong
from models.webview import WebView
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest as qreq

from bs4 import BeautifulSoup

import sys
import time
from threading import Thread


class Pandora(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.webView = WebView(parent.pd_webView)
        self.webView.interceptor.subscribe(self.wait_for_DOM)

        self.parent.html_test.clicked.connect(self.send_req)

    def wait_for_DOM(self, event):
        '''Delay toHtml call to allow DOM to load'''
        url = event.url
        thr = Thread(target=self.get_html, args=(url,))
        thr.start()

    def get_html(self, url):
        time.sleep(2)
        self.webView.page.toHtml(lambda html: self.create_song(html, url))

    def create_song(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("div", {"class": "Marquee__wrapper__content"}).contents[0]
        artist = soup.find("a", {"class": "nowPlayingTopInfo__current__artistName nowPlayingTopInfo__current__link"}).contents[0]
        album = soup.find("a", {"class": "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link"}).contents[0]
        song = PandoraSong(title, artist, album, url)

    def send_req(self):
        temp = "https://www.pandora.com"
        r = qreq()
        r.setUrl(QUrl(temp))
        r.setMethod(qreq.Get)
        self.webView.view.load(r)
