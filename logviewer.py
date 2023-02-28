import os
import codecs
import re
import ostools
from time import strftime, strptime

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    print("PyQt5 fallback (logviewer.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets
from generic import RightClickList, RightClickTree
from parsetools import convertTags
from convo import PesterText

_datadir = ostools.getDataDir()


class PesterLogSearchInput(QtWidgets.QLineEdit):
    def __init__(self, theme, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.setStyleSheet(theme["convo/input/style"] + "; margin-right:0px;")

    def keyPressEvent(self, event):
        QtWidgets.QLineEdit.keyPressEvent(self, event)
        if hasattr(self.parent(), "textArea"):
            if event.key() == QtCore.Qt.Key.Key_Return:
                self.parent().logSearch(self.text())
                if self.parent().textArea.find(self.text()):
                    self.parent().textArea.ensureCursorVisible()
        else:
            self.parent().logSearch(self.text())


class PesterLogHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.searchTerm = ""
        self.hilightstyle = QtGui.QTextCharFormat()
        self.hilightstyle.setBackground(QtGui.QBrush(QtCore.Qt.GlobalColor.green))
        self.hilightstyle.setForeground(QtGui.QBrush(QtCore.Qt.GlobalColor.black))

    def highlightBlock(self, text):
        for i in range(0, len(text) - (len(self.searchTerm) - 1)):
            if text[i : i + len(self.searchTerm)].lower() == self.searchTerm.lower():
                self.setFormat(i, len(self.searchTerm), self.hilightstyle)


class PesterLogUserSelect(QtWidgets.QDialog):
    def __init__(self, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.parent = parent
        self.handle = parent.profile().handle
        self.logpath = _datadir + "logs"

        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pesterlogs")

        instructions = QtWidgets.QLabel("Pick a memo or chumhandle:")

        if os.path.exists("{}/{}".format(self.logpath, self.handle)):
            chumMemoList = os.listdir("{}/{}/".format(self.logpath, self.handle))
        else:
            chumMemoList = []
        chumslist = config.chums()
        for c in chumslist:
            if not c in chumMemoList:
                chumMemoList.append(c)
        chumMemoList.sort()

        self.chumsBox = RightClickList(self)
        self.chumsBox.setStyleSheet(self.theme["main/chums/style"])
        self.chumsBox.optionsMenu = QtWidgets.QMenu(self)

        for _, t in enumerate(chumMemoList):
            item = QtWidgets.QListWidgetItem(t)
            item.setForeground(
                QtGui.QBrush(QtGui.QColor(self.theme["main/chums/userlistcolor"]))
            )
            self.chumsBox.addItem(item)

        self.search = PesterLogSearchInput(theme, self)
        self.search.setFocus()

        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.viewActivatedLog)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)
        self.directory = QtWidgets.QPushButton("LOG DIRECTORY", self)
        self.directory.clicked.connect(self.openDir)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(instructions)
        layout_0.addWidget(self.chumsBox)
        layout_0.addWidget(self.search)
        layout_0.addLayout(layout_ok)
        layout_0.addWidget(self.directory)

        self.setLayout(layout_0)

    def selectedchum(self):
        return self.chumsBox.currentItem()

    def logSearch(self, search):
        found = self.chumsBox.findItems(search, QtCore.Qt.MatchFlag.MatchStartsWith)
        if len(found) > 0 and len(found) < self.chumsBox.count():
            self.chumsBox.setCurrentItem(found[0])

    @QtCore.pyqtSlot()
    def viewActivatedLog(self):
        selectedchum = self.selectedchum()
        if not selectedchum:
            return
        selectedchum = selectedchum.text()
        if not hasattr(self, "pesterlogviewer"):
            self.pesterlogviewer = None
        if not self.pesterlogviewer:
            self.pesterlogviewer = PesterLogViewer(
                selectedchum, self.config, self.theme, self.parent
            )
            self.pesterlogviewer.rejected.connect(self.closeActiveLog)
            self.pesterlogviewer.show()
            self.pesterlogviewer.raise_()
            self.pesterlogviewer.activateWindow()
        self.accept()

    @QtCore.pyqtSlot()
    def closeActiveLog(self):
        self.pesterlogviewer.close()
        self.pesterlogviewer = None

    @QtCore.pyqtSlot()
    def openDir(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "file:///" + os.path.join(_datadir, "logs"),
                QtCore.QUrl.ParsingMode.TolerantMode,
            )
        )


