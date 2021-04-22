# vim: set autoindent ts=4 sts=4 sw=4 textwidth=79 expandtab:
# -*- coding=UTF-8; tab-width: 4 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
import re, os, traceback, sys
import time, datetime
from os import remove

import dataobjs, generic, memos, parsetools, ostools
from version import _pcVersion

try:
    from pnc.attrdict import AttrDict
except ImportError:
    # Fall back on the old location, just in case
    from pnc.dep.attrdict import AttrDict
#~from styling import styler

_datadir = ostools.getDataDir()

import logging
logging.basicConfig(level=logging.WARNING)




class ConsoleWindow(QtWidgets.QDialog):
#~class ConsoleWindow(styler.PesterBaseWindow):
    # A simple console class, cobbled together from the corpse of another.

    stylesheet_path = "main/defaultwindow/style"
    # This is a holder for our text inputs.
    text = AttrDict()
    # I should probably put up constants for 'direction' if this is going to
    # get this complicated. TODO!
    incoming_prefix = "<<<"
    miscinfo_prefix = "==>"
    outgoing_prefix = ">>>"
    neutral_prefix = "!!!"
    waiting_prefix = "..."

    selected_widget = None
    show_info_on_select = True

    _CUSTOM_ENV = {}

    def __init__(self, parent):
        super(ConsoleWindow, self).__init__(parent)
        self.prnt = parent
        try:
            self.mainwindow = parent.mainwindow
        except:
            self.mainwindow = parent
        theme = self.mainwindow.theme
        # This won't initialize the sub-objects, because they don't exist yet.
        self.initTheme(theme)

        self.text = AttrDict()
        self.text.area = ConsoleText(theme, self)
        self.text.input = ConsoleInput(theme, self)
        self.text.input.setFocus()

        self.text.input.returnPressed.connect(self.sentMessage)

        self.text.history = dataobjs.PesterHistory()

        # For backing these up
        self.stdout = self.stderr = None

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.text.area)
        layout_0.addWidget(self.text.input)
        self.setLayout(layout_0)

    def parent(self):
        return self.prnt

    def clearNewMessage(self):
        pass

    @QtCore.pyqtSlot()
    def sentMessage(self):
        text = self.text.input.text()
        # TODO: Make this deal with unicode text, it'll crash and burn as-is.
        text = str(text)
        text = text.rstrip()

        self.text.history.add(text)
        self.text.input.setText("")

        self.execInConsole(text)
        # Scroll down to the bottom so we can see the results.
        sb = self.text.area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def addTraceback(self, tb=None):
        # We should do the formatting here, but eventually pass it to text.area
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
        self.text.area.addMessage(msg, direction=direction)

    def closeEvent(self, event):
        # TODO: Set up ESC to close the console...or refer to hiding it as
        # closing it. Not sure which is preferable.
        parent = self.parent()
        parent.console.is_open = False
        parent.console.window = None
        return super(ConsoleWindow, self).closeEvent(event)

    def hideEvent(self, event):
        parent = self.parent()
        parent.console.is_open = False

    def initTheme(self, theme):
        # Set up our style/window specifics
        self.changeTheme(theme)
        self.resize(400,600)

    def changeTheme(self, theme):
        self.setStyleSheet(theme[self.stylesheet_path])
        self.setWindowTitle("==> Console")
        if "area" in self.text and "input" in self.text:
            self.text.area.changeTheme(theme)
            self.text.input.changeTheme(theme)

    @QtCore.pyqtSlot()
    def designateCurrentWidget(self):
        # Display and save the current widget!
        # TODO: Consider (reversible) highlighting or selection or something
        # fancy. It'd help people write styles, wouldn't it?
        # ...just remember to use mouseRelease() if you work with hovering.

        # Direction: Misc. Info
        direction = 2

        pos = QtGui.QCursor.pos()
        wgt = QtWidgets.QApplication.widgetAt(pos)
        if wgt is None:
            # Don't set None, for now. May change this later.
            self.addMessage("You need to have your cursor over something " + \
                    "in Pesterchum to use that.",
                    direction=direction)
            return

        self.selected_widget = wgt
        nchild = len(wgt.children())
        output = []
        output.append("CONSOLE.selected_widget = {0!r}".format(wgt))
        output.append("{0: <4}Parent: {1!r}".format('', wgt.parent()))
        output.append("{0: <4}{1:4d} child{2}".format('',
            nchild, ("ren" if abs(nchild) != 1 else "") ))
        if self.show_info_on_select:
            qtss = None
            uses_ss = None
            try:
                qtss = wgt.styleSheet()
            except:
                pass
            else:
                if str(qtss) == str(""):
                    uses_ss, ss_msg = False, "No"
                elif qtss is not None:
                    uses_ss, ss_msg = True, "Yes"
                else:
                    uses_ss, ss_msg = None, "Invalid"

            ss_par, ss_par_msg = None, ""
            if uses_ss is False:
                # TODO: Split this into a sub-function or integrate it into
                # Styler or *something*.
                # The stylesheet was probably defined on a parent higher up.
                # Rungs above the start
                i = 0
                # qtss is still "" from earlier
                while not qtss:
                    try:
                        ss_par = wgt.parent()
                        qtss = ss_par.styleSheet()
                    except:
                        # Can't ascend...and we're still in loop, so we don't
                        # have what we came for.
                        # Either that, or it's incompatible, which means the
                        # ones above are anyway.
                        ss_par = False
                        break
                    else:
                        # Indicate that we got this from a parent
                        i += 1

                if not qtss:
                    # There are no stylesheets here.
                    if ss_par is False:
                        # We had parent issues.
                        # TODO: Specifically indicate invalid parent.
                        uses_ss, ss_msg = None, "Invalid"
                    else:
                        uses_ss, ss_msg = False, "No"
                else:
                    # We got a stylesheet out of this!
                    uses_ss, ss_msg = True, "Yes"
                    #~ss_par_msg = "{0: <4}...on parent ↑{1:d}: {2!r}".format('',
                    ss_par_msg = "{0: <4}...on parent #{1:d}: {2!r}".format('',
                            i, ss_par)

            msg = []
            msg.append("{0: <4}QtSS?: {1}".format('', ss_msg))
            # A stylesheet analyzer would be wonderful here. Perhaps something
            # that tells us how many parent classes define stylesheets?
            if uses_ss:
                if ss_par_msg:
                    # We got this stylesheet from a parent object somewhere.
                    msg.append(ss_par_msg)
                msg.append("{0: <4}".format("Stylesheet:"))
                for ln in qtss.split('\n'):
                    msg.append("{0: <8}".format(ln))

            # Actually add this stuff to the result we're constructing
            output.extend(msg)

        output = '\n'.join(output)
        self.addMessage(output, direction=direction)


    # Actual console stuff.
    def execInConsole(self, scriptstr, env=None):
        # Since that's what imports *us*, this should be okay
        # Tab completion could be set up in ConsoleInput, and would be nice
        import pesterchum as pchum

        if env is None:
            env = pchum._retrieveGlobals()

        # Modify the environment the script will execute in.
        # Fetch from the class/instance first.
        _CUSTOM_ENV = self._CUSTOM_ENV.copy()
        # Modify with some hard-coded environmental additions.
        _CUSTOM_ENV.update({
                "CONSOLE": self,
                "MAINWIN": self.mainwindow,
                "PCONFIG": self.mainwindow.config,
                "exit": lambda: self.mainwindow.exitaction.trigger()
                })
        # Aliases.
        _CUSTOM_ENV.update({
                "quit": _CUSTOM_ENV["exit"]
                })
        # Add whatever additions were set in the main pesterchum file.
        _CUSTOM_ENV.update(pchum._CONSOLE_ENV)

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
                warn = "Console environment item {0!r} already exists in CENV."
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
                    logging.info(repr(result))
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


