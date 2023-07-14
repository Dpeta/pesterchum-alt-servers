 
import logging
from os import remove

try:
    from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork
    from PyQt6.QtGui import QAction
    _flag_selectable = QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
    _flag_topalign = QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop
except ImportError:
    print("PyQt5 fallback (menus.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
    from PyQt5.QtWidgets import QAction
    _flag_selectable = QtCore.Qt.TextSelectableByMouse
    _flag_topalign = QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop

# ~Lisanne
# This file has all the stuff needed to use a theme repository
# - ThemeManagerWidget, a GUI widget that 
# - class for fetching & parsing database
# - class for handling installs & uninstalls. it also updates the manifest
# - manifest variable / json which keeps track of installed themes & their version

def unzip_file(path_zip, path_destination):
    pass

class ThemeManagerWidget(QtWidgets.QWidget):
    manifest = {}
    database = {}
    config = None
    promise = None
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setupUI()
        self.refresh()
    
    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def themeSelected(self, item):
        print("Done!")
        print(item)
        pass

    @QtCore.pyqtSlot(QtNetwork.QNetworkReply)
    def receiveReply(self, reply):
        print(reply)
        breakpoint
    
    @QtCore.pyqtSlot()
    def refresh(self):
        print("Starting refresh @ ",self.config.theme_repo_url())
        request = QtNetwork.QNetworkRequest()
        request.setUrl(QtCore.QUrl(self.config.theme_repo_url()))
        manager = QtNetwork.QNetworkAccessManager()
        promise = manager.get(request)
        manager.finished[QtNetwork.QNetworkReply].connect(self.receiveReply)


    def setupUI(self):
        self.layout_main = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout_main)
        
        # Search bar
        self.line_search = QtWidgets.QLineEdit()
        self.line_search.setPlaceholderText("Search for themes")
        self.layout_main.addWidget(self.line_search)

        # Main layout
        # [list of themes/results] | [selected theme details]
        layout_hbox_list_and_details = QtWidgets.QHBoxLayout()
        # This is the list of database themes
        self.list_results = QtWidgets.QListWidget()
        self.list_results.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
        )
        self.list_results.itemActivated.connect(self.themeSelected)
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
        self.lbl_theme_name = QtWidgets.QLabel("Theme name here")
        self.lbl_theme_name.setTextInteractionFlags(_flag_selectable)
        self.lbl_theme_name.setStyleSheet("QLabel { font-size: 16px; font-weight:bold;}")
        self.lbl_theme_name.setWordWrap(True)
        layout_vbox_scroll_insides.addWidget(self.lbl_theme_name)
        
        # Author name
        self.lbl_author_name = QtWidgets.QLabel("Author: ?")
        self.lbl_author_name.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_author_name)
        
        # description. this needs to be the biggest
        self.lbl_description = QtWidgets.QLabel("Description")
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
        self.lbl_requires = QtWidgets.QLabel("Requires: pibby")
        self.lbl_requires.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_requires)
        
        # Version number. this will also show the current installed one if there is an update
        self.lbl_version = QtWidgets.QLabel("Version: 2 (installed: 0)")
        self.lbl_version.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_version)

        # Last update time
        self.lbl_last_update = QtWidgets.QLabel("DD/MM/YYYY HH:MM")
        self.lbl_last_update.setTextInteractionFlags(_flag_selectable)
        layout_vbox_scroll_insides.addWidget(self.lbl_last_update)
        
        # Theme details done, so we wont need the scroll after this
        self.frame_scroll.setLayout(layout_vbox_scroll_insides)
        layout_vbox_details.addWidget(self.frame_scroll)
        # Insta//uninstall buttons
        # "Uninstall" button. Only visisble when the selected thene is installed
        self.btn_uninstall = QtWidgets.QPushButton("Uninstall", self)
        self.btn_uninstall.setHidden(True)
        layout_vbox_details.addWidget(self.btn_uninstall)
        # "Install" button. can also say "Update" if an update is availible
        self.btn_install = QtWidgets.QPushButton("Install", self)
        layout_vbox_details.addWidget(self.btn_install)
        
        # Done with details
        layout_hbox_list_and_details.addLayout(layout_vbox_details)
        self.layout_main.addLayout(layout_hbox_list_and_details)

        self.btn_refresh = QtWidgets.QPushButton("Refresh", self)
        self.btn_refresh.clicked.connect(self.refresh)
        self.layout_main.addWidget(self.btn_refresh)

