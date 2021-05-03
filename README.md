# PESTERCHUM
Maintained repository of ghostDunk's Pesterchum. Connects to irc.pesterchum.xyz by defaults since the official server shut down (custom servers can be configured in server.json!!). Pesterchum is an instant messaging client copying the look and feel of clients from Andrew Hussie's webcomic Homestuck.

This repository builds on (and was mirrored from!) from pesterchum-karxi + Hydrothermal's nickserv fix.

Check out [CHANGELOG.md] file to see what's changed!
Check out [TODO.md] to see this repo's current goals >:3c

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


## INSTALATION
Download the appropriate release for your platform from [releases][releases]. If you're on windows you can use the installer, for a manual install download the zip file and extract it to any directory, and run the executable : )

Because of the nature of cx_freeze & pyinstaller, some libraries (like glibc) are dynamically linked. If the executeable for your platform is uncompatible with the version of your operating system, see the next section for running Pesterchum directly.
 
[releases]: https://github.com/Dpeta/pesterchum-alt-servers/releases

## RUNNING & BUILDING
Here's a quick guide on what to do to run Pesterchum from the command line, and to build it if you so desire (that is, generating an executable). Running Pesterchum directly or building Pesterchum yourself is not required to run it!!! This is only relevant if you know what you're doing >:3c

If you have Python and Pesterchum's dependencies installed, you can simply run Pesterchum from the commandline with ```python pesterchum.py```.
### REQUIREMENTS:

 - [Python 3]

#### PYTHON DEPENDENCIES
You can install them with Python's pip or your package manager if you're on linux :)
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

### PYINSTALLER BUILDING
My preferred method of generating binary releases.
``python pyinstaller.py``

### CX_FREEZE BUILDING

#### Windows:
``python setup.py build``
or
``python setup.py bdist_msi``

#### Mac:
``python setup.py build``

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
