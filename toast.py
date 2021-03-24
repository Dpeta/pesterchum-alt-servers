import inspect
import threading
import time, os
import ostools
import logging
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    import pynotify
except:
    pynotify = None

class DefaultToast(object):
    def __init__(self, machine, title, msg, icon):
        self.machine = machine
        self.title   = title
        self.msg     = msg
        self.icon    = icon
    def show(self):
        print(self.title, self.msg, self.icon)
        self.done()
    def done(self):
        t = self.machine.toasts[0]
        if t.title == self.title and t.msg == self.msg and t.icon == self.icon:
            self.machine.toasts.pop(0)
            self.machine.displaying = False
            print("Done")

class ToastMachine(object):
    class __Toast__(object):
        def __init__(self, machine, title, msg, time=3000, icon="", importance=0):
            self.machine    = machine
            self.title      = title
            self.msg        = msg
            self.time       = time
            if icon:
                icon = os.path.abspath(icon)
            self.icon       = icon
            self.importance = importance
            if inspect.ismethod(self.title) or inspect.isfunction(self.title):
                self.title = self.title()

        def titleM(self, title=None):
            if title:
                self.title = title
                if inspect.ismethod(self.title) or inspect.isfunction(self.title):
                    self.title = self.title()
            else:     return self.title
        def msgM(self, msg=None):
            if msg:   self.msg = msg
            else:     return self.msg
        def timeM(self, time=None):
            if time:  self.time = time
            else:     return self.time
        def iconM(self, icon=None):
            if icon:  self.icon = icon
            else:     return self.icon
        def importanceM(self, importance=None):
            if importance != None: self.importance = importance
            else:                  return self.importance

        def show(self):
            if self.machine.on:
                # Use libnotify's queue if using libnotify
                if self.machine.type == "libnotify" or self.machine.type == "twmn":
                    self.realShow()
                elif self.machine.toasts:
                    self.machine.toasts.append(self)
                else:
                    self.machine.toasts.append(self)
                    self.realShow()

        def realShow(self):
            self.machine.displaying = True
            t = None
            for (k,v) in self.machine.types.items():
                if self.machine.type == k:
                    try:
                        args = inspect.getargspec(v.__init__).args
                    except:
                        args = []

                    extras = {}
                    if 'parent' in args:
                        extras['parent'] = self.machine.parent
                    if 'time' in args:
                        extras['time'] = self.time
                    if k == "libnotify" or k == "twmn":
                        t = v(self.title, self.msg, self.icon, **extras)
                    else:
                        t = v(self.machine, self.title, self.msg, self.icon, **extras)
                    # Use libnotify's urgency setting
                    if k == "libnotify":
                        if self.importance < 0:
                            t.set_urgency(pynotify.URGENCY_CRITICAL)
                        elif self.importance == 0:
                            t.set_urgency(pynotify.URGENCY_NORMAL)
                        elif self.importance > 0:
                            t.set_urgency(pynotify.URGENCY_LOW)
                    break
            if not t:
                if 'default' in self.machine.types:
                    if 'parent' in inspect.getargspec(self.machine.types['default'].__init__).args:
                        t = self.machine.types['default'](self.machine, self.title, self.msg, self.icon, self.machine.parent)
                    else:
                        t = self.machine.types['default'](self.machine, self.title, self.msg, self.icon)
                else:
                    t = DefaultToast(self.title, self.msg, self.icon)
            t.show()

    def __init__(self, parent, name, on=True, type="default",
                                              types=({'default'  : DefaultToast,
                                                      'libnotify': pynotify.Notification}
                                                      if pynotify else
                                                      {'default' : DefaultToast}),
                                              extras={}):
        self.parent     = parent
        self.name       = name
        self.on         = on
        types.update(extras)
        self.types      = types
        self.type       = "default"
        self.quit       = False
        self.displaying = False

        self.setCurrentType(type)

        self.toasts = []

    def Toast(self, title, msg, icon="", time=3000):
        return self.__Toast__(self, title, msg, time=time, icon=icon)

    def setEnabled(self, on):
        self.on = (on is True)

    def currentType(self):
        return self.type

    def availableTypes(self):
        return sorted(self.types.keys())

    def setCurrentType(self, type):
        if type in self.types:
            if type == "libnotify":
                if not pynotify or not pynotify.init("ToastMachine"):
                    print("Problem initilizing pynotify")
                    return
                    #self.type = type = "default"
            elif type == "twmn":
                import pytwmn
                try:
                    pytwmn.init()
                except pytwmn.ERROR as e:
                    print("Problem initilizing pytwmn: " + str(e))
                    return
                    #self.type = type = "default"
            self.type = type

    def appName(self):
        if inspect.ismethod(self.name) or inspect.isfunction(self.name):
            return self.name()
        else:
            return self.name

    def showNext(self):
        if not self.displaying and self.toasts:
            self.toasts.sort(key=lambda x: x.importance)
            self.toasts[0].realShow()

    def showAll(self):
        while self.toasts:
            self.showNext()

    def run(self):
        while not self.quit:
            if self.on and self.toasts:
                self.showNext()


