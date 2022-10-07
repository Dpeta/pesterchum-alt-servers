# Windows-only cx_freeze setup file, macOS may work but I've not tested it.
import sys

from cx_Freeze import setup, Executable
import pygame

from version import buildVersion

if sys.version_info < (3, 0, 0):
    sys.exit("Python versions lower than 3 are not supported.")


def is_64bit() -> bool:
    return sys.maxsize > 2**32


path = ""
base = None
if sys.platform == "win32":
    base = "Win32GUI"

    path = sys.path
    if is_64bit() == True:
        path.append(
            r"C:\Program Files (x86)\Windows Kits\10\Redist\10.0.22000.0\ucrt\DLLs\x64"
        )
    elif is_64bit() == False:
        path.append(
            r"C:\Program Files (x86)\Windows Kits\10\Redist\10.0.22000.0\ucrt\DLLs\x86"
        )

    print("Path = " + str(path))

includefiles = [
    "quirks",
    "smilies",
    "themes",
    "docs",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "PCskins.png",
    "Pesterchum.png",
]
build_exe_options = {
    #    "includes": ['PyQt6.QtCore',
    #        'PyQt6.QtGui',
    #        'PyQt6.QtWidgets'],
    "excludes": [
        "collections.sys",
        "collections._sre",
        "collections._json",
        "collections._locale",
        "collections._struct",
        "collections.array",
        "collections._weakref",
        "PyQt6.QtMultimedia",
        "PyQt6.QtDBus",
        "PyQt6.QtDeclarative",
        "PyQt6.QtHelp",
        "PyQt6.QtNetwork",
        "PyQt6.QtSql",
        "PyQt6.QtSvg",
        "PyQt6.QtTest",
        "PyQt6.QtWebKit",
        "PyQt6.QtXml",
        "PyQt6.QtXmlPatterns",
        "PyQt6.phonon",
        "PyQt6.QtAssistant",
        "PyQt6.QtDesigner",
        "PyQt6.QAxContainer",
        "pygame.docs"  # Hopefully we can just not have pygame at all at some point =3
        # (when QtMultimedia stops relying on local codecs </3)
        "pygame.examples",
        "pygame.tests",
        "pydoc_data",
    ],
    "include_files": includefiles,
    "include_msvcr": True,  # cx_freeze copies 64-bit binaries always?
    "path": path  # Improved in 6.6, path to be safe
    # VCRUNTIME140.dll <3
}

if (
    (sys.platform == "win32")
    & (sys.version_info.major == 3)
    & (sys.version_info.minor == 8)
):
    build_exe_options["excludes"].append("tkinter")


bdist_mac_options = {"iconfile": "trayicon32.icns", "bundle_name": "Pesterchum"}

description = "Pesterchum"
icon = "pesterchum.ico"

# See https://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop
shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        "Pesterchum",  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]pesterchum.exe",  # Target
        None,  # Arguments
        description,  # Description
        None,  # Hotkey
        None,  # Icon (Is inherited from pesterchum.exe)
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
    (
        "StartMenuShortcut",  # Shortcut
        "StartMenuFolder",  # Directory_
        "Pesterchum",  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]pesterchum.exe",  # Target
        None,  # Arguments
        description,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {
    "data": msi_data,
    "summary_data": {"comments": "FL1P", "keywords": "Pesterchum"},
    "upgrade_code": "{86740d75-f1f2-48e8-8266-f36395a2d77f}",
    "add_to_path": False,  # !!!
    "all_users": False,
    "install_icon": "pesterchum.ico",
}

setup(
    name="Pesterchum",
    version=buildVersion,
    url="https://github.com/Dpeta/pesterchum-alt-servers",
    description=description,  # "P3ST3RCHUM",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
        "bdist_mac": bdist_mac_options,
    },
    packages="",
    executables=[Executable("pesterchum.py", base=base, icon=icon)],
)
