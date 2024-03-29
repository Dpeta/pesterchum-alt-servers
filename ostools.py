import os
import sys
import ctypes

try:
    from PyQt6.QtCore import QStandardPaths
except ImportError:
    print("PyQt5 fallback (ostools.py)")
    from PyQt5.QtCore import QStandardPaths

DATADIR = None


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
    themes = os.path.join(datadir, "themes")
    # ~lisanne `datadir/themes` is for repository installed themes
    # Apparently everything checks this folder for themes already
    # So hopefully im not plugging into an existng system on accident

    js_pchum = os.path.join(datadir, "pesterchum.js")
    js_manifest = os.path.join(datadir, "manifest.json")

    dirs = [datadir, profile, quirks, logs, themes, errorlogs, backup]
    for d in dirs:
        if not os.path.isdir(d) or not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    # pesterchum.js
    for filepath in [js_pchum, js_manifest]:
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write("{}")


def getDataDir():
    # Temporary fix for non-ascii usernames
    # If username has non-ascii characters, just store userdata
    # in the Pesterchum install directory (like before)

    if DATADIR is not None:
        # ~Lisanne
        # On some systems (windows known 2b affected, OSX unknown, at least 1 linux distro unaffected)
        # the QStandardPaths.writableLocation changes its return path after the QApplication initialises
        # This means that anytime its called during runtime after init will just return a lie. it will just give you a different path
        # (Because the Application now has a Name which in turn makes it return an application-name-specific writableLocation, which pchum isnt expecting anywhere)
        # so
        # here im caching the result at init & returning that
        # seemed like the safest way to do this without breaking half of this program
        return DATADIR

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


DATADIR = getDataDir()