class PesterToast(QtWidgets.QWidget, DefaultToast):
    def __init__(self, machine, title, msg, icon, time=3000, parent=None):
        logging.info(isinstance(parent, QtWidgets.QWidget))
        kwds = dict(machine=machine, title=title, msg=msg, icon=icon)
        super().__init__(parent, **kwds)

        self.machine = machine
        self.time = time

        if ostools.isWin32():
            self.setWindowFlags(QtCore.Qt.ToolTip)
        else:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.ToolTip)

        self.m_animation = QtCore.QParallelAnimationGroup()
        anim = QtCore.QPropertyAnimation(self)
        anim.setTargetObject(self)
        self.m_animation.addAnimation(anim)
        anim.setEasingCurve(QtCore.QEasingCurve.OutBounce)
        anim.setDuration(1000)
        anim.finished.connect(self.reverseTrigger)

        self.m_animation.setDirection(QtCore.QAnimationGroup.Forward)

        self.title = QtWidgets.QLabel(title, self)
        self.msg = QtWidgets.QLabel(msg, self)
        self.content = msg
        if icon:
            self.icon = QtWidgets.QLabel("")
            self.icon.setPixmap(QtGui.QPixmap(icon).scaledToWidth(30))
        else:
            self.icon = QtWidgets.QLabel("")
            self.icon.setPixmap(QtGui.QPixmap(30, 30))
            self.icon.pixmap().fill(QtGui.QColor(0,0,0,0))

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.setContentsMargins(0, 0, 0, 0)
        layout_0.setContentsMargins(0, 0, 0, 0)

        if self.icon:
            layout_1 = QtWidgets.QGridLayout()
            layout_1.addWidget(self.icon, 0,0, 1,1)
            layout_1.addWidget(self.title, 0,1, 1,7)
            layout_1.setAlignment(self.msg, QtCore.Qt.AlignTop)
            layout_0.addLayout(layout_1)
        else:
            layout_0.addWidget(self.title)
        layout_0.addWidget(self.msg)

        self.setMaximumWidth(self.parent().theme["toasts/width"])
        self.msg.setMaximumWidth(self.parent().theme["toasts/width"])
        self.title.setMinimumHeight(self.parent().theme["toasts/title/minimumheight"])

        self.setLayout(layout_0)

        self.setGeometry(0,0, self.parent().theme["toasts/width"], self.parent().theme["toasts/height"])
        self.setStyleSheet(self.parent().theme["toasts/style"])
        self.title.setStyleSheet(self.parent().theme["toasts/title/style"])
        if self.icon:
            self.icon.setStyleSheet(self.parent().theme["toasts/icon/style"])
        self.msg.setStyleSheet(self.parent().theme["toasts/content/style"])
        self.layout().setSpacing(0)

        self.msg.setText(PesterToast.wrapText(self.msg.font(), str(self.msg.text()), self.parent().theme["toasts/width"], self.parent().theme["toasts/content/style"]))

        p = QtWidgets.QApplication.desktop().availableGeometry(self).bottomRight()
        o = QtWidgets.QApplication.desktop().screenGeometry(self).bottomRight()
        anim.setStartValue(p.y() - o.y())
        anim.setEndValue(100)
        anim.valueChanged[QtCore.QVariant].connect(self.updateBottomLeftAnimation)

        self.byebye = False

    @QtCore.pyqtSlot()
    def show(self):
        self.m_animation.start()

    @QtCore.pyqtSlot()
    def done(self):
        QtWidgets.QWidget.hide(self)
        t = self.machine.toasts[0]
        if t.title == str(self.title.text()) and \
           t.msg == str(self.content):
            self.machine.toasts.pop(0)
            self.machine.displaying = False
        if self.machine.on:
            self.machine.showNext()
        del self

    @QtCore.pyqtSlot()
    def reverseTrigger(self):
        if self.time >= 0:
            QtCore.QTimer.singleShot(self.time, self.reverseStart)

    @QtCore.pyqtSlot()
    def reverseStart(self):
        if not self.byebye:
            self.byebye = True
            anim = self.m_animation.animationAt(0)
            self.m_animation.setDirection(QtCore.QAnimationGroup.Backward)
            anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
            anim.finished.disconnect(self.reverseTrigger)
            anim.finished.connect(self.done)
            self.m_animation.start()

    @QtCore.pyqtSlot(QtCore.QVariant)
    def updateBottomLeftAnimation(self, value):
        p = QtWidgets.QApplication.desktop().availableGeometry(self).bottomRight()
        val = float(self.height())/100
        self.move(p.x()-self.width(), p.y() - (value * val) +1)
        self.layout().setSpacing(0)
        QtWidgets.QWidget.show(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.reverseStart()
        elif event.button() == QtCore.Qt.LeftButton:
            pass

    @staticmethod
    def wrapText(font, text, maxwidth, css=""):
        ret = []
        metric = QtGui.QFontMetrics(font)
        if "padding" in css:
            if css[css.find("padding")+7] != "-":
                colon = css.find(":", css.find("padding"))
                semicolon = css.find(";", css.find("padding"))
                if semicolon < 0:
                    stuff = css[colon+1:]
                else:
                    stuff = css[colon+1:semicolon]
                stuff = stuff.replace("px", "").lstrip().rstrip()
                stuff = stuff.split(" ")
                if len(stuff) == 1:
                    maxwidth -= int(stuff[0])*2
                elif len(stuff) == 2:
                    maxwidth -= int(stuff[1])*2
                elif len(stuff) == 3:
                    maxwidth -= int(stuff[1])*2
                elif len(stuff) == 4:
                    maxwidth -= int(stuff[1]) + int(stuff[3])
            else:
                if "padding-left" in css:
                    colon = css.find(":", css.find("padding-left"))
                    semicolon = css.find(";", css.find("padding-left"))
                    if semicolon < 0:
                        stuff = css[colon+1:]
                    else:
                        stuff = css[colon+1:semicolon]
                    stuff = stuff.replace("px", "").lstrip().rstrip()
                    if stuff.isdigit():
                        maxwidth -= int(stuff)
                if "padding-right" in css:
                    colon = css.find(":", css.find("padding-right"))
                    semicolon = css.find(";", css.find("padding-right"))
                    if semicolon < 0:
                        stuff = css[colon+1:]
                    else:
                        stuff = css[colon+1:semicolon]
                    stuff = stuff.replace("px", "").lstrip().rstrip()
                    if stuff.isdigit():
                        maxwidth -= int(stuff)

        if metric.width(text) < maxwidth:
            return text
        while metric.width(text) > maxwidth:
            lastspace = text.find(" ")
            curspace = lastspace
            while metric.width(text, curspace) < maxwidth:
                lastspace = curspace
                curspace = text.find(" ", lastspace+1)
                if curspace == -1:
                    break
            if (metric.width(text[:lastspace]) > maxwidth) or \
               len(text[:lastspace]) < 1:
                for i in range(len(text)):
                    if metric.width(text[:i]) > maxwidth:
                        lastspace = i-1
                        break
            ret.append(text[:lastspace])
            text = text[lastspace+1:]
        ret.append(text)
        return "\n".join(ret)


class PesterToastMachine(ToastMachine, QtCore.QObject):
    def __init__(self, parent, name, on=True, type="default",
                 types=({'default'  : DefaultToast,
                        'libnotify' : pynotify.Notification}
                        if pynotify else
                        {'default' : DefaultToast}),
                 extras={}):
        ToastMachine.__init__(self, parent, name, on, type, types, extras)
        QtCore.QObject.__init__(self, parent)

    def setEnabled(self, on):
        oldon = self.on
        ToastMachine.setEnabled(self, on)
        if oldon != self.on:
            self.parent.config.set('notify', self.on)
            if self.on:
                self.timer.start()
            else:
                self.timer.stop()

    def setCurrentType(self, type):
        oldtype = self.type
        ToastMachine.setCurrentType(self, type)
        if oldtype != self.type:
            self.parent.config.set('notifyType', self.type)

    @QtCore.pyqtSlot()
    def showNext(self):
        ToastMachine.showNext(self)

    def run(self):
        pass
        #~ self.timer = QtCore.QTimer(self)
        #~ self.timer.setInterval(1000)
        #~ self.connect(self.timer, QtCore.SIGNAL('timeout()'),
                     #~ self, QtCore.SLOT('showNext()'))
        #~ if self.on:
            #~ self.timer.start()
