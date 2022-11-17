#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import traceback
import logging
import datetime
import random
import re
import time
import json

# Set working directory
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

import ostools
import nickservmsgs
import pytwmn

# import console
from pnc.dep.attrdict import AttrDict
from profile import userConfig, userProfile, pesterTheme, PesterLog, PesterProfileDB
from menus import (
    PesterChooseQuirks,
    PesterChooseTheme,
    PesterChooseProfile,
    PesterOptions,
    PesterUserlist,
    PesterMemoList,
    LoadingScreen,
    AboutPesterchum,
    UpdatePesterchum,
    AddChumDialog,
)
from mood import Mood, PesterMoodAction, PesterMoodHandler, PesterMoodButton
from dataobjs import PesterProfile, pesterQuirk, pesterQuirks
from generic import (
    PesterIcon,
    RightClickTree,
    PesterList,
    CaseInsensitiveDict,
    MovingWindow,
    NoneSound,
    WMButton,
)
from convo import PesterTabWindow, PesterConvo
from parsetools import (
    convertTags,
    addTimeInitial,
    themeChecker,
    ThemeException,
    loadQuirks,
)
from memos import PesterMemo, MemoTabWindow, TimeTracker
from irc import PesterIRC
from logviewer import PesterLogUserSelect, PesterLogViewer
from randomer import RandomHandler, RANDNICK
from toast import PesterToastMachine, PesterToast

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtGui import QShortcut, QAction, QActionGroup
except ImportError:
    print("PyQt5 fallback (pesterchum.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QAction, QShortcut, QActionGroup

# Data directory
ostools.validateDataDir()
_datadir = ostools.getDataDir()

# Data directory dependent actions
loadQuirks()

# Command line options
parser = argparse.ArgumentParser()
parser.add_argument(
    "--server", "-s", metavar="ADDRESS", help="Specify server override. (legacy)"
)
parser.add_argument(
    "--port", "-p", metavar="PORT", help="Specify port override. (legacy)"
)
parser.add_argument(
    "--logging",
    "-l",
    metavar="LEVEL",
    default="WARNING",
    help=(
        "Specify level of logging, possible values are:"
        " CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET."
        " (https://docs.python.org/3/library/logging.html)"
    ),
)
parser.add_argument(
    "--advanced",
    action="store_true",
    help=(
        "Enable 'advanced' mode. Adds an 'advanced' tab"
        " to settings for setting user mode and adds"
        " channel modes in memo titles."
        " This feature is currently not maintained."
    ),
)
parser.add_argument(
    "--nohonk", action="store_true", help="Disables the honk soundeffect 🤡📣"
)

# Set logging config section, log level is in oppts.
# Logger
PchumLog = logging.getLogger("pchumLogger")
# Handlers
file_handler = logging.FileHandler(os.path.join(_datadir, "pesterchum.log"))
stream_handler = logging.StreamHandler()
# Format
formatter = logging.Formatter("%(asctime)s - %(module)s  - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add handlers
PchumLog.addHandler(file_handler)
PchumLog.addHandler(stream_handler)

# Global variables
BOTNAMES = []
CUSTOMBOTS = ["CALSPRITE", RANDNICK.upper()]
SERVICES = [
    "NICKSERV",
    "CHANSERV",
    "MEMOSERV",
    "OPERSERV",
    "HELPSERV",
    "HOSTSERV",
    "BOTSERV",
]
BOTNAMES.extend(CUSTOMBOTS)
BOTNAMES.extend(SERVICES)
# Save the main app. From here, we should be able to get everything else in
# order, for console use.
_CONSOLE = False
_CONSOLE_ENV = AttrDict()
_CONSOLE_ENV.PAPP = None
# Python 3
QString = str
# Command line arguments
_ARGUMENTS = parser.parse_args()

# Import audio module
# Qt6.4's ffmpeg audio backend makes using QtMultimedia on linux less risky
try:
    # PyQt6, QtMultimedia is prefered.
    from PyQt6 import QtMultimedia

    # print("Audio module is PyQt6 QtMultimedia.")
except ImportError:
    if ostools.isWin32() or ostools.isOSX():
        # PyQt5 QtMultimedia has native backends for MacOS and Windows
        try:
            from PyQt5 import QtMultimedia

            print(
                "Using PyQt5 QtMultimedia as sound module. (fallback, PyQt6 QtMultimedia not availible)"
            )
        except ImportError:
            try:
                try:
                    # Mute pygame support print
                    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
                except:
                    pass
                import pygame

                print(
                    "Using pygame as sound module. (fallback, PyQt6 QtMultimedia and PyQt5 QtMultimedia not availible)"
                )
            except ImportError:
                print(
                    "All possible audio modules failed to import."
                    "\nPossible audio modules in order of preference (Windows/MacOS): PyQt6 QtMultimedia > PyQt5 QtMultimedia > pygame"
                )
    # Linux or misc.
    else:
        # PyQt5 QtMultimedia needs gstreamer on linux, so pygame is prefered.
        try:
            try:
                # Mute pygame support print
                os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
            except:
                pass
            import pygame

            print(
                "Using pygame as sound module. (fallback, PyQt6 QtMultimedia not availible)"
            )
        except ImportError:
            try:
                from PyQt5 import QtMultimedia

                print(
                    "Using PyQt5 QtMultimedia as sound module. (fallback, PyQt6 QtMultimedia and pygame not availible)"
                )
                print(
                    "PyQt5 Multimedia will silently fail without GStreamer with relevant"
                    " plugins on Linux, pygame is prefered when using PyQt5."
                )
            except ImportError:
                print(
                    "All possible audio modules failed to import."
                    "\nLPossible audio modules in order of preference (Linux/Unknown): PyQt6 QtMultimedia > pygame > PyQt5 QtMultimedia"
                )


class waitingMessageHolder(object):
    def __init__(self, mainwindow, **msgfuncs):
        self.mainwindow = mainwindow
        self.funcs = msgfuncs
        self.queue = list(msgfuncs.keys())
        if len(self.queue) > 0:
            self.mainwindow.updateSystemTray()

    def waitingHandles(self):
        return self.queue

    def answerMessage(self):
        func = self.funcs[self.queue[0]]
        func()

    def messageAnswered(self, handle):
        if handle not in self.queue:
            return
        self.queue = [q for q in self.queue if q != handle]
        del self.funcs[handle]
        if len(self.queue) == 0:
            self.mainwindow.updateSystemTray()

    def addMessage(self, handle, func):
        if handle not in self.funcs:
            self.queue.append(handle)
        self.funcs[handle] = func
        if len(self.queue) > 0:
            self.mainwindow.updateSystemTray()

    def __len__(self):
        return len(self.queue)


class chumListing(QtWidgets.QTreeWidgetItem):
    def __init__(self, chum, window):
        super(chumListing, self).__init__([chum.handle])
        self.mainwindow = window
        self.chum = chum
        self.handle = chum.handle
        self.setMood(Mood("offline"))
        self.status = None
        self.setToolTip(
            0, "%s: %s" % (chum.handle, window.chumdb.getNotes(chum.handle))
        )

    def setMood(self, mood):
        if hasattr(self.mainwindow, "chumList") and self.mainwindow.chumList.notify:
            # print "%s -> %s" % (self.chum.mood.name(), mood.name())
            if (
                self.mainwindow.config.notifyOptions() & self.mainwindow.config.SIGNOUT
                and mood.name() == "offline"
                and self.chum.mood.name() != "offline"
            ):
                # print "OFFLINE NOTIFY: " + self.handle
                uri = self.mainwindow.theme["toasts/icon/signout"]
                n = self.mainwindow.tm.Toast(
                    self.mainwindow.tm.appName, "%s is Offline" % (self.handle), uri
                )
                n.show()
            elif (
                self.mainwindow.config.notifyOptions() & self.mainwindow.config.SIGNIN
                and mood.name() != "offline"
                and self.chum.mood.name() == "offline"
            ):
                # print "ONLINE NOTIFY: " + self.handle
                uri = self.mainwindow.theme["toasts/icon/signin"]
                n = self.mainwindow.tm.Toast(
                    self.mainwindow.tm.appName, "%s is Online" % (self.handle), uri
                )
                n.show()
        login = False
        logout = False
        if mood.name() == "offline" and self.chum.mood.name() != "offline":
            logout = True
        elif mood.name() != "offline" and self.chum.mood.name() == "offline":
            login = True
        self.chum.mood = mood
        self.updateMood(login=login, logout=logout)

    def setColor(self, color):
        self.chum.color = color

    def updateMood(self, unblock=False, login=False, logout=False):
        mood = self.chum.mood
        self.mood = mood
        icon = self.mood.icon(self.mainwindow.theme)
        if login:
            self.login()
        elif logout:
            self.logout()
        else:
            self.setIcon(0, icon)
        try:
            self.setForeground(
                0,
                QtGui.QBrush(
                    QtGui.QColor(
                        self.mainwindow.theme["main/chums/moods"][self.mood.name()][
                            "color"
                        ]
                    )
                ),
            )
        except KeyError:
            self.setForeground(
                0,
                QtGui.QBrush(
                    QtGui.QColor(self.mainwindow.theme["main/chums/moods/chummy/color"])
                ),
            )

    def changeTheme(self, theme):
        icon = self.mood.icon(theme)
        self.setIcon(0, icon)
        try:
            self.setForeground(
                0,
                QtGui.QBrush(
                    QtGui.QColor(
                        (
                            self.mainwindow.theme["main/chums/moods"][self.mood.name()][
                                "color"
                            ]
                        )
                    )
                ),
            )
        except KeyError:
            self.setForeground(
                0,
                QtGui.QBrush(
                    QtGui.QColor(
                        (self.mainwindow.theme["main/chums/moods/chummy/color"])
                    )
                ),
            )

    def login(self):
        self.setIcon(0, PesterIcon("themes/arrow_right.png"))
        self.status = "in"
        QtCore.QTimer.singleShot(5000, self.doneLogin)

    def doneLogin(self):
        icon = self.mood.icon(self.mainwindow.theme)
        self.setIcon(0, icon)

    def logout(self):
        self.setIcon(0, PesterIcon("themes/arrow_left.png"))
        self.status = "out"
        QtCore.QTimer.singleShot(5000, self.doneLogout)

    def doneLogout(self):
        hideoff = self.mainwindow.config.hideOfflineChums()
        icon = self.mood.icon(self.mainwindow.theme)
        self.setIcon(0, icon)
        if hideoff and self.status and self.status == "out":
            self.mainwindow.chumList.takeItem(self)

    def __lt__(self, cl):
        h1 = self.handle.lower()
        h2 = cl.handle.lower()
        return h1 < h2


class chumArea(RightClickTree):
    # This is the class that controls the actual main chumlist, I think.
    # Looking into how the groups work might be wise.
    def __init__(self, chums, parent=None):
        super(chumArea, self).__init__(parent)
        self.notify = False
        QtCore.QTimer.singleShot(30000, self.beginNotify)
        self.mainwindow = parent
        theme = self.mainwindow.theme
        self.chums = chums
        gTemp = self.mainwindow.config.getGroups()
        self.groups = [g[0] for g in gTemp]
        self.openGroups = [g[1] for g in gTemp]
        self.showAllGroups(True)
        if not self.mainwindow.config.hideOfflineChums():
            self.showAllChums()
        if not self.mainwindow.config.showEmptyGroups():
            self.hideEmptyGroups()
        self.groupMenu = QtWidgets.QMenu(self)
        self.canonMenu = QtWidgets.QMenu(self)
        self.optionsMenu = QtWidgets.QMenu(self)
        self.pester = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/pester"], self
        )
        self.pester.triggered.connect(self.activateChum)
        self.removechum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/removechum"], self
        )
        self.removechum.triggered.connect(self.removeChum)
        self.blockchum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/blockchum"], self
        )
        self.blockchum.triggered.connect(self.blockChum)
        self.logchum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/viewlog"], self
        )
        self.logchum.triggered.connect(self.openChumLogs)
        self.reportchum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/report"], self
        )
        self.reportchum.triggered.connect(self.reportChum)
        self.findalts = QAction("Find Alts", self)
        self.findalts.triggered.connect(self.findAlts)
        self.removegroup = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/removegroup"], self
        )
        self.removegroup.triggered.connect(self.removeGroup)
        self.renamegroup = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/renamegroup"], self
        )
        self.renamegroup.triggered.connect(self.renameGroup)
        self.notes = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/notes"], self
        )
        self.notes.triggered.connect(self.editNotes)

        self.optionsMenu.addAction(self.pester)
        self.optionsMenu.addAction(self.logchum)
        self.optionsMenu.addAction(self.notes)
        self.optionsMenu.addAction(self.blockchum)
        self.optionsMenu.addAction(self.removechum)
        self.moveMenu = QtWidgets.QMenu(
            self.mainwindow.theme["main/menus/rclickchumlist/movechum"], self
        )
        self.optionsMenu.addMenu(self.moveMenu)
        self.optionsMenu.addAction(self.reportchum)
        self.moveGroupMenu()

        self.groupMenu.addAction(self.renamegroup)
        self.groupMenu.addAction(self.removegroup)

        self.canonMenu.addAction(self.pester)
        self.canonMenu.addAction(self.logchum)
        self.canonMenu.addAction(self.blockchum)
        self.canonMenu.addAction(self.removechum)
        self.canonMenu.addMenu(self.moveMenu)
        self.canonMenu.addAction(self.reportchum)
        self.canonMenu.addAction(self.findalts)

        self.initTheme(theme)
        # self.sortItems()
        # self.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder)
        self.setSortingEnabled(False)
        self.header().hide()
        self.setDropIndicatorShown(True)
        self.setIndentation(4)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setAnimated(True)
        self.setRootIsDecorated(False)

        self.itemDoubleClicked[QtWidgets.QTreeWidgetItem, int].connect(self.expandGroup)

    @QtCore.pyqtSlot()
    def beginNotify(self):
        PchumLog.info("BEGIN NOTIFY")
        self.notify = True

    def getOptionsMenu(self):
        if not self.currentItem():
            return None
        text = str(self.currentItem().text(0))
        if text.rfind(" (") != -1:
            text = text[0 : text.rfind(" (")]
        if text == "Chums":
            return None
        elif text in self.groups:
            return self.groupMenu
        else:
            # currenthandle = self.currentItem().chum.handle

            # if currenthandle in canon_handles:
            #    return self.canonMenu
            # else:
            return self.optionsMenu

    def startDrag(self, dropAction):
        ##        Traceback (most recent call last):
        ##            File "pesterchum.py", line 355, in startDrag
        ##            mime.setData('application/x-item', '???')
        ##            TypeErroreError: setData(self, str, Union[QByteArray, bytes, bytearray]): argument 2 has unexpected type 'str'
        try:
            # create mime data object
            mime = QtCore.QMimeData()
            mime.setData(
                "application/x-item", QtCore.QByteArray()
            )  # Voodoo programming :"3
            # start drag
            drag = QtGui.QDrag(self)
            drag.setMimeData(mime)
            drag.exec(QtCore.Qt.DropAction.MoveAction)
        except:
            logging.exception("")

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-item"):
            event.setDropAction(QtCore.Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-item"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-item"):
            event.acceptProposedAction()
        else:
            event.ignore()
            return
        thisitem = str(event.source().currentItem().text(0))
        if thisitem.rfind(" (") != -1:
            thisitem = thisitem[0 : thisitem.rfind(" (")]
        # Drop item is a group
        thisitem = str(event.source().currentItem().text(0))
        if thisitem.rfind(" (") != -1:
            thisitem = thisitem[0 : thisitem.rfind(" (")]
        if thisitem == "Chums" or thisitem in self.groups:
            try:
                # PyQt6
                droppos = self.itemAt(event.position().toPoint())
            except AttributeError:
                # PyQt5
                droppos = self.itemAt(event.pos())
            if not droppos:
                return
            droppos = str(droppos.text(0))
            if droppos.rfind(" ") != -1:
                droppos = droppos[0 : droppos.rfind(" ")]
            if droppos == "Chums" or droppos in self.groups:
                saveOpen = event.source().currentItem().isExpanded()
                try:
                    # PyQt6
                    saveDrop = self.itemAt(event.position().toPoint())
                except AttributeError:
                    # PyQt5
                    saveDrop = self.itemAt(event.pos())
                saveItem = self.takeTopLevelItem(
                    self.indexOfTopLevelItem(event.source().currentItem())
                )
                self.insertTopLevelItems(
                    self.indexOfTopLevelItem(saveDrop) + 1, [saveItem]
                )
                if saveOpen:
                    saveItem.setExpanded(True)

                gTemp = []
                for i in range(self.topLevelItemCount()):
                    text = str(self.topLevelItem(i).text(0))
                    if text.rfind(" (") != -1:
                        text = text[0 : text.rfind(" (")]
                    gTemp.append([str(text), self.topLevelItem(i).isExpanded()])
                self.mainwindow.config.saveGroups(gTemp)
        # Drop item is a chum
        else:
            try:
                # PyQt6
                eventpos = event.position().toPoint()
            except AttributeError:
                # PyQt5
                eventpos = event.pos()
            item = self.itemAt(eventpos)
            if item:
                text = str(item.text(0))
                # Figure out which group to drop into
                if text.rfind(" (") != -1:
                    text = text[0 : text.rfind(" (")]
                if text == "Chums" or text in self.groups:
                    group = text
                    gitem = item
                else:
                    ptext = str(item.parent().text(0))
                    if ptext.rfind(" ") != -1:
                        ptext = ptext[0 : ptext.rfind(" ")]
                    group = ptext
                    gitem = item.parent()

                chumLabel = event.source().currentItem()
                chumLabel.chum.group = group
                self.mainwindow.chumdb.setGroup(chumLabel.chum.handle, group)
                self.takeItem(chumLabel)
                # Using manual chum reordering
                if self.mainwindow.config.sortMethod() == 2:
                    insertIndex = gitem.indexOfChild(item)
                    if insertIndex == -1:
                        insertIndex = 0
                    gitem.insertChild(insertIndex, chumLabel)
                    chums = self.mainwindow.config.chums()
                    if item == gitem:
                        item = gitem.child(0)
                    inPos = chums.index(str(item.text(0)))
                    if chums.index(thisitem) < inPos:
                        inPos -= 1
                    chums.remove(thisitem)
                    chums.insert(inPos, str(thisitem))

                    self.mainwindow.config.setChums(chums)
                else:
                    self.addItem(chumLabel)
                if self.mainwindow.config.showOnlineNumbers():
                    self.showOnlineNumbers()

    def moveGroupMenu(self):
        currentGroup = self.currentItem()
        if currentGroup:
            if currentGroup.parent():
                text = str(currentGroup.parent().text(0))
            else:
                text = str(currentGroup.text(0))
            if text.rfind(" (") != -1:
                text = text[0 : text.rfind(" (")]
            currentGroup = text
        self.moveMenu.clear()
        actGroup = QActionGroup(self)

        groups = self.groups[:]
        for gtext in groups:
            if gtext == currentGroup:
                continue
            movegroup = self.moveMenu.addAction(gtext)
            actGroup.addAction(movegroup)
        actGroup.triggered[QAction].connect(self.moveToGroup)

    def addChum(self, chum):
        if len([c for c in self.chums if c.handle == chum.handle]) != 0:
            return
        self.chums.append(chum)
        if not (
            self.mainwindow.config.hideOfflineChums() and chum.mood.name() == "offline"
        ):
            chumLabel = chumListing(chum, self.mainwindow)
            self.addItem(chumLabel)
            # self.topLevelItem(0).addChild(chumLabel)
            # self.topLevelItem(0).sortChildren(0, QtCore.Qt.SortOrder.AscendingOrder)

    def getChums(self, handle):
        chums = self.findItems(
            handle,
            QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive,
        )
        return chums

    def showAllChums(self):
        for c in self.chums:
            chandle = c.handle
            if not len(
                self.findItems(
                    chandle,
                    QtCore.Qt.MatchFlag.MatchExactly
                    | QtCore.Qt.MatchFlag.MatchRecursive,
                )
            ):
                # if True:# For if it doesn't work at all :/
                chumLabel = chumListing(c, self.mainwindow)
                self.addItem(chumLabel)
        self.sort()

    def hideOfflineChums(self):
        for j in range(self.topLevelItemCount()):
            i = 0
            listing = self.topLevelItem(j).child(i)
            while listing is not None:
                if listing.chum.mood.name() == "offline":
                    self.topLevelItem(j).takeChild(i)
                else:
                    i += 1
                listing = self.topLevelItem(j).child(i)
            self.sort()

    def showAllGroups(self, first=False):
        if first:
            for i, g in enumerate(self.groups):
                child_1 = QtWidgets.QTreeWidgetItem(["%s" % (g)])
                self.addTopLevelItem(child_1)
                if self.openGroups[i]:
                    child_1.setExpanded(True)
            return
        curgroups = []
        for i in range(self.topLevelItemCount()):
            text = str(self.topLevelItem(i).text(0))
            if text.rfind(" (") != -1:
                text = text[0 : text.rfind(" (")]
            curgroups.append(text)
        for i, g in enumerate(self.groups):
            if g not in curgroups:
                child_1 = QtWidgets.QTreeWidgetItem(["%s" % (g)])
                j = 0
                for h in self.groups:
                    if h == g:
                        self.insertTopLevelItem(j, child_1)
                        break
                    if h in curgroups:
                        j += 1
                if self.openGroups[i]:
                    child_1.setExpanded(True)
        if self.mainwindow.config.showOnlineNumbers():
            self.showOnlineNumbers()

    def showOnlineNumbers(self):
        if hasattr(self, "groups"):
            self.hideOnlineNumbers()
            totals = {"Chums": 0}
            online = {"Chums": 0}
            for g in self.groups:
                totals[str(g)] = 0
                online[str(g)] = 0
            for c in self.chums:
                yes = c.mood.name() != "offline"
                if c.group == "Chums":
                    totals[str(c.group)] = totals[str(c.group)] + 1
                    if yes:
                        online[str(c.group)] = online[str(c.group)] + 1
                elif c.group in totals:
                    totals[str(c.group)] = totals[str(c.group)] + 1
                    if yes:
                        online[str(c.group)] = online[str(c.group)] + 1
                else:
                    totals["Chums"] = totals["Chums"] + 1
                    if yes:
                        online["Chums"] = online["Chums"] + 1
            for i in range(self.topLevelItemCount()):
                text = str(self.topLevelItem(i).text(0))
                if text.rfind(" (") != -1:
                    text = text[0 : text.rfind(" (")]
                if text in online:
                    self.topLevelItem(i).setText(
                        0, "%s (%i/%i)" % (text, online[text], totals[text])
                    )

    def hideOnlineNumbers(self):
        for i in range(self.topLevelItemCount()):
            text = str(self.topLevelItem(i).text(0))
            if text.rfind(" (") != -1:
                text = text[0 : text.rfind(" (")]
            self.topLevelItem(i).setText(0, "%s" % (text))

    def hideEmptyGroups(self):
        i = 0
        listing = self.topLevelItem(i)
        while listing is not None:
            if listing.childCount() == 0:
                self.takeTopLevelItem(i)
            else:
                i += 1
            listing = self.topLevelItem(i)

    @QtCore.pyqtSlot()
    def expandGroup(self):
        item = self.currentItem()
        text = str(item.text(0))
        if text.rfind(" (") != -1:
            text = text[0 : text.rfind(" (")]

        if text in self.groups:
            expand = item.isExpanded()
            self.mainwindow.config.expandGroup(text, not expand)

    def addItem(self, chumLabel):
        if hasattr(self, "groups"):
            if chumLabel.chum.group not in self.groups:
                chumLabel.chum.group = "Chums"
            if "Chums" not in self.groups:
                self.mainwindow.config.addGroup("Chums")
            curgroups = []
            for i in range(self.topLevelItemCount()):
                text = str(self.topLevelItem(i).text(0))
                if text.rfind(" (") != -1:
                    text = text[0 : text.rfind(" (")]
                curgroups.append(text)
            if not self.findItems(
                chumLabel.handle,
                QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive,
            ):
                # if True:# For if it doesn't work at all :/
                if chumLabel.chum.group not in curgroups:
                    child_1 = QtWidgets.QTreeWidgetItem(["%s" % (chumLabel.chum.group)])
                    i = 0
                    for g in self.groups:
                        if g == chumLabel.chum.group:
                            self.insertTopLevelItem(i, child_1)
                            break
                        if g in curgroups:
                            i += 1
                    if self.openGroups[
                        self.groups.index("%s" % (chumLabel.chum.group))
                    ]:
                        child_1.setExpanded(True)
                for i in range(self.topLevelItemCount()):
                    text = str(self.topLevelItem(i).text(0))
                    if text.rfind(" (") != -1:
                        text = text[0 : text.rfind(" (")]
                    if text == chumLabel.chum.group:
                        break
                # Manual sorting
                if self.mainwindow.config.sortMethod() == 2:
                    chums = self.mainwindow.config.chums()
                    if chumLabel.chum.handle in chums:
                        fi = chums.index(chumLabel.chum.handle)
                    else:
                        fi = 0
                    c = 1

                    # TODO: Rearrange chums list on drag-n-drop
                    bestj = 0
                    bestname = ""
                    if fi > 0:
                        while not bestj:
                            for j in range(self.topLevelItem(i).childCount()):
                                if chums[fi - c] == str(
                                    self.topLevelItem(i).child(j).text(0)
                                ):
                                    bestj = j
                                    bestname = chums[fi - c]
                                    break
                            c += 1
                            if fi - c < 0:
                                break
                    if bestname:
                        self.topLevelItem(i).insertChild(bestj + 1, chumLabel)
                    else:
                        self.topLevelItem(i).insertChild(bestj, chumLabel)
                    # sys.exit(0)
                    self.topLevelItem(i).addChild(chumLabel)
                else:  # All other sorting
                    self.topLevelItem(i).addChild(chumLabel)
                self.sort()
                if self.mainwindow.config.showOnlineNumbers():
                    self.showOnlineNumbers()
        else:  # usually means this is now the trollslum
            if not self.findItems(
                chumLabel.handle,
                QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive,
            ):
                # if True:# For if it doesn't work at all :/
                self.topLevelItem(0).addChild(chumLabel)
                self.topLevelItem(0).sortChildren(0, QtCore.Qt.SortOrder.AscendingOrder)

    def takeItem(self, chumLabel):
        r = None
        if not hasattr(chumLabel, "chum"):
            return r
        for i in range(self.topLevelItemCount()):
            for j in range(self.topLevelItem(i).childCount()):
                if self.topLevelItem(i).child(j).text(0) == chumLabel.chum.handle:
                    r = self.topLevelItem(i).takeChild(j)
                    break
        if not self.mainwindow.config.showEmptyGroups():
            self.hideEmptyGroups()
        if self.mainwindow.config.showOnlineNumbers():
            self.showOnlineNumbers()
        return r

    def updateMood(self, handle, mood):
        hideoff = self.mainwindow.config.hideOfflineChums()
        chums = self.getChums(handle)
        oldmood = None
        if hideoff:
            if (
                mood.name() != "offline"
                and len(chums) == 0
                and handle in [p.handle for p in self.chums]
            ):
                newLabel = chumListing(
                    [p for p in self.chums if p.handle == handle][0], self.mainwindow
                )
                self.addItem(newLabel)
                # self.sortItems()
                chums = [newLabel]
            elif mood.name() == "offline" and len(chums) > 0:
                for c in chums:
                    if hasattr(c, "mood"):
                        c.setMood(mood)
                    # self.takeItem(c)
                chums = []
        for c in chums:
            if hasattr(c, "mood"):
                oldmood = c.mood
                c.setMood(mood)
        if self.mainwindow.config.sortMethod() == 1:
            for i in range(self.topLevelItemCount()):
                saveCurrent = self.currentItem()
                self.moodSort(i)
                self.setCurrentItem(saveCurrent)
        if self.mainwindow.config.showOnlineNumbers():
            self.showOnlineNumbers()
        return oldmood

    def updateColor(self, handle, color):
        chums = self.findItems(handle, QtCore.Qt.MatchFlag.MatchExactly)
        for c in chums:
            c.setColor(color)

    def initTheme(self, theme):
        self.resize(*theme["main/chums/size"])
        self.move(*theme["main/chums/loc"])
        if "main/chums/scrollbar" in theme:
            self.setStyleSheet(
                "QListWidget { %s } \
                QScrollBar { %s } \
                QScrollBar::handle { %s } \
                QScrollBar::add-line { %s } \
                QScrollBar::sub-line { %s } \
                QScrollBar:up-arrow { %s } \
                QScrollBar:down-arrow { %s }"
                % (
                    theme["main/chums/style"],
                    theme["main/chums/scrollbar/style"],
                    theme["main/chums/scrollbar/handle"],
                    theme["main/chums/scrollbar/downarrow"],
                    theme["main/chums/scrollbar/uparrow"],
                    theme["main/chums/scrollbar/uarrowstyle"],
                    theme["main/chums/scrollbar/darrowstyle"],
                )
            )
        else:
            self.setStyleSheet(theme["main/chums/style"])
        self.pester.setText(theme["main/menus/rclickchumlist/pester"])
        self.removechum.setText(theme["main/menus/rclickchumlist/removechum"])
        self.blockchum.setText(theme["main/menus/rclickchumlist/blockchum"])
        self.logchum.setText(theme["main/menus/rclickchumlist/viewlog"])
        self.reportchum.setText(theme["main/menus/rclickchumlist/report"])
        self.notes.setText(theme["main/menus/rclickchumlist/notes"])
        self.removegroup.setText(theme["main/menus/rclickchumlist/removegroup"])
        self.renamegroup.setText(theme["main/menus/rclickchumlist/renamegroup"])
        self.moveMenu.setTitle(theme["main/menus/rclickchumlist/movechum"])

    def changeTheme(self, theme):
        self.initTheme(theme)
        chumlistings = []
        for i in range(self.topLevelItemCount()):
            for j in range(self.topLevelItem(i).childCount()):
                chumlistings.append(self.topLevelItem(i).child(j))
        # chumlistings = [self.item(i) for i in range(0, self.count())]
        for c in chumlistings:
            c.changeTheme(theme)

    def count(self):
        c = 0
        for i in range(self.topLevelItemCount()):
            c = c + self.topLevelItem(i).childCount()
        return c

    def sort(self):
        if self.mainwindow.config.sortMethod() == 2:
            pass  # Do nothing!!!!! :OOOOOOO It's manual, bitches
        elif self.mainwindow.config.sortMethod() == 1:
            for i in range(self.topLevelItemCount()):
                self.moodSort(i)
        else:
            for i in range(self.topLevelItemCount()):
                self.topLevelItem(i).sortChildren(0, QtCore.Qt.SortOrder.AscendingOrder)

    def moodSort(self, group):
        scrollPos = self.verticalScrollBar().sliderPosition()
        chums = []
        listing = self.topLevelItem(group).child(0)
        while listing is not None:
            chums.append(self.topLevelItem(group).takeChild(0))
            listing = self.topLevelItem(group).child(0)
        chums.sort(
            key=lambda x: (
                (999 if x.chum.mood.value() == 2 else x.chum.mood.value()),
                x.chum.handle,
            ),
            reverse=False,
        )
        for c in chums:
            self.topLevelItem(group).addChild(c)
        self.verticalScrollBar().setSliderPosition(scrollPos)

    @QtCore.pyqtSlot()
    def activateChum(self):
        self.itemActivated.emit(self.currentItem(), 0)

    @QtCore.pyqtSlot()
    def removeChum(self, handle=None):
        if handle:
            clistings = self.getChums(handle)
            if len(clistings) <= 0:
                return
            for c in clistings:
                self.setCurrentItem(c)
        if not self.currentItem():
            return
        currentChum = self.currentItem().chum
        self.chums = [c for c in self.chums if c.handle != currentChum.handle]
        self.removeChumSignal.emit(self.currentItem().chum.handle)
        oldlist = self.takeItem(self.currentItem())
        del oldlist

    @QtCore.pyqtSlot()
    def blockChum(self):
        currentChum = self.currentItem()
        if not currentChum:
            return
        self.blockChumSignal.emit(self.currentItem().chum.handle)

    @QtCore.pyqtSlot()
    def reportChum(self):
        currentChum = self.currentItem()
        if not currentChum:
            return
        self.mainwindow.reportChum(self.currentItem().chum.handle)

    @QtCore.pyqtSlot()
    def findAlts(self):
        currentChum = self.currentItem()
        if not currentChum:
            return
        self.mainwindow.sendMessage.emit(
            "ALT %s" % (currentChum.chum.handle), "calSprite"
        )

    @QtCore.pyqtSlot()
    def openChumLogs(self):
        currentChum = self.currentItem()
        if not currentChum:
            return
        currentChum = currentChum.text(0)
        self.pesterlogviewer = PesterLogViewer(
            currentChum, self.mainwindow.config, self.mainwindow.theme, self.mainwindow
        )
        self.pesterlogviewer.rejected.connect(self.closeActiveLog)
        self.pesterlogviewer.show()
        self.pesterlogviewer.raise_()
        self.pesterlogviewer.activateWindow()

    @QtCore.pyqtSlot()
    def closeActiveLog(self):
        self.pesterlogviewer.close()
        self.pesterlogviewer = None

    @QtCore.pyqtSlot()
    def editNotes(self):
        currentChum = self.currentItem()
        if not currentChum:
            return
        (notes, ok) = QtWidgets.QInputDialog.getText(
            self, "Notes", "Enter your notes..."
        )
        if ok:
            notes = str(notes)
            self.mainwindow.chumdb.setNotes(currentChum.handle, notes)
            currentChum.setToolTip(0, "%s: %s" % (currentChum.handle, notes))

    @QtCore.pyqtSlot()
    def renameGroup(self):
        if not hasattr(self, "renamegroupdialog"):
            self.renamegroupdialog = None
        if not self.renamegroupdialog:
            (gname, ok) = QtWidgets.QInputDialog.getText(
                self, "Rename Group", "Enter a new name for the group:"
            )
            if ok:
                gname = str(gname)
                if re.search("[^A-Za-z0-9_\s]", gname) is not None:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setStyleSheet(
                        "QMessageBox{ %s }"
                        % self.mainwindow.theme["main/defaultwindow/style"]
                    )
                    msgbox.setInformativeText("THIS IS NOT A VALID GROUP NAME")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.exec()
                    self.addgroupdialog = None
                    return
                currentGroup = self.currentItem()
                if not currentGroup:
                    return
                index = self.indexOfTopLevelItem(currentGroup)
                if index != -1:
                    expanded = currentGroup.isExpanded()
                    text = str(currentGroup.text(0))
                    if text.rfind(" (") != -1:
                        text = text[0 : text.rfind(" (")]
                    self.mainwindow.config.delGroup(text)
                    self.mainwindow.config.addGroup(gname, expanded)
                    gTemp = self.mainwindow.config.getGroups()
                    self.groups = [g[0] for g in gTemp]
                    self.openGroups = [g[1] for g in gTemp]
                    for i in range(currentGroup.childCount()):
                        currentGroup.child(i).chum.group = gname
                        self.mainwindow.chumdb.setGroup(
                            currentGroup.child(i).chum.handle, gname
                        )
                    currentGroup.setText(0, gname)
        if self.mainwindow.config.showOnlineNumbers():
            self.showOnlineNumbers()
        self.renamegroupdialog = None

    @QtCore.pyqtSlot()
    def removeGroup(self):
        currentGroup = self.currentItem()
        if not currentGroup:
            return
        text = str(currentGroup.text(0))
        if text.rfind(" (") != -1:
            text = text[0 : text.rfind(" (")]
        self.mainwindow.config.delGroup(text)
        gTemp = self.mainwindow.config.getGroups()
        self.groups = [g[0] for g in gTemp]
        self.openGroups = [g[1] for g in gTemp]
        for c in self.chums:
            if c.group == text:
                c.group = "Chums"
                self.mainwindow.chumdb.setGroup(c.handle, "Chums")
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).text(0) == currentGroup.text(0):
                break
        while self.topLevelItem(i) and self.topLevelItem(i).child(0):
            chumLabel = self.topLevelItem(i).child(0)
            self.takeItem(chumLabel)
            self.addItem(chumLabel)
        self.takeTopLevelItem(i)

    @QtCore.pyqtSlot(QAction)
    def moveToGroup(self, item):
        if not item:
            return
        group = str(item.text())
        chumLabel = self.currentItem()
        if not chumLabel:
            return
        chumLabel.chum.group = group
        self.mainwindow.chumdb.setGroup(chumLabel.chum.handle, group)
        self.takeItem(chumLabel)
        self.addItem(chumLabel)

    removeChumSignal = QtCore.pyqtSignal("QString")
    blockChumSignal = QtCore.pyqtSignal("QString")