class PesterLogViewer(QtWidgets.QDialog):
    def __init__(self, chum, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.parent = parent
        self.mainwindow = parent
        global _datadir
        self.handle = parent.profile().handle
        self.chum = chum
        self.convos = {}
        self.logpath = _datadir + "logs"

        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pesterlogs with " + self.chum)

        self.format = "bbcode"
        if os.path.exists(
            "{}/{}/{}/{}".format(self.logpath, self.handle, chum, self.format)
        ):
            self.logList = os.listdir(
                "{}/{}/{}/{}/".format(self.logpath, self.handle, self.chum, self.format)
            )
        else:
            self.logList = []

        if (
            not os.path.exists(
                "{}/{}/{}/{}".format(self.logpath, self.handle, chum, self.format)
            )
            or len(self.logList) == 0
        ):
            instructions = QtWidgets.QLabel("No Pesterlogs were found")

            self.ok = QtWidgets.QPushButton("CLOSE", self)
            self.ok.setDefault(True)
            self.ok.clicked.connect(self.reject)
            layout_ok = QtWidgets.QHBoxLayout()
            layout_ok.addWidget(self.ok)

            layout_0 = QtWidgets.QVBoxLayout()
            layout_0.addWidget(instructions)
            layout_0.addLayout(layout_ok)

            self.setLayout(layout_0)
        else:
            self.instructions = QtWidgets.QLabel("Pesterlog with " + self.chum + " on")

            self.textArea = PesterLogText(theme, self.parent)
            self.textArea.setReadOnly(True)
            self.textArea.setFixedWidth(600)
            if "convo/scrollbar" in theme:
                self.textArea.setStyleSheet(
                    "QTextEdit { width:500px; %s } QScrollBar:vertical { %s } QScrollBar::handle:vertical { %s } QScrollBar::add-line:vertical { %s } QScrollBar::sub-line:vertical { %s } QScrollBar:up-arrow:vertical { %s } QScrollBar:down-arrow:vertical { %s }"
                    % (
                        theme["convo/textarea/style"],
                        theme["convo/scrollbar/style"],
                        theme["convo/scrollbar/handle"],
                        theme["convo/scrollbar/downarrow"],
                        theme["convo/scrollbar/uparrow"],
                        theme["convo/scrollbar/uarrowstyle"],
                        theme["convo/scrollbar/darrowstyle"],
                    )
                )
            else:
                self.textArea.setStyleSheet(
                    "QTextEdit { width:500px; %s }" % (theme["convo/textarea/style"])
                )

            self.logList.sort()
            self.logList.reverse()

            self.tree = RightClickTree()
            self.tree.optionsMenu = QtWidgets.QMenu(self)
            self.tree.setFixedSize(260, 300)
            self.tree.header().hide()
            if "convo/scrollbar" in theme:
                self.tree.setStyleSheet(
                    "QTreeWidget { %s } QScrollBar:vertical { %s } QScrollBar::handle:vertical { %s } QScrollBar::add-line:vertical { %s } QScrollBar::sub-line:vertical { %s } QScrollBar:up-arrow:vertical { %s } QScrollBar:down-arrow:vertical { %s }"
                    % (
                        theme["convo/textarea/style"],
                        theme["convo/scrollbar/style"],
                        theme["convo/scrollbar/handle"],
                        theme["convo/scrollbar/downarrow"],
                        theme["convo/scrollbar/uparrow"],
                        theme["convo/scrollbar/uarrowstyle"],
                        theme["convo/scrollbar/darrowstyle"],
                    )
                )
            else:
                self.tree.setStyleSheet("%s" % (theme["convo/textarea/style"]))
            self.tree.itemSelectionChanged.connect(self.loadSelectedLog)
            self.tree.setSortingEnabled(False)

            child_1 = None
            last = ["", ""]
            # blackbrush = QtGui.QBrush(QtCore.Qt.GlobalColor.black)
            for i, l in enumerate(self.logList):
                my = self.fileToMonthYear(l)
                if my[0] != last[0]:
                    child_1 = QtWidgets.QTreeWidgetItem(["{} {}".format(my[0], my[1])])
                    # child_1.setForeground(0, blackbrush)
                    self.tree.addTopLevelItem(child_1)
                    if i == 0:
                        child_1.setExpanded(True)
                child_1.addChild(QtWidgets.QTreeWidgetItem([self.fileToTime(l)]))
                last = self.fileToMonthYear(l)

            self.hilight = PesterLogHighlighter(self.textArea)
            if len(self.logList) > 0:
                self.loadLog(self.logList[0])

            self.search = PesterLogSearchInput(theme, self)
            self.search.setFocus()
            self.find = QtWidgets.QPushButton("Find", self)
            font = self.find.font()
            font.setPointSize(8)
            self.find.setFont(font)
            self.find.setDefault(True)
            self.find.setFixedSize(40, 20)
            layout_search = QtWidgets.QHBoxLayout()
            layout_search.addWidget(self.search)
            layout_search.addWidget(self.find)

            self.ok = QtWidgets.QPushButton("CLOSE", self)
            self.ok.setFixedWidth(80)
            self.ok.clicked.connect(self.reject)
            layout_ok = QtWidgets.QHBoxLayout()
            layout_ok.addWidget(self.ok)
            layout_ok.setAlignment(self.ok, QtCore.Qt.AlignmentFlag.AlignRight)

            layout_logs = QtWidgets.QHBoxLayout()
            layout_logs.addWidget(self.tree)
            layout_right = QtWidgets.QVBoxLayout()
            layout_right.addWidget(self.textArea)
            layout_right.addLayout(layout_search)
            layout_logs.addLayout(layout_right)

            layout_0 = QtWidgets.QVBoxLayout()
            layout_0.addWidget(self.instructions)
            layout_0.addLayout(layout_logs)
            layout_0.addLayout(layout_ok)

            self.setLayout(layout_0)

    @QtCore.pyqtSlot()
    def loadSelectedLog(self):
        if len(self.tree.currentItem().text(0)) > len("September 2011"):
            self.loadLog(self.timeToFile(self.tree.currentItem().text(0)))

    def loadLog(self, fname: str):
        fp = codecs.open(
            "%s/%s/%s/%s/%s"
            % (self.logpath, self.handle, self.chum, self.format, fname),
            encoding="utf-8",
            mode="r",
        )
        self.textArea.clear()
        for line in fp:
            cline = (
                line.replace("\r\n", "")
                .replace("[/color]", "</c>")
                .replace("[url]", "")
                .replace("[/url]", "")
            )
            cline = re.sub(r"\[color=(#.{6})]", r"<c=\1>", cline)
            self.textArea.append(convertTags(cline))
        textCur = self.textArea.textCursor()
        # textCur.movePosition(1)
        self.textArea.setTextCursor(textCur)
        self.instructions.setText(
            "Pesterlog with " + self.chum + " on " + self.fileToTime(fname)
        )

    def logSearch(self, search):
        self.hilight.searchTerm = search
        self.hilight.rehighlight()

    def fileToMonthYear(self, fname):
        time = strptime(
            fname[(fname.index(".") + 1) : fname.index(".txt")], "%Y-%m-%d.%H.%M"
        )
        return [strftime("%B", time), strftime("%Y", time)]

    def fileToTime(self, fname):
        timestr = fname[(fname.index(".") + 1) : fname.index(".txt")]
        return strftime("%a %d %b %Y %H %M", strptime(timestr, "%Y-%m-%d.%H.%M"))

    def timeToFile(self, time):
        return self.chum + strftime(
            ".%Y-%m-%d.%H.%M.txt", strptime(str(time), "%a %d %b %Y %H %M")
        )


class PesterLogText(PesterText):
    def __init__(self, theme, parent=None):
        PesterText.__init__(self, theme, parent)

    def focusInEvent(self, event):
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def mousePressEvent(self, event):
        try:
            # PyQt6
            url = self.anchorAt(event.position().toPoint())
        except AttributeError:
            # PyQt5
            url = self.anchorAt(event.pos())
        if url != "":
            if url[0] == "#" and url != "#pesterchum":
                self.parent().parent.showMemos(url[1:])
            elif url[0] == "@":
                handle = url[1:]
                self.parent().parent.newConversation(handle)
            else:
                QtGui.QDesktopServices.openUrl(
                    QtCore.QUrl(url, QtCore.QUrl.ParsingMode.TolerantMode)
                )
        QtWidgets.QTextEdit.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        QtWidgets.QTextEdit.mouseMoveEvent(self, event)
        try:
            # PyQt6
            pos = event.position().toPoint()
        except AttributeError:
            # PyQt5
            pos = event.pos()
        if self.anchorAt(pos):
            if (
                self.viewport().cursor().shape
                != QtCore.Qt.CursorShape.PointingHandCursor
            ):
                self.viewport().setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                )
        else:
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))

    def contextMenuEvent(self, event):
        textMenu = self.createStandardContextMenu()
        a = textMenu.actions()
        a[0].setText("Copy Plain Text")
        a[0].setShortcut(self.tr("Ctrl+C"))
        textMenu.exec(event.globalPos())
