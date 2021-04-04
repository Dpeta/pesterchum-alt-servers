# Changelog
(This document uses YYYY-MM-DD as per ISO 8601)

## [v2.1.0] - 2021-4-4

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
