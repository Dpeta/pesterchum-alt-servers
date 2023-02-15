"""Renamed from 'profile.py' to avoid conflict with standard library 'profile' module."""
import os
import sys
import json
import re
import codecs
import shutil
import zipfile
import logging
from string import Template
from datetime import datetime
from time import strftime

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    print("PyQt5 fallback (profile.py)")
    from PyQt5 import QtCore, QtGui, QtWidgets

import ostools
from mood import Mood
from dataobjs import PesterProfile, pesterQuirks
from parsetools import convertTags

_datadir = ostools.getDataDir()
PchumLog = logging.getLogger("pchumLogger")


class PesterLog:
    def __init__(self, handle, parent=None):
        global _datadir
        self.parent = parent
        self.handle = handle
        self.convos = {}
        self.logpath = _datadir + "logs"

    def log(self, handle, msg):
        if self.parent.config.time12Format():
            log_time = strftime("[%I:%M")
        else:
            log_time = strftime("[%H:%M")
        if self.parent.config.showSeconds():
            log_time += strftime(":%S] ")
        else:
            log_time += "] "
        if handle[0] == "#":
            if not self.parent.config.logMemos() & self.parent.config.LOG:
                return
            if not self.parent.config.logMemos() & self.parent.config.STAMP:
                log_time = ""
        else:
            if not self.parent.config.logPesters() & self.parent.config.LOG:
                return
            if not self.parent.config.logPesters() & self.parent.config.STAMP:
                log_time = ""
        if self.parent.isBot(handle):
            return
        # watch out for illegal characters
        handle = re.sub(r'[<>:"/\\|?*]', "_", handle)
        bbcodemsg = log_time + convertTags(msg, "bbcode")
        html = log_time + convertTags(msg, "html") + "<br />"
        msg = log_time + convertTags(msg, "text")
        modes = {"bbcode": bbcodemsg, "html": html, "text": msg}
        try:
            if handle not in self.convos:
                log_time = datetime.now().strftime("%Y-%m-%d.%H.%M")
                self.convos[handle] = {}
                for format, t in modes.items():
                    if not os.path.exists(
                        "{}/{}/{}/{}".format(self.logpath, self.handle, handle, format)
                    ):
                        os.makedirs(
                            "{}/{}/{}/{}".format(
                                self.logpath, self.handle, handle, format
                            )
                        )
                    fp = codecs.open(
                        "%s/%s/%s/%s/%s.%s.txt"
                        % (self.logpath, self.handle, handle, format, handle, log_time),
                        encoding="utf-8",
                        mode="a",
                    )
                    self.convos[handle][format] = fp

            for format, t in modes.items():
                f = self.convos[handle][format]
                f.write(t + "\r\n")
                # flush + fsync force a write,
                # makes sure logs are saved in the case of a crash.
                f.flush()
                os.fsync(f.fileno())

            # This way the file descriptors are closed and reopened for every message,
            # which is sub-optimal and definitely a performance drain but,
            # otherwise we still run into the ulimit on platforms like MacOS fairly easily.
            # if ostools.isOSX() == True:
            #    for (format, t) in modes.items():
            #        self.finish(handle)

        except (OSError, KeyError, IndexError, ValueError) as e:
            # Catching this exception does not stop pchum from dying if we run out of file handles </3
            PchumLog.critical(e)
            errmsg = QtWidgets.QMessageBox()
            errmsg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            errmsg.setText(
                "Warning: Pesterchum could not open the log file for %s!" % (handle)
            )
            errmsg.setInformativeText(
                "Your log for %s will not be saved because something went wrong. We suggest restarting Pesterchum. Sorry :("
                % (handle)
                + "\n"
                + str(e)
            )
            errmsg.setWindowTitle(":(")
            errmsg.exec()
            PchumLog.debug("post-error msg")

    def finish(self, handle):
        if handle not in self.convos:
            return
        for f in list(self.convos[handle].values()):
            f.close()
        del self.convos[handle]

    def close(self):
        for h in list(self.convos.keys()):
            for f in list(self.convos[h].values()):
                f.close()


