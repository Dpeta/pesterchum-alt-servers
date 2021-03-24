# Windows-only cx_freeze setup file
from cx_Freeze import setup, Executable
import sys
import os
import shutil

from version import _pcVersion

if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "includes": ["requests","urllib"],
    'excludes': ['collections.sys',
                 'collections._sre',
                 'collections._json',
                 'collections._locale',
                 'collections._struct',
                 'collections.array',
                 'collections._weakref'],
}

setup(
        name = "Pesterchum",
        version = str(_pcVersion),
        description = "Pesterchum Alt. 2.0 :)",
        options = {"build_exe": build_exe_options},
        executables = [Executable("pesterchum.py",
                                  base=base,
                                  icon="pesterchum.ico",
                                  ),
                       Executable("pesterchum_debug.py",
                                  base=base,
                                  icon="pesterchum.ico",
                                  )])

#if sys.platform == "win32":
#    os.rename("build/exe.win32-2.7", "build/pesterchum")

shutil.copytree("themes", "build/pesterchum/themes")
shutil.copytree("smilies", "build/pesterchum/smilies")
shutil.copytree("quirks", "build/pesterchum/quirks")
#shutil.copy("pesterchum.nsi", "build/pesterchum/")
#shutil.copy("pesterchum-update.nsi", "build/pesterchum/")
#os.mkdir("build/pesterchum/profiles")
#os.mkdir("build/pesterchum/logs")

#Readme & txt
#shutil.copy("README.md", "build/pesterchum/")
#shutil.copy("README-pesterchum.mkdn", "build/pesterchum/")
#shutil.copy("README-karxi.mkdn", "build/pesterchum/")
#shutil.copy("themes.txt", "build/pesterchum/")
