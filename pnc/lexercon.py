from pnc.unicolor import Color

import re

global basestr
basestr = str
try:
    basestr = str
except NameError:
    # We're running Python 3. Leave it be.
    pass

# Yanked from the old Textsub file. Pardon the mess.

# TODO: Need to consider letting conversions register themselves - or, as a
# simpler solution, just have CTag.convert and have it search for a conversion
# function appropriate to the given format - e.g. CTag.convert_pchum.


class Lexeme:
    def __init__(self, string, origin):
        # The 'string' property is just what it came from; the original
        # representation. It doesn't have to be used, and honestly probably
        # shouldn't be.
        self.string = string
        self.origin = origin

    def __str__(self):
        ##return self.string
        return self.convert(self.origin)

    def __len__(self):
        ##return len(self.string)
        return len(str(self))

    def convert(self, format):
        # This is supposed to be overwritten by subclasses
        raise NotImplementedError

    def rebuild(self, format):
        """Builds a copy of the owning Lexeme as if it had 'come from' a
        different original format, and returns the result."""
        # TODO: This. Need to decide whether overloading will be required for
        # nearly every single subclass....
        raise NotImplementedError

    @classmethod
    def from_mo(cls, mo, origin):
        raise NotImplementedError


# class Message(Lexeme):
#    """An object designed to represent a message, possibly containing Lexeme
#    objects in their native form as well. Intended to be a combination of a
#    list and a string, combining the former with the latter's methods."""
#
#    def __init__(self, contents, origin):
#        lexer = Lexer.lexer_for(origin)()
#        working = lexer.lex(contents)
#        # TODO: Rebuild all lexemes so that they all 'come from' the same
#        # format (e.g. their .origin values are all the same as the Message's).
#        for i, elt in enumerate(working):
#            try:
#                # Try to rebuild for the new format
#                elt = elt.rebuild(origin)
#            except AttributeError:
#                # It doesn't let us rebuild, so it's probably not a Lexeme
#                continue
#            else:
#                # Assign it to the proper place, replacing the old one
#                working[i] = elt
#        self.origin = origin
#        self.contents = working
#        self.string = "".join(lexer.list_convert(working))
#
#    # TODO: Finish all the rest of this.


class Specifier(Lexeme):
    # Almost purely for classification at present
    sets_color = sets_bold = sets_italic = sets_underline = None
    resets_color = resets_bold = resets_italic = resets_underline = None
    resets_formatting = None
    # If this form has a more compact form, use it
    compact = False


# Made so that certain odd message-ish things have a place to go. May have its
# class changed later.
class Chunk(Specifier):
    pass


class FTag(Specifier):
    pass


class CTag(Specifier):
    """Denotes the beginning or end of a color change."""

    sets_color = True

    def __init__(self, string, origin, color):
        super().__init__(string, origin)
        # So we can also have None
        if isinstance(color, tuple):
            if len(color) < 2:
                raise ValueError
            self.color, self.bg_color = color[:2]
        else:
            self.color = color
            self.bg_color = None

    def has_color(self):
        if self.color is not None or self.bg_color is not None:
            return True
        return False

    def convert(self, format):
        text = ""
        color = self.color
        bg = self.bg_color
        if format == "irc":
            # Put in the control character for a color code.
            text = "\x03"
            if color:
                text += color.ccode
                if bg:
                    text += "," + bg.ccode
            elif bg:
                text += "99," + bg.ccode
        elif format == "pchum":
            if not color:
                text = "</c>"
            else:
                if color.name:
                    text = "<c=%s>" % color.name
                else:
                    # We should have a toggle here, just in case this isn't
                    # acceptable for some reason, but it usually will be.
                    rgb = "<c=%d,%d,%d>" % color.to_rgb_tuple()
                    hxs = color.hexstr
                    if self.compact:
                        # Try to crush it down even further.
                        hxs = color.reduce_hexstr(hxs)
                    hxs = "<c=%s>" % hxs
                    if len(rgb) <= len(hxs):
                        # Prefer the more widely-recognized default format
                        text = rgb
                    else:
                        # Hex is shorter, and recognized by everything thus
                        # far; use it.
                        text = hxs
        elif format == "plaintext":
            text = ""
        return text

    @classmethod
    def from_mo(cls, mo, origin):
        inst = None
        if origin == "irc":
            text = mo.group()
            fg, bg = mo.groups()
            try:
                fg = Color("\x03" + fg)
            except:
                fg = None
            try:
                bg = Color("\x03" + bg)
            except:
                bg = None
            inst = cls(text, origin, color=(fg, bg))
        elif origin == "pchum":
            text = mo.group()
            inst = cls(text, origin, color=None)
            if mo.lastindex:
                text = mo.group(1)
                cmatch = Pesterchum._ctag_rgb.match(text)
                if cmatch:
                    working = cmatch.groups()
                    working = list(map(int, working))
                    inst.color = Color(*working)
                else:
                    try:
                        inst.color = Color(text)
                    except:
                        pass
        return inst


