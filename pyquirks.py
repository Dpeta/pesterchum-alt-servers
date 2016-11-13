import os, sys, imp, re, ostools
from quirks import ScriptQuirks
from PyQt5 import QtGui, QtCore, QtWidgets

class PythonQuirks(ScriptQuirks):
    def loadModule(self, name, filename):
        return imp.load_source(name, filename)

    def getExtension(self):
        return '.py'

    def modHas(self, module, attr):
        if attr == 'commands':
            variables = vars(module)
            for name, obj in variables.iteritems():
                if self.modHas(obj, 'command'):
                    return True
        return hasattr(module, attr)

    def register(self, module):
        variables = vars(module)
        for name, obj in variables.iteritems():
            if self.modHas(obj, 'command'):
                try:
                    if not isinstance(obj("test"), basestring):
                        raise Exception
                except:
                    print "Quirk malformed: %s" % (obj.command)
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Error!")
                    msgbox.setText("Quirk malformed: %s" % (obj.command))
                    msgbox.exec_()
                else:
                    self.quirks[obj.command] = obj

