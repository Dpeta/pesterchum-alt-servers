import re
import random
import ostools
import collections
from copy import copy
from datetime import timedelta
from PyQt5 import QtCore, QtGui, QtWidgets

from generic import mysteryTime
from quirks import ScriptQuirks
from pyquirks import PythonQuirks
from luaquirks import LuaQuirks
import dataobjs
import logging

# karxi: My own contribution to this - a proper lexer.
import pnc.lexercon as lexercon

# I'll clean up the things that are no longer needed once the transition is
# actually finished.
try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

_ctag_begin = re.compile(r'(?i)<c=(.*?)>')
_gtag_begin = re.compile(r'(?i)<g[a-f]>')
_ctag_end = re.compile(r'(?i)</c>')
_ctag_rgb = re.compile(r'\d+,\d+,\d+')
_urlre = re.compile(r"(?i)(?:^|(?<=\s))(?:(?:https?|ftp)://|magnet:)[^\s]+")
_url2re = re.compile(r"(?i)(?<!//)\bwww\.[^\s]+?\.")
_memore = re.compile(r"(\s|^)(#[A-Za-z0-9_]+)")
_handlere = re.compile(r"(\s|^)(@[A-Za-z0-9_]+)")
_imgre = re.compile(r"""(?i)<img src=['"](\S+)['"]\s*/>""")
_mecmdre = re.compile(r"^(/me|PESTERCHUM:ME)(\S*)")
_oocre = re.compile(r"([\[(\{])\1.*([\])\}])\2")
_format_begin = re.compile(r'(?i)<([ibu])>')
_format_end = re.compile(r'(?i)</([ibu])>')
_honk = re.compile(r"(?i)\bhonk\b")

quirkloader = ScriptQuirks()
quirkloader.add(PythonQuirks())
quirkloader.add(LuaQuirks())
quirkloader.loadAll()
logging.info(quirkloader.funcre())
_functionre = re.compile(r"%s" % quirkloader.funcre())
_groupre = re.compile(r"\\([0-9]+)")

def reloadQuirkFunctions():
    quirkloader.loadAll()
    global _functionre
    _functionre = re.compile(r"%s" % quirkloader.funcre())

def lexer(string, objlist):
    """objlist is a list: [(objecttype, re),...] list is in order of preference"""
    stringlist = [string]
    for (oType, regexp) in objlist:
        newstringlist = []
        for (stri, s) in enumerate(stringlist):
            if type(s) not in [str, str]:
                newstringlist.append(s)
                continue
            lasti = 0
            for m in regexp.finditer(s):
                start = m.start()
                end = m.end()
                tag = oType(m.group(0), *m.groups())
                if lasti != start:
                    newstringlist.append(s[lasti:start])
                newstringlist.append(tag)
                lasti = end
            if lasti < len(string):
                newstringlist.append(s[lasti:])
        stringlist = copy(newstringlist)
    return stringlist

# karxi: All of these were derived from object before. I changed them to
# lexercon.Chunk so that I'd have an easier way to match against them until
# they're redone/removed.
class colorBegin(lexercon.Chunk):
    def __init__(self, string, color):
        self.string = string
        self.color = color
    def convert(self, format):
        color = self.color
        if format == "text":
            return ""
        if _ctag_rgb.match(color) is not None:
            if format=='ctag':
                return "<c=%s>" % (color)
            try:
                qc = QtGui.QColor(*[int(c) for c in color.split(",")])
            except ValueError:
                qc = QtGui.QColor("black")
        else:
            qc = QtGui.QColor(color)
        if not qc.isValid():
            qc = QtGui.QColor("black")
        if format == "html":
            return '<span style="color:%s">' % (qc.name())
        elif format == "bbcode":
            return '[color=%s]' % (qc.name())
        elif format == "ctag":
            (r,g,b,a) = qc.getRgb()
            return '<c=%s,%s,%s>' % (r,g,b)

class colorEnd(lexercon.Chunk):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "</span>"
        elif format == "bbcode":
            return "[/color]"
        elif format == "text":
            return ""
        else:
            return self.string

class formatBegin(lexercon.Chunk):
    def __init__(self, string, ftype):
        self.string = string
        self.ftype = ftype
    def convert(self, format):
        if format == "html":
            return "<%s>" % (self.ftype)
        elif format == "bbcode":
            return "[%s]" % (self.ftype)
        elif format == "text":
            return ""
        else:
            return self.string

class formatEnd(lexercon.Chunk):
    def __init__(self, string, ftype):
        self.string = string
        self.ftype = ftype
    def convert(self, format):
        if format == "html":
            return "</%s>" % (self.ftype)
        elif format == "bbcode":
            return "[/%s]" % (self.ftype)
        elif format == "text":
            return ""
        else:
            return self.string

class hyperlink(lexercon.Chunk):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "<a href='%s'>%s</a>" % (self.string, self.string)
        elif format == "bbcode":
            return "[url]%s[/url]" % (self.string)
        else:
            return self.string