class CTagEnd(CTag):
    # TODO: Make this a separate class - NOT a subclass of CTag like it is at
    # present
    resets_color = True

    def convert(self, format):
        text = ""
        if format == "irc":
            return "\x03"
        elif format == "pchum":
            return "</c>"
        elif format == "plaintext":
            return ""
        return text

    def has_color(self):
        return False

    @classmethod
    def from_mo(cls, mo, origin):
        # Turns the whole match into it (for now)
        return cls(mo.group(), origin, color=None)


class LineColor(CTag):
    pass


class LineColorEnd(CTagEnd):
    pass


class FTagEnd(Specifier):
    resets_formatting = True


class ResetTag(CTagEnd, FTagEnd):
    def convert(self, format):
        text = ""
        if format == "irc":
            return "\x0F"
        elif format == "pchum":
            # Later on, this one is going to be infuriatingly tricky.
            # Supporting things like bold and so on doesn't really allow for an
            # easy 'reset' tag.
            # I *could* implement it, and it wouldn't be too hard, but it would
            # probably confuse more people than it helped.
            return "</c>"
        elif format == "plaintext":
            return ""
        return text


class SpecifierEnd(CTagEnd, FTagEnd):
    # This might not ever even be used, but you never know....
    # If it does, we may need properties such as .resets_color, .resets_bold,
    # and so on and so forth
    pass


# TODO: Consider using a metaclass to check those properties - e.g. if
# a class .sets_color and a subclass .resets_color, set the subclass's
# .sets_color to False


class Lexer:
    # Subclasses need to supply a ref themselves
    ref = None
    compress_tags = False

    def breakdown(self, string, objlist):
        if not isinstance(string, basestr):
            msglist = string
        else:
            msglist = [string]
        for obj, rxp in objlist:
            working = []
            for i, msg in enumerate(msglist):
                if not isinstance(msg, basestr):
                    # We've probably got a tag or something else that we can't
                    # actually parse into a tag
                    working.append(msg)
                    continue
                # If we got here, we have a string to parse
                oend = 0
                for mo in rxp.finditer(msg):
                    start, end = mo.span()
                    if oend != start:
                        # There's text between the end of the last match and
                        # the beginning of this one, add it
                        working.append(msg[oend:start])
                    tag = obj.from_mo(mo, origin=self.ref)
                    working.append(tag)
                    oend = end
                # We've finished parsing every match, check if there's any text
                # left
                if oend < len(msg):
                    # There is; add it to the end of the list
                    working.append(msg[oend:])
            # Exchange the old list with the processed one, and continue
            msglist = working
        return msglist

    def lex(self, string):
        # Needs to be implemented by subclasses
        return self.breakdown(string, [])

    def list_convert(self, target, format=None):
        if format is None:
            format = self.ref
        converted = []

        for elt in target:
            if isinstance(elt, Lexeme):
                elt = elt.convert(format)
            if not isinstance(elt, basestr):
                # Tempted to make this toss an error, but for now, we'll be
                # safe and make it convert to str
                elt = str(elt)
            converted.append(elt)
        return converted


