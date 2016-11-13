from string import Template
import re
import platform
import httplib, urllib
from time import strftime
from copy import copy
from datetime import datetime, timedelta
from PyQt4 import QtGui, QtCore

from mood import Mood
from dataobjs import PesterProfile, PesterHistory
from generic import PesterIcon
from parsetools import convertTags, lexMessage, splitMessage, mecmd, colorBegin, colorEnd, \
    img2smiley, smiledict, oocre

class PesterTabWindow(QtGui.QFrame):
    def __init__(self, mainwindow, parent=None, convo="convo"):
        QtGui.QFrame.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mainwindow = mainwindow

        self.tabs = QtGui.QTabBar(self)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.connect(self.tabs, QtCore.SIGNAL('currentChanged(int)'),
                     self, QtCore.SLOT('changeTab(int)'))
        self.connect(self.tabs, QtCore.SIGNAL('tabCloseRequested(int)'),
                     self, QtCore.SLOT('tabClose(int)'))
        self.connect(self.tabs, QtCore.SIGNAL('tabMoved(int, int)'),
                     self, QtCore.SLOT('tabMoved(int, int)'))

        self.initTheme(self.mainwindow.theme)
        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.convos = {}
        self.tabIndices = {}
        self.currentConvo = None
        self.changedTab = False
        self.softclose = False

        self.type = convo

        # get default tab color i guess
        self.defaultTabTextColor = self.getTabTextColor()

    def getTabTextColor(self):
        # ugly, ugly hack
        self.changedTab = True
        i = self.tabs.addTab(".")
        c = self.tabs.tabTextColor(i)
        self.tabs.removeTab(i)
        self.changedTab = False
        return c
    def addChat(self, convo):
        self.convos[convo.title()] = convo
        # either addTab or setCurrentIndex will trigger changed()
        newindex = self.tabs.addTab(convo.title())
        self.tabIndices[convo.title()] = newindex
        self.tabs.setCurrentIndex(newindex)
        self.tabs.setTabIcon(newindex, convo.icon())
    def showChat(self, handle):
        tabi = self.tabIndices[handle]
        if self.tabs.currentIndex() == tabi:
            self.activateWindow()
            self.raise_()
            self.convos[handle].raiseChat()
        else:
            self.tabs.setCurrentIndex(tabi)

    def convoHasFocus(self, convo):
        if ((self.hasFocus() or self.tabs.hasFocus()) and
            self.tabs.tabText(self.tabs.currentIndex()) == convo.title()):
            return True

    def keyPressEvent(self, event):
        keypress = event.key()
        mods = event.modifiers()
        if ((mods & QtCore.Qt.ControlModifier) and
            keypress == QtCore.Qt.Key_Tab):
            handles = self.convos.keys()
            waiting = self.mainwindow.waitingMessages.waitingHandles()
            waitinghandles = list(set(handles) & set(waiting))
            if len(waitinghandles) > 0:
                nexti = self.tabIndices[waitinghandles[0]]
            else:
                nexti = (self.tabIndices[self.currentConvo.title()] + 1) % self.tabs.count()
            self.tabs.setCurrentIndex(nexti)

    def closeSoft(self):
        self.softclose = True
        self.close()
    def updateBlocked(self, handle):
        i = self.tabIndices[handle]
        icon = QtGui.QIcon(self.mainwindow.theme["main/chums/moods/blocked/icon"])
        self.tabs.setTabIcon(i, icon)
        if self.tabs.currentIndex() == i:
            self.setWindowIcon(icon)
    def updateMood(self, handle, mood, unblocked=False):
        i = self.tabIndices[handle]
        if handle in self.mainwindow.config.getBlocklist() and not unblocked:
            icon = QtGui.QIcon(self.mainwindow.theme["main/chums/moods/blocked/icon"])
        else:
            icon = mood.icon(self.mainwindow.theme)
        self.tabs.setTabIcon(i, icon)
        if self.tabs.currentIndex() == i:
            self.setWindowIcon(icon)
    def closeEvent(self, event):
        if not self.softclose:
            while self.tabs.count() > 0:
                self.tabClose(0)
        self.windowClosed.emit()
    def focusInEvent(self, event):
        # make sure we're not switching tabs!
        i = self.tabs.tabAt(self.mapFromGlobal(QtGui.QCursor.pos()))
        if i == -1:
              i = self.tabs.currentIndex()
        handle = unicode(self.tabs.tabText(i))
        self.clearNewMessage(handle)
    def convoHasFocus(self, handle):
        i = self.tabIndices[handle]
        if (self.tabs.currentIndex() == i and
            (self.hasFocus() or self.tabs.hasFocus())):
            return True
        else:
            return False
    def notifyNewMessage(self, handle):
        i = self.tabIndices[handle]
        self.tabs.setTabTextColor(i, QtGui.QColor(self.mainwindow.theme["%s/tabs/newmsgcolor" % (self.type)]))
        convo = self.convos[handle]
        def func():
            convo.showChat()
        self.mainwindow.waitingMessages.addMessage(handle, func)
        # set system tray
    def clearNewMessage(self, handle):
        try:
            i = self.tabIndices[handle]
            self.tabs.setTabTextColor(i, self.defaultTabTextColor)
        except KeyError:
            pass
        self.mainwindow.waitingMessages.messageAnswered(handle)
    def initTheme(self, theme):
        self.resize(*theme["convo/size"])
        self.setStyleSheet(theme["convo/tabwindow/style"])
        self.tabs.setShape(theme["convo/tabs/tabstyle"])
        self.tabs.setStyleSheet("QTabBar::tab{ %s } QTabBar::tab:selected { %s }" % (theme["convo/tabs/style"], theme["convo/tabs/selectedstyle"]))

    def changeTheme(self, theme):
        self.initTheme(theme)
        for c in self.convos.values():
            tabi = self.tabIndices[c.title()]
            self.tabs.setTabIcon(tabi, c.icon())
        currenttabi = self.tabs.currentIndex()
        if currenttabi >= 0:
            currentHandle = unicode(self.tabs.tabText(self.tabs.currentIndex()))
            self.setWindowIcon(self.convos[currentHandle].icon())
        self.defaultTabTextColor = self.getTabTextColor()

    @QtCore.pyqtSlot(int)
    def tabClose(self, i):
        handle = unicode(self.tabs.tabText(i))
        self.mainwindow.waitingMessages.messageAnswered(handle)
        convo = self.convos[handle]
        del self.convos[handle]
        del self.tabIndices[handle]
        self.tabs.removeTab(i)
        for (h, j) in self.tabIndices.iteritems():
            if j > i:
                self.tabIndices[h] = j-1
        self.layout.removeWidget(convo)
        convo.close()
        if self.tabs.count() == 0:
            self.close()
            return
        if self.currentConvo == convo:
            currenti = self.tabs.currentIndex()
            currenth = unicode(self.tabs.tabText(currenti))
            self.currentConvo = self.convos[currenth]
        self.currentConvo.raiseChat()

    @QtCore.pyqtSlot(int)
    def changeTab(self, i):
        if i < 0:
            return
        if self.changedTab:
            self.changedTab = False
            return
        handle = unicode(self.tabs.tabText(i))
        convo = self.convos[handle]
        if self.currentConvo:
            self.layout.removeWidget(self.currentConvo)
        self.currentConvo = convo
        self.layout.addWidget(convo)
        self.setWindowIcon(convo.icon())
        self.setWindowTitle(convo.title())
        self.activateWindow()
        self.raise_()
        convo.raiseChat()

    @QtCore.pyqtSlot(int, int)
    def tabMoved(self, to, fr):
        l = self.tabIndices
        for i in l:
            if l[i] == fr:
                oldpos = i
            if l[i] == to:
                newpos = i
        l[oldpos] = to
        l[newpos] = fr

    windowClosed = QtCore.pyqtSignal()

