"""
Okay so, this definitely doesn't work in its current state-
Probably broke when transitioning to Python 3? Might've been broken for longer-
Hard for me to work on this since I know absolutely nothing about lua, plus I'm not sure what 'lua' library this was originally supposed to work with.
 + I asked and there doesn't seem to be a single person who actually used this 💀

import logging
import logging.config
import os
import sys
import re

from PyQt6 import QtCore, QtGui, QtWidgets

import ostools
from quirks import ScriptQuirks

_datadir = ostools.getDataDir()
logging.config.fileConfig(_datadir + "logging.ini")
PchumLog = logging.getLogger('pchumLogger')

try:
    try:
        import lua
    except ImportError:
        import lupa
        from lupa import LuaRuntime
        
    lua = LuaRuntime(unpack_returned_tuples=True)
    PchumLog.info("Lua \"successfully\" imported.")
except ImportError as e:
    PchumLog.warning("No lua library. " + str(e))
    lua = None

class LuaQuirks(ScriptQuirks):
    def loadModule(self, name, filename):
        if lua is None:
            return None

        lua.globals().package.loaded[name] = None

        CurrentDir = os.getcwd()
        os.chdir('quirks')

        lua.globals().package.path = filename.replace(name+".lua", "?.lua")

        try:
            return lua.require(name)
        except Exception as e:
            PchumLog.warning(e)
            return None
        finally:
            os.chdir(CurrentDir)

    def getExtension(self):
        return '.lua'

    def modHas(self, module, attr):
        return attr in module

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
                except Exception as e:
                    PchumLog.warning(e)
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
                PchumLog.error("Quirk malformed: %s" % (name))
                
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
"""