class Pesterchum(Lexer):
    ref = "pchum"
    _ctag_begin = re.compile(r"<c=(.*?)>", flags=re.I)
    _ctag_rgb = re.compile(r"(\d+),(\d+),(\d+)")
    _ctag_end = re.compile(r"</c>", flags=re.I)
    _mecmdre = re.compile(r"^(/me|PESTERCHUM:ME)(\S*)")

    # TODO: At some point, this needs to have support for setting up
    # optimization controls - so ctags will be rendered down into things like
    # "<c=#FAF>" instead of "<c=#FFAAFF>".
    # I'd make this the default, but I'd like to retain *some* compatibility
    # with Chumdroid's faulty implementation...or at least have the option to.

    def lex(self, string):
        lexlist = [
            ##(mecmd, self._mecmdre),
            (CTag, self._ctag_begin),
            ##(CTag, self._ctag_end)
            (CTagEnd, self._ctag_end),
        ]

        lexed = self.breakdown(string, lexlist)

        balanced = []
        beginc = 0
        endc = 0
        for o in lexed:
            if isinstance(o, CTag):
                ##if o:
                if o.has_color():
                    # This means it has a color of some sort
                    # TODO: Change this; pesterchum doesn't support BG colors,
                    # so we should only check FG ones (has_color() checks both)
                    # TODO: Consider making a Lexer method that checks if
                    # a provided object would actually contribute something
                    # when rendered under a certain format
                    beginc += 1
                elif beginc >= endc:
                    endc += 1
                # Apply compression, if we're set to. We made these objects, so
                # that should be okay.
                if self.compress_tags:
                    o.compact = True
            balanced.append(o)
            # Original (Pesterchum) code:
            ##if isinstance(o, colorBegin):
            ##  beginc += 1
            ##  balanced.append(o)
            ##elif isinstance(o, colorEnd):
            ##  if beginc >= endc:
            ##      endc += 1
            ##      balanced.append(o)
            ##  else:
            ##      balanced.append(o.string)
            ##else:
            ##  balanced.append(o)
        # This will need to be re-evaluated to support the line end lexeme/etc.
        if beginc > endc:
            for i in range(0, beginc - endc):
                ##balanced.append(colorEnd("</c>"))
                balanced.append(CTagEnd("</c>", self.ref, None))
        return balanced

    # TODO: Let us contextually set compression here or something, ugh. If
    # 'None' assume the self-set one.
    def list_convert(self, target, format=None):
        if format is None:
            format = self.ref
        converted = []
        cstack = []

        ##closecolor = lambda: converted.append(CTagEnd("</c>", self.ref, None))
        closecolor = lambda: converted.append(
            CTagEnd("</c>", self.ref, None).convert(format)
        )

        for elt in target:
            if isinstance(elt, LineColorEnd):
                # Go down the stack until we have a line color TO end
                while cstack:
                    # Add a </c> since we'll need one anyway
                    closecolor()
                    ##if isinstance(color, LineColor):
                    if isinstance(cstack.pop(), LineColor):
                        # We found what we wanted, and the color
                        # was already popped from the stack, so
                        # we're good
                        # Breaking here allows it to be appended
                        break
                continue
            elif isinstance(elt, ResetTag):
                # If it says reset, reset - which means go down the
                # stack to the most recent line color.
                while cstack:
                    color = cstack[-1]
                    if not isinstance(color, LineColor):
                        # It's not a line color, so remove it
                        del cstack[-1]
                        # Add a </c>
                        closecolor()
                    else:
                        # It's a line color, so stop searching.
                        # Using break here prevents the 'else'
                        # clause of this while statement from
                        # executing, which means that we go on to
                        # add this to the result.
                        break
                else:
                    # We don't have any more entries in the stack;
                    # just continue.
                    continue
                ## We found the line color, so add it and continue
                ##converted.append(color.convert(format))
                continue
                ## TODO: Make this actually add the reset char
                # The above shouldn't be necessary because this is Pesterchum's
                # format, not IRC's
            elif isinstance(elt, CTagEnd):
                try:
                    color = cstack[-1]
                    # Remove the oldest color, the one we're exiting
                    if not isinstance(color, LineColor):
                        # If we got here, we don't have a line color,
                        # so we're free to act as usual
                        cstack.pop()
                        # Fetch the current nested color
                        color = cstack[-1]
                    else:
                        # We have a line color and the current lexeme
                        # is NOT a line color end; don't even bother
                        # adding it to the processed result
                        continue
                except LookupError:
                    # We aren't nested in a color anymore
                    # Passing here causes us to fall through to normal
                    # handling
                    pass
                # Not necessary due to Pesterchum's format
                ##else:
                ##  # We're still nested....
                ##  ##converted.append(elt.convert(format))
                ##  converted.append(color.convert(format))
                ##  # We already added to the working list, so just
                ##  # skip the rest
                ##  continue
            elif isinstance(elt, CTag):
                # Push the color onto the stack - we're nested in it now
                cstack.append(elt)
                # Falling through adds it to the converted result

            if isinstance(elt, Lexeme):
                elt = elt.convert(format)
            elif not isinstance(elt, basestr):
                # Tempted to make this toss an error, but for now, we'll be
                # safe and make it convert to str
                elt = str(elt)
            converted.append(elt)
        return converted


