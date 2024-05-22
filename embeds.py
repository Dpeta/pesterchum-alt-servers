from collections import OrderedDict
import logging

try:
    from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork
except ImportError:
    print("PyQt5 fallback (thememanager.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

from theme_repo_manager import get_request


PchumLog = logging.getLogger("pchumLogger")


class EmbedsManager(QtCore.QObject):
    cache = OrderedDict()
    downloading = set()
    max_items = 100

    embed_loading = QtCore.pyqtSignal(str)  # when the get request starts (url: str)
    embed_loaded = QtCore.pyqtSignal(
        str
    )  # when the embed is done downloading (url: str)
    embed_purged = QtCore.pyqtSignal(
        str
    )  # when the embed is cleared from memory (url: str)
    embed_failed = QtCore.pyqtSignal(
        str, str
    )  # when the embed fails to load (url: str, reason: str)

    def __init__(self):
        super().__init__()

    def get_embeds(self):
        return list(self.cache.keys())

    def get_embed(self, url, placeholder=None):
        ## Returns the QPixmap object of the embed image after fetching
        ## Should be called when the embed_loaded signal has been emitted, OR after checking that has_embed == True
        return self.cache.get(url, placeholder)

    def has_embed(self, url):
        return url in self.cache

    def fetch_embed(self, url, ignore_cache=False):
        ## Downloads a new embed if it does not exist yet
        if not ignore_cache and self.has_embed(url):
            self.cache.move_to_end(url)
            PchumLog.debug(
                f"Requested embed fetch of {url}, but it was already fetched"
            )
            return
        elif url in self.downloading:
            PchumLog.debug(
                f"Requested embed fetch of {url} but its already in progress"
            )
            return

        PchumLog.info(f"Fetching embed of {url}")

        self.downloading.add(
            url
        )  # Track which embeds are downloading so we dont do double-fetches
        self.embed_loading.emit(url)
        reply = get_request(url)
        reply.finished.connect(lambda: self._on_request_finished(reply, url))

    def _on_request_finished(self, reply, url):
        ## Callback, called when an embed is finished downloading
        self.downloading.remove(url)
        if reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            PchumLog.info(f"Finished fetching embed {url}")

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(reply.readAll())

            self.cache[url] = pixmap
            self.embed_loaded.emit(url)

            if len(self.cache) > self.max_items:
                to_purge = list(self.cache.keys())[0]
                self.embed_purged.emit(to_purge)
                del self.cache[to_purge]
        else:
            PchumLog.error("Error fetching embed %s: %s" % (url, reply.error()))


manager = EmbedsManager()
