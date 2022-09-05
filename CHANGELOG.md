# Changelog
(This document uses YYYY-MM-DD)

## [v2.4.3] - 2022-09-05

### Added
 - Support for color via IRCv3 metadata draft.
    - This way clients can keep track of each other's colors without requiring them to send a message first.
 - Prompt for connecting anyway when certificate validation fails.

### Changed
 - Reenabled server certificate validation when using SSL.
    - Uses the system's local certificates, so might fail on some installations.
 
### Fixed
 - Error when setting quirk with PyQt5.

## [v2.4.2] - 2022-08-14

### Added
 - Application-level connection checks:
    - Send ping if we haven't received any data from the server in 30 seconds.
    - Show S3RV3R NOT R3SPOND1NG if the server hasn't responded in 45 seconds. (15 seconds after ping)
    - Close connection and try to reconnect if the server hasn't responded in 90 seconds. (60 seconds after ping)
 - Fallback to PyQt5. (for Windows 7 users mainly)
 - Warning for people who forgot to extract the zipfile.
 
### Fixed
 - Error when manually moving group.
 - EOF on send not resulting in a disconnect.
 - Desynced memo userlist on handle change, userlist is now re-requested from server on handle change.

## [v2.4.1] - 2022-07-05

### Added
 - Support for more IRC replies/commands that imply a (forced) nick/handle change.

### Fixed
 - Connecting dialog not disappearing when theme was changed.
 - Client not sending QUIT on manual reconnect or exit via tray.
 - Manual reconnect occasionally failing.
 
### Changed
 - LoadingScreen/connecting dialog is no longer blocking.
 - Console output is less verbose.
 
### Deprecated
 - Removed the weird metadata support timeout thingy, I think ought to just get the full 005 before we try to get moods.
 - Replaced instances of socket.error excepts with OSError, since it's depreciated.

## [v2.4] - 2022-06-30

### Added
 - Error message when server gives forbiddenchannel reply, for example, if the memo name is over the allowed length.
 - Services messages from bots like memoServ now also show up as toasts/notifications.

### Fixed
 - Some text using the system's default color instead of black in the 'pesterchum' theme. (white text on white background)
 - Toasts/Notifications without icons being filled with garbage colors.

### Changed
 - Transitioned from PyQt5 to PyQt6 🌈
    - High-DPI scaling is now enabled, so Pesterchum will be bigger for people with higher resolutions/higher scaling factors.
 - Exception hook is overwriten to give an error message box and create a log instead of always ending the process.

## [v2.3.1] - 2022-06-23

### Added
 - Option to exclude smilies, links, @handles and #memos, from quirks.
 - An example of a gradient function/quirk, "rainbow", that doesn't break smilies/links/@handles/#memos. (see gradient.py in the quirks folder) 
 - Disconnect reasons are now shown if the server closes the connection via ERROR message or erroneusnickname reply.
    - This includes ban reasons if a user is banned by a server, or kick reason if the handle contains a disallowed phrase or character.
 - More allowed PESTERCHUM: values to the pesterchum message tag.
 
### Fixed
 - Obtuse warning for 'i' time.
 - Incorrect handling for certain connection exceptions.
 - Bbcode and html logs not being written until the memo tab was closed, would sometimes cause the log not to write at all if Pesterchum crashed.
 
### Changed
 - Socket stuff... 💀

## [v2.3] - 2022-06-06

