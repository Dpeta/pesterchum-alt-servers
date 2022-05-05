# PESTERCHUM
Pesterchum is an instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck.

Maintained repository of ghostDunk's Pesterchum. Prompts the user to choose a server at launch (irc.pesterchum.xyz by default).

This repository builds on (and was mirrored from!) pesterchum-karxi + Hydrothermal's nickserv fix.

Check out [CHANGELOG.md] file to see what's changed!

[CHANGELOG.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/CHANGELOG.md
[TODO.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/TODO.md

## GUIDES

The old READMEs and guides can be viewed in the [docs] folder.
I'd highly recommend you take a look at the following files if you're new to Pesterchum:
- [README-pesterchum.mkdn]
- [trollquirks.mkdn]

Guides for python quirks and themes are also in the [docs] folder. If you want to set up a gradient quirk you should take a look at [these guides][gradient-guide].

[gradient-guide]: https://paste.0xfc.de/?e60df5a155e93583#AmcgN9cRnCcBycmVMvw6KJ1YLKPXGbaSzZLbgAhoNCQD
[trollquirks.mkdn]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/docs/trollquirks.mkdn
[README-pesterchum.mkdn]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/docs/README-pesterchum.mkdn
[docs]: https://github.com/Dpeta/pesterchum-alt-servers/tree/py3_pyqt5/docs/

## INSTALLATION
1. Download the appropriate release for your platform and architecture from [releases][releases].
2. Extract the zip file.
3. Run the executable:


    - For Windows, run ``pesterchum.exe``, this may show up as just "pesterchum".
        - Users running outdated versions of Windows 7 used to have to install the [Microsoft Visual C++ Redistributable](https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170), but the relevant DLLs should now be packaged with the releases. Might still be worth trying though if you run into any issues.
        - Newer releases probably won't run on Windows XP since Python stopped supporting it, if you're the singular Windows XP user left consider running from source. :'3


    - For Linux, run ``Pesterchum``.
        - Linux releases are not backwards compatible with glibc versions older than the one it was build against. The glibc version the release was build against will be included in the filename, like: *PesterchumAlt.-2.2-linux64-**glibc2.27**.tar.gz*. This really shouldn't be an issue unless your distro is absolutely ancient, if it is, run from source.
    - For macOS, run ``Pesterchum.app``, this may show up as just "Pesterchum". Alternatively, run the binary directly from ``Pesterchum\Pesterchum.app\Contents\MacOS\Pesterchum``.


        - macOS releases don't support macOS versions older than the one it was build on, recently, I've been using Catalina. If you're running Mojave or older, you'll probably have to run from source.
        - My releases are unsigned, so you'll probably have to click ["Open Anyway"](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unidentified-developer-mh40616/mac).
 
[releases]: https://github.com/Dpeta/pesterchum-alt-servers/releases

## RUNNING FROM SOURCE
Pesterchum is a Python script. This means that as long as you have Python installed you can run it without requiring a build/executable. This is useful if there's no compatible build for your system.

### REQUIREMENTS
 - [Python 3]
 - [PyQt5>=5.15]
 - [pygame] (Only required for audio, Pesterchum will probably still run without it.)
 
### WALKTHROUGH

1. Verify you have [Python 3] and [pip] installed by running ``python --version`` and ``python -m pip --version`` on your system's console/terminal. If not, [install Python](https://www.python.org/downloads/), make sure to check to include pip and "Add to path" in the installer. If you have Python 3 but not pip, you could use [get-pip](https://github.com/pypa/get-pip).
    - On Windows, depending on your installation, Python 3 might be available with the ``py -3`` command instead of ``python``.
    - Some platforms, mostly Linux and macOS, might require you to run ``python3`` instead of ``python``. Some old installations still have Python 2 available under ``python``.
    - On Linux it's better to install Python & pip via your package manager.
    - On macOS it's also possible to install (a more recent version of) Python via [Brew](https://brew.sh/).
2. Install Pesterchum's dependencies with pip, run: ``python -m pip install PyQt5 pygame``
    - If this fails, try running ``python -m pip install -U pip setuptools wheel`` to update pip, setuptools & wheel and then trying again.
3. Download [this repository's source](https://github.com/Dpeta/pesterchum-alt-servers/archive/refs/heads/py3_pyqt5.zip), or choose the "Source Code" option on any release, and extract the archive to a folder of your choice.
4. Navigate your terminal to the folder you chose with ``cd /folder/you/chose``.
    - For example, if you extracted it to your documents on Windows, run ``cd C:\Users\user\Documents\pesterchum-alt-servers-py3_pyqt5``.
        - Windows's cd command requires the /d flag to navigate to a different drive. (``cd D:\pesterchum-alt-servers-py3_pyqt5``)
5. Run Pesterchum by running either ``pesterchum.py`` or ``python pesterchum.py``.

[Python 3]: https://www.python.org/downloads/
[pip]: https://pypi.org/project/pip/
[PyQt5>=5.15]: https://pypi.org/project/PyQt5/
[pygame]: https://pypi.org/project/pygame/
 
## FREEZE / BUILD
Here's a quick guide on how to freeze Pesterchum, (that is, packaging it with python as an executable). :3

Ideally, you'll want to create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) before anything else, this is not 100% required though.

### [CX_FREEZE](https://cx-freeze.readthedocs.io/en/latest/index.html)
1. ``pip install cx_freeze``
2. ``python3 setup.py build``

### [PYINSTALLER](https://pyinstaller.readthedocs.io/en/stable/)
1. ``pip install pyinstaller``
2. ``python3 pyinstaller.py``

## SMILIES
Just for easy reference. :3 (Taken from docs/README-karxi.mkdn)

* `:rancorous:`
* `:apple:`
* `:bathearst:`
* `:cathearst:`
* `:woeful:`
* `:pleasant:`
* `:blueghost:`
* `:slimer:`
* `:candycorn:`
* `:cheer:`
* `:duhjohn:`
* `:datrump:`
* `:facepalm:`
* `:bonk:`
* `:mspa:`
* `:gun:`
* `:cal:`
* `:amazedfirman:`
* `:amazed:`
* `:chummy:`
* `:cool:`
* `:smooth:`
* `:distraughtfirman:`
* `:distraught:`
* `:insolent:`
* `:bemused:`
* `:3:`
* `:mystified:`
* `:pranky:`
* `:tense:`
* `:record:`
* `:squiddle:`
* `:tab:`
* `:beetip:`
* `:flipout:`
* `:befuddled:`
* `:pumpkin:`
* `:trollcool:`
* `:jadecry:`
* `:ecstatic:`
* `:relaxed:`
* `:discontent:`
* `:devious:`
* `:sleek:`
* `:detestful:`
* `:mirthful:`
* `:manipulative:`
* `:vigorous:`
* `:perky:`
* `:acceptant:`
* `:olliesouty:`
* `:billiards:`
* `:billiardslarge:`
* `:whatdidyoudo:`