class hyperlink_lazy(hyperlink):
    def __init__(self, string):
        self.string = "http://" + string

class imagelink(lexercon.Chunk):
    def __init__(self, string, img):
        self.string = string
        self.img = img
    def convert(self, format):
        if format == "html":
            return self.string
        elif format == "bbcode":
            if self.img[0:7] == "http://":
                return "[img]%s[/img]" % (self.img)
            else:
                return ""
        else:
            return ""

class memolex(lexercon.Chunk):
    def __init__(self, string, space, channel):
        self.string = string
        self.space = space
        self.channel = channel
    def convert(self, format):
        if format == "html":
            return "%s<a href='%s'>%s</a>" % (self.space, self.channel, self.channel)
        else:
            return self.string

class chumhandlelex(lexercon.Chunk):
    def __init__(self, string, space, handle):
        self.string = string
        self.space = space
        self.handle = handle
    def convert(self, format):
        if format == "html":
            return "%s<a href='%s'>%s</a>" % (self.space, self.handle, self.handle)
        else:
            return self.string

class smiley(lexercon.Chunk):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "<img src='smilies/%s' alt='%s' title='%s' />" % (smiledict[self.string], self.string, self.string)
        else:
            return self.string

class honker(lexercon.Chunk):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "<img src='smilies/honk.png' alt'honk' title='honk' />"
        else:
            return self.string

class mecmd(lexercon.Chunk):
    def __init__(self, string, mecmd, suffix):
        self.string = string
        self.suffix = suffix
    def convert(self, format):
        return self.string

kxpclexer = lexercon.Pesterchum()

def kxlexMsg(string):
    # Do a bit of sanitization.
    msg = str(string)
    # TODO: Let people paste line-by-line normally. Maybe have a mass-paste
    # right-click option?
    msg = msg.replace('\n', ' ').replace('\r', ' ')
    # Something the original doesn't seem to have accounted for.
    # Replace tabs with 4 spaces.
    msg = msg.replace('\t', ' ' * 4)
    # Begin lexing.
    msg = kxpclexer.lex(msg)
    # ...and that's it for this.
    return msg

def lexMessage(string):
    lexlist = [(mecmd, _mecmdre),
               (colorBegin, _ctag_begin), (colorBegin, _gtag_begin),
               (colorEnd, _ctag_end),
               # karxi: Disabled this for now. No common versions of Pesterchum
               # actually use it, save for Chumdroid...which shouldn't.
               # When I change out parsers, I might add it back in.
               ##(formatBegin, _format_begin), (formatEnd, _format_end),
               (imagelink, _imgre),
               (hyperlink, _urlre), (hyperlink_lazy, _url2re),
               (memolex, _memore),
               (chumhandlelex, _handlere),
               (smiley, _smilere),
               (honker, _honk)]

    string = str(string)
    string = string.replace("\n", " ").replace("\r", " ")
    lexed = lexer(str(string), lexlist)

    balanced = []
    beginc = 0
    endc = 0
    for o in lexed:
        if type(o) is colorBegin:
            beginc += 1
            balanced.append(o)
        elif type(o) is colorEnd:
            if beginc >= endc:
                endc += 1
                balanced.append(o)
            else:
                balanced.append(o.string)
        else:
            balanced.append(o)
    if beginc > endc:
        for i in range(0, beginc-endc):
            balanced.append(colorEnd("</c>"))
    if len(balanced) == 0:
        balanced.append("")
    if type(balanced[len(balanced)-1]) not in [str, str]:
        balanced.append("")
    return balanced

def convertTags(lexed, format="html"):
    if format not in ["html", "bbcode", "ctag", "text"]:
        raise ValueError("Color format not recognized")

    if type(lexed) in [str, str]:
        lexed = lexMessage(lexed)
    escaped = ""
    firststr = True
    for (i, o) in enumerate(lexed):
        if type(o) in [str, str]:
            if format == "html":
                escaped += o.replace("&", "&amp;").replace(">", "&gt;").replace("<","&lt;")
            else:
                escaped += o
        else:
            escaped += o.convert(format)

    return escaped

def _max_msg_len(mask=None, target=None, nick=None, ident=None):
    # karxi: Copied from another file of mine, and modified to work with
    # Pesterchum.
    # Note that this effectively assumes the worst when not provided the
    # information it needs to get an accurate read, so later on, it'll need to
    # be given a nick or the user's hostmask, as well as where the message is
    # being sent.
    # It effectively has to construct the message that'll be sent in advance.
    limit = 512

    # Start subtracting
    # ':', " PRIVMSG ", ' ', ':', \r\n
    limit -= 14

    if mask is not None:
        # Since this will be included in what we send
        limit -= len(str(mask))
    else:
        # Since we should always be able to fetch this
        # karxi: ... Which we can't, right now, unlike in the old script.
        # TODO: Resolve this issue, give it the necessary information.
        
        # If we CAN'T, stick with a length of 30, since that seems to be
        # the average maximum nowadays
        limit -= len(nick) if nick is not None else 30
        # '!', '@'
        limit -= 2
        # ident length
        limit -= len(ident) if nick is not None else 10
        # Maximum (?) host length
        limit -= 63				# RFC 2812
    # The target is the place this is getting sent to - a channel or a nick
    if target is not None:
        limit -= len(target)
    else:
        # Normally I'd assume about 60...just to be safe.
        # However, the current (2016-11-13) Pesterchum limit for memo name
        # length is 32, so I'll bump it to 40 for some built-in leeway.
        limit -= 40

    return limit

