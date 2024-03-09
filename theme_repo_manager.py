import os
import io
import json
import time
import zipfile
import logging
import hashlib
from shutil import rmtree
from datetime import datetime

from ostools import getDataDir

try:
    from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork
    from PyQt6.QtGui import QAction

    _flag_search_exact = QtCore.Qt.MatchFlag.MatchExactly
    _flag_selectable = QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
    _flag_topalign = (
        QtCore.Qt.AlignmentFlag.AlignLeading
        | QtCore.Qt.AlignmentFlag.AlignLeft
        | QtCore.Qt.AlignmentFlag.AlignTop
    )
except ImportError:
    print("PyQt5 fallback (thememanager.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
    from PyQt5.QtWidgets import QAction

    _flag_search_exact = QtCore.Qt.MatchExactly
    _flag_selectable = QtCore.Qt.TextSelectableByMouse
    _flag_topalign = QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop

# ~Lisanne
# This file has all the stuff needed to use a theme repository
# - ThemeManagerWidget, a GUI widget that lets the user install, update, & delete repository themes
# - ThemeManager, the class that the widget hooks up to. Handles fetching, downloading, installing, & keeps the manifest updated
#
# It works with version 4 of the theme repository database 4
# You can read more about it here: https://github.com/mocchapi/pesterchum-themes

# manifest.json is a local file in the datadir that tracks the metadata of themes installed from the repository
# Its structured as such:
# {
#   meta: {
#       format_version: <format version last used>,
#       updated_at: <timestamp when last written to>
#   },
#   entries: {
#       <installed theme name>: {<theme data as seen in the database>}
#   }
# }

# Possible future additions:
# - compare hashes of installed themes with a databases `sha256_install`

PchumLog = logging.getLogger("pchumLogger")
downloads = set()
themeManager = None
networkManager = QtNetwork.QNetworkAccessManager()  # Does the HTTP requests
# PyQT docs say only instance one is needed per program
userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"


# ~lisanne:
# these are here because we connect the reply finished() signal to lambdas later on
# and APPARENTLY they get garbage collected & never trigger if your code leaves the scope before it finishes downloading
# which is basically always unless the file is like 0.001kb. anyways. evil pyqt
def get_request(url):
    request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
    request.setRawHeader(b"User-Agent", userAgent.encode())
    reply = networkManager.get(request)
    # Add to downloads set to prevent GC until its finished
    downloads.add(reply)
    return reply


def _on_request_finished(reply):
    # Remove the reply from the downloads set to make it GC-able again
    downloads.remove(reply)
    reply.deleteLater()


networkManager.finished.connect(_on_request_finished)


def sha256_bytes(buff):
    return hashlib.sha256(buff).hexdigest()


class ThemeManager(QtCore.QObject):
    # signals
    theme_installed = QtCore.pyqtSignal(str)  # theme name
    zip_downloaded = QtCore.pyqtSignal(str, str)  # theme name, zip location
    database_refreshed = QtCore.pyqtSignal(dict)  # self.manifest
    manifest_updated = QtCore.pyqtSignal(dict)  # self.manifest
    errored = QtCore.pyqtSignal(str)  # error_text

    # variables
    manifest = {}  # In-memory version of manifest
    database = {}  # The latest db.json fetch
    database_entries = (
        {}
    )  # name:entry lookup table of compatible themes in the database

    config = None
    manifest_path = os.path.join(getDataDir(), "manifest.json")

    SUPPORTED_VERSION = 4  # theme format version supported

    def __init__(self, config):
        super().__init__()
        with open(self.manifest_path, "r") as f:
            self.manifest = json.load(f)
        PchumLog.debug("manifest.json loaded with: %s", self.manifest)
        self.config = config

        self.validate_manifest()
        self.refresh_database()

    @QtCore.pyqtSlot()
    def refresh_database(self):
        # Fetches a new copy of the theme database from the given URL
        # The initialisation & processing of it is handled in self._on_database_reply
        if self.config.theme_repo_url().strip() == "":
            self._error(
                "No theme repository db URL has been set in the Idle/Updates settings."
            )
            return

        PchumLog.debug(
            "Refreshing theme repo database @ %s", self.config.theme_repo_url()
        )
        reply = get_request(self.config.theme_repo_url())
        reply.finished.connect(lambda: self._on_database_reply(reply))

    def delete_theme(self, theme_name, cascade_delete=True):
        # Deletes the given theme
        # If cascade_delete == True, then all installed themes that inherit from the given theme (directly or indirectly) will also be deleted
        # Note that this function will never delete a theme inside the pesterchum/themes folder, only themes installed through the repository will be removed
        if cascade_delete:
            for item in self.get_inheriting_themes(theme_name, only_installed=True):
                if self.is_installed(item):
                    self.delete_theme(item, cascade_delete=cascade_delete)

        PchumLog.info("Deleting installed repo theme %s", theme_name)
        theme = self.manifest["entries"].get(theme_name)
        if theme is None:
            PchumLog.error("Theme was not installed!")
            return
        directory = os.path.join(getDataDir(), "themes", theme_name)

        if os.path.isdir(directory):
            rmtree(directory)

        self.manifest["entries"].pop(theme_name)
        self.save_manifest()
        self.manifest_updated.emit(self.manifest)

    def get_inheriting_themes(self, theme_name, only_installed=False, max_depth=20):
        # Returns a list of themes that (directly or indirectly) inherit from the given theme
        # if only_instaled == True, then only themes who's entire ancestry towards the given theme are installed will be included
        out = []
        targets = set(self.database_entries.keys())

        def recurse(name, depth=0):
            for item_name in tuple(targets):
                if depth > max_depth:
                    PchumLog.warning("Exceeded inheriting detection recurse depth")
                    return out

                inherits = self.database_entries[item_name]["inherits"]
                if inherits == "":
                    inherits = "pesterchum"

                if inherits == name:
                    if only_installed and not self.is_installed(item_name):
                        continue
                    targets.remove(item_name)
                    out.append(item_name)
                    recurse(out[-1], depth + 1)
            return out

        return recurse(theme_name)

    def save_manifest(self):
        # Writes manifest.json to datadir
        self.manifest["meta"] = self.manifest.get("meta", {})
        self.manifest["meta"]["updated_at"] = time.time()
        self.manifest["meta"]["format_version"] = self.database.get("meta", {}).get(
            "format_version", self.SUPPORTED_VERSION
        )
        self.manifest["entries"] = self.manifest.get("entries", {})
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f)
        PchumLog.debug("Saved manifes.js to %s", self.manifest_path)

    def validate_manifest(self):
        # Checks if the themes the manifest claims are installed actually exists & does some structure validation
        # Removes them from the manifest if they dont
        if not "meta" in self.manifest:
            self.manifest["meta"] = {}
        if not "updated_at" in self.manifest["meta"]:
            self.manifest["meta"]["updated_at"] = time.time()
        if not "format_version" in self.manifest["meta"]:
            self.manifest["meta"]["format_version"] = self.SUPPORTED_VERSION
        if not "entries" in self.manifest:
            self.manifest["entries"] = {}

        if self.manifest["meta"]["format_version"] != self.SUPPORTED_VERSION:
            PchumLog.warning(
                "Existing manifest version (%s) does not match supported version (%s). Was the client updated?",
                self.manifest["meta"]["format_version"],
                self.SUPPORTED_VERSION,
            )
        to_pop = set()
        all_themes = self.config.availableThemes()
        for theme_name in self.manifest["entries"]:
            if not theme_name in all_themes:
                PchumLog.warning(
                    "Supposedly installed theme %s from the manifest seems to have been deleted, removing from manifest now",
                    theme_name,
                )
                # Cannot be popped while iterating!
                to_pop.add(theme_name)

        for theme_name in to_pop:
            self.manifest["entries"].pop(theme_name)

    def _download_theme(self, theme_name):
        # Downloads the theme .zip
        # The actual installing is handled by _on_theme_reply when the theme is downloaded
        # Performs no version checks or dependency handling
        # Use install_theme() instead unless you know what you're doing
        PchumLog.info("Downloading %s", theme_name)
        if not theme_name in self.database_entries:
            PchumLog.error("Theme name %s does not exist in the database!", theme_name)
            return
        PchumLog.debug("(From %s)", self.database_entries[theme_name]["download"])
        reply = get_request(self.database_entries[theme_name]["download"])
        reply.finished.connect(
            lambda: self._on_theme_reply(
                reply, self.database_entries[theme_name].copy()
            )
        )

    def _error(self, msg):
        PchumLog.error("ThemeManager: %s", msg)
        self.errored.emit(msg)

    def install_theme(self, theme_name, force_install=False):
        # A higher way to install a theme than _download_theme
        # Checks if the theme is already installed & if its up to date
        # Also recursively handled dependencies, which _download_theme does not
        # !! note that this does not check if theres a circular dependency !!
        # Setting force_install to True will install a given theme, even if it is deemed unnecessary to do so or its inherit dependency cannot be installed
        # This gives it the same no-nonsense operation as _download_theme, but with the checks in place
        PchumLog.info("Installing theme %s", theme_name)
        if force_install:
            PchumLog.debug("(force_install is enabled)")

        if not theme_name in self.database_entries:
            self._error("Theme %s does not exist in the database!" % theme_name)
            return

        all_themes = self.config.availableThemes()
        theme = self.database_entries[theme_name]
        if (
            not self.is_installed(theme_name) and theme_name in all_themes
        ):  # Theme exists, but not installed by manager
            PchumLog.warning(
                "Theme %s is already installed manually. The manual version will get shadowed by the repository version & will not be usable",
                theme_name,
            )

        # Check depedencies
        if theme["inherits"] != "":
            if self.is_installed(theme["inherits"]):
                # Inherited theme is installed. A-OK
                PchumLog.debug(
                    "Theme %s requires theme %s, which is already installed through the repository",
                    theme_name,
                    theme["inherits"],
                )
            if theme["inherits"] in all_themes:
                # Inherited theme is manually installed. A-OK
                PchumLog.debug(
                    "Theme %s requires theme %s, which is already installed manually by the user",
                    theme_name,
                    theme["inherits"],
                )
            elif theme["inherits"] in self.database_entries:
                # The Inherited theme is not installed, but can be. A-OK
                PchumLog.info(
                    "Theme %s requires theme %s, which will now be installed",
                    theme_name,
                    theme["inherits"],
                )
                self.install_theme(theme["inherits"])
            else:
                # Inherited theme is not installed, and can't be installed automatically. Exits unless force_install is True
                if force_install:
                    PchumLog.error(
                        "Theme %s requires theme %s, which is not installed and not in the database. Installing %s anyways, because force_install is True",
                        theme_name,
                        theme,
                        theme_name["inherits"],
                    )
                else:
                    # TODO: maybe make this a popup?
                    self._error(
                        "Theme %s requires theme %s, which is not installed and not in the database. Cancelling install"
                        % (theme_name, theme["inherits"])
                    )
                    return

        # Check if there's no need to re-install theme
        # This is done after the dependency check in case an inherited theme has an update or is missing two levels down
        if self.is_installed(theme_name) and not self.has_update(
            theme_name
        ):  # Theme is installed by manager, and is up-to-date
            if force_install:
                PchumLog.warning(
                    "Theme %s is already installed, and no update is available. Installing anyways, because force_install is True",
                    theme_name,
                )
            else:
                self._error(
                    "Theme %s is already installed, and no update is available. Cancelling install"
                    % theme_name
                )
                return

        # All is ok. or we're just ignoring the errors through force_install
        # No matter. downloading time
        self._download_theme(theme_name)

    def has_update(self, theme_name):
        # Has the given theme an update available
        # Returns False if the theme is installed manually or when the theme is up to date
        if self.is_installed(theme_name) and theme_name in self.database_entries:
            return (
                self.manifest["entries"][theme_name]["version"]
                < self.database_entries[theme_name]["version"]
            )
        return False

    def is_installed(self, theme_name):
        # checks if a theme is installed through the manager
        # Note that this will return False if the given name is a theme that the user installed manually!
        return theme_name in self.manifest.get("entries", {})

    def is_database_valid(self):
        return (
            "entries" in self.database
            and isinstance(self.database.get("entries"), list)
            and self.SUPPORTED_VERSION
            == self.database.get("meta", {}).get("format_version", -1)
        )

    def _on_database_reply(self, reply):
        # This is a database refresh!

        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            self._error(
                "An error occured contacting the repository: %s" % reply.error()
            )
            return

        try:
            as_json = bytes(reply.readAll()).decode("utf-8")
            self.database = json.loads(as_json)
            self.database_entries = {}

            version = self.database.get("meta", {}).get("format_version")

            if version != self.SUPPORTED_VERSION:
                if version is None:
                    self._error(
                        "Theme database is malformed! No format version specified."
                    )
                elif version > self.SUPPORTED_VERSION:
                    self._error(
                        f"Theme database version is too new! (got v{version} instead of supported v{self.SUPPORTED_VERSION}). Try checking if there is a new client update available!"
                    )
                else:
                    self._error(
                        f"Theme database version is too old! (got v{version} instead of supported v{self.SUPPORTED_VERSION})."
                    )
                self.database = {}
                self.database_entries = {}
                return

            if not self.is_database_valid():
                self._error('Incorrect database format, missing "entries"')
                self.database = {}
                self.database_entries = {}
                return

            # Makes an easy name:theme lookup table instead of the array we get from the DB
            for idx, item in enumerate(self.database["entries"]):
                # Iterate over all the themes in the database
                if item["client"] == "pesterchum":
                    # Only add it to database_entries if the theme is for this client
                    # Store the index in the dict to make it easier to reference
                    item["id"] = idx
                    self.database_entries[item["name"]] = item

            PchumLog.info("Database refreshed")
            self.database_refreshed.emit(self.database)
        except KeyError as e:
            self.database = {}
            self.database_entries = {}
            self._error("Vital key missing from theme database: %s" % e)
        except json.decoder.JSONDecodeError as e:
            self.database = {}
            self.database_entries = {}
            self._error("Could not decode theme database JSON: %s" % e)

    def _on_theme_reply(self, reply, metadata):
        # This is called when a theme .zip is downloaded
        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            self._error(
                "An error occured contacting the repository: %s" % reply.error()
            )
            return

        buffer = bytes(reply.readAll())
        # Verify hash
        PchumLog.info("Verifying hash")
        hash = sha256_bytes(buffer)
        if hash != metadata.get("sha256_download"):
            self._error(
                "Download hash does not match! calculated %s, but expected %s"
                % (hash, str(metadata.get("sha256_download")))
            )
            return

        # Install the theme
        self._unzip_buffer(buffer, metadata["name"])
        self.manifest["entries"][metadata["name"]] = metadata
        self.save_manifest()
        self.manifest_updated.emit(self.manifest)
        PchumLog.info("Theme %s is now installed", metadata.get("name"))

    def _unzip_buffer(self, zip_buffer, theme_name):
        # Unzips the downloaded theme zip in-memory & writes to datadir/themes/theme_name
        #
        # ~lisanne
        # This runs on the MAIN THREAD so it may freeze for a second
        # I attempted to use a QThread but that made everything excruciatingly slow. maybe i didnt implement it right though
        # Could be revisited in the future
        directory = os.path.join(getDataDir(), "themes", theme_name)
        with zipfile.ZipFile(io.BytesIO(zip_buffer)) as z:
            if os.path.exists(directory):
                rmtree(directory)
                # Deletes old files that may have been removed in an update
            os.mkdir(directory)
            z.extractall(directory)


