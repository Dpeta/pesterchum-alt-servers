# Windows-only cx_freeze setup file
from cx_Freeze import setup, Executable
import sys
import os
import shutil
import requests
import urllib
import PyQt4
from Queue import *

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = "Console"

build_exe_options = {
    "includes": ["requests","urllib"] # <-- Include
}

setup(
        name = "PESTERCHUM-ALT-SERVERS",
        version = "3.41",
        description = "P3ST3RCHUM",
        executables = [Executable("pesterchum.py",
                                  base=base,
                                  compress=True,
                                  icon="pesterchum.ico",
                                  ),
                       Executable("pesterchum_debug.py",
                                  base=base,
                                  compress=True,
                                  icon="pesterchum.ico",
                                  )])

#Replace exe.win-amd64-2.7 with whatever it seems to generate as for you.
if sys.platform == "win32":
    os.rename("build/exe.win-amd64-2.7", "build/pesterchum")

shutil.copytree("themes", "build/pesterchum/themes")
shutil.copytree("smilies", "build/pesterchum/smilies")
shutil.copy("pesterchum.nsi", "build/pesterchum/")
shutil.copy("pesterchum-update.nsi", "build/pesterchum/")
os.mkdir("build/pesterchum/profiles")
os.mkdir("build/pesterchum/logs")

#Readme & txt
shutil.copy("README.md", "build/pesterchum/")
shutil.copy("README-pesterchum.mkdn", "build/pesterchum/")
shutil.copy("README-karxi.mkdn", "build/pesterchum/")
shutil.copy("themes.txt", "build/pesterchum/")
