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
from generic import RightClickTree

try:
    from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork
    from PyQt6.QtGui import QAction

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

    _flag_selectable = QtCore.Qt.TextSelectableByMouse
    _flag_topalign = QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop


PchumLog = logging.getLogger("pchumLogger")
themeManager = None


# ~Lisanne
# This file has all the stuff needed to use a theme repository
# - ThemeManagerWidget, a GUI widget that lets the user install, update, & delete repository themes
# - ThemeManager, the class that the widget hooks up to. Handles fetching, downloading, installing, & keeps the manifest updated

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
    database = {}  # The latest database data downloaded in full
    database_entries = {}

    config = None
    manifest_path = os.path.join(getDataDir(), "manifest.json")

    network_manager = None  # Does the requests

    SUPPORTED_VERSION = 4  # theme format version supported

    def __init__(self, config):
        super().__init__()
        with open(self.manifest_path, "r") as f:
            self.manifest = json.load(f)
        PchumLog.debug("manifest.json loaded with: %s", self.manifest)
        self.config = config
        # TODO: maybe make seperate QNetworkAccessManagers for theme downloads, database fetches, and integrity checkfile
        # OR figure out how to connect the signal to tasks instead of the whole object
        # That way we dont have to figure out what got downloaded afterwards, and can just have a _on_reply_theme & _on_reply_database or something
        self.network_manager = QtNetwork.QNetworkAccessManager()
        self.validate_manifest()
        self.refresh_database()

    @QtCore.pyqtSlot()
    def refresh_database(self):
        # Fetches a new copy of the theme database from the given URL
        # The initialisation & processing of it is handled in self._on_database_reply
        if self.config.theme_repo_url().strip() == "":
            self._error("No theme repository db URL has been set in the Idle/Updates settings.")
            return

        PchumLog.debug(
            "Refreshing theme repo database @ %s", self.config.theme_repo_url()
        )
        reply = self.network_manager.get(
            QtNetwork.QNetworkRequest(QtCore.QUrl(self.config.theme_repo_url()))
        )
        reply.finished.connect(lambda: self._on_database_reply(reply))

    def delete_theme(self, theme_name):
        # TODO: check if other installed themes inherit from this to avoid broken themes
        # would require some kinda confirmation popup which i havent figure out yet
        PchumLog.info("Deleting installed repo theme %s", theme_name)
        theme = self.manifest['entries'][theme_name]
        directory = os.path.join(getDataDir(), "themes", theme["name"])
        if os.path.isdir(directory):
            rmtree(directory)
        self.manifest['entries'].pop(theme_name)
        self.save_manifest()
        self.manifest_updated.emit(self.manifest)

    def save_manifest(self):
        # Writes manifest.json to datadir
        self.manifest['meta'] = self.manifest.get('meta',{})
        self.manifest["meta"]['updated_at'] = time.time()
        self.manifest['meta']['format_version'] = self.database.get('meta',{}).get('format_version', self.SUPPORTED_VERSION)
        self.manifest['entries'] = self.manifest.get('entries', {})
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f)
        PchumLog.debug("Saved manifes.js to %s", self.manifest_path)

    def validate_manifest(self):
        # Checks if the themes the manifest claims are installed actually exists & does some structure validation
        # Removes them from the manifest if they dont
        if not "meta" in self.manifest:
            self.manifest["meta"] = {}
        if not "updated_at" in self.manifest['meta']:
            self.manifest['meta']["updated_at"] = time.time()
        if not "format_version" in self.manifest['meta']:
            self.manifest['meta']["format_version"] =  self.SUPPORTED_VERSION
        if not "entries" in self.manifest:
            self.manifest['entries'] = {}

        if self.manifest['meta']['format_version'] != self.SUPPORTED_VERSION:
            PchumLog.warning(
                "Existing manifest version (%s) does not match supported version (%s). Was the client updated?",
                self.manifest['meta']['format_version'],
                self.SUPPORTED_VERSION,
            )
        to_pop = set()
        all_themes = self.config.availableThemes()
        for theme_name in self.manifest['entries']:
            if not theme_name in all_themes:
                PchumLog.warning(
                    "Supposedly installed theme %s from the manifest seems to have been deleted, removing from manifest now",
                    theme_name,
                )
                # Cannot be popped while iterating!
                to_pop.add(theme_name)

        for theme_name in to_pop:
            self.manifest['entries'].pop(theme_name)

    def download_theme(self, theme_name):
        # Downloads the theme .zip
        # The actual installing is handled by _on_theme_reply when the theme is downloaded
        # Performs no version checks or dependency handling
        # Use install_theme() instead unless you know what you're doing
        PchumLog.info("Downloading %s", theme_name)
        if not theme_name in self.database_entries:
            PchumLog.error("Theme name %s does not exist in the database!", theme_name)
            return
        PchumLog.debug("(From %s)", self.database_entries[theme_name]["download"])
        reply = self.network_manager.get(
            QtNetwork.QNetworkRequest(
                QtCore.QUrl(self.database_entries[theme_name]["download"])
            )
        )
        reply.finished.connect(lambda : self._on_theme_reply(reply, self.database_entries[theme_name]))

    def _error(self, msg):
        PchumLog.error("ThemeManager: %s", msg)
        self.errored.emit(msg)

    def install_theme(self, theme_name, force_install=False):
        # A higher way to install a theme than download_theme
        # Checks if the theme is already installed & if its up to date
        # Also recursively handled dependencies, which download_theme does not
        # !! note that this does not check if theres a circular dependency !!
        # Setting force_install to True will install a given theme, even if it is deemed unnecessary to do so or its inherit dependency cannot be installed
        # This gives it the same no-nonsense operation as download_theme, but with the checks in place
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
        self.download_theme(theme_name)

    def has_update(self, theme_name):
        # Has the given theme an update available
        # Returns False if the theme is installed manually or when the theme is up to date
        if self.is_installed(theme_name) and theme_name in self.database_entries:
            return (
                self.manifest['entries'][theme_name]["version"]
                < self.database_entries[theme_name]["version"]
            )
        return False

    def is_installed(self, theme_name):
        # checks if a theme is installed through the manager
        # Note that this will return False if the given name is a theme that the user installed manually!
        return theme_name in self.manifest.get('entries',{})

    def is_database_valid(self):
        return "entries" in self.database and isinstance(
            self.database.get("entries"), list
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
                if version == None:
                    self._error(
                        "Theme database is malformed! No format version specified."
                    )
                elif version > self.SUPPORTED_VERSION:
                    self._error(
                        f"Theme database is too new! (got v{version} instead of supported v{self.SUPPORTED_VERSION}). Try checking if there is a new client update available!"
                    )
                else:
                    self._error(
                        f"Theme database is too old! (got v{version} instead of supported v{self.SUPPORTED_VERSION})."
                    )
                self.database = {}
                self.database_entries = {}
                return

            if not self.is_database_valid():
                self._error('Incorrect database format, missing "entries"')
                self.database = {}
                self.database_entries = {}
                return

            # Filter out non-QTchum client themes, like for godot
            for dbindex in range(
                len(self.database["entries"]) - 1, -1, -1
            ):  # Iterate over the database in reverse
                dbitem = self.database["entries"][dbindex]
                if dbitem["client"] != "pesterchum":
                    # PchumLog.debug(
                    #     "Removed database theme %s because it is not compatible with this client",
                    #     dbitem["name"],
                    # )
                    # self.database["entries"].pop(dbindex)
                    pass # TODO: rethink this
                else:
                    # Store the index in the dict to make it easier to reference
                    dbitem["id"] = dbindex
                    # Make an easy lookup table instead of the array we get from the DB
                    self.database_entries[dbitem["name"]] = dbitem
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
        reply.deleteLater()

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
            self._error("Download hash does not match! calculated %s, but expected %s" % (hash, str(metadata.get("sha256_download"))))
            return

        # Install the theme
        self._unzip_buffer(buffer, metadata["name"])
        self.manifest['entries'][metadata["name"]] = metadata
        self.save_manifest()
        self.manifest_updated.emit(self.manifest)
        PchumLog.info("Theme %s is now installed", metadata.get("name"))
        reply.deleteLater()

    # using a slot decorator here raises `ERROR - <class 'TypeError'>, connect() failed between finished(QNetworkReply*) and _on_reply()``
    # maybe because of the underscore?
    # @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def _on_reply(self, reply):
        pass

    def _unzip_buffer(self, zip_buffer, theme_name):
        # Unzips the downloaded theme zip in-memory & writes to datadir/themes/theme_name
        # TODO: QThread this
        directory = os.path.join(getDataDir(), "themes", theme_name)
        with zipfile.ZipFile(io.BytesIO(zip_buffer)) as z:
            if os.path.exists(directory):
                rmtree(directory)
                # Deletes old files that may have been removed in an update
            os.mkdir(directory)
            z.extractall(directory)






class ThemeListItem(QtWidgets.QTreeWidgetItem):
    name = ""
    installed = False
    author = ""
    updated_at = 0

    has_update = False
    index = 0
    def __init__(self, installed, name, author, updated_at, has_update, index):
        self.name = name,
        self.installed = installed,
        self.author = author,
        self.updated_at = updated_at

        self.has_update = has_update
        self.index = index
        QtWidgets.QTreeWidgetItem.__init__(self, ["yes" if installed else "no", name, author, str(updated_at)])

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        if (self.text(column)).isdigit() and (other.text(column)).isdigit():
            return int(self.text(column)) < int(other.text(column))
        return self.text(column) < other.text(column)

class ThemeManagerWidget(QtWidgets.QWidget):
    icons = None
    config = None

    rebuilt = QtCore.pyqtSignal()

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.icons = [
            QtGui.QIcon("img/download_pending.png"),
            QtGui.QIcon("img/download_done.png"),
            QtGui.QIcon("img/download_update.png"),
        ]
        self.config = config
        global themeManager
        if themeManager is None or not themeManager.is_database_valid():
            themeManager = ThemeManager(config)
            self.setupUI()
        else:
            self.setupUI()
            self.rebuild()
        themeManager.database_refreshed.connect(self._on_database_refreshed)
        themeManager.manifest_updated.connect(self._on_database_refreshed)

    def setupUI(self):
        self.layout_main = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout_main)

        # Search bar
        # TODO: implement searching
        # self.line_search = QtWidgets.QLineEdit()
        # self.line_search.setPlaceholderText("Search for themes")
        # self.layout_main.addWidget(self.line_search)

        # Main layout
        # [list of themes/results] | [selected theme details]
        layout_hbox_list_and_details = QtWidgets.QHBoxLayout()
        # This is the list of database themes
        self.list_results = RightClickTree()
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

        # here starts the actual detail labels
        # Selected theme's name
        self.lbl_theme_name = QtWidgets.QLabel("Click a theme to get started")
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

        # requires. shows up if a theme has "inherits" set & we dont have it installed
        self.lbl_requires = QtWidgets.QLabel("")
        self.lbl_requires.setTextInteractionFlags(_flag_selectable)
        self.lbl_requires.setWordWrap(True)
        layout_vbox_scroll_insides.addWidget(self.lbl_requires)

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
        # Insta//uninstall buttons
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

        self.btn_refresh = QtWidgets.QPushButton("Refresh", self)
        self.btn_refresh.clicked.connect(
            themeManager.refresh_database
        )  # Conneced to themeManager!
        self.layout_main.addWidget(self.btn_refresh)

        self.lbl_error = QtWidgets.QLabel("")
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        themeManager.errored.connect(self._on_fetch_error)
        self.lbl_error.setTextInteractionFlags(_flag_selectable)
        self.lbl_error.setStyleSheet(
            " QLabel { background-color:black; color:red; font-size: 16px;}"
        )
        self.layout_main.addWidget(self.lbl_error)

    def _on_fetch_error(self, text):
        self.lbl_error.setText(text)
        self.lbl_error.setVisible(True)

    def _on_uninstall_clicked(self):
        theme = themeManager.database["entries"][self.list_results.currentRow()]
        themeManager.delete_theme(theme["name"])

    def _on_install_clicked(self):
        theme = themeManager.database["entries"][self.list_results.currentRow()]
        themeManager.install_theme(theme["name"])

    @QtCore.pyqtSlot()
    def _on_theme_selected(self):
        index = self.list_results.currentRow()
        theme = themeManager.database["entries"][index]
        theme_name = theme["name"]
        is_installed = themeManager.is_installed(theme_name)
        has_update = themeManager.has_update(theme_name)
        self.btn_install.setDisabled(False)
        self.btn_install.setText("Update" if has_update else "Install")
        self.btn_install.setVisible((is_installed and has_update) or not is_installed)
        self.btn_uninstall.setVisible(themeManager.is_installed(theme_name))

        self.lbl_theme_name.setText(theme_name)
        self.lbl_author_name.setText("By %s" % theme["author"])
        self.lbl_description.setText(theme["description"])
        version_text = "Version %s" % theme["version"]
        if has_update:
            version_text += (
                " (installed: %s)" % themeManager.manifest[theme_name]["version"]
            )
        self.lbl_version.setText(version_text)
        requires_text = ""
        if theme["inherits"]:
            requires_text += "Requires %s" % theme["inherits"]
        if theme["inherits"] in self.config.availableThemes():
            requires_text += " (installed)"
        self.lbl_requires.setText((requires_text) if theme["inherits"] else "")
        last_update_text = "Latest update: "
        last_update_text += datetime.fromtimestamp(theme["updated_at"]).strftime(
            "%d/%m/%Y, %H:%M"
        )
        self.lbl_last_update.setText(last_update_text)

    @QtCore.pyqtSlot(dict)
    def _on_database_refreshed(self, _):
        self.rebuild()

    def rebuild(self):
        prev_selected_items = self.list_results.selectedItems()
        database = themeManager.database
        self.list_results.clear()
        self.lbl_error.setText("")
        self.lbl_error.setVisible(False)

        if not themeManager.is_database_valid():
            self.lbl_error.setText("")
            self.lbl_error.setVisible(True)

        # Repopulate the list
        for dbitem in database["entries"]:
            # Determine the suffix

            # icon = self.icons[0]
            # status = ""
            # if themeManager.is_installed(dbitem["name"]):
            #     if themeManager.has_update(dbitem["name"]):
            #         status = "~ (update available)"
            #         icon = self.icons[2]
            #     else:
            #         status = "~ (installed)"
            #         icon = self.icons[1]
            # text = "%s by %s %s" % (dbitem["name"], dbitem["author"], status)
            item = ThemeListItem(
                themeManager.is_installed(dbitem["name"]),
                dbitem['name'],
                dbitem['author'],
                dbitem['updated_at'],
                themeManager.has_update(dbitem["name"]),
                dbitem['id']
                )
            self.list_results.addTopLevelItem(item)

        if len(prev_selected_items) > 0:
            print(prev_selected_items)
            # Re-select last item, if it was selected
            self.list_results.setCurrentRow(prev_selected_index)
            self._on_theme_selected()
        else:
            # Return sidebar info panel to defaults if nothing was selected
            self.btn_install.setDisabled(True)
            for lbl in [
                self.lbl_author_name,
                self.lbl_description,
                self.lbl_version,
                self.lbl_requires,
                self.lbl_last_update,
            ]:
                lbl.setText("")
            self.lbl_theme_name.setText("Click a theme to get started")
            self.btn_uninstall.setVisible(False)
            self.btn_install.setVisible(True)
            self.btn_install.setDisabled(True)

        self.rebuilt.emit()
        PchumLog.debug("Rebuilt emitted")