class userConfig:
    def __init__(self, parent):
        self.parent = parent
        # Use for bit flag log setting
        self.LOG = 1
        self.STAMP = 2
        # Use for bit flag blink
        self.PBLINK = 1
        self.MBLINK = 2
        # Use for bit flag notfications
        self.SIGNIN = 1
        self.SIGNOUT = 2
        self.NEWMSG = 4
        self.NEWCONVO = 8
        self.INITIALS = 16
        self.filename = _datadir + "pesterchum.js"
        try:
            with open(self.filename) as fp:
                self.config = json.load(fp)
        except json.decoder.JSONDecodeError as e:
            PchumLog.critical("ohno :(")
            PchumLog.critical("failed to load pesterchum.js")
            PchumLog.critical(e)
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setWindowTitle(":(")
            msgbox.setTextFormat(QtCore.Qt.TextFormat.RichText)  # Clickable html links
            msgbox.setInformativeText(
                "<html><h3>Failed to load pesterchum.js, this might require manual intervention.<br><br>\
Consider overriding: <a href='%s'>%s</a> <br>\
with a backup from: <a href='%s'>%s</a></h3></html>"
                % (
                    _datadir,
                    self.filename,
                    os.path.join(_datadir, "backup"),
                    os.path.join(_datadir, "backup"),
                )
            )
            msgbox.exec()
            sys.exit()

        # Trying to fix:
        #     IOError: [Errno 2]
        #     No such file or directory:
        #     u'XXX\\AppData\\Local\\pesterchum/profiles/XXX.js'
        # Part 2 :(
        if "defaultprofile" in self.config:
            try:
                self.userprofile = userProfile(self.config["defaultprofile"])
            except:
                self.userprofile = None
        else:
            self.userprofile = None

        self.logpath = _datadir + "logs"

        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)
        try:
            with open("%s/groups.js" % (self.logpath)) as fp:
                self.groups = json.load(fp)
        except (OSError, ValueError):
            self.groups = {}
            with open("%s/groups.js" % (self.logpath), "w") as fp:
                json.dump(self.groups, fp)

        self.backup()

    def backup(self):
        # Backups

        try:
            # Backup pesterchum.js file.
            # Useful because it seems to randomly get blanked for people.
            backup_path = os.path.join(_datadir, "backup")
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            current_backup = datetime.now().day % 5
            shutil.copyfile(
                self.filename,
                os.path.join(
                    backup_path, "pesterchum.backup-" + str(current_backup) + ".js"
                ),
            )

            # Backup profiles.
            # Useful because people don't know how to add underscores to handles.
            profile_path = os.path.join(_datadir, "profiles")
            profile_list = os.listdir(profile_path)
            with zipfile.ZipFile(
                os.path.join(backup_path, "profiles.backup-" + str(current_backup))
                + ".zip",
                "w",
            ) as pzip:
                for x in profile_list:
                    if x.endswith(".js"):
                        with open(self.filename) as f:
                            pzip.writestr(x, f.read())

            PchumLog.info("Updated backups-%s.", current_backup)
        except shutil.Error as e:
            PchumLog.warning("Failed to make backup, shutil error?\n%s", e)
        except zipfile.BadZipFile as e:
            PchumLog.warning("Failed to make backup, BadZipFile?\n%s", e)
        except OSError as e:
            PchumLog.warning("Failed to make backup, no permission?\n%s", e)

    def chums(self):
        if "chums" not in self.config:
            self.set("chums", [])
        return self.config.get("chums", [])

    def setChums(self, newchums):
        with open(self.filename) as fp:
            # what if we have two clients open??
            newconfig = json.load(fp)
        oldchums = newconfig["chums"]
        # Time to merge these two! :OOO
        for c in list(set(oldchums) - set(newchums)):
            newchums.append(c)

        self.set("chums", newchums)

    def hideOfflineChums(self):
        return self.config.get("hideOfflineChums", False)

    def defaultprofile(self):
        try:
            return self.config["defaultprofile"]
        except KeyError:
            return None

    def tabs(self):
        return self.config.get("tabs", True)

    def tabMemos(self):
        if "tabmemos" not in self.config:
            self.set("tabmemos", self.tabs())
        return self.config.get("tabmemos", True)

    def showTimeStamps(self):
        if "showTimeStamps" not in self.config:
            self.set("showTimeStamps", True)
        return self.config.get("showTimeStamps", True)

    def time12Format(self):
        if "time12Format" not in self.config:
            self.set("time12Format", True)
        return self.config.get("time12Format", True)

    def showSeconds(self):
        if "showSeconds" not in self.config:
            self.set("showSeconds", False)
        return self.config.get("showSeconds", False)

    def sortMethod(self):
        return self.config.get("sortMethod", 0)

    def useGroups(self):
        return self.config.get("useGroups", False)

    def openDefaultGroup(self):
        groups = self.getGroups()
        for g in groups:
            if g[0] == "Chums":
                return g[1]
        return True

    def showEmptyGroups(self):
        if "emptyGroups" not in self.config:
            self.set("emptyGroups", False)
        return self.config.get("emptyGroups", False)

    def showOnlineNumbers(self):
        if "onlineNumbers" not in self.config:
            self.set("onlineNumbers", False)
        return self.config.get("onlineNumbers", False)

    def logPesters(self):
        return self.config.get("logPesters", self.LOG | self.STAMP)

    def logMemos(self):
        return self.config.get("logMemos", self.LOG)

    def disableUserLinks(self):
        return not self.config.get("userLinks", True)

    def idleTime(self):
        return self.config.get("idleTime", 10)

    def minimizeAction(self):
        return self.config.get("miniAction", 0)

    def closeAction(self):
        return self.config.get("closeAction", 1)

    def opvoiceMessages(self):
        return self.config.get("opvMessages", True)

    def animations(self):
        return self.config.get("animations", True)

    # def checkForUpdates(self):
    #    u = self.config.get('checkUpdates', 0)
    #    if type(u) == type(bool()):
    #        if u: u = 2
    #        else: u = 3
    #    return u
    #    # Once a day
    #    # Once a week
    #    # Only on start
    #    # Never
    # def lastUCheck(self):
    #    return self.config.get('lastUCheck', 0)
    # def checkMSPA(self):
    #    return self.config.get('mspa', False)
    def blink(self):
        return self.config.get("blink", self.PBLINK | self.MBLINK)

    def notify(self):
        return self.config.get("notify", True)

    def notifyType(self):
        return self.config.get("notifyType", "default")

    def notifyOptions(self):
        return self.config.get(
            "notifyOptions", self.SIGNIN | self.NEWMSG | self.NEWCONVO | self.INITIALS
        )

    def irc_compatibility_mode(self):
        return self.config.get("irc_compatibility_mode", False)

    def ghostchum(self):
        return self.config.get("ghostchum", False)

    def addChum(self, chum):
        if chum.handle not in self.chums():
            with open(self.filename) as fp:
                # what if we have two clients open??
                newconfig = json.load(fp)
            newchums = newconfig["chums"] + [chum.handle]
            self.set("chums", newchums)

    def removeChum(self, chum):
        if isinstance(chum, PesterProfile):
            handle = chum.handle
        else:
            handle = chum
        newchums = [c for c in self.config["chums"] if c != handle]
        self.set("chums", newchums)

    def getBlocklist(self):
        if "block" not in self.config:
            self.set("block", [])
        return self.config["block"]

    def addBlocklist(self, handle):
        l = self.getBlocklist()
        if handle not in l:
            l.append(handle)
            self.set("block", l)

    def delBlocklist(self, handle):
        l = self.getBlocklist()
        l.pop(l.index(handle))
        self.set("block", l)

    def getGroups(self):
        if "groups" not in self.groups:
            self.saveGroups([["Chums", True]])
        return self.groups.get("groups", [["Chums", True]])

    def addGroup(self, group, open=True):
        l = self.getGroups()
        exists = False
        for g in l:
            if g[0] == group:
                exists = True
                break
        if not exists:
            l.append([group, open])
            l.sort()
            self.saveGroups(l)

    def delGroup(self, group):
        l = self.getGroups()
        i = 0
        for g in l:
            if g[0] == group:
                break
            i = i + 1
        l.pop(i)
        l.sort()
        self.saveGroups(l)

    def expandGroup(self, group, open=True):
        l = self.getGroups()
        for g in l:
            if g[0] == group:
                g[1] = open
                break
        self.saveGroups(l)

    def saveGroups(self, groups):
        self.groups["groups"] = groups
        try:
            jsonoutput = json.dumps(self.groups)
        except ValueError as e:
            raise e
        with open("%s/groups.js" % (self.logpath), "w") as fp:
            fp.write(jsonoutput)

    def server(self):
        if hasattr(self.parent, "serverOverride"):
            return self.parent.serverOverride
        try:
            with open(_datadir + "server.json") as server_file:
                read_file = server_file.read()
                server_obj = json.loads(read_file)
            return server_obj["server"]
        except:
            PchumLog.exception("Failed to load server, falling back to default.")
            try:
                with open(_datadir + "server.json", "w") as server_file:
                    json_server_file = {
                        "server": "irc.pesterchum.xyz",
                        "port": "6697",
                        "TLS": True,
                    }
                    server_file.write(json.dumps(json_server_file, indent=4))
                server = "irc.pesterchum.xyz"
            except:
                return self.config.get("server", "irc.pesterchum.xyz")

    def port(self):
        if hasattr(self.parent, "portOverride"):
            return self.parent.portOverride
        try:
            with open(_datadir + "server.json") as server_file:
                read_file = server_file.read()
            server_obj = json.loads(read_file)
            port = server_obj["port"]
            return port
        except:
            PchumLog.exception("Failed to load port, falling back to default.")
            return self.config.get("port", "6697")

    def ssl(self):
        # if hasattr(self.parent, 'tlsOverride'):
        #    return self.parent.tlsOverride
        try:
            with open(_datadir + "server.json") as server_file:
                read_file = server_file.read()
            server_obj = json.loads(read_file)
            return server_obj["TLS"]
        except:
            PchumLog.exception("Failed to load TLS setting, falling back to default.")
            return self.config.get("TLS", True)

    def password(self):
        try:
            with open(_datadir + "server.json") as server_file:
                read_file = server_file.read()
            server_obj = json.loads(read_file)
            password = ""
            if "pass" in server_obj:
                password = server_obj["pass"]
            return password
        except:
            PchumLog.exception("Failed to load TLS setting, falling back to default.")
            return self.config.get("TLS", True)

    def soundOn(self):
        if "soundon" not in self.config:
            self.set("soundon", True)
        return self.config["soundon"]

    def chatSound(self):
        return self.config.get("chatSound", True)

    def memoSound(self):
        return self.config.get("memoSound", True)

    def memoPing(self):
        return self.config.get("pingSound", True)

    def nameSound(self):
        return self.config.get("nameSound", True)

    def volume(self):
        return self.config.get("volume", 100)

    def trayMessage(self):
        return self.config.get("traymsg", True)

    def set(self, item, setting):
        self.config[item] = setting
        try:
            jsonoutput = json.dumps(self.config)
        except ValueError as e:
            raise e
        with open(self.filename, "w") as fp:
            fp.write(jsonoutput)

    def availableThemes(self):
        themes = []
        # Load user themes.
        for dirname, dirnames, filenames in os.walk(_datadir + "themes"):
            for d in dirnames:
                themes.append(d)
        # Also load embedded themes.
        if _datadir:
            for dirname, dirnames, filenames in os.walk("themes"):
                for d in dirnames:
                    if d not in themes:
                        themes.append(d)
        themes.sort()
        return themes

    def availableProfiles(self):
        profs = []
        profileloc = _datadir + "profiles"
        for dirname, dirnames, filenames in os.walk(profileloc):
            for filename in filenames:
                l = len(filename)
                if filename[l - 3 : l] == ".js":
                    profs.append(filename[0 : l - 3])
        profs.sort()
        PchumLog.info("Profiles: %s", profs)

        # Validity check
        PchumLog.info("Starting profile check. . .")
        for x in profs:
            c_profile = os.path.join(profileloc, x + ".js")
            try:
                json.load(open(c_profile))
                PchumLog.info("%s: Pass.", x)
            except json.JSONDecodeError as e:
                PchumLog.warning("%s: Fail.", x)
                PchumLog.warning(e)
                profs.remove(x)
                PchumLog.warning("%s removed from profile list.", x)

                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msgBox.setWindowTitle(":(")
                msgBox.setTextFormat(
                    QtCore.Qt.TextFormat.RichText
                )  # Clickable html links
                self.filename = _datadir + "pesterchum.js"
                msgBox.setText(
                    "<html><h3>Failed to load "
                    + x
                    + ", removed from list."
                    + "<br><br>Consider taking a look at: <a href="
                    + profileloc
                    + ">"
                    + os.path.join(profileloc, x + ".js")
                    + "</a>"
                    + "<br><br>"
                    + str(e)
                    + r"<\h3><\html>"
                )
                # "\" if pesterchum acts oddly you might want to try backing up and then deleting \"" + \
                # _datadir+"pesterchum.js" + \
                # "\"")
                PchumLog.critical(e)
                msgBox.exec()

        return [userProfile(p) for p in profs]