def kxsplitMsg(lexed, ctx, fmt="pchum", maxlen=None, debug=False):
    """Split messages so that they don't go over the length limit.
    Returns a list of the messages, neatly split.
    
    Keep in mind that there's a little bit of magic involved in this at the
    moment; some unsafe assumptions are made."""

    # NOTE: Keep in mind that lexercon CTag objects convert to "r,g,b" format.
    # This means that they're usually going to be fairly long.
    # Support for changing this will probably be added later, but it won't work
    # properly with Chumdroid...I'll probably have to leave it as an actual
    # config option that's applied to the parser.

    # Procedure: Lex. Convert for lengths as we go, keep starting tag
    # length as we go too. Split whenever we hit the limit, add the tags to
    # the start of the next line (or just keep a running line length
    # total), and continue.
    # N.B.: Keep the end tag length too. (+4 for each.)
    # Copy the list so we can't break anything.
    # TODO: There's presently an issue where certain combinations of color
    # codes end up being added as a separate, empty line. This is a bug, of
    # course, and should be looked into.
    # TODO: This may not work properly with unicode! Because IRC doesn't
    # formally use it, it should probably use the lengths of the decomposed
    # characters...ugh.
    lexed = list(lexed)
    working = []
    output = []
    open_ctags = []
    # Number of characters we've used.
    curlen = 0
    # Maximum number of characters *to* use.
    if not maxlen:
        maxlen = __max_msg_len(None, None, ctx.mainwindow.profile().handle, ctx.mainwindow.irc.cli.real_name)
    elif maxlen < 0:
        # Subtract the (negative) length, giving us less leeway in this
        # function.
        maxlen = _max_msg_len(None, None, ctx.mainwindow.profile().handle, ctx.mainwindow.irc.cli.real_name) + maxlen

    # Defined here, but modified in the loop.
    msglen = 0

    def efflenleft():
        """Get the remaining space we have to work with, accounting for closing
        tags that will be needed."""
        return maxlen - curlen - (len(open_ctags) * 4)

    safekeeping = lexed[:]
    lexed = collections.deque(lexed)
    rounds = 0
    # NOTE: This entire mess is due for a rewrite. I'll start splitting it into
    # sub-functions for the eventualities that arise during parsing.
    # (E.g. the text block splitter NEEDS to be a different function....)
    while len(lexed) > 0:
        rounds += 1
        if debug:
            logging.info("[Starting round {}...]".format(rounds))
        msg = lexed.popleft()
        msglen = 0
        is_text = False

        try:
            msglen = len(msg.convert(fmt))
        except AttributeError:
            # It's probably not a lexer tag. Assume a string.
            # The input to this is supposed to be sanitary, after all.
            msglen = len(msg)
            # We allow this to error out if it fails for some reason.
            # Remind us that it's a string, and thus can be split.
            is_text = True

        # Test if we have room.
        if msglen > efflenleft():
            # We do NOT have room - which means we need to think of how to
            # handle this.
            # If we have text, we can split it, keeping color codes in mind.
            # Since those were already parsed, we don't have to worry about
            # breaking something that way.
            # Thus, we can split it, finalize it, and add the remainder to the
            # next line (after the color codes).
            if is_text and efflenleft() > 30:
                # We use 30 as a general 'guess' - if there's less space than
                # that, it's probably not worth trying to cram text in.
                # This also saves us from infinitely trying to reduce the size
                # of the input.
                stack = []
                # We have text to split.
                # This is okay because we don't apply the changes until the
                # end - and the rest is shoved onto the stack to be dealt with
                # immediately after.
                lenl = efflenleft()
                subround = 0
                while len(msg) > lenl:
                    # NOTE: This may be cutting it a little close. Maybe use >=
                    # instead?
                    subround += 1
                    if debug:
                        logging.info("[Splitting round {}-{}...]".format(
                                rounds, subround
                                ))
                    point = msg.rfind(' ', 0, lenl)
                    if point < 0:
                        # No spaces to break on...ugh. Break at the last space
                        # we can instead.
                        point = lenl ## - 1
                        # NOTE: The - 1 is for safety (but probably isn't
                        # actually necessary.)
                    # Split and push what we have.
                    stack.append(msg[:point])
                    # Remove what we just added.
                    msg = msg[point:]
                    if debug:
                        logging.info("msg = {!r}".format(msg))
                else:
                    # Catch the remainder.
                    stack.append(msg)
                    if debug:
                        logging.info("msg caught; stack = {!r}".format(stack))
                # Done processing. Pluck out the first portion so we can
                # continue processing, clean it up a bit, then add the rest to
                # our waiting list.
                msg = stack.pop(0).rstrip()
                msglen = len(msg)
                # A little bit of touching up for the head of our next line.
                stack[0] = stack[0].lstrip()
                # Now we have a separated list, so we can add it.
                # First we have to reverse it, because the extendleft method of
                # deque objects - like our lexed queue - inserts the elements
                # *backwards*....
                stack.reverse()
                # Now we put them on 'top' of the proverbial deck, and deal
                # with them next round.
                lexed.extendleft(stack)
                # We'll deal with those later. Now to get the 'msg' on the
                # working list and finalize it for output - which really just
                # means forcing the issue....
                working.append(msg)
                curlen += msglen
                # NOTE: This is here so we can catch it later - it marks that
                # we've already worked on this.
                msg = None

            # Clear the slate. Add the remaining ctags, then add working to
            # output, then clear working and statistics. Then we can move on.
            # Keep in mind that any open ctags get added to the beginning of
            # working again, since they're still open!

            # Add proper CTagEnd objects ourselves. Won't break anything to use
            # raw text at time of writing, but it can't hurt to be careful.
            # We specify the ref as our format, to note. They should match up,
            # both being 'pchum'.
            # It shouldn't matter that we use the same object for this - the
            # process of rendering isn't destructive.
            # This also doesn't follow compression settings, but closing color
            # tags can't BE compressed, so it hardly matters.
            cte = lexercon.CTagEnd("</c>", fmt, None)
            working.extend([cte] * len(open_ctags))
            if debug:
                print("\tRound {0} linebreak: Added {1} closing ctags".format(
                        rounds, len(open_ctags)
                        ))

            # Run it through the lexer again to render it.
            working = ''.join(kxpclexer.list_convert(working))
            if debug:
                print("\tRound {0} add: len == {1} (of {2})".format(
                        rounds, len(working), maxlen
                        ))
            # Now that it's done the work for us, append and resume.
            output.append(working)

            if msg is not None:
                # We didn't catch it earlier for preprocessing. Thus, toss it
                # on the stack and continue, so it'll go through the loop.
                # Remember, we're doing this because we don't have enough space
                # for it. Hopefully it'll fit on the next line, or split.
                lexed.appendleft(msg)
                # Fall through to the next case.
            if lexed:
                # We have more to go.
                # Reset working, starting it with the unclosed ctags.
                if debug:
                    print("\tRound {0}: More to lex".format(rounds))
                working = open_ctags[:]
                # Calculate the length of the starting tags, add it before
                # anything else.
                curlen = sum(len(tag.convert(fmt)) for tag in working)
            else:
                # There's nothing in lexed - but if msg wasn't None, we ADDED
                # it to lexed. Thus, if we get here, we don't have anything
                # more to add.
                # Getting here means we already flushed the last of what we had
                # to the stack.
                # Nothing in lexed. If we didn't preprocess, then we're done.
                if debug or True:
                    # This probably shouldn't happen, and if it does, I want to
                    # know if it *works* properly.
                    print("\tRound {0}: No more to lex".format(rounds))
                # Clean up, just in case.
                working = []
                open_ctags = []
                curlen = 0
                # TODO: What does this mean for the ctags that'd be applied?
                # Will this break parsing? It shouldn't, but....

                # Break us out of the loop...we could BREAK here and skip the
                # else, since we know what's going on.
                continue
            # We got here because we have more to process, so head back to
            # resume.
            continue

        # Normal tag processing stuff. Considerably less interesting/intensive
        # than the text processing we did up there.
        if isinstance(msg, lexercon.CTagEnd):
            # Check for Ends first (subclassing issue).
            if len(open_ctags) > 0:
                # Don't add it unless it's going to make things /more/ even.
                # We could have a Strict checker that errors on that, who
                # knows.
                # We just closed a ctag.
                open_ctags.pop()
            else:
                # Ignore it.
                # NOTE: I realize this is going to screw up something I do, but
                # it also stops us from screwing up Chumdroid, so...whatever.
                continue
        elif isinstance(msg, lexercon.CTag):
            # It's an opening color tag!
            open_ctags.append(msg)
            # TODO: Check and see if we have enough room for the lexemes
            # *after* this one. If not, shunt it back into lexed and flush
            # working into output.

        # Add it to the working message.
        working.append(msg)

        # Record the additional length.
        # Also, need to be sure to account for the ends that would be added.
        curlen += msglen
    else:
        # Once we're finally out of things to add, we're, well...out.
        # So add working to the result one last time.
        working = kxpclexer.list_convert(working)
        if len(working) > 0:
            if debug:
                print("Adding end trails: {!r}".format(working))
            working = ''.join(working)
            output.append(working)

    # We're...done?
    return output

