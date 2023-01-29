import os
import sys
import ctypes

try:
    from PyQt6.QtCore import QStandardPaths
except ImportError:
    print("PyQt5 fallback (ostools.py)")
    from PyQt5.QtCore import QStandardPaths


def isOSX():
    return sys.platform == "darwin"


def isWin32():
    return sys.platform == "win32"


def isLinux():
    return sys.platform.startswith("linux")


def isOSXBundle():
    return isOSX() and (os.path.abspath(".").find(".app") != -1)


def isRoot():
    """Return True if running as root on Linux/Mac/Misc"""
    if hasattr(os, "getuid"):
        return not os.getuid()  # 0 if root
    return False


def isAdmin():
    """Return True if running as Admin on Windows."""
    try:
        if isWin32():
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except OSError as win_issue:
        print(win_issue)
    return False


def validateDataDir():
    """Checks if data directory is present"""
    # Define paths
    datadir = getDataDir()
    profile = os.path.join(datadir, "profiles")
    quirks = os.path.join(datadir, "quirks")
    logs = os.path.join(datadir, "logs")
    errorlogs = os.path.join(datadir, "errorlogs")
    backup = os.path.join(datadir, "backup")
    js_pchum = os.path.join(datadir, "pesterchum.js")

    dirs = [datadir, profile, quirks, logs, errorlogs, backup]
    for d in dirs:
        if (os.path.isdir(d) == False) or (os.path.exists(d) == False):
            os.makedirs(d, exist_ok=True)

    # pesterchum.js
    if not os.path.exists(js_pchum):
        with open(js_pchum, "w") as f:
            f.write("{}")


def getDataDir():
    # Temporary fix for non-ascii usernames
    # If username has non-ascii characters, just store userdata
    # in the Pesterchum install directory (like before)
    try:
        if isOSX():
            return os.path.join(
                QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.AppLocalDataLocation
                ),
                "Pesterchum/",
            )
        elif isLinux():
            return os.path.join(
                QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.HomeLocation
                ),
                ".pesterchum/",
            )
        else:
            return os.path.join(
                QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.AppLocalDataLocation
                ),
                "pesterchum/",
            )
    except UnicodeDecodeError as e:
        print(e)
        return ""
