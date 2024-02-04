import os
import io
import json
import zipfile
import logging
from shutil import rmtree
from datetime import datetime

from ostools import getDataDir

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

# Manifest is a local file that tracks the metadata of themes downloaded from the repository
# Its a themename: {database entry} dict


class ThemeManager(QtCore.QObject):
    # signals
    theme_installed = QtCore.pyqtSignal(str)  # theme name
    zip_downloaded = QtCore.pyqtSignal(str, str)  # theme name, zip location
    database_refreshed = QtCore.pyqtSignal(dict)  # self.manifest
    manifest_updated = QtCore.pyqtSignal(dict)  # self.manifest
    errored = QtCore.pyqtSignal(str)  # error_text

    # variables
    manifest = {}
    database = {}
    database_entries = {}
    config = None
    manifest_path = os.path.join(getDataDir(), "manifest.js")
    NAManager = None

    supported_version = 3

    downloads = {}

    def __init__(self, config):
        super().__init__()
        with open(self.manifest_path, "r") as f:
            self.manifest = json.load(f)
        PchumLog.debug("Manifest.js loaded with: %s", self.manifest)
        self.config = config
        # TODO: maybe make seperate QNetworkAccessManagers for theme downloads, database fetches, and integrity checkfile
        # OR figure out how to connect the signal to tasks instead of the whole object
        # That way we dont have to figure out what got downloaded afterwards, and can just have a _on_reply_theme & _on_reply_database or something
        self.NAManager = QtNetwork.QNetworkAccessManager()
        self.NAManager.finished[QtNetwork.QNetworkReply].connect(self._on_reply)
        self.validate_manifest()
        self.refresh_database()

    @QtCore.pyqtSlot()
    def refresh_database(self):
        # Fetches a new copy of the theme database from the given URL
        # The initialisation & processing of it is handled in self._on_reply
        PchumLog.debug(
            "Refreshing theme repo database @ %s", self.config.theme_repo_url()
        )
        promise = self.NAManager.get(
            QtNetwork.QNetworkRequest(QtCore.QUrl(self.config.theme_repo_url()))
        )

    def delete_theme(self, theme_name):
        # TODO: check if other installed themes inherit from this to avoid broken themes
        # would require some kinda confirmation popup which i havent figure out yet
        PchumLog.info("Deleting installed repo theme %s", theme_name)
        theme = self.manifest[theme_name]
        directory = os.path.join(getDataDir(), "themes", theme["name"])
        if os.path.isdir(directory):
            rmtree(directory)
        self.manifest.pop(theme_name)
        self.save_manifest()
        self.manifest_updated.emit(self.manifest)

    def save_manifest(self):
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f)
        PchumLog.debug("Saved manifes.js to %s", self.manifest_path)

    def validate_manifest(self):
        # Checks if the themes the manifest claims are installed actually exists
        # Removes them from the manifest if they dont
        to_pop = set()
        all_themes = self.config.availableThemes()
        for theme_name in self.manifest:
            if not theme_name in all_themes:
                PchumLog.warning(
                    "Supposedly installed theme %s from the manifest seems to have been deleted, removing from manifest now",
                    theme_name,
                )
                # Cannot be popped while iterating!
                to_pop.add(theme_name)

        for theme_name in to_pop:
            self.manifest.pop(theme_name)

    def download_theme(self, theme_name):
        # Downloads the theme .zip
        # The actual installing is handled by _on_reply when the theme is downloaded
        # Performs no version checks or dependency handling
        # Use install_theme() instead unless you know what you're doing
        PchumLog.info("Downloading %s", theme_name)
        if not theme_name in self.database_entries:
            PchumLog.error("Theme name %s does not exist in the database!", theme_name)
            return
        PchumLog.debug("(From %s)", self.database_entries[theme_name]["download"])
        promise = self.NAManager.get(
            QtNetwork.QNetworkRequest(
                QtCore.QUrl(self.database_entries[theme_name]["download"])
            )
        )
        self.downloads[
            self.database_entries[theme_name]["download"]
        ] = self.database_entries[theme_name]

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
            PchumLog.error("Theme %s does not exist in the database!", theme_name)
            self.errored.emit("Theme %s does not exist in the database!" % theme_name)
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
                    PchumLog.error(
                        "Theme %s requires theme %s, which is not installed and not in the database. Cancelling install",
                        theme_name,
                        theme["inherits"],
                    )
                    self.errored.emit(
                        "Theme %s requires theme %s, which is not installed and not in the database. Cancelling install"
                        % (theme_name, theme["inherits"])
                    )
                    return

        # Check if there's no need to re-install theme
        # This is done after the dependency check in case an inherited theme is missing two levels down
        if self.is_installed(theme_name) and not self.has_update(
            theme_name
        ):  # Theme is installed by manager, and is up-to-date
            if force_install:
                PchumLog.warning(
                    "Theme %s is already installed, and no update is available. Installing anyways, because force_install is True",
                    theme_name,
                )
            else:
                PchumLog.warning(
                    "Theme %s is already installed, and no update is available. Cancelling install",
                    theme_name,
                )
                self.errored.emit(
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
                self.manifest[theme_name]["version"]
                < self.database_entries[theme_name]["version"]
            )
        return False

    def is_installed(self, theme_name):
        # checks if a theme is installed through the manager
        # Note that this will return False if the given name is a theme that the user installed manually!
        return theme_name in self.manifest

    def is_database_valid(self):
        return "entries" in self.database and isinstance(
            self.database.get("entries"), list
        )

    # using a slot decorator here raises `ERROR - <class 'TypeError'>, connect() failed between finished(QNetworkReply*) and _on_reply()``
    # maybe because of the underscore?
    # @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def _on_reply(self, reply):
        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            PchumLog.error(
                "An error occured contacting the repository: %s", reply.error()
            )
            self.errored.emit(
                "An error occured contacting the repository: %s" % reply.error()
            )
            return
        try:
            original_url = reply.request().url().url()
            # Check if zipfile or database fetch
            if original_url in self.downloads:
                # This is a theme zip!
                theme = self.downloads[original_url]
                self._handle_downloaded_zip(bytes(reply.readAll()), theme["name"])
                self.downloads.pop(original_url)
                self.manifest[theme["name"]] = theme
                self.save_manifest()
                self.manifest_updated.emit(self.manifest)
                PchumLog.info("Theme %s is now installed", theme["name"])
            else:
                # This is a database refresh!
                as_json = bytes(reply.readAll()).decode("utf-8")
                self.database = json.loads(as_json)
                self.database_entries = {}

                version = self.database.get("meta", {}).get("format_version")

                if version != self.supported_version:
                    err = ""
                    if version > self.supported_version:
                        err = f"Theme database is too new! (got v{version} instead of supported v{self.supported_version}). Try checking if there is a new client update available!"
                    else:
                        err = f"Theme database is too old! (got v{version} instead of supported v{self.supported_version})."
                    PchumLog.error(err)
                    self.errored.emit(err)
                    self.database = {}
                    self.database_entries = {}
                    return

                if not self.is_database_valid():
                    self.database = {}
                    self.database_entries = {}
                    PchumLog.error('Incorrect database format, missing "entries"')
                    self.errored.emit('Incorrect database format, missing "entries"')
                    return

                # Filter out non-QTchum client themes, like for godot
                for dbindex in range(
                    len(self.database["entries"]) - 1, -1, -1
                ):  # Iterate over the database in reverse
                    dbitem = self.database["entries"][dbindex]
                    if dbitem["client"] != "pesterchum":
                        PchumLog.debug(
                            "Removed database theme %s because it is not compatible with this client",
                            dbitem["name"],
                        )
                        self.database["entries"].pop(dbindex)
                # Make an easy lookup table instead of the array we get from the DB
                for dbitem in self.database["entries"]:
                    self.database_entries[dbitem["name"]] = dbitem
                PchumLog.info("Database refreshed")
                self.database_refreshed.emit(self.database)

        except json.decoder.JSONDecodeError as e:
            PchumLog.error("Could not decode theme database JSON: %s", e)
            self.errored.emit("Could not decode theme database JSON: %s" % e)
            return
        except KeyError as e:
            self.database = {}
            self.database_entries = {}
            PchumLog.error("Vital key missing from theme database: %s", e)
            self.errored.emit("Vital key missing from theme database: %s" % e)
            return

    def _handle_downloaded_zip(self, zip_buffer, theme_name):
        # Unzips the downloaded theme package in-memory to datadir/themes/theme_name
        # I dont think this runs in a thread so it may block, but its so fast i dont think it really matters
        # But i guess if its a zip bomb itll crash
        directory = os.path.join(getDataDir(), "themes", theme_name)
        with zipfile.ZipFile(io.BytesIO(zip_buffer)) as z:
            if os.path.isdir(directory):
                rmtree(directory)
                # Deletes old files that have been removed in an update
            z.extractall(directory)


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
        self.list_results = QtWidgets.QListWidget()
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
        last_update_text = "Released on: "
        last_update_text += datetime.fromtimestamp(theme["updated"]).strftime(
            "%d/%m/%Y, %H:%M"
        )
        self.lbl_last_update.setText(last_update_text)

    @QtCore.pyqtSlot(dict)
    def _on_database_refreshed(self, _):
        self.rebuild()

    def rebuild(self):
        prev_selected_index = self.list_results.currentRow()
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
            icon = self.icons[0]
            status = ""
            if themeManager.is_installed(dbitem["name"]):
                if themeManager.has_update(dbitem["name"]):
                    status = "~ (update available)"
                    icon = self.icons[2]
                else:
                    status = "~ (installed)"
                    icon = self.icons[1]
            text = "%s by %s %s" % (dbitem["name"], dbitem["author"], status)
            item = QtWidgets.QListWidgetItem(icon, text)
            self.list_results.addItem(item)

        if prev_selected_index > -1:
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
