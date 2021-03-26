# PESTERCHUM
Maintained repository of ghostDunk's Pesterchum. Connects to irc.pesterchum.xyz by defaults since the official server shut down (custom servers can be configured in server.json!!). Pesterchum is an instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck.

This repository builds on (and was mirrored from!) from pesterchum-karxi + Hydrothermal's nickserv fix.

Check out [CHANGELOG.md] file to see what's changed!
Check out [TODO.md] to see this repo's current goals >:3c

For the old READMEs and guides, view the [docs] folder. (I removed Lexicality's macBuilds since it's no longer applicable)

[CHANGELOG.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/CHANGELOG.md
[docs]: https://github.com/Dpeta/pesterchum-alt-servers/tree/py3_pyqt5/docs/
[TODO.md]: https://github.com/Dpeta/pesterchum-alt-servers/blob/py3_pyqt5/TODO.md

## INSTALATION
Download the appropriate release for your platform from [releases][releases]. If you're on windows you can use the installer, for a manual install download the zip file and extract it to any directory, and run the executable : )
 
[releases]: https://github.com/Dpeta/pesterchum-alt-servers/releases

## BUILDING
Building Pesterchum yourself is not required to run it!!! This is only relevant if you know what you're doing >:3c

### REQUIREMENTS:

 - [Python 3]

#### PYTHON DEPENDENCIES
 - [pygame]
 - [PyQt5] (And, depending on your package manager & platform, python3-pyqt5.qtmultimedia)
 - [feedparser]
 - [python-magic]
 - [ostools]
 - [requests]

[Python 3]: https://www.python.org/downloads/
[PyQt5]: https://pypi.org/project/PyQt5/
[pygame]: https://pypi.org/project/pygame/
[feedparser]: https://pypi.org/project/feedparser/
[python-magic]: https://pypi.org/project/python-magic/
[ostools]: https://pypi.org/project/ostools/
[requests]: https://pypi.org/project/requests/
### CX_FREEZE METHOD

#### Windows:
``python setup.py build``
or
``python setup.py bdist_msi``

#### Mac:
``python setup.py bdist_msi`` (I, can't get it working, but this *should* work...)

### PYINSTALLER METHOD
#### Linux (might also work on other platforms!!): 
``pyinstaller pesterchum.spec``

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
