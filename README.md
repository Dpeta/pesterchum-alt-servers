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
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge"></a>
</h1>
<img alt="PESTERCHUM" align="right" src="Pesterchum.png">

Pesterchum is an instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck.

Contributions in any form are very welcome!! Including for extra themes, bug fixes, features, etc. Just hmu in the support server or make a pull request :3

There's a [Russian translation of this repository](https://github.com/Daosp/pesterchum-Dpeta-rus/releases) available, it's somewhat outdated though.

This repository is a maintained version of [ghostDunk's Pesterchum](https://github.com/illuminatedwax/pesterchum/), originally forked from <a href= "https://github.com/karxi/pesterchum">pesterchum-karxi</a> + [Hydrothermal](https://github.com/Hydrothermal)'s fix of the "YOUR NICK IS BEING CHANGED TO X" msgbox-spam exploit.

## MAIN CHANGES <img width="40" src="https://www.pesterchum.xyz/img/bigsleek.png">
 - Updated dependencies; [Python 2 --> Python 3](https://www.python.org/doc/sunset-python-2/), [Qt4 --> Qt5 & Qt6](https://www.qt.io/blog/2014/11/27/qt-4-8-x-support-to-be-extended-for-another-year)
 - Basic GUI for choosing a server
 - Client --> Server encrypted connection via [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) 
 - UTF-8 encoded text, emojis 😿💀😱 work and so do non-western characters that weren't supported with ascii
 - Get moods (and color) privately via metadata (IRCv3 draft), previously any IRC user could see who you were messaging since it would send out a public GETMOOD request
 - Tentative support for communicating color and timeline via [IRCv3 Message Tags/TAGMSG](https://ircv3.net/specs/extensions/message-tags#the-tagmsg-tag-only-message)
 - More options for quirks: <a href="quirks/gradient.py">build-in gradient function</a>, <a href="CHANGELOG.md#v231---2022-06-23"> exclude smilies/links</a> (https://github.com/Dpeta/pesterchum-alt-servers/issues/35)
 - Funky [win95-theme](https://www.pesterchum.xyz/img/win95.png) by [cubicSimulation](https://twitter.com/cubicSimulation) <img width="24" src="themes/win95chum/trayicon.png">
 - Works better with high resolutions since size scales via Qt's [high DPI scaling](https://doc.qt.io/qt-6/highdpi.html) (https://github.com/Dpeta/pesterchum-alt-servers/issues/66)
 - Usable with Wayland on Linux, it used to break because of the way Pesterchum set its window position
 - Excecutables build with PyInstaller, allows for a smaller release filesize + dlls can be include with the binary
 - Lots of fixes for miscellaneous crashes/issues. . . check out the <a href="CHANGELOG.md">CHANGELOG</a>! :3

[CHANGELOG.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/main/CHANGELOG.md
[TODO.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/main/TODO.md

## INSTALLATION <img width="40" src="smilies/headbonk.gif">

1. Download the appropriate release for your platform and architecture from [releases][releases].
2. Extract the zip file.
3. Run the executable:


    - For Windows, run ``pesterchum.exe``, this may show up as just "pesterchum" if you have file extensions set to hidden.
        - Newer releases won't run on Windows XP/Vista since Python stopped supporting it.

    - For Linux, run ``Pesterchum``.
        - Linux releases are not backwards compatible with glibc versions older than the one it was build against. The glibc version the release was build against will be included in the filename, like: *PesterchumAlt.-2.2-linux64-**glibc2.27**.tar.gz*. This really shouldn't be an issue unless your distro is absolutely ancient, if it is, run from source.
        
    - For macOS, run the ``Pesterchum.app`` app file, this may show up as just "Pesterchum" if you have file extensions set to hidden. Alternatively, run the binary directly from ``Pesterchum\Pesterchum.app\Contents\MacOS\Pesterchum``.
        - macOS releases require at least 10.14 (Mojave) or older and a 64 bit processor.
        - My releases are unsigned, so you'll probably have to click ["Open Anyway"](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unidentified-developer-mh40616/mac).
 
[releases]: https://github.com/Dpeta/pesterchum-alt-servers/releases


## DOCUMENTATION <img width="40" src="smilies/theprofessor.png">

The old documentation can be found in [docs](docs), these have aged pretty well:
 - <a href="docs/themes.txt">HOW TO MAKE YOUR OWN THEME</a>
 - <a href="docs/trollquirks.mkdn">Canon troll quirk guide (REGEXP REPLACE)</a>
 - <a href="docs/PYQUIRKS.mkdn">Guide for setting up Python quirk functions</a>

I've been adding some info to [the wiki](https://github.com/Dpeta/pesterchum-alt-servers/wiki), the available pages as of me updating this readme are:
 - [Handle registration and ownership (nickServ)](https://github.com/Dpeta/pesterchum-alt-servers/wiki/Handle-registration-and-ownership)
 - [Memo registration and ownership (chanServ)](https://github.com/Dpeta/pesterchum-alt-servers/wiki/Memo-registration-and-ownership)

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
Pesterchum is a Python script. This means that as long as you have Python installed you can run it without requiring a build/executable, this is useful if there's no compatible build for your system.

### DEPENDENCIES
 - [Python 3]
     - Ideally 3.8 or later, though older versions may still work, I don't test them.
 - [PyQt6] (prefered) or [PyQt5] (legacy)
     - Qt6 only supports maintained 64 bit operating systems, like Windows 10 or later for Windows. ([Qt 6.3 Supported Platforms](https://doc.qt.io/qt-6/supported-platforms.html))
     - Qt5 supports Windows 7 or later, but is past its EOL for non-commercial use. ([Qt 5.15 Supported Platforms](https://doc.qt.io/qt-6/supported-platforms.html))
 - (Optional) [pygame-ce] or [pygame] can provide an alternative audio backend for certain systems.
     - Useful for Linux systems that don't meet the Qt6 requirements, as Qt5 Multimedia has a GStreamer dependency.
 - (Optional) [certifi] can provide alternative root certificates for TLS certificate validation.
     - Useful for MacOS, as Python doesn't use the system-provided certificates because of MacOS' outdated SSL library. Also miscellaneous systems without usable root certificates.
 - (Optional) [libseccomp] and its Python bindings on Linux let Pesterchum apply seccomp-bpf restrictions on itself.
    - Packages on Arch: ``libseccomp python-libseccomp``
    - Packages on Debian: ``libseccomp2 python-seccomp``
 
### WALKTHROUGH

1. Verify you have [Python 3] and [pip] installed by running ``python --version`` and ``python -m pip --version`` on your system's console/terminal. If not, [install Python](https://www.python.org/downloads/), make sure to check to include pip and "Add to path" in the installer. If you have Python 3 but not pip, you could use [get-pip](https://github.com/pypa/get-pip).
    - On Windows, depending on your installation, Python 3 might be available with the ``py -3`` command instead of ``python``.
    - Some platforms, mostly Linux and macOS, might require you to run ``python3`` instead of ``python``. Some old installations still have Python 2 available under ``python``.
    - On Linux it's better to install Python & pip via your package manager.
    - On macOS it's also possible to install (a more recent version of) Python via [Brew](https://brew.sh/).
2. Install Pesterchum's dependencies with pip, run: ``python -m pip install -r requirements.txt``
    - If this fails, try running ``python -m pip install -U pip setuptools wheel`` to update pip, setuptools & wheel and then trying again.
    - Alternatively, many linux distros also have packages for pyqt and pygame.
        - Debian: [python3-pyqt6](https://packages.debian.org/testing/python/python3-pyqt6), [python3-pygame](https://packages.debian.org/testing/python/python3-pygame)
        - Arch: [python-pyqt6](https://archlinux.org/packages/extra/x86_64/python-pyqt6/), [python-pygame](https://archlinux.org/packages/community/x86_64/python-pygame/)
3. Download [this repository's source](https://github.com/Dpeta/pesterchum-alt-servers/archive/refs/heads/main.zip), or choose the "Source Code" option on any release, and extract the archive to a folder of your choice.
    - Alternatively, clone the repository with git.
4. Navigate your terminal to the folder you chose with ``cd /folder/you/chose``.
    - For example, if you extracted it to your documents on Windows, run ``cd C:\Users\user\Documents\pesterchum-alt-servers-main``.
        - Windows's cd command requires the /d flag to navigate to a different drive. (``cd D:\pesterchum-alt-servers-main``)
5. Run Pesterchum by running ``python pesterchum.py`` or ``python3 pesterchum.py``.

[Python 3]: https://www.python.org/downloads/
[pip]: https://pypi.org/project/pip/
[PyQt5]: https://pypi.org/project/PyQt5/
[PyQt6]: https://pypi.org/project/PyQt6/
[pygame]: https://pypi.org/project/pygame/
[pygame-ce]: https://pypi.org/project/pygame-ce/
[certifi]: https://pypi.org/project/certifi/
[GStreamer]: https://gstreamer.freedesktop.org/
[libseccomp]: https://github.com/seccomp/libseccomp/
 
## FREEZE / BUILD <img src="themes/win95chum/admin.png">
Here's a quick guide on how to freeze Pesterchum, (that is, packaging it with python as an executable). :3

Ideally, you'll want to create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) before anything else, this is not 100% required though.

### [CX_FREEZE](https://cx-freeze.readthedocs.io/en/latest/index.html)
1. ``python3 -m pip install cx_freeze``
2. ``python3 setup.py build``

### [PYINSTALLER](https://pyinstaller.readthedocs.io/en/stable/)
1. ``python3 -m pip install pyinstaller``
2. ``python3 pyinst.py``

## SMILIES <img height="32" alt="pesterchum what did you do smilie" src="smilies/whatdidyoudo.gif">
|Text|Smilie|
|:--- | :--- |
|`:rancorous:`|<img alt=':rancorous: pesterchum smilie/emote' src='smilies/pc_rancorous.png'>|
|`:apple:`|<img alt=':apple: pesterchum smilie/emote' src='smilies/apple.png'>|
|`:bathearst:`|<img alt=':bathearst: pesterchum smilie/emote' src='smilies/bathearst.png'>|
|`:cathearst:`|<img alt=':cathearst: pesterchum smilie/emote' src='smilies/cathearst.png'>|
|`:woeful:`|<img alt=':woeful: pesterchum smilie/emote' src='smilies/pc_bemused.png'>|
|`:sorrow:`|<img alt=':sorrow: pesterchum smilie/emote' src='smilies/blacktear.png'>|
|`:pleasant:`|<img alt=':pleasant: pesterchum smilie/emote' src='smilies/pc_pleasant.png'>|
|`:blueghost:`|<img alt=':blueghost: pesterchum smilie/emote' src='smilies/blueslimer.gif'>|
|`:slimer:`|<img alt=':slimer: pesterchum smilie/emote' src='smilies/slimer.gif'>|
|`:candycorn:`|<img alt=':candycorn: pesterchum smilie/emote' src='smilies/candycorn.png'>|
|`:cheer:`|<img alt=':cheer: pesterchum smilie/emote' src='smilies/cheer.gif'>|
|`:duhjohn:`|<img alt=':duhjohn: pesterchum smilie/emote' src='smilies/confusedjohn.gif'>|
|`:datrump:`|<img alt=':datrump: pesterchum smilie/emote' src='smilies/datrump.png'>|
|`:facepalm:`|<img alt=':facepalm: pesterchum smilie/emote' src='smilies/facepalm.png'>|
|`:bonk:`|<img alt=':bonk: pesterchum smilie/emote' src='smilies/headbonk.gif'>|
|`:mspa:`|<img alt=':mspa: pesterchum smilie/emote' src='smilies/mspa_face.png'>|
|`:gun:`|<img alt=':gun: pesterchum smilie/emote' src='smilies/mspa_reader.gif'>|
|`:cal:`|<img alt=':cal: pesterchum smilie/emote' src='smilies/lilcal.png'>|
|`:amazedfirman:`|<img alt=':amazedfirman: pesterchum smilie/emote' src='smilies/pc_amazedfirman.png'>|
|`:amazed:`|<img alt=':amazed: pesterchum smilie/emote' src='smilies/pc_amazed.png'>|
|`:chummy:`|<img alt=':chummy: pesterchum smilie/emote' src='smilies/pc_chummy.png'>|
|`:cool:`|<img alt=':cool: pesterchum smilie/emote' src='smilies/pccool.png'>|
|`:smooth:`|<img alt=':smooth: pesterchum smilie/emote' src='smilies/pccool.png'>|
|`:distraughtfirman:`|<img alt=':distraughtfirman: pesterchum smilie/emote' src='smilies/pc_distraughtfirman.png'>|
|`:distraught:`|<img alt=':distraught: pesterchum smilie/emote' src='smilies/pc_distraught.png'>|
|`:insolent:`|<img alt=':insolent: pesterchum smilie/emote' src='smilies/pc_insolent.png'>|
|`:bemused:`|<img alt=':bemused: pesterchum smilie/emote' src='smilies/pc_bemused.png'>|
|`:3:`|<img alt=':3: pesterchum smilie/emote' src='smilies/pckitty.png'>|
|`:mystified:`|<img alt=':mystified: pesterchum smilie/emote' src='smilies/pc_mystified.png'>|
|`:pranky:`|<img alt=':pranky: pesterchum smilie/emote' src='smilies/pc_pranky.png'>|
|`:tense:`|<img alt=':tense: pesterchum smilie/emote' src='smilies/pc_tense.png'>|
|`:record:`|<img alt=':record: pesterchum smilie/emote' src='smilies/record.gif'>|
|`:squiddle:`|<img alt=':squiddle: pesterchum smilie/emote' src='smilies/squiddle.gif'>|
|`:tab:`|<img alt=':tab: pesterchum smilie/emote' src='smilies/tab.gif'>|
|`:beetip:`|<img alt=':beetip: pesterchum smilie/emote' src='smilies/theprofessor.png'>|
|`:flipout:`|<img alt=':flipout: pesterchum smilie/emote' src='smilies/weasel.gif'>|
|`:befuddled:`|<img alt=':befuddled: pesterchum smilie/emote' src='smilies/what.png'>|
|`:pumpkin:`|<img alt=':pumpkin: pesterchum smilie/emote' src='smilies/whatpumpkin.png'>|
|`:trollcool:`|<img alt=':trollcool: pesterchum smilie/emote' src='smilies/trollcool.png'>|
|`:jadecry:`|<img alt=':jadecry: pesterchum smilie/emote' src='smilies/jadespritehead.gif'>|
|`:ecstatic:`|<img alt=':ecstatic: pesterchum smilie/emote' src='smilies/ecstatic.png'>|
|`:relaxed:`|<img alt=':relaxed: pesterchum smilie/emote' src='smilies/relaxed.png'>|
|`:discontent:`|<img alt=':discontent: pesterchum smilie/emote' src='smilies/discontent.png'>|
|`:devious:`|<img alt=':devious: pesterchum smilie/emote' src='smilies/devious.png'>|
|`:sleek:`|<img alt=':sleek: pesterchum smilie/emote' src='smilies/sleek.png'>|
|`:detestful:`|<img alt=':detestful: pesterchum smilie/emote' src='smilies/detestful.png'>|
|`:mirthful:`|<img alt=':mirthful: pesterchum smilie/emote' src='smilies/mirthful.png'>|
|`:manipulative:`|<img alt=':manipulative: pesterchum smilie/emote' src='smilies/manipulative.png'>|
|`:vigorous:`|<img alt=':vigorous: pesterchum smilie/emote' src='smilies/vigorous.png'>|
|`:perky:`|<img alt=':perky: pesterchum smilie/emote' src='smilies/perky.png'>|
|`:acceptant:`|<img alt=':acceptant: pesterchum smilie/emote' src='smilies/acceptant.png'>|
|`:olliesouty:`|<img alt=':olliesouty: pesterchum smilie/emote' src='smilies/olliesouty.gif'>|
|`:billiards:`|<img alt=':billiards: pesterchum smilie/emote' src='smilies/poolballS.gif'>|
|`:billiardslarge:`|<img alt=':billiardslarge: pesterchum smilie/emote' src='smilies/poolballL.gif'>|
|`:whatdidyoudo:`|<img alt=':whatdidyoudo: pesterchum smilie/emote' src='smilies/whatdidyoudo.gif'>|
|`:brocool:`|<img alt=':brocool: pesterchum smilie/emote' src='smilies/pcstrider.png'>|
|`:trollbro:`|<img alt=':trollbro: pesterchum smilie/emote' src='smilies/trollbro.png'>|
|`:playagame:`|<img alt=':playagame: pesterchum smilie/emote' src='smilies/saw.gif'>|
|`:trollc00l:`|<img alt=':trollc00l: pesterchum smilie/emote' src='smilies/trollc00l.gif'>|
|`:suckers:`|<img alt=':suckers: pesterchum smilie/emote' src='smilies/Suckers.gif'>|
|`:scorpio:`|<img alt=':scorpio: pesterchum smilie/emote' src='smilies/scorpio.gif'>|
|`:shades:`|<img alt=':shades: pesterchum smilie/emote' src='smilies/shades.png'>|
|`:honk:`|<img alt=':honk: pesterchum smilie/emote' src='smilies/honk.png'>|
