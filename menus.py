from PyQt5 import QtCore, QtGui, QtWidgets
import re, ostools

from os import remove
from generic import RightClickList, RightClickTree, MultiTextDialog, NoneSound
from dataobjs import pesterQuirk, PesterProfile
from memos import TimeSlider, TimeInput
from version import _pcVersion

try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

_datadir = ostools.getDataDir()

class PesterQuirkItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, quirk):
        parent = None
        QtWidgets.QTreeWidgetItem.__init__(self, parent)
        self.quirk = quirk
        self.setText(0, str(quirk))
    def update(self, quirk):
        self.quirk = quirk
        self.setText(0, str(quirk))
    def __lt__(self, quirkitem):
        """Sets the order of quirks if auto-sorted by Qt. Obsolete now."""
        if self.quirk.type == "prefix":
            return True
        elif (self.quirk.type == "replace" or self.quirk.type == "regexp") and \
                quirkitem.type == "suffix":
            return True
        else:
            return False
class PesterQuirkList(QtWidgets.QTreeWidget):
    def __init__(self, mainwindow, parent):
        QtWidgets.QTreeWidget.__init__(self, parent)
        self.resize(400, 200)
        # make sure we have access to mainwindow info like profiles
        self.mainwindow = mainwindow
        self.setStyleSheet("background:black; color:white;")

        self.itemChanged[QtWidgets.QTreeWidgetItem, int].connect(self.changeCheckState)

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
            child_1 = QtWidgets.QTreeWidgetItem([item.quirk.group])
            self.addTopLevelItem(child_1)
            child_1.setFlags(child_1.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            child_1.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless)
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
                msgbox = QtWidgets.QMessageBox()
                msgbox.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
                msgbox.setObjectName("delquirkwarning")
                msgbox.setWindowTitle("WARNING!")
                msgbox.setInformativeText("Are you sure you want to delete the quirk group: %s" % (f.text(0)))
                msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                # Find the Cancel button and make it default
                for b in msgbox.buttons():
                    if msgbox.buttonRole(b) == QtWidgets.QMessageBox.RejectRole:
                        # We found the 'OK' button, set it as the default
                        b.setDefault(True)
                        b.setAutoDefault(True)
                        # Actually set it as the selected option, since we're
                        # already stealing focus
                        b.setFocus()
                        break
                ret = msgbox.exec_()
                if ret == QtWidgets.QMessageBox.Ok:
                    self.takeTopLevelItem(self.indexOfTopLevelItem(f))
            else:
                f.parent().takeChild(f.parent().indexOfChild(f))
        self.changeCheckState()

    @QtCore.pyqtSlot()
    def addQuirkGroup(self):
        if not hasattr(self, 'addgroupdialog'):
            self.addgroupdialog = None
        if not self.addgroupdialog:
            (gname, ok) = QtWidgets.QInputDialog.getText(self, "Add Group", "Enter a name for the new quirk group:")
            if ok:
                gname = str(gname)
                if re.search("[^A-Za-z0-9_\s]", gname) is not None:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setInformativeText("THIS IS NOT A VALID GROUP NAME")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    ret = msgbox.exec_()
                    self.addgroupdialog = None
                    return
                found = self.findItems(gname, QtCore.Qt.MatchExactly)
                if found:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setInformativeText("THIS QUIRK GROUP ALREADY EXISTS")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    ret = msgbox.exec_()
                    return
                child_1 = QtWidgets.QTreeWidgetItem([gname])
                self.addTopLevelItem(child_1)
                child_1.setFlags(child_1.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                child_1.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless)
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
from parsetools import convertTags, lexMessage, mecmd, colorBegin, colorEnd, img2smiley, smiledict
import parsetools
from dataobjs import pesterQuirks, PesterHistory
class QuirkTesterWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.prnt = parent
        self.mainwindow = parent.mainwindow
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Quirk Tester")
        self.resize(350,300)

        self.textArea = PesterText(self.mainwindow.theme, self)
        self.textInput = PesterInput(self.mainwindow.theme, self)
        self.textInput.setFocus()

        self.textInput.returnPressed.connect(self.sentMessage)

        self.chumopen = True
        self.chum = self.mainwindow.profile()
        self.history = PesterHistory()

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.textArea)
        layout_0.addWidget(self.textInput)
        self.setLayout(layout_0)

    def parent(self):
        return self.prnt

    def clearNewMessage(self):
        pass
    @QtCore.pyqtSlot()
    def sentMessage(self):
        text = str(self.textInput.text())

        return parsetools.kxhandleInput(self, text, "menus")

    def addMessage(self, msg, me=True):
        if type(msg) in [str, str]:
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