def _is_ooc(msg, strict=True):
    """Check if a line is OOC. Note that Pesterchum *is* kind enough to strip
    trailing spaces for us, even in the older versions, but we don't do that in
    this function. (It's handled by the calling one.)"""
    # Define the matching braces.
    braces = (
            ('(', ')'),
            ('[', ']'),
            ('{', '}')
            )

    oocDetected = _oocre.match(msg)
    # Somewhat-improved matching.
    if oocDetected:
        if not strict:
            # The regex matched and we're supposed to be lazy. We're done here.
            return True
        # We have a match....
        ooc1, ooc2 = oocDetected.group(1, 2)
        # Make sure the appropriate braces are used.
        mbraces = [ooc1 == br[0] and ooc2 == br[1] for br in braces]
        if any(mbraces):
            # If any of those passes matched, we're good to go; it's OOC.
            return True
    return False

def kxhandleInput(ctx, text=None, flavor=None):
    """The function that user input that should be sent to the server is routed
    through. Handles lexing, splitting, and quirk application, as well as
    sending."""
    # TODO: This needs a 'dryrun' option, and ways to specify alternative
    # outputs and such, if it's to handle all of these.
    # Flavor is important for logic, ctx is 'self'.
    # Flavors are 'convo', 'menus', and 'memos' - so named after the source
    # files for the original sentMessage variants.

    if flavor is None:
        raise ValueError("A flavor is needed to determine suitable logic!")

    if text is None:
        # Fetch the raw text from the input box.
        text = ctx.textInput.text()
        text = str(ctx.textInput.text())

    # Preprocessing stuff.
    msg = text.strip()
    if msg == "" or msg.startswith("PESTERCHUM:"):
        # We don't allow users to send system messages. There's also no
        # point if they haven't entered anything.
        return

    # Add the *raw* text to our history.
    ctx.history.add(text)

    oocDetected = _is_ooc(msg, strict=True)

    if flavor != "menus":
        # Determine if we should be OOC.
        is_ooc = ctx.ooc or oocDetected
        # Determine if the line actually *is* OOC.
        if is_ooc and not oocDetected:
            # If we're supposed to be OOC, apply it artificially.
            msg = "(( {} ))".format(msg)
        # Also, quirk stuff.
        should_quirk = ctx.applyquirks
    else:
        # 'menus' means a quirk tester window, which doesn't have an OOC
        # variable, so we assume it's not OOC.
        # It also invariably has quirks enabled, so there's no setting for
        # that.
        is_ooc = False
        should_quirk = True

    # I'm pretty sure that putting a space before a /me *should* break the
    # /me, but in practice, that's not the case.
    is_action = msg.startswith("/me")
    
    # Begin message processing.
    # We use 'text' despite its lack of processing because it's simpler.
    if should_quirk and not (is_action or is_ooc):
        if flavor != "menus":
            # Fetch the quirks we'll have to apply.
            quirks = ctx.mainwindow.userprofile.quirks
        else:
            # The quirk testing window uses a different set.
            quirks = dataobjs.pesterQuirks(ctx.parent().testquirks())

        try:
            # Do quirk things. (Ugly, but it'll have to do for now.)
            # TODO: Look into the quirk system, modify/redo it.
            # Gotta encapsulate or we might parse the wrong way.
            msg = quirks.apply([msg])
        except Exception as err:
            # Tell the user we couldn't do quirk things.
            # TODO: Include the actual error...and the quirk it came from?
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText("Whoa there! There seems to be a problem.")
            err_info = "A quirk seems to be having a problem. (Error: {!s})"
            err_info = err_info.format(err)
            msgbox.setInformativeText(err_info)
            msgbox.exec_()
            return
        
    # Debug output.
    try:
        # Turns out that Windows consoles can't handle unicode, heh...who'da
        # thunk. We have to repr() this, as such.
        print(repr(msg))
    except Exception as err:
        print("(Couldn't print processed message: {!s})".format(err))

    # karxi: We have a list...but I'm not sure if we ever get anything else, so
    # best to play it safe. I may remove this during later refactoring.
    if isinstance(msg, list):
        for i, m in enumerate(msg):
            if isinstance(m, lexercon.Chunk):
                # NOTE: KLUDGE. Filters out old PChum objects.
                # karxi: This only works because I went in and subtyped them to
                # an object type I provided - just so I could pluck them out
                # later.
                msg[i] = m.convert(format="ctag")
        msg = ''.join(msg)

    # Quirks have been applied. Lex the messages (finally).
    msg = kxlexMsg(msg)

    # Debug output.
    try:
        print(repr(msg))
    except Exception as err:
        print("(Couldn't print lexed message: {!s})".format(err))

    # Remove coloring if this is a /me!
    if is_action:
        # Filter out formatting specifiers (just ctags, at the moment).
        msg = [m for m in msg if not isinstance(m,
                    (lexercon.CTag, lexercon.CTagEnd)
                    )]
        # We'll also add /me to the beginning of any new messages, later.

    # Put what's necessary in before splitting.
    # Fetch our time if we're producing this for a memo.
    if flavor == "memos":
        if ctx.time.getTime() == None:
            ctx.sendtime()
        grammar = ctx.time.getGrammar()
        # Oh, great...there's a parsing error to work around. Times are added
        # automatically when received, but not when added directly?... I'll
        # have to unify that.
        # TODO: Fix parsing disparity.
        initials = ctx.mainwindow.profile().initials()
        colorcmd = ctx.mainwindow.profile().colorcmd()
        # We'll use those later.

    # Split the messages so we don't go over the buffer and lose text.
    maxlen = _max_msg_len(None, None, ctx.mainwindow.profile().handle, ctx.mainwindow.irc.cli.real_name)
         # ctx.mainwindow.profile().handle ==> Get handle
         # ctx.mainwindow.irc.cli.real_name  ==> Get ident (Same as realname in this case.)
    # Since we have to do some post-processing, we need to adjust the maximum
    # length we can use.
    if flavor == "convo":
        # The old Pesterchum setup used 200 for this.
        maxlen = 300
    elif flavor == "memos":
        # Use the max, with some room added so we can make additions.
        # The additions are theoretically 23 characters long, max.
        maxlen -= 25

    # Split the message. (Finally.)
    # This is also set up to parse it into strings.
    lexmsgs = kxsplitMsg(msg, ctx, "pchum", maxlen=maxlen)
    # Strip off the excess.
    for i, m in enumerate(lexmsgs):
        lexmsgs[i] = m.strip()

    # Pester message handling.
    if flavor == "convo":
        # if ceased, rebegin
        if hasattr(ctx, 'chumopen') and not ctx.chumopen:
            ctx.mainwindow.newConvoStarted.emit(
                    QString(ctx.title()), True
                    )
            ctx.setChumOpen(True)

    # Post-process and send the messages.
    for i, lm in enumerate(lexmsgs):
        # If we're working with an action and we split, it should have /mes.
        if is_action and i > 0:
            # Add them post-split.
            lm = "/me " + lm
            # NOTE: No reason to reassign for now, but...why not?
            lexmsgs[i] = lm

        # Copy the lexed result.
        # Note that memos have to separate processing here. The adds and sends
        # should be kept to the end because of that, near the emission.
        clientMsg = copy(lm)
        serverMsg = copy(lm)

        # Memo-specific processing.
        if flavor == "memos" and not is_action:
            # Quirks were already applied, so get the prefix/postfix stuff
            # ready.
            # We fetched the information outside of the loop, so just
            # construct the messages.

            clientMsg = "<c={1}>{2}{3}{4}: {0}</c>".format(
                    clientMsg, colorcmd, grammar.pcf, initials, grammar.number
                    )
            # Not sure if this needs a space at the end...?
            serverMsg = "<c={1}>{2}: {0}</c>".format(
                    serverMsg, colorcmd, initials)

        ctx.addMessage(clientMsg, True)
        if flavor != "menus":
            # If we're not doing quirk testing, actually send.
            ctx.messageSent.emit(serverMsg, ctx.title())

    # Clear the input.
    ctx.textInput.setText("")


