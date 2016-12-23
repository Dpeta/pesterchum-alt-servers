# vim: set autoindent ts=4 softtabstop=4 shiftwidth=4 textwidth=79 expandtab:
# -*- coding=UTF-8; tab-width: 4 -*-

from PyQt4 import QtGui, QtCore
import re, os, traceback, sys
import time, datetime
from os import remove

import dataobjs, generic, memos, parsetools, ostools
from version import _pcVersion

_datadir = ostools.getDataDir()

import logging
logging.basicConfig(level=logging.WARNING)




class ConsoleWindow(QtGui.QDialog):
    # A simple console class, cobbled together from the corpse of another.

    textArea = None
    textInput = None
    history = None
    # I should probably put up constants for 'direction' if this is going to
    # get this complicated. TODO!
    incoming_prefix = "<<<"
    outgoing_prefix = ">>>"
    neutral_prefix = "!!!"
    waiting_prefix = "..."

    def __init__(self, parent):
        super(ConsoleWindow, self).__init__(parent)
        self.prnt = parent
        try:
            self.mainwindow = parent.mainwindow
        except:
            self.mainwindow = parent
        theme = self.mainwindow.theme

        # Set up our style/window specifics
        self.setStyleSheet(theme["main/defaultwindow/style"])
        self.setWindowTitle("==> Console")
        self.resize(350,300)

        self.textArea = ConsoleText(theme, self)
        self.textInput = ConsoleInput(theme, self)
        self.textInput.setFocus()

        self.connect(self.textInput, QtCore.SIGNAL('returnPressed()'),
                     self, QtCore.SLOT('sentMessage()'))

        self.chumopen = True
        self.chum = self.mainwindow.profile()
        self.history = dataobjs.PesterHistory()

        # For backing these up
        self.stdout = self.stderr = None

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.textArea)
        layout_0.addWidget(self.textInput)
        self.setLayout(layout_0)

    def parent(self):
        return self.prnt

    def clearNewMessage(self):
        pass

    @QtCore.pyqtSlot()
    def sentMessage(self):
        text = self.textInput.text()
        # TODO: Make this deal with unicode text, it'll crash and burn as-is.
        text = str(text)
        text = text.rstrip()

        self.history.add(text)
        self.textInput.setText("")

        self.execInConsole(text)
        # Scroll down to the bottom so we can see the results.
        sb = self.textArea.verticalScrollBar()
        sb.setValue(sb.maximum())

    def addTraceback(self, tb=None):
        # We should do the formatting here, but eventually pass it to textArea
        # to addMessage whatever output we produced.
        # If we're called by addMessage - and we should be - then sys.stdout is
        # still being redirected into the console.
        # TODO: Just make an object for setting contexts (and thus optionally
        # redirecting prints). Use 'with', of course.
        # TODO: Make this exclude *our* processing from the traceback stack.
        try:
            self.addMessage(traceback.format_exc(), direction=0)
        except Exception as err:
            logging.error("Failed to display error message (???): %s" % err)

    def addMessage(self, msg, direction):
        # Redirect to where these things belong.
        self.textArea.addMessage(msg, direction=direction)

    def closeEvent(self, event):
        # TODO: Set up ESC to close the console...or refer to hiding it as
        # closing it. Not sure which is preferable.
        parent = self.parent()
        parent.console.is_open = False
        parent.console.window = None

    # Actual console stuff.
    def execInConsole(self, scriptstr, env=None):
        # Since that's what imports *us*, this should be okay
        # Tab completion could be set up in ConsoleInput, and would be nice
        import pesterchum as pchum

        if env is None:
            env = pchum._retrieveGlobals()

        # Modify the environment the script will execute in.
        _CUSTOM_ENV = {
                "CONSOLE": self,
                "MAINWIN": self.mainwindow,
                "PCONFIG": self.mainwindow.config
                }
        _CUSTOM_ENV_USED = []
        cenv = pchum.__dict__
        # Display the input we provided
        # We do this here, *before* we do our variable injection, so that it
        # doesn't have to be part of the try statement, where it could
        # potentially complicate matters/give false positives.
        self.addMessage(scriptstr, 1)
        for k in _CUSTOM_ENV:
            if k not in cenv:
                # Inject the variable for ease of use.
                cenv[k] = _CUSTOM_ENV[k]
                # Record that we injected it.
                _CUSTOM_ENV_USED.append(k)
            else:
                # Don't overwrite anything!
                warn = "Console environment item {!r} already exists in CENV."
                warn.format(k)
                logging.warning(warn)
        # Because all we did was change a linked AttrDict, we should be fine
        # here.
        try:
            # Replace the old writer (for now)
            sysout, sys.stdout = sys.stdout, self
            try:
                code = compile(scriptstr + '\n', "<string>", "single")
                # Will using cenv instead of env cause problems?...
                result = eval(code, cenv)
            except:
                # Something went wrong.
                self.addTraceback(sys.exc_info()[2])
            else:
                # No errors.
                if result is not None:
                    print repr(result)
            finally:
                # Restore system output.
                sys.stdout = sysout
        finally:
            # Try to clean us out of globals - this might be disabled
            # later.
            for k in _CUSTOM_ENV_USED:
                # Remove the key we added.
                cenv.pop(k, None)

    def write(self, data):
        # Replaces sys.stdout briefly
        # We only ever use this for receiving, so it's safe to assume the
        # direction is always -1.
        if not isinstance(data, list):
            data = data.split('\n')
        for line in data:
            if len(line):
                self.addMessage(line, -1)