class ConsoleText(QtWidgets.QTextEdit):
    stylesheet_template = """
        QScrollBar:vertical {{ {style[convo/scrollbar/style]} }}
        QScrollBar::handle:vertical {{ {style[convo/scrollbar/handle]} }}
        QScrollBar::add-line:vertical {{ {style[convo/scrollbar/downarrow]} }}
        QScrollBar::sub-line:vertical {{ {style[convo/scrollbar/uparrow]} }}
        QScrollBar:up-arrow:vertical {{ {style[convo/scrollbar/uarrowstyle]} }}
        QScrollBar:down-arrow:vertical {{ {style[convo/scrollbar/darrowstyle]} }}
        """
    stylesheet_path = "convo/textarea/style"
    # NOTE: Qt applies stylesheets like switching CSS files. They are NOT
    # applied piecemeal.
    # TODO: Consider parsing the themes out into stylesheets with pieces that
    # we can hand to each widget.

    def __init__(self, theme, parent=None):
        super(ConsoleText, self).__init__(parent)
        if hasattr(self.window(), 'mainwindow'):
            self.mainwindow = self.window().mainwindow
        else:
            self.mainwindow = self.window()

        self.hasTabs = False
        self.initTheme(theme)
        self.setReadOnly(True)
        self.setMouseTracking(True)
        self.textSelected = False

        self.copyAvailable[bool].connect(self.textReady)
        self.urls = {}

    # Stripped out animation init - it's all cruft to us.

    @QtCore.pyqtSlot(bool)
    def textReady(self, ready):
        self.textSelected = ready

    def initTheme(self, theme):
        # The basic style...
        stylesheet = "QTextEdit {{ {style[convo/textarea/style]} }}"
        if "convo/scrollbar" in theme:
            # TODO: Make all of this into a Styler mixin, so we can just feed
            # it a theme whenever we want to change.
            # We'd have to define the keys we're affecting, but that shouldn't
            # be too hard - it's what dicts are for.

            # Add the rest.
            stylesheet += '\n' + self.stylesheet_template
        stylesheet = stylesheet.format(style=theme)
        self.setStyleSheet(stylesheet)

    def addMessage(self, msg, direction):
        # Display a message we've received.
        # Direction > 0 == out (sent by us); < 0 == in (sent by script).
        if len(msg) == 0:
            return
        #~color = chum.colorcmd()
        #~initials = chum.initials()
        parent = self.window()
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
        if direction > 1:
            # Misc. Info
            prefix = parent.miscinfo_prefix
        elif direction > 0:
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
        self.appendPlainText(result)

        # Direction doesn't matter here - it's the console.
        self.lastmsg = datetime.datetime.now()
        # This needs to finish being rewritten....

    def appendPlainText(self, text):
        """Add plain text to the end of the document, a la insertPlainText."""
        # Save the old cursor
        oldcur = self.textCursor()
        # Move the cursor to the end of the document for insertion
        self.moveCursor(QtGui.QTextCursor.End)
        # Insert the text
        self.insertPlainText(text)
        # Return the cursor to wherever it was prior
        self.setTextCursor(oldcur)

    def changeTheme(self, theme):
        self.initTheme(theme)
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())

    def focusInEvent(self, event):
        self.window().clearNewMessage()
        super(ConsoleText, self).focusInEvent(event)

    def keyPressEvent(self, event):
        # NOTE: This doesn't give focus to the input bar, which it probably
        # should.
        # karxi: Test for tab changing?
        if self.window().text.input:
            if event.key() not in (QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown,
                                   QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
                self.window().text.input.keyPressEvent(event)

        super(ConsoleText, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            url = self.anchorAt(event.pos())
            if url != "":
                # Skip memo/handle recognition
                # NOTE: Ctrl+Click copies the URL. Maybe it should select it?
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    QtWidgets.QApplication.clipboard().setText(url)
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
        textMenu = self.createStandardContextMenu()
        textMenu.exec_(event.globalPos())


class ConsoleInput(QtWidgets.QLineEdit):
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
        self.window().clearNewMessage()
        self.window().text.area.textCursor().clearSelection()

        super(ConsoleInput, self).focusInEvent(event)

    def keyPressEvent(self, event):
        evtkey = event.key()
        parent = self.window()

        # If a key is pressed here, we're not idle....
        # NOTE: Do we really want everyone knowing we're around if we're
        # messing around in the console? Hm.
        parent.mainwindow.idler.time = 0
        
        if evtkey == QtCore.Qt.Key_Up:
            text = str(self.text())
            next = parent.text.history.next(text)
            if next is not None:
                self.setText(next)
        elif evtkey == QtCore.Qt.Key_Down:
            prev = parent.text.history.prev()
            if prev is not None:
                self.setText(prev)
        elif evtkey in (QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown):
            parent.text.area.keyPressEvent(event)
        else:
            super(ConsoleInput, self).keyPressEvent(event)
