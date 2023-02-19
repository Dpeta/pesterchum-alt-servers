import logging

PchumLog = logging.getLogger("pchumLogger")
try:
    from PyQt6 import QtGui
except ImportError:
    print("PyQt5 fallback (dataobjs.py)")
    from PyQt5 import QtGui
from datetime import datetime
import re
import random

from mood import Mood
from parsetools import (
    timeDifference,
    convertTags,
    lexMessage,
    parseRegexpFunctions,
    smiledict,
)
from mispeller import mispeller

_urlre = re.compile(r"(?i)(?:^|(?<=\s))(?:(?:https?|ftp)://|magnet:)[^\s]+")
# _url2re = re.compile(r"(?i)(?<!//)\bwww\.[^\s]+?\.")
_groupre = re.compile(r"\\([0-9]+)")
_upperre = re.compile(r"upper\(([\w<>\\]+)\)")
_lowerre = re.compile(r"lower\(([\w<>\\]+)\)")
_scramblere = re.compile(r"scramble\(([\w<>\\]+)\)")
_reversere = re.compile(r"reverse\(([\w<>\\]+)\)")
_ctagre = re.compile("(</?c=?.*?>)", re.I)
_smilere = re.compile("|".join(list(smiledict.keys())))
_memore = re.compile(r"(\s|^)(#[A-Za-z0-9_]+)")
_handlere = re.compile(r"(\s|^)(@[A-Za-z0-9_]+)")


class pesterQuirk:
    def __init__(self, quirk):
        if not isinstance(quirk, dict):
            raise ValueError("Quirks must be given a dictionary")
        self.quirk = quirk
        self.type = self.quirk["type"]
        if "on" not in self.quirk:
            self.quirk["on"] = True
        self.on = self.quirk["on"]
        if "group" not in self.quirk:
            self.quirk["group"] = "Miscellaneous"
        self.group = self.quirk["group"]
        try:
            self.checkstate = self.quirk["checkstate"]
        except KeyError:
            pass

    def apply(self, string, first=False, last=False):
        if not self.on:
            return string
        elif self.type == "prefix":
            return self.quirk["value"] + string
        elif self.type == "suffix":
            return string + self.quirk["value"]
        elif self.type == "replace":
            return string.replace(self.quirk["from"], self.quirk["to"])
        elif self.type == "regexp":
            fr = self.quirk["from"]
            if not first and len(fr) > 0 and fr[0] == "^":
                return string
            if not last and len(fr) > 0 and fr[len(fr) - 1] == "$":
                return string
            to = self.quirk["to"]
            pt = parseRegexpFunctions(to)
            return re.sub(fr, pt.expand, string)
        elif self.type == "random":
            if len(self.quirk["randomlist"]) == 0:
                return string
            fr = self.quirk["from"]
            if not first and len(fr) > 0 and fr[0] == "^":
                return string
            if not last and len(fr) > 0 and fr[len(fr) - 1] == "$":
                return string

            def randomrep(mo):
                choice = random.choice(self.quirk["randomlist"])
                pt = parseRegexpFunctions(choice)
                return pt.expand(mo)

            return re.sub(self.quirk["from"], randomrep, string)
        elif self.type == "spelling":
            percentage = self.quirk["percentage"] / 100.0
            words = string.split(" ")
            newl = []
            ctag = re.compile("(</?c=?.*?>)", re.I)
            for w in words:
                p = random.random()
                if not ctag.search(w) and p < percentage:
                    newl.append(mispeller(w))
                elif p < percentage:
                    split = ctag.split(w)
                    tmp = []
                    for s in split:
                        if s and not ctag.search(s):
                            tmp.append(mispeller(s))
                        else:
                            tmp.append(s)
                    newl.append("".join(tmp))
                else:
                    newl.append(w)
            return " ".join(newl)

    def __str__(self):
        if self.type == "prefix":
            return "BEGIN WITH: %s" % (self.quirk["value"])
        elif self.type == "suffix":
            return "END WITH: %s" % (self.quirk["value"])
        elif self.type == "replace":
            return "REPLACE {} WITH {}".format(self.quirk["from"], self.quirk["to"])
        elif self.type == "regexp":
            return "REGEXP: {} REPLACED WITH {}".format(
                self.quirk["from"],
                self.quirk["to"],
            )
        elif self.type == "random":
            return "REGEXP: {} RANDOMLY REPLACED WITH {}".format(
                self.quirk["from"],
                [r for r in self.quirk["randomlist"]],
            )
        elif self.type == "spelling":
            return "MISPELLER: %d%%" % (self.quirk["percentage"])