### Added
 - Support for "CLIENTINFO", "PING" and "SOURCE" CTCP messages.
 - Support for a "GETMOOD" CTCP message which causes the client to return its mood. Currently this isn't used for anything.
 - Limited support for IRC metadata as defined by the [temporary draft specification](https://gist.github.com/k4bek4be/92c2937cefd49990fbebd001faf2b237).
    - Client now sets its own 'mood' metadata key to its mood. (``METADATA * set mood [mood_num]``)
    - Moods are now received via ``METADATA * SUB mood`` and retrieved via ``METADATA [handle] GET mood`` by default, unlike the current GETMOOD PRIVMSG system, this doesn't have the potential to leak your chumroll, trollslum, and people you message to IRC onlookers. 
       - If the server returns ERR_KEYNOTSET, ERR_KEYNOPERMISSION, or ERR_NOMATCHINGKEY, the requestee is probably running an older client, in which case a normal GETMOOD PRIVMSG  is send.
       - If the server hasn't confirmed support for METADATA via ISUPPORT, the GETMOOD message is used after a small timeout.
 - Limited support for [message tags](https://ircv3.net/irc/#message-tags). The client requests the capability by default and strips unused tags.
    - The only supported message tag currently is the '+pesterchum' client tag, which requires a server module for UnrealIRCd to forward it: https://github.com/Dpeta/pesterchum-tag. The tag has its own capability which is always requested from the server. If the server supports the module an alternative to the usual ``PESTERCHUM:BEGIN``, ``PESTERCHUM:CEASE``, ``PESTERCHUM:BLOCK``, ``PESTERCHUM:TIME``, and ``COLOR >`` PRIVMSG can be send to the client in the form of a [TAGMSG](https://ircv3.net/specs/extensions/message-tags#the-tagmsg-tag-only-message).
       - If enough clients support this, it might be feasible to use this as the default method. Unlike the usual PRIVMSG, the tag is only send to clients who have negotiated the message-tags and pesterchum-tag capability with the server and thus support it, so it won't show up as garbage for IRC users.
    

## [v2.2.3] - 2022-05-06

### Changed
 - Added empty 'package' option to 'setup' in setup.py, setuptools v61.0.0 doesn't seem to like our project layout anymore.
 - Qt's startSystemMove() is used to move Pesterchum's main window now. (system-specific move operation)
    - This fixes click-and-drag on Wayland, which doesn't support setting window position via setPosition().
    - Still falls back on legacy code if startSystemMove is not supported.
 - Rewrote pyinstaller.py

### Fixed
 - Unreadable input on MacOS and certain linux distros for themes which didn't explicitly set input color (incl. pesterchum), input color is now black by default instead of being platform-dependent.
 - Logging related crash.
 
## [v2.2.2] - 2022-04-11

### Changed
 - Removed unused imports.
 - Removed unused variables.
 - Made some 'from X import *' imports explicit.

### Fixed
 - Timeline overflow conditions, time is now replaced with platform max/min on OverflowError.
 - Some accidental redefinitions. (modesUpdated function got overwriten by modesUpdated QtCore.pyqtSignal, 'time' module got overwriten by 'time' variable, etc.)
 - A few broken conditions that didn't usually occur.

## [v2.2.1] - 2022-03-26

### Fixed
 - Crash when datadir is missing :"3

## [v2.2] - 2022-03-24

### Added
 - Ban/kick reasons to message box popup.
 - Occasional profile/pesterchum.js backups are now saved to /backup/, since they have a tendency to blank very rarely for some people.

### Fixed
 - Crash when opening logviewer from memo or convo.
 - Smiley-related file descriptor/handle leak, this would crash when you had too many tabs open.
    - macOS has a comparatively low ulimit, so this limit could be reached very easily. (~>10 tabs)
 - Added fallback for if the server passes an unsupported amount of parameters for a command, should no longer cause a crash.
 - Added fallbacks for invalid profiles & json loading problems, should cause a crash less often and display a descriptive message.
    - Invalid profiles are now pruned from list when switching profiles. (would cause a crash previously)
 - RPL_CHANNELMODEIS function missing the mode_params parameter. (Pesterchum doesn't actually do anything with it, but previously it'd cause a crash when the server tried to pass it.)
 
### Changed
 - Animated emotes should work on macOS now if they didn't before.
 - On macOS, file descriptors for logs are now closed after write to prevent reaching the ulimit, this is probably bad for performance.
 - Some imports are reorganized.
 - Now using select module for sockets, should hopefully make random connection errors/broken pipes a bit less common.
 - Failed socket write operations are now tried 5 times before connection is reset.

### Deprecated
 - Replaced imp module with importlib.util, imp has been deprecated since Python 3.4
 - Removed some Python 2 related checks. (py2 is not supported)
 - Disabled checking for "pynotify" module, implementation was broken.
 - Disabled "luaquirks" module, implementation was broken, this might be worth fixing, though I'm not aware of anyone that's ever used it.

## [v2.1.3.3] - 2021-12-1

### Fixed
 - Attempt at fixing up logging.

## [v2.1.3.2] - 2021-12-1

### Fixed
 - Crash for certain invalid values of PESTERCHUM:TIME>
 - Fixed invalid group name causing a crash
 - "Fixed" toast related mac crash?
 - Re-enabled include_msvcr for setup.py (Should hopefully actually work now)

## [v2.1.3.1] - 2021-8-24

### Added
 - Memo messages for the following channel modes: zMQNRODGPCrR (see https://www.unrealircd.org/docs/Channel_Modes for info)
    - (Memo messages for registration is pretty much the only useful one out of these.)
 - More comprehensive logging for DEBUG (Might be a bit obtuse so I'll probably make it more consistent later).

### Fixed
 - Rewrote channel mode function to fix crash when user and channel modes were set in a single command, this also fixes:
    - Crash when being the only person in a non-persistent memo you own while having autoop enabled (with nickServ). 

## [v2.1.3] - 2021-8-09

### Added
- pyinstaller.py script to make building with pyinstaller more convenient.
- Themes by cubicSimulation.
- Link to server rules under help.

### Fixed
- Crash when opening invite-only memo. (My bad-)
- Random encounters occasionally not being disabled when switched off. (RE bot is now updated after connect and on profile switch.)
- A few memo/convo related syntax errors in a few themes.
- nothing.png being missing in some themes.
- 64-bit crt for PyInstaller.
- Manual chumroll sorting not working.

### Changed
- Honk emote now only triggers when typing ':honk:' instead of on every 'honk'.
- Logging is now configured in logging.conf and logs are also writen to pesterchum.log by default.
- Warnings/Errors are now logged to pesterchum.log as well as console.

## [v2.1.2] - 2021-4-16

### Added
- Added HOSTSERV and BOTSERV to BOTNAMES.

### Fixed
- Colors in direct messages sometimes not working.
- Handles sometimes not showing up in chumroll or trollslum.

### Removed
- Separate handling for canon handles on chumroll because it was buggy and unneeded.

### Changed
- setup.py build description to just "Pesterchum"
- Made file capitalization consistent for a few files. (.PNG --> .png), because some file systems are queasy on that, and it wasn't working on Debian. (See https://superuser.com/questions/881804/case-sensitive-file-extensions-in-windows-and-linux) 

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
