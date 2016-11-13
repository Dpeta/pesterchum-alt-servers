from PyQt4 import QtGui, QtCore
import urllib
import ostools
import version

class BugReporter(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Report a Bug")
        self.setModal(False)

        self.title = QtGui.QLabel("Bug Report:")

        layout_0 = QtGui.QVBoxLayout()
        layout_0.addWidget(self.title)

        layout_0.addWidget(QtGui.QLabel("Chumhandle:"))
        handleLabel = QtGui.QLabel("The best chumhandle to contact you at for further information.")
        font = handleLabel.font()
        font.setPointSize(8)
        handleLabel.setFont(font)
        layout_0.addWidget(handleLabel)
        self.name = QtGui.QLineEdit(self)
        self.name.setStyleSheet("background:white; font-weight:bold; color:black; font-size: 10pt;")
        layout_0.addWidget(self.name)

        layout_0.addWidget(QtGui.QLabel("Description of bug:"))
        descLabel = QtGui.QLabel("Include as much information as possible\n(theme, related options, what you were doing at the time, etc.)")
        font = descLabel.font()
        font.setPointSize(8)
        descLabel.setFont(font)
        layout_0.addWidget(descLabel)

        self.textarea = QtGui.QTextEdit(self)
        self.textarea.setStyleSheet("background:white; font-weight:normal; color:black; font-size: 10pt;")

        layout_0.addWidget(self.textarea)

        self.ok = QtGui.QPushButton("SEND", self)
        self.ok.setDefault(True)
        self.connect(self.ok, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('sendReport()'))
        self.cancel = QtGui.QPushButton("CANCEL", self)
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))
        layout_2 = QtGui.QHBoxLayout()
        layout_2.addWidget(self.cancel)
        layout_2.addWidget(self.ok)

        layout_0.addLayout(layout_2)

        self.setLayout(layout_0)

    @QtCore.pyqtSlot()
    def sendReport(self):
        name = unicode(self.mainwindow.profile().handle)
        bestname = unicode(self.name.text())
        os = ostools.osVer()
        full = ostools.platform.platform()
        python = ostools.platform.python_version()
        qt = QtCore.qVersion()
        msg = unicode(self.textarea.toPlainText())

        if len(bestname) <= 0 or len(msg) <= 0:
            msgbox = QtGui.QMessageBox()
            msgbox.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
            msgbox.setText("You must fill out all fields first!")
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            ret = msgbox.exec_()
            return

        QtGui.QDialog.accept(self)
        data = urllib.urlencode({"name":name, "version": version._pcVersion, "bestname":bestname, "os":os, "platform":full, "python":python, "qt":qt, "msg":msg})
        print "Sending..."
        f = urllib.urlopen("http://distantsphere.com/pc/reporter.php", data)
        text = f.read()
        print text
        if text == "success!":
            print "Sent!"
        else:
            print "Problems ):"

