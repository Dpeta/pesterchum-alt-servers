# Windows-only cx_freeze setup file
from cx_Freeze import *
import sys

from version import buildVersion

if sys.version_info < (3, 0, 0):
    sys.exit("Python versions lower than 3 are not supported.")

def is_64bit() -> bool:
    return sys.maxsize > 2**32

#if sys.platform == "win32":
base = "Win32GUI"
#else:
#    sys.exit("This script won't work on this platform </3")

includefiles = ["quirks",
                "smilies",
                "themes",
                "docs",
                "README.md",
                "LICENSE",
                "CHANGELOG.md",
                "server.json",
                "PCskins.png",
                "Pesterchum.png"]
build_exe_options = {
    "includes": ["requests","urllib","pytwmn"],
    "excludes": ["collections.sys",
                 "collections._sre",
                 "collections._json",
                 "collections._locale",
                 "collections._struct",
                 "collections.array",
                 "collections._weakref"],
    "include_files": includefiles
}

bdist_mac_options = {
    'iconfile': 'trayicon32.icns',
    'bundle_name': "Pesterchum",
    'plist': {
        'NSHumanReadableCopyright':   'GPL v3',
    }
}

description = "Instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck."
icon = "pesterchum.ico"

# See https://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Pesterchum",             # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]pesterchum.exe",# Target
     None,                     # Arguments
     description,              # Description
     None,                     # Hotkey
     None,                     # Icon (Is inherited from pesterchum.exe)
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),
    ("StartMenuShortcut",        # Shortcut
     "StartMenuFolder",          # Directory_
     "Pesterchum",             # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]pesterchum.exe",# Target
     None,                     # Arguments
     description,              # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data,
                     'summary_data': {
                         'comments': "FL1P",
                         'keywords': "Pesterchum"},
                     'upgrade_code': "{86740d75-f1f2-48e8-8266-f36395a2d77f}",
                     'add_to_path': False, # !!!
                     'all_users': True,
                     'install_icon': "pesterchum.ico"}

#print("type(includefiles) = " + str(type(includefiles)))
#print("type(build_exe_options) = " + str(type(build_exe_options))


setup(
            name = "Pesterchum",
            version = buildVersion,
            url = "https://github.com/Dpeta/pesterchum-alt-servers",
            description = description,#"P3ST3RCHUM",
            options = {"build_exe": build_exe_options,
                       "bdist_msi": bdist_msi_options,
                       "bdist_mac": bdist_mac_options},
            executables = [Executable("pesterchum.py",
                                      base=base,
                                      icon=icon#,
                                      #shortcut_name="Pesterchum",
                                      #shortcut_dir="DesktopFolder"
                                      )])