class userProfile:
    def __init__(self, user):
        self.profiledir = _datadir + "profiles"

        if isinstance(user, PesterProfile):
            self.chat = user
            self.userprofile = {
                "handle": user.handle,
                "color": str(user.color.name()),
                "quirks": [],
                "theme": "pesterchum",
            }
            self.theme = pesterTheme("pesterchum")
            self.chat.mood = Mood(self.theme["main/defaultmood"])
            self.lastmood = self.chat.mood.value()
            self.quirks = pesterQuirks([])
            self.randoms = False
            initials = self.chat.initials()
            if len(initials) >= 2:
                initials = (
                    initials,
                    "{}{}".format(initials[0].lower(), initials[1]),
                    "{}{}".format(initials[0], initials[1].lower()),
                )
                self.mentions = [r"\b(%s)\b" % ("|".join(initials))]
            else:
                self.mentions = []
            self.autojoins = []
        else:
            # Trying to fix:
            #     IOError: [Errno 2]
            #     No such file or directory:
            #     u'XXX\\AppData\\Local\\pesterchum/profiles/XXX.js'
            # Part 3 :(
            try:
                with open("{}/{}.js".format(self.profiledir, user)) as fp:
                    self.userprofile = json.load(fp)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msgBox.setWindowTitle(":(")
                msgBox.setTextFormat(
                    QtCore.Qt.TextFormat.RichText
                )  # Clickable html links
                self.filename = _datadir + "pesterchum.js"
                msgBox.setText(
                    "<html><h3>Failed to load: "
                    + (
                        "<a href='%s'>%s/%s.js</a>"
                        % (self.profiledir, self.profiledir, user)
                    )
                    + "<br><br> Try to check for syntax errors if the file exists."
                    + "<br><br>If you got this message at launch you may want to change your default profile."
                    + "<br><br>"
                    + str(e)
                    + r"<\h3><\html>"
                )
                # "\" if pesterchum acts oddly you might want to try backing up and then deleting \"" + \
                # _datadir+"pesterchum.js" + \
                # "\"")
                PchumLog.critical(e)
                msgBox.exec()
                raise ValueError(e)

            try:
                self.theme = pesterTheme(self.userprofile["theme"])
            except ValueError:
                self.theme = pesterTheme("pesterchum")
            self.lastmood = self.userprofile.get(
                "lastmood", self.theme["main/defaultmood"]
            )
            self.chat = PesterProfile(
                self.userprofile["handle"],
                QtGui.QColor(self.userprofile["color"]),
                Mood(self.lastmood),
            )
            self.quirks = pesterQuirks(self.userprofile["quirks"])
            if "randoms" not in self.userprofile:
                self.userprofile["randoms"] = False
            self.randoms = self.userprofile["randoms"]
            if "mentions" not in self.userprofile:
                initials = self.chat.initials()
                if len(initials) >= 2:
                    initials = (
                        initials,
                        "{}{}".format(initials[0].lower(), initials[1]),
                        "{}{}".format(initials[0], initials[1].lower()),
                    )
                    self.userprofile["mentions"] = [r"\b(%s)\b" % ("|".join(initials))]
                else:
                    self.userprofile["mentions"] = []
            self.mentions = self.userprofile["mentions"]
            if "autojoins" not in self.userprofile:
                self.userprofile["autojoins"] = []
            self.autojoins = self.userprofile["autojoins"]

        try:
            with open(_datadir + "passwd.js") as fp:
                self.passwd = json.load(fp)
        except:
            self.passwd = {}
        self.autoidentify = False
        self.nickservpass = ""
        if self.chat.handle in self.passwd:
            # Fix for:
            # Traceback (most recent call last):
            # File "pesterchum.py", line 2944, in nickCollision
            #   File "pesterchum.py", line 1692, in changeProfile
            #   File "XXX\menus.py", line 795, in init
            #   File "XXX\profile.py", line 350, in availableProfiles
            #   File "XXX\profile.py", line 432, in init
            # KeyError: 'pw'
            if "auto" in self.passwd[self.chat.handle]:
                self.autoidentify = self.passwd[self.chat.handle]["auto"]
            if "pw" in self.passwd[self.chat.handle]:
                self.nickservpass = self.passwd[self.chat.handle]["pw"]

    def setMood(self, mood):
        self.chat.mood = mood

    def setTheme(self, theme):
        self.theme = theme
        self.userprofile["theme"] = theme.name
        self.save()

    def setColor(self, color):
        self.chat.color = color
        self.userprofile["color"] = str(color.name())
        self.save()

    def setQuirks(self, quirks):
        self.quirks = quirks
        self.userprofile["quirks"] = self.quirks.plainList()
        self.save()

    def getRandom(self):
        return self.randoms

    def setRandom(self, random):
        self.randoms = random
        self.userprofile["randoms"] = random
        self.save()

    def getMentions(self):
        return self.mentions

    def setMentions(self, mentions):
        i = None
        try:
            for i, m in enumerate(mentions):
                re.compile(m)
        except re.error as e:
            PchumLog.error("#%s Not a valid regular expression: %s", i, e)
        else:
            self.mentions = mentions
            self.userprofile["mentions"] = mentions
            self.save()

    def getLastMood(self):
        return self.lastmood

    def setLastMood(self, mood):
        self.lastmood = mood.value()
        self.userprofile["lastmood"] = self.lastmood
        self.save()

    def getTheme(self):
        return self.theme

    def getAutoIdentify(self):
        return self.autoidentify

    def setAutoIdentify(self, b):
        self.autoidentify = b
        if self.chat.handle not in self.passwd:
            self.passwd[self.chat.handle] = {}
        self.passwd[self.chat.handle]["auto"] = b
        self.saveNickServPass()

    def getNickServPass(self):
        return self.nickservpass

    def setNickServPass(self, pw):
        self.nickservpass = pw
        if self.chat.handle not in self.passwd:
            self.passwd[self.chat.handle] = {}
        self.passwd[self.chat.handle]["pw"] = pw
        self.saveNickServPass()

    def getAutoJoins(self):
        return self.autojoins

    def setAutoJoins(self, autojoins):
        self.autojoins = autojoins
        self.userprofile["autojoins"] = self.autojoins
        self.save()

    def save(self):
        handle = self.chat.handle
        if handle[0:12] == "pesterClient":
            # dont save temp profiles
            return
        try:
            jsonoutput = json.dumps(self.userprofile)
        except ValueError as e:
            raise e
        with open("{}/{}.js".format(self.profiledir, handle), "w") as fp:
            fp.write(jsonoutput)

    def saveNickServPass(self):
        # remove profiles with no passwords
        for h, t in list(self.passwd.items()):
            if "auto" not in t and ("pw" not in t or t["pw"] == ""):
                del self.passwd[h]
        try:
            jsonoutput = json.dumps(self.passwd, indent=4)
        except ValueError as e:
            raise e
        with open(_datadir + "passwd.js", "w") as fp:
            fp.write(jsonoutput)

    @staticmethod
    def newUserProfile(chatprofile):
        if os.path.exists("{}/{}.js".format(_datadir + "profiles", chatprofile.handle)):
            newprofile = userProfile(chatprofile.handle)
        else:
            newprofile = userProfile(chatprofile)
            newprofile.save()
        return newprofile


