from models.tab import Tab
from models.webview import WebView
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest as qreq
from PyQt5.QtCore import QByteArray


class YouTube(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.webView = WebView(parent.yt_webView)

        self.parent.url_test.clicked.connect(self.go_google)
    def go_google(self):
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
        #temp = "https://t1-3.p-cdn.us/access/?version=5&lid=1128376929&token=Hk7aZOh%2FpxQo1IaibqEiqDGZtQfAyCw50NmiE4Ht%2F%2FkoHScoGE17JBGllBWBWoPGfnncII9DpvcmwMKkGDM6zT%2B2NhkroU%2FWImSNf%2FPyBbpdRCiy5W0UqvAzlw%2FAI%2F0THKhftV3BeDzjjdvdDV0RWvOl0g3Lh%2FSu4t9cE0JL1WpolLFYqLOzYj%2FIEp3YurUPo96G3ARsbC8MxEthXeDYFNYowF98g8kCPjHcRs%2FvNQ%2Bi7vE4IPq9NgRh3m0NZJMVdDnDcOhEtrHQYJpD2qHijjWQfxREZjzaCkt7yiQyEhngcR3oK4CUaykk2zv3%2F1a9yKDH%2FKUhfLlM4gn%2FEGi7Ig%3D%3D"
        temp = "https://www.pandora.com"
        r = qreq()
        r.setUrl(QUrl(temp))
        r.setMethod(qreq.Get)
        '''
        name = QByteArray(str.encode("Accept"))
        value = QByteArray(str.encode("audio/mpeg"))
        #print("setting {0}: {1}".format(k, v))
        r.setHeader(name, value)
        name = QByteArray(str.encode("Content-Type"))
        value = QByteArray(str.encode("audio/mpeg"))
        #print("setting {0}: {1}".format(k, v))
        r.setHeader(name, value)
        '''
        #
        '''
        for k, v in headers.items():
            name = QByteArray(str.encode(k))
            value = QByteArray(str.encode(v))
            print("setting {0}: {1}".format(k, v))
            r.setHeader(name, value)
        print("headers set, here they are:")
        print(r.headers())
        '''
        self.webView.view.load(r)
        '''
        #url = "http://www.pandora.com"
        r = qreq()
        url = "https://audio-sv5-t1-2-v4v6.pandora.com/access/?version=5&lid=758648365&token=QND38rn6IrAoolMRAWp2V6Q0eqwlQWjhVr9OoZR6oDv%2FHoRQV8FN%2Be60wK6MtFjwTyioX587RYkLu23312PmtEP5945ZN2pPBt915vfrI88flFMJCTudGa%2B8KTlm1dT0jdvZBgbDph5gX77TaR1v8RRQT%2Fbd6nGwSzzv%2BGD3eNkdVpyTz%2F8PkgBnkEkiD1U0RRZbKO1h2GDktY6D%2FwG3dRCpRkm6a%2BKlNihGLMcOssEO%2FbtVO9J9GVSdvmY4tFh0NhrvyzLNYfNgY80qEvddIp4v9%2Bv7OFn%2Fl7iKhqLHQ62jrfrLZLENOA6AK6ZTy4un%2FuT0uX8ctA9kHWuH6qCMLmOFCv%2BrSEit"
        r.setUrl(QUrl(url))
        r.setMethod(qreq.Get)
        r.setHeader(b'Host', b'audio-sv5-t1-2-v4v6.pandora.com')
        print("has?")
        print(r.hasHeader(b'Host'))
        self.webView.view.load(r)
        #self.webView.view.setUrl(QUrl(url))
        '''