class ConsoleText(QtGui.QTextEdit):
    def __init__(self, theme, parent=None):
        super(ConsoleText, self).__init__(parent)
        if hasattr(self.parent(), 'mainwindow'):
            self.mainwindow = self.parent().mainwindow
        else:
            self.mainwindow = self.parent()

        self.hasTabs = False
        self.initTheme(theme)
        self.setReadOnly(True)
        self.setMouseTracking(True)
        self.textSelected = False

        self.connect(self, QtCore.SIGNAL('copyAvailable(bool)'),
                     self, QtCore.SLOT('textReady(bool)'))
        self.urls = {}

    # Stripped out animation init - it's all cruft to us.

    @QtCore.pyqtSlot(bool)
    def textReady(self, ready):
        self.textSelected = ready

    def initTheme(self, theme):
        if theme.has_key("convo/scrollbar"):
            self.setStyleSheet("QTextEdit { %s } QScrollBar:vertical { %s } QScrollBar::handle:vertical { %s } QScrollBar::add-line:vertical { %s } QScrollBar::sub-line:vertical { %s } QScrollBar:up-arrow:vertical { %s } QScrollBar:down-arrow:vertical { %s }" % (theme["convo/textarea/style"], theme["convo/scrollbar/style"], theme["convo/scrollbar/handle"], theme["convo/scrollbar/downarrow"], theme["convo/scrollbar/uparrow"], theme["convo/scrollbar/uarrowstyle"], theme["convo/scrollbar/darrowstyle"] ))
        else:
            self.setStyleSheet("QTextEdit { %s }" % (theme["convo/textarea/style"]))

    def addMessage(self, msg, direction):
        # Display a message we've received.
        # Direction > 0 == out (sent by us); < 0 == in (sent by script).
        if len(msg) == 0:
            return
        #~color = chum.colorcmd()
        #~initials = chum.initials()
        parent = self.parent()
        mwindow = parent.mainwindow

        systemColor = QtGui.QColor(mwindow.theme["convo/systemMsgColor"])

        if mwindow.config.showTimeStamps():
            if mwindow.config.time12Format():
                timestamp = time.strftime("[%I:%M")
            else:
                timestamp = time.strftime("[%H:%M")
            if mwindow.config.showSeconds():
                timestamp += time.strftime(":%S] ")
            else:
                timestamp += "] "
        else:
            timestamp = ""

        # Figure out what prefix to use.
        if direction > 0:
            # Outgoing.
            prefix = parent.outgoing_prefix
        elif direction < 0:
            # Incoming.
            prefix = parent.incoming_prefix
        elif direction == 0:
            # We could just 'else' here, but there might be some oddness later.
            prefix = parent.neutral_prefix

        # Later, this will have to escape things so we don't parse them,
        # likely...hm.
        #~result = "<span style=\"color:#000000\">{} {} {!r}</span>"
        # The input we get is already repr'd...we pass it via print, and thus
        # do that there.
        result = "{}{} {}\n"
        result = result.format(timestamp, prefix, msg)
        #~self.append(result)
        self.insertPlainText(result)

        # Direction doesn't matter here - it's the console.
        self.lastmsg = datetime.datetime.now()
        # This needs to finish being rewritten....

    def changeTheme(self, theme):
        self.initTheme(theme)
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())

    def focusInEvent(self, event):
        self.parent().clearNewMessage()
        super(ConsoleText, self).focusInEvent(event)

    def keyPressEvent(self, event):
        # NOTE: This doesn't give focus to the input bar, which it probably
        # should.
        # karxi: Test for tab changing?
        if hasattr(self.parent(), 'textInput'):
            if event.key() not in (QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown,
                                   QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
                self.parent().textInput.keyPressEvent(event)

        super(ConsoleText, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            url = self.anchorAt(event.pos())
            if url != "":
                # Skip memo/handle recognition
                # NOTE: Ctrl+Click copies the URL. Maybe it should select it?
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    QtGui.QApplication.clipboard().setText(url)
                else:
                    # This'll probably be removed. May change the lexer out.
                    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url, QtCore.QUrl.TolerantMode))

        super(ConsoleText, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Change our cursor when we roll over links (anchors).
        super(ConsoleText, self).mouseMoveEvent(event)
        if self.anchorAt(event.pos()):
            if self.viewport().cursor().shape != QtCore.Qt.PointingHandCursor:
                self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

    def contextMenuEvent(self, event):
        # This is almost certainly no longer necessary.
        textMenu = self.createStandardContextMenu()
        #~if self.textSelected:
        #~    self.submitLogAction = QtGui.QAction("Submit to Pesterchum QDB", self)
        #~    self.connect(self.submitLogAction, QtCore.SIGNAL('triggered()'),
        #~                 self, QtCore.SLOT('submitLog()'))
        #~    textMenu.addAction(self.submitLogAction)
        textMenu.exec_(event.globalPos())


class ConsoleInput(QtGui.QLineEdit):
    """The actual text entry box on a ConsoleWindow."""
    # I honestly feel like this could just be made a private class of
    # ConsoleWindow, but...best not to overcomplicate things.
    stylesheet_path = "convo/input/style"

    def __init__(self, theme, parent=None):
        super(ConsoleInput, self).__init__(parent)

        self.changeTheme(theme)

    def changeTheme(self, theme):
        self.setStyleSheet(theme[self.stylesheet_path])

    def focusInEvent(self, event):
        # We gained focus. Notify the parent window that this happened.
        self.parent().clearNewMessage()
        self.parent().textArea.textCursor().clearSelection()

        super(ConsoleInput, self).focusInEvent(event)

    def keyPressEvent(self, event):
        evtkey = event.key()
        parent = self.parent()

        # If a key is pressed here, we're not idle....
        # NOTE: Do we really want everyone knowing we're around if we're
        # messing around in the console? Hm.
        parent.mainwindow.idler.time = 0
        
        if evtkey == QtCore.Qt.Key_Up:
            text = unicode(self.text())
            next = parent.history.next(text)
            if next is not None:
                self.setText(next)
        elif evtkey == QtCore.Qt.Key_Down:
            prev = parent.history.prev()
            if prev is not None:
                self.setText(prev)
        elif evtkey in (QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown):
            parent.textArea.keyPressEvent(event)
        else:
            super(ConsoleInput, self).keyPressEvent(event)




