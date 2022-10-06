import logging
import importlib.util

try:
    from PyQt6 import QtWidgets
except ImportError:
    print("PyQt5 fallback (pyquirks.py)")
    from PyQt5 import QtWidgets

import ostools
from quirks import ScriptQuirks

PchumLog = logging.getLogger("pchumLogger")


class PythonQuirks(ScriptQuirks):
    def loadModule(self, name, filename):
        # imp is deprecated since Python 3.4
        # return imp.load_source(name, filename)

        spec = importlib.util.spec_from_file_location(name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def getExtension(self):
        return ".py"

    def modHas(self, module, attr):
        if attr == "commands":
            variables = vars(module)
            for name, obj in variables.items():
                if self.modHas(obj, "command"):
                    return True
        return hasattr(module, attr)

    def register(self, module):
        variables = vars(module)
        for name, obj in variables.items():
            if self.modHas(obj, "command"):
                try:
                    if not isinstance(obj("test"), str):
                        raise Exception
                except:
                    # print("Quirk malformed: %s" % (obj.command))
                    PchumLog.error("Quirk malformed: %s" % (obj.command))

                    # Since this is executed before QApplication is constructed,
                    # This prevented pesterchum from starting entirely when a quirk was malformed :/
                    # (QWidget: Must construct a QApplication before a QWidget)

                    if QtWidgets.QApplication.instance() != None:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Error!")
                        msgbox.setText("Quirk malformed: %s" % (obj.command))
                        msgbox.exec()
                else:
                    self.quirks[obj.command] = obj