class pesterQuirks:
    def __init__(self, quirklist):
        self.quirklist = []
        for q in quirklist:
            self.addQuirk(q)

    def plainList(self):
        return [q.quirk for q in self.quirklist]

    def addQuirk(self, q):
        if isinstance(q, dict):
            self.quirklist.append(pesterQuirk(q))
        elif isinstance(q, pesterQuirk):
            self.quirklist.append(q)

    def apply(self, lexed, first=False, last=False):
        prefix = [q for q in self.quirklist if q.type == "prefix"]
        # suffix = [q for q in self.quirklist if q.type == "suffix"]

        newlist = []
        for i, o in enumerate(lexed):
            if not isinstance(o, str):
                if i == 0:
                    string = " "
                    for p in prefix:
                        string += p.apply(string)
                    newlist.append(string)
                newlist.append(o)
                continue
            lastStr = i == len(lexed) - 1
            string = o
            for q in self.quirklist:
                try:
                    checkstate = int(q.checkstate)
                except Exception:
                    checkstate = 0

                # Exclude option is checked
                if checkstate == 2:
                    # Check for substring that should be excluded.
                    excludes = []
                    # Check for links, store in list.
                    for match in re.finditer(_urlre, string):
                        excludes.append(match)
                    # Check for smilies, store in list.
                    for match in re.finditer(_smilere, string):
                        excludes.append(match)
                    # Check for @handles, store in list.
                    for match in re.finditer(_handlere, string):
                        excludes.append(match)
                    # Check for #memos, store in list.
                    for match in re.finditer(_memore, string):
                        excludes.append(match)

                    if len(excludes) >= 1:
                        # SORT !!!
                        excludes.sort(key=lambda exclude: exclude.start())
                        # Recursion check.
                        # Strings like http://:3: require this.
                        for n in range(0, len(excludes) - 1):
                            if excludes[n].end() > excludes[n + 1].start():
                                excludes.pop(n)
                        # Seperate parts to be quirked.
                        sendparts = []
                        # Add string until start of exclude at index 0.
                        until = excludes[0].start()
                        sendparts.append(string[:until])
                        # Add strings between excludes.
                        for part in range(1, len(excludes)):
                            after = excludes[part - 1].end()
                            until = excludes[part].start()
                            sendparts.append(string[after:until])
                        # Add string after exclude at last index.
                        after = excludes[-1].end()
                        sendparts.append(string[after:])

                        # Quirk to-be-quirked parts.
                        recvparts = []
                        for part in sendparts:
                            # No split, apply like normal.
                            if q.type in ("regexp", "random"):
                                recvparts.append(
                                    q.apply(part, first=(i == 0), last=lastStr)
                                )
                            elif q.type == "prefix" and i == 0:
                                recvparts.append(q.apply(part))
                            elif q.type == "suffix" and lastStr:
                                recvparts.append(q.apply(part))
                            else:
                                recvparts.append(q.apply(part))
                        # Reconstruct and update string.
                        string = ""
                        # print("excludes: " + str(excludes))
                        # print("sendparts: " + str(sendparts))
                        # print("recvparts: " + str(recvparts))
                        for part, exclude in enumerate(excludes):
                            string += recvparts[part]
                            string += exclude.group()
                        string += recvparts[-1]
                    else:
                        # No split, apply like normal.
                        if q.type not in ("prefix", "suffix"):
                            if q.type in ("regexp", "random"):
                                string = q.apply(string, first=(i == 0), last=lastStr)
                            else:
                                string = q.apply(string)
                        elif q.type == "prefix" and i == 0:
                            string = q.apply(string)
                        elif q.type == "suffix" and lastStr:
                            string = q.apply(string)
                else:
                    # No split, apply like normal.
                    if q.type not in ("prefix", "suffix"):
                        if q.type in ("regexp", "random"):
                            string = q.apply(string, first=(i == 0), last=lastStr)
                        else:
                            string = q.apply(string)
                    elif q.type == "prefix" and i == 0:
                        string = q.apply(string)
                    elif q.type == "suffix" and lastStr:
                        string = q.apply(string)
            newlist.append(string)
        final = []
        for n in newlist:
            if isinstance(n, str):
                final.extend(lexMessage(n))
            else:
                final.append(n)
        return final

    def __iter__(self):
        yield from self.quirklist


