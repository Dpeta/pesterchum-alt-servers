# Changelog
(This document uses YYYY-MM-DD as per ISO 8601)

## [v2.1.2]

### Changed
- Made file capitalization consistent for a few files. (.PNG --> .png), because some file systems are queasy on that. (See https://superuser.com/questions/881804/case-sensitive-file-extensions-in-windows-and-linux) 


## [v2.1.1] - 2021-4-12

### Fixed
- Fixed theme not getting applied correctly to memo.
- Fixed sRGB profile in steamchum.

### Changed
- convo/tabwindow on trollian 2.5 seems to be used for the general background color, so, I changed it to a value. I'm not use if this was intentional.

## [v2.1.0] - 2021-4-11

### Added
- Server prompt + interface for adding & removing servers.
- Consistently capitalized text for all themes, for example, "REPORT BUG" to "Report Bug" for Trollian.
- Added theme support for "Beep on Message", "Flash on Message", "Mute Notifications".
- "Usage:" for pesterchum.py when running from the command line.
- Made logging level configurable via command line arguments.
- Added -h/--help.

### Fixed
- Fixed current mood icon not showing up.
- Fixed "CHUMHANDLE:" not fitting on some themes.
- Fixed "CONSOLE" & "REPORT BUG" menu options not being updated on theme change.
- Incorrect hex for color in MSChum theme.
- Fixed \_datadir not being used for certain json files.
- Fixed "Specified color without alpha value but alpha given: 'rgb 0,0,0,0'" in johntierchum.
- Fixed "RGB parameters out of range" in MSChum.
- Fixed nothing.png not being present in battlefield theme.
- Fixed "Report" string not being updated in convo window when changing theme.
- Fixed pesterChumAction's text not being updated in memo windows when changing theme.
- Fixed incorrect sRGB profile in paperchum.
- Fixed sound slider in settings not working with pygame.
- Fixed MOOD & CHUMHANDLE not adjusting to style-sheet.

### Changed
- Made it so handle and ident are passed to ``_max_msg_len``, so, hopefully the text cutoff will be *slightly* less restrictive.

### Deprecated
- Removed splitMessage function.

## [v2.0.2] - 2021-4-2

### Fixed
- "Fixed" crash when closing certain windows on certain platforms.

## [v2.0.1] - 2021-4-1

### Fixed
- Added a fallback for non-unicode characters, and for when decoding fails completely, so hopefully they won't cause a crash anymore.

## [v2.0] - 2021-3-25

### Added
- Added styleing/markup to "PESTER" and "ADD GROUP" menu options and some other previously unstyled elements :)
- Added pesterchum.spec for use with pyinstaller.
- Wrapped socket in SSL context and changed the port appropriately, hostname verification is turned off.
- Pesterchum now sends a ``QUIT :reason`` to the server when shutting down instead of just quitting instantly.

### Changed
- Transitioned to Python 3.
- Transitioned to PyQt5.
- Changed character encoding in some placed from ascii to UTF-8 (Emojis should work now)
- Rewrote setup.py file & added bdist_msi

### Fixed
- Fixed sRGB profile issue with certain images.
- Fixed issue where Pesterchum crashed if a quirk was malformed.
- Fixed Pesterchum icon getting stuck on the system tray even after shutdown on windows.
- Fixed floating "PESTERLOGS:" in pesterchum & pesterchum2.5 themes.

### Deprecated
- Removed update system (it seemed to be non-functional).
- Removed MSPA update checking (non-functional since Homestuck ended).
- Removed feedparser.py (feedparser) and magic.py (python-magic) from libs and changed them to be normal imports. (Because we're not running Python 2 anymore)

## [pre-v1.20] - 2021-2-25
### Added
- Made the server configurable with server.json

### Fixed
- Fixed issue where Pesterchum would crash when unable to find the default profile.
- Fixed rare issue where auto-identifying to nickserv would cause Pesterchum to crash.

### Deprecated
- Removed dead links to Pesterchum QDB from menus.
- Removed no longer functional bugreport system.
