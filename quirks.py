import os
import re
import logging

import ostools
from mispeller import mispeller
from parsetools import parseRegexpFunctions

_datadir = ostools.getDataDir()
PchumLog = logging.getLogger("pchumLogger")


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
        """string: string to operate quirk on. first: is the given substring at the very start (idx == 0) of the superstring? last: is the given substring at the very last (idx == -1) of the superstring?"""
        if self.on:
            return self._apply(string, first, last)
        else:
            return string

    def _apply(self, string: str, first: bool, last: bool):
        # Overwrite
        raise NotImplemented()
        return string

    def __str__(self):
        # Overwrite
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

            if not ctag.search(w) and dice < percentage:
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
