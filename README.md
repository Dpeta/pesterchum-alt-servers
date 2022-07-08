<h1 align="center" style="font-family: 'Courier New';">
    <b>
        <img alt="PESTERCHUM" src="https://www.pesterchum.xyz/img/translogo23.png">
        </b>
    <a href="https://github.com/Dpeta/pesterchum-alt-servers/releases"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/Dpeta/pesterchum-alt-servers/total?style=for-the-badge"></a>
    <a href="https://discord.gg/BbHvdwN"><img alt="Community Discord" src="https://img.shields.io/discord/761299023121350726?color=blue&label=COMMUNITY%20DISCORD&logo=discord&style=for-the-badge"></a>
    <a href="https://discord.gg/eKbP6pvUmZ"><img alt="Support Discord" src="https://img.shields.io/discord/906250212362842143?color=blue&label=SUPPORT%20DISCORD&logo=discord&style=for-the-badge"></a>
    <br>
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/Dpeta/pesterchum-alt-servers?style=for-the-badge">
    <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/Dpeta/pesterchum-alt-servers?style=for-the-badge">
</h1>
<img alt="PESTERCHUM" align="right" src="Pesterchum.png">

Pesterchum is an instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck.

Contributions in any form are very welcome!! Including for extra themes, bug fixes, features, etc. Just hmu in the support server or make a pull request :3

There's a [Russian translation of this repository](https://github.com/Daosp/pesterchum-Dpeta-rus) available, it's somewhat outdated though.