class PesterQuirkTypes(QtWidgets.QDialog):
    def __init__(self, parent, quirk=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.mainwindow = parent.mainwindow
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Quirk Wizard")
        self.resize(500,310)

        self.quirk = quirk
        self.pages = QtWidgets.QStackedWidget(self)

        self.next = QtWidgets.QPushButton("Next", self)
        self.next.setDefault(True)
        self.next.clicked.connect(self.nextPage)
        self.back = QtWidgets.QPushButton("Back", self)
        self.back.setEnabled(False)
        self.back.clicked.connect(self.backPage)
        self.cancel = QtWidgets.QPushButton("Cancel", self)
        self.cancel.clicked.connect(self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.setAlignment(QtCore.Qt.AlignRight)
        layout_2.addWidget(self.back)
        layout_2.addWidget(self.next)
        layout_2.addSpacing(5)
        layout_2.addWidget(self.cancel)

        vr = QtWidgets.QFrame()
        vr.setFrameShape(QtWidgets.QFrame.VLine)
        vr.setFrameShadow(QtWidgets.QFrame.Sunken)
        vr2 = QtWidgets.QFrame()
        vr2.setFrameShape(QtWidgets.QFrame.VLine)
        vr2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.funclist = QtWidgets.QListWidget(self)
        self.funclist.setStyleSheet("color: #000000; background-color: #FFFFFF;")
        self.funclist2 = QtWidgets.QListWidget(self)
        self.funclist2.setStyleSheet("color: #000000; background-color: #FFFFFF;")

        from parsetools import quirkloader
        funcs = [q+"()" for q in list(quirkloader.quirks.keys())]
        funcs.sort()
        self.funclist.addItems(funcs)
        self.funclist2.addItems(funcs)

        self.reloadQuirkFuncButton = QtWidgets.QPushButton("RELOAD FUNCTIONS", self)
        self.reloadQuirkFuncButton.clicked.connect(self.reloadQuirkFuncSlot)
        self.reloadQuirkFuncButton2 = QtWidgets.QPushButton("RELOAD FUNCTIONS", self)
        self.reloadQuirkFuncButton2.clicked.connect(self.reloadQuirkFuncSlot)

        self.funclist.setMaximumWidth(160)
        self.funclist.resize(160,50)
        self.funclist2.setMaximumWidth(160)
        self.funclist2.resize(160,50)
        layout_f = QtWidgets.QVBoxLayout()
        layout_f.addWidget(QtWidgets.QLabel("Available Regexp\nFunctions"))
        layout_f.addWidget(self.funclist)
        layout_f.addWidget(self.reloadQuirkFuncButton)
        layout_g = QtWidgets.QVBoxLayout()
        layout_g.addWidget(QtWidgets.QLabel("Available Regexp\nFunctions"))
        layout_g.addWidget(self.funclist2)
        layout_g.addWidget(self.reloadQuirkFuncButton2)

        # Pages
        # Type select
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_select = QtWidgets.QVBoxLayout(widget)
        layout_select.setAlignment(QtCore.Qt.AlignTop)
        self.radios = []
        self.radios.append(QtWidgets.QRadioButton("Prefix", self))
        self.radios.append(QtWidgets.QRadioButton("Suffix", self))
        self.radios.append(QtWidgets.QRadioButton("Simple Replace", self))
        self.radios.append(QtWidgets.QRadioButton("Regexp Replace", self))
        self.radios.append(QtWidgets.QRadioButton("Random Replace", self))
        self.radios.append(QtWidgets.QRadioButton("Mispeller", self))

        layout_select.addWidget(QtWidgets.QLabel("Select Quirk Type:"))
        for r in self.radios:
            layout_select.addWidget(r)

        # Prefix
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_prefix = QtWidgets.QVBoxLayout(widget)
        layout_prefix.setAlignment(QtCore.Qt.AlignTop)
        layout_prefix.addWidget(QtWidgets.QLabel("Prefix"))
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("Value:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_prefix.addLayout(layout_3)

        # Suffix
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_suffix = QtWidgets.QVBoxLayout(widget)
        layout_suffix.setAlignment(QtCore.Qt.AlignTop)
        layout_suffix.addWidget(QtWidgets.QLabel("Suffix"))
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("Value:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_suffix.addLayout(layout_3)

        # Simple Replace
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_replace = QtWidgets.QVBoxLayout(widget)
        layout_replace.setAlignment(QtCore.Qt.AlignTop)
        layout_replace.addWidget(QtWidgets.QLabel("Simple Replace"))
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("Replace:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_replace.addLayout(layout_3)
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("With:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_replace.addLayout(layout_3)

        # Regexp Replace
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_all = QtWidgets.QHBoxLayout(widget)
        layout_regexp = QtWidgets.QVBoxLayout()
        layout_regexp.setAlignment(QtCore.Qt.AlignTop)
        layout_regexp.addWidget(QtWidgets.QLabel("Regexp Replace"))
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("Regexp:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_regexp.addLayout(layout_3)
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(QtWidgets.QLabel("Replace With:"))
        layout_3.addWidget(QtWidgets.QLineEdit())
        layout_regexp.addLayout(layout_3)
        layout_all.addLayout(layout_f)
        layout_all.addWidget(vr)
        layout_all.addLayout(layout_regexp)

        # Random Replace
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_all = QtWidgets.QHBoxLayout(widget)
        layout_random = QtWidgets.QVBoxLayout()
        layout_random.setAlignment(QtCore.Qt.AlignTop)
        layout_random.addWidget(QtWidgets.QLabel("Random Replace"))
        layout_5 = QtWidgets.QHBoxLayout()
        regexpl = QtWidgets.QLabel("Regexp:", self)
        self.regexp = QtWidgets.QLineEdit("", self)
        layout_5.addWidget(regexpl)
        layout_5.addWidget(self.regexp)
        replacewithl = QtWidgets.QLabel("Replace With:", self)
        layout_all.addLayout(layout_g)
        layout_all.addWidget(vr2)
        layout_all.addLayout(layout_random)

        layout_6 = QtWidgets.QVBoxLayout()
        layout_7 = QtWidgets.QHBoxLayout()
        self.replacelist = QtWidgets.QListWidget(self)
        self.replaceinput = QtWidgets.QLineEdit(self)
        addbutton = QtWidgets.QPushButton("ADD", self)
        addbutton.clicked.connect(self.addRandomString)
        removebutton = QtWidgets.QPushButton("REMOVE", self)
        removebutton.clicked.connect(self.removeRandomString)
        layout_7.addWidget(addbutton)
        layout_7.addWidget(removebutton)
        layout_6.addLayout(layout_5)
        layout_6.addWidget(replacewithl)
        layout_6.addWidget(self.replacelist)
        layout_6.addWidget(self.replaceinput)
        layout_6.addLayout(layout_7)
        layout_random.addLayout(layout_6)

        # Misspeller
        widget = QtWidgets.QWidget()
        self.pages.addWidget(widget)
        layout_mispeller = QtWidgets.QVBoxLayout(widget)
        layout_mispeller.setAlignment(QtCore.Qt.AlignTop)
        layout_mispeller.addWidget(QtWidgets.QLabel("Mispeller"))
        layout_1 = QtWidgets.QHBoxLayout()
        zero = QtWidgets.QLabel("1%", self)
        hund = QtWidgets.QLabel("100%", self)
        self.current = QtWidgets.QLabel("50%", self)
        self.current.setAlignment(QtCore.Qt.AlignHCenter)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged[int].connect(self.printValue)
        layout_1.addWidget(zero)
        layout_1.addWidget(self.slider)
        layout_1.addWidget(hund)
        layout_mispeller.addLayout(layout_1)
        layout_mispeller.addWidget(self.current)

        layout_0 = QtWidgets.QVBoxLayout()
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
                    item = QtWidgets.QListWidgetItem(v, self.replacelist)
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
        text = str(self.replaceinput.text())
        item = QtWidgets.QListWidgetItem(text, self.replacelist)
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
        funcs = [q+"()" for q in list(quirkloader.quirks.keys())]
        funcs.sort()
        self.funclist.clear()
        self.funclist.addItems(funcs)
        self.funclist2.clear()
        self.funclist2.addItems(funcs)

class PesterChooseQuirks(QtWidgets.QDialog):
    def __init__(self, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Set Quirks")

        self.quirkList = PesterQuirkList(self.mainwindow, self)

        self.addQuirkButton = QtWidgets.QPushButton("ADD QUIRK", self)
        self.addQuirkButton.clicked.connect(self.addQuirkDialog)

        self.upShiftButton = QtWidgets.QPushButton("^", self)
        self.downShiftButton = QtWidgets.QPushButton("v", self)
        self.upShiftButton.setToolTip("Move quirk up one")
        self.downShiftButton.setToolTip("Move quirk down one")
        self.upShiftButton.clicked.connect(self.quirkList.upShiftQuirk)
        self.downShiftButton.clicked.connect(self.quirkList.downShiftQuirk)

        self.newGroupButton = QtWidgets.QPushButton("*", self)
        self.newGroupButton.setToolTip("New Quirk Group")
        self.newGroupButton.clicked.connect(self.quirkList.addQuirkGroup)

        layout_quirklist = QtWidgets.QHBoxLayout() #the nude layout quirklist
        layout_shiftbuttons = QtWidgets.QVBoxLayout() #the shift button layout
        layout_shiftbuttons.addWidget(self.upShiftButton)
        layout_shiftbuttons.addWidget(self.newGroupButton)
        layout_shiftbuttons.addWidget(self.downShiftButton)
        layout_quirklist.addWidget(self.quirkList)
        layout_quirklist.addLayout(layout_shiftbuttons)

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.addQuirkButton)

        self.editSelectedButton = QtWidgets.QPushButton("EDIT", self)
        self.editSelectedButton.clicked.connect(self.editSelected)
        self.removeSelectedButton = QtWidgets.QPushButton("REMOVE", self)
        self.removeSelectedButton.clicked.connect(self.quirkList.removeCurrent)
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(self.editSelectedButton)
        layout_3.addWidget(self.removeSelectedButton)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.test = QtWidgets.QPushButton("TEST QUIRKS", self)
        self.test.clicked.connect(self.testQuirks)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.test)
        layout_ok.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
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
        self.quirkadd.accepted.connect(self.addQuirk)
        self.quirkadd.rejected.connect(self.closeQuirk)
        self.quirkadd.show()
    @QtCore.pyqtSlot()
    def addQuirk(self):
        types = ["prefix","suffix","replace","regexp","random","spelling"]
        vdict = {}
        vdict["type"] = types[self.quirkadd.pages.currentIndex()-1]
        page = self.quirkadd.pages.currentWidget().layout()
        if vdict["type"] in ("prefix","suffix"):
            vdict["value"] = str(page.itemAt(1).layout().itemAt(1).widget().text())
        elif vdict["type"] == "replace":
            vdict["from"] = str(page.itemAt(1).layout().itemAt(1).widget().text())
            vdict["to"] = str(page.itemAt(2).layout().itemAt(1).widget().text())
        elif vdict["type"] == "regexp":
            vdict["from"] = str(page.itemAt(2).layout().itemAt(1).layout().itemAt(1).widget().text())
            vdict["to"] = str(page.itemAt(2).layout().itemAt(2).layout().itemAt(1).widget().text())
        elif vdict["type"] == "random":
            vdict["from"] = str(self.quirkadd.regexp.text())
            randomlist = [str(self.quirkadd.replacelist.item(i).text())
                          for i in range(0,self.quirkadd.replacelist.count())]
            vdict["randomlist"] = randomlist
        elif vdict["type"] == "spelling":
            vdict["percentage"] = self.quirkadd.slider.value()

        if vdict["type"] in ("regexp", "random"):
            try:
                re.compile(vdict["from"])
            except re.error as e:
                quirkWarning = QtWidgets.QMessageBox(self)
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

class PesterChooseTheme(QtWidgets.QDialog):
    def __init__(self, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.config = config
        self.theme = theme
        self.parent = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pick a theme")

        instructions = QtWidgets.QLabel("Pick a theme:")

        avail_themes = config.availableThemes()
        self.themeBox = QtWidgets.QComboBox(self)
        for (i, t) in enumerate(avail_themes):
            self.themeBox.addItem(t)
            if t == theme.name:
                self.themeBox.setCurrentIndex(i)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(instructions)
        layout_0.addWidget(self.themeBox)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)

        self.accepted.connect(parent.themeSelected)
        self.rejected.connect(parent.closeTheme)

class PesterChooseProfile(QtWidgets.QDialog):
    def __init__(self, userprofile, config, theme, parent, collision=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.userprofile = userprofile
        self.theme = theme
        self.config = config
        self.parent = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        self.currentHandle = QtWidgets.QLabel("CHANGING FROM %s" % userprofile.chat.handle)
        self.chumHandle = QtWidgets.QLineEdit(self)
        self.chumHandle.setMinimumWidth(200)
        self.chumHandle.setObjectName("setprofilehandle")
        self.chumHandleLabel = QtWidgets.QLabel(self.theme["main/mychumhandle/label/text"], self)
        self.chumColorButton = QtWidgets.QPushButton(self)
        self.chumColorButton.setObjectName("setprofilecolor")
        self.chumColorButton.resize(50, 20)
        self.chumColorButton.setStyleSheet("background: %s" % (userprofile.chat.colorhtml()))
        self.chumcolor = userprofile.chat.color
        self.chumColorButton.clicked.connect(self.openColorDialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.chumHandleLabel)
        layout_1.addWidget(self.chumHandle)
        layout_1.addWidget(self.chumColorButton)

        # available profiles?
        avail_profiles = self.config.availableProfiles()
        if avail_profiles:
            self.profileBox = QtWidgets.QComboBox(self)
            self.profileBox.addItem("Choose a profile...")
            for p in avail_profiles:
                self.profileBox.addItem(p.chat.handle)
        else:
            self.profileBox = None

        self.defaultcheck = QtWidgets.QCheckBox(self)
        self.defaultlabel = QtWidgets.QLabel("Set This Profile As Default", self)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.defaultlabel)
        layout_2.addWidget(self.defaultcheck)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.validateProfile)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        if not collision and avail_profiles:
            self.delete = QtWidgets.QPushButton("DELETE", self)
            self.delete.clicked.connect(self.deleteProfile)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
        if collision:
            collision_warning = QtWidgets.QLabel("%s is taken already! Pick a new profile." % (collision))
            layout_0.addWidget(collision_warning)
        else:
            layout_0.addWidget(self.currentHandle, alignment=QtCore.Qt.AlignHCenter)
        layout_0.addLayout(layout_1)
        if avail_profiles:
            profileLabel = QtWidgets.QLabel("Or choose an existing profile:", self)
            layout_0.addWidget(profileLabel)
            layout_0.addWidget(self.profileBox)
        layout_0.addLayout(layout_ok)
        if not collision and avail_profiles:
            layout_0.addWidget(self.delete)
        layout_0.addLayout(layout_2)
        self.errorMsg = QtWidgets.QLabel(self)
        self.errorMsg.setObjectName("errormsg")
        self.errorMsg.setStyleSheet("color:red;")
        layout_0.addWidget(self.errorMsg)
        self.setLayout(layout_0)

        self.accepted.connect(parent.profileSelected)
        self.rejected.connect(parent.closeProfile)

    @QtCore.pyqtSlot()
    def openColorDialog(self):
        self.colorDialog = QtWidgets.QColorDialog(self)
        color = self.colorDialog.getColor(initial=self.userprofile.chat.color)
        self.chumColorButton.setStyleSheet("background: %s" % color.name())
        self.chumcolor = color
        self.colorDialog = None

    @QtCore.pyqtSlot()
    def validateProfile(self):
        if not self.profileBox or self.profileBox.currentIndex() == 0:
            handle = str(self.chumHandle.text())
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
            handle = str(self.profileBox.currentText())
            if handle == self.parent.profile().handle:
                problem = QtWidgets.QMessageBox()
                # karxi Will probably change this to its own name later.
                problem.setObjectName("errmsg")
                problem.setStyleSheet(self.theme["main/defaultwindow/style"])
                problem.setWindowTitle("Problem!")
                problem.setInformativeText("You can't delete the profile you're currently using!")
                problem.setStandardButtons(QtWidgets.QMessageBox.Ok)
                problem.exec_()
                return
            # TODO: Make this select 'no' as the default, as usual.
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(self.theme["main/defaultwindow/style"])
            msgbox.setWindowTitle("WARNING!")
            msgbox.setInformativeText("Are you sure you want to delete the profile: %s" % (handle))
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            ret = msgbox.exec_()
            if ret == QtWidgets.QMessageBox.Ok:
                try:
                    remove(_datadir+"profiles/%s.js" % (handle))
                except OSError:
                    problem = QtWidgets.QMessageBox()
                    problem.setObjectName("errmsg")
                    problem.setStyleSheet(self.theme["main/defaultwindow/style"])
                    problem.setWindowTitle("Problem!")
                    problem.setInformativeText("There was a problem deleting the profile: %s" % (handle))
                    problem.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    problem.exec_()

class PesterMentions(QtWidgets.QDialog):
    def __init__(self, window, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Mentions")
        self.setModal(True)
        self.mainwindow = window
        self.theme = theme
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        self.mentionlist = QtWidgets.QListWidget(self)
        self.mentionlist.addItems(self.mainwindow.userprofile.getMentions())

        self.addBtn = QtWidgets.QPushButton("ADD MENTION", self)
        self.addBtn.clicked.connect(self.addMention)

        self.editBtn = QtWidgets.QPushButton("EDIT", self)
        self.editBtn.clicked.connect(self.editSelected)
        self.rmBtn = QtWidgets.QPushButton("REMOVE", self)
        self.rmBtn.clicked.connect(self.removeCurrent)
        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.editBtn)
        layout_1.addWidget(self.rmBtn)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
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
        except re.error as e:
            quirkWarning = QtWidgets.QMessageBox(self)
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

class PesterOptions(QtWidgets.QDialog):
    def __init__(self, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Options")
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.setStyleSheet(self.theme["main/defaultwindow/style"])

        layout_4 = QtWidgets.QVBoxLayout()

        hr = QtWidgets.QFrame()
        hr.setFrameShape(QtWidgets.QFrame.HLine)
        hr.setFrameShadow(QtWidgets.QFrame.Sunken)
        vr = QtWidgets.QFrame()
        vr.setFrameShape(QtWidgets.QFrame.VLine)
        vr.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.tabs = QtWidgets.QButtonGroup(self)
        self.tabs.buttonClicked[int].connect(self.changePage)
        tabNames = ["Chum List", "Conversations", "Interface", "Sound", "Notifications", "Logging", "Idle/Updates", "Theme", "Connection"]
        if parent.advanced: tabNames.append("Advanced")
        for t in tabNames:
            button = QtWidgets.QPushButton(t)
            self.tabs.addButton(button)
            layout_4.addWidget(button)
            button.setCheckable(True)
        self.tabs.button(-2).setChecked(True)
        self.pages = QtWidgets.QStackedWidget(self)

        self.bandwidthcheck = QtWidgets.QCheckBox("Low Bandwidth", self)
        if self.config.lowBandwidth():
            self.bandwidthcheck.setChecked(True)
        bandwidthLabel = QtWidgets.QLabel("(Stops you for receiving the flood of MOODS,\n"
                                      " though stops chumlist from working properly)")
        font = bandwidthLabel.font()
        font.setPointSize(8)
        bandwidthLabel.setFont(font)

        self.autonickserv = QtWidgets.QCheckBox("Auto-Identify with NickServ", self)
        self.autonickserv.setChecked(parent.userprofile.getAutoIdentify())
        self.autonickserv.stateChanged[int].connect(self.autoNickServChange)
        self.nickservpass = QtWidgets.QLineEdit(self)
        self.nickservpass.setPlaceholderText("NickServ Password")
        self.nickservpass.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.nickservpass.setText(parent.userprofile.getNickServPass())

        self.autojoinlist = QtWidgets.QListWidget(self)
        self.autojoinlist.addItems(parent.userprofile.getAutoJoins())
        self.addAutoJoinBtn = QtWidgets.QPushButton("Add", self)
        self.addAutoJoinBtn.clicked.connect(self.addAutoJoin)
        self.delAutoJoinBtn = QtWidgets.QPushButton("Remove", self)
        self.delAutoJoinBtn.clicked.connect(self.delAutoJoin)

        self.tabcheck = QtWidgets.QCheckBox("Tabbed Conversations", self)
        if self.config.tabs():
            self.tabcheck.setChecked(True)
        self.tabmemocheck = QtWidgets.QCheckBox("Tabbed Memos", self)
        if self.config.tabMemos():
            self.tabmemocheck.setChecked(True)
        self.hideOffline = QtWidgets.QCheckBox("Hide Offline Chums", self)
        if self.config.hideOfflineChums():
            self.hideOffline.setChecked(True)

        self.soundcheck = QtWidgets.QCheckBox("Sounds On", self)
        self.soundcheck.stateChanged[int].connect(self.soundChange)
        self.chatsoundcheck = QtWidgets.QCheckBox("Pester Sounds", self)
        self.chatsoundcheck.setChecked(self.config.chatSound())
        self.memosoundcheck = QtWidgets.QCheckBox("Memo Sounds", self)
        self.memosoundcheck.setChecked(self.config.memoSound())
        self.memosoundcheck.stateChanged[int].connect(self.memoSoundChange)
        self.memopingcheck = QtWidgets.QCheckBox("Memo Ping", self)
        self.memopingcheck.setChecked(self.config.memoPing())
        self.namesoundcheck = QtWidgets.QCheckBox("Memo Mention (initials)", self)
        self.namesoundcheck.setChecked(self.config.nameSound())
        if self.config.soundOn():
            self.soundcheck.setChecked(True)
            if not self.memosoundcheck.isChecked():
                self.memoSoundChange(0)
        else:
            self.chatsoundcheck.setEnabled(False)
            self.memosoundcheck.setEnabled(False)
            self.memoSoundChange(0)

        self.editMentions = QtWidgets.QPushButton("Edit Mentions", self)
        self.editMentions.clicked.connect(self.openMentions)
        self.editMentions2 = QtWidgets.QPushButton("Edit Mentions", self)
        self.editMentions2.clicked.connect(self.openMentions)

        self.volume = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(self.config.volume())
        self.volume.valueChanged[int].connect(self.printValue)
        # Disable the volume slider if we can't actually use it.
        if parent.canSetVolume():
            self.currentVol = QtWidgets.QLabel(
                    "{0!s}%".format(self.config.volume()), self)
            # We don't need to explicitly set this, but it helps drive the
            # point home
            self.volume.setEnabled(True)
        else:
            # We can't set the volume....
            self.currentVol = QtWidgets.QLabel(
                    "(Disabled: Sound Mixer Error)", self)
            self.volume.setEnabled(False)
        self.currentVol.setAlignment(QtCore.Qt.AlignHCenter)


        self.timestampcheck = QtWidgets.QCheckBox("Time Stamps", self)
        if self.config.showTimeStamps():
            self.timestampcheck.setChecked(True)

        self.timestampBox = QtWidgets.QComboBox(self)
        self.timestampBox.addItem("12 hour")
        self.timestampBox.addItem("24 hour")
        if self.config.time12Format():
            self.timestampBox.setCurrentIndex(0)
        else:
            self.timestampBox.setCurrentIndex(1)
        self.secondscheck = QtWidgets.QCheckBox("Show Seconds", self)
        if self.config.showSeconds():
            self.secondscheck.setChecked(True)

        self.memomessagecheck = QtWidgets.QCheckBox("Show OP and Voice Messages in Memos", self)
        if self.config.opvoiceMessages():
            self.memomessagecheck.setChecked(True)

        if not ostools.isOSXBundle():
            self.animationscheck = QtWidgets.QCheckBox("Use animated smilies", self)
            if self.config.animations():
                self.animationscheck.setChecked(True)
            animateLabel = QtWidgets.QLabel("(Disable if you leave chats open for LOOOONG periods of time)")
            font = animateLabel.font()
            font.setPointSize(8)
            animateLabel.setFont(font)

        self.userlinkscheck = QtWidgets.QCheckBox("Disable #Memo and @User Links", self)
        self.userlinkscheck.setChecked(self.config.disableUserLinks())
        self.userlinkscheck.setVisible(False)


        # Will add ability to turn off groups later
        #self.groupscheck = QtGui.QCheckBox("Use Groups", self)
        #self.groupscheck.setChecked(self.config.useGroups())
        self.showemptycheck = QtWidgets.QCheckBox("Show Empty Groups", self)
        self.showemptycheck.setChecked(self.config.showEmptyGroups())
        self.showonlinenumbers = QtWidgets.QCheckBox("Show Number of Online Chums", self)
        self.showonlinenumbers.setChecked(self.config.showOnlineNumbers())

        sortLabel = QtWidgets.QLabel("Sort Chums")
        self.sortBox = QtWidgets.QComboBox(self)
        self.sortBox.addItem("Alphabetically")
        self.sortBox.addItem("By Mood")
        self.sortBox.addItem("Manually")
        method = self.config.sortMethod()
        if method >= 0 and method < self.sortBox.count():
            self.sortBox.setCurrentIndex(method)
        layout_3 = QtWidgets.QHBoxLayout()
        layout_3.addWidget(sortLabel)
        layout_3.addWidget(self.sortBox, 10)

        self.logpesterscheck = QtWidgets.QCheckBox("Log all Pesters", self)
        if self.config.logPesters() & self.config.LOG:
            self.logpesterscheck.setChecked(True)
        self.logmemoscheck = QtWidgets.QCheckBox("Log all Memos", self)
        if self.config.logMemos() & self.config.LOG:
            self.logmemoscheck.setChecked(True)
        self.stamppestercheck = QtWidgets.QCheckBox("Log Time Stamps for Pesters", self)
        if self.config.logPesters() & self.config.STAMP:
            self.stamppestercheck.setChecked(True)
        self.stampmemocheck = QtWidgets.QCheckBox("Log Time Stamps for Memos", self)
        if self.config.logMemos() & self.config.STAMP:
            self.stampmemocheck.setChecked(True)

        self.idleBox = QtWidgets.QSpinBox(self)
        self.idleBox.setStyleSheet("background:#FFFFFF")
        self.idleBox.setRange(1, 1440)
        self.idleBox.setValue(self.config.idleTime())
        layout_5 = QtWidgets.QHBoxLayout()
        layout_5.addWidget(QtWidgets.QLabel("Minutes before Idle:"))
        layout_5.addWidget(self.idleBox)

        #self.updateBox = QtWidgets.QComboBox(self)
        #self.updateBox.addItem("Once a Day")
        #self.updateBox.addItem("Once a Week")
        #self.updateBox.addItem("Only on Start")
        #self.updateBox.addItem("Never")
        #check = self.config.checkForUpdates()
        #if check >= 0 and check < self.updateBox.count():
        #    self.updateBox.setCurrentIndex(check)
        layout_6 = QtWidgets.QHBoxLayout()
        #layout_6.addWidget(QtWidgets.QLabel("Check for\nPesterchum Updates:"))
        #layout_6.addWidget(self.updateBox)

        #if not ostools.isOSXLeopard():
        #    self.mspaCheck = QtWidgets.QCheckBox("Check for MSPA Updates", self)
        #    self.mspaCheck.setChecked(self.config.checkMSPA())

        self.randomscheck = QtWidgets.QCheckBox("Receive Random Encounters")
        self.randomscheck.setChecked(parent.userprofile.randoms)
        if not parent.randhandler.running:
            self.randomscheck.setEnabled(False)

        avail_themes = self.config.availableThemes()
        self.themeBox = QtWidgets.QComboBox(self)
        notheme = (theme.name not in avail_themes)
        for (i, t) in enumerate(avail_themes):
            self.themeBox.addItem(t)
            if (not notheme and t == theme.name) or (notheme and t == "pesterchum"):
                self.themeBox.setCurrentIndex(i)
        self.refreshtheme = QtWidgets.QPushButton("Refresh current theme", self)
        self.refreshtheme.clicked.connect(parent.themeSelectOverride)
        self.ghostchum = QtWidgets.QCheckBox("Pesterdunk Ghostchum!!", self)
        self.ghostchum.setChecked(self.config.ghostchum())

        self.buttonOptions = ["Minimize to Taskbar", "Minimize to Tray", "Quit"]
        self.miniBox = QtWidgets.QComboBox(self)
        self.miniBox.addItems(self.buttonOptions)
        self.miniBox.setCurrentIndex(self.config.minimizeAction())
        self.closeBox = QtWidgets.QComboBox(self)
        self.closeBox.addItems(self.buttonOptions)
        self.closeBox.setCurrentIndex(self.config.closeAction())
        layout_mini = QtWidgets.QHBoxLayout()
        layout_mini.addWidget(QtWidgets.QLabel("Minimize"))
        layout_mini.addWidget(self.miniBox)
        layout_close = QtWidgets.QHBoxLayout()
        layout_close.addWidget(QtWidgets.QLabel("Close"))
        layout_close.addWidget(self.closeBox)

        self.pesterBlink = QtWidgets.QCheckBox("Blink Taskbar on Pesters", self)
        if self.config.blink() & self.config.PBLINK:
            self.pesterBlink.setChecked(True)
        self.memoBlink = QtWidgets.QCheckBox("Blink Taskbar on Memos", self)
        if self.config.blink() & self.config.MBLINK:
            self.memoBlink.setChecked(True)

        self.notifycheck = QtWidgets.QCheckBox("Toast Notifications", self)
        if self.config.notify():
            self.notifycheck.setChecked(True)
        self.notifycheck.stateChanged[int].connect(self.notifyChange)
        self.notifyOptions = QtWidgets.QComboBox(self)
        types = self.parent().tm.availableTypes()
        cur = self.parent().tm.currentType()
        self.notifyOptions.addItems(types)
        for (i,t) in enumerate(types):
            if t == cur:
                self.notifyOptions.setCurrentIndex(i)
                break
        self.notifyTypeLabel = QtWidgets.QLabel("Type", self)
        layout_type = QtWidgets.QHBoxLayout()
        layout_type.addWidget(self.notifyTypeLabel)
        layout_type.addWidget(self.notifyOptions)
        self.notifySigninCheck   = QtWidgets.QCheckBox("Chum signs in", self)
        if self.config.notifyOptions() & self.config.SIGNIN:
            self.notifySigninCheck.setChecked(True)
        self.notifySignoutCheck  = QtWidgets.QCheckBox("Chum signs out", self)
        if self.config.notifyOptions() & self.config.SIGNOUT:
            self.notifySignoutCheck.setChecked(True)
        self.notifyNewMsgCheck   = QtWidgets.QCheckBox("New messages", self)
        if self.config.notifyOptions() & self.config.NEWMSG:
            self.notifyNewMsgCheck.setChecked(True)
        self.notifyNewConvoCheck = QtWidgets.QCheckBox("Only new conversations", self)
        if self.config.notifyOptions() & self.config.NEWCONVO:
            self.notifyNewConvoCheck.setChecked(True)
        self.notifyMentionsCheck = QtWidgets.QCheckBox("Memo Mentions (initials)", self)
        if self.config.notifyOptions() & self.config.INITIALS:
            self.notifyMentionsCheck.setChecked(True)
        self.notifyChange(self.notifycheck.checkState())

        if parent.advanced:
            # NOTE: This doesn't do anything right now - so change it!
            self.modechange = QtWidgets.QLineEdit(self)
            layout_change = QtWidgets.QHBoxLayout()
            layout_change.addWidget(QtWidgets.QLabel("Change:"))
            layout_change.addWidget(self.modechange)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        # Tab layouts
        # Chum List
        widget = QtWidgets.QWidget()
        layout_chumlist = QtWidgets.QVBoxLayout(widget)
        layout_chumlist.setAlignment(QtCore.Qt.AlignTop)
        layout_chumlist.addWidget(self.hideOffline)
        #layout_chumlist.addWidget(self.groupscheck)
        layout_chumlist.addWidget(self.showemptycheck)
        layout_chumlist.addWidget(self.showonlinenumbers)
        layout_chumlist.addLayout(layout_3)
        self.pages.addWidget(widget)

        # Conversations
        widget = QtWidgets.QWidget()
        layout_chat = QtWidgets.QVBoxLayout(widget)
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
        widget = QtWidgets.QWidget()
        layout_interface = QtWidgets.QVBoxLayout(widget)
        layout_interface.setAlignment(QtCore.Qt.AlignTop)
        layout_interface.addWidget(self.tabcheck)
        layout_interface.addWidget(self.tabmemocheck)
        layout_interface.addLayout(layout_mini)
        layout_interface.addLayout(layout_close)
        layout_interface.addWidget(self.pesterBlink)
        layout_interface.addWidget(self.memoBlink)
        self.pages.addWidget(widget)

        # Sound
        widget = QtWidgets.QWidget()
        layout_sound = QtWidgets.QVBoxLayout(widget)
        layout_sound.setAlignment(QtCore.Qt.AlignTop)
        layout_sound.addWidget(self.soundcheck)
        layout_indent = QtWidgets.QVBoxLayout()
        layout_indent.addWidget(self.chatsoundcheck)
        layout_indent.addWidget(self.memosoundcheck)
        layout_doubleindent = QtWidgets.QVBoxLayout()
        layout_doubleindent.addWidget(self.memopingcheck)
        layout_doubleindent.addWidget(self.namesoundcheck)
        layout_doubleindent.addWidget(self.editMentions)
        layout_doubleindent.setContentsMargins(22,0,0,0)
        layout_indent.addLayout(layout_doubleindent)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_sound.addLayout(layout_indent)
        layout_sound.addSpacing(15)
        mvol = QtWidgets.QLabel("Master Volume:", self)
        # If we can't set the volume, grey this out as well
        #~mvol.setEnabled(parent.canSetVolume())
        # Normally we'd grey this out, but that presently makes things
        # rather unreadable
        # Later we can look into changing the color to a theme[] entry
        layout_sound.addWidget(mvol)
        layout_sound.addWidget(self.volume)
        layout_sound.addWidget(self.currentVol)
        self.pages.addWidget(widget)

        # Notifications
        widget = QtWidgets.QWidget()
        layout_notify = QtWidgets.QVBoxLayout(widget)
        layout_notify.setAlignment(QtCore.Qt.AlignTop)
        layout_notify.addWidget(self.notifycheck)
        layout_indent = QtWidgets.QVBoxLayout()
        layout_indent.addLayout(layout_type)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_indent.addWidget(self.notifySigninCheck)
        layout_indent.addWidget(self.notifySignoutCheck)
        layout_indent.addWidget(self.notifyNewMsgCheck)
        layout_doubleindent = QtWidgets.QVBoxLayout()
        layout_doubleindent.addWidget(self.notifyNewConvoCheck)
        layout_doubleindent.setContentsMargins(22,0,0,0)
        layout_indent.addLayout(layout_doubleindent)
        layout_indent.addWidget(self.notifyMentionsCheck)
        layout_indent.addWidget(self.editMentions2)
        layout_notify.addLayout(layout_indent)
        self.pages.addWidget(widget)

        # Logging
        widget = QtWidgets.QWidget()
        layout_logs = QtWidgets.QVBoxLayout(widget)
        layout_logs.setAlignment(QtCore.Qt.AlignTop)
        layout_logs.addWidget(self.logpesterscheck)
        layout_logs.addWidget(self.logmemoscheck)
        layout_logs.addWidget(self.stamppestercheck)
        layout_logs.addWidget(self.stampmemocheck)
        self.pages.addWidget(widget)

        # Idle/Updates
        widget = QtWidgets.QWidget()
        layout_idle = QtWidgets.QVBoxLayout(widget)
        layout_idle.setAlignment(QtCore.Qt.AlignTop)
        layout_idle.addLayout(layout_5)
        layout_idle.addLayout(layout_6)
        #if not ostools.isOSXLeopard():
        #    layout_idle.addWidget(self.mspaCheck)
        self.pages.addWidget(widget)

        # Theme
        widget = QtWidgets.QWidget()
        layout_theme = QtWidgets.QVBoxLayout(widget)
        layout_theme.setAlignment(QtCore.Qt.AlignTop)
        layout_theme.addWidget(QtWidgets.QLabel("Pick a Theme:"))
        layout_theme.addWidget(self.themeBox)
        layout_theme.addWidget(self.refreshtheme)
        layout_theme.addWidget(self.ghostchum)
        self.pages.addWidget(widget)

        # Connection
        widget = QtWidgets.QWidget()
        layout_connect = QtWidgets.QVBoxLayout(widget)
        layout_connect.setAlignment(QtCore.Qt.AlignTop)
        layout_connect.addWidget(self.bandwidthcheck)
        layout_connect.addWidget(bandwidthLabel)
        layout_connect.addWidget(self.autonickserv)
        layout_indent = QtWidgets.QVBoxLayout()
        layout_indent.addWidget(self.nickservpass)
        layout_indent.setContentsMargins(22,0,0,0)
        layout_connect.addLayout(layout_indent)
        layout_connect.addWidget(QtWidgets.QLabel("Auto-Join Memos:"))
        layout_connect.addWidget(self.autojoinlist)
        layout_8 = QtWidgets.QHBoxLayout()
        layout_8.addWidget(self.addAutoJoinBtn)
        layout_8.addWidget(self.delAutoJoinBtn)
        layout_connect.addLayout(layout_8)
        self.pages.addWidget(widget)

        # Advanced
        if parent.advanced:
            widget = QtWidgets.QWidget()
            layout_advanced = QtWidgets.QVBoxLayout(widget)
            layout_advanced.setAlignment(QtCore.Qt.AlignTop)
            layout_advanced.addWidget(QtWidgets.QLabel("Current User Mode: %s" % parent.modes))
            layout_advanced.addLayout(layout_change)
            self.pages.addWidget(widget)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_1 = QtWidgets.QHBoxLayout()
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
            self.mentionmenu.accepted.connect(self.updateMentions)
            self.mentionmenu.rejected.connect(self.closeMentions)
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

class PesterUserlist(QtWidgets.QDialog):
    def __init__(self, config, theme, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(False)
        self.config = config
        self.theme = theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.resize(200, 600)

        self.searchbox = QtWidgets.QLineEdit(self)
        #self.searchbox.setStyleSheet(theme["convo/input/style"]) # which style is better?
        self.searchbox.setPlaceholderText("Search")
        self.searchbox.textChanged['QString'].connect(self.updateUsers)

        self.label = QtWidgets.QLabel("USERLIST")
        self.userarea = RightClickList(self)
        self.userarea.setStyleSheet(self.theme["main/chums/style"])
        self.userarea.optionsMenu = QtWidgets.QMenu(self)

        self.addChumAction = QtWidgets.QAction(self.mainwindow.theme["main/menus/rclickchumlist/addchum"], self)
        self.addChumAction.triggered.connect(self.addChumSlot)
        self.pesterChumAction = QtWidgets.QAction(self.mainwindow.theme["main/menus/rclickchumlist/pester"], self)
        self.pesterChumAction.triggered.connect(self.pesterChumSlot)
        self.userarea.optionsMenu.addAction(self.addChumAction)
        self.userarea.optionsMenu.addAction(self.pesterChumAction)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.label)
        layout_0.addWidget(self.userarea)
        layout_0.addWidget(self.searchbox)
        layout_0.addWidget(self.ok)

        self.setLayout(layout_0)

        self.mainwindow.namesUpdated.connect(self.updateUsers)

        self.mainwindow.userPresentSignal['QString', 'QString', 'QString'].connect(self.updateUserPresent)
        self.updateUsers()

        self.searchbox.setFocus()
    @QtCore.pyqtSlot()
    def updateUsers(self):
        names = self.mainwindow.namesdb["#pesterchum"]
        self.userarea.clear()
        for n in names:
            if str(self.searchbox.text()) == "" or n.lower().find(str(self.searchbox.text()).lower()) != -1:
                item = QtWidgets.QListWidgetItem(n)
                item.setForeground(QtGui.QBrush(QtGui.QColor(self.theme["main/chums/userlistcolor"])))
                self.userarea.addItem(item)
        self.userarea.sortItems()
    @QtCore.pyqtSlot(QString, QString, QString)
    def updateUserPresent(self, handle, channel, update):
        h = str(handle)
        c = str(channel)
        if update == "quit":
            self.delUser(h)
        elif update == "left" and c == "#pesterchum":
            self.delUser(h)
        elif update == "join" and c == "#pesterchum":
            if str(self.searchbox.text()) == "" or h.lower().find(str(self.searchbox.text()).lower()) != -1:
                self.addUser(h)
    def addUser(self, name):
        item = QtWidgets.QListWidgetItem(name)
        item.setForeground(QtGui.QBrush(QtGui.QColor(self.theme["main/chums/userlistcolor"])))
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
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(theme["main/chums/userlistcolor"])))

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

    addChum = QtCore.pyqtSignal('QString')
    pesterChum = QtCore.pyqtSignal('QString')


class MemoListItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, channel, usercount):
        QtWidgets.QTreeWidgetItem.__init__(self, [channel, str(usercount)])
        self.target = channel
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        if str(self.text(column)).isdigit() and str(other.text(column)).isdigit():
            return int(self.text(column)) < int(other.text(column))
        return self.text(column) < other.text(column)

class PesterMemoList(QtWidgets.QDialog):
    def __init__(self, parent, channel=""):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(False)
        self.theme = parent.theme
        self.mainwindow = parent
        self.setStyleSheet(self.theme["main/defaultwindow/style"])
        self.resize(460, 300)

        self.label = QtWidgets.QLabel("MEMOS")
        self.channelarea = RightClickTree(self)
        self.channelarea.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.channelarea.setStyleSheet(self.theme["main/chums/style"])
        self.channelarea.optionsMenu = QtWidgets.QMenu(self)
        self.channelarea.setColumnCount(2)
        self.channelarea.setHeaderLabels(["Memo", "Users"])
        self.channelarea.setIndentation(0)
        self.channelarea.setColumnWidth(0,200)
        self.channelarea.setColumnWidth(1,10)
        self.channelarea.setSortingEnabled(True)
        self.channelarea.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.channelarea.itemDoubleClicked[QtWidgets.QTreeWidgetItem, int].connect(self.AcceptSelection)

        self.orjoinlabel = QtWidgets.QLabel("OR MAKE A NEW MEMO:")
        self.newmemo = QtWidgets.QLineEdit(channel, self)
        self.secretChannel = QtWidgets.QCheckBox("HIDDEN CHANNEL?", self)
        self.inviteChannel = QtWidgets.QCheckBox("INVITATION ONLY?", self)

        self.timelabel = QtWidgets.QLabel("TIMEFRAME:")
        self.timeslider = TimeSlider(QtCore.Qt.Horizontal, self)
        self.timeinput = TimeInput(self.timeslider, self)

        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        self.join = QtWidgets.QPushButton("JOIN", self)
        self.join.setDefault(True)
        self.join.clicked.connect(self.AcceptIfSelectionMade)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.join)

        layout_left  = QtWidgets.QVBoxLayout()
        layout_right = QtWidgets.QVBoxLayout()
        layout_right.setAlignment(QtCore.Qt.AlignTop)
        layout_0 = QtWidgets.QVBoxLayout()
        layout_1 = QtWidgets.QHBoxLayout()
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
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(self.theme["main/chums/userlistcolor"])))
            item.setForeground(1, QtGui.QBrush(QtGui.QColor(self.theme["main/chums/userlistcolor"])))
            item.setIcon(0, QtGui.QIcon(self.theme["memos/memoicon"]))
            self.channelarea.addTopLevelItem(item)

    def updateTheme(self, theme):
        self.theme = theme
        self.setStyleSheet(theme["main/defaultwindow/style"])
        for item in [self.userarea.item(i) for i in range(0, self.channelarea.count())]:
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(theme["main/chums/userlistcolor"])))
            item.setIcon(QtGui.QIcon(theme["memos/memoicon"]))

    @QtCore.pyqtSlot()
    def AcceptIfSelectionMade(self):
        if self.HasSelection():
            self.AcceptSelection()

    @QtCore.pyqtSlot()
    def AcceptSelection(self):
        self.accept()


