import version
from theme_repo_manager import get_request

try:
    from PyQt6 import QtCore
except ImportError:
    print("PyQt5 fallback (update.py)")
    from PyQt5 import QtCore


# thank you mocha for putting up with my bs
# my contributions to this project would be nil if not for u

url_version = (
    "https://raw.githubusercontent.com/Dpeta/pesterchum-alt-servers/main/version.py"
)
url_changelog = (
    "https://raw.githubusercontent.com/Dpeta/pesterchum-alt-servers/main/CHANGELOG.md"
)

class UpdateChecker(QtCore.QObject):
    ver_latest = ""
    ver_curr = ""
    changelog = ""
    update_available = False

    check_done = QtCore.pyqtSignal()

    reply_version = None
    reply_changelog = None

    def check(self):
        self.ver_latest = ""
        self.changelog = ""
        self.ver_curr = version.buildVersion

        self.reply_version = get_request(url_version)
        self.reply_changelog = get_request(url_changelog)

        self.reply_version.finished.connect(self._on_version_reply)
        self.reply_changelog.finished.connect(self._on_changelog_reply)


    def _on_version_reply(self):

        version_text = bytes(self.reply_version.readAll()).decode("utf-8")
        for line in version_text.split('\n'):
            if "buildVersion" in line:
                temp = line.replace("buildVersion = ", "")
                self.ver_latest = temp.strip("\"")
        
        self.ver_latest.replace('"', "")
        self.ver_curr.replace('"', "")

        buildLatest = self.ver_latest.split(".")
        buildCurrent = self.ver_curr.split(".")
        x = 0
        for x in range(2):
            if buildCurrent[x] < buildLatest[x]:
                self.update_available = True 

        if self.changelog != "":
            self.check_done.emit()

    def _on_changelog_reply(self):

        self.changelog = bytes(self.reply_changelog.readAll()).decode("utf-8")

        if self.ver_latest != "":
            self.check_done.emit()
        