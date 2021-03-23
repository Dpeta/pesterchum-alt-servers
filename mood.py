from PyQt5 import QtCore, QtGui, QtWidgets

from generic import PesterIcon

class Mood(object):
    moods = ["chummy", "rancorous", "offline", "pleasant", "distraught",
             "pranky", "smooth", "ecstatic", "relaxed", "discontent",
             "devious", "sleek", "detestful", "mirthful", "manipulative",
             "vigorous", "perky", "acceptant", "protective", "mystified",
             "amazed", "insolent", "bemused" ]
    moodcats = ["chums", "trolls", "other"]
    revmoodcats = {'discontent': 'trolls', 'insolent': 'chums', 'rancorous': 'chums', 'sleek': 'trolls', 'bemused': 'chums', 'mystified': 'chums', 'pranky': 'chums', 'distraught': 'chums', 'offline': 'chums', 'chummy': 'chums', 'protective': 'other', 'vigorous': 'trolls', 'ecstatic': 'trolls', 'relaxed': 'trolls', 'pleasant': 'chums', 'manipulative': 'trolls', 'detestful': 'trolls', 'smooth': 'chums', 'mirthful': 'trolls', 'acceptant': 'trolls', 'perky': 'trolls', 'devious': 'trolls', 'amazed': 'chums'}

    def __init__(self, mood):
        if type(mood) is int:
            self.mood = mood
        else:
            self.mood = self.moods.index(mood)
    def value(self):
        return self.mood
    def name(self):
        try:
            name = self.moods[self.mood]
        except IndexError:
            name = "chummy"
        return name
    def icon(self, theme):
        try:
            f = theme["main/chums/moods"][self.name()]["icon"]
        except KeyError:
            return PesterIcon(theme["main/chums/moods/chummy/icon"])
        return PesterIcon(f)

class PesterMoodAction(QtCore.QObject):
    def __init__(self, m, func):
        QtCore.QObject.__init__(self)
        self.mood = m
        self.func = func
    @QtCore.pyqtSlot()
    def updateMood(self):
        self.func(self.mood)

class PesterMoodHandler(QtCore.QObject):
    def __init__(self, parent, *buttons):
        QtCore.QObject.__init__(self)
        self.buttons = {}
        self.mainwindow = parent
        for b in buttons:
            self.buttons[b.mood.value()] = b
            if b.mood.value() == self.mainwindow.profile().mood.value():
                b.setSelected(True)
            b.clicked.connect(b.updateMood)
            b.moodUpdated[int].connect(self.updateMood)
    def removeButtons(self):
        for b in list(self.buttons.values()):
            b.close()
    def showButtons(self):
        for b in list(self.buttons.values()):
            b.show()
            b.raise_()
    @QtCore.pyqtSlot(int)
    def updateMood(self, m):
        # update MY mood
        oldmood = self.mainwindow.profile().mood
        try:
            oldbutton = self.buttons[oldmood.value()]
            oldbutton.setSelected(False)
        except KeyError:
            pass
        try:
            newbutton = self.buttons[m]
            newbutton.setSelected(True)
        except KeyError:
            pass
        newmood = Mood(m)
        self.mainwindow.userprofile.chat.mood = newmood
        self.mainwindow.userprofile.setLastMood(newmood)
        if self.mainwindow.currentMoodIcon:
            moodicon = newmood.icon(self.mainwindow.theme)
            self.mainwindow.currentMoodIcon.setPixmap(moodicon.pixmap(moodicon.realsize()))
        if oldmood.name() != newmood.name():
            for c in list(self.mainwindow.convos.values()):
                c.myUpdateMood(newmood)
        self.mainwindow.moodUpdated.emit()

class PesterMoodButton(QtWidgets.QPushButton):
    def __init__(self, parent, **options):
        icon = PesterIcon(options["icon"])
        QtWidgets.QPushButton.__init__(self, icon, options["text"], parent)
        self.setIconSize(icon.realsize())
        self.setFlat(True)
        self.resize(*options["size"])
        self.move(*options["loc"])
        self.unselectedSheet = options["style"]
        self.selectedSheet = options["selected"]
        self.setStyleSheet(self.unselectedSheet)
        self.mainwindow = parent
        self.mood = Mood(options["mood"])
    def setSelected(self, selected):
        if selected:
            self.setStyleSheet(self.selectedSheet)
        else:
            self.setStyleSheet(self.unselectedSheet)
    @QtCore.pyqtSlot()
    def updateMood(self):
        # updates OUR mood
        self.moodUpdated.emit(self.mood.value())
    moodUpdated = QtCore.pyqtSignal(int)
