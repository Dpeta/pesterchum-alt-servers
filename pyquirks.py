import os
import logging
import importlib.util

try:
    from PyQt6 import QtWidgets
except ImportError:
    print("PyQt5 fallback (pyquirks.py)")
    from PyQt5 import QtWidgets

import ostools

# from quirks import ScriptQuirks

PchumLog = logging.getLogger("pchumLogger")


# python-based runtime-imported quirk stuff


class ScriptQuirks:
    def __init__(self):
        self._datadir = ostools.getDataDir()
        self.home = os.getcwd()
        self.quirks = {}
        self.last = {}
        self.scripts = []
        # self.load()

    def loadModule(self, name, filename):
        raise Exception

    def modHas(self, module, attr):
        return False

    def loadAll(self):
        self.last = self.quirks.copy()
        self.quirks.clear()
        for script in self.scripts:
            PchumLog.info(script.getExtension())
            script.load()
            # print script.quirks
            for q in script.quirks:
                self.quirks.update(script.quirks)
        for k in self.last:
            if k in self.quirks:
                if self.last[k] == self.quirks[k]:
                    del self.quirks[k]
        # print self.quirks
        if hasattr(self, "quirks"):
            # See https://stackoverflow.com/questions/12843099/python-logging-typeerror-not-all-arguments-converted-during-string-formatting
            reg_quirks = ("Registered quirks:", "(), ".join(self.quirks) + "()")
            PchumLog.info(reg_quirks)
        else:
            PchumLog.warning("Couldn't find any script quirks")

    def add(self, script):
        self.scripts.append(script)

    def load(self):
        self.last = self.quirks.copy()
        self.quirks.clear()
        try:
            extension = self.getExtension()
        except AttributeError:
            PchumLog.exception(
                "No self.getExtension(), does ScriptQuirks need to be subclassed?"
            )
            return
        filenames = []
        if not os.path.exists(os.path.join(self.home, "quirks")):
            os.makedirs(os.path.join(self.home, "quirks"), exist_ok=True)
        for fn in os.listdir(os.path.join(self.home, "quirks")):
            if fn.endswith(extension) and not fn.startswith("_"):
                filenames.append(os.path.join(self.home, "quirks", fn))
        if hasattr(self, "_datadir"):
            if not os.path.exists(os.path.join(self._datadir, "quirks")):
                os.makedirs(os.path.join(self._datadir, "quirks"), exist_ok=True)
            for fn in os.listdir(os.path.join(self._datadir, "quirks")):
                if fn.endswith(extension) and not fn.startswith("_"):
                    filenames.append(os.path.join(self._datadir, "quirks", fn))

        modules = []
        for filename in filenames:
            try:
                extension_length = len(self.getExtension())
            except AttributeError:
                PchumLog.exception(
                    "No self.getExtension(), does ScriptQuirks need to be subclassed?"
                )
                return
            name = os.path.basename(filename)[:-extension_length]
            try:
                module = self.loadModule(name, filename)
                if module is None:
                    continue
            except Exception as e:
                PchumLog.warning(
                    "Error loading %s: %s (in quirks.py)", os.path.basename(name), e
                )
            else:
                if self.modHas(module, "setup"):
                    module.setup()
                if self.modHas(module, "commands"):
                    self.register(module)
                modules.append(name)
        for k in self.last:
            if k in self.quirks:
                if self.last[k] == self.quirks[k]:
                    del self.quirks[k]

    def funcre(self):
        if not hasattr(self, "quirks"):
            return r"\\[0-9]+"
        f = r"("
        for q in self.quirks:
            f = f + q + r"\(|"
        f = f + r"\)|\\[0-9]+)"
        return f


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
                    PchumLog.error("Quirk malformed: %s", obj.command)

                    # Since this is executed before QApplication is constructed,
                    # This prevented pesterchum from starting entirely when a quirk was malformed :/
                    # (QWidget: Must construct a QApplication before a QWidget)

                    if QtWidgets.QApplication.instance() is not None:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Error!")
                        msgbox.setText("Quirk malformed: %s" % (obj.command))
                        msgbox.exec()
                else:
                    self.quirks[obj.command] = obj