This repository is a maintained version of [ghostDunk's Pesterchum](https://github.com/illuminatedwax/pesterchum/), originally forked from <a href= "https://github.com/karxi/pesterchum">pesterchum-karxi</a> + [Hydrothermal](https://github.com/Hydrothermal)'s fix of the "YOUR NICK IS BEING CHANGED TO X" msgbox-spam exploit.

## NEW FEATURES <img width="40" src="https://www.pesterchum.xyz/img/bigsleek.png">
 - Updated codebase; [Python 2 --> Python 3](https://www.python.org/doc/sunset-python-2/), [Qt4 --> Qt6](https://www.qt.io/blog/2014/11/27/qt-4-8-x-support-to-be-extended-for-another-year)
     - Size scales with resolution via Qt's [high DPI scaling](https://doc.qt.io/qt-6/highdpi.html)
 - GUI for choosing a server
 - Secure connection with [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) 
 - UTF-8 text, annoy chums with 😿💀😱
 - Get moods privately via [METADATA](https://github.com/pirc-pl/unrealircd-modules#metadata), <a href="CHANGELOG.md#v23---2022-06-06">IRC-stalking is harder</a>
 - Tentative support for communicating color and timeline via [IRCv3 Message Tags/TAGMSG](https://ircv3.net/specs/extensions/message-tags#the-tagmsg-tag-only-message)
 - More options for quirks (<a href="quirks/gradient.py">build-in gradient function</a>, <a href="CHANGELOG.md#v231---2022-06-23"> exclude smilies/links</a>)
 - Funky [win95-theme](https://www.pesterchum.xyz/img/win95.png) by [cubicSimulation](https://twitter.com/cubicSimulation) <img width="24" src="themes/win95chum/trayicon.png">
 - [Wayland](https://en.wikipedia.org/wiki/Wayland_(display_server_protocol)) compatibility
 - Excecutables build with PyInstaller
 - Lots of fixes for miscellaneous crashes/issues. . . check out the <a href="CHANGELOG.md">CHANGELOG</a>! :3

[CHANGELOG.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/main/CHANGELOG.md
[TODO.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/main/TODO.md

## INSTALLATION <img width="40" src="smilies/headbonk.gif">

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


## DOCUMENTATION <img width="40" src="smilies/theprofessor.png">

The old documentation can be found in [docs](docs), these have aged pretty well:
 - <a href="docs/themes.txt">HOW TO MAKE YOUR OWN THEME</a>
 - <a href="docs/trollquirks.mkdn">Canon troll quirk guide (REGEXP REPLACE)</a>
 - <a href="docs/PYQUIRKS.mkdn">Guide for setting up Python quirk functions</a>

Some useful off-repo guides:
 - [How to register your handle with nickServ](https://squidmaid.tumblr.com/post/67595522089/how-to-register-your-pesterchum-handle-the-actual)
 - [Collection of gradient quirk function guides](https://paste.0xfc.de/?e60df5a155e93583#AmcgN9cRnCcBycmVMvw6KJ1YLKPXGbaSzZLbgAhoNCQD
)

The old READMEs are also preserved in the [docs](docs) folder:
- <a href="docs/README-pesterchum.mkdn"> illuminatedWax's README</a>
- <a href="docs/README-karxi.mkdn "> karxi's README</a>
- <a href="docs/TODO.mkdn "> karxi's TODO</a>
- <a href="docs/CHANGELOG-karxi.mkdn "> karxi's CHANGELOG</a>

## RUNNING FROM SOURCE <img src="smilies/tab.gif">
Pesterchum is a Python script. This means that as long as you have Python installed you can run it without requiring a build/executable. This is useful if there's no compatible build for your system.

### REQUIREMENTS
 - [Python 3]
 - [PyQt6]
 - On Linux, optionally [pygame] for audio. (QtMultimedia has a [GStreamer] dependency on Linux)
 
### WALKTHROUGH

1. Verify you have [Python 3] and [pip] installed by running ``python --version`` and ``python -m pip --version`` on your system's console/terminal. If not, [install Python](https://www.python.org/downloads/), make sure to check to include pip and "Add to path" in the installer. If you have Python 3 but not pip, you could use [get-pip](https://github.com/pypa/get-pip).
    - On Windows, depending on your installation, Python 3 might be available with the ``py -3`` command instead of ``python``.
    - Some platforms, mostly Linux and macOS, might require you to run ``python3`` instead of ``python``. Some old installations still have Python 2 available under ``python``.
    - On Linux it's better to install Python & pip via your package manager.
    - On macOS it's also possible to install (a more recent version of) Python via [Brew](https://brew.sh/).
2. Install Pesterchum's dependencies with pip, run: ``python -m pip install PyQt6 pygame``
    - If this fails, try running ``python -m pip install -U pip setuptools wheel`` to update pip, setuptools & wheel and then trying again.
3. Download [this repository's source](https://github.com/Dpeta/pesterchum-alt-servers/archive/refs/heads/main.zip), or choose the "Source Code" option on any release, and extract the archive to a folder of your choice.
4. Navigate your terminal to the folder you chose with ``cd /folder/you/chose``.
    - For example, if you extracted it to your documents on Windows, run ``cd C:\Users\user\Documents\pesterchum-alt-servers-main``.
        - Windows's cd command requires the /d flag to navigate to a different drive. (``cd D:\pesterchum-alt-servers-main``)
5. Run Pesterchum by running either ``pesterchum.py`` or ``python pesterchum.py``.

[Python 3]: https://www.python.org/downloads/
[pip]: https://pypi.org/project/pip/
[PyQt6]: https://pypi.org/project/PyQt6/
[pygame]: https://pypi.org/project/pygame/
[GStreamer]: https://gstreamer.freedesktop.org/
 
## FREEZE / BUILD <img src="themes/win95chum/admin.png">
Here's a quick guide on how to freeze Pesterchum, (that is, packaging it with python as an executable). :3

Ideally, you'll want to create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) before anything else, this is not 100% required though.

### [CX_FREEZE](https://cx-freeze.readthedocs.io/en/latest/index.html)
1. ``pip install cx_freeze``
2. ``python3 setup.py build``

### [PYINSTALLER](https://pyinstaller.readthedocs.io/en/stable/)
1. ``pip install pyinstaller``
2. ``python3 pyinstaller.py``

## SMILIES <img height="32" src="smilies/whatdidyoudo.gif">
<img align="right" src="https://www.pesterchum.xyz/img/scrunkle3.gif">

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
