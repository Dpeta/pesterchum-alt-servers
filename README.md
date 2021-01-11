# Pesterchum Alternate Servers
A mirror of pesterchum with added functionality to connect to alternative servers in response to the offical servers shutting down on 01-01-2021. (And with an edited setup.py file)

Normal pesterchum documentation is in "README-pesterchum.mkdn" and the one for Karxi's fork is README-karxi.mkdn.

## Servers
Currently promts the user on launch to choose a server. The implementation of this isn't very pretty, but it seems to function in it's current state.

Currently lets you choose between:
* pesterchum.xyz (turntechCatnip's server)
* havoc.ddns.net (@chaoticCharacte's server)


## Building
Just simply running "python setup.py build" seems to be working for me for building on windows as of now.

Make sure you are running Python 2 and have all the dependencies installed. PyQt4 binaries for windows can be installed from it's sourceforce page if you don't want to go through the hell that's compiling it manually.

On mac I was able to install most of the dependencies via macports and build with "python setup-py2app.py py2app".