class trollSlum(chumArea):
    unblockChumSignal = QtCore.pyqtSignal()

    def __init__(self, trolls, mainwindow, parent=None):
        # ~super(trollSlum, self).__init__(parent)
        # TODO: Rework inheritance here.
        QtWidgets.QTreeWidgetItem.__init__(self, parent)
        self.mainwindow = mainwindow
        theme = self.mainwindow.theme
        self.setStyleSheet(theme["main/trollslum/chumroll/style"])
        self.chums = trolls
        child_1 = QtWidgets.QTreeWidgetItem([""])
        self.addTopLevelItem(child_1)
        child_1.setExpanded(True)
        for c in self.chums:
            chandle = c.handle
            if not self.findItems(chandle, QtCore.Qt.MatchFlag.MatchExactly):
                chumLabel = chumListing(c, self.mainwindow)
                self.addItem(chumLabel)

        self.setSortingEnabled(False)
        self.header().hide()
        self.setDropIndicatorShown(False)
        self.setIndentation(0)

        self.optionsMenu = QtWidgets.QMenu(self)
        self.unblockchum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/unblockchum"], self
        )
        self.unblockchum.triggered.connect(self.unblockChumSignal)
        self.optionsMenu.addAction(self.unblockchum)

        # self.sortItems()

    def contextMenuEvent(self, event):
        # fuckin Qt
        if event.reason() == QtGui.QContextMenuEvent.Reason.Mouse:
            listing = self.itemAt(event.pos())
            self.setCurrentItem(listing)
            if self.currentItem().text(0) != "":
                self.optionsMenu.popup(event.globalPos())

    def changeTheme(self, theme):
        self.setStyleSheet(theme["main/trollslum/chumroll/style"])
        self.removechum.setText(theme["main/menus/rclickchumlist/removechum"])
        self.unblockchum.setText(theme["main/menus/rclickchumlist/blockchum"])

        chumlistings = [self.item(i) for i in range(0, self.count())]
        for c in chumlistings:
            c.changeTheme(theme)

    # This causes:
    #     TypeError: connect() failed between triggered(bool) and unblockChumSignal()
    # I'm not sure why this was here in the first place-
    # Does removing it break anything else...?
    # unblockChumSignal = QtCore.pyqtSignal('QString')