def addTimeInitial(string, grammar):
    endofi = string.find(":")
    endoftag = string.find(">")
    # support Doc Scratch mode
    if (endoftag < 0 or endoftag > 16) or (endofi < 0 or endofi > 17):
        return string
    return string[0:endoftag+1]+grammar.pcf+string[endoftag+1:endofi]+grammar.number+string[endofi:]

def timeProtocol(cmd):
    dir = cmd[0]
    if dir == "?":
        return mysteryTime(0)
    cmd = cmd[1:]
    cmd = re.sub("[^0-9:]", "", cmd)
    try:
        l = [int(x) for x in cmd.split(":")]
    except ValueError:
        l = [0,0]
    timed = timedelta(0, l[0]*3600+l[1]*60)
    if dir == "P":
        timed = timed*-1
    return timed

def timeDifference(td):
    if td == timedelta(microseconds=1): # mysteryTime replacement :(
        return "??:?? FROM ????"
    if td < timedelta(0):
        when = "AGO"
    else:
        when = "FROM NOW"
    atd = abs(td)
    minutes = (atd.days*86400 + atd.seconds) // 60
    hours = minutes // 60
    leftoverminutes = minutes % 60
    if atd == timedelta(0):
        timetext = "RIGHT NOW"
    elif atd < timedelta(0,3600):
        if minutes == 1:
            timetext = "%d MINUTE %s" % (minutes, when)
        else:
            timetext = "%d MINUTES %s" % (minutes, when)
    elif atd < timedelta(0,3600*100):
        if hours == 1 and leftoverminutes == 0:
            timetext = "%d:%02d HOUR %s" % (hours, leftoverminutes, when)
        else:
            timetext = "%d:%02d HOURS %s" % (hours, leftoverminutes, when)
    else:
        timetext = "%d HOURS %s" % (hours, when)
    return timetext

