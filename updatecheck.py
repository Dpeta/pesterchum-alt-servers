# Adapted from Eco-Mono's F5Stuck RSS Client

from libs import feedparser
import pickle
import os
import threading
from time import mktime
from PyQt5 import QtCore, QtGui, QtWidgets

class MSPAChecker(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.mainwindow = parent
        self.refreshRate = 30 # seconds
        self.status = None
        self.lock = False
        self.timer = QtCore.QTimer(self, timeout=self.check_site_wrapper)
        self.timer.start(1000*self.refreshRate)

    def save_state(self):
        try:
            current_status = open("status_new.pkl","w")
            pickle.dump(self.status, current_status)
            current_status.close()
            try:
              os.rename("status.pkl","status_old.pkl")
            except:
                pass
            try:
                os.rename("status_new.pkl","status.pkl")
            except:
                if os.path.exists("status_old.pkl"):
                    os.rename("status_old.pkl","status.pkl")
                raise
            if os.path.exists("status_old.pkl"):
                os.remove("status_old.pkl")
        except Exception, e:
            print e
            msg = QtWidgets.QMessageBox(self)
            msg.setText("Problems writing save file.")
            msg.show()

    @QtCore.pyqtSlot()
    def check_site_wrapper(self):
        if not self.mainwindow.config.checkMSPA():
            return
        if self.lock:
            return
        print "Checking MSPA updates..."
        s = threading.Thread(target=self.check_site)
        s.start()

    def check_site(self):
        rss = None
        must_save = False
        try:
            self.lock = True
            rss = feedparser.parse("http://www.mspaintadventures.com/rss/rss.xml")
        except:
            return
        finally:
            self.lock = False
        if len(rss.entries) == 0:
            return
        entries = sorted(rss.entries,key=(lambda x: mktime(x.updated_parsed)))
        if self.status == None:
            self.status = {}
            self.status['last_visited'] = {'pubdate':mktime(entries[-1].updated_parsed),'link':entries[-1].link}
            self.status['last_seen'] = {'pubdate':mktime(entries[-1].updated_parsed),'link':entries[-1].link}
            must_save = True
        elif mktime(entries[-1].updated_parsed) > self.status['last_seen']['pubdate']:
            #This is the first time the app itself has noticed this update.
            self.status['last_seen'] = {'pubdate':mktime(entries[-1].updated_parsed),'link':entries[-1].link}
            must_save = True
        if self.status['last_seen']['pubdate'] > self.status['last_visited']['pubdate']:
            if not hasattr(self, "mspa"):
                self.mspa = None
            if not self.mspa:
                self.mspa = MSPAUpdateWindow(self.parent())
                self.mspa.accepted.connect(self.visit_site)
                self.mspa.rejected.connect(self.nothing)
                self.mspa.show()
        else:
            #print "No new updates :("
            pass
        if must_save:
            self.save_state()

    @QtCore.pyqtSlot()
    def visit_site(self):
        print self.status['last_visited']['link']
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.status['last_visited']['link'], QtCore.QUrl.TolerantMode))
        if self.status['last_seen']['pubdate'] > self.status['last_visited']['pubdate']:
            #Visited for the first time. Untrip the icon and remember that we saw it.
            self.status['last_visited'] = self.status['last_seen']
            self.save_state()
        self.mspa = None
    @QtCore.pyqtSlot()
    def nothing(self):
        self.mspa = None

class MSPAUpdateWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("MSPA Update!")
        self.setModal(False)

        self.title = QtWidgets.QLabel("You have an unread MSPA update! :o)")

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.title)

        self.ok = QtWidgets.QPushButton("GO READ NOW!", self, clicked=self.accept)
        self.ok.setDefault(True)
        self.cancel = QtWidgets.QPushButton("LATER", self, clicked=self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)
