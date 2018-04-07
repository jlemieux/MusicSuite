from models.tab import Tab
from models.webview import WebView

class Pandora(Tab):
    def __init__(self, parent):
        super().__init__(parent)
        self.webView = WebView(parent.pd_webView)
