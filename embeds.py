from collections import OrderedDict
import logging

try:
    from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork
except ImportError:
    print("PyQt5 fallback (thememanager.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

from theme_repo_manager import get_request


PchumLog = logging.getLogger("pchumLogger")

## embeds.py
# system for fetching & displaying image previews for image URLs
# has a single instance called `manager` at the bottom of this file

## TODO:
## - add domain filters in settings
## - add "ignore filters" or whatever toggle in settings
## - *verify* domain filters


class EmbedsManager(QtCore.QObject):
    cache = OrderedDict()
    downloading = set()
    max_items = 50

    main_window = None

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
        """Returns all cached embeds"""
        return list(self.cache.keys())

    def get_embed(self, url, placeholder=None):
        """Returns the QPixmap object of the embed image after fetching
        Should be called when the embed_loaded signal has been emitted, OR after checking that has_embed == True
        """
        if url in self.cache:
            self.cache.move_to_end(url)
            # make sure that embeds that were fetched a while ago but recently used do not get purged first
        return self.cache.get(url, placeholder)

    def has_embed(self, url):
        return url in self.cache

    def check_trustlist(self, url):
        for item in self.main_window.config.userprofile.getTrustedDomains():
            print("~~", item)
            if url.startswith(item):
                print("yurt")
                return True
        print("nah")
        return False

    def fetch_embed(self, url, ignore_cache=False):
        """Downloads a new embed if it does not exist yet"""

        if not self.check_trustlist(url):
            PchumLog.warning(
                "Requested embed fetch of %s denied because it does not match te trust filter.",
                url,
            )
            return

        if not ignore_cache and self.has_embed(url):
            PchumLog.debug(
                "Requested embed fetch of %s, but it was already fetched", url
            )
            return
        elif url in self.downloading:
            PchumLog.debug(
                "Requested embed fetch of %s, but it is already being fetched", url
            )
            return

        PchumLog.info("Fetching embed of %s", url)

        self.downloading.add(url)
        # Track which embeds are downloading so we dont do double-fetches

        self.embed_loading.emit(url)
        reply = get_request(url)
        reply.finished.connect(lambda: self._on_request_finished(reply, url))

    def _on_request_finished(self, reply, url):
        """Callback, called when an embed has finished downloading"""
        self.downloading.remove(url)
        if reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            PchumLog.info(f"Finished fetching embed {url}")

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(reply.readAll())

            self.cache[url] = pixmap
            self.embed_loaded.emit(url)

            if len(self.cache) > self.max_items:
                to_purge = list(self.cache.keys())[0]
                PchumLog.debug("Purging embed %s", to_purge)
                self.embed_purged.emit(to_purge)
                del self.cache[to_purge]
        else:
            PchumLog.error("Error fetching embed %s: %s", url, reply.error())
            self.embed_failed.emit(url, str(reply.error()))


manager = EmbedsManager()
