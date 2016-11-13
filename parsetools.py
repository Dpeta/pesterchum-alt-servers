import re
import random
import ostools
from copy import copy
from datetime import timedelta
from PyQt5 import QtGui

from generic import mysteryTime
from quirks import ScriptQuirks
from pyquirks import PythonQuirks
from luaquirks import LuaQuirks

_ctag_begin = re.compile(r'(?i)<c=(.*?)>')
_gtag_begin = re.compile(r'(?i)<g[a-f]>')
_ctag_end = re.compile(r'(?i)</c>')
_ctag_rgb = re.compile(r'\d+,\d+,\d+')
_urlre = re.compile(r"(?i)(?:^|(?<=\s))(?:(?:https?|ftp)://|magnet:)[^\s]+")
_url2re = re.compile(r"(?i)www\.[^\s]+")
_memore = re.compile(r"(\s|^)(#[A-Za-z0-9_]+)")
_handlere = re.compile(r"(\s|^)(@[A-Za-z0-9_]+)")
_imgre = re.compile(r"""(?i)<img src=['"](\S+)['"]\s*/>""")
_mecmdre = re.compile(r"^(/me|PESTERCHUM:ME)(\S*)")
oocre = re.compile(r"[\[(][\[(].*[\])][\])]")
_format_begin = re.compile(r'(?i)<([ibu])>')
_format_end = re.compile(r'(?i)</([ibu])>')
_honk = re.compile(r"(?i)\bhonk\b")

quirkloader = ScriptQuirks()
quirkloader.add(PythonQuirks())
quirkloader.add(LuaQuirks())
quirkloader.loadAll()
print quirkloader.funcre()
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
            if type(s) not in [str, unicode]:
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

class colorBegin(object):
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
class colorEnd(object):
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
class formatBegin(object):
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
class formatEnd(object):
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
class hyperlink(object):
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
class imagelink(object):
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
class memolex(object):
    def __init__(self, string, space, channel):
        self.string = string
        self.space = space
        self.channel = channel
    def convert(self, format):
        if format == "html":
            return "%s<a href='%s'>%s</a>" % (self.space, self.channel, self.channel)
        else:
            return self.string
class chumhandlelex(object):
    def __init__(self, string, space, handle):
        self.string = string
        self.space = space
        self.handle = handle
    def convert(self, format):
        if format == "html":
            return "%s<a href='%s'>%s</a>" % (self.space, self.handle, self.handle)
        else:
            return self.string
class smiley(object):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "<img src='smilies/%s' alt='%s' title='%s' />" % (smiledict[self.string], self.string, self.string)
        else:
            return self.string
class honker(object):
    def __init__(self, string):
        self.string = string
    def convert(self, format):
        if format == "html":
            return "<img src='smilies/honk.png' alt'honk' title='honk' />"
        else:
            return self.string
class mecmd(object):
    def __init__(self, string, mecmd, suffix):
        self.string = string
        self.suffix = suffix
    def convert(self, format):
        return self.string

def lexMessage(string):
    lexlist = [(mecmd, _mecmdre),
               (colorBegin, _ctag_begin), (colorBegin, _gtag_begin),
               (colorEnd, _ctag_end),
               (formatBegin, _format_begin), (formatEnd, _format_end),
               (imagelink, _imgre),
               (hyperlink, _urlre), (hyperlink_lazy, _url2re),
               (memolex, _memore),
               (chumhandlelex, _handlere),
               (smiley, _smilere),
               (honker, _honk)]

    string = unicode(string)
    string = string.replace("\n", " ").replace("\r", " ")
    lexed = lexer(unicode(string), lexlist)

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
    if type(balanced[len(balanced)-1]) not in [str, unicode]:
        balanced.append("")
    return balanced

def convertTags(lexed, format="html"):
    if format not in ["html", "bbcode", "ctag", "text"]:
        raise ValueError("Color format not recognized")

    if type(lexed) in [str, unicode]:
        lexed = lexMessage(lexed)
    escaped = ""
    firststr = True
    for (i, o) in enumerate(lexed):
        if type(o) in [str, unicode]:
            if format == "html":
                escaped += o.replace("&", "&amp;").replace(">", "&gt;").replace("<","&lt;")
            else:
                escaped += o
        else:
            escaped += o.convert(format)

    return escaped

def splitMessage(msg, format="ctag"):
    """Splits message if it is too long."""
    # split long text lines
    buf = []
    for o in msg:
        if type(o) in [str, unicode] and len(o) > 200:
            for i in range(0, len(o), 200):
                buf.append(o[i:i+200])
        else:
            buf.append(o)
    msg = buf
    okmsg = []
    cbegintags = []
    output = []
    for o in msg:
        oldctag = None
        okmsg.append(o)
        if type(o) is colorBegin:
            cbegintags.append(o)
        elif type(o) is colorEnd:
            try:
                oldctag = cbegintags.pop()
            except IndexError:
                pass
        # yeah normally i'd do binary search but im lazy
        msglen = len(convertTags(okmsg, format)) + 4*(len(cbegintags))
        if msglen > 400:
            okmsg.pop()
            if type(o) is colorBegin:
                cbegintags.pop()
            elif type(o) is colorEnd and oldctag is not None:
                cbegintags.append(oldctag)
            if len(okmsg) == 0:
                output.append([o])
            else:
                tmp = []
                for color in cbegintags:
                    okmsg.append(colorEnd("</c>"))
                    tmp.append(color)
                output.append(okmsg)
                if type(o) is colorBegin:
                    cbegintags.append(o)
                elif type(o) is colorEnd:
                    try:
                        cbegintags.pop()
                    except IndexError:
                        pass
                tmp.append(o)
                okmsg = tmp

    if len(okmsg) > 0:
        output.append(okmsg)
    return output



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
    if type(td) is mysteryTime:
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
            elif mo.group()[:-1] in functiondict.keys():
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
    string = unicode(string)
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




reverse_smiley = dict((v,k) for k, v in smiledict.iteritems())
_smilere = re.compile("|".join(smiledict.keys()))

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