class LoadingScreen(QtWidgets.QDialog):
    tryAgain = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent, (QtCore.Qt.CustomizeWindowHint |
                                              QtCore.Qt.FramelessWindowHint))
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])

        self.loadinglabel = QtWidgets.QLabel("CONN3CT1NG", self)
        self.cancel = QtWidgets.QPushButton("QU1T >:?", self)
        self.ok = QtWidgets.QPushButton("R3CONN3CT >:]", self)
        # Help reduce the number of accidental Pesterchum closures... :|
        self.cancel.setAutoDefault(False)
        self.ok.setAutoDefault(True)
        self.cancel.clicked.connect(self.reject)
        self.ok.clicked.connect(self.tryAgain)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.loadinglabel)
        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.cancel)
        layout_1.addWidget(self.ok)
        self.layout.addLayout(layout_1)
        self.setLayout(self.layout)
        # Help reduce the number of accidental Pesterchum closures... :|
        self.cancel.setDefault(False)
        self.ok.setDefault(True)
        self.ok.setFocus()
        self.timer = None

    def hideReconnect(self, safe=True):
        self.ok.hide()
        if safe:
            # Set a timer so that we don't immediately disconnect anyway.
            self.cancel.setEnabled(False)
            # A few seconds should be enough.
            self.timer = QtCore.QTimer.singleShot(2000, self.enableQuit)

    def showReconnect(self):
        self.ok.show()
        # Again...stop accidental closes.
        self.ok.setFocus()

    @QtCore.pyqtSlot()
    def enableQuit(self):
        self.cancel.setEnabled(True)

    tryAgain = QtCore.pyqtSignal()

