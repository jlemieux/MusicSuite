from PyQt5.QtWebEngineWidgets import QWebEngineSettings


class WebView(object):
    def __init__(self, view):
        self.view = view
        self.enable_plugins()
        self.enable_fullscreen()
    def enable_plugins(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.PluginsEnabled, True)
    def enable_fullscreen(self):
        self.view.settings().setAttribute(
          QWebEngineSettings.FullScreenSupportEnabled, True)
        self.view.page().fullScreenRequested.connect(
          lambda request: request.accept())