class PesterMovie(QtGui.QMovie):
    def __init__(self, parent):
        QtGui.QMovie.__init__(self, parent)
        self.textwindow = parent
    @QtCore.pyqtSlot(int)
    def animate(self, frame):
        text = self.textwindow
        if text.mainwindow.config.animations():
            movie = self
            url = text.urls[movie].toString()
            html = unicode(text.toHtml())
            if html.find(url) != -1:
                if text.hasTabs:
                    i = text.tabobject.tabIndices[text.parent().title()]
                    if text.tabobject.tabs.currentIndex() == i:
                        text.document().addResource(QtGui.QTextDocument.ImageResource,
                                          text.urls[movie], movie.currentPixmap())
                        text.setLineWrapColumnOrWidth(text.lineWrapColumnOrWidth())
                else:
                    text.document().addResource(QtGui.QTextDocument.ImageResource,
                                       text.urls[movie], movie.currentPixmap())
                    text.setLineWrapColumnOrWidth(text.lineWrapColumnOrWidth())

class PesterText(QtGui.QTextEdit):
    def __init__(self, theme, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        if hasattr(self.parent(), 'mainwindow'):
            self.mainwindow = self.parent().mainwindow
        else:
            self.mainwindow = self.parent()
        if type(parent.parent()) is PesterTabWindow:
            self.tabobject = parent.parent()
            self.hasTabs = True
        else:
            self.hasTabs = False
        self.initTheme(theme)
        self.setReadOnly(True)
        self.setMouseTracking(True)
        self.textSelected = False
        self.connect(self, QtCore.SIGNAL('copyAvailable(bool)'),
                     self, QtCore.SLOT('textReady(bool)'))
        self.urls = {}
        for k in smiledict:
            self.addAnimation(QtCore.QUrl("smilies/%s" % (smiledict[k])), "smilies/%s" % (smiledict[k]))
        self.connect(self.mainwindow, QtCore.SIGNAL('animationSetting(bool)'),
                     self, QtCore.SLOT('animateChanged(bool)'))
    def addAnimation(self, url, fileName):
        movie = PesterMovie(self)
        movie.setFileName(fileName)
        movie.setCacheMode(QtGui.QMovie.CacheAll)
        if movie.frameCount() > 1:
            self.urls[movie] = url
            movie.connect(movie, QtCore.SIGNAL('frameChanged(int)'),
                          movie, QtCore.SLOT('animate(int)'))
            #movie.start()
    @QtCore.pyqtSlot(bool)
    def animateChanged(self, animate):
        if animate:
            for m in self.urls:
                html = unicode(self.toHtml())
                if html.find(self.urls[m].toString()) != -1:
                    if m.frameCount() > 1:
                        m.start()
        else:
            for m in self.urls:
                html = unicode(self.toHtml())
                if html.find(self.urls[m].toString()) != -1:
                    if m.frameCount() > 1:
                        m.stop()

    @QtCore.pyqtSlot(bool)
    def textReady(self, ready):
        self.textSelected = ready
    def initTheme(self, theme):
        if theme.has_key("convo/scrollbar"):
            self.setStyleSheet("QTextEdit { %s } QScrollBar:vertical { %s } QScrollBar::handle:vertical { %s } QScrollBar::add-line:vertical { %s } QScrollBar::sub-line:vertical { %s } QScrollBar:up-arrow:vertical { %s } QScrollBar:down-arrow:vertical { %s }" % (theme["convo/textarea/style"], theme["convo/scrollbar/style"], theme["convo/scrollbar/handle"], theme["convo/scrollbar/downarrow"], theme["convo/scrollbar/uparrow"], theme["convo/scrollbar/uarrowstyle"], theme["convo/scrollbar/darrowstyle"] ))
        else:
            self.setStyleSheet("QTextEdit { %s }" % (theme["convo/textarea/style"]))
    def addMessage(self, lexmsg, chum):
        if len(lexmsg) == 0:
            return
        color = chum.colorcmd()
        systemColor = QtGui.QColor(self.parent().mainwindow.theme["convo/systemMsgColor"])
        initials = chum.initials()
        parent = self.parent()
        window = parent.mainwindow
        me = window.profile()
        if self.mainwindow.config.animations():
            for m in self.urls:
                if convertTags(lexmsg).find(self.urls[m].toString()) != -1:
                    if m.state() == QtGui.QMovie.NotRunning:
                        m.start()
        if self.parent().mainwindow.config.showTimeStamps():
            if self.parent().mainwindow.config.time12Format():
                time = strftime("[%I:%M")
            else:
                time = strftime("[%H:%M")
            if self.parent().mainwindow.config.showSeconds():
                time += strftime(":%S] ")
            else:
                time += "] "
        else:
            time = ""
        if lexmsg[0] == "PESTERCHUM:BEGIN":
            parent.setChumOpen(True)
            pmsg = chum.pestermsg(me, systemColor, window.theme["convo/text/beganpester"])
            window.chatlog.log(chum.handle, pmsg)
            self.append(convertTags(pmsg))
        elif lexmsg[0] == "PESTERCHUM:CEASE":
            parent.setChumOpen(False)
            pmsg = chum.pestermsg(me, systemColor, window.theme["convo/text/ceasepester"])
            window.chatlog.log(chum.handle, pmsg)
            self.append(convertTags(pmsg))
        elif lexmsg[0] == "PESTERCHUM:BLOCK":
            pmsg = chum.pestermsg(me, systemColor, window.theme['convo/text/blocked'])
            window.chatlog.log(chum.handle, pmsg)
            self.append(convertTags(pmsg))
        elif lexmsg[0] == "PESTERCHUM:UNBLOCK":
            pmsg = chum.pestermsg(me, systemColor, window.theme['convo/text/unblocked'])
            window.chatlog.log(chum.handle, pmsg)
            self.append(convertTags(pmsg))
        elif lexmsg[0] == "PESTERCHUM:BLOCKED":
            pmsg = chum.pestermsg(me, systemColor, window.theme['convo/text/blockedmsg'])
            window.chatlog.log(chum.handle, pmsg)
            self.append(convertTags(pmsg))
        elif lexmsg[0] == "PESTERCHUM:IDLE":
            imsg = chum.idlemsg(systemColor, window.theme['convo/text/idle'])
            window.chatlog.log(chum.handle, imsg)
            self.append(convertTags(imsg))
        elif type(lexmsg[0]) is mecmd:
            memsg = chum.memsg(systemColor, lexmsg)
            if chum is me:
                window.chatlog.log(parent.chum.handle, memsg)
            else:
                window.chatlog.log(chum.handle, memsg)
            self.append(time + convertTags(memsg))
        else:
            if not parent.chumopen and chum is not me:
                beginmsg = chum.pestermsg(me, systemColor, window.theme["convo/text/beganpester"])
                parent.setChumOpen(True)
                window.chatlog.log(chum.handle, beginmsg)
                self.append(convertTags(beginmsg))

            lexmsg[0:0] = [colorBegin("<c=%s>" % (color), color),
                           "%s: " % (initials)]
            lexmsg.append(colorEnd("</c>"))
            self.append("<span style=\"color:#000000\">" + time + convertTags(lexmsg) + "</span>")
            #self.append('<img src="/Users/lexi/pesterchum-lex/smilies/tab.gif" />'
            #            + '<img src="/Users/lexi/pesterchum/smilies/tab.gif" />'
            #            + '<img src="/Applications/Pesterchum.app/Contents/Resources/smilies/tab.gif" />'
            #            + '<img src="smilies/tab.gif" />');
            if chum is me:
                window.chatlog.log(parent.chum.handle, lexmsg)
            else:
                if window.idleaction.isChecked() and parent.chumopen:
                    idlethreshhold = 60
                    if (not hasattr(self, 'lastmsg')) or \
                            datetime.now() - self.lastmsg > timedelta(0,idlethreshhold):
                        verb = window.theme["convo/text/idle"]
                        idlemsg = me.idlemsg(systemColor, verb)
                        parent.textArea.append(convertTags(idlemsg))
                        window.chatlog.log(parent.title(), idlemsg)
                        parent.messageSent.emit("PESTERCHUM:IDLE", parent.title())
                self.lastmsg = datetime.now()
                window.chatlog.log(chum.handle, lexmsg)
    def changeTheme(self, theme):
        self.initTheme(theme)
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())
    def focusInEvent(self, event):
        self.parent().clearNewMessage()
        QtGui.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if hasattr(self.parent(), 'textInput'):
            if event.key() not in [QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown, \
                                   QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
                self.parent().textInput.keyPressEvent(event)
        QtGui.QTextEdit.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            url = self.anchorAt(event.pos())
            if url != "":
                if url[0] == "#" and url != "#pesterchum":
                    self.parent().mainwindow.showMemos(url[1:])
                elif url[0] == "@":
                    handle = unicode(url[1:])
                    self.parent().mainwindow.newConversation(handle)
                else:
                    if event.modifiers() == QtCore.Qt.ControlModifier:
                        QtGui.QApplication.clipboard().setText(url)
                    else:
                        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url, QtCore.QUrl.TolerantMode))
        QtGui.QTextEdit.mousePressEvent(self, event)
    def mouseMoveEvent(self, event):
        QtGui.QTextEdit.mouseMoveEvent(self, event)
        if self.anchorAt(event.pos()):
            if self.viewport().cursor().shape != QtCore.Qt.PointingHandCursor:
                self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

    def contextMenuEvent(self, event):
        textMenu = self.createStandardContextMenu()
        if self.textSelected:
            self.submitLogAction = QtGui.QAction("Submit to Pesterchum QDB", self)
            self.connect(self.submitLogAction, QtCore.SIGNAL('triggered()'),
                         self, QtCore.SLOT('submitLog()'))
            textMenu.addAction(self.submitLogAction)
        textMenu.exec_(event.globalPos())

    def submitLogTitle(self):
        return "[%s -> %s]" % (self.parent().mainwindow.profile().handle,
                               self.parent().chum.handle)

    @QtCore.pyqtSlot()
    def submitLog(self):
        mimedata = self.createMimeDataFromSelection()
        htmldata = img2smiley(mimedata.data("text/html"))
        textdoc = QtGui.QTextDocument()
        textdoc.setHtml(htmldata)
        logdata = "%s\n%s" % (self.submitLogTitle(), textdoc.toPlainText())
        self.sending = QtGui.QDialog(self)
        layout = QtGui.QVBoxLayout()
        self.sending.sendinglabel = QtGui.QLabel("S3ND1NG...", self.sending)
        cancelbutton = QtGui.QPushButton("OK", self.sending)
        self.sending.connect(cancelbutton, QtCore.SIGNAL('clicked()'),
                             self.sending, QtCore.SLOT('close()'))
        layout.addWidget(self.sending.sendinglabel)
        layout.addWidget(cancelbutton)
        self.sending.setLayout(layout)
        self.sending.show()
        params = urllib.urlencode({'quote': logdata, 'do': "add"})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        try:
            pass
            hconn = httplib.HTTPConnection('qdb.pesterchum.net', 80,
                                           timeout=15)
            hconn.request("POST", "/index.php", params, headers)
            response = hconn.getresponse()
            if response.status == 200:
                self.sending.sendinglabel.setText("SUCC3SS!")
            else:
                self.sending.sendinglabel.setText("F41L3D: %s %s" % (response.status, response.reason))
            hconn.close()
        except Exception, e:
            self.sending.sendinglabel.setText("F41L3D: %s" % (e))
        del self.sending