class AboutPesterchum(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])

        self.title = QtWidgets.QLabel("P3ST3RCHUM %s" % (_pcVersion))
        self.credits = QtWidgets.QLabel("Programming by:\n\
  illuminatedwax (ghostDunk)\n\
  Kiooeht (evacipatedBox)\n\
  Lexi (lexicalNuance)\n\
  oakwhiz\n\
  alGore\n\
  Cerxi (binaryCabalist)\n\
  Arcane (arcaneAgilmente)\n\
  karxi (Midna)\n\
  Shou :)\n\
\n\
Art by:\n\
  Grimlive (aquaMarinist)\n\
  Cerxi (binaryCabalist)\n\
\n\
Special Thanks:\n\
  ABT\n\
  gamblingGenocider\n\
  Eco-Mono")

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.clicked.connect(self.reject)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.title)
        layout_0.addWidget(self.credits)
        layout_0.addWidget(self.ok)

        self.setLayout(layout_0)

class UpdatePesterchum(QtWidgets.QDialog):
    def __init__(self, ver, url, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.url = url
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Pesterchum v%s Update" % (ver))
        self.setModal(False)

        self.title = QtWidgets.QLabel("An update to Pesterchum is available!")

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.title)

        self.ok = QtWidgets.QPushButton("D0WNL04D 4ND 1NST4LL N0W", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)

class AddChumDialog(QtWidgets.QDialog):
    def __init__(self, avail_groups, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Enter Chum Handle")
        self.setModal(True)

        self.title = QtWidgets.QLabel("Enter Chum Handle")
        self.chumBox = QtWidgets.QLineEdit(self)
        self.groupBox = QtWidgets.QComboBox(self)
        avail_groups.sort()
        avail_groups.pop(avail_groups.index("Chums"))
        avail_groups.insert(0, "Chums")
        for g in avail_groups:
            self.groupBox.addItem(g)
        self.newgrouplabel = QtWidgets.QLabel("Or make a new group:")
        self.newgroup = QtWidgets.QLineEdit(self)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.title)
        layout_0.addWidget(self.chumBox)
        layout_0.addWidget(self.groupBox)
        layout_0.addWidget(self.newgrouplabel)
        layout_0.addWidget(self.newgroup)

        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)