class TrollSlumWindow(QtWidgets.QFrame):
    def __init__(self, trolls, mainwindow, parent=None):
        super(TrollSlumWindow, self).__init__(parent)
        self.mainwindow = mainwindow
        theme = self.mainwindow.theme
        self.slumlabel = QtWidgets.QLabel(self)
        self.initTheme(theme)

        self.trollslum = trollSlum(trolls, self.mainwindow, self)
        self.trollslum.unblockChumSignal.connect(self.removeCurrentTroll)
        layout_1 = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("ADD", self)
        self.addButton.clicked.connect(self.addTrollWindow)
        self.removeButton = QtWidgets.QPushButton("REMOVE", self)
        self.removeButton.clicked.connect(self.removeCurrentTroll)
        layout_1.addWidget(self.addButton)
        layout_1.addWidget(self.removeButton)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.slumlabel)
        layout_0.addWidget(self.trollslum)
        layout_0.addLayout(layout_1)
        self.setLayout(layout_0)

    def initTheme(self, theme):
        self.resize(*theme["main/trollslum/size"])
        self.setStyleSheet(theme["main/trollslum/style"])
        self.slumlabel.setText(theme["main/trollslum/label/text"])
        self.slumlabel.setStyleSheet(theme["main/trollslum/label/style"])
        if not self.parent():
            self.setWindowTitle(theme["main/menus/profile/block"])
            self.setWindowIcon(self.mainwindow.windowIcon())

    def changeTheme(self, theme):
        self.initTheme(theme)
        self.trollslum.changeTheme(theme)
        # move unblocked trolls from slum to chumarea

    def closeEvent(self, event):
        self.mainwindow.closeTrollSlum()

    def updateMood(self, handle, mood):
        self.trollslum.updateMood(handle, mood)

    def addTroll(self, chum):
        self.trollslum.addChum(chum)

    def removeTroll(self, handle):
        self.trollslum.removeChum(handle)

    @QtCore.pyqtSlot()
    def removeCurrentTroll(self):
        currentListing = self.trollslum.currentItem()
        if not currentListing or not hasattr(currentListing, "chum"):
            return
        self.unblockChumSignal.emit(currentListing.chum.handle)

    @QtCore.pyqtSlot()
    def addTrollWindow(self):
        if not hasattr(self, "addtrolldialog"):
            self.addtrolldialog = None
        if self.addtrolldialog:
            return
        self.addtrolldialog = QtWidgets.QInputDialog(self)
        (handle, ok) = self.addtrolldialog.getText(
            self, "Add Troll", "Enter Troll Handle:"
        )
        if ok:
            handle = str(handle)
            if not (
                PesterProfile.checkLength(handle)
                and PesterProfile.checkValid(handle)[0]
            ):
                errormsg = QtWidgets.QErrorMessage(self)
                errormsg.showMessage("THIS IS NOT A VALID CHUMTAG!")
                self.addchumdialog = None
                return

            self.blockChumSignal.emit(handle)
        self.addtrolldialog = None

    blockChumSignal = QtCore.pyqtSignal("QString")
    unblockChumSignal = QtCore.pyqtSignal("QString")


