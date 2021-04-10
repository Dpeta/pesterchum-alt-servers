import os, sys, re, ostools, logging
try:
    import lua
except ImportError:
    lua = None
from quirks import ScriptQuirks
from PyQt5 import QtCore, QtGui, QtWidgets

class LuaQuirks(ScriptQuirks):
    def loadModule(self, name, filename):
        if lua is None:
            return None

        lua.globals().package.loaded[name] = None

        CurrentDir = os.getcwd()
        os.chdir('quirks')
        try:
            return lua.require(name)
        except Error as e:
            logging.error(e)
            return None
        finally:
            os.chdir(CurrentDir)

    def getExtension(self):
        return '.lua'

    def modHas(self, module, attr):
        return module[attr] is not None

    def register(self, module):
        class Wrapper(object):
            def __init__(self, module, name):
                self.module = module
                self.name = name

            def __call__(self, text):
                CurrentDir = os.getcwd()
                os.chdir('quirks')
                try:
                    return self.module.commands[self.name](lua.globals().tostring(text))
                except:
                    return None
                finally:
                    os.chdir(CurrentDir)

        for name in module.commands:
            CommandWrapper = Wrapper(module,name)
            try:
                if not isinstance(CommandWrapper("test"), str):
                    raise Exception
            except:
                #print("Quirk malformed: %s" % (name))
                logging.error("Quirk malformed: %s" % (name))
                
                # Since this is executed before QApplication is constructed,
                # This prevented pesterchum from starting entirely when a quirk was malformed :/
                # (QWidget: Must construct a QApplication before a QWidget)
                    
                if QtWidgets.QApplication.instance() != None:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Error!")
                    msgbox.setText("Quirk malformed: %s" % (name))
                    msgbox.exec_()
            else:
                self.quirks[name] = CommandWrapper

