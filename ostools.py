import os
import sys
import platform

from PyQt6.QtCore import QStandardPaths

def isOSX():
    return sys.platform == "darwin"

def isWin32():
    return sys.platform == "win32"

def isLinux():
    return sys.platform.startswith("linux")

def isOSXBundle():
    return isOSX() and (os.path.abspath('.').find(".app") != -1)

def isOSXLeopard():
    return isOSX() and platform.mac_ver()[0].startswith("10.5")

def osVer():
    if isWin32():
        return " ".join(platform.win32_ver())
    elif isOSX():
        ver = platform.mac_ver();
        return " ".join((ver[0], " (", ver[2], ")"))
    elif isLinux():
        return " ".join(platform.linux_distribution())

def getDataDir():
    # Temporary fix for non-ascii usernames
    # If username has non-ascii characters, just store userdata
    # in the Pesterchum install directory (like before)
    try:
        if isOSX():
            return os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DataLocation), "Pesterchum/")
        elif isLinux():
            return os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation), ".pesterchum/")
        else:
            return os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DataLocation), "pesterchum/")
    except UnicodeDecodeError:
        return ''
