from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class WebView(object):
    def __init__(self, view):
        self.view = view

        self.create_profile()
        self.set_page()
        self.set_interceptor()

        self.enable_plugins()
        self.enable_fullscreen()

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
    url_received = pyqtSignal(str)

    def __init__(self, webView):
        super().__init__()

    def interceptRequest(self, info):
        if info.resourceType() == 8:  # media type
            download_url = info.requestUrl().toString()
            self.url_received.emit(download_url)
