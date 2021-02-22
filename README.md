# Pesterchum Alternate Servers
Pesterchum with added functionality to connect to alternative servers. (And some other stuff.)

Normal pesterchum documentation is in "README-pesterchum.mkdn" and the one for Karxi's fork is README-karxi.mkdn.

## Servers
If you'd like to connect to a different server than the default "pesterchum.xyz", put the server you'd like to connect to in the server.json file.

## Tips for building
- For windows use "setup.py". PyQt4 binaries for windows can be installed from it's sourceforce page if you don't want to go through the hell that's compiling it manually.
- On mac you can install most of the dependencies via macports and build with "python setup-py2app.py py2app".
