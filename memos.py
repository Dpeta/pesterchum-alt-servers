import logging
import re
from string import Template
from datetime import timedelta, datetime

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtGui import QAction
except ImportError:
    print("PyQt5 fallback (memos.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QAction

import parsetools
from dataobjs import PesterProfile, PesterHistory
from generic import PesterIcon, RightClickList, mysteryTime
from convo import PesterConvo, PesterInput, PesterText, PesterTabWindow
from parsetools import (
    convertTags,
    timeProtocol,
    lexMessage,
    colorBegin,
    mecmd,
    smiledict,
)
from logviewer import PesterLogViewer

PchumLog = logging.getLogger("pchumLogger")

# Python 3
QString = str


def delta2txt(d, format="pc"):
    if type(d) is mysteryTime:
        return "?"
    if format == "pc":
        sign = "+" if d >= timedelta(0) else "-"
    else:
        if d == timedelta(0):
            return "i"
        sign = "F" if d >= timedelta(0) else "P"
    d = abs(d)
    totalminutes = (d.days * 86400 + d.seconds) // 60
    hours = totalminutes // 60
    leftovermins = totalminutes % 60
    if hours < 100:
        if format == "pc":
            return "%s%d:%02d" % (sign, hours, leftovermins)
        else:
            return "%s%02d:%02d" % (sign, hours, leftovermins)
    else:
        if format == "pc":
            return "%s%d" % (sign, hours)
        else:
            return "%s%02d:%02d" % (sign, hours, leftovermins)


def txt2delta(txt):
    sign = 1
    if txt[0] == "?":
        return mysteryTime()
    if txt[0] == "+":
        txt = txt[1:]
    elif txt[0] == "-":
        sign = -1
        txt = txt[1:]
    l = txt.split(":")
    try:
        h = int(l[0])
        m = 0
        if len(l) > 1:
            m = int(l[1])
        timed = timedelta(0, h * 3600 + m * 60)
    except ValueError:
        timed = timedelta(0)
    except OverflowError:
        if sign < 0:
            return timedelta.min
        else:
            return timedelta.max
    return sign * timed


def pcfGrammar(td):
    if td == timedelta(microseconds=1):  # Replacement for mysteryTime </3
        when = "???"
        temporal = "???"
        pcf = "?"
    elif td > timedelta(0):
        when = "FROM NOW"
        temporal = "FUTURE"
        pcf = "F"
    elif td < timedelta(0):
        when = "AGO"
        temporal = "PAST"
        pcf = "P"
    else:
        when = "RIGHT NOW"
        temporal = "CURRENT"
        pcf = "C"
    return (temporal, pcf, when)


class TimeGrammar:
    def __init__(self, temporal, pcf, when, number="0"):
        self.temporal = temporal
        self.pcf = pcf
        self.when = when
        if number == "0" or number == 0:
            self.number = ""
        else:
            self.number = str(number)


class TimeTracker(list):
    def __init__(self, time=None):
        # mysteryTime breaks stuff now, so, uh
        # I'm replacing it with 1 day...
        if type(time) == mysteryTime:
            time = timedelta(microseconds=1)
        self.timerecord = {"P": [], "F": []}
        self.open = {}
        if time is not None:
            self.append(time)
            self.current = 0
            self.addRecord(time)
            self.open[time] = False
        else:
            self.current = -1

    def addTime(self, timed):
        # mysteryTime </3
        if type(timed) == mysteryTime:
            timed = timedelta(microseconds=1)
        try:
            i = self.index(timed)
            self.current = i
            return True
        except ValueError:
            self.current = len(self)
            self.append(timed)
            self.open[timed] = False
            self.addRecord(timed)
            return False

    def prevTime(self):
        i = self.current
        i = (i - 1) % len(self)
        return self[i]

    def nextTime(self):
        i = self.current
        i = (i + 1) % len(self)
        return self[i]

    def setCurrent(self, timed):
        self.current = self.index(timed)

    def addRecord(self, timed):
        try:
            # (temporal, pcf, when) = pcfGrammar(timed - timedelta(0))
            pcf = pcfGrammar(timed - timedelta(0))[1]
        except TypeError:
            # (temporal, pcf, when) = pcfGrammar(mysteryTime())
            pcf = pcfGrammar(mysteryTime())[1]
        if pcf == "C" or pcf == "?":
            return
        if timed in self.timerecord[pcf]:
            return
        self.timerecord[pcf].append(timed)

    def getRecord(self, timed):
        try:
            # (temporal, pcf, when) = pcfGrammar(timed - timedelta(0))
            pcf = pcfGrammar(timed - timedelta(0))[1]
        except TypeError:
            pcf = pcfGrammar(mysteryTime())[1]
        if pcf == "C" or pcf == "?":
            return 0
        if len(self.timerecord[pcf]) > 1:
            return self.timerecord[pcf].index(timed) + 1
        else:
            return 0

    def removeTime(self, timed):
        try:
            self.pop(self.index(timed))
            self.current = len(self) - 1
            del self.open[timed]
            return True
        except ValueError:
            return None

    def openTime(self, time):
        if time in self.open:
            self.open[time] = True

    def openCurrentTime(self):
        timed = self.getTime()
        self.openTime(timed)

    def isFirstTime(self):
        timed = self.getTime()
        return not self.open[timed]

    def getTime(self):
        if self.current >= 0:
            return self[self.current]
        else:
            return None

    def getGrammar(self):
        timed = self.getTime()
        return self.getGrammarTime(timed)

    def getGrammarTime(self, timed):
        mytime = timedelta(0)
        try:
            (temporal, pcf, when) = pcfGrammar(timed - mytime)
        except TypeError:
            (temporal, pcf, when) = pcfGrammar(mysteryTime())
        if timed == mytime:
            return TimeGrammar(temporal, pcf, when, 0)
        return TimeGrammar(temporal, pcf, when, self.getRecord(timed))


class TimeInput(QtWidgets.QLineEdit):
    def __init__(self, timeslider, parent):
        super().__init__(parent)
        self.timeslider = timeslider
        self.setText("+0:00")
        self.timeslider.valueChanged[int].connect(self.setTime)
        self.editingFinished.connect(self.setSlider)

    @QtCore.pyqtSlot(int)
    def setTime(self, sliderval):
        self.setText(self.timeslider.getTime())

    @QtCore.pyqtSlot()
    def setSlider(self):
        value = str(self.text())
        timed = txt2delta(value)
        if type(timed) is mysteryTime:
            self.timeslider.setValue(0)
            self.setText("?")
            return
        sign = 1 if timed >= timedelta(0) else -1
        abstimed = abs(txt2delta(value))
        index = 50
        for i, td in enumerate(timedlist):
            if abstimed < td:
                index = i - 1
                break
        self.timeslider.setValue(sign * index)
        text = delta2txt(timed)
        self.setText(text)


class TimeSlider(QtWidgets.QSlider):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setTracking(True)
        self.setMinimum(-50)
        self.setMaximum(50)
        self.setValue(0)
        self.setPageStep(1)

    def getTime(self):
        time = timelist[abs(self.value())]
        sign = "+" if self.value() >= 0 else "-"
        return sign + time

    def mouseDoubleClickEvent(self, event):
        self.setValue(0)


class MemoTabWindow(PesterTabWindow):
    def __init__(self, mainwindow, parent=None):
        super().__init__(mainwindow, parent, "memos")

    def addChat(self, convo):
        self.convos[convo.channel] = convo
        # either addTab or setCurrentIndex will trigger changed()
        newindex = self.tabs.addTab(convo.channel)
        self.tabIndices[convo.channel] = newindex
        self.tabs.setCurrentIndex(newindex)
        self.tabs.setTabIcon(
            newindex, PesterIcon(self.mainwindow.theme["memos/memoicon"])
        )

    def updateBlocked(self):
        pass

    def updateMood(self):
        pass


_ctag_begin = re.compile(r"<c=(.*?)>")


class MemoText(PesterText):
    def __init__(self, theme, parent=None):
        super().__init__(theme, parent)
        if hasattr(self.parent(), "mainwindow"):
            self.mainwindow = self.parent().mainwindow
        else:
            self.mainwindow = self.parent()
        if type(parent.parent) is PesterTabWindow:
            self.tabobject = parent.parent()
            self.hasTabs = True
        else:
            self.hasTabs = False
        self.initTheme(theme)
        self.setReadOnly(True)
        self.setMouseTracking(True)
        self.textSelected = False
        self.copyAvailable[bool].connect(self.textReady)
        self.urls = {}
        for k in smiledict:
            self.addAnimation(
                QtCore.QUrl("smilies/%s" % (smiledict[k])),
                "smilies/%s" % (smiledict[k]),
            )
        # self.mainwindow.animationSetting[bool].connect(self.animateChanged)

    def initTheme(self, theme):
        if "memos/scrollbar" in theme:
            self.setStyleSheet(
                "QTextEdit { %s }"
                "QScrollBar:vertical { %s }"
                "QScrollBar::handle:vertical { %s }"
                "QScrollBar::add-line:vertical { %s }"
                "QScrollBar::sub-line:vertical { %s }"
                "QScrollBar:up-arrow:vertical { %s }"
                "QScrollBar:down-arrow:vertical { %s }"
                % (
                    theme["memos/textarea/style"],
                    theme["memos/scrollbar/style"],
                    theme["memos/scrollbar/handle"],
                    theme["memos/scrollbar/downarrow"],
                    theme["memos/scrollbar/uparrow"],
                    theme["memos/scrollbar/uarrowstyle"],
                    theme["memos/scrollbar/darrowstyle"],
                )
            )
        else:
            self.setStyleSheet("QTextEdit { %s }" % theme["memos/textarea/style"])

        # So it doesn't inherit the memo's background image.
        # Fixes floating "PESTERLOG:"
        try:
            self.setStyleSheet(
                self.styleSheet() + ("QMenu{ %s }" % theme["main/defaultwindow/style"])
            )
        except:
            pass

    def addMessage(self, msg, chum):
        if type(msg) in [str, str]:
            lexmsg = lexMessage(msg)
        else:
            lexmsg = msg
        parent = self.parent()
        window = parent.mainwindow
        me = window.profile()
        if self.mainwindow.config.animations():
            for m in self.urls:
                if convertTags(lexmsg).find(self.urls[m].toString()) != -1:
                    if m.state() == QtGui.QMovie.MovieState.NotRunning:
                        m.start()
        chumdb = window.chumdb
        if chum is not me:  # SO MUCH WH1T3SP4C3 >:]
            if type(lexmsg[0]) is colorBegin:  # get color tag
                colortag = lexmsg[0]
                try:
                    color = QtGui.QColor(*[int(c) for c in colortag.color.split(",")])
                except ValueError:
                    color = QtGui.QColor("black")
                else:
                    chumdb.setColor(chum.handle, color)
                    parent.updateColor(chum.handle, color)
            else:
                color = chumdb.getColor(chum.handle)
        else:
            color = me.color

        chum.color = color
        systemColor = QtGui.QColor(window.theme["memos/systemMsgColor"])
        if chum is not me:
            if chum.handle in parent.times:
                time = parent.times[chum.handle]
                if time.getTime() is None:
                    # MY WAY OR THE HIGHWAY
                    time.addTime(timedelta(0))
            else:
                # new chum! time current
                newtime = timedelta(0)
                time = TimeTracker(newtime)
                parent.times[chum.handle] = time
        else:
            time = parent.time

        if time.isFirstTime():
            grammar = time.getGrammar()
            joinmsg = chum.memojoinmsg(
                systemColor,
                time.getTime(),
                grammar,
                window.theme["convo/text/joinmemo"],
            )
            self.append(convertTags(joinmsg))
            parent.mainwindow.chatlog.log(parent.channel, joinmsg)
            time.openCurrentTime()

        def makeSafe(msg):
            if msg.count("<c") > msg.count("</c>"):
                for _ in range(msg.count("<c") - msg.count("</c>")):
                    msg = msg + "</c>"
            return '<span style="color:#000000">' + msg + "</span>"

        if type(lexmsg[0]) is mecmd:
            memsg = chum.memsg(systemColor, lexmsg, time=time.getGrammar())
            window.chatlog.log(parent.channel, memsg)
            self.append(convertTags(memsg))
        else:
            self.append(makeSafe(convertTags(lexmsg)))
            window.chatlog.log(parent.channel, lexmsg)

    def changeTheme(self, theme):
        self.initTheme(theme)


class MemoInput(PesterInput):
    stylesheet_path = "memos/input/style"
    # karxi: Because of the use of stylesheet_path, we don't have to rewrite
    # this code.
    # Neat, huh?


class PesterMemo(PesterConvo):
    # TODO: Clean up inheritance between these!! The inits are ugly.
    def __init__(self, channel, timestr, mainwindow, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.channel = channel
        self.setObjectName(self.channel)
        self.mainwindow = mainwindow
        self.time = TimeTracker(txt2delta(timestr))
        self.setWindowTitle(channel)
        self.channelLabel = QtWidgets.QLabel(self)
        self.channelLabel.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )

        self.textArea = MemoText(self.mainwindow.theme, self)
        self.textInput = MemoInput(self.mainwindow.theme, self)
        self.textInput.setFocus()

        self.miniUserlist = QtWidgets.QPushButton(">\n>", self)
        # self.miniUserlist.setStyleSheet("border:1px solid #a68168; border-width: 2px 0px 2px 2px; height: 90px; width: 10px; color: #cd8f9d; font-family: 'Arial'; background: white; margin-left: 2px;")
        self.miniUserlist.clicked.connect(self.toggleUserlist)

        self.userlist = RightClickList(self)
        self.userlist.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Fixed,
                QtWidgets.QSizePolicy.Policy.Expanding,
            )
        )
        self.userlist.optionsMenu = QtWidgets.QMenu(self)
        self.pesterChumAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/pester"], self
        )
        self.pesterChumAction.triggered.connect(self.newPesterSlot)
        self.addchumAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/addchum"], self
        )
        self.addchumAction.triggered.connect(self.addChumSlot)
        self.banuserAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/banuser"], self
        )
        self.banuserAction.triggered.connect(self.banSelectedUser)
        self.opAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/opuser"], self
        )
        self.opAction.triggered.connect(self.opSelectedUser)
        self.voiceAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/voiceuser"], self
        )
        self.voiceAction.triggered.connect(self.voiceSelectedUser)
        self.quirkDisableAction = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/quirkkill"], self
        )
        self.quirkDisableAction.triggered.connect(self.killQuirkUser)
        self.userlist.optionsMenu.addAction(self.pesterChumAction)
        self.userlist.optionsMenu.addAction(self.addchumAction)
        # ban & op list added if we are op

        self.optionsMenu = QtWidgets.QMenu(self)
        self.optionsMenu.setStyleSheet(
            self.mainwindow.theme["main/defaultwindow/style"]
        )  # So it doesn't inherit the memo's background image.
        # Fixes floating "PESTERLOG:"
        self.oocToggle = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/ooc"], self
        )
        self.oocToggle.setCheckable(True)
        self.oocToggle.toggled[bool].connect(self.toggleOOC)
        self.quirksOff = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/quirksoff"], self
        )
        self.quirksOff.setCheckable(True)
        self.quirksOff.toggled[bool].connect(self.toggleQuirks)
        self.logchum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/viewlog"], self
        )
        self.logchum.triggered.connect(self.openChumLogs)
        self.invitechum = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/invitechum"], self
        )
        self.invitechum.triggered.connect(self.inviteChums)

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/beeponmessage"):
        try:
            self._beepToggle = QAction(
                self.mainwindow.theme["main/menus/rclickchumlist/beeponmessage"], self
            )
        except:
            self._beepToggle = QAction("BEEP ON MESSAGE", self)
        self._beepToggle.setCheckable(True)
        self._beepToggle.toggled[bool].connect(self.toggleBeep)

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/flashonmessage"):
        try:
            self._flashToggle = QAction(
                self.mainwindow.theme["main/menus/rclickchumlist/flashonmessage"], self
            )
        except:
            self._flashToggle = QAction("FLASH ON MESSAGE", self)
        self._flashToggle.setCheckable(True)
        self._flashToggle.toggled[bool].connect(self.toggleFlash)

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/mutenotifications"):
        try:
            self._muteToggle = QAction(
                self.mainwindow.theme["main/menus/rclickchumlist/mutenotifications"],
                self,
            )
        except:
            self._muteToggle = QAction("MUTE NOTIFICATIONS", self)
        self._muteToggle.setCheckable(True)
        self._muteToggle.toggled[bool].connect(self.toggleMute)

        self.optionsMenu.addAction(self.quirksOff)
        self.optionsMenu.addAction(self.oocToggle)

        self.optionsMenu.addAction(self._beepToggle)
        self.optionsMenu.addAction(self._flashToggle)
        self.optionsMenu.addAction(self._muteToggle)

        self.optionsMenu.addAction(self.logchum)
        self.optionsMenu.addAction(self.invitechum)

        self.chanModeMenu = QtWidgets.QMenu(
            self.mainwindow.theme["main/menus/rclickchumlist/memosetting"], self
        )
        self.chanNoquirks = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/memonoquirk"], self
        )
        self.chanNoquirks.setCheckable(True)
        self.chanNoquirks.toggled[bool].connect(self.noquirksChan)
        self.chanHide = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/memohidden"], self
        )
        self.chanHide.setCheckable(True)
        self.chanHide.toggled[bool].connect(self.hideChan)
        self.chanInvite = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/memoinvite"], self
        )
        self.chanInvite.setCheckable(True)
        self.chanInvite.toggled[bool].connect(self.inviteChan)
        self.chanMod = QAction(
            self.mainwindow.theme["main/menus/rclickchumlist/memomute"], self
        )
        self.chanMod.setCheckable(True)
        self.chanMod.toggled[bool].connect(self.modChan)
        self.chanModeMenu.addAction(self.chanNoquirks)
        self.chanModeMenu.addAction(self.chanHide)
        self.chanModeMenu.addAction(self.chanInvite)
        self.chanModeMenu.addAction(self.chanMod)
        self.chanModeMenu.setStyleSheet(
            self.mainwindow.theme["main/defaultwindow/style"]
        )  # BWAH BWAH FLOATING "PESTERLOG:"

        self.timeslider = TimeSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.timeinput = TimeInput(self.timeslider, self)
        self.timeinput.setText(timestr)
        self.timeinput.setSlider()
        self.timetravel = QtWidgets.QPushButton("GO", self)
        self.timeclose = QtWidgets.QPushButton("CLOSE", self)
        self.timeswitchl = QtWidgets.QPushButton(self)
        self.timeswitchr = QtWidgets.QPushButton(self)

        self.timetravel.clicked.connect(self.sendtime)
        self.timeclose.clicked.connect(self.smashclock)
        self.timeswitchl.clicked.connect(self.prevtime)
        self.timeswitchr.clicked.connect(self.nexttime)

        self.times = {}

        self.initTheme(self.mainwindow.theme)

        # connect
        self.textInput.returnPressed.connect(self.sentMessage)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.textArea)
        layout_0.addWidget(self.textInput)

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addLayout(layout_0)
        layout_1.addWidget(self.miniUserlist)
        layout_1.addWidget(self.userlist)

        #        layout_1 = QtGui.QGridLayout()
        #        layout_1.addWidget(self.timeslider, 0, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        #        layout_1.addWidget(self.timeinput, 1, 0, 1, 3)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.timeslider)
        layout_2.addWidget(self.timeinput)
        layout_2.addWidget(self.timetravel)
        layout_2.addWidget(self.timeclose)
        layout_2.addWidget(self.timeswitchl)
        layout_2.addWidget(self.timeswitchr)
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.channelLabel)
        self.layout.addLayout(layout_1)
        self.layout.addLayout(layout_2)
        self.layout.setSpacing(0)
        margins = self.mainwindow.theme["memos/margins"]
        self.layout.setContentsMargins(
            margins["left"], margins["top"], margins["right"], margins["bottom"]
        )

        self.setLayout(self.layout)

        if parent:
            parent.addChat(self)

        p = self.mainwindow.profile()
        timeGrammar = self.time.getGrammar()
        systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
        msg = p.memoopenmsg(
            systemColor,
            self.time.getTime(),
            timeGrammar,
            self.mainwindow.theme["convo/text/openmemo"],
            self.channel,
        )
        self.time.openCurrentTime()
        self.textArea.append(convertTags(msg))
        self.mainwindow.chatlog.log(self.channel, msg)

        self.op = False
        self.newmessage = False
        self.history = PesterHistory()
        self.applyquirks = True
        self.ooc = False

        self.always_beep = False
        self.always_flash = False
        self.notifications_muted = False

    @QtCore.pyqtSlot()
    def toggleUserlist(self):
        if self.userlist.isHidden():
            self.userlist.show()
            self.miniUserlist.setText(">\n>")
            self.miniUserlist.setStyleSheet(
                "%s border-width: 2px 0px 2px 2px;" % self.miniUserlist.styleSheet()
            )
        else:
            self.userlist.hide()
            self.miniUserlist.setText("<\n<")
            self.miniUserlist.setStyleSheet(
                "%s border-width: 2px;" % self.miniUserlist.styleSheet()
            )

    def title(self):
        return self.channel

    def icon(self):
        return PesterIcon(self.mainwindow.theme["memos/memoicon"])

    def sendTimeInfo(self, newChum=False):
        if newChum:
            self.messageSent.emit(
                "PESTERCHUM:TIME>%s" % (delta2txt(self.time.getTime(), "server") + "i"),
                self.title(),
            )
        else:
            self.messageSent.emit(
                "PESTERCHUM:TIME>%s" % (delta2txt(self.time.getTime(), "server")),
                self.title(),
            )

    def updateMood(self):
        pass

    def updateBlocked(self):
        pass

    def updateColor(self, handle, color):
        chums = self.userlist.findItems(handle, QtCore.Qt.MatchFlag.MatchExactly)
        for c in chums:
            c.setForeground(QtGui.QBrush(color))

    def addMessage(self, text, handle):
        if type(handle) is bool:
            chum = self.mainwindow.profile()
        else:
            chum = PesterProfile(handle)
            self.notifyNewMessage()
        self.textArea.addMessage(text, chum)

    def initTheme(self, theme):
        self.resize(*theme["memos/size"])
        self.setStyleSheet("QtWidgets.QFrame { %s };" % (theme["memos/style"]))
        self.setWindowIcon(PesterIcon(theme["memos/memoicon"]))
        t = Template(theme["memos/label/text"])
        if self.mainwindow.advanced and hasattr(self, "modes"):
            self.channelLabel.setText(
                t.safe_substitute(channel=self.channel) + "(%s)" % (self.modes)
            )
        else:
            self.channelLabel.setText(t.safe_substitute(channel=self.channel))
        self.channelLabel.setStyleSheet(theme["memos/label/style"])
        self.channelLabel.setAlignment(
            self.aligndict["h"][theme["memos/label/align/h"]]
            | self.aligndict["v"][theme["memos/label/align/v"]]
        )
        self.channelLabel.setMaximumHeight(theme["memos/label/maxheight"])
        self.channelLabel.setMinimumHeight(theme["memos/label/minheight"])

        self.userlist.optionsMenu.setStyleSheet(theme["main/defaultwindow/style"])
        scrolls = "width: 12px; height: 12px; border: 0; padding: 0;"
        if "main/chums/scrollbar" in theme:
            self.userlist.setStyleSheet(
                "QListWidget { %s }"
                "QScrollBar { %s }"
                "QScrollBar::handle { %s }"
                "QScrollBar::add-line { %s }"
                "QScrollBar::sub-line { %s }"
                "QScrollBar:up-arrow { %s }"
                "QScrollBar:down-arrow { %s }"
                % (
                    theme["memos/userlist/style"],
                    theme["main/chums/scrollbar/style"] + scrolls,
                    theme["main/chums/scrollbar/handle"],
                    theme["main/chums/scrollbar/downarrow"],
                    theme["main/chums/scrollbar/uparrow"],
                    theme["main/chums/scrollbar/uarrowstyle"],
                    theme["main/chums/scrollbar/darrowstyle"],
                )
            )
        elif "convo/scrollbar" in theme:
            self.userlist.setStyleSheet(
                "QListWidget { %s }"
                "QScrollBar { %s }"
                "QScrollBar::handle { %s }"
                "QScrollBar::add-line { %s }"
                "QScrollBar::sub-line { %s }"
                "QScrollBar:up-arrow { %s }"
                "QScrollBar:down-arrow { %s }"
                % (
                    theme["memos/userlist/style"],
                    theme["convo/scrollbar/style"] + scrolls,
                    theme["convo/scrollbar/handle"],
                    "display: none;",
                    "display: none;",
                    "display: none;",
                    "display: none;",
                )
            )
        else:
            self.userlist.setStyleSheet(
                "QListWidget { %s }"
                "QScrollBar { %s }"
                "QScrollBar::handle { %s }"
                % (theme["memos/userlist/style"], scrolls, "background-color: black;")
            )
        self.userlist.setFixedWidth(theme["memos/userlist/width"])

        if self.userlist.isHidden():
            borders = "border-width: 2px;"
        else:
            borders = "border-width: 2px 0px 2px 2px;"
        self.miniUserlist.setStyleSheet(
            "padding: 0px;"
            "margin: 0px;"
            "margin-left: 5px;"
            "width: 10px;"
            "height: 90px;" + borders + theme["memos/userlist/style"]
        )

        self.addchumAction.setText(theme["main/menus/rclickchumlist/addchum"])
        self.banuserAction.setText(theme["main/menus/rclickchumlist/banuser"])
        self.opAction.setText(theme["main/menus/rclickchumlist/opuser"])
        self.voiceAction.setText(theme["main/menus/rclickchumlist/voiceuser"])
        self.quirkDisableAction.setText(theme["main/menus/rclickchumlist/quirkkill"])
        self.quirksOff.setText(theme["main/menus/rclickchumlist/quirksoff"])
        self.logchum.setText(theme["main/menus/rclickchumlist/viewlog"])
        self.invitechum.setText(theme["main/menus/rclickchumlist/invitechum"])
        self.chanModeMenu.setTitle(theme["main/menus/rclickchumlist/memosetting"])
        self.chanNoquirks.setText(theme["main/menus/rclickchumlist/memonoquirk"])
        self.chanHide.setText(theme["main/menus/rclickchumlist/memohidden"])
        self.chanInvite.setText(theme["main/menus/rclickchumlist/memoinvite"])
        self.chanMod.setText(theme["main/menus/rclickchumlist/memomute"])

        self.timeinput.setFixedWidth(theme["memos/time/text/width"])
        self.timeinput.setStyleSheet(theme["memos/time/text/style"])
        slidercss = (
            "QSlider { %s }"
            "Slider::groove { %s }"
            "QSlider::handle { %s }"
            % (
                theme["memos/time/slider/style"],
                theme["memos/time/slider/groove"],
                theme["memos/time/slider/handle"],
            )
        )
        self.timeslider.setStyleSheet(slidercss)

        larrow = PesterIcon(self.mainwindow.theme["memos/time/arrows/left"])
        self.timeswitchl.setIcon(larrow)
        self.timeswitchl.setIconSize(larrow.realsize())
        self.timeswitchl.setStyleSheet(self.mainwindow.theme["memos/time/arrows/style"])
        self.timetravel.setStyleSheet(self.mainwindow.theme["memos/time/buttons/style"])
        self.timeclose.setStyleSheet(self.mainwindow.theme["memos/time/buttons/style"])

        rarrow = PesterIcon(self.mainwindow.theme["memos/time/arrows/right"])
        self.timeswitchr.setIcon(rarrow)
        self.timeswitchr.setIconSize(rarrow.realsize())
        self.timeswitchr.setStyleSheet(self.mainwindow.theme["memos/time/arrows/style"])

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/beeponmessage"):
        try:
            self._beepToggle.setText(
                self.mainwindow.theme["main/menus/rclickchumlist/beeponmessage"]
            )
        except:
            self._beepToggle.setText("BEEP ON MESSAGE")

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/flashonmessage"):
        try:
            self._flashToggle.setText(
                self.mainwindow.theme["main/menus/rclickchumlist/flashonmessage"]
            )
        except:
            self._flashToggle.setText("FLASH ON MESSAGE")

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/mutenotifications"):
        try:
            self._muteToggle.setText(
                self.mainwindow.theme["main/menus/rclickchumlist/mutenotifications"]
            )
        except:
            self._muteToggle.setText("MUTE NOTIFICATIONS")

        # if self.mainwindow.theme.has_key("main/menus/rclickchumlist/pester"):
        try:
            self.pesterChumAction.setText(
                self.mainwindow.theme["main/menus/rclickchumlist/pester"]
            )
        except:
            pass

    def changeTheme(self, theme):
        self.initTheme(theme)
        self.textArea.changeTheme(theme)
        self.textInput.changeTheme(theme)
        margins = theme["memos/margins"]
        self.layout.setContentsMargins(
            margins["left"], margins["top"], margins["right"], margins["bottom"]
        )
        for item in [self.userlist.item(i) for i in range(0, self.userlist.count())]:
            self.iconCrap(item)

    def addUser(self, handle):
        chumdb = self.mainwindow.chumdb
        defaultcolor = QtGui.QColor("black")
        founder = False
        op = False
        halfop = False
        admin = False
        voice = False
        if handle[0] == "@":
            op = True
            handle = handle[1:]
            if handle == self.mainwindow.profile().handle:
                self.userlist.optionsMenu.addAction(self.opAction)
                self.userlist.optionsMenu.addAction(self.banuserAction)
                self.optionsMenu.addMenu(self.chanModeMenu)
                self.op = True
        elif handle[0] == "%":
            halfop = True
            handle = handle[1:]
            if handle == self.mainwindow.profile().handle:
                self.userlist.optionsMenu.addAction(self.opAction)
                self.userlist.optionsMenu.addAction(self.banuserAction)
                self.optionsMenu.addMenu(self.chanModeMenu)
                self.halfop = True
        elif handle[0] == "+":
            voice = True
            handle = handle[1:]
        elif handle[0] == "~":
            founder = True
            handle = handle[1:]
        elif handle[0] == "&":
            admin = True
            handle = handle[1:]
        item = QtWidgets.QListWidgetItem(handle)
        if handle == self.mainwindow.profile().handle:
            color = self.mainwindow.profile().color
        else:
            color = chumdb.getColor(handle, defaultcolor)
        item.box = handle == "evacipatedBox"
        item.setForeground(QtGui.QBrush(color))
        item.founder = founder
        item.op = op
        item.halfop = halfop
        item.admin = admin
        item.voice = voice
        self.umodes = ["box", "founder", "admin", "op", "halfop", "voice"]
        self.iconCrap(item)
        self.userlist.addItem(item)
        self.sortUsers()

    def sortUsers(self):
        users = []
        listing = self.userlist.item(0)
        while listing is not None:
            users.append(self.userlist.takeItem(0))
            listing = self.userlist.item(0)
        users.sort(
            key=lambda x: (
                (
                    -1
                    if x.box
                    else (
                        0
                        if x.founder
                        else (
                            1
                            if x.admin
                            else (
                                2
                                if x.op
                                else (3 if x.halfop else (4 if x.voice else 5))
                            )
                        )
                    )
                ),
                x.text(),
            )
        )
        for u in users:
            self.userlist.addItem(u)

    def updateChanModes(self, modes, op):
        PchumLog.debug("updateChanModes(%s, %s)", modes, op)
        if not hasattr(self, "modes"):
            self.modes = ""
        chanmodes = list(str(self.modes))
        if chanmodes and chanmodes[0] == "+":
            chanmodes = chanmodes[1:]
        modes = str(modes)
        if op:
            systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
            chum = self.mainwindow.profile()
            opchum = PesterProfile(op)
            if op in self.times:
                opgrammar = self.times[op].getGrammar()
            elif op == self.mainwindow.profile().handle:
                opgrammar = self.time.getGrammar()
            else:
                opgrammar = TimeGrammar("CURRENT", "C", "RIGHT NOW")
        if modes[0] == "+":
            for m in modes[1:]:
                if m not in chanmodes:
                    chanmodes.extend(m)
            # Make +c (disable ANSI colours) disable quirks.
            if modes.find("c") >= 0:
                self.chanNoquirks.setChecked(True)
                self.quirksOff.setChecked(True)
                self.applyquirks = False
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "A No-Quirk zone", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("s") >= 0:
                self.chanHide.setChecked(True)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Secret", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("i") >= 0:
                self.chanInvite.setChecked(True)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Invite-Only", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("m") >= 0:
                self.chanMod.setChecked(True)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Muted", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)

            # New
            if modes.find("C") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-CTCP", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("D") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Join Delayed", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("f") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Flood Protected", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("G") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Censored", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("H") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Remembering Chat History", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("k") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Key-only", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("K") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-Knock", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("L") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Redirecting", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("K") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-Knock", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("l") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum,
                        opgrammar,
                        systemColor,
                        "Limiting maximum amount of users",
                        True,
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("M") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Non-Auth muted", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("N") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Handle-locked", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("O") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "An Oper-Only channel", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("P") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Permanent", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("Q") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-kick", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("R") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Registered users only", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("r") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Registered", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("z") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Secure-only", True
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
        elif modes[0] == "-":
            for i in modes[1:]:
                try:
                    chanmodes.remove(i)
                except ValueError:
                    pass
            if modes.find("c") >= 0:
                self.chanNoquirks.setChecked(False)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "A No-Quirk zone", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("s") >= 0:
                self.chanHide.setChecked(False)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Secret", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("i") >= 0:
                self.chanInvite.setChecked(False)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Invite-Only", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("m") >= 0:
                self.chanMod.setChecked(False)
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Muted", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)

            # New
            if modes.find("C") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-CTCP", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("D") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Join Delayed", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("f") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Flood Protected", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("G") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Censored", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("H") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum,
                        opgrammar,
                        systemColor,
                        "Remembering Chat History",
                        False,
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("k") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Key-only", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("K") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-Knock", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("L") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Redirecting", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("K") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-Knock", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("l") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum,
                        opgrammar,
                        systemColor,
                        "Limiting maximum amount of users",
                        False,
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("M") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Non-Auth muted", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("N") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Handle-locked", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("O") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "An Oper-Only channel", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("P") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Permanent", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("Q") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "No-kick", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("R") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Registered users only", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("r") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Registered", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            if modes.find("z") >= 0:
                if op:
                    msg = chum.memomodemsg(
                        opchum, opgrammar, systemColor, "Secure-only", False
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
        chanmodes.sort()
        self.modes = "+" + "".join(chanmodes)
        if self.mainwindow.advanced:
            t = Template(self.mainwindow.theme["memos/label/text"])
            self.channelLabel.setText(
                t.safe_substitute(channel=self.channel) + "(%s)" % (self.modes)
            )

    def timeUpdate(self, handle, cmd):
        window = self.mainwindow
        chum = PesterProfile(handle)
        systemColor = QtGui.QColor(window.theme["memos/systemMsgColor"])
        close = None
        # old TC command?
        try:
            secs = int(cmd)
            time = datetime.fromtimestamp(secs)
            timed = time - datetime.now()
            s = (timed.seconds // 60) * 60
            timed = timedelta(timed.days, s)
        except OverflowError:
            if secs < 0:
                timed = timedelta.min
            else:
                timed = timedelta.max
        except (OSError, ValueError):
            try:
                if cmd == "i":
                    timed = timedelta(0)
                else:
                    if cmd[len(cmd) - 1] == "c":
                        close = timeProtocol(cmd)
                        timed = None
                    else:
                        timed = timeProtocol(cmd)
            except:
                PchumLog.warning("Invalid PESTERCHUM:TIME> %s", cmd)
                timed = timedelta(0)

        if handle in self.times:
            if close is not None:
                if close in self.times[handle]:
                    self.times[handle].setCurrent(close)
                    grammar = self.times[handle].getGrammar()
                    self.times[handle].removeTime(close)
                    msg = chum.memoclosemsg(
                        systemColor, grammar, window.theme["convo/text/closememo"]
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
            elif timed not in self.times[handle]:
                self.times[handle].addTime(timed)
            else:
                self.times[handle].setCurrent(timed)
        else:
            if timed is not None:
                ttracker = TimeTracker(timed)
                self.times[handle] = ttracker

    @QtCore.pyqtSlot()
    def sentMessage(self):
        text = str(self.textInput.text())

        return parsetools.kxhandleInput(self, text, flavor="memos")

    @QtCore.pyqtSlot(QString)
    def namesUpdated(self, channel):
        c = str(channel)
        if c.lower() != self.channel.lower():
            return
        # get namesdb (unused)
        # namesdb = self.mainwindow.namesdb
        # reload names
        self.userlist.clear()
        for n in self.mainwindow.namesdb[self.channel]:
            self.addUser(n)

    @QtCore.pyqtSlot(QString, QString)
    def modesUpdated(self, channel, modes):
        PchumLog.debug("modesUpdated(%s, %s)", channel, modes)
        if channel.lower() == self.channel.lower():
            self.updateChanModes(modes, None)

    @QtCore.pyqtSlot(QString)
    def closeInviteOnly(self, channel):
        c = str(channel)
        if c.lower() == self.channel.lower():
            self.mainwindow.inviteOnlyChan["QString"].disconnect(self.closeInviteOnly)
            if self.parent():
                PchumLog.info(self.channel)
                i = self.parent().tabIndices[self.channel]
                self.parent().tabClose(i)
            else:
                self.close()
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.mainwindow.theme["main/defaultwindow/style"]
            )
            msgbox.setText("%s: Invites only!" % (c))
            msgbox.setInformativeText(
                "This channel is invite-only. "
                "You must get an invitation from someone on the inside before entering."
            )
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.exec()

    @QtCore.pyqtSlot(QString, QString)
    def closeForbidden(self, channel, reason):
        c = str(channel)
        if c.lower() == self.channel.lower():
            self.mainwindow.forbiddenChan["QString", "QString"].disconnect(
                self.closeForbidden
            )
            if self.parent():
                PchumLog.info(self.channel)
                i = self.parent().tabIndices[self.channel]
                self.parent().tabClose(i)
            else:
                self.close()
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(
                "QMessageBox{ %s }" % self.mainwindow.theme["main/defaultwindow/style"]
            )
            msgbox.setText("%s: D: CANT JOIN MEMO!!!" % (c))
            msgbox.setInformativeText(reason)
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.exec()

    def quirkDisable(self, op, msg):
        chums = self.userlist.findItems(op, QtCore.Qt.MatchFlag.MatchExactly)
        for c in chums:
            if c.op:
                if msg == self.mainwindow.profile().handle:
                    self.quirksOff.setChecked(True)
                    self.applyquirks = False
                    systemColor = QtGui.QColor(
                        self.mainwindow.theme["memos/systemMsgColor"]
                    )
                    chum = self.mainwindow.profile()
                    opchum = PesterProfile(op)
                    if op in self.times:
                        opgrammar = self.times[op].getGrammar()
                    elif op == self.mainwindow.profile().handle:
                        opgrammar = self.time.getGrammar()
                    else:
                        opgrammar = TimeGrammar("CURRENT", "C", "RIGHT NOW")
                    msg = chum.memoquirkkillmsg(opchum, opgrammar, systemColor)
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)

    def chumOPstuff(self, h, op):
        chum = PesterProfile(h)
        if h == self.mainwindow.profile().handle:
            chum = self.mainwindow.profile()
            # ttracker = self.time
            # curtime = self.time.getTime()
        # elif h in self.times:
        #    ttracker = self.times[h]
        # else:
        #    ttracker = TimeTracker(timedelta(0))
        opchum = PesterProfile(op)
        PchumLog.debug("op = %s", op)
        PchumLog.debug("opchum = %s", opchum.handle)
        if op in self.times:
            opgrammar = self.times[op].getGrammar()
        elif op == self.mainwindow.profile().handle:
            opgrammar = self.time.getGrammar()
        else:
            opgrammar = TimeGrammar("CURRENT", "C", "RIGHT NOW")
        return (chum, opchum, opgrammar)

    def iconCrap(self, c, down=True):
        for m in self.umodes if down else reversed(self.umodes):
            # These if attr used to be an if eval("c." + m),
            # better not to use eval() unnecessarily for security reasons though.
            # Hopefully this works fine too.
            if hasattr(c, str(m)):
                if getattr(c, str(m)):
                    if m == "box":
                        icon = PesterIcon("smilies/box.png")
                    else:
                        icon = PesterIcon(self.mainwindow.theme[f"memos/{m}/icon"])
                    c.setIcon(icon)
                    return
        icon = QtGui.QIcon()
        c.setIcon(icon)

    @QtCore.pyqtSlot()
    def dumpNetsplit(self):
        if len(self.netsplit) > 0:
            chum = self.mainwindow.profile()
            systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
            msg = chum.memonetsplitmsg(systemColor, self.netsplit)
            self.textArea.append(convertTags(msg))
            self.mainwindow.chatlog.log(self.channel, msg)
        del self.netsplit

    @QtCore.pyqtSlot(QString, QString, QString)
    def userPresentChange(self, handle, channel, update):
        # print("handle: %s, channel: %s, update: %s" % (handle, channel, update))
        h = str(handle)
        c = str(channel)
        update = str(update)
        # PchumLog.debug("h=%s\nc=%s\nupdate=%s" % (h,c,update))
        if update[0:4] == "kick":  # yeah, i'm lazy.
            l = update.split(":")
            update = l[0]
            op = l[1]
            reason = ":".join(l[2:])
        if update == "nick":
            l = h.split(":")
            oldnick = l[0]
            newnick = l[1]
            h = oldnick
        if update[0:1] in ["+", "-"]:
            l = update.split(":")
            update = l[0]
            op = l[1]
        if (
            update
            in [
                "join",
                "left",
                "kick",
                "+q",
                "-q",
                "+o",
                "-o",
                "+h",
                "-h",
                "+a",
                "-a",
                "+v",
                "-v",
            ]
        ) and c.lower() != self.channel.lower():
            return
        chums = self.userlist.findItems(h, QtCore.Qt.MatchFlag.MatchExactly)
        systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
        # print exit
        if update in ("quit", "left", "nick", "netsplit"):
            if update == "netsplit":
                if not hasattr(self, "netsplit"):
                    self.netsplit = []
                    QtCore.QTimer.singleShot(1500, self, QtCore.SLOT("dumpNetsplit()"))
            for c in chums:
                chum = PesterProfile(h)
                self.userlist.takeItem(self.userlist.row(c))
                if h not in self.times:
                    self.times[h] = TimeTracker(timedelta(0))
                allinitials = []
                while self.times[h].getTime() is not None:
                    t = self.times[h]
                    grammar = t.getGrammar()
                    allinitials.append(
                        "{}{}{}".format(grammar.pcf, chum.initials(), grammar.number)
                    )
                    self.times[h].removeTime(t.getTime())
                if update == "netsplit":
                    self.netsplit.extend(allinitials)
                else:
                    msg = chum.memoclosemsg(
                        systemColor,
                        allinitials,
                        self.mainwindow.theme["convo/text/closememo"],
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
                if update == "nick":
                    self.addUser(newnick)
                    newchums = self.userlist.findItems(
                        newnick, QtCore.Qt.MatchFlag.MatchExactly
                    )
                    for nc in newchums:
                        for c in chums:
                            nc.founder = c.founder
                            nc.op = c.op
                            nc.halfop = c.halfop
                            nc.admin = c.admin
                            self.iconCrap(nc)
                    self.sortUsers()
        elif update == "kick":
            if len(chums) == 0:
                return
            c = chums[0]
            chum = PesterProfile(h)
            if h == self.mainwindow.profile().handle:
                chum = self.mainwindow.profile()
                ttracker = self.time
                curtime = self.time.getTime()
            elif h in self.times:
                ttracker = self.times[h]
            else:
                ttracker = TimeTracker(timedelta(0))
            allinitials = []
            opchum = PesterProfile(op)
            if op in self.times:
                opgrammar = self.times[op].getGrammar()
            elif op == self.mainwindow.profile().handle:
                opgrammar = self.time.getGrammar()
            else:
                opgrammar = TimeGrammar("CURRENT", "C", "RIGHT NOW")
            while ttracker.getTime() is not None:
                grammar = ttracker.getGrammar()
                allinitials.append(
                    "{}{}{}".format(grammar.pcf, chum.initials(), grammar.number)
                )
                ttracker.removeTime(ttracker.getTime())
            msg = chum.memobanmsg(opchum, opgrammar, systemColor, allinitials, reason)
            self.textArea.append(convertTags(msg))
            self.mainwindow.chatlog.log(self.channel, msg)

            if chum is self.mainwindow.profile():
                # are you next?
                msgbox = QtWidgets.QMessageBox()
                msgbox.setStyleSheet(
                    "QMessageBox{ %s }"
                    % self.mainwindow.theme["main/defaultwindow/style"]
                )
                msgbox.setText(self.mainwindow.theme["convo/text/kickedmemo"])

                # Add ban(kick) reason
                # l = split update
                kick_msg = "press 0k to rec0nnect or cancel to absc0nd"
                if len(l) >= 3:
                    try:
                        if (
                            l[1] != l[2]
                        ):  # If there's no reason then reason is set to handle
                            # Process spare ':' characters (this might not be safe?)
                            aggrievocation = l[1] + ": " + l[2]
                            if len(l) > 3:
                                aggrievocation += ":"
                                for x in range(3, len(l)):
                                    aggrievocation += l[x]
                                    # Not for last slice
                                    if x != (len(l) - 1):
                                        aggrievocation += ":"
                            kick_msg = (
                                "%s\n\npress 0k to rec0nnect or cancel to absc0nd"
                                % aggrievocation
                            )
                    except IndexError as e:
                        # This shouldn't happen
                        PchumLog.warning("kickmsg IndexError: %s", e)
                msgbox.setInformativeText(kick_msg)
                msgbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok
                    | QtWidgets.QMessageBox.StandardButton.Cancel
                )
                # Find the OK button and make it default
                for b in msgbox.buttons():
                    if (
                        msgbox.buttonRole(b)
                        == QtWidgets.QMessageBox.ButtonRole.AcceptRole
                    ):
                        # We found the 'OK' button, set it as the default
                        b.setDefault(True)
                        b.setAutoDefault(True)
                        # Actually set it as the selected option, since we're
                        # already stealing focus
                        b.setFocus()
                        break
                ret = msgbox.exec()
                if ret == QtWidgets.QMessageBox.StandardButton.Ok:
                    self.userlist.clear()
                    self.time = TimeTracker(curtime)
                    self.resetSlider(curtime)
                    self.mainwindow.joinChannel.emit(self.channel)
                    me = self.mainwindow.profile()
                    self.time.openCurrentTime()
                    msg = me.memoopenmsg(
                        systemColor,
                        self.time.getTime(),
                        self.time.getGrammar(),
                        self.mainwindow.theme["convo/text/openmemo"],
                        self.channel,
                    )
                    self.textArea.append(convertTags(msg))
                    self.mainwindow.chatlog.log(self.channel, msg)
                elif ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                    if self.parent():
                        i = self.parent().tabIndices[self.channel]
                        self.parent().tabClose(i)
                    else:
                        self.close()
            else:
                # i warned you about those stairs bro
                self.userlist.takeItem(self.userlist.row(c))
        elif update == "join":
            self.addUser(h)
            time = self.time.getTime()
            txt_time = delta2txt(time, "server")
            # Only send if time isn't CURRENT, it's very spammy otherwise.
            # CURRENT should be the default already.
            if txt_time != "i":
                serverText = "PESTERCHUM:TIME>" + txt_time
                self.messageSent.emit(serverText, self.title())
        elif update == "+q":
            for c in chums:
                c.founder = True
                self.iconCrap(c)
            self.sortUsers()
        elif update == "-q":
            for c in chums:
                c.founder = False
                self.iconCrap(c)
            self.sortUsers()
        elif update == "+o":
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                # PchumLog.debug("chum.handle = %s\nopchum.handle = %s\nopgrammar = %s\n systemColor = %s\n"
                #               % (chum.handle, opchum.handle, opgrammar, systemColor))
                msg = chum.memoopmsg(opchum, opgrammar, systemColor)
                # PchumLog.debug("post memoopmsg")
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.op = True
                self.iconCrap(c)
                if str(c.text()) == self.mainwindow.profile().handle:
                    self.userlist.optionsMenu.addAction(self.opAction)
                    self.userlist.optionsMenu.addAction(self.voiceAction)
                    self.userlist.optionsMenu.addAction(self.banuserAction)
                    self.userlist.optionsMenu.addAction(self.quirkDisableAction)
                    self.optionsMenu.addMenu(self.chanModeMenu)
            self.sortUsers()
        elif update == "-o":
            self.mainwindow.channelNames.emit(self.channel)
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                msg = chum.memodeopmsg(opchum, opgrammar, systemColor)
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.op = False
                self.iconCrap(c)
                if str(c.text()) == self.mainwindow.profile().handle:
                    self.userlist.optionsMenu.removeAction(self.opAction)
                    self.userlist.optionsMenu.removeAction(self.voiceAction)
                    self.userlist.optionsMenu.removeAction(self.banuserAction)
                    self.userlist.optionsMenu.removeAction(self.quirkDisableAction)
                    self.optionsMenu.removeAction(self.chanModeMenu.menuAction())
            self.sortUsers()
        elif update == "+h":
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                msg = chum.memoopmsg(opchum, opgrammar, systemColor)
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.halfop = True
                self.iconCrap(c)
                if str(c.text()) == self.mainwindow.profile().handle:
                    self.userlist.optionsMenu.addAction(self.opAction)
                    self.userlist.optionsMenu.addAction(self.voiceAction)
                    self.userlist.optionsMenu.addAction(self.banuserAction)
                    self.userlist.optionsMenu.addAction(self.quirkDisableAction)
                    self.optionsMenu.addMenu(self.chanModeMenu)
            self.sortUsers()
        elif update == "-h":
            self.mainwindow.channelNames.emit(self.channel)
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                msg = chum.memodeopmsg(opchum, opgrammar, systemColor)
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.halfop = False
                self.iconCrap(c)
                if str(c.text()) == self.mainwindow.profile().handle:
                    self.userlist.optionsMenu.removeAction(self.opAction)
                    self.userlist.optionsMenu.removeAction(self.voiceAction)
                    self.userlist.optionsMenu.removeAction(self.banuserAction)
                    self.userlist.optionsMenu.removeAction(self.quirkDisableAction)
                    self.optionsMenu.removeAction(self.chanModeMenu.menuAction())
            self.sortUsers()
        elif update == "+a":
            for c in chums:
                c.admin = True
                self.iconCrap(c)
            self.sortUsers()
        elif update == "-a":
            for c in chums:
                c.admin = False
                self.iconCrap(c)
            self.sortUsers()
        elif c.lower() == self.channel.lower() and h == "" and update[0] in ["+", "-"]:
            self.updateChanModes(update, op)
        elif update == "+v":
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                msg = chum.memovoicemsg(opchum, opgrammar, systemColor)
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.voice = True
                self.iconCrap(c)
            self.sortUsers()
        elif update == "-v":
            if self.mainwindow.config.opvoiceMessages():
                (chum, opchum, opgrammar) = self.chumOPstuff(h, op)
                msg = chum.memodevoicemsg(opchum, opgrammar, systemColor)
                self.textArea.append(convertTags(msg))
                self.mainwindow.chatlog.log(self.channel, msg)
            for c in chums:
                c.voice = False
                self.iconCrap(c)
            self.sortUsers()
        elif c.lower() == self.channel.lower() and h == "" and update[0] in ["+", "-"]:
            self.updateChanModes(update, op)

    @QtCore.pyqtSlot()
    def newPesterSlot(self):
        # We're opening a pester with someone in our user list.
        user = self.userlist.currentItem()
        if not user:
            return
        user = str(user.text())
        self.mainwindow.newConversation(user)

    @QtCore.pyqtSlot()
    def addChumSlot(self):
        if not self.userlist.currentItem():
            return
        currentChum = PesterProfile(str(self.userlist.currentItem().text()))
        self.mainwindow.addChum(currentChum)

    @QtCore.pyqtSlot()
    def banSelectedUser(self):
        if not self.userlist.currentItem():
            return
        currentHandle = str(self.userlist.currentItem().text())
        (reason, ok) = QtWidgets.QInputDialog.getText(
            self, "Ban User", "Enter the reason you are banning this user (optional):"
        )
        if ok:
            self.mainwindow.kickUser.emit(self.channel, currentHandle, reason)

    @QtCore.pyqtSlot()
    def opSelectedUser(self):
        if not self.userlist.currentItem():
            return
        currentHandle = str(self.userlist.currentItem().text())
        self.mainwindow.setChannelMode.emit(self.channel, "+o", currentHandle)

    @QtCore.pyqtSlot()
    def voiceSelectedUser(self):
        if not self.userlist.currentItem():
            return
        currentHandle = str(self.userlist.currentItem().text())
        self.mainwindow.setChannelMode.emit(self.channel, "+v", currentHandle)

    @QtCore.pyqtSlot()
    def killQuirkUser(self):
        if not self.userlist.currentItem():
            return
        currentHandle = str(self.userlist.currentItem().text())
        self.mainwindow.killSomeQuirks.emit(self.channel, currentHandle)

    def resetSlider(self, time, send=True):
        self.timeinput.setText(delta2txt(time))
        self.timeinput.setSlider()
        if send:
            self.sendtime()

    @QtCore.pyqtSlot()
    def openChumLogs(self):
        currentChum = self.channel
        self.mainwindow.chumList.pesterlogviewer = PesterLogViewer(
            currentChum, self.mainwindow.config, self.mainwindow.theme, self.mainwindow
        )
        self.mainwindow.chumList.pesterlogviewer.rejected.connect(
            self.mainwindow.chumList.closeActiveLog
        )
        self.mainwindow.chumList.pesterlogviewer.show()
        self.mainwindow.chumList.pesterlogviewer.raise_()
        self.mainwindow.chumList.pesterlogviewer.activateWindow()

    @QtCore.pyqtSlot()
    def inviteChums(self):
        if not hasattr(self, "invitechums"):
            self.invitechums = None
        if not self.invitechums:
            (chum, ok) = QtWidgets.QInputDialog.getText(
                self,
                "Invite to Chat",
                "Enter the chumhandle of the user you'd like to invite:",
            )
            if ok:
                chum = str(chum)
                self.mainwindow.inviteChum.emit(chum, self.channel)
            self.invitechums = None

    @QtCore.pyqtSlot(bool)
    def noquirksChan(self, on):
        x = ["-", "+"][on]
        self.mainwindow.setChannelMode.emit(self.channel, x + "c", "")

    @QtCore.pyqtSlot(bool)
    def hideChan(self, on):
        x = ["-", "+"][on]
        self.mainwindow.setChannelMode.emit(self.channel, x + "s", "")

    @QtCore.pyqtSlot(bool)
    def inviteChan(self, on):
        x = ["-", "+"][on]
        self.mainwindow.setChannelMode.emit(self.channel, x + "i", "")

    @QtCore.pyqtSlot(bool)
    def modChan(self, on):
        x = ["-", "+"][on]
        self.mainwindow.setChannelMode.emit(self.channel, x + "m", "")

    @QtCore.pyqtSlot()
    def sendtime(self):
        # me = self.mainwindow.profile()
        # systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
        time = txt2delta(self.timeinput.text())
        # present = self.time.addTime(time)
        self.time.addTime(time)

        serverText = "PESTERCHUM:TIME>" + delta2txt(time, "server")
        self.messageSent.emit(serverText, self.title())

    @QtCore.pyqtSlot()
    def smashclock(self):
        me = self.mainwindow.profile()
        time = txt2delta(self.timeinput.text())
        removed = self.time.removeTime(time)
        if removed:
            grammar = self.time.getGrammarTime(time)
            systemColor = QtGui.QColor(self.mainwindow.theme["memos/systemMsgColor"])
            msg = me.memoclosemsg(
                systemColor, grammar, self.mainwindow.theme["convo/text/closememo"]
            )
            self.textArea.append(convertTags(msg))
            self.mainwindow.chatlog.log(self.channel, msg)

        newtime = self.time.getTime()
        if newtime is None:
            newtime = timedelta(0)
            self.resetSlider(newtime, send=False)
        else:
            self.resetSlider(newtime)

    @QtCore.pyqtSlot()
    def prevtime(self):
        time = self.time.prevTime()
        self.time.setCurrent(time)
        self.resetSlider(time)
        self.textInput.setFocus()

    @QtCore.pyqtSlot()
    def nexttime(self):
        time = self.time.nextTime()
        self.time.setCurrent(time)
        self.resetSlider(time)
        self.textInput.setFocus()

    def closeEvent(self, event):
        self.mainwindow.waitingMessages.messageAnswered(self.channel)
        self.windowClosed.emit(self.title())

    windowClosed = QtCore.pyqtSignal("QString")


timelist = [
    "0:00",
    "0:01",
    "0:02",
    "0:04",
    "0:06",
    "0:10",
    "0:14",
    "0:22",
    "0:30",
    "0:41",
    "1:00",
    "1:34",
    "2:16",
    "3:14",
    "4:13",
    "4:20",
    "5:25",
    "6:12",
    "7:30",
    "8:44",
    "10:25",
    "11:34",
    "14:13",
    "16:12",
    "17:44",
    "22:22",
    "25:10",
    "33:33",
    "42:00",
    "43:14",
    "50:00",
    "62:12",
    "75:00",
    "88:44",
    "100",
    "133",
    "143",
    "188",
    "200",
    "222",
    "250",
    "314",
    "333",
    "413",
    "420",
    "500",
    "600",
    "612",
    "888",
    "1000",
    "1025",
]

timedlist = [
    timedelta(0),
    timedelta(0, 60),
    timedelta(0, 120),
    timedelta(0, 240),
    timedelta(0, 360),
    timedelta(0, 600),
    timedelta(0, 840),
    timedelta(0, 1320),
    timedelta(0, 1800),
    timedelta(0, 2460),
    timedelta(0, 3600),
    timedelta(0, 5640),
    timedelta(0, 8160),
    timedelta(0, 11640),
    timedelta(0, 15180),
    timedelta(0, 15600),
    timedelta(0, 19500),
    timedelta(0, 22320),
    timedelta(0, 27000),
    timedelta(0, 31440),
    timedelta(0, 37500),
    timedelta(0, 41640),
    timedelta(0, 51180),
    timedelta(0, 58320),
    timedelta(0, 63840),
    timedelta(0, 80520),
    timedelta(1, 4200),
    timedelta(1, 34380),
    timedelta(1, 64800),
    timedelta(1, 69240),
    timedelta(2, 7200),
    timedelta(2, 51120),
    timedelta(3, 10800),
    timedelta(3, 60240),
    timedelta(4, 14400),
    timedelta(5, 46800),
    timedelta(5, 82800),
    timedelta(7, 72000),
    timedelta(8, 28800),
    timedelta(9, 21600),
    timedelta(10, 36000),
    timedelta(13, 7200),
    timedelta(13, 75600),
    timedelta(17, 18000),
    timedelta(17, 43200),
    timedelta(20, 72000),
    timedelta(25),
    timedelta(25, 43200),
    timedelta(37),
    timedelta(41, 57600),
    timedelta(42, 61200),
]