class PesterProfileDB(dict):
    def __init__(self):
        self.logpath = _datadir + "logs"

        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)
        try:
            with open("%s/chums.js" % (self.logpath)) as fp:
                chumdict = json.load(fp)
        except (OSError, ValueError):
            # karxi: This code feels awfully familiar....
            chumdict = {}
            with open("%s/chums.js" % (self.logpath), "w") as fp:
                json.dump(chumdict, fp)

        u = []
        for handle, c in chumdict.items():
            options = {}
            if "group" in c:
                options["group"] = c["group"]
            if "notes" in c:
                options["notes"] = c["notes"]
            if "color" not in c:
                c["color"] = "#000000"
            if "mood" not in c:
                c["mood"] = "offline"
            u.append(
                (
                    handle,
                    PesterProfile(
                        handle,
                        color=QtGui.QColor(c["color"]),
                        mood=Mood(c["mood"]),
                        **options,
                    ),
                )
            )
        converted = dict(u)
        self.update(converted)

    def save(self):
        try:
            with open("%s/chums.js" % (self.logpath), "w") as fp:
                chumdict = dict([p.plaindict() for p in self.values()])
                json.dump(chumdict, fp)
        except Exception as e:
            raise e

    def getColor(self, handle, default=None):
        if handle not in self:
            return default
        else:
            return self[handle].color

    def setColor(self, handle, color):
        if handle in self:
            self[handle].color = color
        else:
            self[handle] = PesterProfile(handle, color)

    def getGroup(self, handle, default="Chums"):
        if handle not in self:
            return default
        else:
            return self[handle].group

    def setGroup(self, handle, theGroup):
        if handle in self:
            self[handle].group = theGroup
        else:
            self[handle] = PesterProfile(handle, group=theGroup)
        self.save()

    def getNotes(self, handle, default=""):
        if handle not in self:
            return default
        else:
            return self[handle].notes

    def setNotes(self, handle, notes):
        if handle in self:
            self[handle].notes = notes
        else:
            self[handle] = PesterProfile(handle, notes=notes)
        self.save()

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        self.save()