class PesterInput(QtGui.QLineEdit):
    def __init__(self, theme, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setStyleSheet(theme["convo/input/style"])
    def changeTheme(self, theme):
        self.setStyleSheet(theme["convo/input/style"])
    def focusInEvent(self, event):
        self.parent().clearNewMessage()
        self.parent().textArea.textCursor().clearSelection()
        QtGui.QLineEdit.focusInEvent(self, event)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            text = unicode(self.text())
            next = self.parent().history.next(text)
            if next is not None:
                self.setText(next)
        elif event.key() == QtCore.Qt.Key_Down:
            prev = self.parent().history.prev()
            if prev is not None:
                self.setText(prev)
        elif event.key() in [QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]:
            self.parent().textArea.keyPressEvent(event)
        self.parent().mainwindow.idletime = 0
        QtGui.QLineEdit.keyPressEvent(self, event)

class PesterConvo(QtGui.QFrame):
    def __init__(self, chum, initiated, mainwindow, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.setObjectName(chum.handle)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.chum = chum
        self.mainwindow = mainwindow
        theme = self.mainwindow.theme
        self.resize(*theme["convo/size"])
        self.setStyleSheet("QFrame#%s { %s }" % (chum.handle, theme["convo/style"]))
        self.setWindowIcon(self.icon())
        self.setWindowTitle(self.title())

        t = Template(self.mainwindow.theme["convo/chumlabel/text"])

        self.chumLabel = QtGui.QLabel(t.safe_substitute(handle=chum.handle), self)
        self.chumLabel.setStyleSheet(self.mainwindow.theme["convo/chumlabel/style"])
        self.chumLabel.setAlignment(self.aligndict["h"][self.mainwindow.theme["convo/chumlabel/align/h"]] | self.aligndict["v"][self.mainwindow.theme["convo/chumlabel/align/v"]])
        self.chumLabel.setMaximumHeight(self.mainwindow.theme["convo/chumlabel/maxheight"])
        self.chumLabel.setMinimumHeight(self.mainwindow.theme["convo/chumlabel/minheight"])
        self.chumLabel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding))
        self.textArea = PesterText(self.mainwindow.theme, self)
        self.textInput = PesterInput(self.mainwindow.theme, self)
        self.textInput.setFocus()

        self.connect(self.textInput, QtCore.SIGNAL('returnPressed()'),
                     self, QtCore.SLOT('sentMessage()'))

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.chumLabel)
        self.layout.addWidget(self.textArea)
        self.layout.addWidget(self.textInput)
        self.layout.setSpacing(0)
        margins = self.mainwindow.theme["convo/margins"]
        self.layout.setContentsMargins(margins["left"], margins["top"],
                                      margins["right"], margins["bottom"])

        self.setLayout(self.layout)

        self.optionsMenu = QtGui.QMenu(self)
        self.optionsMenu.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.addChumAction = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/addchum"], self)
        self.connect(self.addChumAction, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('addThisChum()'))
        self.blockAction = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/blockchum"], self)
        self.connect(self.blockAction, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('blockThisChum()'))
        self.quirksOff = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/quirksoff"], self)
        self.quirksOff.setCheckable(True)
        self.connect(self.quirksOff, QtCore.SIGNAL('toggled(bool)'),
                     self, QtCore.SLOT('toggleQuirks(bool)'))
        self.oocToggle = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/ooc"], self)
        self.oocToggle.setCheckable(True)
        self.connect(self.oocToggle, QtCore.SIGNAL('toggled(bool)'),
                     self, QtCore.SLOT('toggleOOC(bool)'))
        self.unblockchum = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/unblockchum"], self)
        self.connect(self.unblockchum, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('unblockChumSlot()'))
        self.reportchum = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/report"], self)
        self.connect(self.reportchum, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('reportThisChum()'))
        self.logchum = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/viewlog"], self)
        self.connect(self.logchum, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('openChumLogs()'))

        self.optionsMenu.addAction(self.quirksOff)
        self.optionsMenu.addAction(self.oocToggle)
        self.optionsMenu.addAction(self.logchum)
        self.optionsMenu.addAction(self.addChumAction)
        self.optionsMenu.addAction(self.blockAction)
        self.optionsMenu.addAction(self.reportchum)

        self.chumopen = False
        self.applyquirks = True
        self.ooc = False

        if parent:
            parent.addChat(self)
        if initiated:
            msg = self.mainwindow.profile().pestermsg(self.chum, QtGui.QColor(self.mainwindow.theme["convo/systemMsgColor"]), self.mainwindow.theme["convo/text/beganpester"])
            self.setChumOpen(True)
            self.textArea.append(convertTags(msg))
            self.mainwindow.chatlog.log(self.title(), msg)
        self.newmessage = False
        self.history = PesterHistory()

    def title(self):
        return self.chum.handle
    def icon(self):
        return self.chum.mood.icon(self.mainwindow.theme)
    def myUpdateMood(self, mood):
        chum = self.mainwindow.profile()
        syscolor = QtGui.QColor(self.mainwindow.theme["convo/systemMsgColor"])
        msg = chum.moodmsg(mood, syscolor, self.mainwindow.theme)
        self.textArea.append(convertTags(msg))
        self.mainwindow.chatlog.log(self.title(), msg)

    def updateMood(self, mood, unblocked=False, old=None):
        syscolor = QtGui.QColor(self.mainwindow.theme["convo/systemMsgColor"])
        #~ if mood.name() == "offline" and self.chumopen == True and not unblocked:
            #~ self.mainwindow.ceasesound.play()
            #~ msg = self.chum.pestermsg(self.mainwindow.profile(), syscolor, self.mainwindow.theme["convo/text/ceasepester"])
            #~ self.textArea.append(convertTags(msg))
            #~ self.mainwindow.chatlog.log(self.title(), msg)
            #~ self.chumopen = False
        if old and old.name() != mood.name():
            msg = self.chum.moodmsg(mood, syscolor, self.mainwindow.theme)
            self.textArea.append(convertTags(msg))
            self.mainwindow.chatlog.log(self.title(), msg)
        if self.parent():
            self.parent().updateMood(self.title(), mood, unblocked)
        else:
            if self.chum.blocked(self.mainwindow.config) and not unblocked:
                self.setWindowIcon(QtGui.QIcon(self.mainwindow.theme["main/chums/moods/blocked/icon"]))
                self.optionsMenu.addAction(self.unblockchum)
                self.optionsMenu.removeAction(self.blockAction)
            else:
                self.setWindowIcon(mood.icon(self.mainwindow.theme))
                self.optionsMenu.removeAction(self.unblockchum)
                self.optionsMenu.addAction(self.blockAction)
        # print mood update?
    def updateBlocked(self):
        if self.parent():
            self.parent().updateBlocked(self.title())
        else:
            self.setWindowIcon(QtGui.QIcon(self.mainwindow.theme["main/chums/moods/blocked/icon"]))
        self.optionsMenu.addAction(self.unblockchum)
        self.optionsMenu.removeAction(self.blockAction)

    def updateColor(self, color):
        self.chum.color = color
    def addMessage(self, msg, me=True):
        if type(msg) in [str, unicode]:
            lexmsg = lexMessage(msg)
        else:
            lexmsg = msg
        if me:
            chum = self.mainwindow.profile()
        else:
            chum = self.chum
            self.notifyNewMessage()
        self.textArea.addMessage(lexmsg, chum)

    def notifyNewMessage(self):
        # first see if this conversation HASS the focus
        if not (self.hasFocus() or self.textArea.hasFocus() or
                self.textInput.hasFocus() or
                (self.parent() and self.parent().convoHasFocus(self.title()))):
            # ok if it has a tabconvo parent, send that the notify.
            if self.parent():
                self.parent().notifyNewMessage(self.title())
                if type(self.parent()).__name__ == "PesterTabWindow":
                  if self.mainwindow.config.blink() & self.mainwindow.config.PBLINK:
                    self.mainwindow.gainAttention.emit(self.parent())
                elif type(self.parent()).__name__ == "MemoTabWindow":
                  if self.mainwindow.config.blink() & self.mainwindow.config.MBLINK:
                    self.mainwindow.gainAttention.emit(self.parent())
            # if not change the window title and update system tray
            else:
                self.newmessage = True
                self.setWindowTitle(self.title()+"*")
                def func():
                    self.showChat()
                self.mainwindow.waitingMessages.addMessage(self.title(), func)
                if type(self).__name__ == "PesterConvo":
                  if self.mainwindow.config.blink() & self.mainwindow.config.PBLINK:
                    self.mainwindow.gainAttention.emit(self)
                elif type(self).__name__ == "PesterMemo":
                  if self.mainwindow.config.blink() & self.mainwindow.config.MBLINK:
                    self.mainwindow.gainAttention.emit(self)

    def clearNewMessage(self):
        if self.parent():
            self.parent().clearNewMessage(self.title())
        elif self.newmessage:
            self.newmessage = False
            self.setWindowTitle(self.title())
            self.mainwindow.waitingMessages.messageAnswered(self.title())
            # reset system tray
    def focusInEvent(self, event):
        self.clearNewMessage()
        self.textInput.setFocus()

    def raiseChat(self):
        self.activateWindow()
        self.raise_()
        self.textInput.setFocus()

    def showChat(self):
        if self.parent():
            self.parent().showChat(self.title())
        self.raiseChat()
    def contextMenuEvent(self, event):
        if event.reason() == QtGui.QContextMenuEvent.Mouse:
            self.optionsMenu.popup(event.globalPos())
    def closeEvent(self, event):
        self.mainwindow.waitingMessages.messageAnswered(self.title())
        for movie in self.textArea.urls:
            movie.stop()
            del movie
        self.windowClosed.emit(self.title())

    def setChumOpen(self, o):
        self.chumopen = o
    def changeTheme(self, theme):
        self.resize(*theme["convo/size"])
        self.setStyleSheet("QFrame#%s { %s }" % (self.chum.handle, theme["convo/style"]))

        margins = theme["convo/margins"]
        self.layout.setContentsMargins(margins["left"], margins["top"],
                                       margins["right"], margins["bottom"])

        self.setWindowIcon(self.icon())
        t = Template(self.mainwindow.theme["convo/chumlabel/text"])
        self.chumLabel.setText(t.safe_substitute(handle=self.title()))
        self.chumLabel.setStyleSheet(theme["convo/chumlabel/style"])
        self.chumLabel.setAlignment(self.aligndict["h"][self.mainwindow.theme["convo/chumlabel/align/h"]] | self.aligndict["v"][self.mainwindow.theme["convo/chumlabel/align/v"]])
        self.chumLabel.setMaximumHeight(self.mainwindow.theme["convo/chumlabel/maxheight"])
        self.chumLabel.setMinimumHeight(self.mainwindow.theme["convo/chumlabel/minheight"])
        self.chumLabel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding))
        self.quirksOff.setText(self.mainwindow.theme["main/menus/rclickchumlist/quirksoff"])
        self.addChumAction.setText(self.mainwindow.theme["main/menus/rclickchumlist/addchum"])
        self.blockAction.setText(self.mainwindow.theme["main/menus/rclickchumlist/blockchum"])
        self.unblockchum.setText(self.mainwindow.theme["main/menus/rclickchumlist/unblockchum"])
        self.logchum.setText(self.mainwindow.theme["main/menus/rclickchumlist/viewlog"])

        self.textArea.changeTheme(theme)
        self.textInput.changeTheme(theme)


    @QtCore.pyqtSlot()
    def sentMessage(self):
        text = unicode(self.textInput.text())
        if text == "" or text[0:11] == "PESTERCHUM:":
            return
        oocDetected = oocre.match(text.strip())
        if self.ooc and not oocDetected:
            text = "(( %s ))" % (text)
        self.history.add(text)
        quirks = self.mainwindow.userprofile.quirks
        lexmsg = lexMessage(text)
        if type(lexmsg[0]) is not mecmd and self.applyquirks and not (self.ooc or oocDetected):
            try:
                lexmsg = quirks.apply(lexmsg)
            except:
                msgbox = QtGui.QMessageBox()
                msgbox.setText("Whoa there! There seems to be a problem.")
                msgbox.setInformativeText("A quirk seems to be having a problem. (Possibly you're trying to capture a non-existant group?)")
                msgbox.exec_()
                return
        lexmsgs = splitMessage(lexmsg)

        for lm in lexmsgs:
            serverMsg = copy(lm)
            self.addMessage(lm, True)
            # if ceased, rebegin
            if hasattr(self, 'chumopen') and not self.chumopen:
                self.mainwindow.newConvoStarted.emit(QtCore.QString(self.title()), True)
                self.setChumOpen(True)
            text = convertTags(serverMsg, "ctag")
            self.messageSent.emit(text, self.title())
        self.textInput.setText("")

    @QtCore.pyqtSlot()
    def addThisChum(self):
        self.mainwindow.addChum(self.chum)
    @QtCore.pyqtSlot()
    def blockThisChum(self):
        self.mainwindow.blockChum(self.chum.handle)
    @QtCore.pyqtSlot()
    def reportThisChum(self):
        self.mainwindow.reportChum(self.chum.handle)
    @QtCore.pyqtSlot()
    def unblockChumSlot(self):
        self.mainwindow.unblockChum(self.chum.handle)
    @QtCore.pyqtSlot(bool)
    def toggleQuirks(self, toggled):
        self.applyquirks = not toggled
    @QtCore.pyqtSlot(bool)
    def toggleOOC(self, toggled):
        self.ooc = toggled
    @QtCore.pyqtSlot()
    def openChumLogs(self):
        currentChum = self.chum.handle
        self.mainwindow.chumList.pesterlogviewer = PesterLogViewer(currentChum, self.mainwindow.config, self.mainwindow.theme, self.mainwindow)
        self.connect(self.mainwindow.chumList.pesterlogviewer, QtCore.SIGNAL('rejected()'),
                     self.mainwindow.chumList, QtCore.SLOT('closeActiveLog()'))
        self.mainwindow.chumList.pesterlogviewer.show()
        self.mainwindow.chumList.pesterlogviewer.raise_()
        self.mainwindow.chumList.pesterlogviewer.activateWindow()

    messageSent = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    windowClosed = QtCore.pyqtSignal(QtCore.QString)

    aligndict = {"h": {"center": QtCore.Qt.AlignHCenter,
                       "left": QtCore.Qt.AlignLeft,
                       "right": QtCore.Qt.AlignRight },
                 "v": {"center": QtCore.Qt.AlignVCenter,
                       "top": QtCore.Qt.AlignTop,
                       "bottom": QtCore.Qt.AlignBottom } }

# the import is way down here to avoid recursive imports
from logviewer import PesterLogViewer
