import os, sys, re, ostools
from PyQt4 import QtGui, QtCore

class ScriptQuirks(object):
    def __init__(self):
        self._datadir = ostools.getDataDir()
        self.home = os.getcwd()
        self.quirks = {}
        self.last = {}
        self.scripts = []
        #self.load()

    def loadModule(self, name, filename):
        raise Exception

    def modHas(self, module, attr):
        return False

    def loadAll(self):
        self.last = self.quirks.copy()
        self.quirks.clear()
        for script in self.scripts:
            print script.getExtension()
            script.load()
            #print script.quirks
            for q in script.quirks:
                self.quirks.update(script.quirks)
        for k in self.last:
            if k in self.quirks:
                if self.last[k] == self.quirks[k]:
                    del self.quirks[k]
        #print self.quirks
        if self.quirks:
            print 'Registered quirks:', '(), '.join(self.quirks) + "()"
        else:
            print "Warning: Couldn't find any script quirks"

    def add(self, script):
        self.scripts.append(script)

    def load(self):
        self.last = self.quirks.copy()
        self.quirks.clear()
        extension = self.getExtension()
        filenames = []
        if not os.path.exists(os.path.join(self.home, 'quirks')):
            os.mkdir(os.path.join(self.home, 'quirks'))
        for fn in os.listdir(os.path.join(self.home, 'quirks')):
            if fn.endswith(extension) and not fn.startswith('_'):
                filenames.append(os.path.join(self.home, 'quirks', fn))
        if self._datadir:
            if not os.path.exists(os.path.join(self._datadir, 'quirks')):
                os.mkdir(os.path.join(self._datadir, 'quirks'))
            for fn in os.listdir(os.path.join(self._datadir, 'quirks')):
                if fn.endswith(extension) and not fn.startswith('_'):
                    filenames.append(os.path.join(self._datadir, 'quirks', fn))


        modules = []
        for filename in filenames:
            extension_length = len(self.getExtension())
            name = os.path.basename(filename)[:-extension_length]
            try:
                module = self.loadModule(name, filename)
                if module is None:
                    continue
            except Exception as e:
                print "Error loading %s: %s (in quirks.py)" % (os.path.basename(name), e)
                msgbox = QtGui.QMessageBox()
                msgbox.setWindowTitle("Error!")
                msgbox.setText("Error loading %s: %s (in quirks.py)" % (os.path.basename(filename), e))
                msgbox.exec_()
            else:
                if self.modHas(module, 'setup'):
                    module.setup()
                if self.modHas(module, 'commands'):
                    self.register(module)
                modules.append(name)
        for k in self.last:
            if k in self.quirks:
                if self.last[k] == self.quirks[k]:
                    del self.quirks[k]

    def funcre(self):
        if not self.quirks:
            return r"\\[0-9]+"
        f = r"("
        for q in self.quirks:
            f = f + q+r"\(|"
        f = f + r"\)|\\[0-9]+)"
        return f