class ThemeListItem(QtWidgets.QTreeWidgetItem):
    name = ""
    installed_state = False
    author = ""
    updated_at = 0
    state_icon = None
    theme_icon = None

    index = 0

    def __init__(
        self, installed_state, name, author, updated_at, theme_icon, state_icon, index
    ):
        self.name = name
        self.installed_state = installed_state
        self.author = author
        self.updated_at = updated_at

        self.index = index
        QtWidgets.QTreeWidgetItem.__init__(
            self,
            [
                installed_state,
                name,
                author,
                datetime.fromtimestamp(updated_at).strftime("%d/%m/%Y %H:%M"),
            ],
        )
        self.setIcon(0, state_icon)
        if theme_icon is not None:
            self.setIcon(1, theme_icon)

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        if column == 3:
            # "Updated at" column → sort by timestamp instead of string because its in DD/MM/YYYY format and thus incorrect
            return self.updated_at < other.updated_at
        if (self.text(column)).isdigit() and (other.text(column)).isdigit():
            return int(self.text(column)) < int(other.text(column))
        return self.text(column) < other.text(column)


class ThemeManagerWidget(QtWidgets.QWidget):
    state_icons = None
    theme_icons = {}
    config = None
    theme = None

    rebuilt = QtCore.pyqtSignal()

    def __init__(self, config, theme, parent=None):
        super().__init__(parent)
        self.state_icons = [
            QtGui.QIcon("img/download_pending.png"),
            QtGui.QIcon("img/download_done.png"),
            QtGui.QIcon("img/download_update.png"),
        ]
        self.config = config
        self.theme = theme

        global themeManager
        if themeManager is None or not themeManager.is_database_valid():
            themeManager = ThemeManager(config)
            self.setupUI()
        else:
            self.setupUI()
            self.rebuild()
        themeManager.database_refreshed.connect(self._on_database_refreshed)
        themeManager.manifest_updated.connect(self._on_database_refreshed)

    def updateTheme(self, theme):
        self.theme = theme
        self._check_icons()

    def setupUI(self):
        self.layout_main = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout_main)

        # Search bar
        # TODO?: implement searching
        # (future ~lisanne: i dont think this is necessary
        # now that you can sort each column and search by hitting the first character key )

        # Main layout
        # [ list of themes/results ] | [ selected theme details ]
        # [ list of themes/results ] | [  (install) / (delete)  ]
        # [                      (refresh)                      ]
        layout_hbox_list_and_details = QtWidgets.QHBoxLayout()
        # This is the list of database themes
        self.list_results = QtWidgets.QTreeWidget()
        self.list_results.setColumnCount(4)
        self.list_results.setIndentation(0)
        self.list_results.setSortingEnabled(True)
        self.list_results.setHeaderLabels(["Installed", "Name", "Author", "Updated at"])
        self.list_results.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.list_results.itemSelectionChanged.connect(self._on_theme_selected)
        layout_hbox_list_and_details.addWidget(self.list_results)

        # This is the right side, has the install buttons & all the theme details of the selected item
        layout_vbox_details = QtWidgets.QVBoxLayout()
        # The theme details are inside a scroll container in case of small window
        self.frame_scroll = QtWidgets.QScrollArea()
        self.frame_scroll.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        # The vbox that the detail labels will rest in
        layout_vbox_scroll_insides = QtWidgets.QVBoxLayout()

        self.img_theme_icon = QtWidgets.QLabel()
        layout_vbox_scroll_insides.addWidget(self.img_theme_icon)
        # here starts the actual detail labels
        # Selected theme's name
        self.lbl_theme_name = QtWidgets.QLabel("Select a theme to get started")
        self.lbl_theme_name.setTextInteractionFlags(_flag_selectable)
        self.lbl_theme_name.setStyleSheet(
            "QLabel { font-size: 16px; font-weight:bold;}"
        )
        self.lbl_theme_name.setWordWrap(True)
        layout_vbox_scroll_insides.addWidget(self.lbl_theme_name)

        # Author name
        self.lbl_author_name = QtWidgets.QLabel("")
        self.lbl_author_name.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_author_name)

        # description. this needs to be the biggest
        self.lbl_description = QtWidgets.QLabel("")
        self.lbl_description.setTextInteractionFlags(_flag_selectable)
        self.lbl_description.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
        )
        self.lbl_description.setAlignment(_flag_topalign)
        self.lbl_description.setWordWrap(True)
        layout_vbox_scroll_insides.addWidget(self.lbl_description)

        # Line between description and the "requires" string. Only shown when the label is
        self.info_line_requires = QtWidgets.QFrame()
        self.info_line_requires.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.info_line_requires.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.info_line_requires.setHidden(True)
        layout_vbox_scroll_insides.addWidget(self.info_line_requires)

        # requires. shows up if a theme has "inherits" set
        self.lbl_requires = QtWidgets.QLabel("")
        self.lbl_requires.setTextInteractionFlags(_flag_selectable)
        self.lbl_requires.setWordWrap(True)
        layout_vbox_scroll_insides.addWidget(self.lbl_requires)

        # fix button. shows up if a theme has "inherits" set & we dont have it installed AND it is available on the repo
        self.btn_fix_requires = QtWidgets.QPushButton("Fix it!!!")
        self.btn_fix_requires.setHidden(True)
        self.btn_fix_requires.clicked.connect(self._on_fix_requires_clicked)
        layout_vbox_scroll_insides.addWidget(self.btn_fix_requires)

        # Line between the descripton/requires string. shown when theme is selected
        self.info_line = QtWidgets.QFrame()
        self.info_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.info_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout_vbox_scroll_insides.addWidget(self.info_line)
        self.info_line.setHidden(True)

        # Version number. this will also show the current installed one if there is an update
        self.lbl_version = QtWidgets.QLabel("")
        self.lbl_version.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_version)

        # Last update time
        self.lbl_last_update = QtWidgets.QLabel("")
        self.lbl_last_update.setWordWrap(True)
        self.lbl_last_update.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_last_update)

        # Theme details done, so we wont need the scroll after this
        self.frame_scroll.setLayout(layout_vbox_scroll_insides)
        layout_vbox_details.addWidget(self.frame_scroll)
        # Install/uninstall buttons
        # "Uninstall" button. Only visisble when the selected thene is installed
        self.btn_uninstall = QtWidgets.QPushButton("Uninstall", self)
        self.btn_uninstall.setHidden(True)
        self.btn_uninstall.clicked.connect(self._on_uninstall_clicked)
        layout_vbox_details.addWidget(self.btn_uninstall)
        # "Install" button. can also say "Update" if an update is availible
        # Only visible when not installed or if theres an update
        self.btn_install = QtWidgets.QPushButton("Install", self)
        self.btn_install.clicked.connect(self._on_install_clicked)
        self.btn_install.setDisabled(True)
        layout_vbox_details.addWidget(self.btn_install)

        # Done with details
        layout_hbox_list_and_details.addLayout(layout_vbox_details)
        self.layout_main.addLayout(layout_hbox_list_and_details)

        # Bottom buttons layout
        layout_hbox_bottom_buttons = QtWidgets.QHBoxLayout()
        # Refresh database button
        self.btn_refresh = QtWidgets.QPushButton("Refresh", self)
        self.btn_refresh.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.btn_refresh.clicked.connect(
            themeManager.refresh_database
        )  # Connected to themeManager!
        # Submit theme button (just opens the browser page as is defined in the database)
        self.btn_submit_theme = QtWidgets.QPushButton("Submit your own themes", self)
        self.btn_submit_theme.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.btn_submit_theme.setMinimumWidth(242)
        self.btn_submit_theme.setHidden(True)
        self.btn_submit_theme.clicked.connect(self.openSubmissionPage)

        layout_hbox_bottom_buttons.addWidget(self.btn_refresh)
        layout_hbox_bottom_buttons.addWidget(self.btn_submit_theme)
        self.layout_main.addLayout(layout_hbox_bottom_buttons)

        self.lbl_error = QtWidgets.QLabel("")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        themeManager.errored.connect(self._on_fetch_error)
        self.lbl_error.setTextInteractionFlags(_flag_selectable)
        self.lbl_error.setStyleSheet(
            " QLabel { background-color:black; color:red; font-size: 16px;}"
        )
        self.layout_main.addWidget(self.lbl_error)

    def openSubmissionPage(self):
        url = themeManager.database.get("meta", {}).get("submission_page", "")
        if url == "":
            return
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                url,
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )

    def _on_fetch_error(self, text):
        self.lbl_error.setText(text)
        self.lbl_error.setVisible(True)

    def _on_uninstall_clicked(self):
        theme_name = self.list_results.selectedItems()[0].name
        inheriting_themes = themeManager.get_inheriting_themes(
            theme_name, only_installed=True
        )

        if len(inheriting_themes) == 0:
            # No installed themes depend on this one, so its safe to delete
            themeManager.delete_theme(theme_name, cascade_delete=True)
        else:
            # One or more installed themes depend on this one, so ask the user what to do
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText(
                "Uninstalling '%s' will break the following other themes: \n\n"
                % theme_name
                + "%s\n\n" % "\n".join([" • " + x for x in inheriting_themes])
                + "It is recommended to also uninstall these, as they likely wont work correctly anymore.\n"
                + "How would you like to proceed?"
            )
            btn_delete_all = QtWidgets.QPushButton("Uninstall all (recommended)")
            btn_delete_one = QtWidgets.QPushButton("Uninstall only '%s'" % theme_name)
            btn_cancel = QtWidgets.QPushButton("Cancel")

            msgbox.addButton(
                btn_delete_all, QtWidgets.QMessageBox.ButtonRole.AcceptRole
            )
            msgbox.addButton(btn_delete_one, QtWidgets.QMessageBox.ButtonRole.YesRole)
            msgbox.addButton(btn_cancel, QtWidgets.QMessageBox.ButtonRole.RejectRole)

            def _on_buttonClicked(button):
                if button == btn_delete_all:
                    themeManager.delete_theme(theme_name, cascade_delete=True)
                elif button == btn_delete_one:
                    themeManager.delete_theme(theme_name, cascade_delete=False)

            msgbox.buttonClicked.connect(_on_buttonClicked)
            msgbox.exec()

    def _on_install_clicked(self):
        # Install button is clicked. wahoo
        themeManager.install_theme(self.list_results.selectedItems()[0].name)

    def _on_fix_requires_clicked(self):
        # Rare scenario where a theme has been downloaded but it inherits from a theme we dont have downloaded
        # and that inherited theme IS available on the theme repo
        # All this does is just do an install of that missing theme
        theme_name = self.list_results.selectedItems()[0].name
        if theme_name not in themeManager.database_entries:
            PchumLog.error("No such theme in database: %s", theme_name)
            return
        inherits = themeManager.database_entries[theme_name].get("inherits")
        if inherits == "":
            PchumLog.error("Theres no inherit (== '') to install. lol.")
            return
        themeManager.install_theme(inherits)

    def _on_theme_selected(self):
        # Triggers when a theme in the list is selected (mouse click or keyboard arrows)
        # Sets the correct info on the info panel next to the list
        selected_item = self.list_results.selectedItems()
        if len(selected_item) == 0:
            self._deselect()
            # Early return if there wasnt anything selected after all
            return
        else:
            selected_item = selected_item[0]
        theme_name = selected_item.name

        # Some shortcuts to make this block less verbose
        theme = themeManager.database_entries[theme_name]
        is_installed = themeManager.is_installed(theme_name)
        has_update = themeManager.has_update(theme_name)

        # Show the proper button (update|install / delete)
        self.btn_install.setDisabled(False)
        self.btn_install.setText("Update" if has_update else "Install")
        self.btn_install.setVisible((is_installed and has_update) or not is_installed)
        self.btn_uninstall.setVisible(themeManager.is_installed(theme_name))

        # Show the icon above the name
        self.img_theme_icon.setPixmap(self.get_theme_icon(theme_name).pixmap(32, 32))
        # Show the name / author / description text
        self.lbl_theme_name.setText(theme_name)
        self.lbl_author_name.setText("By %s" % theme["author"])
        self.lbl_description.setText(theme["description"])
        # Unhide that funky seperator line
        self.info_line.setHidden(False)

        # Show the current version & sometimes the new update version
        version_text = "Version %s" % theme["version"]
        if has_update:
            version_text += (
                " (installed: %s)"
                % themeManager.manifest["entries"][theme_name]["version"]
            )
        self.lbl_version.setText(version_text)

        # Show which theme this one inherits from (if applicable)
        # (And show a warning if that theme is missing)
        self.btn_fix_requires.setHidden(True)
        requires_text = ""
        if theme["inherits"]:
            self.lbl_requires.setStyleSheet("")
            requires_text = "Requires %s" % theme["inherits"]
            if themeManager.is_installed(theme_name):
                if theme["inherits"] in self.config.availableThemes():
                    requires_text += " (installed)"
                else:
                    requires_text += " (missing)"
                    self.lbl_requires.setStyleSheet(" QLabel { color: red; }")
                    self.btn_fix_requires.setHidden(False)
        self.lbl_requires.setText(requires_text)
        self.lbl_requires.setHidden(requires_text == "")
        self.info_line_requires.setHidden(requires_text == "")

        last_update_text = "Last update: "
        last_update_text += datetime.fromtimestamp(theme["updated_at"]).strftime(
            "%d/%m/%Y %H:%M"
        )
        self.lbl_last_update.setText(last_update_text)

    @QtCore.pyqtSlot(dict)
    def _on_database_refreshed(self, _):
        self._check_icons()
        self.rebuild()

    def _check_icons(self):
        def make_lambda(callable, *args, **kwargs):
            # Did you know using a lambda in a for loop is a nightmare
            return lambda: callable(*args, **kwargs)

        for item in themeManager.database_entries.values():
            if item["icon"] != "" and item["name"] not in self.theme_icons:
                reply = get_request(item["icon"])
                # Using a lambda directly here would make it only ever use the last loop's variables
                # Because apparently python lambdas suck badly. big L
                reply.theme_name = item["name"]
                reply.finished.connect(
                    make_lambda(self._on_icon_reply, reply, item["name"])
                )

    def get_theme_icon(self, theme_name):
        if theme_name in self.theme_icons:
            return self.theme_icons[theme_name]

        if self.theme.name not in self.theme_icons:
            self.theme_icons[self.theme.name] = QtGui.QIcon(self.theme["main/icon"])
        default_icon = self.theme_icons[self.theme.name]

        if not theme_name in themeManager.database_entries:
            return default_icon
        inherits = themeManager.database_entries[theme_name]["inherits"]

        if inherits in ("pesterchum", ""):
            return default_icon
        return self.get_theme_icon(inherits)

    def _on_icon_reply(self, reply, theme_name):
        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            PchumLog.error(
                "Could not fetch theme icon for %s at %s: %s",
                theme_name,
                reply.request().url().url(),
                reply.error(),
            )
            return
        PchumLog.debug(
            "Fetched theme %s's icon @%s", theme_name, reply.request().url().url()
        )
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(reply.readAll())
        icon = QtGui.QIcon(pixmap)

        self.theme_icons[theme_name] = icon
        for item in self.list_results.findItems(theme_name, _flag_search_exact, 1):
            if item.name == theme_name:
                item.setIcon(1, icon)
        self._check_icons()

    def _deselect(self):
        # Clears the info panel of values
        self.btn_install.setDisabled(True)
        for lbl in [
            self.lbl_author_name,
            self.lbl_description,
            self.lbl_version,
            self.lbl_requires,
            self.lbl_last_update,
        ]:
            lbl.setText("")
        self.lbl_theme_name.setText("Select a theme to get started")
        self.btn_uninstall.setVisible(False)
        self.btn_install.setVisible(True)
        self.btn_install.setDisabled(True)
        self.info_line.setHidden(True)
        self.info_line_requires.setHidden(True)
        self.btn_fix_requires.setHidden(True)

    def rebuild(self):
        prev_selected_item = self.list_results.selectedItems()
        prev_selected_item = (
            prev_selected_item[0].name if len(prev_selected_item) > 0 else None
        )
        self.list_results.clear()
        self.lbl_error.setText("")
        self.lbl_error.setVisible(False)

        if not themeManager.is_database_valid():
            self.lbl_error.setText("")
            self.lbl_error.setVisible(True)

        # Repopulate the list
        for dbitem in themeManager.database_entries.values():
            is_installed = themeManager.is_installed(dbitem["name"])
            has_update = themeManager.has_update(dbitem["name"])

            treeitem = ThemeListItem(
                ["No", "Yes", "Update available"][int(is_installed) + int(has_update)],
                dbitem["name"],
                dbitem["author"],
                dbitem["updated_at"],
                self.get_theme_icon(dbitem["name"]),
                self.state_icons[int(is_installed) + int(has_update)],
                dbitem["id"],
            )
            self.list_results.addTopLevelItem(treeitem)
            # Re-select last item, if it was selected
            if dbitem["name"] == prev_selected_item:
                self.list_results.setCurrentItem(treeitem)

        if prev_selected_item is not None:
            self._on_theme_selected()
        else:
            # Return sidebar info panel to defaults if nothing was selected
            self._deselect()

        self.btn_submit_theme.setHidden(
            themeManager.database.get("meta", {}).get("submission_page", "") == ""
        )

        self.rebuilt.emit()
        PchumLog.debug("Rebuilt emitted")
