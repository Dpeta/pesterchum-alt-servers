import os
import sys
import imp
import re
import logging
import logging.config

from PyQt5 import QtCore, QtGui, QtWidgets

import ostools
from quirks import ScriptQuirks

_datadir = ostools.getDataDir()
logging.config.fileConfig(_datadir + "logging.ini")
PchumLog = logging.getLogger('pchumLogger')

class PythonQuirks(ScriptQuirks):
    def loadModule(self, name, filename):
        return imp.load_source(name, filename)

    def getExtension(self):
        return '.py'

    def modHas(self, module, attr):
        if attr == 'commands':
            variables = vars(module)
            for name, obj in variables.items():
                if self.modHas(obj, 'command'):
                    return True
        return hasattr(module, attr)

    def register(self, module):
        variables = vars(module)
        for name, obj in variables.items():
            if self.modHas(obj, 'command'):
                try:
                    if not isinstance(obj("test"), str):
                        raise Exception
                except:
                    #print("Quirk malformed: %s" % (obj.command))
                    PchumLog.error("Quirk malformed: %s" % (obj.command))

                    # Since this is executed before QApplication is constructed,
                    # This prevented pesterchum from starting entirely when a quirk was malformed :/
                    # (QWidget: Must construct a QApplication before a QWidget)
                    
                    if QtWidgets.QApplication.instance() != None:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Error!")
                        msgbox.setText("Quirk malformed: %s" % (obj.command))
                        msgbox.exec_()
                else:
                    self.quirks[obj.command] = obj

