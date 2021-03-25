# Windows-only cx_freeze setup file
from cx_Freeze import setup, Executable
import sys

from version import buildVersion

if sys.version_info < (3, 0, 0):
    sys.exit("Python versions lower than 3 are not supported.")

def is_64bit() -> bool:
    return sys.maxsize > 2**32

if sys.platform == "win32":
    base = "Win32GUI"
else:
    sys.exit("This script won't work on this platform </3")

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
    'include_files': includefiles
    #'build_exe': ["build"]
}
#print("type(includefiles) = " + str(type(includefiles)))
#print("type(build_exe_options) = " + str(type(build_exe_options))

if is_64bit() == True:
    setup(
            name = "PESTERCHUM ALT.",
            version = buildVersion,
            url = "https://github.com/Dpeta/pesterchum-alt-servers",
            description = "P3ST3RCHUM ALT.",
            options = {"build_exe": build_exe_options},
            executables = [Executable("pesterchum.py",
                                      base=base,
                                      icon="pesterchum.ico"
                                      )])
