from app.models import Tab, WebView


class YouTube(Tab):
    def __init__(self, gui):
        super().__init__(gui)
        self.webView = WebView(self.gui.yt_webView)
