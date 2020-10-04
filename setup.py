# Windows-only cx_freeze setup file
from cx_Freeze import setup, Executable
import sys
import os
import shutil
import requests
import urllib
import PyQt4
import configparser
from Queue import *

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = "Console"

build_exe_options = {
    "includes": ["requests","urllib"],
    'excludes': ['collections.sys',
                 'collections._sre',
                 'collections._json',
                 'collections._locale',
                 'collections._struct',
                 'collections.array',
                 'collections._weakref'], # Not excluding these is the only way I could get it to build while using configparser. I don't know why though.
}

setup(
        name = "PESTERCHUM",
        version = "3.41",
        description = "P3ST3RCHUM",
        options = {"build_exe": build_exe_options},
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
shutil.copy("server.ini", "build/pesterchum/")
os.mkdir("build/pesterchum/profiles")
os.mkdir("build/pesterchum/logs")

#Readme & txt
shutil.copy("README.md", "build/pesterchum/")
shutil.copy("README-pesterchum.mkdn", "build/pesterchum/")
shutil.copy("README-karxi.mkdn", "build/pesterchum/")
shutil.copy("themes.txt", "build/pesterchum/")
