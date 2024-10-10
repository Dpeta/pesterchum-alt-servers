import os
import re
import random
import logging
import itertools

import ostools
from mispeller import mispeller
from parsetools import parseRegexpFunctions, lexMessage, smiledict


_datadir = ostools.getDataDir()
PchumLog = logging.getLogger("pchumLogger")

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
_alternian = re.compile(r"<alt>.*?</alt>")

# traditional quirks


def PesterQuirkFactory(quirk: dict):
    """Returns a valid PesterQuirk object from the given quirk dictionary"""
    # This is a "factory" because a lot of old code depends on calling the old class which was all quirks rolled into 1
    match quirk["type"]:
        case "prefix":
            return PrefixPesterQuirk(quirk)
        case "suffix":
            return SuffixPesterQuirk(quirk)
        case "replace":
            return ReplacePesterQuirk(quirk)
        case "regexp":
            return RegexpPesterQuirk(quirk)
        case "random":
            return RandomPesterQuirk(quirk)
        case "spelling":
            return MispellerPesterQuirk(quirk)


class PesterQuirk:
    def __init__(self, quirk: dict):
        self.quirk = quirk
        self.type = self.quirk["type"]
        self.on = self.quirk.get("on", True)
        self.group = self.quirk.get("group", "Miscellaneous")

        self.checkstate = self.quirk.get(
            "checkstate", 0
        )  ## Seems to be somethign related to the QT checkbox? QtCore.QT.CheckState

    def apply(self, string: str, first: bool = False, last: bool = False):
        """string: string to operate quirk on. first: is the given substring at the very start (is_first_string) of the superstring? last: is the given substring at the very last (idx == -1) of the superstring?"""
        if self.on:
            return self._apply(string, first, last)
        else:
            return string

    def _apply(self, string: str, first: bool, last: bool):
        # Overwrite (return string)
        raise NotImplementedError()

    def __str__(self):
        # Overwrite (return string)
        return "UNKNOWN QUIRK"


class PrefixPesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "prefix"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        return self.quirk["value"] + string

    def __str__(self):
        return "BEGIN WITH: %s" % (self.quirk["value"])


class SuffixPesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "suffix"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        return string + self.quirk["value"]

    def __str__(self):
        return "END WITH: %s" % (self.quirk["value"])


class ReplacePesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "replace"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        return string.replace(self.quirk["from"], self.quirk["to"])

    def __str__(self):
        return "REPLACE {} WITH {}".format(self.quirk["from"], self.quirk["to"])


class RegexpPesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "regexp"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        # regex string
        from_ = self.quirk["from"]

        # Exit prematurely if the regexp is only supposed to act on the first substring of the superstring and this isnt that (^ is start of string)
        if not first and len(from_) > 0 and from_[0] == "^":
            return string
        # Exit prematurely if the regexp is only supposed to act on the last substring of the superstring and this isnt that ($ is end of string)
        if not last and len(from_) > 0 and from_[-1] == "$":
            return string

        # the replace string
        to = self.quirk["to"]
        # I think this handles the regex functions like rainbow()
        parse_tree = parseRegexpFunctions(to)
        return re.sub(from_, parse_tree.expand, string)

    def __str__(self):
        return "REGEXP: {} REPLACED WITH {}".format(
            self.quirk["from"],
            self.quirk["to"],
        )


class RandomPesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "random"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        # Fallback if the quirk is not set up right (no random strings to replace with)
        if len(self.quirk.get("randomlist", [])) == 0:
            return string

        # regex string
        from_ = self.quirk["from"]

        # See regexPesterQuirk
        if not first and len(from_) > 0 and from_[0] == "^":
            return string
        if not last and len(from_) > 0 and from_[-1] == "$":
            return string

        # Pick random item
        # I believe this gets called for each match in the re.sub
        def randomrep(mo):
            choice = random.choice(self.quirk["randomlist"])
            parse_tree = parseRegexpFunctions(choice)
            return parse_tree.expand(mo)

        return re.sub(from_, randomrep, string)

    def __str__(self):
        return "REGEXP: {} RANDOMLY REPLACED WITH {}".format(
            self.quirk["from"],
            self.quirk["randomlist"],
        )


