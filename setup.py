# Windows-only cx_freeze setup file
from cx_Freeze import setup, Executable
import sys
import os
import shutil

if sys.version_info < (3, 0, 0):
    sys.exit("Python3 versions lower than 3 are not supported.")

def is_64bit() -> bool:
    return sys.maxsize > 2**32

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
                 'collections._weakref'],
}
if is_64bit() == true:
    setup(
            name = "PESTERCHUM",
            version = "3.41",
            description = "P3ST3RCHUM",
            options = {"build_exe": build_exe_options},
            executables = [Executable("pesterchum.py",
                                      base=base,
                                      compress=True,
                                      icon="pesterchum.ico",
                                      build_exe: 'build\Pesterchum\'
                                      )])
    if sys.platform == "win32":
        os.rename("build/exe.win-amd64-2.7", "build/pesterchum")
else:
    pass
#Replace exe.win-amd64-2.7 with whatever it seems to generate as for you.


shutil.copytree("themes", "build/pesterchum/themes")
shutil.copytree("smilies", "build/pesterchum/smilies")
shutil.copytree("quirks", "build/pesterchum/quirks")
shutil.copy("pesterchum.nsi", "build/pesterchum/")
shutil.copy("pesterchum-update.nsi", "build/pesterchum/")
os.mkdir("build/pesterchum/profiles")
os.mkdir("build/pesterchum/logs")

#Readme & txt
shutil.copy("README.md", "build/pesterchum/")
shutil.copy("README-pesterchum.mkdn", "build/pesterchum/")
shutil.copy("README-karxi.mkdn", "build/pesterchum/")
shutil.copy("themes.txt", "build/pesterchum/")
