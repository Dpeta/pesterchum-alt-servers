try:
    from PyQt6 import QtGui, QtWidgets
except ImportError:
    print("PyQt5 fallback (generic.py)")
    from PyQt5 import QtGui, QtWidgets
from datetime import timedelta


class mysteryTime(timedelta):
    def __sub__(self, other):
        return self

    def __eq__(self, other):
        return type(other) is mysteryTime

    def __neq__(self, other):
        return type(other) is not mysteryTime


class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def has_key(self, key):
        return key.lower() in super()

    def __delitem__(self, key):
        super().__delitem__(key.lower())


class PesterList(list):
    def __init__(self, l):
        self.extend(l)


class PesterIcon(QtGui.QIcon):
    def __init__(self, *x):
        super().__init__(x[0])
        if type(x[0]) in [str, str]:
            self.icon_pixmap = QtGui.QPixmap(x[0])
        else:
            self.icon_pixmap = None

    def realsize(self):
        if self.icon_pixmap:
            return self.icon_pixmap.size()
        else:
            try:
                return self.availableSizes()[0]
            except IndexError:
                return None


class RightClickList(QtWidgets.QListWidget):
    def contextMenuEvent(self, event):
        # fuckin Qt <--- I feel that </3
        if event.reason() == QtGui.QContextMenuEvent.Reason.Mouse:
            listing = self.itemAt(event.pos())
            self.setCurrentItem(listing)
            optionsMenu = self.getOptionsMenu()
            if optionsMenu:
                optionsMenu.popup(event.globalPos())

    def getOptionsMenu(self):
        return self.optionsMenu


class RightClickTree(QtWidgets.QTreeWidget):
    def contextMenuEvent(self, event):
        if event.reason() == QtGui.QContextMenuEvent.Reason.Mouse:
            listing = self.itemAt(event.pos())
            self.setCurrentItem(listing)
            optionsMenu = self.getOptionsMenu()
            if optionsMenu:
                optionsMenu.popup(event.globalPos())

    def getOptionsMenu(self):
        return self.optionsMenu


class MultiTextDialog(QtWidgets.QDialog):
    def __init__(self, title, parent, *queries):
        super().__init__(parent)
        self.setWindowTitle(title)
        if len(queries) == 0:
            return
        self.inputs = {}
        layout_1 = QtWidgets.QHBoxLayout()
        for d in queries:
            label = d["label"]
            inputname = d["inputname"]
            value = d.get("value", "")
            l = QtWidgets.QLabel(label, self)
            layout_1.addWidget(l)
            self.inputs[inputname] = QtWidgets.QLineEdit(value, self)
            layout_1.addWidget(self.inputs[inputname])
        self.ok = QtWidgets.QPushButton("OK", self)
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.accept)
        self.cancel = QtWidgets.QPushButton("CANCEL", self)
        self.cancel.clicked.connect(self.reject)
        layout_ok = QtWidgets.QHBoxLayout()
        layout_ok.addWidget(self.cancel)
        layout_ok.addWidget(self.ok)

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addLayout(layout_1)
        layout_0.addLayout(layout_ok)

        self.setLayout(layout_0)

    def getText(self):
        r = self.exec()
        if r == QtWidgets.QDialog.DialogCode.Accepted:
            retval = {}
            for name, widget in self.inputs.items():
                retval[name] = str(widget.text())
            return retval
        else:
            return None


class MovingWindow(QtWidgets.QFrame):
    # Qt supports starting a system-specific move operation since 5.15, so we shouldn't need to manually set position like this anymore.
    # https://doc.qt.io/qt-5/qwindow.html#startSystemMove
    # This is also the only method that works on Wayland, which doesn't support setting position.
    def __init__(self, *x, **y):
        super().__init__(*x, **y)
        self.moving = None
        self.moveupdate = 0

    def mouseMoveEvent(self, event):
        if self.moving:
            move = event.globalPos() - self.moving
            self.move(move)
            self.moveupdate += 1
            if self.moveupdate > 5:
                self.moveupdate = 0
                self.update()

    def mousePressEvent(self, event):
        # Assuming everything is supported, we only need this function to call "self.windowHandle().startSystemMove()".
        # If not supported, startSystemMove() returns False and the legacy code runs anyway.
        try:
            if self.windowHandle().startSystemMove() != True:
                if event.button() == 1:
                    self.moving = event.globalPos() - self.pos()
        except AttributeError as e:
            print("PyQt <= 5.14?")
            print(str(e))
            if event.button() == 1:
                self.moving = event.globalPos() - self.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.update()
            self.moving = None


class NoneSound:
    def __init__(self, *args, **kwargs):
        pass

    def play(self):
        pass

    def setVolume(self, v):
        pass

    def set_volume(self, v):
        pass


class WMButton(QtWidgets.QPushButton):
    def __init__(self, icon, parent=None):
        super().__init__(icon, "", parent)
        self.setIconSize(icon.realsize())
        self.resize(icon.realsize())
        self.setFlat(True)
        self.setStyleSheet("QPushButton { padding: 0px; }")
        self.setAutoDefault(False)
