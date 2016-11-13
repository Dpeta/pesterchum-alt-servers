from PyQt4 import QtGui, QtCore

RANDNICK = "randomEncounter"

class RandomHandler(QtCore.QObject):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.randNick = RANDNICK
        self.mainwindow = parent
        self.queue = []
        self.running = False

    def setRunning(self, on):
        self.running = on
        self.mainwindow.rand.setEnabled(on)

    def getRandomer(self):
        self.queue.append("?")
        self.mainwindow.sendNotice.emit("?", self.randNick)

    def setRandomer(self, r):
        if r != self.mainwindow.userprofile.getRandom():
            if r: code = "+"
            else: code = "-"
            self.queue.append(code)
            self.mainwindow.sendNotice.emit(code, self.randNick)

    def setIdle(self, i):
        if i: code = "~"
        else: code = "*"
        self.queue.append(code)
        self.mainwindow.sendNotice.emit(code, self.randNick)

    @QtCore.pyqtSlot()
    def getEncounter(self):
        self.queue.append("!")
        self.mainwindow.sendNotice.emit("!", self.randNick)

    def incoming(self, msg):
        l = msg.split("=")
        code = l[0][0]
        if code not in self.queue:
            return # Ignore if we didn't request this
        self.queue.remove(code)
        if code == "?":
            if l[1][0] == "y":
                self.mainwindow.userprofile.setRandom(True)
            elif l[1][0] == "n":
                self.mainwindow.userprofile.setRandom(False)
        elif code in ["+","-"]:
            if l[1][0] == "k":
                if code == "+":
                    self.mainwindow.userprofile.setRandom(True)
                else:
                    self.mainwindow.userprofile.setRandom(False)
        elif code in ["~","*"]:
            if l[1][0] == "k":
                pass
        elif code == "!":
            if l[1] == "x":
                from PyQt4 import QtGui
                msgbox = QtGui.QMessageBox()
                msgbox.setText("Unable to fetch you a random encounter!")
                msgbox.setInformativeText("Try again later :(")
                msgbox.exec_()
                return
            name = unicode(l[1])
            print name
            self.mainwindow.newConversation(name)