def nonerep(text):
    return text

class parseLeaf(object):
    def __init__(self, function, parent):
        self.nodes = []
        self.function = function
        self.parent = parent
    def append(self, node):
        self.nodes.append(node)
    def expand(self, mo):
        out = ""
        for n in self.nodes:
            if type(n) == parseLeaf:
                out += n.expand(mo)
            elif type(n) == backreference:
                out += mo.group(int(n.number))
            else:
                out += n
        out = self.function(out)
        return out

class backreference(object):
    def __init__(self, number):
        self.number = number
    def __str__(self):
        return self.number

def parseRegexpFunctions(to):
    parsed = parseLeaf(nonerep, None)
    current = parsed
    curi = 0
    functiondict = quirkloader.quirks
    while curi < len(to):
        tmp = to[curi:]
        mo = _functionre.search(tmp)
        if mo is not None:
            if mo.start() > 0:
                current.append(to[curi:curi+mo.start()])
            backr = _groupre.search(mo.group())
            if backr is not None:
                current.append(backreference(backr.group(1)))
            elif mo.group()[:-1] in list(functiondict.keys()):
                p = parseLeaf(functiondict[mo.group()[:-1]], current)
                current.append(p)
                current = p
            elif mo.group() == ")":
                if current.parent is not None:
                    current = current.parent
                else:
                    current.append(")")
            curi = mo.end()+curi
        else:
            current.append(to[curi:])
            curi = len(to)
    return parsed


