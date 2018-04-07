from models.tab import Tab
from models.webview import WebView

class YouTube(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.webView = WebView(parent.yt_webView)