class RelayChat(Lexer):
    ref = "irc"
    # This could use some cleaning up later, but it'll work for now, hopefully
    ##_ccode_rxp = re.compile(r"\x03(?P<fg>\d\d?)?(?(fg),(?P<bg>\d\d?))?|\x0F")
    _ccode_rxp = re.compile(r"\x03(?P<fg>\d\d?)(?(fg),(?P<bg>\d\d?))?")
    _ccode_end_rxp = re.compile(r"\x03(?!\d\d?)")
    _reset_rxp = re.compile(r"\x0F")

    def lex(self, string):
        ##lexlist = [(CTag, self._ccode_rxp)]
        lexlist = [
            (CTag, self._ccode_rxp),
            (CTagEnd, self._ccode_end_rxp),
            (ResetTag, self._reset_rxp),
        ]

        lexed = self.breakdown(string, lexlist)

        # Don't bother with the whole fancy color-balancing thing yet
        return lexed

    def list_convert(self, target, format=None):
        if format is None:
            format = self.ref
        converted = []
        cstack = []

        for elt in target:
            if isinstance(elt, CTag):
                if isinstance(elt, CTagEnd) or not elt.has_color():
                    if isinstance(elt, LineColorEnd):
                        # Go down the stack until we have a line color TO
                        # end
                        while cstack:
                            ##if isinstance(color, LineColor):
                            if isinstance(cstack.pop(), LineColor):
                                # We found what we wanted, and the color
                                # was already popped from the stack, so
                                # we're good
                                break
                    # The current lexeme isn't a line color end
                    elif isinstance(elt, ResetTag):
                        # If it says reset, reset - which means go down the
                        # stack to the most recent line color.
                        while cstack:
                            color = cstack[-1]
                            if not isinstance(color, LineColor):
                                # It's not a line color, so remove it
                                del cstack[-1]
                            else:
                                # It's a line color, so stop searching.
                                # Using break here prevents the 'else'
                                # clause of this while statement from
                                # executing.
                                break
                        else:
                            # We don't have any more entries in the stack;
                            # just continue.
                            continue
                        # We found the line color, so add it and continue
                        converted.append(color.convert(format))
                        continue
                        # TODO: Make this actually add the reset char
                    else:
                        try:
                            color = cstack[-1]
                            # Remove the oldest color, the one we're exiting
                            if not isinstance(color, LineColor):
                                # If we got here, we don't have a line color,
                                # so we're free to act as usual
                                cstack.pop()
                                # Fetch the current nested color
                                color = cstack[-1]
                            else:
                                # We have a line color and the current lexeme
                                # is NOT a line color end; don't even bother
                                # adding it to the processed result
                                continue
                        except LookupError:
                            # We aren't nested in a color anymore
                            # Passing here causes us to fall through to normal
                            # handling
                            pass
                        else:
                            # We're still nested....
                            ##converted.append(elt.convert(format))
                            converted.append(color.convert(format))
                            # We already added to the working list, so just
                            # skip the rest
                            continue
                else:
                    # Push the color onto the stack - we're nested in it now
                    cstack.append(elt)

            if isinstance(elt, Lexeme):
                elt = elt.convert(format)
            elif not isinstance(elt, basestr):
                # Tempted to make this toss an error, but for now, we'll be
                # safe and make it convert to str
                elt = str(elt)
            converted.append(elt)
        return converted

    def _list_convert_new(self, target, format=None):
        if format is None:
            format = self.ref
        converted = []
        cstack = []

        for elt in target:
            if isinstance(elt, LineColorEnd):
                # Go down the stack until we have a line color TO end
                while cstack:
                    # Add a </c> since we'll need one anyway

                    # Is closecolor accessible here?
                    # No. :/
                    # try:
                    #     closecolor()
                    # except Exception as e:
                    #     print(e)

                    ##if isinstance(color, LineColor):
                    if isinstance(cstack.pop(), LineColor):
                        # We found what we wanted, and the color
                        # was already popped from the stack, so
                        # we're good
                        # Breaking here allows it to be appended
                        break
                continue
            elif isinstance(elt, ResetTag):
                # If it says reset, reset - which means go down the
                # stack to the most recent line color.
                while cstack:
                    color = cstack[-1]
                    if not isinstance(color, LineColor):
                        # It's not a line color, so remove it
                        del cstack[-1]
                        # Add a </c>
                        # Is closecolor accessible here?
                        # try:
                        #     closecolor()
                        # except Exception as e:
                        #     print(e)
                    else:
                        # It's a line color, so stop searching.
                        # Using break here prevents the 'else'
                        # clause of this while statement from
                        # executing.
                        break
                else:
                    # We don't have any more entries in the stack;
                    # just continue.
                    continue
                ## We found the line color, so add it and continue
                ##converted.append(color.convert(format))
                continue
                ## TODO: Make this actually add the reset char
                # The above shouldn't be necessary because this is Pesterchum's
                # format, not IRC's
            elif isinstance(elt, CTagEnd):
                try:
                    color = cstack[-1]
                    # Remove the oldest color, the one we're exiting
                    if not isinstance(color, LineColor):
                        # If we got here, we don't have a line color,
                        # so we're free to act as usual
                        cstack.pop()
                        # Fetch the current nested color
                        color = cstack[-1]
                    else:
                        # We have a line color and the current lexeme
                        # is NOT a line color end; don't even bother
                        # adding it to the processed result
                        continue
                except LookupError:
                    # We aren't nested in a color anymore
                    # Passing here causes us to fall through to normal
                    # handling
                    pass
                # Not necessary due to Pesterchum's format
                ##else:
                ##  # We're still nested....
                ##  ##converted.append(elt.convert(format))
                ##  converted.append(color.convert(format))
                ##  # We already added to the working list, so just
                ##  # skip the rest
                ##  continue
            elif isinstance(elt, CTag):
                # Push the color onto the stack - we're nested in it now
                cstack.append(elt)
                # Falling through adds it to the converted result

            if isinstance(elt, Lexeme):
                elt = elt.convert(format)
            elif not isinstance(elt, basestr):
                # Tempted to make this toss an error, but for now, we'll be
                # safe and make it convert to str
                elt = str(elt)
            converted.append(elt)
        return converted
