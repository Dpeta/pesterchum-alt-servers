from PyQt4 import QtGui, QtCore
import re, ostools

from os import remove
from generic import RightClickList, RightClickTree, MultiTextDialog
from dataobjs import pesterQuirk, PesterProfile
from memos import TimeSlider, TimeInput
from version import _pcVersion

_datadir = ostools.getDataDir()

class PesterQuirkItem(QtGui.QTreeWidgetItem):
    def __init__(self, quirk):
        parent = None
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.quirk = quirk
        self.setText(0, unicode(quirk))
    def update(self, quirk):
        self.quirk = quirk
        self.setText(0, unicode(quirk))
    def __lt__(self, quirkitem):
        """Sets the order of quirks if auto-sorted by Qt. Obsolete now."""
        if self.quirk.type == "prefix":
            return True
        elif (self.quirk.type == "replace" or self.quirk.type == "regexp") and \
                quirkitem.type == "suffix":
            return True
        else:
            return False
class PesterQuirkList(QtGui.QTreeWidget):
    def __init__(self, mainwindow, parent):
        QtGui.QTreeWidget.__init__(self, parent)
        self.resize(400, 200)
        # make sure we have access to mainwindow info like profiles
        self.mainwindow = mainwindow
        self.setStyleSheet("background:black; color:white;")

        self.connect(self, QtCore.SIGNAL('itemChanged(QTreeWidgetItem *, int)'),
                     self, QtCore.SLOT('changeCheckState()'))

        for q in mainwindow.userprofile.quirks:
            item = PesterQuirkItem(q)
            self.addItem(item, False)
        self.changeCheckState()
        #self.setDragEnabled(True)
        #self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.setSortingEnabled(False)
        self.setIndentation(15)
        self.header().hide()

    def addItem(self, item, new=True):
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if item.quirk.on:
            item.setCheckState(0, 2)
        else:
            item.setCheckState(0, 0)
        if new:
            curgroup = self.currentItem()
            if curgroup:
                if curgroup.parent(): curgroup = curgroup.parent()
                item.quirk.quirk["group"] = item.quirk.group = curgroup.text(0)
        found = self.findItems(item.quirk.group, QtCore.Qt.MatchExactly)
        if len(found) > 0:
            found[0].addChild(item)
        else:
            child_1 = QtGui.QTreeWidgetItem([item.quirk.group])
            self.addTopLevelItem(child_1)
            child_1.setFlags(child_1.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            child_1.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.DontShowIndicatorWhenChildless)
            child_1.setCheckState(0,0)
            child_1.setExpanded(True)
            child_1.addChild(item)
        self.changeCheckState()

    def currentQuirk(self):
        if type(self.currentItem()) is PesterQuirkItem:
            return self.currentItem()
        else: return None

    @QtCore.pyqtSlot()
    def upShiftQuirk(self):
        found = self.findItems(self.currentItem().text(0), QtCore.Qt.MatchExactly)
        if len(found): # group
            i = self.indexOfTopLevelItem(found[0])
            if i > 0:
                expand = found[0].isExpanded()
                shifted_item = self.takeTopLevelItem(i)
                self.insertTopLevelItem(i-1, shifted_item)
                shifted_item.setExpanded(expand)
                self.setCurrentItem(shifted_item)
        else: # quirk
            found = self.findItems(self.currentItem().text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            for f in found:
                if not f.isSelected(): continue
                if not f.parent(): continue
                i = f.parent().indexOfChild(f)
                if i > 0: # keep in same group
                    p = f.parent()
                    shifted_item = f.parent().takeChild(i)
                    p.insertChild(i-1, shifted_item)
                    self.setCurrentItem(shifted_item)
                else: # move to another group
                    j = self.indexOfTopLevelItem(f.parent())
                    if j <= 0: continue
                    shifted_item = f.parent().takeChild(i)
                    self.topLevelItem(j-1).addChild(shifted_item)
                    self.setCurrentItem(shifted_item)
            self.changeCheckState()

    @QtCore.pyqtSlot()
    def downShiftQuirk(self):
        found = self.findItems(self.currentItem().text(0), QtCore.Qt.MatchExactly)
        if len(found): # group
            i = self.indexOfTopLevelItem(found[0])
            if i < self.topLevelItemCount()-1 and i >= 0:
                expand = found[0].isExpanded()
                shifted_item = self.takeTopLevelItem(i)
                self.insertTopLevelItem(i+1, shifted_item)
                shifted_item.setExpanded(expand)
                self.setCurrentItem(shifted_item)
        else: # quirk
            found = self.findItems(self.currentItem().text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            for f in found:
                if not f.isSelected(): continue
                if not f.parent(): continue
                i = f.parent().indexOfChild(f)
                if i < f.parent().childCount()-1 and i >= 0:
                    p = f.parent()
                    shifted_item = f.parent().takeChild(i)
                    p.insertChild(i+1, shifted_item)
                    self.setCurrentItem(shifted_item)
                else:
                    j = self.indexOfTopLevelItem(f.parent())
                    if j >= self.topLevelItemCount()-1 or j < 0: continue
                    shifted_item = f.parent().takeChild(i)
                    self.topLevelItem(j+1).insertChild(0, shifted_item)
                    self.setCurrentItem(shifted_item)
            self.changeCheckState()

    @QtCore.pyqtSlot()
    def removeCurrent(self):
        i = self.currentItem()
        found = self.findItems(i.text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        for f in found:
            if not f.isSelected(): continue
            if not f.parent(): # group
                msgbox = QtGui.QMessageBox()
                msgbox.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
                msgbox.setWindowTitle("WARNING!")
                msgbox.setInformativeText("Are you sure you want to delete the quirk group: %s" % (f.text(0)))
                msgbox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                ret = msgbox.exec_()
                if ret == QtGui.QMessageBox.Ok:
                    self.takeTopLevelItem(self.indexOfTopLevelItem(f))
            else:
                f.parent().takeChild(f.parent().indexOfChild(f))
        self.changeCheckState()

    @QtCore.pyqtSlot()
    def addQuirkGroup(self):
        if not hasattr(self, 'addgroupdialog'):
            self.addgroupdialog = None
        if not self.addgroupdialog:
            (gname, ok) = QtGui.QInputDialog.getText(self, "Add Group", "Enter a name for the new quirk group:")
            if ok:
                gname = unicode(gname)
                if re.search("[^A-Za-z0-9_\s]", gname) is not None:
                    msgbox = QtGui.QMessageBox()
                    msgbox.setInformativeText("THIS IS NOT A VALID GROUP NAME")
                    msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                    ret = msgbox.exec_()
                    self.addgroupdialog = None
                    return
                found = self.findItems(gname, QtCore.Qt.MatchExactly)
                if found:
                    msgbox = QtGui.QMessageBox()
                    msgbox.setInformativeText("THIS QUIRK GROUP ALREADY EXISTS")
                    msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
                    ret = msgbox.exec_()
                    return
                child_1 = QtGui.QTreeWidgetItem([gname])
                self.addTopLevelItem(child_1)
                child_1.setFlags(child_1.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                child_1.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.DontShowIndicatorWhenChildless)
                child_1.setCheckState(0,0)
                child_1.setExpanded(True)

            self.addgroupdialog = None

    @QtCore.pyqtSlot()
    def changeCheckState(self):
        index = self.indexOfTopLevelItem(self.currentItem())
        if index == -1:
            for i in range(self.topLevelItemCount()):
                allChecked = True
                noneChecked = True
                for j in range(self.topLevelItem(i).childCount()):
                    if self.topLevelItem(i).child(j).checkState(0):
                        noneChecked = False
                    else:
                        allChecked = False
                if allChecked:    self.topLevelItem(i).setCheckState(0, 2)
                elif noneChecked: self.topLevelItem(i).setCheckState(0, 0)
                else:             self.topLevelItem(i).setCheckState(0, 1)
        else:
            state = self.topLevelItem(index).checkState(0)
            for j in range(self.topLevelItem(index).childCount()):
                self.topLevelItem(index).child(j).setCheckState(0, state)

from copy import copy
from convo import PesterInput, PesterText
from parsetools import convertTags, lexMessage, splitMessage, mecmd, colorBegin, colorEnd, img2smiley, smiledict
import parsetools
from dataobjs import pesterQuirks, PesterHistory
class QuirkTesterWindow(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prnt = parent
        self.mainwindow = parent.mainwindow
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Quirk Tester")
        self.resize(350,300)

        self.textArea = PesterText(self.mainwindow.theme, self)
        self.textInput = PesterInput(self.mainwindow.theme, self)
        self.textInput.setFocus()

        self.connect(self.textInput, QtCore.SIGNAL('returnPressed()'),
                     self, QtCore.SLOT('sentMessage()'))

        self.chumopen = True
        self.chum = self.mainwindow.profile()
        self.history = PesterHistory()

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
        text = unicode(self.textInput.text())

        return parsetools.kxhandleInput(self, text, "menus")

    def addMessage(self, msg, me=True):
        if type(msg) in [str, unicode]:
            lexmsg = lexMessage(msg)
        else:
            lexmsg = msg
        if me:
            chum = self.mainwindow.profile()
        else:
            chum = self.chum
        self.textArea.addMessage(lexmsg, chum)

    def closeEvent(self, event):
        self.parent().quirktester = None

class PesterQuirkTypes(QtGui.QDialog):
    def __init__(self, parent, quirk=None):
        QtGui.QDialog.__init__(self, parent)
        self.mainwindow = parent.mainwindow
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Quirk Wizard")
        self.resize(500,310)

        self.quirk = quirk
        self.pages = QtGui.QStackedWidget(self)

        self.next = QtGui.QPushButton("Next", self)
        self.next.setDefault(True)
        self.connect(self.next, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('nextPage()'))
        self.back = QtGui.QPushButton("Back", self)
        self.back.setEnabled(False)
        self.connect(self.back, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('backPage()'))
        self.cancel = QtGui.QPushButton("Cancel", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.setAlignment(QtCore.Qt.AlignRight)
        layout_2.addWidget(self.back)
        layout_2.addWidget(self.next)
        layout_2.addSpacing(5)
        layout_2.addWidget(self.cancel)

        vr = QtGui.QFrame()
        vr.setFrameShape(QtGui.QFrame.VLine)
        vr.setFrameShadow(QtGui.QFrame.Sunken)
        vr2 = QtGui.QFrame()
        vr2.setFrameShape(QtGui.QFrame.VLine)
        vr2.setFrameShadow(QtGui.QFrame.Sunken)

        self.funclist = QtGui.QListWidget(self)
        self.funclist.setStyleSheet("color: #000000; background-color: #FFFFFF;")
        self.funclist2 = QtGui.QListWidget(self)
        self.funclist2.setStyleSheet("color: #000000; background-color: #FFFFFF;")

        from parsetools import quirkloader
        funcs = [q+"()" for q in quirkloader.quirks.keys()]
        funcs.sort()
        self.funclist.addItems(funcs)
        self.funclist2.addItems(funcs)

        self.reloadQuirkFuncButton = QtGui.QPushButton("RELOAD FUNCTIONS", self)
        self.connect(self.reloadQuirkFuncButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reloadQuirkFuncSlot()'))
        self.reloadQuirkFuncButton2 = QtGui.QPushButton("RELOAD FUNCTIONS", self)
        self.connect(self.reloadQuirkFuncButton2, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reloadQuirkFuncSlot()'))

        self.funclist.setMaximumWidth(160)
        self.funclist.resize(160,50)
        self.funclist2.setMaximumWidth(160)
        self.funclist2.resize(160,50)
        layout_f = QtGui.QVBoxLayout()
        layout_f.addWidget(QtGui.QLabel("Available Regexp\nFunctions"))
        layout_f.addWidget(self.funclist)
        layout_f.addWidget(self.reloadQuirkFuncButton)
        layout_g = QtGui.QVBoxLayout()
        layout_g.addWidget(QtGui.QLabel("Available Regexp\nFunctions"))
        layout_g.addWidget(self.funclist2)
        layout_g.addWidget(self.reloadQuirkFuncButton2)

        # Pages
        # Type select
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_select = QtGui.QVBoxLayout(widget)
        layout_select.setAlignment(QtCore.Qt.AlignTop)
        self.radios = []
        self.radios.append(QtGui.QRadioButton("Prefix", self))
        self.radios.append(QtGui.QRadioButton("Suffix", self))
        self.radios.append(QtGui.QRadioButton("Simple Replace", self))
        self.radios.append(QtGui.QRadioButton("Regexp Replace", self))
        self.radios.append(QtGui.QRadioButton("Random Replace", self))
        self.radios.append(QtGui.QRadioButton("Mispeller", self))

        layout_select.addWidget(QtGui.QLabel("Select Quirk Type:"))
        for r in self.radios:
            layout_select.addWidget(r)

        # Prefix
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_prefix = QtGui.QVBoxLayout(widget)
        layout_prefix.setAlignment(QtCore.Qt.AlignTop)
        layout_prefix.addWidget(QtGui.QLabel("Prefix"))
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("Value:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_prefix.addLayout(layout_3)

        # Suffix
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_suffix = QtGui.QVBoxLayout(widget)
        layout_suffix.setAlignment(QtCore.Qt.AlignTop)
        layout_suffix.addWidget(QtGui.QLabel("Suffix"))
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("Value:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_suffix.addLayout(layout_3)

        # Simple Replace
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_replace = QtGui.QVBoxLayout(widget)
        layout_replace.setAlignment(QtCore.Qt.AlignTop)
        layout_replace.addWidget(QtGui.QLabel("Simple Replace"))
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("Replace:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_replace.addLayout(layout_3)
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("With:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_replace.addLayout(layout_3)

        # Regexp Replace
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_all = QtGui.QHBoxLayout(widget)
        layout_regexp = QtGui.QVBoxLayout()
        layout_regexp.setAlignment(QtCore.Qt.AlignTop)
        layout_regexp.addWidget(QtGui.QLabel("Regexp Replace"))
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("Regexp:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_regexp.addLayout(layout_3)
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(QtGui.QLabel("Replace With:"))
        layout_3.addWidget(QtGui.QLineEdit())
        layout_regexp.addLayout(layout_3)
        layout_all.addLayout(layout_f)
        layout_all.addWidget(vr)
        layout_all.addLayout(layout_regexp)

        # Random Replace
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_all = QtGui.QHBoxLayout(widget)
        layout_random = QtGui.QVBoxLayout()
        layout_random.setAlignment(QtCore.Qt.AlignTop)
        layout_random.addWidget(QtGui.QLabel("Random Replace"))
        layout_5 = QtGui.QHBoxLayout()
        regexpl = QtGui.QLabel("Regexp:", self)
        self.regexp = QtGui.QLineEdit("", self)
        layout_5.addWidget(regexpl)
        layout_5.addWidget(self.regexp)
        replacewithl = QtGui.QLabel("Replace With:", self)
        layout_all.addLayout(layout_g)
        layout_all.addWidget(vr2)
        layout_all.addLayout(layout_random)

        layout_6 = QtGui.QVBoxLayout()
        layout_7 = QtGui.QHBoxLayout()
        self.replacelist = QtGui.QListWidget(self)
        self.replaceinput = QtGui.QLineEdit(self)
        addbutton = QtGui.QPushButton("ADD", self)
        self.connect(addbutton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('addRandomString()'))
        removebutton = QtGui.QPushButton("REMOVE", self)
        self.connect(removebutton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('removeRandomString()'))
        layout_7.addWidget(addbutton)
        layout_7.addWidget(removebutton)
        layout_6.addLayout(layout_5)
        layout_6.addWidget(replacewithl)
        layout_6.addWidget(self.replacelist)
        layout_6.addWidget(self.replaceinput)
        layout_6.addLayout(layout_7)
        layout_random.addLayout(layout_6)

        # Misspeller
        widget = QtGui.QWidget()
        self.pages.addWidget(widget)
        layout_mispeller = QtGui.QVBoxLayout(widget)
        layout_mispeller.setAlignment(QtCore.Qt.AlignTop)
        layout_mispeller.addWidget(QtGui.QLabel("Mispeller"))
        layout_1 = QtGui.QHBoxLayout()
        zero = QtGui.QLabel("1%", self)
        hund = QtGui.QLabel("100%", self)
        self.current = QtGui.QLabel("50%", self)
        self.current.setAlignment(QtCore.Qt.AlignHCenter)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                     self, QtCore.SLOT('printValue(int)'))
        layout_1.addWidget(zero)
        layout_1.addWidget(self.slider)
        layout_1.addWidget(hund)
        layout_mispeller.addLayout(layout_1)
        layout_mispeller.addWidget(self.current)

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.pages)
        layout_0.addLayout(layout_2)

        if quirk:
            types = ["prefix","suffix","replace","regexp","random","spelling"]
            for (i,r) in enumerate(self.radios):
                if i == types.index(quirk.quirk.type):
                    r.setChecked(True)
            self.changePage(types.index(quirk.quirk.type)+1)
            page = self.pages.currentWidget().layout()
            q = quirk.quirk.quirk
            if q["type"] in ("prefix","suffix"):
                page.itemAt(1).layout().itemAt(1).widget().setText(q["value"])
            elif q["type"] == "replace":
                page.itemAt(1).layout().itemAt(1).widget().setText(q["from"])
                page.itemAt(2).layout().itemAt(1).widget().setText(q["to"])
            elif q["type"] == "regexp":
                page.itemAt(2).layout().itemAt(1).layout().itemAt(1).widget().setText(q["from"])
                page.itemAt(2).layout().itemAt(2).layout().itemAt(1).widget().setText(q["to"])
            elif q["type"] == "random":
                self.regexp.setText(q["from"])
                for v in q["randomlist"]:
                    item = QtGui.QListWidgetItem(v, self.replacelist)
            elif q["type"] == "spelling":
                self.slider.setValue(q["percentage"])

        self.setLayout(layout_0)

    def closeEvent(self, event):
        self.parent().quirkadd = None

    def changePage(self, page):
        c = self.pages.count()
        if page >= c or page < 0: return
        self.back.setEnabled(page > 0)
        if page >= 1 and page <= 6:
            self.next.setText("Finish")
        else:
            self.next.setText("Next")
        self.pages.setCurrentIndex(page)
    @QtCore.pyqtSlot()
    def nextPage(self):
        if self.next.text() == "Finish":
            self.accept()
            return
        cur = self.pages.currentIndex()
        if cur == 0:
            for (i,r) in enumerate(self.radios):
                if r.isChecked():
                    self.changePage(i+1)
        else:
            self.changePage(cur+1)
    @QtCore.pyqtSlot()
    def backPage(self):
        cur = self.pages.currentIndex()
        if cur >= 1 and cur <= 6:
            self.changePage(0)

    @QtCore.pyqtSlot(int)
    def printValue(self, value):
        self.current.setText(str(value)+"%")
    @QtCore.pyqtSlot()
    def addRandomString(self):
        text = unicode(self.replaceinput.text())
        item = QtGui.QListWidgetItem(text, self.replacelist)
        self.replaceinput.setText("")
        self.replaceinput.setFocus()
    @QtCore.pyqtSlot()
    def removeRandomString(self):
        if not self.replacelist.currentItem():
            return
        else:
            self.replacelist.takeItem(self.replacelist.currentRow())
        self.replaceinput.setFocus()

    @QtCore.pyqtSlot()
    def reloadQuirkFuncSlot(self):
        from parsetools import reloadQuirkFunctions, quirkloader
        reloadQuirkFunctions()
        funcs = [q+"()" for q in quirkloader.quirks.keys()]
        funcs.sort()
        self.funclist.clear()
        self.funclist.addItems(funcs)
        self.funclist2.clear()
        self.funclist2.addItems(funcs)

class PesterChooseQuirks(QtGui.QDialog):
    def __init__(self, config, theme, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Set Quirks")

        self.quirkList = PesterQuirkList(self.mainwindow, self)

        self.addQuirkButton = QtGui.QPushButton("ADD QUIRK", self)
        self.connect(self.addQuirkButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('addQuirkDialog()'))

        self.upShiftButton = QtGui.QPushButton("^", self)
        self.downShiftButton = QtGui.QPushButton("v", self)
        self.upShiftButton.setToolTip("Move quirk up one")
        self.downShiftButton.setToolTip("Move quirk down one")
        self.connect(self.upShiftButton, QtCore.SIGNAL('clicked()'),
                     self.quirkList, QtCore.SLOT('upShiftQuirk()'))
        self.connect(self.downShiftButton, QtCore.SIGNAL('clicked()'),
                    self.quirkList, QtCore.SLOT('downShiftQuirk()'))

        self.newGroupButton = QtGui.QPushButton("*", self)
        self.newGroupButton.setToolTip("New Quirk Group")
        self.connect(self.newGroupButton, QtCore.SIGNAL('clicked()'),
                     self.quirkList, QtCore.SLOT('addQuirkGroup()'))

        layout_quirklist = QtGui.QHBoxLayout() #the nude layout quirklist
        layout_shiftbuttons = QtGui.QVBoxLayout() #the shift button layout
        layout_shiftbuttons.addWidget(self.upShiftButton)
        layout_shiftbuttons.addWidget(self.newGroupButton)
        layout_shiftbuttons.addWidget(self.downShiftButton)
        layout_quirklist.addWidget(self.quirkList)
        layout_quirklist.addLayout(layout_shiftbuttons)

        layout_1 = QtGui.QHBoxLayout()
        layout_1.addWidget(self.addQuirkButton)

        self.editSelectedButton = QtGui.QPushButton("EDIT", self)
        self.connect(self.editSelectedButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('editSelected()'))
        self.removeSelectedButton = QtGui.QPushButton("REMOVE", self)
        self.connect(self.removeSelectedButton, QtCore.SIGNAL('clicked()'),
                     self.quirkList, QtCore.SLOT('removeCurrent()'))
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(self.editSelectedButton)
        layout_3.addWidget(self.removeSelectedButton)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.test = QtGui.QPushButton("TEST QUIRKS", self)
        self.connect(self.test, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('testQuirks()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_ok = QtGui.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.test)
        layout_ok.addWidget(self.ok)

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addLayout(layout_quirklist)
        layout_0.addLayout(layout_1)
        #layout_0.addLayout(layout_2)
        layout_0.addLayout(layout_3)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)

    def quirks(self):
        u = []
        for i in range(self.quirkList.topLevelItemCount()):
            for j in range(self.quirkList.topLevelItem(i).childCount()):
                u.append(self.quirkList.topLevelItem(i).child(j).quirk)
        return u
        #return [self.quirkList.item(i).quirk for i in range(self.quirkList.count())]
    def testquirks(self):
        u = []
        for i in range(self.quirkList.topLevelItemCount()):
            for j in range(self.quirkList.topLevelItem(i).childCount()):
                item = self.quirkList.topLevelItem(i).child(j)
                if (item.checkState(0) == QtCore.Qt.Checked):
                    u.append(item.quirk)
        return u

    @QtCore.pyqtSlot()
    def testQuirks(self):
        if not hasattr(self, 'quirktester'):
            self.quirktester = None
        if self.quirktester:
            return
        self.quirktester = QuirkTesterWindow(self)
        self.quirktester.show()

    @QtCore.pyqtSlot()
    def editSelected(self):
        q = self.quirkList.currentQuirk()
        if not q: return
        quirk = q.quirk
        self.addQuirkDialog(q)

    @QtCore.pyqtSlot()
    def addQuirkDialog(self, quirk=None):
        if not hasattr(self, 'quirkadd'):
            self.quirkadd = None
        if self.quirkadd:
            return
        self.quirkadd = PesterQuirkTypes(self, quirk)
        self.connect(self.quirkadd, QtCore.SIGNAL('accepted()'),
                     self, QtCore.SLOT('addQuirk()'))
        self.connect(self.quirkadd, QtCore.SIGNAL('rejected()'),
                     self, QtCore.SLOT('closeQuirk()'))
        self.quirkadd.show()
    @QtCore.pyqtSlot()
    def addQuirk(self):
        types = ["prefix","suffix","replace","regexp","random","spelling"]
        vdict = {}
        vdict["type"] = types[self.quirkadd.pages.currentIndex()-1]
        page = self.quirkadd.pages.currentWidget().layout()
        if vdict["type"] in ("prefix","suffix"):
            vdict["value"] = unicode(page.itemAt(1).layout().itemAt(1).widget().text())
        elif vdict["type"] == "replace":
            vdict["from"] = unicode(page.itemAt(1).layout().itemAt(1).widget().text())
            vdict["to"] = unicode(page.itemAt(2).layout().itemAt(1).widget().text())
        elif vdict["type"] == "regexp":
            vdict["from"] = unicode(page.itemAt(2).layout().itemAt(1).layout().itemAt(1).widget().text())
            vdict["to"] = unicode(page.itemAt(2).layout().itemAt(2).layout().itemAt(1).widget().text())
        elif vdict["type"] == "random":
            vdict["from"] = unicode(self.quirkadd.regexp.text())
            randomlist = [unicode(self.quirkadd.replacelist.item(i).text())
                          for i in range(0,self.quirkadd.replacelist.count())]
            vdict["randomlist"] = randomlist
        elif vdict["type"] == "spelling":
            vdict["percentage"] = self.quirkadd.slider.value()

        if vdict["type"] in ("regexp", "random"):
            try:
                re.compile(vdict["from"])
            except re.error, e:
                quirkWarning = QtGui.QMessageBox(self)
                quirkWarning.setText("Not a valid regular expression!")
                quirkWarning.setInformativeText("H3R3S WHY DUMP4SS: %s" % (e))
                quirkWarning.exec_()
                self.quirkadd = None
                return

        quirk = pesterQuirk(vdict)
        if self.quirkadd.quirk is None:
            item = PesterQuirkItem(quirk)
            self.quirkList.addItem(item)
        else:
            self.quirkadd.quirk.update(quirk)
        self.quirkadd = None
    @QtCore.pyqtSlot()
    def closeQuirk(self):
        self.quirkadd = None

class PesterChooseTheme(QtGui.QDialog):
    def __init__(self, config, theme, parent):
        QtGui.QDialog.__init__(self, parent)
        self.config = config
        self.theme = theme
        self.parent = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pick a theme")

        instructions = QtGui.QLabel("Pick a theme:")

        avail_themes = config.availableThemes()
        self.themeBox = QtGui.QComboBox(self)
        for (i, t) in enumerate(avail_themes):
            self.themeBox.addItem(t)
            if t == theme.name:
                self.themeBox.setCurrentIndex(i)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_ok = QtGui.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(instructions)
        layout_0.addWidget(self.themeBox)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)

        self.connect(self, QtCore.SIGNAL('accepted()'),
                     parent, QtCore.SLOT('themeSelected()'))
        self.connect(self, QtCore.SIGNAL('rejected()'),
                     parent, QtCore.SLOT('closeTheme()'))

class PesterChooseProfile(QtGui.QDialog):
    def __init__(self, userprofile, config, theme, parent, collision=None):
        QtGui.QDialog.__init__(self, parent)
        self.userprofile = userprofile
        self.theme = theme
        self.config = config
        self.parent = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        self.currentHandle = QtGui.QLabel("CHANGING FROM %s" % userprofile.chat.handle)
        self.chumHandle = QtGui.QLineEdit(self)
        self.chumHandle.setMinimumWidth(200)
        self.chumHandleLabel = QtGui.QLabel(self.theme["main/mychumhandle/label/text"], self)
        self.chumColorButton = QtGui.QPushButton(self)
        self.chumColorButton.resize(50, 20)
        self.chumColorButton.setStyleSheet("background: %s" % (userprofile.chat.colorhtml()))
        self.chumcolor = userprofile.chat.color
        self.connect(self.chumColorButton, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('openColorDialog()'))
        layout_1 = QtGui.QHBoxLayout()
        layout_1.addWidget(self.chumHandleLabel)
        layout_1.addWidget(self.chumHandle)
        layout_1.addWidget(self.chumColorButton)

        # available profiles?
        avail_profiles = self.config.availableProfiles()
        if avail_profiles:
            self.profileBox = QtGui.QComboBox(self)
            self.profileBox.addItem("Choose a profile...")
            for p in avail_profiles:
                self.profileBox.addItem(p.chat.handle)
        else:
            self.profileBox = None

        self.defaultcheck = QtGui.QCheckBox(self)
        self.defaultlabel = QtGui.QLabel("Set This Profile As Default", self)
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.defaultlabel)
        layout_2.addWidget(self.defaultcheck)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('validateProfile()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        if not collision and avail_profiles:
            self.delete = QtGui.QPushButton("DELETE", self)
            self.connect(self.delete, QtCore.SIGNAL('clicked()'),
                         self, QtCore.SLOT('deleteProfile()'))
        layout_ok = QtGui.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtGui.QVBoxLayout()
        if collision:
            collision_warning = QtGui.QLabel("%s is taken already! Pick a new profile." % (collision))
            layout_0.addWidget(collision_warning)
        else:
            layout_0.addWidget(self.currentHandle, alignment=QtCore.Qt.AlignHCenter)
        layout_0.addLayout(layout_1)
        if avail_profiles:
            profileLabel = QtGui.QLabel("Or choose an existing profile:", self)
            layout_0.addWidget(profileLabel)
            layout_0.addWidget(self.profileBox)
        layout_0.addLayout(layout_ok)
        if not collision and avail_profiles:
            layout_0.addWidget(self.delete)
        layout_0.addLayout(layout_2)
        self.errorMsg = QtGui.QLabel(self)
        self.errorMsg.setStyleSheet("color:red;")
        layout_0.addWidget(self.errorMsg)
        self.setLayout(layout_0)

        self.connect(self, QtCore.SIGNAL('accepted()'),
                     parent, QtCore.SLOT('profileSelected()'))
        self.connect(self, QtCore.SIGNAL('rejected()'),
                     parent, QtCore.SLOT('closeProfile()'))

    @QtCore.pyqtSlot()
    def openColorDialog(self):
        self.colorDialog = QtGui.QColorDialog(self)
        color = self.colorDialog.getColor(initial=self.userprofile.chat.color)
        self.chumColorButton.setStyleSheet("background: %s" % color.name())
        self.chumcolor = color
        self.colorDialog = None

    @QtCore.pyqtSlot()
    def validateProfile(self):
        if not self.profileBox or self.profileBox.currentIndex() == 0:
            handle = unicode(self.chumHandle.text())
            if not PesterProfile.checkLength(handle):
                self.errorMsg.setText("PROFILE HANDLE IS TOO LONG")
                return
            if not PesterProfile.checkValid(handle)[0]:
                self.errorMsg.setText("NOT A VALID CHUMTAG. REASON:\n%s" % (PesterProfile.checkValid(handle)[1]))
                return
        self.accept()

    @QtCore.pyqtSlot()
    def deleteProfile(self):
        if self.profileBox and self.profileBox.currentIndex() > 0:
            handle = unicode(self.profileBox.currentText())
            if handle == self.parent.profile().handle:
                problem = QtGui.QMessageBox()
                problem.setStyleSheet(self.theme["main/defaultwindow/style"])
                problem.setWindowTitle("Problem!")
                problem.setInformativeText("You can't delete the profile you're currently using!")
                problem.setStandardButtons(QtGui.QMessageBox.Ok)
                problem.exec_()
                return
            msgbox = QtGui.QMessageBox()
            msgbox.setStyleSheet(self.theme["main/defaultwindow/style"])
            msgbox.setWindowTitle("WARNING!")
            msgbox.setInformativeText("Are you sure you want to delete the profile: %s" % (handle))
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            ret = msgbox.exec_()
            if ret == QtGui.QMessageBox.Ok:
                try:
                    remove(_datadir+"profiles/%s.js" % (handle))
                except OSError:
                    problem = QtGui.QMessageBox()
                    problem.setStyleSheet(self.theme["main/defaultwindow/style"])
                    problem.setWindowTitle("Problem!")
                    problem.setInformativeText("There was a problem deleting the profile: %s" % (handle))
                    problem.setStandardButtons(QtGui.QMessageBox.Ok)
                    problem.exec_()

class PesterMentions(QtGui.QDialog):
    def __init__(self, window, theme, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Mentions")
        self.setModal(True)
        self.mainwindow = window
        self.theme = theme
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        self.mentionlist = QtGui.QListWidget(self)
        self.mentionlist.addItems(self.mainwindow.userprofile.getMentions())

        self.addBtn = QtGui.QPushButton("ADD MENTION", self)
        self.connect(self.addBtn, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('addMention()'))

        self.editBtn = QtGui.QPushButton("EDIT", self)
        self.connect(self.editBtn, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('editSelected()'))
        self.rmBtn = QtGui.QPushButton("REMOVE", self)
        self.connect(self.rmBtn, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('removeCurrent()'))
        layout_1 = QtGui.QHBoxLayout()
        layout_1.addWidget(self.editBtn)
        layout_1.addWidget(self.rmBtn)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.mentionlist)
        layout_0.addWidget(self.addBtn)
        layout_0.addLayout(layout_1)
        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)

    @QtCore.pyqtSlot()
    def editSelected(self):
        m = self.mentionlist.currentItem()
        if not m:
            return
        self.addMention(m)

    @QtCore.pyqtSlot()
    def addMention(self, mitem=None):
        d = {"label": "Mention:", "inputname": "value" }
        if mitem is not None:
            d["value"] = str(mitem.text())
        pdict = MultiTextDialog("ENTER MENTION", self, d).getText()
        if pdict is None:
            return
        try:
            re.compile(pdict["value"])
        except re.error, e:
            quirkWarning = QtGui.QMessageBox(self)
            quirkWarning.setText("Not a valid regular expression!")
            quirkWarning.setInformativeText("H3R3S WHY DUMP4SS: %s" % (e))
            quirkWarning.exec_()
        else:
            if mitem is None:
                self.mentionlist.addItem(pdict["value"])
            else:
                mitem.setText(pdict["value"])

    @QtCore.pyqtSlot()
    def removeCurrent(self):
        i = self.mentionlist.currentRow()
        if i >= 0:
            self.mentionlist.takeItem(i)

class PesterOptions(QtGui.QDialog):
    def __init__(self, config, theme, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Options")
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        layout_4 = QtGui.QVBoxLayout()

        hr = QtGui.QFrame()
        hr.setFrameShape(QtGui.QFrame.HLine)
        hr.setFrameShadow(QtGui.QFrame.Sunken)
        vr = QtGui.QFrame()
        vr.setFrameShape(QtGui.QFrame.VLine)
        vr.setFrameShadow(QtGui.QFrame.Sunken)

        self.tabs = QtGui.QButtonGroup(self)
        self.connect(self.tabs, QtCore.SIGNAL('buttonClicked(int)'),
                     self, QtCore.SLOT('changePage(int)'))
        tabNames = ["Chum List", "Conversations", "Interface", "Sound", "Notifications", "Logging", "Idle/Updates", "Theme", "Connection"]
        if parent.advanced: tabNames.append("Advanced")
        for t in tabNames:
            button = QtGui.QPushButton(t)
            self.tabs.addButton(button)
            layout_4.addWidget(button)
            button.setCheckable(True)
        self.tabs.button(-2).setChecked(True)
        self.pages = QtGui.QStackedWidget(self)

        self.bandwidthcheck = QtGui.QCheckBox("Low Bandwidth", self)
        if self.config.lowBandwidth():
            self.bandwidthcheck.setChecked(True)
        bandwidthLabel = QtGui.QLabel("(Stops you for receiving the flood of MOODS,\n"
                                      " though stops chumlist from working properly)")
        font = bandwidthLabel.font()
        font.setPointSize(8)
        bandwidthLabel.setFont(font)

        self.autonickserv = QtGui.QCheckBox("Auto-Identify with NickServ", self)
        self.autonickserv.setChecked(parent.userprofile.getAutoIdentify())
        self.connect(self.autonickserv, QtCore.SIGNAL('stateChanged(int)'),
                     self, QtCore.SLOT('autoNickServChange(int)'))
        self.nickservpass = QtGui.QLineEdit(self)
        self.nickservpass.setPlaceholderText("NickServ Password")
        self.nickservpass.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.nickservpass.setText(parent.userprofile.getNickServPass())

        self.autojoinlist = QtGui.QListWidget(self)
        self.autojoinlist.addItems(parent.userprofile.getAutoJoins())
        self.addAutoJoinBtn = QtGui.QPushButton("Add", self)
        self.connect(self.addAutoJoinBtn, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('addAutoJoin()'))
        self.delAutoJoinBtn = QtGui.QPushButton("Remove", self)
        self.connect(self.delAutoJoinBtn, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('delAutoJoin()'))

        self.tabcheck = QtGui.QCheckBox("Tabbed Conversations", self)
        if self.config.tabs():
            self.tabcheck.setChecked(True)
        self.tabmemocheck = QtGui.QCheckBox("Tabbed Memos", self)
        if self.config.tabMemos():
            self.tabmemocheck.setChecked(True)
        self.hideOffline = QtGui.QCheckBox("Hide Offline Chums", self)
        if self.config.hideOfflineChums():
            self.hideOffline.setChecked(True)

        self.soundcheck = QtGui.QCheckBox("Sounds On", self)
        self.connect(self.soundcheck, QtCore.SIGNAL('stateChanged(int)'),
                     self, QtCore.SLOT('soundChange(int)'))
        self.chatsoundcheck = QtGui.QCheckBox("Pester Sounds", self)
        self.chatsoundcheck.setChecked(self.config.chatSound())
        self.memosoundcheck = QtGui.QCheckBox("Memo Sounds", self)
        self.memosoundcheck.setChecked(self.config.memoSound())
        self.connect(self.memosoundcheck, QtCore.SIGNAL('stateChanged(int)'),
                     self, QtCore.SLOT('memoSoundChange(int)'))
        self.memopingcheck = QtGui.QCheckBox("Memo Ping", self)
        self.memopingcheck.setChecked(self.config.memoPing())
        self.namesoundcheck = QtGui.QCheckBox("Memo Mention (initials)", self)
        self.namesoundcheck.setChecked(self.config.nameSound())
        if self.config.soundOn():
            self.soundcheck.setChecked(True)
            if not self.memosoundcheck.isChecked():
                self.memoSoundChange(0)
        else:
            self.chatsoundcheck.setEnabled(False)
            self.memosoundcheck.setEnabled(False)
            self.memoSoundChange(0)

        self.editMentions = QtGui.QPushButton("Edit Mentions", self)
        self.connect(self.editMentions, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('openMentions()'))
        self.editMentions2 = QtGui.QPushButton("Edit Mentions", self)
        self.connect(self.editMentions2, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('openMentions()'))

        self.volume = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(self.config.volume())
        self.connect(self.volume, QtCore.SIGNAL('valueChanged(int)'),
                     self, QtCore.SLOT('printValue(int)'))
        self.currentVol = QtGui.QLabel(str(self.config.volume())+"%", self)
        self.currentVol.setAlignment(QtCore.Qt.AlignHCenter)


        self.timestampcheck = QtGui.QCheckBox("Time Stamps", self)
        if self.config.showTimeStamps():
            self.timestampcheck.setChecked(True)

        self.timestampBox = QtGui.QComboBox(self)
        self.timestampBox.addItem("12 hour")
        self.timestampBox.addItem("24 hour")
        if self.config.time12Format():
            self.timestampBox.setCurrentIndex(0)
        else:
            self.timestampBox.setCurrentIndex(1)
        self.secondscheck = QtGui.QCheckBox("Show Seconds", self)
        if self.config.showSeconds():
            self.secondscheck.setChecked(True)

        self.memomessagecheck = QtGui.QCheckBox("Show OP and Voice Messages in Memos", self)
        if self.config.opvoiceMessages():
            self.memomessagecheck.setChecked(True)

        if not ostools.isOSXBundle():
            self.animationscheck = QtGui.QCheckBox("Use animated smilies", self)
            if self.config.animations():
                self.animationscheck.setChecked(True)
            animateLabel = QtGui.QLabel("(Disable if you leave chats open for LOOOONG periods of time)")
            font = animateLabel.font()
            font.setPointSize(8)
            animateLabel.setFont(font)

        self.userlinkscheck = QtGui.QCheckBox("Disable #Memo and @User Links", self)
        self.userlinkscheck.setChecked(self.config.disableUserLinks())
        self.userlinkscheck.setVisible(False)


        # Will add ability to turn off groups later
        #self.groupscheck = QtGui.QCheckBox("Use Groups", self)
        #self.groupscheck.setChecked(self.config.useGroups())
        self.showemptycheck = QtGui.QCheckBox("Show Empty Groups", self)
        self.showemptycheck.setChecked(self.config.showEmptyGroups())
        self.showonlinenumbers = QtGui.QCheckBox("Show Number of Online Chums", self)
        self.showonlinenumbers.setChecked(self.config.showOnlineNumbers())

        sortLabel = QtGui.QLabel("Sort Chums")
        self.sortBox = QtGui.QComboBox(self)
        self.sortBox.addItem("Alphabetically")
        self.sortBox.addItem("By Mood")
        self.sortBox.addItem("Manually")
        method = self.config.sortMethod()
        if method >= 0 and method < self.sortBox.count():
            self.sortBox.setCurrentIndex(method)
        layout_3 = QtGui.QHBoxLayout()
        layout_3.addWidget(sortLabel)
        layout_3.addWidget(self.sortBox, 10)

        self.logpesterscheck = QtGui.QCheckBox("Log all Pesters", self)
        if self.config.logPesters() & self.config.LOG:
            self.logpesterscheck.setChecked(True)
        self.logmemoscheck = QtGui.QCheckBox("Log all Memos", self)
        if self.config.logMemos() & self.config.LOG:
            self.logmemoscheck.setChecked(True)
        self.stamppestercheck = QtGui.QCheckBox("Log Time Stamps for Pesters", self)
        if self.config.logPesters() & self.config.STAMP:
            self.stamppestercheck.setChecked(True)
        self.stampmemocheck = QtGui.QCheckBox("Log Time Stamps for Memos", self)
        if self.config.logMemos() & self.config.STAMP:
            self.stampmemocheck.setChecked(True)

        self.idleBox = QtGui.QSpinBox(self)
        self.idleBox.setStyleSheet("background:#FFFFFF")
        self.idleBox.setRange(1, 1440)
        self.idleBox.setValue(self.config.idleTime())
        layout_5 = QtGui.QHBoxLayout()
        layout_5.addWidget(QtGui.QLabel("Minutes before Idle:"))
        layout_5.addWidget(self.idleBox)

        self.updateBox = QtGui.QComboBox(self)
        self.updateBox.addItem("Once a Day")
        self.updateBox.addItem("Once a Week")
        self.updateBox.addItem("Only on Start")
        self.updateBox.addItem("Never")
        check = self.config.checkForUpdates()
        if check >= 0 and check < self.updateBox.count():
            self.updateBox.setCurrentIndex(check)
        layout_6 = QtGui.QHBoxLayout()
        layout_6.addWidget(QtGui.QLabel("Check for\nPesterchum Updates:"))
        layout_6.addWidget(self.updateBox)

        if not ostools.isOSXLeopard():
            self.mspaCheck = QtGui.QCheckBox("Check for MSPA Updates", self)
            self.mspaCheck.setChecked(self.config.checkMSPA())

        self.randomscheck = QtGui.QCheckBox("Receive Random Encounters")
        self.randomscheck.setChecked(parent.userprofile.randoms)
        if not parent.randhandler.running:
            self.randomscheck.setEnabled(False)

        avail_themes = self.config.availableThemes()
        self.themeBox = QtGui.QComboBox(self)
        notheme = (theme.name not in avail_themes)
        for (i, t) in enumerate(avail_themes):
            self.themeBox.addItem(t)
            if (not notheme and t == theme.name) or (notheme and t == "pesterchum"):
                self.themeBox.setCurrentIndex(i)
        self.refreshtheme = QtGui.QPushButton("Refresh current theme", self)
        self.connect(self.refreshtheme, QtCore.SIGNAL('clicked()'),
                     parent, QtCore.SLOT('themeSelectOverride()'))
        self.ghostchum = QtGui.QCheckBox("Pesterdunk Ghostchum!!", self)
        self.ghostchum.setChecked(self.config.ghostchum())

        self.buttonOptions = ["Minimize to Taskbar", "Minimize to Tray", "Quit"]
        self.miniBox = QtGui.QComboBox(self)
        self.miniBox.addItems(self.buttonOptions)
        self.miniBox.setCurrentIndex(self.config.minimizeAction())
        self.closeBox = QtGui.QComboBox(self)
        self.closeBox.addItems(self.buttonOptions)
        self.closeBox.setCurrentIndex(self.config.closeAction())
        layout_mini = QtGui.QHBoxLayout()
        layout_mini.addWidget(QtGui.QLabel("Minimize"))
        layout_mini.addWidget(self.miniBox)
        layout_close = QtGui.QHBoxLayout()
        layout_close.addWidget(QtGui.QLabel("Close"))
        layout_close.addWidget(self.closeBox)

        self.pesterBlink = QtGui.QCheckBox("Blink Taskbar on Pesters", self)
        if self.config.blink() & self.config.PBLINK:
            self.pesterBlink.setChecked(True)
        self.memoBlink = QtGui.QCheckBox("Blink Taskbar on Memos", self)
        if self.config.blink() & self.config.MBLINK:
            self.memoBlink.setChecked(True)

        self.notifycheck = QtGui.QCheckBox("Toast Notifications", self)
        if self.config.notify():
            self.notifycheck.setChecked(True)
        self.connect(self.notifycheck, QtCore.SIGNAL('stateChanged(int)'),
                     self, QtCore.SLOT('notifyChange(int)'))
        self.notifyOptions = QtGui.QComboBox(self)
        types = self.parent().tm.availableTypes()
        cur = self.parent().tm.currentType()
        self.notifyOptions.addItems(types)
        for (i,t) in enumerate(types):
            if t == cur:
                self.notifyOptions.setCurrentIndex(i)
                break
        self.notifyTypeLabel = QtGui.QLabel("Type", self)
        layout_type = QtGui.QHBoxLayout()
        layout_type.addWidget(self.notifyTypeLabel)
        layout_type.addWidget(self.notifyOptions)
        self.notifySigninCheck   = QtGui.QCheckBox("Chum signs in", self)
        if self.config.notifyOptions() & self.config.SIGNIN:
            self.notifySigninCheck.setChecked(True)
        self.notifySignoutCheck  = QtGui.QCheckBox("Chum signs out", self)
        if self.config.notifyOptions() & self.config.SIGNOUT:
            self.notifySignoutCheck.setChecked(True)
        self.notifyNewMsgCheck   = QtGui.QCheckBox("New messages", self)
        if self.config.notifyOptions() & self.config.NEWMSG:
            self.notifyNewMsgCheck.setChecked(True)
        self.notifyNewConvoCheck = QtGui.QCheckBox("Only new conversations", self)
        if self.config.notifyOptions() & self.config.NEWCONVO:
            self.notifyNewConvoCheck.setChecked(True)
        self.notifyMentionsCheck = QtGui.QCheckBox("Memo Mentions (initials)", self)
        if self.config.notifyOptions() & self.config.INITIALS:
            self.notifyMentionsCheck.setChecked(True)
        self.notifyChange(self.notifycheck.checkState())

        if parent.advanced:
            self.modechange = QtGui.QLineEdit(self)
            layout_change = QtGui.QHBoxLayout()
            layout_change.addWidget(QtGui.QLabel("Change:"))
            layout_change.addWidget(self.modechange)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        # Tab layouts
        # Chum List
        widget = QtGui.QWidget()
        layout_chumlist = QtGui.QVBoxLayout(widget)
        layout_chumlist.setAlignment(QtCore.Qt.AlignTop)
        layout_chumlist.addWidget(self.hideOffline)
        #layout_chumlist.addWidget(self.groupscheck)
        layout_chumlist.addWidget(self.showemptycheck)
        layout_chumlist.addWidget(self.showonlinenumbers)
        layout_chumlist.addLayout(layout_3)
        self.pages.addWidget(widget)

        # Conversations
        widget = QtGui.QWidget()
        layout_chat = QtGui.QVBoxLayout(widget)
        layout_chat.setAlignment(QtCore.Qt.AlignTop)
        layout_chat.addWidget(self.timestampcheck)
        layout_chat.addWidget(self.timestampBox)
        layout_chat.addWidget(self.secondscheck)
        layout_chat.addWidget(self.memomessagecheck)
        if not ostools.isOSXBundle():
            layout_chat.addWidget(self.animationscheck)
            layout_chat.addWidget(animateLabel)
        layout_chat.addWidget(self.randomscheck)
        # Re-enable these when it's possible to disable User and Memo links
        #layout_chat.addWidget(hr)
        #layout_chat.addWidget(QtGui.QLabel("User and Memo Links"))
        #layout_chat.addWidget(self.userlinkscheck)
        self.pages.addWidget(widget)

        # Interface
        widget = QtGui.QWidget()
        layout_interface = QtGui.QVBoxLayout(widget)
        layout_interface.setAlignment(QtCore.Qt.AlignTop)
        layout_interface.addWidget(self.tabcheck)
        layout_interface.addWidget(self.tabmemocheck)
        layout_interface.addLayout(layout_mini)
        layout_interface.addLayout(layout_close)
        layout_interface.addWidget(self.pesterBlink)
        layout_interface.addWidget(self.memoBlink)
        self.pages.addWidget(widget)

        # Sound
        widget = QtGui.QWidget()
        layout_sound = QtGui.QVBoxLayout(widget)
        layout_sound.setAlignment(QtCore.Qt.AlignTop)
        layout_sound.addWidget(self.soundcheck)
        layout_indent = QtGui.QVBoxLayout()
        layout_indent.addWidget(self.chatsoundcheck)
        layout_indent.addWidget(self.memosoundcheck)
        layout_doubleindent = QtGui.QVBoxLayout()
        layout_doubleindent.addWidget(self.memopingcheck)
        layout_doubleindent.addWidget(self.namesoundcheck)
        layout_doubleindent.addWidget(self.editMentions)
        layout_doubleindent.setContentsMargins(22,0,0,0)
        layout_indent.addLayout(layout_doubleindent)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_sound.addLayout(layout_indent)
        layout_sound.addSpacing(15)
        layout_sound.addWidget(QtGui.QLabel("Master Volume:", self))
        layout_sound.addWidget(self.volume)
        layout_sound.addWidget(self.currentVol)
        self.pages.addWidget(widget)

        # Notifications
        widget = QtGui.QWidget()
        layout_notify = QtGui.QVBoxLayout(widget)
        layout_notify.setAlignment(QtCore.Qt.AlignTop)
        layout_notify.addWidget(self.notifycheck)
        layout_indent = QtGui.QVBoxLayout()
        layout_indent.addLayout(layout_type)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_indent.addWidget(self.notifySigninCheck)
        layout_indent.addWidget(self.notifySignoutCheck)
        layout_indent.addWidget(self.notifyNewMsgCheck)
        layout_doubleindent = QtGui.QVBoxLayout()
        layout_doubleindent.addWidget(self.notifyNewConvoCheck)
        layout_doubleindent.setContentsMargins(22,0,0,0)
        layout_indent.addLayout(layout_doubleindent)
        layout_indent.addWidget(self.notifyMentionsCheck)
        layout_indent.addWidget(self.editMentions2)
        layout_notify.addLayout(layout_indent)
        self.pages.addWidget(widget)

        # Logging
        widget = QtGui.QWidget()
        layout_logs = QtGui.QVBoxLayout(widget)
        layout_logs.setAlignment(QtCore.Qt.AlignTop)
        layout_logs.addWidget(self.logpesterscheck)
        layout_logs.addWidget(self.logmemoscheck)
        layout_logs.addWidget(self.stamppestercheck)
        layout_logs.addWidget(self.stampmemocheck)
        self.pages.addWidget(widget)

        # Idle/Updates
        widget = QtGui.QWidget()
        layout_idle = QtGui.QVBoxLayout(widget)
        layout_idle.setAlignment(QtCore.Qt.AlignTop)
        layout_idle.addLayout(layout_5)
        layout_idle.addLayout(layout_6)
        if not ostools.isOSXLeopard():
            layout_idle.addWidget(self.mspaCheck)
        self.pages.addWidget(widget)

        # Theme
        widget = QtGui.QWidget()
        layout_theme = QtGui.QVBoxLayout(widget)
        layout_theme.setAlignment(QtCore.Qt.AlignTop)
        layout_theme.addWidget(QtGui.QLabel("Pick a Theme:"))
        layout_theme.addWidget(self.themeBox)
        layout_theme.addWidget(self.refreshtheme)
        layout_theme.addWidget(self.ghostchum)
        self.pages.addWidget(widget)

        # Connection
        widget = QtGui.QWidget()
        layout_connect = QtGui.QVBoxLayout(widget)
        layout_connect.setAlignment(QtCore.Qt.AlignTop)
        layout_connect.addWidget(self.bandwidthcheck)
        layout_connect.addWidget(bandwidthLabel)
        layout_connect.addWidget(self.autonickserv)
        layout_indent = QtGui.QVBoxLayout()
        layout_indent.addWidget(self.nickservpass)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_connect.addLayout(layout_indent)
        layout_connect.addWidget(QtGui.QLabel("Auto-Join Memos:"))
        layout_connect.addWidget(self.autojoinlist)
        layout_8 = QtGui.QHBoxLayout()
        layout_8.addWidget(self.addAutoJoinBtn)
        layout_8.addWidget(self.delAutoJoinBtn)
        layout_connect.addLayout(layout_8)
        self.pages.addWidget(widget)

        # Advanced
        if parent.advanced:
            widget = QtGui.QWidget()
            layout_advanced = QtGui.QVBoxLayout(widget)
            layout_advanced.setAlignment(QtCore.Qt.AlignTop)
            layout_advanced.addWidget(QtGui.QLabel("Current User Mode: %s" % parent.modes))
            layout_advanced.addLayout(layout_change)
            self.pages.addWidget(widget)

        layout_0 = QtGui.QVBoxLayout()
        layout_1 = QtGui.QHBoxLayout()
        layout_1.addLayout(layout_4)
        layout_1.addWidget(vr)
        layout_1.addWidget(self.pages)
        layout_0.addLayout(layout_1)
        layout_0.addSpacing(30)
        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)

    @QtCore.pyqtSlot(int)
    def changePage(self, page):
        self.tabs.button(page).setChecked(True)
        # What is this, I don't even. qt, fuck
        page = -page - 2
        self.pages.setCurrentIndex(page)

    @QtCore.pyqtSlot(int)
    def notifyChange(self, state):
        if state == 0:
            self.notifyTypeLabel.setEnabled(False)
            self.notifyOptions.setEnabled(False)
            self.notifySigninCheck.setEnabled(False)
            self.notifySignoutCheck.setEnabled(False)
            self.notifyNewMsgCheck.setEnabled(False)
            self.notifyNewConvoCheck.setEnabled(False)
            self.notifyMentionsCheck.setEnabled(False)
        else:
            self.notifyTypeLabel.setEnabled(True)
            self.notifyOptions.setEnabled(True)
            self.notifySigninCheck.setEnabled(True)
            self.notifySignoutCheck.setEnabled(True)
            self.notifyNewMsgCheck.setEnabled(True)
            self.notifyNewConvoCheck.setEnabled(True)
            self.notifyMentionsCheck.setEnabled(True)

    @QtCore.pyqtSlot(int)
    def autoNickServChange(self, state):
        self.nickservpass.setEnabled(state != 0)

    @QtCore.pyqtSlot()
    def addAutoJoin(self, mitem=None):
        d = {"label": "Memo:", "inputname": "value" }
        if mitem is not None:
            d["value"] = str(mitem.text())
        pdict = MultiTextDialog("ENTER MEMO", self, d).getText()
        if pdict is None:
            return
        pdict["value"] = "#" + pdict["value"]
        if mitem is None:
            items = self.autojoinlist.findItems(pdict["value"], QtCore.Qt.MatchFixedString)
            if len(items) == 0:
                self.autojoinlist.addItem(pdict["value"])
        else:
            mitem.setText(pdict["value"])

    @QtCore.pyqtSlot()
    def delAutoJoin(self):
        i = self.autojoinlist.currentRow()
        if i >= 0:
            self.autojoinlist.takeItem(i)

    @QtCore.pyqtSlot(int)
    def soundChange(self, state):
        if state == 0:
            self.chatsoundcheck.setEnabled(False)
            self.memosoundcheck.setEnabled(False)
            self.memoSoundChange(0)
        else:
            self.chatsoundcheck.setEnabled(True)
            self.memosoundcheck.setEnabled(True)
            if self.memosoundcheck.isChecked():
                self.memoSoundChange(1)
    @QtCore.pyqtSlot(int)
    def memoSoundChange(self, state):
        if state == 0:
            self.memopingcheck.setEnabled(False)
            self.namesoundcheck.setEnabled(False)
        else:
            self.memopingcheck.setEnabled(True)
            self.namesoundcheck.setEnabled(True)
    @QtCore.pyqtSlot(int)
    def printValue(self, v):
        self.currentVol.setText(str(v)+"%")

    @QtCore.pyqtSlot()
    def openMentions(self):
        if not hasattr(self, 'mentionmenu'):
            self.mentionmenu = None
        if not self.mentionmenu:
            self.mentionmenu = PesterMentions(self.parent(), self.theme, self)
            self.connect(self.mentionmenu, QtCore.SIGNAL('accepted()'),
                         self, QtCore.SLOT('updateMentions()'))
            self.connect(self.mentionmenu, QtCore.SIGNAL('rejected()'),
                         self, QtCore.SLOT('closeMentions()'))
            self.mentionmenu.show()
            self.mentionmenu.raise_()
            self.mentionmenu.activateWindow()
    @QtCore.pyqtSlot()
    def closeMentions(self):
        self.mentionmenu.close()
        self.mentionmenu = None
    @QtCore.pyqtSlot()
    def updateMentions(self):
        m = []
        for i in range(self.mentionmenu.mentionlist.count()):
            m.append(str(self.mentionmenu.mentionlist.item(i).text()))
        self.parent().userprofile.setMentions(m)
        self.mentionmenu = None

class PesterUserlist(QtGui.QDialog):
    def __init__(self, config, theme, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.resize(200, 600)

        self.searchbox = QtGui.QLineEdit(self)
        #self.searchbox.setStyleSheet(theme["convo/input/style"]) # which style is better?
        self.searchbox.setPlaceholderText("Search")
        self.connect(self.searchbox, QtCore.SIGNAL("textChanged(QString)"), self, QtCore.SLOT("updateUsers()"))

        self.label = QtGui.QLabel("USERLIST")
        self.userarea = RightClickList(self)
        self.userarea.setStyleSheet(self.theme["main/chums/style"])
        self.userarea.optionsMenu = QtGui.QMenu(self)

        self.addChumAction = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/addchum"], self)
        self.connect(self.addChumAction, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('addChumSlot()'))
        self.pesterChumAction = QtGui.QAction(self.mainwindow.theme["main/menus/rclickchumlist/pester"], self)
        self.connect(self.pesterChumAction, QtCore.SIGNAL('triggered()'),
                     self, QtCore.SLOT('pesterChumSlot()'))
        self.userarea.optionsMenu.addAction(self.addChumAction)
        self.userarea.optionsMenu.addAction(self.pesterChumAction)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.label)
        layout_0.addWidget(self.userarea)
        layout_0.addWidget(self.searchbox)
        layout_0.addWidget(self.ok)

        self.setLayout(layout_0)

        self.connect(self.mainwindow, QtCore.SIGNAL('namesUpdated()'),
                     self, QtCore.SLOT('updateUsers()'))

        self.connect(self.mainwindow,
                     QtCore.SIGNAL('userPresentSignal(QString, QString, QString)'),
                     self,
                     QtCore.SLOT('updateUserPresent(QString, QString, QString)'))
        self.updateUsers()

        self.searchbox.setFocus()
    @QtCore.pyqtSlot()
    def updateUsers(self):
        names = self.mainwindow.namesdb["#pesterchum"]
        self.userarea.clear()
        for n in names:
            if str(self.searchbox.text()) == "" or n.lower().find(str(self.searchbox.text()).lower()) != -1:
                item = QtGui.QListWidgetItem(n)
                item.setTextColor(QtGui.QColor(self.theme["main/chums/userlistcolor"]))
                self.userarea.addItem(item)
        self.userarea.sortItems()
    @QtCore.pyqtSlot(QtCore.QString, QtCore.QString, QtCore.QString)
    def updateUserPresent(self, handle, channel, update):
        h = unicode(handle)
        c = unicode(channel)
        if update == "quit":
            self.delUser(h)
        elif update == "left" and c == "#pesterchum":
            self.delUser(h)
        elif update == "join" and c == "#pesterchum":
            if str(self.searchbox.text()) == "" or h.lower().find(str(self.searchbox.text()).lower()) != -1:
                self.addUser(h)
    def addUser(self, name):
        item = QtGui.QListWidgetItem(name)
        item.setTextColor(QtGui.QColor(self.theme["main/chums/userlistcolor"]))
        self.userarea.addItem(item)
        self.userarea.sortItems()
    def delUser(self, name):
        matches = self.userarea.findItems(name, QtCore.Qt.MatchFlags(0))
        for m in matches:
            self.userarea.takeItem(self.userarea.row(m))

    def changeTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(theme["main/defaultwindow/style"])
        self.userarea.setStyleSheet(theme["main/chums/style"])
        self.addChumAction.setText(theme["main/menus/rclickchumlist/addchum"])
        for item in [self.userarea.item(i) for i in range(0, self.userarea.count())]:
            item.setTextColor(QtGui.QColor(theme["main/chums/userlistcolor"]))

    @QtCore.pyqtSlot()
    def addChumSlot(self):
        cur = self.userarea.currentItem()
        if not cur:
            return
        self.addChum.emit(cur.text())
    @QtCore.pyqtSlot()
    def pesterChumSlot(self):
        cur = self.userarea.currentItem()
        if not cur:
            return
        self.pesterChum.emit(cur.text())

    addChum = QtCore.pyqtSignal(QtCore.QString)
    pesterChum = QtCore.pyqtSignal(QtCore.QString)


class MemoListItem(QtGui.QTreeWidgetItem):
    def __init__(self, channel, usercount):
        QtGui.QTreeWidgetItem.__init__(self, [channel, str(usercount)])
        self.target = channel
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        if str(self.text(column)).isdigit() and str(other.text(column)).isdigit():
            return int(self.text(column)) < int(other.text(column))
        return self.text(column) < other.text(column)

class PesterMemoList(QtGui.QDialog):
    def __init__(self, parent, channel=""):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(False)
        self.theme = parent.theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.resize(460, 300)

        self.label = QtGui.QLabel("MEMOS")
        self.channelarea = RightClickTree(self)
        self.channelarea.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.channelarea.setStyleSheet(self.theme["main/chums/style"])
        self.channelarea.optionsMenu = QtGui.QMenu(self)
        self.channelarea.setColumnCount(2)
        self.channelarea.setHeaderLabels(["Memo", "Users"])
        self.channelarea.setIndentation(0)
        self.channelarea.setColumnWidth(0,200)
        self.channelarea.setColumnWidth(1,10)
        self.channelarea.setSortingEnabled(True)
        self.channelarea.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.connect(self.channelarea,
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'),
                     self, QtCore.SLOT('AcceptSelection()'))

        self.orjoinlabel = QtGui.QLabel("OR MAKE A NEW MEMO:")
        self.newmemo = QtGui.QLineEdit(channel, self)
        self.secretChannel = QtGui.QCheckBox("HIDDEN CHANNEL?", self)
        self.inviteChannel = QtGui.QCheckBox("INVITATION ONLY?", self)

        self.timelabel = QtGui.QLabel("TIMEFRAME:")
        self.timeslider = TimeSlider(QtCore.Qt.Horizontal, self)
        self.timeinput = TimeInput(self.timeslider, self)

        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        self.join = QtGui.QPushButton("JOIN", self)
        self.join.setDefault(True)
        self.connect(self.join, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('AcceptIfSelectionMade()'))
        layout_ok = QtGui.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.join)

        layout_left  = QtGui.QVBoxLayout()
        layout_right = QtGui.QVBoxLayout()
        layout_right.setAlignment(QtCore.Qt.AlignTop)
        layout_0 = QtGui.QVBoxLayout()
        layout_1 = QtGui.QHBoxLayout()
        layout_left.addWidget(self.label)
        layout_left.addWidget(self.channelarea)
        layout_right.addWidget(self.orjoinlabel)
        layout_right.addWidget(self.newmemo)
        layout_right.addWidget(self.secretChannel)
        layout_right.addWidget(self.inviteChannel)
        layout_right.addWidget(self.timelabel)
        layout_right.addWidget(self.timeslider)
        layout_right.addWidget(self.timeinput)
        layout_1.addLayout(layout_left)
        layout_1.addLayout(layout_right)
        layout_0.addLayout(layout_1)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)

    def newmemoname(self):
        return self.newmemo.text()

    def SelectedMemos(self):
        return self.channelarea.selectedItems()

    def HasSelection(self):
        return len(self.SelectedMemos()) > 0 or self.newmemoname()

    def updateChannels(self, channels):
        for c in channels:
            item = MemoListItem(c[0][1:],c[1])
            item.setTextColor(0, QtGui.QColor(self.theme["main/chums/userlistcolor"]))
            item.setTextColor(1, QtGui.QColor(self.theme["main/chums/userlistcolor"]))
            item.setIcon(0, QtGui.QIcon(self.theme["memos/memoicon"]))
            self.channelarea.addTopLevelItem(item)

    def updateTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(theme["main/defaultwindow/style"])
        for item in [self.userarea.item(i) for i in range(0, self.channelarea.count())]:
            item.setTextColor(QtGui.QColor(theme["main/chums/userlistcolor"]))
            item.setIcon(QtGui.QIcon(theme["memos/memoicon"]))

    @QtCore.pyqtSlot()
    def AcceptIfSelectionMade(self):
        if self.HasSelection():
            self.AcceptSelection()

    @QtCore.pyqtSlot()
    def AcceptSelection(self):
        self.accept()


class LoadingScreen(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent, (QtCore.Qt.CustomizeWindowHint |
                                              QtCore.Qt.FramelessWindowHint))
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])

        self.loadinglabel = QtGui.QLabel("CONN3CT1NG", self)
        self.cancel = QtGui.QPushButton("QU1T >:?", self)
        self.ok = QtGui.QPushButton("R3CONN3CT >:]", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SIGNAL('tryAgain()'))

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.loadinglabel)
        layout_1 = QtGui.QHBoxLayout()
        layout_1.addWidget(self.cancel)
        layout_1.addWidget(self.ok)
        self.layout.addLayout(layout_1)
        self.setLayout(self.layout)

    def hideReconnect(self):
        self.ok.hide()
    def showReconnect(self):
        self.ok.show()

    tryAgain = QtCore.pyqtSignal()

class AboutPesterchum(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])

        self.title = QtGui.QLabel("P3ST3RCHUM V. %s" % (_pcVersion))
        self.credits = QtGui.QLabel("Programming by:\n\
  illuminatedwax (ghostDunk)\n\
  Kiooeht (evacipatedBox)\n\
  Lexi (lexicalNuance)\n\
  oakwhiz\n\
  alGore\n\
  Cerxi (binaryCabalist)\n\
  karxi (Midna)\n\
\n\
Art by:\n\
  Grimlive (aquaMarinist)\n\
  Cerxi (binaryCabalist)\n\
\n\
Special Thanks:\n\
  ABT\n\
  gamblingGenocider\n\
  Eco-Mono")

        self.ok = QtGui.QPushButton("OK", self)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.title)
        layout_0.addWidget(self.credits)
        layout_0.addWidget(self.ok)

        self.setLayout(layout_0)

class UpdatePesterchum(QtGui.QDialog):
    def __init__(self, ver, url, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.url = url
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pesterchum v%s Update" % (ver))
        self.setModal(False)

        self.title = QtGui.QLabel("An update to Pesterchum is available!")

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.title)

        self.ok = QtGui.QPushButton("D0WNL04D 4ND 1NST4LL N0W", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)

class AddChumDialog(QtGui.QDialog):
    def __init__(self, avail_groups, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Enter Chum Handle")
        self.setModal(True)

        self.title = QtGui.QLabel("Enter Chum Handle")
        self.chumBox = QtGui.QLineEdit(self)
        self.groupBox = QtGui.QComboBox(self)
        avail_groups.sort()
        avail_groups.pop(avail_groups.index("Chums"))
        avail_groups.insert(0, "Chums")
        for g in avail_groups:
            self.groupBox.addItem(g)
        self.newgrouplabel = QtGui.QLabel("Or make a new group:")
        self.newgroup = QtGui.QLineEdit(self)

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.title)
        layout_0.addWidget(self.chumBox)
        layout_0.addWidget(self.groupBox)
        layout_0.addWidget(self.newgrouplabel)
        layout_0.addWidget(self.newgroup)

        self.ok = QtGui.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('accept()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)