def img2smiley(string):
    string = str(string)
    def imagerep(mo):
        return reverse_smiley[mo.group(1)]
    string = re.sub(r'<img src="smilies/(\S+)" />', imagerep, string)
    return string

smiledict = {
    ":rancorous:": "pc_rancorous.png",
    ":apple:": "apple.png",
    ":bathearst:": "bathearst.png",
    ":cathearst:": "cathearst.png",
    ":woeful:": "pc_bemused.png",
    ":sorrow:": "blacktear.png",
    ":pleasant:": "pc_pleasant.png",
    ":blueghost:": "blueslimer.gif",
    ":slimer:": "slimer.gif",
    ":candycorn:": "candycorn.png",
    ":cheer:": "cheer.gif",
    ":duhjohn:": "confusedjohn.gif",
    ":datrump:": "datrump.png",
    ":facepalm:": "facepalm.png",
    ":bonk:": "headbonk.gif",
    ":mspa:": "mspa_face.png",
    ":gun:": "mspa_reader.gif",
    ":cal:": "lilcal.png",
    ":amazedfirman:": "pc_amazedfirman.png",
    ":amazed:": "pc_amazed.png",
    ":chummy:": "pc_chummy.png",
    ":cool:": "pccool.png",
    ":smooth:": "pccool.png",
    ":distraughtfirman": "pc_distraughtfirman.png",
    ":distraught:": "pc_distraught.png",
    ":insolent:": "pc_insolent.png",
    ":bemused:": "pc_bemused.png",
    ":3:": "pckitty.png",
    ":mystified:": "pc_mystified.png",
    ":pranky:": "pc_pranky.png",
    ":tense:": "pc_tense.png",
    ":record:": "record.gif",
    ":squiddle:": "squiddle.gif",
    ":tab:": "tab.gif",
    ":beetip:": "theprofessor.png",
    ":flipout:": "weasel.gif",
    ":befuddled:": "what.png",
    ":pumpkin:": "whatpumpkin.png",
    ":trollcool:": "trollcool.png",
    ":jadecry:": "jadespritehead.gif",
    ":ecstatic:": "ecstatic.png",
    ":relaxed:": "relaxed.png",
    ":discontent:": "discontent.png",
    ":devious:": "devious.png",
    ":sleek:": "sleek.png",
    ":detestful:": "detestful.png",
    ":mirthful:": "mirthful.png",
    ":manipulative:": "manipulative.png",
    ":vigorous:": "vigorous.png",
    ":perky:": "perky.png",
    ":acceptant:": "acceptant.png",
    ":olliesouty:": "olliesouty.gif",
    ":billiards:": "poolballS.gif",
    ":billiardslarge:": "poolballL.gif",
    ":whatdidyoudo:": "whatdidyoudo.gif",
    ":brocool:": "pcstrider.png",
    ":trollbro:": "trollbro.png",
    ":playagame:": "saw.gif",
    ":trollc00l:": "trollc00l.gif",
    ":suckers:": "Suckers.gif",
    ":scorpio:": "scorpio.gif",
    ":shades:": "shades.png",
    }

if ostools.isOSXBundle():
    for emote in smiledict:
        graphic = smiledict[emote]
        if graphic.find(".gif"):
            graphic = graphic.replace(".gif", ".png")
            smiledict[emote] = graphic




reverse_smiley = dict((v,k) for k, v in smiledict.items())
_smilere = re.compile("|".join(list(smiledict.keys())))

