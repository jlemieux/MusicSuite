from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest as qreq
import requests

n = 0
class WebView(object):
    def __init__(self, view):
        self.view = view

        self.create_profile()
        self.set_page()
        self.set_interceptor()

        self.enable_plugins()
        self.enable_fullscreen()

        #print(self.page.profile().httpUserAgent())

    def enable_plugins(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.PluginsEnabled, True)
        self.view.settings().setAttribute(
          QWebEngineSettings.AllowRunningInsecureContent, True)

    def enable_fullscreen(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.FullScreenSupportEnabled, True)
        self.view.page().fullScreenRequested.connect(
          lambda request: request.accept())

    def create_profile(self):
        self.profile = QWebEngineProfile(self.view)

    def set_page(self):
        self.page = QWebEnginePage(self.profile, self.view)
        self.view.setPage(self.page)

    def set_interceptor(self):
        self.interceptor = WebUrlRequestInterceptor(self.view)
        self.profile.setRequestInterceptor(self.interceptor)

class WebUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        print(info.requestUrl().toString())
        '''
        headers = {
            "Host": "audio-sv5-t1-2-v4v6.pandora.com",
            "Connection": "keep-alive",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "chrome-proxy": "frfr",
            "Accept": "*/*",
            "Referer": "https://audio-sv5-t1-2-v4v6.pandora.com/access/?version=5&lid=758648365&token=QND38rn6IrAoolMRAWp2V6Q0eqwlQWjhVr9OoZR6oDv%2FHoRQV8FN%2Be60wK6MtFjwTyioX587RYkLu23312PmtEP5945ZN2pPBt915vfrI88flFMJCTudGa%2B8KTlm1dT0jdvZBgbDph5gX77TaR1v8RRQT%2Fbd6nGwSzzv%2BGD3eNkdVpyTz%2F8PkgBnkEkiD1U0RRZbKO1h2GDktY6D%2FwG3dRCpRkm6a%2BKlNihGLMcOssEO%2FbtVO9J9GVSdvmY4tFh0NhrvyzLNYfNgY80qEvddIp4v9%2Bv7OFn%2Fl7iKhqLHQ62jrfrLZLENOA6AK6ZTy4un%2FuT0uX8ctA9kHWuH6qCMLmOFCv%2BrSEit",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
            "Range": "bytes=0-",
        }
        temp = "https://audio-sv5-t1-2-v4v6.pandora.com/access/?version=5&lid=758648365&token=QND38rn6IrAoolMRAWp2V6Q0eqwlQWjhVr9OoZR6oDv%2FHoRQV8FN%2Be60wK6MtFjwTyioX587RYkLu23312PmtEP5945ZN2pPBt915vfrI88flFMJCTudGa%2B8KTlm1dT0jdvZBgbDph5gX77TaR1v8RRQT%2Fbd6nGwSzzv%2BGD3eNkdVpyTz%2F8PkgBnkEkiD1U0RRZbKO1h2GDktY6D%2FwG3dRCpRkm6a%2BKlNihGLMcOssEO%2FbtVO9J9GVSdvmY4tFh0NhrvyzLNYfNgY80qEvddIp4v9%2Bv7OFn%2Fl7iKhqLHQ62jrfrLZLENOA6AK6ZTy4un%2FuT0uX8ctA9kHWuH6qCMLmOFCv%2BrSEit"
        if info.requestUrl().toString() == temp:
            r = qreq()
            r.setUrl(info.requestUrl())
            r.setMethod(qreq.Get)
            for k, v in headers.items():
                name = QByteArray(str.encode(k))
                value = QByteArray(str.encode(v))
                print("setting {0}: {1}".format(k, v))
                r.setHeader(name, value)
            print("headers set, here they are:")
            print(r.headers())
            
        
        url = "https://audio-sv5-t1-2-v4v6.pandora.com/access/?version=5&lid=758648365&token=QND38rn6IrAoolMRAWp2V6Q0eqwlQWjhVr9OoZR6oDv%2FHoRQV8FN%2Be60wK6MtFjwTyioX587RYkLu23312PmtEP5945ZN2pPBt915vfrI88flFMJCTudGa%2B8KTlm1dT0jdvZBgbDph5gX77TaR1v8RRQT%2Fbd6nGwSzzv%2BGD3eNkdVpyTz%2F8PkgBnkEkiD1U0RRZbKO1h2GDktY6D%2FwG3dRCpRkm6a%2BKlNihGLMcOssEO%2FbtVO9J9GVSdvmY4tFh0NhrvyzLNYfNgY80qEvddIp4v9%2Bv7OFn%2Fl7iKhqLHQ62jrfrLZLENOA6AK6ZTy4un%2FuT0uX8ctA9kHWuH6qCMLmOFCv%2BrSEit"
        r.setUrl(QUrl(url))
        r.setMethod(qreq.Get)
        r.setHeader(b'Host', b'audio-sv5-t1-2-v4v6.pandora.com')
        print("has?")
        print(r.hasHeader(b'Host'))
        self.webView.view.load(r)
        #self.webView.view.setUrl(QUrl(url))
        for k, v in headers.items():
            name = QByteArray(str.encode(k))
            value = QByteArray(str.encode(v))
            print("setting {0}: {1}".format(k, v))
            info.setHttpHeader(name, value)
        temp = "https://audio-sv5-t1-2-v4v6.pandora.com/access/?version=5&lid=758648365&token=QND38rn6IrAoolMRAWp2V6Q0eqwlQWjhVr9OoZR6oDv%2FHoRQV8FN%2Be60wK6MtFjwTyioX587RYkLu23312PmtEP5945ZN2pPBt915vfrI88flFMJCTudGa%2B8KTlm1dT0jdvZBgbDph5gX77TaR1v8RRQT%2Fbd6nGwSzzv%2BGD3eNkdVpyTz%2F8PkgBnkEkiD1U0RRZbKO1h2GDktY6D%2FwG3dRCpRkm6a%2BKlNihGLMcOssEO%2FbtVO9J9GVSdvmY4tFh0NhrvyzLNYfNgY80qEvddIp4v9%2Bv7OFn%2Fl7iKhqLHQ62jrfrLZLENOA6AK6ZTy4un%2FuT0uX8ctA9kHWuH6qCMLmOFCv%2BrSEit"
        if info.requestUrl().toString() == temp:
            print("tempgin...")
            info.setHttpHeader(b'Host', b'audio-sv5-t1-2-v4v6.pandora.com')
        global n
        print("{0}-{1}: {2}".format(n, info.resourceType(), info.requestUrl()))
        n += 1
        '''
        if info.resourceType() == 8:  # media type
            song_url = info.requestUrl().toString()
            fp = "C:\\Programming\\QTApps\\Suite\\misc\\song.mp3"
            input("About to download {0}".format(song_url))
            with open(fp, "wb") as song:
                response = requests.get(song_url)
                song.write(response.content)