class PesterProfile:
    def __init__(
        self,
        handle,
        color=None,
        mood=Mood("offline"),
        group=None,
        notes="",
        chumdb=None,
    ):
        self.handle = handle
        if color is None:
            if chumdb:
                color = chumdb.getColor(handle, QtGui.QColor("black"))
            else:
                color = QtGui.QColor("black")
        self.color = color
        self.mood = mood
        if group is None:
            if chumdb:
                group = chumdb.getGroup(handle, "Chums")
            else:
                group = "Chums"
        self.group = group
        self.notes = notes

    def initials(self, time=None):
        handle = self.handle
        caps = [l for l in handle if l.isupper()]
        if not caps:
            caps = [""]
        PchumLog.debug("handle = %s", handle)
        PchumLog.debug("caps = %s", caps)
        # Fallback for invalid string
        try:
            initials = (handle[0] + caps[0]).upper()
        except:
            PchumLog.exception("")
            initials = "XX"
        PchumLog.debug("initials = %s", initials)
        if hasattr(self, "time"):
            if time:
                if self.time > time:
                    return "F" + initials
                elif self.time < time:
                    return "P" + initials
                else:
                    return "C" + initials
            else:
                return initials
        else:
            return initials

    def colorhtml(self):
        if self.color:
            return self.color.name()
        else:
            return "#000000"

    def colorcmd(self):
        if self.color:
            (r, g, b, _a) = self.color.getRgb()
            return "%d,%d,%d" % (r, g, b)
        else:
            return "0,0,0"

    def plaindict(self):
        return (
            self.handle,
            {
                "handle": self.handle,
                "mood": self.mood.name(),
                "color": str(self.color.name()),
                "group": str(self.group),
                "notes": str(self.notes),
            },
        )

    def blocked(self, config):
        return self.handle in config.getBlocklist()

    def memsg(self, syscolor, lexmsg, time=None):
        suffix = lexmsg[0].suffix
        msg = convertTags(lexmsg[1:], "text")
        uppersuffix = suffix.upper()
        if time is not None:
            handle = f"{time.temporal} {self.handle}"
            initials = time.pcf + self.initials() + time.number + uppersuffix
        else:
            handle = self.handle
            initials = self.initials() + uppersuffix
        return "<c={}>-- {}{} <c={}>[{}]</c> {} --</c>".format(
            syscolor.name(),
            handle,
            suffix,
            self.colorhtml(),
            initials,
            msg,
        )

    def pestermsg(self, otherchum, syscolor, verb):
        return "<c={}>-- {} <c={}>[{}]</c> {} {} <c={}>[{}]</c> at {} --</c>".format(
            syscolor.name(),
            self.handle,
            self.colorhtml(),
            self.initials(),
            verb,
            otherchum.handle,
            otherchum.colorhtml(),
            otherchum.initials(),
            datetime.now().strftime("%H:%M"),
        )

    def moodmsg(self, mood, syscolor, theme):
        return (
            "<c=%s>-- %s <c=%s>[%s]</c> changed their mood to %s <img src='%s' /> --</c>"
            % (
                syscolor.name(),
                self.handle,
                self.colorhtml(),
                self.initials(),
                mood.name().upper(),
                theme["main/chums/moods"][mood.name()]["icon"],
            )
        )

    def idlemsg(self, syscolor, verb):
        return "<c={}>-- {} <c={}>[{}]</c> {} --</c>".format(
            syscolor.name(),
            self.handle,
            self.colorhtml(),
            self.initials(),
            verb,
        )

    def memoclosemsg(self, syscolor, initials, verb):
        if isinstance(initials, list):
            return "<c={}><c={}>{}</c> {}.</c>".format(
                syscolor.name(),
                self.colorhtml(),
                ", ".join(initials),
                verb,
            )
        return "<c={}><c={}>{}{}{}</c> {}.</c>".format(
            syscolor.name(),
            self.colorhtml(),
            initials.pcf,
            self.initials(),
            initials.number,
            verb,
        )

    def memonetsplitmsg(self, syscolor, initials):
        if len(initials) <= 0:
            return "<c=%s>Netsplit quits: <c=black>None</c></c>" % (syscolor.name())
        else:
            return "<c={}>Netsplit quits: <c=black>{}</c></c>".format(
                syscolor.name(),
                ", ".join(initials),
            )

    def memoopenmsg(self, syscolor, td, timeGrammar, verb, channel):
        """timeGrammar.temporal and timeGrammar.when are unused"""
        timetext = timeDifference(td)
        PchumLog.debug("pre pcf+self.initials()")
        initials = timeGrammar.pcf + self.initials()
        PchumLog.debug("post pcf+self.initials()")
        return "<c={}><c={}>{}</c> {} {} {}.</c>".format(
            syscolor.name(),
            self.colorhtml(),
            initials,
            timetext,
            verb,
            channel[1:].upper().replace("_", " "),
        )

    def memobanmsg(self, opchum, opgrammar, syscolor, initials, reason):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        if isinstance(initials, list):
            if opchum.handle == reason:
                return (
                    "<c={}>{}</c> banned <c={}>{}</c> from responding to memo.".format(
                        opchum.colorhtml(),
                        opinit,
                        self.colorhtml(),
                        ", ".join(initials),
                    )
                )
            else:
                return (
                    "<c=%s>%s</c> banned <c=%s>%s</c> from responding to memo: <c=black>[%s]</c>."
                    % (
                        opchum.colorhtml(),
                        opinit,
                        self.colorhtml(),
                        ", ".join(initials),
                        reason,
                    )
                )
        else:
            PchumLog.exception("")
            initials = self.initials()
            if opchum.handle == reason:
                return "<c=%s>%s</c> banned <c=%s>%s</c> from responding to memo." % (
                    opchum.colorhtml(),
                    opinit,
                    self.colorhtml(),
                    initials,
                )
            else:
                return (
                    "<c=%s>%s</c> banned <c=%s>%s</c> from responding to memo: <c=black>[%s]</c>."
                    % (
                        opchum.colorhtml(),
                        opinit,
                        self.colorhtml(),
                        initials,
                        reason,
                    )
                )

    # As far as I'm aware, there's no IRC reply for this, this seems impossible to check for in practice.
    def memopermabanmsg(self, opchum, opgrammar, syscolor, timeGrammar):
        initials = timeGrammar.pcf + self.initials() + timeGrammar.number
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}>{}</c> permabanned <c={}>{}</c> from the memo.".format(
            opchum.colorhtml(),
            opinit,
            self.colorhtml(),
            initials,
        )

    def memojoinmsg(self, syscolor, td, timeGrammar, verb):
        # (temporal, pcf, when) = (timeGrammar.temporal, timeGrammar.pcf, timeGrammar.when)
        timetext = timeDifference(td)
        initials = timeGrammar.pcf + self.initials() + timeGrammar.number
        return "<c={}><c={}>{} {} [{}]</c> {} {}.</c>".format(
            syscolor.name(),
            self.colorhtml(),
            timeGrammar.temporal,
            self.handle,
            initials,
            timetext,
            verb,
        )

    def memoopmsg(self, opchum, opgrammar, syscolor):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}>{}</c> made <c={}>{}</c> an OP.".format(
            opchum.colorhtml(),
            opinit,
            self.colorhtml(),
            self.initials(),
        )

    def memodeopmsg(self, opchum, opgrammar, syscolor):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}>{}</c> took away <c={}>{}</c>'s OP powers.".format(
            opchum.colorhtml(),
            opinit,
            self.colorhtml(),
            self.initials(),
        )

    def memovoicemsg(self, opchum, opgrammar, syscolor):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}>{}</c> gave <c={}>{}</c> voice.".format(
            opchum.colorhtml(),
            opinit,
            self.colorhtml(),
            self.initials(),
        )

    def memodevoicemsg(self, opchum, opgrammar, syscolor):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}>{}</c> took away <c={}>{}</c>'s voice.".format(
            opchum.colorhtml(),
            opinit,
            self.colorhtml(),
            self.initials(),
        )

    def memomodemsg(self, opchum, opgrammar, syscolor, modeverb, modeon):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        if modeon:
            modeon = "now"
        else:
            modeon = "no longer"
        return "<c={}>Memo is {} <c=black>{}</c> by <c={}>{}</c></c>".format(
            syscolor.name(),
            modeon,
            modeverb,
            opchum.colorhtml(),
            opinit,
        )

    def memoquirkkillmsg(self, opchum, opgrammar, syscolor):
        opinit = opgrammar.pcf + opchum.initials() + opgrammar.number
        return "<c={}><c={}>{}</c> turned off your quirk.</c>".format(
            syscolor.name(),
            opchum.colorhtml(),
            opinit,
        )

    @staticmethod
    def checkLength(handle):
        return len(handle) <= 256

    @staticmethod
    def checkValid(handle):
        caps = [l for l in handle if l.isupper()]
        if len(caps) != 1:
            return (False, "Must have exactly 1 uppercase letter")
        if handle[0].isupper():
            return (False, "Cannot start with uppercase letter")
        if re.search("[^A-Za-z0-9]", handle) is not None:
            return (False, "Only alphanumeric characters allowed")
        if handle[0].isnumeric():  # IRC doesn't allow this
            return (False, "Handles may not start with a number")
        return (True,)


class PesterHistory:
    def __init__(self):
        self.history = []
        self.current = 0
        self.saved = None

    def next(self, text):
        if self.current == 0:
            return None
        if self.current == len(self.history):
            self.save(text)
        self.current -= 1
        text = self.history[self.current]
        return text

    def prev(self):
        self.current += 1
        if self.current >= len(self.history):
            self.current = len(self.history)
            return self.retrieve()
        return self.history[self.current]

    def reset(self):
        self.current = len(self.history)
        self.saved = None

    def save(self, text):
        self.saved = text

    def retrieve(self):
        return self.saved

    def add(self, text):
        if len(self.history) == 0 or text != self.history[len(self.history) - 1]:
            self.history.append(text)
        self.reset()