class PesterWindow(MovingWindow):
    disconnectIRC = QtCore.pyqtSignal()
    sendMessage = QtCore.pyqtSignal("QString", "QString")

    def __init__(self, options, parent=None, app=None):
        super(PesterWindow, self).__init__(
            None,
            (
                QtCore.Qt.WindowType.CustomizeWindowHint
                | QtCore.Qt.WindowType.FramelessWindowHint
            ),
        )
        # For debugging
        _CONSOLE_ENV.PAPP = self
        # TODO: karxi: SO! At the end of this function it seems like that
        # object is just made into None or.../something/. Somehow, it just
        # DIES, and I haven't the slightest idea why. I've tried multiple ways
        # to set it that shouldn't cause issues with globals; I honestly don't
        # know what to do.
        # Putting logging statements in here *gives me an object*, but I can't
        # carry it out of the function. I'll hvae to think of a way around
        # this....
        # If I use a definition made in here without having another elsewhere,
        # it comes back as undefined. Just...what?

        self.autoJoinDone = False
        self.app = app
        self.parent = parent
        self.convos = CaseInsensitiveDict()
        self.memos = CaseInsensitiveDict()
        self.tabconvo = None
        self.tabmemo = None
        self.shortcuts = AttrDict()

        self.setAutoFillBackground(False)
        self.setObjectName("main")
        self.config = userConfig(self)
        # Trying to fix:
        #     IOError: [Errno 2]
        #     No such file or directory:
        #     u'XXX\\AppData\\Local\\pesterchum/profiles/XXX.js'
        # Part 1 :(
        try:
            if self.config.defaultprofile():
                self.userprofile = userProfile(self.config.defaultprofile())
                self.theme = self.userprofile.getTheme()
            else:
                self.userprofile = userProfile(
                    PesterProfile(
                        "pesterClient%d" % (random.randint(100, 999)),
                        QtGui.QColor("black"),
                        Mood(0),
                    )
                )
                self.theme = self.userprofile.getTheme()
        except Exception as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msgBox.setWindowTitle(":(")
            msgBox.setTextFormat(QtCore.Qt.TextFormat.RichText)  # Clickable html links
            self.filename = _datadir + "pesterchum.js"
            msgBox.setText(
                "<html><h3>A profile error occured, "
                "trying to switch to default pesterClient profile."
                "<br><br>%s<\h3><\html>" % e
            )
            PchumLog.critical(e)
            msgBox.exec()
            self.userprofile = userProfile(
                PesterProfile(
                    "pesterClient%d" % (random.randint(100, 999)),
                    QtGui.QColor("black"),
                    Mood(0),
                )
            )
            self.theme = self.userprofile.getTheme()

        # Silly guy prevention pt. 2
        # We really shouldn't run as root.
        self.root_check()

        # karxi: For the record, these are set via commandline arguments. By
        # default, they aren't usable any other way - you can't set them via
        # the config files.
        # ...which means the flag for disabling honking is also hidden and
        # impossible to set via pesterchum.js.
        #
        # This was almost certainly intentional.
        if "advanced" in options:
            self.advanced = options["advanced"]
        else:
            self.advanced = False
        if "server" in options:
            self.serverOverride = options["server"]
        if "port" in options:
            self.portOverride = options["port"]
        if "honk" in options:
            self.honk = options["honk"]
        else:
            self.honk = True
        self.modes = ""

        self.sound_type = None

        self.randhandler = RandomHandler(self)

        try:
            themeChecker(self.theme)
        except ThemeException as inst:
            PchumLog.error("Caught: %s", inst.parameter)
            themeWarning = QtWidgets.QMessageBox(self)
            themeWarning.setText("Theme Error: %s" % inst)
            themeWarning.exec()
            self.theme = pesterTheme("pesterchum")

        extraToasts = {"default": PesterToast}
        if pytwmn.confExists():
            extraToasts["twmn"] = pytwmn.Notification
        self.tm = PesterToastMachine(
            self,
            lambda: self.theme["main/windowtitle"],
            on=self.config.notify(),
            type=self.config.notifyType(),
            extras=extraToasts,
        )
        self.tm.run()

        self.chatlog = PesterLog(self.profile().handle, self)

        self.move(100, 100)

        talk = QAction(self.theme["main/menus/client/talk"], self)
        self.talk = talk
        talk.triggered.connect(self.openChat)
        logv = QAction(self.theme["main/menus/client/logviewer"], self)
        self.logv = logv
        logv.triggered.connect(self.openLogv)
        grps = QAction(self.theme["main/menus/client/addgroup"], self)
        self.grps = grps
        grps.triggered.connect(self.addGroupWindow)
        self.rand = QAction(self.theme["main/menus/client/randen"], self)
        self.rand.triggered.connect(self.randhandler.getEncounter)
        opts = QAction(self.theme["main/menus/client/options"], self)
        self.opts = opts
        opts.triggered.connect(self.openOpts)
        exitaction = QAction(self.theme["main/menus/client/exit"], self)
        self.exitaction = exitaction
        exitaction.triggered.connect(
            self.killApp, QtCore.Qt.ConnectionType.QueuedConnection
        )
        userlistaction = QAction(self.theme["main/menus/client/userlist"], self)
        self.userlistaction = userlistaction
        userlistaction.triggered.connect(self.showAllUsers)
        memoaction = QAction(self.theme["main/menus/client/memos"], self)
        self.memoaction = memoaction
        memoaction.triggered.connect(self.showMemos)
        self.importaction = QAction(self.theme["main/menus/client/import"], self)
        self.importaction.triggered.connect(self.importExternalConfig)
        self.idleaction = QAction(self.theme["main/menus/client/idle"], self)
        self.idleaction.setCheckable(True)
        self.idleaction.toggled[bool].connect(self.toggleIdle)
        self.reconnectAction = QAction(self.theme["main/menus/client/reconnect"], self)
        self.reconnectAction.triggered.connect(self.disconnectIRC)

        self.menu = QtWidgets.QMenuBar(self)
        self.menu.setNativeMenuBar(False)
        self.menu.setObjectName("mainmenu")

        if self.theme.has_key("main/menus/client/console"):
            self.console = AttrDict(
                dict(
                    window=None,
                    action=QAction(self.theme["main/menus/client/console"], self),
                    is_open=False,
                )
            )
        else:
            self.console = AttrDict(
                dict(window=None, action=QAction("Console", self), is_open=False)
            )
        self.console.shortcuts = AttrDict(
            dict(
                conkey=QShortcut(
                    QtGui.QKeySequence("Ctrl+`"),
                    self,
                    context=QtCore.Qt.ShortcutContext.ApplicationShortcut,
                ),
                curwgt=QShortcut(
                    QtGui.QKeySequence("Ctrl+Alt+w"),
                    self,
                    context=QtCore.Qt.ShortcutContext.ApplicationShortcut,
                ),
            )
        )
        self.console.action.triggered.connect(self.toggleConsole)
        # Make sure the shortcut works anywhere.
        # karxi: There's something wrong with the inheritance scheme here.
        # ~self.console.shortcuts.conkey.setContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.console.shortcuts.conkey.activated.connect(self.toggleConsole)
        # ~# Use new-style connections
        # ~self.console.shortcut.activated.connect(self.toggleConsole)
        # Apparently those can crash sometimes...c'est la vie. Can't use 'em.
        # ~self.connect(self.console.shortcuts.curwgt,
        # ~        QtCore.SIGNAL('activate()'), self.console.
        self.console.is_open = False

        filemenu = self.menu.addMenu(self.theme["main/menus/client/_name"])
        self.filemenu = filemenu
        filemenu.addAction(opts)
        filemenu.addAction(memoaction)
        filemenu.addAction(logv)
        filemenu.addAction(self.rand)
        if not self.randhandler.running:
            self.rand.setEnabled(False)
        filemenu.addAction(userlistaction)
        filemenu.addAction(talk)
        filemenu.addAction(self.idleaction)
        filemenu.addAction(grps)
        if _CONSOLE:
            filemenu.addAction(self.console.action)
        filemenu.addAction(self.importaction)
        filemenu.addAction(self.reconnectAction)
        filemenu.addAction(exitaction)

        changequirks = QAction(self.theme["main/menus/profile/quirks"], self)
        self.changequirks = changequirks
        changequirks.triggered.connect(self.openQuirks)
        loadslum = QAction(self.theme["main/menus/profile/block"], self)
        self.loadslum = loadslum
        loadslum.triggered.connect(self.showTrollSlum)

        changecoloraction = QAction(self.theme["main/menus/profile/color"], self)
        self.changecoloraction = changecoloraction
        changecoloraction.triggered.connect(self.changeMyColor)

        switch = QAction(self.theme["main/menus/profile/switch"], self)
        self.switch = switch
        switch.triggered.connect(self.switchProfile)

        profilemenu = self.menu.addMenu(self.theme["main/menus/profile/_name"])
        self.profilemenu = profilemenu
        profilemenu.addAction(changequirks)
        profilemenu.addAction(loadslum)
        profilemenu.addAction(changecoloraction)
        profilemenu.addAction(switch)

        self.helpAction = QAction(self.theme["main/menus/help/help"], self)
        self.helpAction.triggered.connect(self.launchHelp)
        self.botAction = QAction(self.theme["main/menus/help/calsprite"], self)
        self.botAction.triggered.connect(self.loadCalsprite)
        self.nickServAction = QAction(self.theme["main/menus/help/nickserv"], self)
        self.nickServAction.triggered.connect(self.loadNickServ)
        self.chanServAction = QAction(self.theme["main/menus/help/chanserv"], self)
        self.chanServAction.triggered.connect(self.loadChanServ)
        self.aboutAction = QAction(self.theme["main/menus/help/about"], self)
        self.aboutAction.triggered.connect(self.aboutPesterchum)

        # Because I can't expect all themes to have this included.
        # if self.theme.has_key("main/menus/help/reportbug"):
        try:
            self.reportBugAction = QAction(
                self.theme["main/menus/help/reportbug"], self
            )
        except:
            self.reportBugAction = QAction("REPORT BUG", self)
        try:
            self.xyzRulesAction = QAction(self.theme["main/menus/help/rules"], self)
        except:
            self.xyzRulesAction = QAction("RULES", self)

        self.reportBugAction.triggered.connect(self.reportBug)
        self.xyzRulesAction.triggered.connect(self.xyzRules)
        helpmenu = self.menu.addMenu(self.theme["main/menus/help/_name"])
        self.helpmenu = helpmenu
        self.helpmenu.addAction(self.helpAction)
        self.helpmenu.addAction(self.xyzRulesAction)
        self.helpmenu.addAction(self.botAction)
        self.helpmenu.addAction(self.chanServAction)
        self.helpmenu.addAction(self.nickServAction)
        self.helpmenu.addAction(self.aboutAction)
        self.helpmenu.addAction(self.reportBugAction)

        self.closeButton = WMButton(PesterIcon(self.theme["main/close/image"]), self)
        self.setButtonAction(self.closeButton, self.config.closeAction(), -1)
        self.miniButton = WMButton(PesterIcon(self.theme["main/minimize/image"]), self)
        self.setButtonAction(self.miniButton, self.config.minimizeAction(), -1)

        self.namesdb = CaseInsensitiveDict()
        self.chumdb = PesterProfileDB()

        chums = [PesterProfile(c, chumdb=self.chumdb) for c in set(self.config.chums())]
        self.chumList = chumArea(chums, self)
        self.chumList.itemActivated[QtWidgets.QTreeWidgetItem, int].connect(
            self.pesterSelectedChum
        )
        self.chumList.removeChumSignal["QString"].connect(self.removeChum)
        self.chumList.blockChumSignal["QString"].connect(self.blockChum)

        self.addChumButton = QtWidgets.QPushButton(
            self.theme["main/addchum/text"], self
        )
        self.addChumButton.setObjectName("addchumbtn")
        self.addChumButton.clicked.connect(self.addChumWindow)
        self.pesterButton = QtWidgets.QPushButton(self.theme["main/pester/text"], self)
        self.pesterButton.setObjectName("newpesterbtn")
        self.pesterButton.clicked.connect(self.pesterSelectedChum)
        self.blockButton = QtWidgets.QPushButton(self.theme["main/block/text"], self)
        self.blockButton.setObjectName("blockbtn")
        self.blockButton.clicked.connect(self.blockSelectedChum)

        self.moodsLabel = QtWidgets.QLabel(self.theme["main/moodlabel/text"], self)
        self.moodsLabel.setObjectName("moodlabel")
        self.mychumhandleLabel = QtWidgets.QLabel(
            self.theme["main/mychumhandle/label/text"], self
        )
        self.mychumhandleLabel.setObjectName("myhandlelabel")
        self.mychumhandle = QtWidgets.QPushButton(self.profile().handle, self)
        self.mychumhandle.setFlat(True)
        self.mychumhandle.clicked.connect(self.switchProfile)

        self.mychumcolor = QtWidgets.QPushButton(self)
        self.mychumcolor.clicked.connect(self.changeMyColor)

        # self.show() before self.initTheme() fixes a
        # layering issue on windows... for some reason...
        self.show()

        self.initTheme(self.theme)

        # self.mychumhandleLabel.setStyleSheet("QLabel {);};")

        self.hide()

        self.waitingMessages = waitingMessageHolder(self)

        self.idler = AttrDict(
            dict(
                # autoidle
                auto=False,
                # setidle
                manual=False,
                # idlethreshold
                threshold=60 * self.config.idleTime(),
                # idleaction
                action=self.idleaction,
                # idletimer
                timer=QtCore.QTimer(self),
                # idleposition
                pos=QtGui.QCursor.pos(),
                # idletime
                time=0,
            )
        )
        self.idler.timer.timeout.connect(self.checkIdle)
        self.idler.timer.start(1000)

        if not self.config.defaultprofile():
            self.changeProfile()

        # Fuck you some more OSX leopard! >:(
        # if not ostools.isOSXLeopard():
        #    QtCore.QTimer.singleShot(1000, self.mspacheck)

        self.pcUpdate["QString", "QString"].connect(self.updateMsg)

        self.mychumhandleLabel.adjustSize()  # Required so "CHUMHANDLE:" regardless of style-sheet.
        self.moodsLabel.adjustSize()  # Required so "MOOD:" regardless of style-sheet.

        self.chooseServerAskedToReset = False
        self.chooseServer()

        # Update RE bot
        try:
            if self.userprofile.getRandom():
                code = "+"
            else:
                code = "-"
            self.sendNotice.emit(code, RANDNICK)
        except:
            PchumLog.warning("No randomEncounter set in userconfig?")

        # Client --> Server pings
        self.pingtimer = QtCore.QTimer()
        self.pingtimer.timeout.connect(self.checkPing)
        self.sincerecv = 0  # Time since last recv
        self.lastCheckPing = None

    @QtCore.pyqtSlot(QString, QString)
    def updateMsg(self, ver, url):
        if not hasattr(self, "updatemenu"):
            self.updatemenu = None
        if not self.updatemenu:
            self.updatemenu = UpdatePesterchum(ver, url, self)
            self.updatemenu.accepted.connect(self.updatePC)
            self.updatemenu.rejected.connect(self.noUpdatePC)
            self.updatemenu.show()
            self.updatemenu.raise_()
            self.updatemenu.activateWindow()

    """
    Deprecated
    
    @QtCore.pyqtSlot()
    def updatePC(self):
        version.updateDownload(str(self.updatemenu.url))
        self.updatemenu = None
    @QtCore.pyqtSlot()
    def noUpdatePC(self):
        self.updatemenu = None
    """

    def root_check(self):
        """Raise a warning message box if Pesterchum has admin/root privileges."""
        if ostools.isRoot():
            msgbox = QtWidgets.QMessageBox()
            msg = (
                "Running with elevated privileges, "
                "this is potentially a security risk."
                "\nThere is no valid reason to run Pesterchum as an administrator or as root."
                "\n\nQuit?"
            )
            msgbox.setWindowTitle("Unnecessary permissions warning")
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
            )
            msgbox.setInformativeText(msg)
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No
            )
            continue_anyway = msgbox.button(QtWidgets.QMessageBox.StandardButton.No)
            continue_anyway.setText(
                "I'm a silly little guy and want to continue anyway"
            )
            msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
            ret = msgbox.exec()
            if ret == QtWidgets.QMessageBox.StandardButton.Yes:
                self.app.quit()  # Optional
                sys.exit()

    @QtCore.pyqtSlot()
    def checkPing(self):
        """Check if server is alive on app level,
        this function is called every 15sec"""
        # Return without irc
        if not hasattr(self.parent, "irc"):
            self.lastCheckPing = None
            self.sincerecv = 0
            return

        # We have IRC but we're missing a variable?
        # gweh.jpg
        if self.lastCheckPing is None or self.sincerecv is None:
            return

        # Desync check, happens if pc comes out of sleep.
        currentTime = time.time()
        timeDif = abs(currentTime - self.lastCheckPing)
        if timeDif > 180:  # default UnrealIRCd ping timeout time.
            # 180 is the default UnrealIRCd ping timeout time.
            PchumLog.warning(
                (
                    "Possible desync, system time changed by %s "
                    "seconds since last check. abs(%s - %s)"
                )
                % (timeDif, currentTime, self.lastCheckPing)
            )
            self.sincerecv = 80  # Allows 2 more ping attempts before disconnect.
        self.lastCheckPing = time.time()

        # Presume connection is dead after 90 seconds of silence.
        if self.sincerecv >= 90:
            self.disconnectIRC.emit()

        # Show unresponsive if timing out
        if self.sincerecv >= 45:
            if not self.parent.irc.unresponsive:
                self.parent.irc.unresponsive = True
                self.parent.showLoading(self.parent.widget, "S3RV3R NOT R3SPOND1NG >:?")
                self.show()
                self.setFocus()
        else:
            self.parent.irc.unresponsive = False
            if hasattr(self, "loadingscreen"):
                if self.loadingscreen is not None:
                    PchumLog.info("Server alive !! :O")
                    self.loadingscreen.done(QtWidgets.QDialog.DialogCode.Accepted)
                    self.loadingscreen = None

        # Send a ping if it's been 30 seconds since we've heard from the server.
        if self.sincerecv >= 30:
            self.pingServer.emit()

        self.sincerecv += 5  # Not updating too frequently is better for performance.

    def profile(self):
        return self.userprofile.chat

    def closeConversations(self, switch=False):
        if not hasattr(self, "tabconvo"):
            self.tabconvo = None
        if self.tabconvo:
            self.tabconvo.close()
        else:
            for c in list(self.convos.values()):
                c.close()
        if self.tabmemo:
            if not switch:
                self.tabmemo.close()
            else:
                for m in self.tabmemo.convos:
                    self.tabmemo.convos[m].sendtime()
        else:
            for m in list(self.memos.values()):
                if not switch:
                    m.close()
                else:
                    m.sendtime()

    def paintEvent(self, _):
        """Argument 'event'"""
        try:
            self.backgroundImage
        except:
            pass
        else:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(self.backgroundImage)
            palette.setBrush(QtGui.QPalette.ColorRole.Window, brush)
            self.setPalette(palette)

    @QtCore.pyqtSlot()
    def closeToTray(self):
        # I'm just gonna include a toast here to make sure people don't get confused. :'3
        t = self.tm.Toast("Notice:", "Pesterchum has been minimized to your tray.")
        t.show()
        self.hide()
        self.closeToTraySignal.emit()

    def closeEvent(self, event):
        if hasattr(self, "trollslum") and self.trollslum:
            self.trollslum.close()
        try:
            setting = self.config.closeAction()
        except:
            logging.exception("")
            setting = 0
        if setting == 0:  # minimize to taskbar
            self.showMinimized()
        elif setting == 1:  # minimize to tray
            self.closeToTray()
        elif setting == 2:  # quit
            self.closeConversations()
            self.closeSignal.emit()
        event.accept()

    def newMessage(self, handle, msg):
        if handle in self.config.getBlocklist():
            # yeah suck on this
            self.sendMessage.emit("PESTERCHUM:BLOCKED", handle)
            return
        # notify
        if self.config.notifyOptions() & self.config.NEWMSG:
            if handle not in self.convos:
                t = self.tm.Toast("New Conversation", "From: %s" % handle)
                t.show()
            elif not self.config.notifyOptions() & self.config.NEWCONVO:
                if msg[:11] != "PESTERCHUM:":
                    if handle.upper() not in BOTNAMES:
                        t = self.tm.Toast(
                            "From: %s" % handle, re.sub("</?c(=.*?)?>", "", msg)
                        )
                        t.show()
                else:
                    if msg == "PESTERCHUM:CEASE":
                        t = self.tm.Toast("Closed Conversation", handle)
                        t.show()
                    elif msg == "PESTERCHUM:BLOCK":
                        t = self.tm.Toast("Blocked", handle)
                        t.show()
                    elif msg == "PESTERCHUM:UNBLOCK":
                        t = self.tm.Toast("Unblocked", handle)
                        t.show()
        if handle not in self.convos:
            if msg == "PESTERCHUM:CEASE":  # ignore cease after we hang up
                return
            matchingChums = [c for c in self.chumList.chums if c.handle == handle]
            if len(matchingChums) > 0:
                mood = matchingChums[0].mood
            else:
                mood = Mood(0)
            chum = PesterProfile(handle, mood=mood, chumdb=self.chumdb)
            self.newConversation(chum, False)
            if len(matchingChums) == 0:
                self.moodRequest.emit(chum)
        convo = self.convos[handle]
        convo.addMessage(msg, False)
        # play sound here
        if self.config.soundOn():
            if self.config.chatSound() or convo.always_beep:
                if msg in ["PESTERCHUM:CEASE", "PESTERCHUM:BLOCK"]:
                    self.ceasesound.play()
                else:
                    self.alarm.play()

    def newMemoMsg(self, chan, handle, msg):
        if chan not in self.memos:
            # silently ignore in case we forgot to /part
            # TODO: This is really bad practice. Fix it later.
            return
        memo = self.memos[chan]
        msg = str(msg)
        if handle not in memo.times:
            # new chum! time current
            newtime = datetime.timedelta(0)
            time = TimeTracker(newtime)
            memo.times[handle] = time
        if not (msg.startswith("/me") or msg.startswith("PESTERCHUM:ME")):
            msg = addTimeInitial(msg, memo.times[handle].getGrammar())
        if handle == "ChanServ":
            systemColor = QtGui.QColor(self.theme["memos/systemMsgColor"])
            msg = "<c=%s>%s</c>" % (systemColor.name(), msg)
        memo.addMessage(msg, handle)
        mentioned = False
        m = convertTags(msg, "text")
        if m.find(":") <= 3:
            m = m[m.find(":") :]
        for search in self.userprofile.getMentions():
            if re.search(search, m):
                mentioned = True
                break
        if mentioned:
            if self.config.notifyOptions() & self.config.INITIALS:
                t = self.tm.Toast(chan, re.sub("</?c(=.*?)?>", "", msg))
                t.show()

        if self.config.soundOn():
            if self.config.memoSound():
                if self.config.nameSound():
                    if mentioned:
                        self.namesound.play()
                        return
                if not memo.notifications_muted:
                    if self.honk and re.search(
                        r"\bhonk\b", convertTags(msg, "text"), re.I
                    ):
                        # TODO: I've got my eye on you, Gamzee.
                        self.honksound.play()
                    elif self.config.memoPing() or memo.always_beep:
                        self.memosound.play()

    def changeColor(self, handle, color):
        # pesterconvo and chumlist
        self.chumList.updateColor(handle, color)
        if handle in self.convos:
            self.convos[handle].updateColor(color)
        self.chumdb.setColor(handle, color)

    def updateMood(self, handle, mood):
        # updates OTHER chums' moods
        oldmood = self.chumList.updateMood(handle, mood)
        if handle in self.convos:
            self.convos[handle].updateMood(mood, old=oldmood)
        if hasattr(self, "trollslum") and self.trollslum:
            self.trollslum.updateMood(handle, mood)

    def newConversation(self, chum, initiated=True):
        if type(chum) in [str, str]:
            matchingChums = [c for c in self.chumList.chums if c.handle == chum]
            if len(matchingChums) > 0:
                mood = matchingChums[0].mood
            else:
                mood = Mood(2)
            chum = PesterProfile(chum, mood=mood, chumdb=self.chumdb)
            if len(matchingChums) == 0:
                self.moodRequest.emit(chum)

        if chum.handle in self.convos:
            self.convos[chum.handle].showChat()
            return
        if self.config.tabs():
            if not self.tabconvo:
                self.createTabWindow()
            convoWindow = PesterConvo(chum, initiated, self, self.tabconvo)
            self.tabconvo.show()
        else:
            convoWindow = PesterConvo(chum, initiated, self)
        convoWindow.messageSent["QString", "QString"].connect(
            self.sendMessage["QString", "QString"]
        )
        convoWindow.windowClosed["QString"].connect(self.closeConvo)
        self.convos[chum.handle] = convoWindow
        if str(chum.handle).upper() in BOTNAMES:
            convoWindow.toggleQuirks(True)
            convoWindow.quirksOff.setChecked(True)
            if str(chum.handle).upper() in CUSTOMBOTS:
                self.newConvoStarted.emit(QString(chum.handle), initiated)
        else:
            self.newConvoStarted.emit(QString(chum.handle), initiated)
        convoWindow.show()

    def createTabWindow(self):
        self.tabconvo = PesterTabWindow(self)
        self.tabconvo.windowClosed.connect(self.tabsClosed)

    def createMemoTabWindow(self):
        self.tabmemo = MemoTabWindow(self)
        self.tabmemo.windowClosed.connect(self.memoTabsClosed)

    @QtCore.pyqtSlot()
    def toggleConsole(self):
        if not _CONSOLE:
            # We don't have the module file for this at the moment.
            return
        win = self.console.window
        if win is None:
            # We have no console window; make one.
            PchumLog.info("Making a console....")
            self.console.window = win = console.ConsoleWindow(parent=self)
            PchumLog.info("Console made.")
            # 'ConsoleWindow' object has no attribute 'windowClosed'
            win.finished.connect(self.consoleWindowClosed)
            self.console.shortcuts.curwgt.activated.connect(win.designateCurrentWidget)

        if self.console.is_open:
            for wgt in win.findChildren(QtWidgets.QWidget):
                try:
                    focused = wgt.hasFocus()
                except AttributeError:
                    # The widget doesn't have a hasFocus method.
                    # Just to reduce ambiguity
                    focused = False
                    # Try the next one.
                    continue
                # No error, let's see if we're actually focused.
                if focused:
                    PchumLog.debug(
                        "{0!r} is in focus (parent: {1!r}); hiding".format(
                            wgt, wgt.parent()
                        )
                    )
                    # This widget, a child of our console, has focus.
                    # So...the console has focus.
                    # Set focus to the text input just for good measure.
                    win.text.input.setFocus()
                    # ...then hide it all.
                    win.hide()
                    self.console.is_open = False
                    break
            else:
                # The console is open, but not in focus. Bring it to the fore.
                # NOTE: This is a bit of a kludgy method - it may not work
                # properly on Windows. Need to look into workarounds.
                #
                # karxi: I *think* that Windows doesn't mind if the
                # process/window that 'owns' this one changes our focus, since
                # the application ultimately already *has* our focus - but I'm
                # not sure.
                PchumLog.debug("Console isn't in focus; fixing")
                win.raise_()
                win.show()
                win.activateWindow()

                win.text.input.setFocus()
                # No need to explicitly set it as open; it already is.
        else:
            PchumLog.debug("Console not visible; showing")
            # Console isn't visible - show it.
            win.show()
            self.console.is_open = True

    @QtCore.pyqtSlot()
    def consoleWindowClosed(self):
        self.console.is_open = False
        self.console.window = None
        PchumLog.info("Console closed.")

    def newMemo(self, channel, timestr, secret=False, invite=False):
        if channel == "#pesterchum":
            return
        if channel in self.memos:
            self.memos[channel].showChat()
            return
        # do slider dialog then set
        if self.config.tabMemos():
            if not self.tabmemo:
                self.createMemoTabWindow()
            memoWindow = PesterMemo(channel, timestr, self, self.tabmemo)
            self.tabmemo.show()
        else:
            memoWindow = PesterMemo(channel, timestr, self, None)
        # connect signals
        self.inviteOnlyChan["QString"].connect(memoWindow.closeInviteOnly)
        self.forbiddenChan["QString", "QString"].connect(memoWindow.closeForbidden)
        memoWindow.messageSent["QString", "QString"].connect(
            self.sendMessage["QString", "QString"]
        )
        memoWindow.windowClosed["QString"].connect(self.closeMemo)
        self.namesUpdated["QString"].connect(memoWindow.namesUpdated)
        self.modesUpdated["QString", "QString"].connect(memoWindow.modesUpdated)
        self.userPresentSignal["QString", "QString", "QString"].connect(
            memoWindow.userPresentChange
        )
        # chat client send memo open
        self.memos[channel] = memoWindow
        self.joinChannel.emit(channel)  # race condition?
        self.secret = secret
        if self.secret:
            self.secret = True
            self.setChannelMode.emit(channel, "+s", "")
        if invite:
            self.setChannelMode.emit(channel, "+i", "")
        # memoWindow.sendTimeInfo()
        memoWindow.show()

    def addChum(self, chum):
        self.chumList.addChum(chum)
        self.config.addChum(chum)
        self.moodRequest.emit(chum)

    def addGroup(self, gname):
        self.config.addGroup(gname)
        gTemp = self.config.getGroups()
        self.chumList.groups = [g[0] for g in gTemp]
        self.chumList.openGroups = [g[1] for g in gTemp]
        self.chumList.moveGroupMenu()
        self.chumList.showAllGroups()
        if not self.config.showEmptyGroups():
            self.chumList.hideEmptyGroups()
        if self.config.showOnlineNumbers():
            self.chumList.showOnlineNumbers()

    def changeProfile(self, collision=None, svsnick=None):
        if not hasattr(self, "chooseprofile"):
            self.chooseprofile = None
        if not self.chooseprofile:
            self.chooseprofile = PesterChooseProfile(
                self.userprofile,
                self.config,
                self.theme,
                self,
                collision=collision,
                svsnick=svsnick,
            )
            self.chooseprofile.exec()

    def themePicker(self):
        if not hasattr(self, "choosetheme"):
            self.choosetheme = None
        if not self.choosetheme:
            self.choosetheme = PesterChooseTheme(self.config, self.theme, self)
            self.choosetheme.exec()

    def initTheme(self, theme):
        self.resize(*theme["main/size"])
        self.setWindowIcon(PesterIcon(theme["main/icon"]))
        self.setWindowTitle(theme["main/windowtitle"])
        self.setStyleSheet("QtWidgets.QFrame#main { %s }" % (theme["main/style"]))

        self.backgroundImage = QtGui.QPixmap(theme["main/background-image"])
        self.setMask(self.backgroundImage.mask())

        self.menu.setStyleSheet(
            (
                "QMenuBar { background: transparent; %s }"
                "QMenuBar::item { background: transparent; %s }"
            )
            % (theme["main/menubar/style"], theme["main/menu/menuitem"])
            + (
                "QMenu { background: transparent; %s }"
                "QMenu::item::selected { %s }"
                "QMenu::item::disabled { %s }"
            )
            % (
                theme["main/menu/style"],
                theme["main/menu/selected"],
                theme["main/menu/disabled"],
            )
        )
        newcloseicon = PesterIcon(theme["main/close/image"])
        self.closeButton.setIcon(newcloseicon)
        self.closeButton.setIconSize(newcloseicon.realsize())
        self.closeButton.resize(newcloseicon.realsize())
        self.closeButton.move(*theme["main/close/loc"])
        newminiicon = PesterIcon(theme["main/minimize/image"])
        self.miniButton.setIcon(newminiicon)
        self.miniButton.setIconSize(newminiicon.realsize())
        self.miniButton.resize(newminiicon.realsize())
        self.miniButton.move(*theme["main/minimize/loc"])
        # menus
        self.menu.move(*theme["main/menu/loc"])
        self.talk.setText(theme["main/menus/client/talk"])
        self.logv.setText(theme["main/menus/client/logviewer"])
        self.grps.setText(theme["main/menus/client/addgroup"])
        self.rand.setText(self.theme["main/menus/client/randen"])
        self.opts.setText(theme["main/menus/client/options"])
        self.exitaction.setText(theme["main/menus/client/exit"])
        self.userlistaction.setText(theme["main/menus/client/userlist"])
        self.memoaction.setText(theme["main/menus/client/memos"])
        self.importaction.setText(theme["main/menus/client/import"])
        self.idleaction.setText(theme["main/menus/client/idle"])
        self.reconnectAction.setText(theme["main/menus/client/reconnect"])
        self.filemenu.setTitle(theme["main/menus/client/_name"])
        self.changequirks.setText(theme["main/menus/profile/quirks"])
        self.loadslum.setText(theme["main/menus/profile/block"])
        self.changecoloraction.setText(theme["main/menus/profile/color"])
        self.switch.setText(theme["main/menus/profile/switch"])
        self.profilemenu.setTitle(theme["main/menus/profile/_name"])
        self.aboutAction.setText(self.theme["main/menus/help/about"])
        self.helpAction.setText(self.theme["main/menus/help/help"])
        self.botAction.setText(self.theme["main/menus/help/calsprite"])
        self.chanServAction.setText(self.theme["main/menus/help/chanserv"])
        self.nickServAction.setText(self.theme["main/menus/help/nickserv"])
        self.helpmenu.setTitle(self.theme["main/menus/help/_name"])

        # Console
        ##        if self.theme.has_key("main/menus/client/console"):
        ##            self.console.action.setText(self.theme["main/menus/client/console"])
        ##        else:
        ##            self.console.action.setText("Console")
        # has_key doesn't work out here for some reason, possibly because of inherits?
        try:
            self.console.action.setText(self.theme["main/menus/client/console"])
        except:
            self.console.action.setText("Console")

        try:
            self.reportBugAction.setText(self.theme["main/menus/help/reportbug"])
        except:
            self.reportBugAction.setText("REPORT BUG")

        try:
            self.xyzRulesAction.setText(self.theme["main/menus/help/rules"])
        except:
            self.xyzRulesAction.setText("RULES")

        # moods
        self.moodsLabel.setText(theme["main/moodlabel/text"])
        self.moodsLabel.move(*theme["main/moodlabel/loc"])
        self.moodsLabel.setStyleSheet(theme["main/moodlabel/style"])

        if hasattr(self, "moods"):
            self.moods.removeButtons()
        mood_list = theme["main/moods"]
        mood_list = [dict([(str(k), v) for (k, v) in d.items()]) for d in mood_list]
        self.moods = PesterMoodHandler(
            self, *[PesterMoodButton(self, **d) for d in mood_list]
        )
        self.moods.showButtons()
        # chum
        addChumStyle = "QPushButton { %s }" % (theme["main/addchum/style"])
        if "main/addchum/pressed" in theme:
            addChumStyle += "QPushButton:pressed { %s }" % (
                theme["main/addchum/pressed"]
            )
        pesterButtonStyle = "QPushButton { %s }" % (theme["main/pester/style"])
        if "main/pester/pressed" in theme:
            pesterButtonStyle += "QPushButton:pressed { %s }" % (
                theme["main/pester/pressed"]
            )
        blockButtonStyle = "QPushButton { %s }" % (theme["main/block/style"])
        if "main/block/pressed" in theme:
            pesterButtonStyle += "QPushButton:pressed { %s }" % (
                theme["main/block/pressed"]
            )
        self.addChumButton.setText(theme["main/addchum/text"])
        self.addChumButton.resize(*theme["main/addchum/size"])
        self.addChumButton.move(*theme["main/addchum/loc"])
        self.addChumButton.setStyleSheet(addChumStyle)
        self.pesterButton.setText(theme["main/pester/text"])
        self.pesterButton.resize(*theme["main/pester/size"])
        self.pesterButton.move(*theme["main/pester/loc"])
        self.pesterButton.setStyleSheet(pesterButtonStyle)
        self.blockButton.setText(theme["main/block/text"])
        self.blockButton.resize(*theme["main/block/size"])
        self.blockButton.move(*theme["main/block/loc"])
        self.blockButton.setStyleSheet(blockButtonStyle)
        # buttons
        self.mychumhandleLabel.setText(theme["main/mychumhandle/label/text"])
        self.mychumhandleLabel.move(*theme["main/mychumhandle/label/loc"])
        self.mychumhandleLabel.setStyleSheet(theme["main/mychumhandle/label/style"])
        self.mychumhandle.setText(self.profile().handle)
        self.mychumhandle.move(*theme["main/mychumhandle/handle/loc"])
        self.mychumhandle.resize(*theme["main/mychumhandle/handle/size"])
        self.mychumhandle.setStyleSheet(theme["main/mychumhandle/handle/style"])
        self.mychumcolor.resize(*theme["main/mychumhandle/colorswatch/size"])
        self.mychumcolor.move(*theme["main/mychumhandle/colorswatch/loc"])
        self.mychumcolor.setStyleSheet("background: %s" % (self.profile().colorhtml()))
        # I don't know why "if "main/mychumhandle/currentMood" in self.theme:" doesn't work,
        # But this seems to work just as well :3c
        # GWAHH why does inheriting not work with this </3
        # For some reason, this only works on trollian with 'try' :/
        # if self.theme.has_key("main/mychumhandle/currentMood"):
        try:
            moodicon = self.profile().mood.icon(theme)
            if hasattr(self, "currentMoodIcon") and self.currentMoodIcon:
                self.currentMoodIcon.hide()
                self.currentMoodIcon = None
            self.currentMoodIcon = QtWidgets.QLabel(self)
            self.currentMoodIcon.setPixmap(moodicon.pixmap(moodicon.realsize()))
            self.currentMoodIcon.move(*theme["main/mychumhandle/currentMood"])
            self.currentMoodIcon.show()
        except:
            if hasattr(self, "currentMoodIcon") and self.currentMoodIcon:
                self.currentMoodIcon.hide()
            self.currentMoodIcon = None

        # This is a better spot to put this :)
        # Setting QMessageBox's style usually doesn't do anything.
        self.setStyleSheet(
            "QInputDialog { %s } QMessageBox { %s }"
            % (
                self.theme["main/defaultwindow/style"],
                self.theme["main/defaultwindow/style"],
            )
        )

        if theme["main/mychumhandle/colorswatch/text"]:
            self.mychumcolor.setText(theme["main/mychumhandle/colorswatch/text"])
        else:
            self.mychumcolor.setText("")

        self.mychumhandleLabel.adjustSize()  # Required so "CHUMHANDLE:" regardless of style-sheet.
        self.moodsLabel.adjustSize()  # Required so "MOOD:" regardless of style-sheet.

        if _CONSOLE:
            if self.console.window:
                # A bit of an ugly hack....
                self.console.window.changeTheme(theme)

        # sounds
        self._setup_sounds()
        self.setVolume(self.config.volume())

    def _setup_sounds(self, soundclass=None):
        """Set up the event sounds for later use."""
        # Set up the sounds we're using.
        try:
            # Pygame
            soundclass = pygame.mixer.Sound
        except:
            try:
                # QtMultimedia
                soundclass = QtMultimedia.QSoundEffect
            except:
                # death
                soundclass = NoneSound
                PchumLog.warning("No sound module loaded?")

        self.sound_type = soundclass

        # These get redefined if sound works
        self.alarm = NoneSound()
        self.memosound = NoneSound()
        self.namesound = NoneSound()
        self.ceasesound = NoneSound()
        self.honksound = NoneSound()

        # Use the class we chose to build the sound set.
        try:
            if "pygame" in sys.modules:
                if soundclass == pygame.mixer.Sound:
                    self.alarm = soundclass(self.theme["main/sounds/alertsound"])
                    self.memosound = soundclass(self.theme["main/sounds/memosound"])
                    self.namesound = soundclass("themes/namealarm.wav")
                    self.ceasesound = soundclass(self.theme["main/sounds/ceasesound"])
                    self.honksound = soundclass("themes/honk.wav")
            if ("PyQt6.QtMultimedia" in sys.modules) or (
                "PyQt5.QtMultimedia" in sys.modules
            ):
                if soundclass == QtMultimedia.QSoundEffect:
                    self.alarm = soundclass()
                    self.memosound = soundclass()
                    self.namesound = soundclass()
                    self.ceasesound = soundclass()
                    self.honksound = soundclass()

                    self.alarm.setSource(
                        QtCore.QUrl.fromLocalFile(self.theme["main/sounds/alertsound"])
                    )
                    self.memosound.setSource(
                        QtCore.QUrl.fromLocalFile(self.theme["main/sounds/memosound"])
                    )
                    self.namesound.setSource(
                        QtCore.QUrl.fromLocalFile("themes/namealarm.wav")
                    )
                    self.ceasesound.setSource(
                        QtCore.QUrl.fromLocalFile(self.theme["main/sounds/ceasesound"])
                    )
                    self.honksound.setSource(
                        QtCore.QUrl.fromLocalFile("themes/honk.wav")
                    )
        except Exception as err:
            PchumLog.error("Warning: Error loading sounds! ({0!r})".format(err))
            self.alarm = NoneSound()
            self.memosound = NoneSound()
            self.namesound = NoneSound()
            self.ceasesound = NoneSound()
            self.honksound = NoneSound()

        self.sounds = [
            self.alarm,
            self.memosound,
            self.namesound,
            self.ceasesound,
            self.honksound,
        ]

    def setVolume(self, vol_percent):
        vol = vol_percent / 100.0
        for sound in self.sounds:
            try:
                if "pygame" in sys.modules:
                    if self.sound_type == pygame.mixer.Sound:
                        sound.set_volume(vol)
                if ("PyQt6.QtMultimedia" in sys.modules) or (
                    "PyQt5.QtMultimedia" in sys.modules
                ):
                    if self.sound_type == QtMultimedia.QSoundEffect:
                        sound.setVolume(vol)
            except Exception as err:
                PchumLog.warning("Couldn't set volume: {}".format(err))

    def canSetVolume(self):
        """Returns the state of volume setting capabilities."""
        # If the volume can be changed by Pesterchum.
        if self.sound_type is None:
            # We haven't initialized yet.
            return False
        elif self.sound_type == NoneSound:
            # Sound is dead
            return False
        else:
            # We can set volume
            return True

    def changeTheme(self, theme):
        # check theme
        try:
            themeChecker(theme)
        except ThemeException as inst:
            themeWarning = QtWidgets.QMessageBox(self)
            themeWarning.setText("Theme Error: %s" % inst)
            themeWarning.exec()
            theme = pesterTheme("pesterchum")
            return
        self.theme = theme
        # do self
        self.initTheme(theme)
        # set mood
        self.moods.updateMood(theme["main/defaultmood"])
        # chum area
        self.chumList.changeTheme(theme)
        # do open windows
        if self.tabconvo:
            self.tabconvo.changeTheme(theme)
        if self.tabmemo:
            self.tabmemo.changeTheme(theme)
        for c in list(self.convos.values()):
            c.changeTheme(theme)
        for m in list(self.memos.values()):
            m.changeTheme(theme)
        if hasattr(self, "trollslum") and self.trollslum:
            self.trollslum.changeTheme(theme)
        if hasattr(self, "allusers") and self.allusers:
            self.allusers.changeTheme(theme)
        if self.config.ghostchum():
            self.theme["main"]["icon"] = "themes/pesterchum/pesterdunk.png"
            self.theme["main"]["newmsgicon"] = "themes/pesterchum/ghostchum.png"
            self.setWindowIcon(PesterIcon(self.theme["main/icon"]))
        # system tray icon
        self.updateSystemTray()

    def updateSystemTray(self):
        if len(self.waitingMessages) == 0:
            self.trayIconSignal.emit(0)
        else:
            self.trayIconSignal.emit(1)

    def systemTrayFunction(self):
        if len(self.waitingMessages) == 0:
            if self.isMinimized():
                self.showNormal()
            elif self.isHidden():
                self.show()
            else:
                if self.isActiveWindow():
                    self.closeToTray()
                else:
                    self.raise_()
                    self.activateWindow()
        else:
            self.waitingMessages.answerMessage()

    def doAutoIdentify(self):
        if self.userprofile.getAutoIdentify():
            self.sendMessage.emit(
                "identify " + self.userprofile.getNickServPass(), "NickServ"
            )

    def doAutoJoins(self):
        if not self.autoJoinDone:
            self.autoJoinDone = True
            for memo in self.userprofile.getAutoJoins():
                self.newMemo(memo, "i")

    @QtCore.pyqtSlot()
    def connected(self):
        if self.loadingscreen:
            self.loadingscreen.done(QtWidgets.QDialog.DialogCode.Accepted)
        self.loadingscreen = None

        self.doAutoIdentify()
        self.doAutoJoins()

        # Start client --> server pings
        if hasattr(self, "pingtimer"):
            self.pingtimer.start(1000 * 5)  # time in ms
        else:
            PchumLog.warning("No ping timer.")

        # Desync check
        if hasattr(self, "lastCheckPing"):
            self.lastCheckPing = time.time()
        else:
            PchumLog.warning("No ping timer.")

    @QtCore.pyqtSlot()
    def blockSelectedChum(self):
        curChumListing = self.chumList.currentItem()
        if curChumListing:
            curChum = curChumListing.chum
            self.blockChum(curChum.handle)

    @QtCore.pyqtSlot()
    def pesterSelectedChum(self):
        curChum = self.chumList.currentItem()
        if curChum:
            text = str(curChum.text(0))
            if text.rfind(" (") != -1:
                text = text[0 : text.rfind(" (")]
            if text not in self.chumList.groups and text != "Chums":
                self.newConversationWindow(curChum)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def newConversationWindow(self, chumlisting):
        # check chumdb
        chum = chumlisting.chum
        color = self.chumdb.getColor(chum)
        if color:
            chum.color = color
        self.newConversation(chum)

    @QtCore.pyqtSlot(QString)
    def closeConvo(self, handle):
        h = str(handle)
        try:
            chum = self.convos[h].chum
        except KeyError:
            chum = self.convos[h.lower()].chum
        try:
            chumopen = self.convos[h].chumopen
        except KeyError:
            chumopen = self.convos[h.lower()].chumopen
        if chumopen:
            self.chatlog.log(
                chum.handle,
                self.profile().pestermsg(
                    chum,
                    QtGui.QColor(self.theme["convo/systemMsgColor"]),
                    self.theme["convo/text/ceasepester"],
                ),
            )
            self.convoClosed.emit(handle)
        self.chatlog.finish(h)
        del self.convos[h]

    @QtCore.pyqtSlot(QString)
    def closeMemo(self, channel):
        c = str(channel)
        self.chatlog.finish(c)
        self.leftChannel.emit(channel)
        try:
            del self.memos[c]
        except KeyError:
            try:
                del self.memos[c.lower()]
            except KeyError:
                pass

    @QtCore.pyqtSlot()
    def tabsClosed(self):
        del self.tabconvo
        self.tabconvo = None

    @QtCore.pyqtSlot()
    def memoTabsClosed(self):
        del self.tabmemo
        self.tabmemo = None

    @QtCore.pyqtSlot(QString, Mood)
    def updateMoodSlot(self, handle, mood):
        h = str(handle)
        self.updateMood(h, mood)

    @QtCore.pyqtSlot(QString, QtGui.QColor)
    def updateColorSlot(self, handle, color):
        PchumLog.debug("updateColorSlot, " + str(handle) + ", " + str(color))
        h = str(handle)
        self.changeColor(h, color)

    @QtCore.pyqtSlot(QString, QString)
    def deliverMessage(self, handle, msg):
        h = str(handle)
        m = str(msg)
        self.newMessage(h, m)

    @QtCore.pyqtSlot(QString, QString, QString)
    def deliverMemo(self, chan, handle, msg):
        (c, h, m) = (str(chan), str(handle), str(msg))
        self.newMemoMsg(c, h, m)

    @QtCore.pyqtSlot(QString, QString)
    def deliverNotice(self, handle, msg):
        h = str(handle)
        m = str(msg)
        if h.upper() == "NICKSERV" and m.startswith(
            "Your nickname is now being changed to"
        ):
            changedto = m[39:-1]
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
            )
            msgbox.setText(
                "This chumhandle has been registered; " "you may not use it."
            )
            msgbox.setInformativeText(
                "Your handle is now being changed to %s." % (changedto)
            )
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.exec()
        elif h == self.randhandler.randNick:
            self.randhandler.incoming(msg)
        elif h in self.convos:
            self.newMessage(h, m)
        elif h.upper() == "NICKSERV" and "PESTERCHUM:" not in m:
            m = nickservmsgs.translate(m)
            if m:
                t = self.tm.Toast("NickServ:", m)
                t.show()
        elif ("PESTERCHUM:" not in m) and (h.upper() in SERVICES):
            # Show toast for rest services notices
            # "Your VHOST is actived", "You have one new memo", etc.
            t = self.tm.Toast("%s:" % h, m)
            t.show()

    @QtCore.pyqtSlot(QString, QString)
    def deliverInvite(self, handle, channel):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText("You're invited!")
        msgbox.setStyleSheet(
            "QMessageBox{" + self.theme["main/defaultwindow/style"] + "}"
        )
        msgbox.setInformativeText(
            ("%s has invited you to the memo: %s" "\nWould you like to join them?")
            % (handle, channel)
        )
        msgbox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Ok
            | QtWidgets.QMessageBox.StandardButton.Cancel
        )
        # Find the Cancel button and make it default
        for b in msgbox.buttons():
            if msgbox.buttonRole(b) == QtWidgets.QMessageBox.ButtonRole.RejectRole:
                # We found the 'OK' button, set it as the default
                b.setDefault(True)
                b.setAutoDefault(True)
                # Actually set it as the selected option, since we're
                # already stealing focus
                b.setFocus()
                break
        ret = msgbox.exec()
        if ret == QtWidgets.QMessageBox.StandardButton.Ok:
            self.newMemo(str(channel), "+0:00")

    @QtCore.pyqtSlot(QString)
    def chanInviteOnly(self, channel):
        self.inviteOnlyChan.emit(channel)

    @QtCore.pyqtSlot(QString, QString)
    def cannotSendToChan(self, channel, msg):
        self.deliverMemo(channel, "ChanServ", msg)

    # Unused and redefined.
    # @QtCore.pyqtSlot(QString, QString)
    # def modesUpdated(self, channel, modes):
    #    self.modesUpdated.emit(channel, modes)
    @QtCore.pyqtSlot(QString, QString, QString)
    def timeCommand(self, chan, handle, command):
        (c, h, cmd) = (str(chan), str(handle), str(command))
        if self.memos[c]:
            self.memos[c].timeUpdate(h, cmd)

    @QtCore.pyqtSlot(QString, QString, QString)
    def quirkDisable(self, channel, msg, op):
        (c, msg, op) = (str(channel), str(msg), str(op))
        if c not in self.memos:
            return
        memo = self.memos[c]
        memo.quirkDisable(op, msg)

    @QtCore.pyqtSlot(QString, PesterList)
    def updateNames(self, channel, names):
        c = str(channel)
        # update name DB
        self.namesdb[c] = names
        # warn interested party of names
        self.namesUpdated.emit(c)

    @QtCore.pyqtSlot(QString, QString, QString)
    def userPresentUpdate(self, handle, channel, update):
        c = str(channel)
        n = str(handle)
        # print("c=%s\nn=%s\nupdate=%s\n" % (c, n, update))
        if update == "nick":
            l = n.split(":")
            oldnick = l[0]
            newnick = l[1]
        if update in ("quit", "netsplit"):
            for c in list(self.namesdb.keys()):
                try:
                    i = self.namesdb[c].index(n)
                    self.namesdb[c].pop(i)
                except ValueError:
                    pass
                except KeyError:
                    self.namesdb[c] = []
        elif update == "left":
            try:
                i = self.namesdb[c].index(n)
                self.namesdb[c].pop(i)
            except ValueError:
                pass
            except KeyError:
                self.namesdb[c] = []
        elif update == "nick":
            for c in list(self.namesdb.keys()):
                try:
                    i = self.namesdb[c].index(oldnick)
                    self.namesdb[c].pop(i)
                    self.namesdb[c].append(newnick)
                except ValueError:
                    pass
                except KeyError:
                    pass
        elif update == "join":
            # SAJOIN-ed?
            if (n == self.profile().handle) and (c not in self.memos):
                self.newMemo(channel, "+0:00")
            try:
                i = self.namesdb[c].index(n)
            except ValueError:
                self.namesdb[c].append(n)
            except KeyError:
                self.namesdb[c] = [n]

        # PchumLog.debug("handle=%s\nchannel=%s\nupdate=%s\n" % (handle, channel, update))
        self.userPresentSignal.emit(handle, channel, update)

    @QtCore.pyqtSlot()
    def addChumWindow(self):
        if not hasattr(self, "addchumdialog"):
            self.addchumdialog = None
        if not self.addchumdialog:
            available_groups = [g[0] for g in self.config.getGroups()]
            self.addchumdialog = AddChumDialog(available_groups, self)
            ok = self.addchumdialog.exec()
            handle = str(self.addchumdialog.chumBox.text()).strip()
            newgroup = str(self.addchumdialog.newgroup.text()).strip()
            selectedGroup = self.addchumdialog.groupBox.currentText()
            group = newgroup if newgroup else selectedGroup
            if ok:
                handle = str(handle)
                if handle in [h.handle for h in self.chumList.chums]:
                    self.addchumdialog = None
                    return
                if not (
                    PesterProfile.checkLength(handle)
                    and PesterProfile.checkValid(handle)[0]
                ):
                    errormsg = QtWidgets.QErrorMessage(self)
                    errormsg.showMessage("THIS IS NOT A VALID CHUMTAG!")
                    self.addchumdialog = None
                    return
                if re.search("[^A-Za-z0-9_\s]", group) is not None:
                    errormsg = QtWidgets.QErrorMessage(self)
                    errormsg.showMessage("THIS IS NOT A VALID GROUP NAME")
                    self.addchumdialog = None
                    return
                if newgroup:
                    # make new group
                    self.addGroup(group)
                chum = PesterProfile(handle, chumdb=self.chumdb, group=group)
                self.chumdb.setGroup(handle, group)
                self.addChum(chum)
            self.addchumdialog = None

    @QtCore.pyqtSlot(QString)
    def removeChum(self, chumlisting):
        self.config.removeChum(chumlisting)

    def reportChum(self, handle):
        (reason, ok) = QtWidgets.QInputDialog.getText(
            self,
            "Report User",
            "Enter the reason you are reporting this user (optional):",
        )
        if ok:
            self.sendMessage.emit("REPORT %s %s" % (handle, reason), "calSprite")

    @QtCore.pyqtSlot(QString)
    def blockChum(self, handle):
        h = str(handle)
        self.config.addBlocklist(h)
        self.config.removeChum(h)
        if h in self.convos:
            convo = self.convos[h]
            msg = self.profile().pestermsg(
                convo.chum,
                QtGui.QColor(self.theme["convo/systemMsgColor"]),
                self.theme["convo/text/blocked"],
            )
            convo.textArea.append(convertTags(msg))
            self.chatlog.log(convo.chum.handle, msg)
            convo.updateBlocked()
        self.chumList.removeChum(h)
        if hasattr(self, "trollslum") and self.trollslum:
            newtroll = PesterProfile(h)
            self.trollslum.addTroll(newtroll)
            self.moodRequest.emit(newtroll)
        self.blockedChum.emit(handle)

    @QtCore.pyqtSlot(QString)
    def unblockChum(self, handle):
        h = str(handle)
        self.config.delBlocklist(h)
        if h in self.convos:
            convo = self.convos[h]
            msg = self.profile().pestermsg(
                convo.chum,
                QtGui.QColor(self.theme["convo/systemMsgColor"]),
                self.theme["convo/text/unblocked"],
            )
            convo.textArea.append(convertTags(msg))
            self.chatlog.log(convo.chum.handle, msg)
            convo.updateMood(convo.chum.mood, unblocked=True)
        chum = PesterProfile(h, chumdb=self.chumdb)
        if hasattr(self, "trollslum") and self.trollslum:
            self.trollslum.removeTroll(handle)
        self.config.addChum(chum)
        self.chumList.addChum(chum)
        self.moodRequest.emit(chum)
        self.unblockedChum.emit(handle)

    @QtCore.pyqtSlot(bool)
    def toggleIdle(self, idle):
        if idle:
            # We checked the box to go idle.
            self.idler.manual = True
            self.setAway.emit(True)
            self.randhandler.setIdle(True)
            self._sendIdleMsgs()
        else:
            self.idler.manual = False
            self.setAway.emit(False)
            self.randhandler.setIdle(False)
            self.idler.time = 0

    # karxi: TODO: Need to consider sticking an idle-setter here.
    @QtCore.pyqtSlot()
    def checkIdle(self):
        newpos = QtGui.QCursor.pos()
        oldpos = self.idler.pos
        # Save the new position.
        self.idler.pos = newpos

        if self.idler.manual:
            # We're already idle, because the user said to be.
            self.idler.time = 0
            return
        elif self.idler.auto:
            self.idler.time = 0
            if newpos != oldpos:
                # Cursor moved; unset idle.
                self.idler.auto = False
                self.setAway.emit(False)
                self.randhandler.setIdle(False)
            return

        if newpos != oldpos:
            # Our cursor has moved, which means we can't be idle.
            self.idler.time = 0
            return

        # If we got here, WE ARE NOT IDLE, but may become so
        self.idler.time += 1
        if self.idler.time >= self.idler.threshold:
            # We've been idle for long enough to fall automatically idle.
            self.idler.auto = True
            # We don't need this anymore.
            self.idler.time = 0
            # Make it clear that we're idle.
            self.setAway.emit(True)
            self.randhandler.setIdle(True)
            self._sendIdleMsgs()

    def _sendIdleMsgs(self):
        # Tell everyone we're in a chat with that we just went idle.
        sysColor = QtGui.QColor(self.theme["convo/systemMsgColor"])
        verb = self.theme["convo/text/idle"]
        for (h, convo) in self.convos.items():
            # karxi: There's an irritating issue here involving a lack of
            # consideration for case-sensitivity.
            # This fix is a little sloppy, and I need to look into what it
            # might affect, but I've been using it for months and haven't
            # noticed any issues....
            handle = convo.chum.handle
            if self.isBot(handle):
                # Don't send these idle messages.
                continue
            # karxi: Now we just use 'handle' instead of 'h'.
            if convo.chumopen:
                msg = self.profile().idlemsg(sysColor, verb)
                convo.textArea.append(convertTags(msg))
                self.chatlog.log(handle, msg)
                self.sendMessage.emit("PESTERCHUM:IDLE", handle)

    # Presented here so it can be called by other scripts.
    @staticmethod
    def isBot(handle):
        return handle.upper() in BOTNAMES

    @QtCore.pyqtSlot()
    def importExternalConfig(self):
        f = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if f == "":
            return
        fp = open(f, "r")
        regexp_state = None
        for l in fp:
            # import chumlist
            l = l.rstrip()
            chum_mo = re.match("handle: ([A-Za-z0-9]+)", l)
            if chum_mo is not None:
                chum = PesterProfile(chum_mo.group(1))
                self.addChum(chum)
                continue
            if regexp_state is not None:
                replace_mo = re.match("replace: (.+)", l)
                if replace_mo is not None:
                    replace = replace_mo.group(1)
                    try:
                        re.compile(regexp_state)
                    except re.error:
                        continue
                    newquirk = pesterQuirk(
                        {"type": "regexp", "from": regexp_state, "to": replace}
                    )
                    qs = self.userprofile.quirks
                    qs.addQuirk(newquirk)
                    self.userprofile.setQuirks(qs)
                regexp_state = None
                continue
            search_mo = re.match("search: (.+)", l)
            if search_mo is not None:
                regexp_state = search_mo.group(1)
                continue
            other_mo = re.match("(prefix|suffix): (.+)", l)
            if other_mo is not None:
                newquirk = pesterQuirk(
                    {"type": other_mo.group(1), "value": other_mo.group(2)}
                )
                qs = self.userprofile.quirks
                qs.addQuirk(newquirk)
                self.userprofile.setQuirks(qs)

    @QtCore.pyqtSlot()
    def showMemos(self, channel=""):
        if not hasattr(self, "memochooser"):
            self.memochooser = None
        if self.memochooser:
            return
        self.memochooser = PesterMemoList(self, channel)
        self.memochooser.accepted.connect(self.joinSelectedMemo)
        self.memochooser.rejected.connect(self.memoChooserClose)
        self.requestChannelList.emit()
        self.memochooser.show()

    @QtCore.pyqtSlot()
    def joinSelectedMemo(self):

        time = str(self.memochooser.timeinput.text())
        secret = self.memochooser.secretChannel.isChecked()
        invite = self.memochooser.inviteChannel.isChecked()

        # Join the ones on the list first
        for SelectedMemo in self.memochooser.SelectedMemos():
            channel = "#" + str(SelectedMemo.target)
            self.newMemo(channel, time)

        if self.memochooser.newmemoname():
            newmemo = self.memochooser.newmemoname()
            channel = str(newmemo).replace(" ", "_")
            channel = re.sub(r"[^A-Za-z0-9#_\,]", "", channel)
            # Allow us to join more than one with this.
            chans = channel.split(",")
            # Filter out empty entries.
            chans = [_f for _f in chans if _f]
            for c in chans:
                c = "#" + c
                # We should really change this code to only make the memo once
                # the server has confirmed that we've joined....
                self.newMemo(c, time, secret=secret, invite=invite)

        self.memochooser = None

    @QtCore.pyqtSlot()
    def memoChooserClose(self):
        self.memochooser = None

    @QtCore.pyqtSlot(PesterList)
    def updateChannelList(self, channels):
        if hasattr(self, "memochooser") and self.memochooser:
            self.memochooser.updateChannels(channels)

    @QtCore.pyqtSlot()
    def showAllUsers(self):
        if not hasattr(self, "allusers"):
            self.allusers = None
        if not self.allusers:
            self.allusers = PesterUserlist(self.config, self.theme, self)
            self.allusers.accepted.connect(self.userListClose)
            self.allusers.rejected.connect(self.userListClose)
            self.allusers.addChum["QString"].connect(self.userListAdd)
            self.allusers.pesterChum["QString"].connect(self.userListPester)
            self.requestNames.emit("#pesterchum")
            self.allusers.show()

    @QtCore.pyqtSlot(QString)
    def userListAdd(self, handle):
        h = str(handle)
        chum = PesterProfile(h, chumdb=self.chumdb)
        self.addChum(chum)

    @QtCore.pyqtSlot(QString)
    def userListPester(self, handle):
        h = str(handle)
        self.newConversation(h)

    @QtCore.pyqtSlot()
    def userListClose(self):
        self.allusers = None

    @QtCore.pyqtSlot()
    def openQuirks(self):
        if not hasattr(self, "quirkmenu"):
            self.quirkmenu = None
        if not self.quirkmenu:
            self.quirkmenu = PesterChooseQuirks(self.config, self.theme, self)
            self.quirkmenu.accepted.connect(self.updateQuirks)
            self.quirkmenu.rejected.connect(self.closeQuirks)
            self.quirkmenu.show()
            self.quirkmenu.raise_()
            self.quirkmenu.activateWindow()

    @QtCore.pyqtSlot()
    def updateQuirks(self):
        for i in range(self.quirkmenu.quirkList.topLevelItemCount()):
            curgroup = str(self.quirkmenu.quirkList.topLevelItem(i).text(0))
            for j in range(self.quirkmenu.quirkList.topLevelItem(i).childCount()):
                item = self.quirkmenu.quirkList.topLevelItem(i).child(j)
                item.quirk.quirk["on"] = item.quirk.on = (
                    item.checkState(0) == QtCore.Qt.CheckState.Checked
                )
                item.quirk.quirk["group"] = item.quirk.group = curgroup
        quirks = pesterQuirks(self.quirkmenu.quirks())
        self.userprofile.setQuirks(quirks)
        if hasattr(self.quirkmenu, "quirktester") and self.quirkmenu.quirktester:
            self.quirkmenu.quirktester.close()
        self.quirkmenu = None

    @QtCore.pyqtSlot()
    def closeQuirks(self):
        if hasattr(self.quirkmenu, "quirktester") and self.quirkmenu.quirktester:
            self.quirkmenu.quirktester.close()
        self.quirkmenu = None

    @QtCore.pyqtSlot()
    def openChat(self):
        if not hasattr(self, "openchatdialog"):
            self.openchatdialog = None
        if not self.openchatdialog:
            (chum, ok) = QtWidgets.QInputDialog.getText(
                self, "Pester Chum", "Enter a handle to pester:"
            )
            try:
                if ok:
                    self.newConversation(str(chum))
            except:
                pass
            finally:
                self.openchatdialog = None

    @QtCore.pyqtSlot()
    def openLogv(self):
        if not hasattr(self, "logusermenu"):
            self.logusermenu = None
        if not self.logusermenu:
            self.logusermenu = PesterLogUserSelect(self.config, self.theme, self)
            self.logusermenu.accepted.connect(self.closeLogUsers)
            self.logusermenu.rejected.connect(self.closeLogUsers)
            self.logusermenu.show()
            self.logusermenu.raise_()
            self.logusermenu.activateWindow()

    @QtCore.pyqtSlot()
    def closeLogUsers(self):
        self.logusermenu.close()
        self.logusermenu = None

    @QtCore.pyqtSlot()
    def addGroupWindow(self):
        if not hasattr(self, "addgroupdialog"):
            self.addgroupdialog = None
        if not self.addgroupdialog:
            (gname, ok) = QtWidgets.QInputDialog.getText(
                self, "Add Group", "Enter a name for the new group:"
            )
            if ok:
                gname = str(gname)
                if re.search("[^A-Za-z0-9_\s]", gname) is not None:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setInformativeText("THIS IS NOT A VALID GROUP NAME")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    # Style :) (memos/style or convo/style works :3 )
                    msgbox.setStyleSheet(
                        "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
                    )
                    msgbox.exec()
                    self.addgroupdialog = None
                    return
                self.addGroup(gname)
            self.addgroupdialog = None

    @QtCore.pyqtSlot()
    def openOpts(self):
        if not hasattr(self, "optionmenu"):
            self.optionmenu = None
        if not self.optionmenu:
            self.optionmenu = PesterOptions(self.config, self.theme, self)
            self.optionmenu.accepted.connect(self.updateOptions)
            self.optionmenu.rejected.connect(self.closeOptions)
            self.optionmenu.show()
            self.optionmenu.raise_()
            self.optionmenu.activateWindow()

    @QtCore.pyqtSlot()
    def closeOptions(self):
        self.optionmenu.close()
        self.optionmenu = None

    @QtCore.pyqtSlot()
    def updateOptions(self):
        try:
            # tabs
            curtab = self.config.tabs()
            tabsetting = self.optionmenu.tabcheck.isChecked()
            if curtab and not tabsetting:
                # split tabs into windows
                windows = []
                if self.tabconvo:
                    windows = list(self.tabconvo.convos.values())

                for w in windows:
                    w.setParent(None)
                    w.show()
                    w.raiseChat()
                if self.tabconvo:
                    self.tabconvo.closeSoft()
                # save options
                self.config.set("tabs", tabsetting)
            elif tabsetting and not curtab:
                # combine
                self.createTabWindow()
                newconvos = {}
                for (h, c) in self.convos.items():
                    c.setParent(self.tabconvo)
                    self.tabconvo.addChat(c)
                    self.tabconvo.show()
                    newconvos[h] = c
                self.convos = newconvos
                # save options
                self.config.set("tabs", tabsetting)

            # tabs memos
            curtabmemo = self.config.tabMemos()
            tabmemosetting = self.optionmenu.tabmemocheck.isChecked()
            if curtabmemo and not tabmemosetting:
                # split tabs into windows
                windows = []
                if self.tabmemo:
                    windows = list(self.tabmemo.convos.values())

                for w in windows:
                    w.setParent(None)
                    w.show()
                    w.raiseChat()
                if self.tabmemo:
                    self.tabmemo.closeSoft()
                # save options
                self.config.set("tabmemos", tabmemosetting)
            elif tabmemosetting and not curtabmemo:
                # combine
                newmemos = {}
                self.createMemoTabWindow()
                for (h, m) in self.memos.items():
                    m.setParent(self.tabmemo)
                    self.tabmemo.addChat(m)
                    self.tabmemo.show()
                    newmemos[h] = m
                self.memos = newmemos
                # save options
                self.config.set("tabmemos", tabmemosetting)
            # hidden chums
            chumsetting = self.optionmenu.hideOffline.isChecked()
            curchum = self.config.hideOfflineChums()
            if curchum and not chumsetting:
                self.chumList.showAllChums()
            elif chumsetting and not curchum:
                self.chumList.hideOfflineChums()
            self.config.set("hideOfflineChums", chumsetting)
            # sorting method
            sortsetting = self.optionmenu.sortBox.currentIndex()
            cursort = self.config.sortMethod()
            self.config.set("sortMethod", sortsetting)
            if sortsetting != cursort:
                self.chumList.sort()
            # sound
            soundsetting = self.optionmenu.soundcheck.isChecked()
            self.config.set("soundon", soundsetting)
            chatsoundsetting = self.optionmenu.chatsoundcheck.isChecked()
            curchatsound = self.config.chatSound()
            if chatsoundsetting != curchatsound:
                self.config.set("chatSound", chatsoundsetting)
            memosoundsetting = self.optionmenu.memosoundcheck.isChecked()
            curmemosound = self.config.memoSound()
            if memosoundsetting != curmemosound:
                self.config.set("memoSound", memosoundsetting)
            memopingsetting = self.optionmenu.memopingcheck.isChecked()
            curmemoping = self.config.memoPing()
            if memopingsetting != curmemoping:
                self.config.set("pingSound", memopingsetting)
            namesoundsetting = self.optionmenu.namesoundcheck.isChecked()
            curnamesound = self.config.nameSound()
            if namesoundsetting != curnamesound:
                self.config.set("nameSound", namesoundsetting)
            volumesetting = self.optionmenu.volume.value()
            curvolume = self.config.volume()
            if volumesetting != curvolume:
                self.config.set("volume", volumesetting)
                self.setVolume(volumesetting)
            # timestamps
            timestampsetting = self.optionmenu.timestampcheck.isChecked()
            self.config.set("showTimeStamps", timestampsetting)
            timeformatsetting = str(self.optionmenu.timestampBox.currentText())
            if timeformatsetting == "12 hour":
                self.config.set("time12Format", True)
            else:
                self.config.set("time12Format", False)
            secondssetting = self.optionmenu.secondscheck.isChecked()
            self.config.set("showSeconds", secondssetting)
            # groups
            # groupssetting = self.optionmenu.groupscheck.isChecked()
            # self.config.set("useGroups", groupssetting)
            emptygroupssetting = self.optionmenu.showemptycheck.isChecked()
            curemptygroup = self.config.showEmptyGroups()
            if curemptygroup and not emptygroupssetting:
                self.chumList.hideEmptyGroups()
            elif emptygroupssetting and not curemptygroup:
                self.chumList.showAllGroups()
            self.config.set("emptyGroups", emptygroupssetting)
            # online numbers
            onlinenumsetting = self.optionmenu.showonlinenumbers.isChecked()
            curonlinenum = self.config.showOnlineNumbers()
            if onlinenumsetting and not curonlinenum:
                self.chumList.showOnlineNumbers()
            elif curonlinenum and not onlinenumsetting:
                self.chumList.hideOnlineNumbers()
            self.config.set("onlineNumbers", onlinenumsetting)
            # logging
            logpesterssetting = 0
            if self.optionmenu.logpesterscheck.isChecked():
                logpesterssetting = logpesterssetting | self.config.LOG
            if self.optionmenu.stamppestercheck.isChecked():
                logpesterssetting = logpesterssetting | self.config.STAMP
            curlogpesters = self.config.logPesters()
            if logpesterssetting != curlogpesters:
                self.config.set("logPesters", logpesterssetting)
            logmemossetting = 0
            if self.optionmenu.logmemoscheck.isChecked():
                logmemossetting = logmemossetting | self.config.LOG
            if self.optionmenu.stampmemocheck.isChecked():
                logmemossetting = logmemossetting | self.config.STAMP
            curlogmemos = self.config.logMemos()
            if logmemossetting != curlogmemos:
                self.config.set("logMemos", logmemossetting)
            # memo and user links
            linkssetting = self.optionmenu.userlinkscheck.isChecked()
            curlinks = self.config.disableUserLinks()
            if linkssetting != curlinks:
                self.config.set("userLinks", not linkssetting)
            # idle time
            idlesetting = self.optionmenu.idleBox.value()
            curidle = self.config.idleTime()
            if idlesetting != curidle:
                self.config.set("idleTime", idlesetting)
                self.idler.threshold = 60 * idlesetting
            # theme
            ghostchumsetting = self.optionmenu.ghostchum.isChecked()
            curghostchum = self.config.ghostchum()
            self.config.set("ghostchum", ghostchumsetting)
            self.themeSelected(ghostchumsetting != curghostchum)
            # randoms
            if self.randhandler.running:
                self.randhandler.setRandomer(self.optionmenu.randomscheck.isChecked())
            # button actions
            minisetting = self.optionmenu.miniBox.currentIndex()
            curmini = self.config.minimizeAction()
            if minisetting != curmini:
                self.config.set("miniAction", minisetting)
                self.setButtonAction(self.miniButton, minisetting, curmini)
            closesetting = self.optionmenu.closeBox.currentIndex()
            curclose = self.config.closeAction()
            if closesetting != curclose:
                self.config.set("closeAction", closesetting)
                self.setButtonAction(self.closeButton, closesetting, curclose)
            # op and voice messages
            opvmesssetting = self.optionmenu.memomessagecheck.isChecked()
            curopvmess = self.config.opvoiceMessages()
            if opvmesssetting != curopvmess:
                self.config.set("opvMessages", opvmesssetting)
            # animated smiles
            animatesetting = self.optionmenu.animationscheck.isChecked()
            curanimate = self.config.animations()
            if animatesetting != curanimate:
                self.config.set("animations", animatesetting)
                self.animationSetting.emit(animatesetting)
            # update checked
            # updatechecksetting = self.optionmenu.updateBox.currentIndex()
            # curupdatecheck = self.config.checkForUpdates()
            # if updatechecksetting != curupdatecheck:
            #    self.config.set('checkUpdates', updatechecksetting)
            # mspa update check
            # if ostools.isOSXLeopard():
            #    mspachecksetting = false
            # else:
            #    mspachecksetting = self.optionmenu.mspaCheck.isChecked()
            # curmspacheck = self.config.checkMSPA()
            # if mspachecksetting != curmspacheck:
            #    self.config.set('mspa', mspachecksetting)
            # Taskbar blink
            blinksetting = 0
            if self.optionmenu.pesterBlink.isChecked():
                blinksetting |= self.config.PBLINK
            if self.optionmenu.memoBlink.isChecked():
                blinksetting |= self.config.MBLINK
            curblink = self.config.blink()
            if blinksetting != curblink:
                self.config.set("blink", blinksetting)
            # toast notifications
            self.tm.setEnabled(self.optionmenu.notifycheck.isChecked())
            self.tm.setCurrentType(str(self.optionmenu.notifyOptions.currentText()))
            notifysetting = 0
            if self.optionmenu.notifySigninCheck.isChecked():
                notifysetting |= self.config.SIGNIN
            if self.optionmenu.notifySignoutCheck.isChecked():
                notifysetting |= self.config.SIGNOUT
            if self.optionmenu.notifyNewMsgCheck.isChecked():
                notifysetting |= self.config.NEWMSG
            if self.optionmenu.notifyNewConvoCheck.isChecked():
                notifysetting |= self.config.NEWCONVO
            if self.optionmenu.notifyMentionsCheck.isChecked():
                notifysetting |= self.config.INITIALS
            curnotify = self.config.notifyOptions()
            if notifysetting != curnotify:
                self.config.set("notifyOptions", notifysetting)
            # low bandwidth
            bandwidthsetting = self.optionmenu.bandwidthcheck.isChecked()
            curbandwidth = self.config.lowBandwidth()
            if bandwidthsetting != curbandwidth:
                self.config.set("lowBandwidth", bandwidthsetting)
                if bandwidthsetting:
                    self.leftChannel.emit("#pesterchum")
                else:
                    self.joinChannel.emit("#pesterchum")
            # nickserv
            autoidentify = self.optionmenu.autonickserv.isChecked()
            nickservpass = self.optionmenu.nickservpass.text()
            self.userprofile.setAutoIdentify(autoidentify)
            self.userprofile.setNickServPass(str(nickservpass))
            # auto join memos
            autojoins = []
            for i in range(self.optionmenu.autojoinlist.count()):
                autojoins.append(str(self.optionmenu.autojoinlist.item(i).text()))
            self.userprofile.setAutoJoins(autojoins)
            # advanced
            ## user mode
            if self.advanced:
                newmodes = self.optionmenu.modechange.text()
                if newmodes:
                    self.setChannelMode.emit(self.profile().handle, newmodes, "")
        except Exception as e:
            PchumLog.error(e)
        finally:
            self.optionmenu = None

    def setButtonAction(self, button, setting, old):
        if old == 0:  # minimize to taskbar
            button.clicked.disconnect(self.showMinimized)
        elif old == 1:  # minimize to tray
            button.clicked.disconnect(self.closeToTray)
        elif old == 2:  # quit
            button.clicked.disconnect(self.app.quit)

        if setting == 0:  # minimize to taskbar
            button.clicked.connect(self.showMinimized)
        elif setting == 1:  # minimize to tray
            button.clicked.connect(self.closeToTray)
        elif setting == 2:  # quit
            button.clicked.connect(self.app.quit)

    @QtCore.pyqtSlot()
    def themeSelectOverride(self):
        self.themeSelected(self.theme.name)

    @QtCore.pyqtSlot()
    def themeSelected(self, override=False):
        if not override:
            themename = str(self.optionmenu.themeBox.currentText())
        else:
            themename = override
        if override or themename != self.theme.name:
            try:
                self.changeTheme(pesterTheme(themename))
            except ValueError as e:
                themeWarning = QtWidgets.QMessageBox(self)
                themeWarning.setText("Theme Error: %s" % (e))
                themeWarning.exec()
                self.choosetheme = None
                return
            # update profile
            self.userprofile.setTheme(self.theme)
        self.choosetheme = None

    @QtCore.pyqtSlot()
    def closeTheme(self):
        self.choosetheme = None

    @QtCore.pyqtSlot()
    def profileSelected(self):
        if (
            self.chooseprofile.profileBox
            and self.chooseprofile.profileBox.currentIndex() > 0
        ):
            handle = str(self.chooseprofile.profileBox.currentText())
            if handle == self.profile().handle:
                self.chooseprofile = None
                return
            try:
                self.userprofile = userProfile(handle)
                self.changeTheme(self.userprofile.getTheme())
            except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msgBox.setWindowTitle(":(")
                msgBox.setTextFormat(
                    QtCore.Qt.TextFormat.RichText
                )  # Clickable html links
                self.filename = _datadir + "pesterchum.js"
                try:
                    msg = (
                        "<html><h3>Failed to load: "
                        "<a href='%s'>%s/%s.js</a>"
                        "<br><br>"
                        "Try to check for syntax errors if the file exists."
                        "<br><br>"
                        "If you got this message at launch you may want to "
                        "change your default profile."
                        "<br><br>%s<\h3><\html>"
                        % (self.profiledir, self.profiledir, handle, e)
                    )

                except:
                    # More generic error for if not all variables are available.
                    msg = (
                        "Unspecified profile error."
                        "<br><br> Try to check for syntax errors if the "
                        "file exists."
                        "<br><br>If you got this message at launch you may "
                        "want to change your default profile."
                        "<br><br>%s<\h3><\html>" % e
                    )
                PchumLog.critical(e)
                msgBox.setText(msg)
                msgBox.exec()
                return
        else:
            handle = str(self.chooseprofile.chumHandle.text())
            if handle == self.profile().handle:
                self.chooseprofile = None
                return
            profile = PesterProfile(handle, self.chooseprofile.chumcolor)
            self.userprofile = userProfile.newUserProfile(profile)
            self.changeTheme(self.userprofile.getTheme())

        self.chatlog.close()
        self.chatlog = PesterLog(handle, self)

        # is default?
        if self.chooseprofile.defaultcheck.isChecked():
            self.config.set("defaultprofile", self.userprofile.chat.handle)
        if hasattr(self, "trollslum") and self.trollslum:
            self.trollslum.close()
        self.chooseprofile = None
        self.profileChanged.emit()

    @QtCore.pyqtSlot()
    def showTrollSlum(self):
        if not hasattr(self, "trollslum"):
            self.trollslum = None
        if self.trollslum:
            return
        trolls = [PesterProfile(h) for h in self.config.getBlocklist()]
        self.trollslum = TrollSlumWindow(trolls, self)
        self.trollslum.blockChumSignal["QString"].connect(self.blockChum)
        self.trollslum.unblockChumSignal["QString"].connect(self.unblockChum)
        self.moodsRequest.emit(PesterList(trolls))
        self.trollslum.show()

    @QtCore.pyqtSlot()
    def closeTrollSlum(self):
        self.trollslum = None

    @QtCore.pyqtSlot()
    def changeMyColor(self):
        if not hasattr(self, "colorDialog"):
            self.colorDialog = None
        if self.colorDialog:
            return
        self.colorDialog = QtWidgets.QColorDialog(self)
        color = self.colorDialog.getColor(initial=self.profile().color)
        if not color.isValid():
            color = self.profile().color
        self.mychumcolor.setStyleSheet("background: %s" % color.name())
        self.userprofile.setColor(color)
        self.mycolorUpdated.emit()
        self.colorDialog = None

    @QtCore.pyqtSlot()
    def closeProfile(self):
        self.chooseprofile = None

    @QtCore.pyqtSlot()
    def switchProfile(self):
        if self.convos:
            closeWarning = QtWidgets.QMessageBox()
            closeWarning.setText(
                "WARNING: CHANGING PROFILES WILL CLOSE ALL CONVERSATION WINDOWS!"
            )
            closeWarning.setInformativeText(
                "i warned you about windows bro!!!! i told you dog!"
            )
            closeWarning.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Cancel
                | QtWidgets.QMessageBox.StandardButton.Ok
            )
            closeWarning.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            ret = closeWarning.exec()
            if ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
        self.changeProfile()
        # Update RE bot
        try:
            if self.userprofile.getRandom():
                code = "+"
            else:
                code = "-"
            self.sendNotice.emit(code, RANDNICK)
        except:
            PchumLog.warning("No randomEncounter set in userconfig?")
        self.mycolorUpdated.emit()

    def aboutPesterchum(self):
        if hasattr(self, "aboutwindow") and self.aboutwindow:
            return
        self.aboutwindow = AboutPesterchum(self)
        self.aboutwindow.exec()
        self.aboutwindow = None

    @QtCore.pyqtSlot()
    def loadCalsprite(self):
        self.newConversation("calSprite")

    @QtCore.pyqtSlot()
    def loadChanServ(self):
        self.newConversation("chanServ")

    @QtCore.pyqtSlot()
    def loadNickServ(self):
        self.newConversation("nickServ")

    @QtCore.pyqtSlot()
    def launchHelp(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://github.com/Dpeta/pesterchum-alt-servers/issues",
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://forum.homestuck.xyz/viewtopic.php?f=7&t=467",
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )

    @QtCore.pyqtSlot()
    def reportBug(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://github.com/Dpeta/pesterchum-alt-servers/issues",
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )

    @QtCore.pyqtSlot()
    def xyzRules(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://www.pesterchum.xyz/pesterchum-rules",
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )

    @QtCore.pyqtSlot(QString, QString)
    def nickCollision(self, handle, tmphandle):
        if hasattr(self, "loadingscreen"):
            if self.loadingscreen is not None:
                self.loadingscreen.done(QtWidgets.QDialog.DialogCode.Accepted)
                self.loadingscreen = None

        self.mychumhandle.setText(tmphandle)
        self.userprofile = userProfile(
            PesterProfile(
                "pesterClient%d" % (random.randint(100, 999)),
                QtGui.QColor("black"),
                Mood(0),
            )
        )
        self.changeTheme(self.userprofile.getTheme())

        if not hasattr(self, "chooseprofile"):
            self.chooseprofile = None
        if not self.chooseprofile:
            h = str(handle)
            self.changeProfile(collision=h)

    @QtCore.pyqtSlot(QString, QString)
    def getSvsnickedOn(self, oldhandle, newhandle):
        if hasattr(self, "loadingscreen"):
            if self.loadingscreen is not None:
                self.loadingscreen.done(QtWidgets.QDialog.DialogCode.Accepted)
                self.loadingscreen = None

        self.mychumhandle.setText(newhandle)
        self.userprofile = userProfile(
            PesterProfile(newhandle, QtGui.QColor("black"), Mood(0))
        )
        self.changeTheme(self.userprofile.getTheme())

        if not hasattr(self, "chooseprofile"):
            self.chooseprofile = None
        if not self.chooseprofile:
            self.changeProfile(svsnick=(oldhandle, newhandle))

    @QtCore.pyqtSlot(QString)
    def myHandleChanged(self, handle):
        # Update nick in channels
        for memo in self.memos.keys():
            self.requestNames.emit(memo)
        if self.profile().handle == handle:
            self.doAutoIdentify()
            self.doAutoJoins()
            return
        else:
            self.nickCollision(self.profile().handle, handle)

    @QtCore.pyqtSlot()
    def pickTheme(self):
        self.themePicker()

    @QtCore.pyqtSlot(QtWidgets.QSystemTrayIcon.ActivationReason)
    def systemTrayActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.systemTrayFunction()
        # elif reason == QtWidgets.QSystemTrayIcon.Context:
        #    pass
        # show context menu i guess
        # self.showTrayContext.emit()

    @QtCore.pyqtSlot()
    def tooManyPeeps(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setText("D: TOO MANY PEOPLE!!!")
        msg.setInformativeText(
            "The server has hit max capacity." "Please try again later."
        )
        # msg.setStyleSheet("QMessageBox{" + self.theme["main/defaultwindow/style"] + "}")
        msg.exec()

    @QtCore.pyqtSlot(QString, QString)
    def forbiddenchannel(self, channel, reason):
        self.forbiddenChan.emit(channel, reason)

    @QtCore.pyqtSlot()
    def killApp(self):
        self.disconnectIRC.emit()
        self.parent.trayicon.hide()
        self.app.quit()

    def passIRC(self, irc):
        self.irc = irc

    def updateServerJson(self):
        PchumLog.info(self.customServerPrompt_qline.text() + " chosen")
        server_and_port = self.customServerPrompt_qline.text().split(":")
        try:
            server = {
                "server": server_and_port[0],
                "port": int(
                    server_and_port[1]
                ),  # to make sure port is a valid integer, and raise an exception if it cannot be converted.
                "TLS": self.TLS_checkbox.isChecked(),
            }
            PchumLog.info("server:    " + str(server))
        except:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
            )
            msgbox.setWindowIcon(PesterIcon(self.theme["main/icon"]))
            msgbox.setInformativeText("Incorrect format :(")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.exec()
            self.chooseServer()
            return 1

        with open(_datadir + "serverlist.json", "r") as server_file:
            read_file = server_file.read()
            server_file.close()
            server_list_obj = json.loads(read_file)
        server_list_obj.append(server)
        try:
            with open(_datadir + "serverlist.json", "w") as server_file:
                server_file.write(json.dumps(server_list_obj, indent=4))
                server_file.close()
        except:
            PchumLog.error("failed")

        # Go back to original screen
        self.chooseServer()

    def resetServerlist(self):
        default_server_list = [
            {"server": "irc.pesterchum.xyz", "port": "6697", "TLS": True}
        ]
        if os.path.isfile(_datadir + "serverlist.json"):
            PchumLog.error("Failed to load server list from serverlist.json.")
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
            )
            msgbox.setWindowIcon(PesterIcon(self.theme["main/icon"]))
            msgbox.setInformativeText(
                "Failed to load server list, do you want to revert to defaults?\n"
                "If you choose no, Pesterchum will most likely crash unless you manually fix serverlist.json\n"
                "Please tell me if this error occurs :'3"
            )
            msgbox.addButton(
                QtWidgets.QPushButton("Yes"), QtWidgets.QMessageBox.ButtonRole.YesRole
            )
            msgbox.addButton(
                QtWidgets.QPushButton("No"), QtWidgets.QMessageBox.ButtonRole.NoRole
            )
            reply = msgbox.exec()

            if reply == QtWidgets.QMessageBox.ButtonRole.YesRole:
                with open(_datadir + "serverlist.json", "w") as server_file:
                    server_file.write(json.dumps(default_server_list, indent=4))
                    server_file.close()

        else:
            PchumLog.warning(
                "Failed to load server list because serverlist.json doesn't exist, "
                "this isn't an issue if this is the first time Pesterchum has been started."
            )
            with open(_datadir + "serverlist.json", "w") as server_file:
                server_file.write(json.dumps(default_server_list, indent=4))
                server_file.close()
        self.chooseServer()

    def removeServer(self):
        server_list_items = []
        try:
            with open(_datadir + "serverlist.json", "r") as server_file:
                read_file = server_file.read()
                server_file.close()
                server_list_obj = json.loads(read_file)
            for i in range(len(server_list_obj)):
                server_list_items.append(server_list_obj[i]["server"])
        except:
            if not self.chooseServerAskedToReset:
                self.chooseServerAskedToReset = True
                self.resetServerlist()
                return 1

        selected_entry = None

        for i in range(len(server_list_obj)):
            if server_list_obj[i]["server"] == self.removeServerBox.currentText():
                selected_entry = i
        if selected_entry is not None:
            server_list_obj.pop(selected_entry)

            try:
                with open(_datadir + "serverlist.json", "w") as server_file:
                    server_file.write(json.dumps(server_list_obj, indent=4))
                    server_file.close()
            except:
                PchumLog.error("failed")

        self.chooseServer()

    def setServer(self):
        if self.serverBox.currentText() == "Add a server [Prompt]":
            # Text input
            self.customServerPrompt_qline = QtWidgets.QLineEdit(self)
            self.customServerPrompt_qline.setMinimumWidth(200)

            # Widget 1
            self.customServerDialog = QtWidgets.QDialog()

            # Buttons
            cancel = QtWidgets.QPushButton("CANCEL")
            ok = QtWidgets.QPushButton("OK")

            ok.setDefault(True)
            ok.clicked.connect(self.customServerDialog.accept)
            cancel.clicked.connect(self.customServerDialog.reject)

            # Layout
            layout = QtWidgets.QHBoxLayout()

            self.TLS_checkbox = QtWidgets.QCheckBox(self)
            self.TLS_checkbox.setChecked(True)
            TLS_checkbox_label = QtWidgets.QLabel(
                ":33 < Check if you want to connect over TLS!!"
            )
            TLS_checkbox_label.setStyleSheet(
                "QLabel { color: #416600; font-weight: bold;}"
            )
            TLS_layout = QtWidgets.QHBoxLayout()
            TLS_layout.addWidget(TLS_checkbox_label)
            TLS_layout.addWidget(self.TLS_checkbox)

            layout.addWidget(cancel)
            layout.addWidget(ok)
            main_layout = QtWidgets.QVBoxLayout()
            nep_prompt = QtWidgets.QLabel(
                ":33 < Please put in the server's address in the format HOSTNAME:PORT\n:33 < Fur example, irc.pesterchum.xyz:6697"
            )
            nep_prompt.setStyleSheet("QLabel { color: #416600; font-weight: bold;}")
            main_layout.addWidget(nep_prompt)
            main_layout.addWidget(self.customServerPrompt_qline)
            main_layout.addLayout(TLS_layout)
            main_layout.addLayout(layout)

            self.customServerDialog.setLayout(main_layout)

            # Theme
            self.customServerDialog.setStyleSheet(
                self.theme["main/defaultwindow/style"]
            )
            self.customServerDialog.setWindowIcon(PesterIcon(self.theme["main/icon"]))

            # Connect
            self.customServerDialog.accepted.connect(self.updateServerJson)
            self.customServerDialog.rejected.connect(self.chooseServer)

            # Show
            self.customServerDialog.show()
            self.customServerDialog.setFocus()

        elif self.serverBox.currentText() == "Remove a server [Prompt]":
            # Read servers.
            server_list_items = []
            try:
                with open(_datadir + "serverlist.json", "r") as server_file:
                    read_file = server_file.read()
                    server_file.close()
                    server_obj = json.loads(read_file)
                for i in range(len(server_obj)):
                    server_list_items.append(server_obj[i]["server"])
            except:
                if not self.chooseServerAskedToReset:
                    self.chooseServerAskedToReset = True
                    self.resetServerlist()
                    return 1

            PchumLog.info("server_list_items:    " + str(server_list_items))

            # Widget 1
            self.chooseRemoveServerWidged = QtWidgets.QDialog()

            # removeServerBox
            self.removeServerBox = QtWidgets.QComboBox()

            for i in range(len(server_list_items)):
                self.removeServerBox.addItem(server_list_items[i])

            # Buttons
            cancel = QtWidgets.QPushButton("CANCEL")
            ok = QtWidgets.QPushButton("OK")

            ok.setDefault(True)
            ok.clicked.connect(self.chooseRemoveServerWidged.accept)
            cancel.clicked.connect(self.chooseRemoveServerWidged.reject)

            # Layout
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(cancel)
            layout.addWidget(ok)
            main_layout = QtWidgets.QVBoxLayout()
            main_layout.addWidget(QtWidgets.QLabel("Please choose a server to remove."))
            main_layout.addWidget(self.removeServerBox)
            main_layout.addLayout(layout)

            self.chooseRemoveServerWidged.setLayout(main_layout)

            # Theme
            self.chooseRemoveServerWidged.setStyleSheet(
                self.theme["main/defaultwindow/style"]
            )
            self.chooseRemoveServerWidged.setWindowIcon(
                PesterIcon(self.theme["main/icon"])
            )

            # Connect
            self.chooseRemoveServerWidged.accepted.connect(self.removeServer)
            self.chooseRemoveServerWidged.rejected.connect(self.chooseServer)

            # Show
            self.chooseRemoveServerWidged.show()
            self.chooseRemoveServerWidged.setFocus()
        else:
            PchumLog.info(self.serverBox.currentText() + " chosen.")

            with open(_datadir + "serverlist.json", "r") as server_file:
                read_file = server_file.read()
                server_file.close()
                server_obj = json.loads(read_file)

            selected_entry = None

            for i in range(len(server_obj)):
                if server_obj[i]["server"] == self.serverBox.currentText():
                    selected_entry = i

            try:
                with open(_datadir + "server.json", "w") as server_file:
                    json_server_file = {
                        "server": server_obj[selected_entry]["server"],
                        "port": server_obj[selected_entry]["port"],
                        "TLS": server_obj[selected_entry]["TLS"],
                    }
                    server_file.write(json.dumps(json_server_file, indent=4))
                    server_file.close()
            except:
                PchumLog.error("Failed to set server :(")

            # Continue running Pesterchum as usual
            # Sorry-
            self.irc.start()
            self.parent.reconnectok = False
            self.parent.showLoading(self.parent.widget)
            self.show()  # Not required?
            self.setFocus()

    def chooseServer(self):
        # Read servers.
        server_list_items = []
        try:
            with open(_datadir + "serverlist.json", "r") as server_file:
                read_file = server_file.read()
                server_file.close()
                server_obj = json.loads(read_file)
            for i in range(len(server_obj)):
                server_list_items.append(server_obj[i]["server"])
        except:
            if not self.chooseServerAskedToReset:
                self.chooseServerAskedToReset = True
                self.resetServerlist()
                return 1

        PchumLog.info("server_list_items:    " + str(server_list_items))

        # Widget 1
        self.chooseServerWidged = QtWidgets.QDialog()

        # Serverbox
        self.serverBox = QtWidgets.QComboBox()

        for i in range(len(server_list_items)):
            self.serverBox.addItem(server_list_items[i])

        self.serverBox.addItem("Add a server [Prompt]")
        self.serverBox.addItem("Remove a server [Prompt]")

        # Buttons
        cancel = QtWidgets.QPushButton("CANCEL")
        ok = QtWidgets.QPushButton("OK")

        ok.setDefault(True)
        ok.clicked.connect(self.chooseServerWidged.accept)
        cancel.clicked.connect(self.chooseServerWidged.reject)

        # Layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(cancel)
        layout.addWidget(ok)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel("Please choose a server."))
        main_layout.addWidget(self.serverBox)
        main_layout.addLayout(layout)

        self.chooseServerWidged.setLayout(main_layout)

        # Theme
        self.chooseServerWidged.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.chooseServerWidged.setWindowIcon(PesterIcon(self.theme["main/icon"]))

        # Connect
        self.chooseServerWidged.accepted.connect(self.setServer)
        self.chooseServerWidged.rejected.connect(
            self.killApp, QtCore.Qt.ConnectionType.QueuedConnection
        )

        # Show
        self.chooseServerWidged.show()
        self.chooseServerWidged.setFocus()

    @QtCore.pyqtSlot(Exception)
    def connectAnyway(self, e):
        # Prompt user to connect anyway
        msgbox = QtWidgets.QMessageBox()
        try:
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.theme["main/defaultwindow/style"]
            )
        except:
            pass
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgbox.setText("Server certificate validation failed")
        msgbox.setInformativeText(
            'Reason: "%s (%s)"' % (e.verify_message, e.verify_code)
            + "\n\nConnect anyway?"
        )
        msgbox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        ret = msgbox.exec()
        if ret == QtWidgets.QMessageBox.StandardButton.Yes:
            self.parent.restartIRC(verify_hostname=False)

    pcUpdate = QtCore.pyqtSignal("QString", "QString")
    closeToTraySignal = QtCore.pyqtSignal()
    newConvoStarted = QtCore.pyqtSignal("QString", bool, name="newConvoStarted")
    sendMessage = QtCore.pyqtSignal("QString", "QString")
    sendNotice = QtCore.pyqtSignal("QString", "QString")
    sendCTCP = QtCore.pyqtSignal("QString", "QString")
    convoClosed = QtCore.pyqtSignal("QString")
    profileChanged = QtCore.pyqtSignal()
    animationSetting = QtCore.pyqtSignal(bool)
    moodRequest = QtCore.pyqtSignal(PesterProfile)
    moodsRequest = QtCore.pyqtSignal(PesterList)
    moodUpdated = QtCore.pyqtSignal()
    requestChannelList = QtCore.pyqtSignal()
    requestNames = QtCore.pyqtSignal("QString")
    namesUpdated = QtCore.pyqtSignal("QString")
    modesUpdated = QtCore.pyqtSignal("QString", "QString")
    userPresentSignal = QtCore.pyqtSignal("QString", "QString", "QString")
    mycolorUpdated = QtCore.pyqtSignal()
    trayIconSignal = QtCore.pyqtSignal(int)
    blockedChum = QtCore.pyqtSignal("QString")
    unblockedChum = QtCore.pyqtSignal("QString")
    kickUser = QtCore.pyqtSignal("QString", "QString")
    joinChannel = QtCore.pyqtSignal("QString")
    leftChannel = QtCore.pyqtSignal("QString")
    setChannelMode = QtCore.pyqtSignal("QString", "QString", "QString")
    channelNames = QtCore.pyqtSignal("QString")
    inviteChum = QtCore.pyqtSignal("QString", "QString")
    inviteOnlyChan = QtCore.pyqtSignal("QString")
    forbiddenChan = QtCore.pyqtSignal("QString", "QString")
    closeSignal = QtCore.pyqtSignal()
    disconnectIRC = QtCore.pyqtSignal()
    gainAttention = QtCore.pyqtSignal(QtWidgets.QWidget)
    pingServer = QtCore.pyqtSignal()
    setAway = QtCore.pyqtSignal(bool)
    killSomeQuirks = QtCore.pyqtSignal("QString", "QString")


class PesterTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, mainwindow, parent):
        super(PesterTray, self).__init__(icon, parent)
        self.mainwindow = mainwindow

    @QtCore.pyqtSlot(int)
    def changeTrayIcon(self, i):
        if i == 0:
            self.setIcon(PesterIcon(self.mainwindow.theme["main/icon"]))
        else:
            self.setIcon(PesterIcon(self.mainwindow.theme["main/newmsgicon"]))

    @QtCore.pyqtSlot()
    def mainWindowClosed(self):
        self.hide()


class MainProgram(QtCore.QObject):
    def __init__(self):
        super(MainProgram, self).__init__()

        _oldhook = sys.excepthook
        sys.excepthook = self.uncaughtException

        if os.name.upper() == "NT":
            # karxi: Before we do *anything* else, we have to make a special
            # exception for Windows. Otherwise, the icon won't work properly.
            # NOTE: This is presently being tested, since I don't have a
            # Windows computer at the moment. Hopefully it'll work.
            # See https://stackoverflow.com/a/1552105 for more details.
            from ctypes import windll

            # Note that this has to be unicode.
            wid = "mspa.homestuck.pesterchum.314"
            # Designate this as a separate process - i.e., tell Windows that
            # Python is just hosting Pesterchum.
            # TODO: Eventually we should get this changed so it checks and
            # restores the old ID upon exit, but this usually doesn't matter -
            # most users won't keep the process running once Pesterchum closes.
            try:
                windll.shell32.SetCurrentProcessExplicitAppUserModelID(wid)
            except Exception as err:
                # Log, but otherwise ignore any exceptions.
                PchumLog.error("Failed to set AppUserModel ID: {0}".format(err))
                PchumLog.error("Attempted to set as {0!r}.".format(wid))
            # Back to our scheduled program.

        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Pesterchum")
        # self.app.setQuitOnLastWindowClosed(False)

        options = self.oppts(sys.argv[1:])

        # Check if the user is a silly little guy
        for folder in ["smilies", "themes"]:
            if not os.path.isdir(folder):
                msgbox = QtWidgets.QMessageBox()
                msg = (
                    "'%s' folder not found, Pesterchum will "
                    "probably not function correctly."
                    "\nIf this is an excecutable build, "
                    "verify you extracted the zipfile." % folder
                )
                msgbox.setWindowTitle("SK1LL 1SSU3 >:[")
                msgbox.setInformativeText(msg)
                msgbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msgbox.exec()

        # If we're using pygame for sound we need to init
        if "pygame" in sys.modules:
            # we could set the frequency higher but i love how cheesy it sounds
            try:
                pygame.mixer.init()
            except (pygame.error, Exception) as err:
                print("Warning: No sound! (pygame error: %s)" % err)

        self.widget = PesterWindow(options, parent=self, app=self.app)
        # self.widget.show() <== Already called in showLoading()

        self.trayicon = PesterTray(
            PesterIcon(self.widget.theme["main/icon"]), self.widget, self.app
        )
        self.traymenu = QtWidgets.QMenu()

        moodMenu = self.traymenu.addMenu("SET MOOD")
        moodCategories = {}
        for k in Mood.moodcats:
            moodCategories[k] = moodMenu.addMenu(k.upper())
        self.moodactions = {}
        for (i, m) in enumerate(Mood.moods):
            maction = QAction(m.upper(), self)
            mobj = PesterMoodAction(i, self.widget.moods.updateMood)
            maction.triggered.connect(mobj.updateMood)
            self.moodactions[i] = mobj
            moodCategories[Mood.revmoodcats[m]].addAction(maction)
        miniAction = QAction("MINIMIZE", self)
        miniAction.triggered.connect(self.widget.showMinimized)
        exitAction = QAction("EXIT", self)
        exitAction.triggered.connect(
            self.widget.killApp, QtCore.Qt.ConnectionType.QueuedConnection
        )
        self.traymenu.addAction(miniAction)
        self.traymenu.addAction(exitAction)

        self.trayicon.setContextMenu(self.traymenu)
        self.trayicon.show()
        self.trayicon.activated[QtWidgets.QSystemTrayIcon.ActivationReason].connect(
            self.widget.systemTrayActivated
        )
        self.widget.trayIconSignal[int].connect(self.trayicon.changeTrayIcon)
        self.widget.closeToTraySignal.connect(self.trayiconShow)
        self.widget.closeSignal.connect(self.trayicon.mainWindowClosed)
        self.trayicon.messageClicked.connect(self.trayMessageClick)

        self.attempts = 0

        # but it's at least better than the way it was before.
        self.irc = PesterIRC(self.widget.config, self.widget)
        self.connectWidgets(self.irc, self.widget)

        self.widget.passIRC(
            self.irc
        )  # Maybe this is absolutely terrible in practice, but screw it.
        self.widget.gainAttention[QtWidgets.QWidget].connect(self.alertWindow)

        # self.app.lastWindowClosed.connect(self.lastWindow)
        self.app.aboutToQuit.connect(self.death)

    def death(self):
        # app murder in progress
        # print("death inbound")
        if hasattr(self, "widget"):
            self.widget.killApp()

    # def lastWindow(self):
    #    print("all windows closed")
    #    if hasattr(self, 'widget'):
    #        self.widget.killApp()

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def alertWindow(self, widget):
        self.app.alert(widget)

    @QtCore.pyqtSlot()
    def trayiconShow(self):
        self.trayicon.show()
        if self.widget.config.trayMessage():
            self.trayicon.showMessage(
                "Pesterchum",
                (
                    "Pesterchum is still running in the system tray."
                    "\n"
                    "Right click to close it."
                ),
            )

    @QtCore.pyqtSlot()
    def trayMessageClick(self):
        self.widget.config.set("traymsg", False)

    widget2irc = [
        ("sendMessage(QString, QString)", "sendMessage(QString, QString)"),
        ("sendNotice(QString, QString)", "sendNotice(QString, QString)"),
        ("sendCTCP(QString, QString)", "sendCTCP(QString, QString)"),
        ("newConvoStarted(QString, bool)", "startConvo(QString, bool)"),
        ("convoClosed(QString)", "endConvo(QString)"),
        ("profileChanged()", "updateProfile()"),
        ("moodRequest(PyQt_PyObject)", "getMood(PyQt_PyObject)"),
        ("moodsRequest(PyQt_PyObject)", "getMoods(PyQt_PyObject)"),
        ("moodUpdated()", "updateMood()"),
        ("mycolorUpdated()", "updateColor()"),
        ("blockedChum(QString)", "blockedChum(QString)"),
        ("unblockedChum(QString)", "unblockedChum(QString)"),
        ("requestNames(QString)", "requestNames(QString)"),
        ("requestChannelList()", "requestChannelList()"),
        ("joinChannel(QString)", "joinChannel(QString)"),
        ("leftChannel(QString)", "leftChannel(QString)"),
        ("kickUser(QString, QString)", "kickUser(QString, QString)"),
        (
            "setChannelMode(QString, QString, QString)",
            "setChannelMode(QString, QString, QString)",
        ),
        ("channelNames(QString)", "channelNames(QString)"),
        ("inviteChum(QString, QString)", "inviteChum(QString, QString)"),
        ("pingServer()", "pingServer()"),
        ("setAway(bool)", "setAway(bool)"),
        ("killSomeQuirks(QString, QString)", "killSomeQuirks(QString, QString)"),
        ("disconnectIRC()", "disconnectIRC()"),
    ]
    # IRC --> Main window
    irc2widget = [
        ("connected()", "connected()"),
        (
            "moodUpdated(QString, PyQt_PyObject)",
            "updateMoodSlot(QString, PyQt_PyObject)",
        ),
        (
            "colorUpdated(QString, QtGui.QColor)",
            "updateColorSlot(QString, QtGui.QColor)",
        ),
        ("messageReceived(QString, QString)", "deliverMessage(QString, QString)"),
        (
            "memoReceived(QString, QString, QString)",
            "deliverMemo(QString, QString, QString)",
        ),
        ("noticeReceived(QString, QString)", "deliverNotice(QString, QString)"),
        ("inviteReceived(QString, QString)", "deliverInvite(QString, QString)"),
        ("nickCollision(QString, QString)", "nickCollision(QString, QString)"),
        ("getSvsnickedOn(QString, QString)", "getSvsnickedOn(QString, QString)"),
        ("myHandleChanged(QString)", "myHandleChanged(QString)"),
        (
            "namesReceived(QString, PyQt_PyObject)",
            "updateNames(QString, PyQt_PyObject)",
        ),
        (
            "userPresentUpdate(QString, QString, QString)",
            "userPresentUpdate(QString, QString, QString)",
        ),
        ("channelListReceived(PyQt_PyObject)", "updateChannelList(PyQt_PyObject)"),
        (
            "timeCommand(QString, QString, QString)",
            "timeCommand(QString, QString, QString)",
        ),
        ("chanInviteOnly(QString)", "chanInviteOnly(QString)"),
        ("modesUpdated(QString, QString)", "modesUpdated(QString, QString)"),
        ("cannotSendToChan(QString, QString)", "cannotSendToChan(QString, QString)"),
        ("tooManyPeeps()", "tooManyPeeps()"),
        (
            "quirkDisable(QString, QString, QString)",
            "quirkDisable(QString, QString, QString)",
        ),
        ("forbiddenchannel(QString)", "forbiddenchannel(QString)"),
    ]

    def ircQtConnections(self, irc, widget):
        # IRC --> Main window
        return (
            (widget.sendMessage, irc.sendMessage),
            (widget.sendNotice, irc.sendNotice),
            (widget.sendCTCP, irc.sendCTCP),
            (widget.newConvoStarted, irc.startConvo),
            (widget.convoClosed, irc.endConvo),
            (widget.profileChanged, irc.updateProfile),
            (widget.moodRequest, irc.getMood),
            (widget.moodsRequest, irc.getMoods),
            (widget.moodUpdated, irc.updateMood),
            (widget.mycolorUpdated, irc.updateColor),
            (widget.blockedChum, irc.blockedChum),
            (widget.unblockedChum, irc.unblockedChum),
            (widget.requestNames, irc.requestNames),
            (widget.requestChannelList, irc.requestChannelList),
            (widget.joinChannel, irc.joinChannel),
            (widget.leftChannel, irc.leftChannel),
            (widget.kickUser, irc.kickUser),
            (widget.setChannelMode, irc.setChannelMode),
            (widget.channelNames, irc.channelNames),
            (widget.inviteChum, irc.inviteChum),
            (widget.pingServer, irc.pingServer),
            (widget.setAway, irc.setAway),
            (widget.killSomeQuirks, irc.killSomeQuirks),
            (widget.disconnectIRC, irc.disconnectIRC),
            # Main window --> IRC
            (irc.connected, widget.connected),
            (irc.askToConnect, widget.connectAnyway),
            (irc.moodUpdated, widget.updateMoodSlot),
            (irc.colorUpdated, widget.updateColorSlot),
            (irc.messageReceived, widget.deliverMessage),
            (irc.memoReceived, widget.deliverMemo),
            (irc.noticeReceived, widget.deliverNotice),
            (irc.inviteReceived, widget.deliverInvite),
            (irc.nickCollision, widget.nickCollision),
            (irc.getSvsnickedOn, widget.getSvsnickedOn),
            (irc.myHandleChanged, widget.myHandleChanged),
            (irc.namesReceived, widget.updateNames),
            (irc.userPresentUpdate, widget.userPresentUpdate),
            (irc.channelListReceived, widget.updateChannelList),
            (irc.timeCommand, widget.timeCommand),
            (irc.chanInviteOnly, widget.chanInviteOnly),
            (irc.modesUpdated, widget.modesUpdated),
            (irc.cannotSendToChan, widget.cannotSendToChan),
            (irc.forbiddenchannel, widget.forbiddenchannel),
            (irc.tooManyPeeps, widget.tooManyPeeps),
            (irc.quirkDisable, widget.quirkDisable),
        )

    def connectWidgets(self, irc, widget):
        irc.finished.connect(self.restartIRC)
        irc.connected.connect(self.connected)
        for sig, slot in self.ircQtConnections(irc, widget):
            sig.connect(slot)

    def disconnectWidgets(self, irc, widget):
        for sig, slot in self.ircQtConnections(irc, widget):
            sig.disconnect(slot)
        irc.connected.disconnect(self.connected)
        self.irc.finished.disconnect(self.restartIRC)

    def showUpdate(self, q):
        new_url = q.get()
        if new_url[0]:
            self.widget.pcUpdate.emit(new_url[0], new_url[1])
        q.task_done()

    def showLoading(self, widget, msg="CONN3CT1NG"):
        self.widget.show()
        if len(msg) > 60:
            newmsg = []
            while len(msg) > 60:
                s = msg.rfind(" ", 0, 60)
                if s == -1:
                    break
                newmsg.append(msg[:s])
                newmsg.append("\n")
                msg = msg[s + 1 :]
            newmsg.append(msg)
            msg = "".join(newmsg)
        if hasattr(self.widget, "loadingscreen") and widget.loadingscreen:
            widget.loadingscreen.loadinglabel.setText(msg)
            if self.reconnectok:
                widget.loadingscreen.showReconnect()
            else:
                widget.loadingscreen.hideReconnect()
        else:
            widget.loadingscreen = LoadingScreen(widget)
            widget.loadingscreen.loadinglabel.setText(msg)
            widget.loadingscreen.rejected.connect(widget.app.quit)
            self.widget.loadingscreen.tryAgain.connect(self.tryAgain)
            if (
                hasattr(self, "irc")
                and self.irc.registeredIRC
                and not self.irc.unresponsive
            ):
                return
            if self.reconnectok:
                widget.loadingscreen.showReconnect()
            else:
                widget.loadingscreen.hideReconnect()
            widget.loadingscreen.open()

    @QtCore.pyqtSlot()
    def connected(self):
        self.attempts = 0

    @QtCore.pyqtSlot()
    def tryAgain(self):
        if not self.reconnectok:
            return
        if self.widget.loadingscreen:
            self.widget.loadingscreen.done(QtWidgets.QDialog.DialogCode.Accepted)
            self.widget.loadingscreen = None
        self.attempts += 1
        if hasattr(self, "irc") and self.irc:
            self.irc.disconnectIRC()
        else:
            self.restartIRC()

    @QtCore.pyqtSlot()
    def restartIRC(self, verify_hostname=True):
        if hasattr(self, "irc") and self.irc:
            self.disconnectWidgets(self.irc, self.widget)
            stop = self.irc.stopIRC
            del self.irc
        else:
            stop = None
        if stop is None:
            self.irc = PesterIRC(
                self.widget.config, self.widget, verify_hostname=verify_hostname
            )
            self.connectWidgets(self.irc, self.widget)
            self.irc.start()
            if self.attempts == 1:
                msg = "R3CONN3CT1NG"
            elif self.attempts > 1:
                msg = "R3CONN3CT1NG %d" % (self.attempts)
            else:
                msg = "CONN3CT1NG"
            self.reconnectok = False
            self.showLoading(self.widget, msg)
        else:
            self.reconnectok = True
            self.showLoading(self.widget, "F41L3D: %s" % stop)

    def oppts(self, argv):
        options = {}
        # The parser and arguments are defined globally,
        # since --help causes Qt to raise an exception otherwise.
        args = _ARGUMENTS
        try:
            if args.server is not None:
                options["server"] = args.server
            if args.port is not None:
                options["port"] = args.port
            # Set log level
            PchumLog.setLevel(args.logging.upper())
            file_handler.setLevel(args.logging.upper())
            stream_handler.setLevel(args.logging.upper())
            # Enable advanced
            options["advanced"] = args.advanced
            # Disable honks
            if args.nohonk:
                options["honk"] = False
        except Exception as e:
            print(e)
            return options

        return options

    def uncaughtException(self, exc, value, tb):
        # Show error to end user and log.
        try:
            # Log to log file
            PchumLog.error("%s, %s" % (exc, value))

            # Try to write to separate logfile
            try:
                lt = time.localtime()
                lt_str = time.strftime("%Y-%m-%d %H-%M", lt)
                f = open(
                    os.path.join(
                        _datadir, "errorlogs", ("pestererror %s.log" % lt_str)
                    ),
                    "a",
                )
                traceback.print_tb(tb, file=f)
                f.close()
            except Exception as e:
                print(str(e))

            # Show msgbox
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            try:
                msgbox.setStyleSheet(
                    "QMessageBox{" + self.widget.theme["main/defaultwindow/style"] + "}"
                )
            except Exception as e:
                print(str(e))
            msgbox.setStyleSheet(
                "background-color: red; color: black; font-size: x-large;"
            )
            msgbox.setText(
                "An uncaught exception occurred: %s \n%s \n%s "
                % (exc, value, "".join(traceback.format_tb(tb)))
            )
            msgbox.exec()
        except Exception as e:
            print("failed to process uncaught except: " + str(e))
            PchumLog.exception("app error")

    def run(self):
        sys.exit(self.app.exec())


def _retrieveGlobals():
    # NOTE: Yes, this is a terrible kludge so that the console can work
    # properly. I'm open to alternatives.
    return globals()


# def main():
#    pesterchum = MainProgram()
#    pesterchum.run()

if __name__ == "__main__":
    # We're being run as a script - not being imported.
    try:
        pesterchum = MainProgram()
        try:
            pesterchum.run()
        except SystemExit:
            pass
    except:
        PchumLog.exception("app error: ")
