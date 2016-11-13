from PyQt5 import QtGui, QtCore, QtWidgets
import urllib
import ostools
import version

class BugReporter(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.mainwindow = parent
        self.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
        self.setWindowTitle("Report a Bug")
        self.setModal(False)

        self.title = QtWidgets.QLabel("Bug Report:")

        layout_0 = QtWidgets.QVBoxLayout()
        layout_0.addWidget(self.title)

        layout_0.addWidget(QtWidgets.QLabel("Chumhandle:"))
        handleLabel = QtWidgets.QLabel("The best chumhandle to contact you at for further information.")
        font = handleLabel.font()
        font.setPointSize(8)
        handleLabel.setFont(font)
        layout_0.addWidget(handleLabel)
        self.name = QtWidgets.QLineEdit(self)
        self.name.setStyleSheet("background:white; font-weight:bold; color:black; font-size: 10pt;")
        layout_0.addWidget(self.name)

        layout_0.addWidget(QtWidgets.QLabel("Description of bug:"))
        descLabel = QtWidgets.QLabel("Include as much information as possible\n(theme, related options, what you were doing at the time, etc.)")
        font = descLabel.font()
        font.setPointSize(8)
        descLabel.setFont(font)
        layout_0.addWidget(descLabel)

        self.textarea = QtWidgets.QTextEdit(self)
        self.textarea.setStyleSheet("background:white; font-weight:normal; color:black; font-size: 10pt;")

        layout_0.addWidget(self.textarea)

        self.ok = QtWidgets.QPushButton("SEND", self, clicked=self.sendReport)
        self.ok.setDefault(True)
        self.cancel = QtWidgets.QPushButton("CANCEL", self, clicked=self.reject)
        layout_2 = QtWidgets.QHBoxLayout()
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
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet(self.mainwindow.theme["main/defaultwindow/style"])
            msgbox.setText("You must fill out all fields first!")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            ret = msgbox.exec_()
            return

        QtWidgets.QDialog.accept(self)
        data = urllib.urlencode({"name":name, "version": version._pcVersion, "bestname":bestname, "os":os, "platform":full, "python":python, "qt":qt, "msg":msg})
        print "Sending..."
        f = urllib.urlopen("http://distantsphere.com/pc/reporter.php", data)
        text = f.read()
        print text
        if text == "success!":
            print "Sent!"
        else:
            print "Problems ):"

