try:
    from PyQt6 import QtCore, QtWidgets
except ImportError:
    print("PyQt5 fallback (mood.py)")
    from PyQt5 import QtCore, QtWidgets

from generic import PesterIcon


class Mood:
    moods = [
        "chummy",
        "rancorous",
        "offline",
        "pleasant",
        "distraught",
        "pranky",
        "smooth",
        "ecstatic",
        "relaxed",
        "discontent",
        "devious",
        "sleek",
        "detestful",
        "mirthful",
        "manipulative",
        "vigorous",
        "perky",
        "acceptant",
        "protective",
        "mystified",
        "amazed",
        "insolent",
        "bemused",
    ]
    moodcats = ["chums", "trolls", "other"]
    revmoodcats = {
        "discontent": "trolls",
        "insolent": "chums",
        "rancorous": "chums",
        "sleek": "trolls",
        "bemused": "chums",
        "mystified": "chums",
        "pranky": "chums",
        "distraught": "chums",
        "offline": "chums",
        "chummy": "chums",
        "protective": "other",
        "vigorous": "trolls",
        "ecstatic": "trolls",
        "relaxed": "trolls",
        "pleasant": "chums",
        "manipulative": "trolls",
        "detestful": "trolls",
        "smooth": "chums",
        "mirthful": "trolls",
        "acceptant": "trolls",
        "perky": "trolls",
        "devious": "trolls",
        "amazed": "chums",
    }

    def __init__(self, mood):
        # self.mood: integer value of the mood
        if isinstance(mood, int):
            self.mood = mood
        else:
            self.mood = self.moods.index(mood)

    def value_str(self):
        """Return mood index as str."""
        return str(self.mood)

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
    def __init__(self, parent, buttons):
        QtCore.QObject.__init__(self)
        self.buttons = {}
        self.mainwindow = parent
        for button in buttons:
            # for each button:
            # map its mood index (IE, 3) to its button object
            self.buttons[button.mood.value()] = button
            # check if the buttons mood is the current users's mood
            if button.mood.value() == self.mainwindow.profile().mood.value():
                # make it selected if yes
                button.setSelected(True)
            # Make clicking the button actually do something
            # (note that the only thing button.updateMood does is emit button.moodUpdated with the button's mood index)
            button.clicked.connect(button.updateMood)
            button.moodUpdated[int].connect(self.updateMood)

    def removeButtons(self):
        for button in list(self.buttons.values()):
            button.close()

    def showButtons(self):
        for button in list(self.buttons.values()):
            button.show()
            button.raise_()

    @QtCore.pyqtSlot(int)
    def updateMood(self, mood_index):
        # update MY mood
        # Currently set, soon to be replaced mood of our user
        oldmood = self.mainwindow.profile().mood

        # Grab previous mood button (if it exists), set it to not be selected anymore
        if oldmood.value() in self.buttons:
            self.buttons[oldmood.value()].setSelected(False)
        # Grab the moodbutton that corrosponds to the new index (if it exists), set it to be selected
        if mood_index in self.buttons:
            self.buttons[mood_index].setSelected(True)

        newmood = Mood(mood_index)
        self.mainwindow.userprofile.chat.mood = (
            newmood  # changes current mood directly (?)
        )
        self.mainwindow.userprofile.setLastMood(
            newmood
        )  # mood saved to the user .js config to be used next time we start up
        if self.mainwindow.currentMoodIcon:
            moodicon = newmood.icon(self.mainwindow.theme)
            self.mainwindow.currentMoodIcon.setPixmap(
                moodicon.pixmap(moodicon.realsize())
            )
        # If the mood value has changed at all
        if oldmood.name() != newmood.name():
            for conversation in list(self.mainwindow.convos.values()):
                conversation.myUpdateMood(newmood)
        self.mainwindow.moodUpdated.emit()  # Global signal to tell the rest of the application our mood changed.
        # why does PesterMoodHandler cause an emit of a signal on mainwindow? who knows.


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