class ThemeException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def themeChecker(theme):
    needs = ["main/size", "main/icon", "main/windowtitle", "main/style", \
    "main/background-image", "main/menubar/style", "main/menu/menuitem", \
    "main/menu/style", "main/menu/selected", "main/close/image", \
    "main/close/loc", "main/minimize/image", "main/minimize/loc", \
    "main/menu/loc", "main/menus/client/logviewer", \
    "main/menus/client/addgroup", "main/menus/client/options", \
    "main/menus/client/exit", "main/menus/client/userlist", \
    "main/menus/client/memos", "main/menus/client/import", \
    "main/menus/client/idle", "main/menus/client/reconnect", \
    "main/menus/client/_name", "main/menus/profile/quirks", \
    "main/menus/profile/block", "main/menus/profile/color", \
    "main/menus/profile/switch", "main/menus/profile/_name", \
    "main/menus/help/about", "main/menus/help/_name", "main/moodlabel/text", \
    "main/moodlabel/loc", "main/moodlabel/style", "main/moods", \
    "main/addchum/style", "main/addchum/text", "main/addchum/size", \
    "main/addchum/loc", "main/pester/text", "main/pester/size", \
    "main/pester/loc", "main/block/text", "main/block/size", "main/block/loc", \
    "main/mychumhandle/label/text", "main/mychumhandle/label/loc", \
    "main/mychumhandle/label/style", "main/mychumhandle/handle/loc", \
    "main/mychumhandle/handle/size", "main/mychumhandle/handle/style", \
    "main/mychumhandle/colorswatch/size", "main/mychumhandle/colorswatch/loc", \
    "main/defaultmood", "main/chums/size", "main/chums/loc", \
    "main/chums/style", "main/menus/rclickchumlist/pester", \
    "main/menus/rclickchumlist/removechum", \
    "main/menus/rclickchumlist/blockchum", "main/menus/rclickchumlist/viewlog", \
    "main/menus/rclickchumlist/removegroup", \
    "main/menus/rclickchumlist/renamegroup", \
    "main/menus/rclickchumlist/movechum", "convo/size", \
    "convo/tabwindow/style", "convo/tabs/tabstyle", "convo/tabs/style", \
    "convo/tabs/selectedstyle", "convo/style", "convo/margins", \
    "convo/chumlabel/text", "convo/chumlabel/style", "convo/chumlabel/align/h", \
    "convo/chumlabel/align/v", "convo/chumlabel/maxheight", \
    "convo/chumlabel/minheight", "main/menus/rclickchumlist/quirksoff", \
    "main/menus/rclickchumlist/addchum", "main/menus/rclickchumlist/blockchum", \
    "main/menus/rclickchumlist/unblockchum", \
    "main/menus/rclickchumlist/viewlog", "main/trollslum/size", \
    "main/trollslum/style", "main/trollslum/label/text", \
    "main/trollslum/label/style", "main/menus/profile/block", \
    "main/chums/moods/blocked/icon", "convo/systemMsgColor", \
    "convo/textarea/style", "convo/text/beganpester", "convo/text/ceasepester", \
    "convo/text/blocked", "convo/text/unblocked", "convo/text/blockedmsg", \
    "convo/text/idle", "convo/input/style", "memos/memoicon", \
    "memos/textarea/style", "memos/systemMsgColor", "convo/text/joinmemo", \
    "memos/input/style", "main/menus/rclickchumlist/banuser", \
    "main/menus/rclickchumlist/opuser", "main/menus/rclickchumlist/voiceuser", \
    "memos/margins", "convo/text/openmemo", "memos/size", "memos/style", \
    "memos/label/text", "memos/label/style", "memos/label/align/h", \
    "memos/label/align/v", "memos/label/maxheight", "memos/label/minheight", \
    "memos/userlist/style", "memos/userlist/width", "memos/time/text/width", \
    "memos/time/text/style", "memos/time/arrows/left", \
    "memos/time/arrows/style", "memos/time/buttons/style", \
    "memos/time/arrows/right", "memos/op/icon", "memos/voice/icon", \
    "convo/text/closememo", "convo/text/kickedmemo", \
    "main/chums/userlistcolor", "main/defaultwindow/style", \
    "main/chums/moods", "main/chums/moods/chummy/icon", "main/menus/help/help", \
    "main/menus/help/calsprite", "main/menus/help/nickserv", "main/menus/help/chanserv", \
    "main/menus/rclickchumlist/invitechum", "main/menus/client/randen", \
    "main/menus/rclickchumlist/memosetting", "main/menus/rclickchumlist/memonoquirk", \
    "main/menus/rclickchumlist/memohidden", "main/menus/rclickchumlist/memoinvite", \
    "main/menus/rclickchumlist/memomute", "main/menus/rclickchumlist/notes"]

    for n in needs:
        try:
            theme[n]
        except KeyError:
            raise ThemeException("Missing theme requirement: %s" % (n))