class MispellerPesterQuirk(PesterQuirk):
    def __init__(self, quirk: dict):
        assert quirk["type"] == "spelling"
        super().__init__(quirk)

    def _apply(self, string: str, first: bool, last: bool):
        percentage = self.quirk["percentage"] / 100.0
        out = []
        # regex to avoid color tags
        ctag = re.compile("(</?c=?.*?>)", re.I)

        # Split by space to get all words in given string
        for word in string.split(" "):
            # get random 0.0 - 1.0 number
            dice = random.random()

            if not ctag.search(word) and dice < percentage:
                # word is not wrapped in color tags :)
                out.append(mispeller(word))
            elif dice < percentage:
                # word IS wrapped in color tags!!
                tmp = []
                split = ctag.split(word)
                # Only garble substrings if they are not a <c> tag
                for sequence in split:
                    if sequence and not ctag.search(sequence):
                        tmp.append(mispeller(sequence))
                    else:
                        tmp.append(sequence)
                out.append("".join(tmp))
            else:
                out.append(word)
        # Turn back into normal sentence
        return " ".join(out)

    def __str__(self):
        return "MISPELLER: %d%%" % (self.quirk["percentage"])


# TODO: clean this up. its huge and really hard to read


class PesterQuirkCollection:
    def __init__(self, quirklist):
        self.quirklist = []
        for quirk in quirklist:
            self.addQuirk(quirk)

    def plainList(self):
        # Returns a list of all the quirk dictionaries
        return [quirk.quirk for quirk in self.quirklist]

    def addQuirk(self, quirk):
        """quirk: dict or a PesterQuirk"""
        if isinstance(quirk, dict):
            self.quirklist.append(PesterQuirkFactory(quirk))
        elif isinstance(quirk, PesterQuirk):
            self.quirklist.append(quirk)

    def apply(self, lexed, first=False, last=False):
        prefixes = [
            quirk for quirk in self.quirklist if isinstance(quirk, PrefixPesterQuirk)
        ]
        # suffix = [q for q in self.quirklist if q.type == "suffix"]

        newlist = []
        for idx, original in enumerate(lexed):
            is_first_string = idx == 0
            if not isinstance(original, str):
                if is_first_string:
                    string = " "
                    for prefix_quirk in prefixes:
                        string += prefix_quirk.apply(string)
                    newlist.append(string)
                newlist.append(original)
                continue
            is_last_string = idx == len(lexed) - 1
            string = original

            for quirk in self.quirklist:
                try:
                    checkstate = int(quirk.checkstate)
                except Exception:
                    checkstate = 0

                # Exclude option is checked
                if checkstate == 2:
                    # Check for substring that should be excluded.
                    excludes = []
                    # Return matches for links, smilies, handles, memos.
                    # Chain the iterators and add to excludes list.
                    matches = itertools.chain(
                        re.finditer(_urlre, string),
                        re.finditer(_smilere, string),
                        re.finditer(_handlere, string),
                        re.finditer(_memore, string),
                        re.finditer(_alternian, string),
                    )
                    excludes.extend(matches)

                    if excludes:
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
                            if quirk.type in ("regexp", "random"):
                                recvparts.append(
                                    quirk.apply(
                                        part,
                                        first=(is_first_string),
                                        last=is_last_string,
                                    )
                                )
                            elif quirk.type == "prefix" and is_first_string:
                                recvparts.append(quirk.apply(part))
                            elif quirk.type == "suffix" and is_last_string:
                                recvparts.append(quirk.apply(part))
                            else:
                                recvparts.append(quirk.apply(part))
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
                        if quirk.type not in ("prefix", "suffix"):
                            if quirk.type in ("regexp", "random"):
                                string = quirk.apply(
                                    string, first=(is_first_string), last=is_last_string
                                )
                            else:
                                string = quirk.apply(string)
                        elif quirk.type == "prefix" and is_first_string:
                            string = quirk.apply(string)
                        elif quirk.type == "suffix" and is_last_string:
                            string = quirk.apply(string)
                else:
                    # No split, apply like normal.
                    if quirk.type not in ("prefix", "suffix"):
                        if quirk.type in ("regexp", "random"):
                            string = quirk.apply(
                                string, first=(is_first_string), last=is_last_string
                            )
                        else:
                            string = quirk.apply(string)
                    elif quirk.type == "prefix" and is_first_string:
                        string = quirk.apply(string)
                    elif quirk.type == "suffix" and is_last_string:
                        string = quirk.apply(string)
            newlist.append(string)

        final = []
        for item in newlist:
            if isinstance(item, str):
                final.extend(lexMessage(item))
            else:
                final.append(item)
        return final

    def __iter__(self):
        yield from self.quirklist
