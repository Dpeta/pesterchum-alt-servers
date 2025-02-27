import version
import logging
from theme_repo_manager import get_request

PchumLog = logging.getLogger("pchumLogger")

try:
    from PyQt6 import QtCore
except ImportError:
    PchumLog.debug("PyQt5 fallback (update.py)")
    from PyQt5 import QtCore


# thank you mocha for putting up with my bs
# my contributions to this project would be nil if not for u

# i accidentally made a commit named "layout" and i'm NOT letting that be the name
# of the actual final commit for this PR

# I'm gonna change this to get version from the site instead
# so I can set it independently of what's on the repo - Shou
url_version = "https://www.pesterchum.xyz/version.txt"
url_changelog = (
    "https://raw.githubusercontent.com/Dpeta/pesterchum-alt-servers/main/CHANGELOG.md"
)


class UpdateChecker(QtCore.QObject):
    check_done = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.ver_latest = ""
        self.ver_curr = ""
        self.changelog = ""
        self.update_available = False

        self.reply_version = None
        self.reply_changelog = None

    def check(self):
        PchumLog.info("Checking for updates...")
        self.ver_latest = ""
        self.changelog = ""
        self.ver_curr = version.buildVersion

        self.reply_version = get_request(url_version)
        self.reply_changelog = get_request(url_changelog)

        self.reply_version.finished.connect(self._on_version_reply)
        self.reply_changelog.finished.connect(self._on_changelog_reply)

    def _on_version_reply(self):
        version_text = bytes(self.reply_version.readAll()).decode(
            "utf-8", errors="replace"
        )
        self.ver_latest = version_text.strip()

        buildLatest = self.ver_latest.replace("v", "").split(".")
        buildCurrent = self.ver_curr.replace("v", "").split(".")

        self.update_available = buildLatest > buildCurrent

        if self.changelog:
            self.check_done.emit()

    def _on_changelog_reply(self):
        self.changelog = bytes(self.reply_changelog.readAll()).decode(
            "utf-8", errors="replace"
        )

        if self.ver_latest:
            self.check_done.emit()