class pesterTheme(dict):
    def __init__(self, name, default=False):
        possiblepaths = (
            _datadir + "themes/%s" % (name),
            "themes/%s" % (name),
            _datadir + "themes/pesterchum",
            "themes/pesterchum",
        )
        self.path = "themes/pesterchum"
        for p in possiblepaths:
            if os.path.exists(p):
                self.path = p
                break

        self.name = name
        try:
            with open(self.path + "/style.js") as fp:
                theme = json.load(fp, object_hook=self.pathHook)
        except OSError:
            theme = json.loads("{}")
        self.update(theme)
        if "inherits" in self:
            self.inheritedTheme = pesterTheme(self["inherits"])
        if not default:
            self.defaultTheme = pesterTheme("pesterchum", default=True)

    def __getitem__(self, key):
        keys = key.split("/")
        try:
            v = super().__getitem__(keys.pop(0))
        except KeyError as e:
            if hasattr(self, "inheritedTheme"):
                return self.inheritedTheme[key]
            elif hasattr(self, "defaultTheme"):
                return self.defaultTheme[key]
            else:
                raise e
        for k in keys:
            try:
                v = v[k]
            except KeyError as e:
                if hasattr(self, "inheritedTheme"):
                    return self.inheritedTheme[key]
                elif hasattr(self, "defaultTheme"):
                    return self.defaultTheme[key]
                else:
                    raise e
        return v

    def pathHook(self, d):
        for k, v in d.items():
            if isinstance(v, str):
                s = Template(v)
                d[k] = s.safe_substitute(path=self.path)
        return d

    def get(self, key, default):
        keys = key.split("/")
        try:
            v = super().__getitem__(keys.pop(0))
            for k in keys:
                v = v[k]
            return default if v is None else v
        except KeyError:
            if hasattr(self, "inheritedTheme"):
                return self.inheritedTheme.get(key, default)
            else:
                return default

    def has_key(self, key):
        keys = key.split("/")
        try:
            v = super().__getitem__(keys.pop(0))
            for k in keys:
                v = v[k]
            return v is not None
        except KeyError:
            if hasattr(self, "inheritedTheme"):
                return key in self.inheritedTheme
            else:
                return False
