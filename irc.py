import logging, logging.config
logging.config.fileConfig('logging.conf')
PchumLog = logging.getLogger('pchumLogger')
from PyQt5 import QtCore, QtGui
from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers, services
import random
import socket
from time import time

from mood import Mood
from dataobjs import PesterProfile
from generic import PesterList
from version import _pcVersion

import ostools
try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

#if ostools.isOSXBundle():
#    logging.basicConfig(level=logging.WARNING)
#else:
#    # karxi; We do NOT need this set to INFO; it's very, very spammy.
#    logging.basicConfig(level=logging.WARNING)

class PesterIRC(QtCore.QThread):
    def __init__(self, config, window):
        QtCore.QThread.__init__(self)
        self.mainwindow = window
        self.config = config
        self.registeredIRC = False
        self.stopIRC = None
        self.NickServ = services.NickServ()
        self.ChanServ = services.ChanServ()
    def IRCConnect(self):
        server = self.config.server()
        port = self.config.port()
        self.cli = IRCClient(PesterHandler, host=server, port=int(port), nick=self.mainwindow.profile().handle, real_name='pcc31', blocking=True, timeout=120)
        self.cli.command_handler.parent = self
        self.cli.command_handler.mainwindow = self.mainwindow
        self.cli.connect()
        self.conn = self.cli.conn()
    def run(self):
        try:
            self.IRCConnect()
        except socket.error as se:
            self.stopIRC = se
            return
        while 1:
            res = True
            try:
                PchumLog.debug("updateIRC()")
                res = self.updateIRC()
            except socket.timeout as se:
                PchumLog.debug("timeout in thread %s" % (self))
                self.cli.close()
                self.stopIRC = se
                return
            except socket.error as se:
                if self.registeredIRC:
                    self.stopIRC = None
                else:
                    self.stopIRC = se
                PchumLog.debug("socket error, exiting thread")
                return
            else:
                if not res:
                    PchumLog.debug("false Yield: %s, returning" % res)
                    return

    def setConnected(self):
        self.registeredIRC = True
        self.connected.emit()
    def setConnectionBroken(self):
        PchumLog.debug("setconnection broken")
        self.reconnectIRC()
        #self.brokenConnection = True
    @QtCore.pyqtSlot()
    def updateIRC(self):
        try:
            res = next(self.conn)
        except socket.timeout as se:
            if self.registeredIRC:
                return True
            else:
                raise se
        except socket.error as se:
            raise se
        except StopIteration:
            self.conn = self.cli.conn()
            return True
        else:
            return res
    @QtCore.pyqtSlot()
    def reconnectIRC(self):
        PchumLog.debug("reconnectIRC() from thread %s" % (self))
        self.cli.close()

    @QtCore.pyqtSlot(PesterProfile)
    def getMood(self, *chums):
        self.cli.command_handler.getMood(*chums)
    @QtCore.pyqtSlot(PesterList)
    def getMoods(self, chums):
        self.cli.command_handler.getMood(*chums)
    @QtCore.pyqtSlot(QString, QString)
    def sendNotice(self, text, handle):
        h = str(handle)
        t = str(text)
        try:
            helpers.notice(self.cli, h, t)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString, QString)
    def sendMessage(self, text, handle):
        h = str(handle)
        textl = [str(text)]
        def splittext(l):
            if len(l[0]) > 450:
                space = l[0].rfind(" ", 0,430)
                if space == -1:
                    space = 450
                elif l[0][space+1:space+5] == "</c>":
                    space = space+4
                a = l[0][0:space+1]
                b = l[0][space+1:]
                if a.count("<c") > a.count("</c>"):
                    # oh god ctags will break!! D=
                    hanging = []
                    usedends = []
                    c = a.rfind("<c")
                    while c != -1:
                        d = a.find("</c>", c)
                        while d in usedends:
                            d = a.find("</c>", d+1)
                        if d != -1: usedends.append(d)
                        else:
                            f = a.find(">", c)+1
                            hanging.append(a[c:f])
                        c = a.rfind("<c",0,c)

                    # end all ctags in first part
                    for i in range(a.count("<c")-a.count("</c>")):
                        a = a + "</c>"
                    #start them up again in the second part
                    for c in hanging:
                        b = c + b
                if len(b) > 0:
                    return [a] + splittext([b])
                else:
                    return [a]
            else:
                return l
        textl = splittext(textl)
        try:
            for t in textl:
                helpers.msg(self.cli, h, t)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString, bool)
    def startConvo(self, handle, initiated):
        h = str(handle)
        try:
            helpers.msg(self.cli, h, "COLOR >%s" % (self.mainwindow.profile().colorcmd()))
            if initiated:
                helpers.msg(self.cli, h, "PESTERCHUM:BEGIN")
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def endConvo(self, handle):
        h = str(handle)
        try:
            helpers.msg(self.cli, h, "PESTERCHUM:CEASE")
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot()
    def updateProfile(self):
        me = self.mainwindow.profile()
        handle = me.handle
        try:
            helpers.nick(self.cli, handle)
        except socket.error:
            self.setConnectionBroken()
        self.mainwindow.closeConversations(True)
        self.mainwindow.doAutoIdentify()
        self.mainwindow.autoJoinDone = False
        self.mainwindow.doAutoJoins()
        self.updateMood()
    @QtCore.pyqtSlot()
    def updateMood(self):
        me = self.mainwindow.profile()
        try:
            helpers.msg(self.cli, "#pesterchum", "MOOD >%d" % (me.mood.value()))
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot()
    def updateColor(self):
        #PchumLog.debug("irc updateColor (outgoing)")
        me = self.mainwindow.profile()
        for h in list(self.mainwindow.convos.keys()):
            try:
                helpers.msg(self.cli, h, "COLOR >%s" % (self.mainwindow.profile().colorcmd()))
            except socket.error:
                self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def blockedChum(self, handle):
        h = str(handle)
        try:
            helpers.msg(self.cli, h, "PESTERCHUM:BLOCK")
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def unblockedChum(self, handle):
        h = str(handle)
        try:
            helpers.msg(self.cli, h, "PESTERCHUM:UNBLOCK")
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def requestNames(self, channel):
        c = str(channel)
        try:
            helpers.names(self.cli, c)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot()
    def requestChannelList(self):
        try:
            helpers.channel_list(self.cli)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def joinChannel(self, channel):
        c = str(channel)
        try:
            helpers.join(self.cli, c)
            helpers.mode(self.cli, c, "", None)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def leftChannel(self, channel):
        c = str(channel)
        try:
            helpers.part(self.cli, c)
            self.cli.command_handler.joined = False
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString, QString)
    def kickUser(self, handle, channel):
        l = handle.split(":")
        c = str(channel)
        h = str(l[0])
        if len(l) > 1:
            reason = str(l[1])
            if len(l) > 2:
              for x in l[2:]:
                reason += str(":") + str(x)
        else:
            reason = ""
        try:
            helpers.kick(self.cli, h, c, reason)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString, QString, QString)
    def setChannelMode(self, channel, mode, command):
        c = str(channel)
        m = str(mode)
        cmd = str(command)
        PchumLog.debug("c=%s\nm=%s\ncmd=%s" % (c,m,cmd))
        if cmd == "":
            cmd = None
        try:
            helpers.mode(self.cli, c, m, cmd)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString)
    def channelNames(self, channel):
        c = str(channel)
        try:
            helpers.names(self.cli, c)
        except socket.error:
            self.setConnectionBroken()
    @QtCore.pyqtSlot(QString, QString)
    def inviteChum(self, handle, channel):
        h = str(handle)
        c = str(channel)
        try:
            helpers.invite(self.cli, h, c)
        except socket.error:
            self.setConnectionBroken()

    @QtCore.pyqtSlot()
    def pingServer(self):
        try:
            self.cli.send("PING %s" % int(time()))
        except socket.error:
            self.setConnectionBroken()

    @QtCore.pyqtSlot(bool)
    def setAway(self, away=True):
        try:
            if away:
                self.cli.send("AWAY Idle")
            else:
                self.cli.send("AWAY")
        except socket.error:
            self.setConnectionBroken()

    @QtCore.pyqtSlot(QString, QString)
    def killSomeQuirks(self, channel, handle):
        c = str(channel)
        h = str(handle)
        try:
            helpers.ctcp(self.cli, c, "NOQUIRKS", h)
        except socket.error:
            self.setConnectionBroken()
            
    def quit_dc(self):
        helpers.quit(self.cli, _pcVersion + " <3")

    #def getMask(self):
        # This needs to be updated when our hostname is changed.
        # Nevermind this entire thing, actually.

    moodUpdated = QtCore.pyqtSignal('QString', Mood)
    colorUpdated = QtCore.pyqtSignal('QString', QtGui.QColor)
    messageReceived = QtCore.pyqtSignal('QString', 'QString')
    memoReceived = QtCore.pyqtSignal('QString', 'QString', 'QString')
    noticeReceived = QtCore.pyqtSignal('QString', 'QString')
    inviteReceived = QtCore.pyqtSignal('QString', 'QString')
    timeCommand = QtCore.pyqtSignal('QString', 'QString', 'QString')
    namesReceived = QtCore.pyqtSignal('QString', PesterList)
    channelListReceived = QtCore.pyqtSignal(PesterList)
    nickCollision = QtCore.pyqtSignal('QString', 'QString')
    myHandleChanged = QtCore.pyqtSignal('QString')
    chanInviteOnly = QtCore.pyqtSignal('QString')
    modesUpdated = QtCore.pyqtSignal('QString', 'QString')
    connected = QtCore.pyqtSignal()
    userPresentUpdate = QtCore.pyqtSignal('QString', 'QString',
                                   'QString')
    cannotSendToChan = QtCore.pyqtSignal('QString', 'QString')
    tooManyPeeps = QtCore.pyqtSignal()
    quirkDisable = QtCore.pyqtSignal('QString', 'QString', 'QString')

class PesterHandler(DefaultCommandHandler):
    def notice(self, nick, chan, msg):
        #try:
        #    msg = msg.decode('utf-8')
        #except UnicodeDecodeError:
        #    msg = msg.decode('iso-8859-1', 'ignore')
        #nick = nick.decode('utf-8')
        #chan = chan.decode('utf-8')
        handle = nick[0:nick.find("!")]
        PchumLog.info("---> recv \"NOTICE %s :%s\"" % (handle, msg))
        if handle == "ChanServ" and chan == self.parent.mainwindow.profile().handle and msg[0:2] == "[#":
                self.parent.memoReceived.emit(msg[1:msg.index("]")], handle, msg)
        else:
            self.parent.noticeReceived.emit(handle, msg)
    def privmsg(self, nick, chan, msg):
        #try:
        #    msg = msg.decode('utf-8')
        #except UnicodeDecodeError:
        #    msg = msg.decode('iso-8859-1', 'ignore')
        # display msg, do other stuff
        if len(msg) == 0:
            return
        # silently ignore CTCP
        # Notice IRC /me (The CTCP kind)
        if msg[0:8] == '\x01ACTION ':
            msg = '/me' + msg[7:-1]
        # silently ignore the rest of the CTCPs
        if msg[0] == '\x01':
            handle = nick[0:nick.find("!")]
            PchumLog.warning("---> recv \"CTCP %s :%s\"" % (handle, msg[1:-1]))
            if msg[1:-1] == "VERSION":
                helpers.ctcp_reply(self.parent.cli, handle, "VERSION", "Pesterchum %s" % (_pcVersion))
            elif msg[1:-1].startswith("NOQUIRKS") and chan[0] == "#":
                op = nick[0:nick.find("!")]
                self.parent.quirkDisable.emit(chan, msg[10:-1], op)
            return
        handle = nick[0:nick.find("!")]

        if chan != "#pesterchum":
            # We don't need anywhere near that much spam.
            PchumLog.info("---> recv \"PRIVMSG %s :%s\"" % (handle, msg))

        if chan == "#pesterchum":
            # follow instructions
            if msg[0:6] == "MOOD >":
                try:
                    mood = Mood(int(msg[6:]))
                except ValueError:
                    mood = Mood(0)
                self.parent.moodUpdated.emit(handle, mood)
            elif msg[0:7] == "GETMOOD":
                mychumhandle = self.mainwindow.profile().handle
                mymood = self.mainwindow.profile().mood.value()
                if msg.find(mychumhandle, 8) != -1:
                    helpers.msg(self.client, "#pesterchum",
                                "MOOD >%d" % (mymood))
        elif chan[0] == '#':
            if msg[0:16] == "PESTERCHUM:TIME>":
                self.parent.timeCommand.emit(chan, handle, msg[16:])
            else:
                self.parent.memoReceived.emit(chan, handle, msg)
        else:
            # private message
            # silently ignore messages to yourself.
            if handle == self.mainwindow.profile().handle:
                return
            if msg[0:7] == "COLOR >":
                colors = msg[7:].split(",")
                try:
                    colors = [int(d) for d in colors]
                except ValueError as e:
                    PchumLog.warning(e)
                    colors = [0,0,0]
                PchumLog.debug("colors: " + str(colors))
                color = QtGui.QColor(*colors)
                self.parent.colorUpdated.emit(handle, color)
            else:
                self.parent.messageReceived.emit(handle, msg)


    def welcome(self, server, nick, msg):
        self.parent.setConnected()
        mychumhandle = self.mainwindow.profile().handle
        mymood = self.mainwindow.profile().mood.value()
        if not self.mainwindow.config.lowBandwidth():
            from time import sleep
            sleep(0.5) # To prevent TLS from dying </3
            helpers.join(self.client, "#pesterchum")
            helpers.msg(self.client, "#pesterchum", "MOOD >%d" % (mymood))
            
    def nicknameinuse(self, server, cmd, nick, msg):
        newnick = "pesterClient%d" % (random.randint(100,999))
        helpers.nick(self.client, newnick)
        self.parent.nickCollision.emit(nick, newnick)
    def quit(self, nick, reason):
        handle = nick[0:nick.find("!")]
        PchumLog.info("---> recv \"QUIT %s: %s\"" % (handle, reason))
        if handle == self.parent.mainwindow.randhandler.randNick:
            self.parent.mainwindow.randhandler.setRunning(False)
        server = self.parent.mainwindow.config.server()
        baseserver = server[server.rfind(".", 0, server.rfind(".")):]
        if reason.count(baseserver) == 2:
            self.parent.userPresentUpdate.emit(handle, "", "netsplit")
        else:
            self.parent.userPresentUpdate.emit(handle, "", "quit")
        self.parent.moodUpdated.emit(handle, Mood("offline"))
    def kick(self, opnick, channel, handle, reason):
        op = opnick[0:opnick.find("!")]
        self.parent.userPresentUpdate.emit(handle, channel, "kick:%s:%s" % (op, reason))
        # ok i shouldnt be overloading that but am lazy
    def part(self, nick, channel, reason="nanchos"):
        handle = nick[0:nick.find("!")]
        PchumLog.info("---> recv \"PART %s: %s\"" % (handle, channel))
        self.parent.userPresentUpdate.emit(handle, channel, "left")
        if channel == "#pesterchum":
            self.parent.moodUpdated.emit(handle, Mood("offline"))
    def join(self, nick, channel):
        handle = nick[0:nick.find("!")]
        PchumLog.info("---> recv \"JOIN %s: %s\"" % (handle, channel))
        self.parent.userPresentUpdate.emit(handle, channel, "join")
        if channel == "#pesterchum":
            if handle == self.parent.mainwindow.randhandler.randNick:
                self.parent.mainwindow.randhandler.setRunning(True)
            self.parent.moodUpdated.emit(handle, Mood("chummy"))
    def mode(self, op, channel, mode, *handles):
        PchumLog.debug("op=" + str(op))
        PchumLog.debug("channel=" + str(channel))
        PchumLog.debug("mode=" + str(mode))
        PchumLog.debug("*handles=" + str(handles))

        if len(handles) <= 0: handles = [""]
        opnick = op[0:op.find("!")]
        PchumLog.debug("opnick=" + opnick)

        # Channel section
        # Okay so, as I understand it channel modes will always be applied to a channel even if the commands also sets a mode to a user.
        # So "MODE #channel +ro handleHandle" will set +r to channel #channel as well as set +o to handleHandle
        # Therefore the bellow method causes a crash if both user and channel mode are being set in one command.

        #if op == channel or channel == self.parent.mainwindow.profile().handle:
        #    modes = list(self.parent.mainwindow.modes)
        #    if modes and modes[0] == "+": modes = modes[1:]
        #    if mode[0] == "+":
        #        for m in mode[1:]:
        #            if m not in modes:
        #                modes.extend(m)
        #    elif mode[0] == "-":
        #        for i in mode[1:]:
        #            try:
        #                modes.remove(i)
        #            except ValueError:
        #                pass
        #    modes.sort()
        #    self.parent.mainwindow.modes = "+" + "".join(modes)


        # EXPIRIMENTAL FIX
        # No clue how stable this is but since it doesn't seem to cause a crash it's probably an improvement.
        # This might be clunky with non-unrealircd IRC servers
        channel_mode = ""
        unrealircd_channel_modes = ['c', 'C', 'd', 'f', 'G', 'H', 'i', 'k', 'K', 'L', 'l', 'm', 'M', 'N', 'n', 'O', 'P', 'p', 'Q', 'R', 'r', 's', 'S', 'T', 't', 'V', 'z', 'Z']
        if any(md in mode for md in unrealircd_channel_modes):
            PchumLog.debug("Channel mode in string.")
            modes = list(self.parent.mainwindow.modes)
            for md in unrealircd_channel_modes:
                if mode.find(md)!= -1: # -1 means not found
                    PchumLog.debug("md=" + md)
                    if mode[0] == "+":
                        modes.extend(md)
                        channel_mode = "+"  + md
                    elif mode[0] == "-":
                        try:
                            modes.remove(md)
                            channel_mode = "-" + md
                        except ValueError:
                            PchumLog.warning("Can't remove channel mode that isn't set.")
                            pass
                    self.parent.userPresentUpdate.emit("", channel, channel_mode+":%s" % (op))
                    PchumLog.debug("pre-mode=" + str(mode))
                    mode = mode.replace(md, "")
                    PchumLog.debug("post-mode=" + str(mode))
            modes.sort()
            self.parent.mainwindow.modes = "+" + "".join(modes)
            
        modes = []
        cur = "+"
        for l in mode:
            if l in ["+","-"]: cur = l
            else:
                modes.append("%s%s" % (cur, l))
        PchumLog.debug("handles=" + str(handles))
        PchumLog.debug("enumerate(modes) = " + str(list(enumerate(modes))))
        for (i,m) in enumerate(modes):

            # Server-set usermodes don't need to be passed.
            if (handles == ['']) & ( ('x' in m) | ('z' in m) | ('o' in m) | ('x' in m) )!=True:
                try:
                    self.parent.userPresentUpdate.emit(handles[i], channel, m+":%s" % (op))
                except:
                    PchumLog.exception('')
                    
                #self.parent.userPresentUpdate.emit(handles[i], channel, m+":%s" % (op))
            # Passing an empty handle here might cause a crash.
            #except IndexError:
                #self.parent.userPresentUpdate.emit("", channel, m+":%s" % (op))
                
    def nick(self, oldnick, newnick):
        oldhandle = oldnick[0:oldnick.find("!")]
        if oldhandle == self.mainwindow.profile().handle:
            self.parent.myHandleChanged.emit(newnick)
        newchum = PesterProfile(newnick, chumdb=self.mainwindow.chumdb)
        self.parent.moodUpdated.emit(oldhandle, Mood("offline"))
        self.parent.userPresentUpdate.emit("%s:%s" % (oldhandle, newnick), "", "nick")
        if newnick in self.mainwindow.chumList.chums:
            self.getMood(newchum)
        if oldhandle == self.parent.mainwindow.randhandler.randNick:
                self.parent.mainwindow.randhandler.setRunning(False)
        elif newnick == self.parent.mainwindow.randhandler.randNick:
                self.parent.mainwindow.randhandler.setRunning(True)
    def namreply(self, server, nick, op, channel, names):
        namelist = names.split(" ")
        PchumLog.info("---> recv \"NAMES %s: %d names\"" % (channel, len(namelist)))
        if not hasattr(self, 'channelnames'):
            self.channelnames = {}
        if channel not in self.channelnames:
            self.channelnames[channel] = []
        self.channelnames[channel].extend(namelist)
    #def ison(self, server, nick, nicks):
    #    nicklist = nicks.split(" ")
    #    getglub = "GETMOOD "
    #    PchumLog.info("---> recv \"ISON :%s\"" % nicks)
    #    for nick_it in nicklist:
    #        self.parent.moodUpdated.emit(nick_it, Mood(0))
    #        if nick_it in self.parent.mainwindow.namesdb["#pesterchum"]:
    #           getglub += nick_it
    #    if getglub != "GETMOOD ":
    #        helpers.msg(self.client, "#pesterchum", getglub)
            
    def endofnames(self, server, nick, channel, msg):
        namelist = self.channelnames[channel]
        pl = PesterList(namelist)
        del self.channelnames[channel]
        self.parent.namesReceived.emit(channel, pl)
        if channel == "#pesterchum" and (not hasattr(self, "joined") or not self.joined):
            self.joined = True
            self.parent.mainwindow.randhandler.setRunning(self.parent.mainwindow.randhandler.randNick in namelist)
            chums = self.mainwindow.chumList.chums
            #self.isOn(*chums)
            lesschums = []
            for c in chums:
                chandle = c.handle
                if chandle in namelist:
                    lesschums.append(c)
            self.getMood(*lesschums)

    def liststart(self, server, handle, *info):
        self.channel_list = []
        info = list(info)
        self.channel_field = info.index("Channel") # dunno if this is protocol
        PchumLog.info("---> recv \"CHANNELS: %s " % (self.channel_field))
    def list(self, server, handle, *info):
        channel = info[self.channel_field]
        usercount = info[1]
        if channel not in self.channel_list and channel != "#pesterchum":
            self.channel_list.append((channel, usercount))
        PchumLog.info("---> recv \"CHANNELS: %s " % (channel))
    def listend(self, server, handle, msg):
        pl = PesterList(self.channel_list)
        PchumLog.info("---> recv \"CHANNELS END\"")
        self.parent.channelListReceived.emit(pl)
        self.channel_list = []

    def umodeis(self, server, handle, modes):
        self.parent.mainwindow.modes = modes
    def invite(self, sender, you, channel):
        handle = sender.split('!')[0]
        self.parent.inviteReceived.emit(handle, channel)
    def inviteonlychan(self, server, handle, channel, msg):
        self.parent.chanInviteOnly.emit(channel)
    def channelmodeis(self, server, handle, channel, modes):
        self.parent.modesUpdated.emit(channel, modes)
    def cannotsendtochan(self, server, handle, channel, msg):
        self.parent.cannotSendToChan.emit(channel, msg)
    def toomanypeeps(self, *stuff):
        self.parent.tooManyPeeps.emit()

    def ping(self, prefix, server):
        self.parent.mainwindow.lastping = int(time())
        self.client.send('PONG', server)

    def getMood(self, *chums):
        chumglub = "GETMOOD "
        for c in chums:
            chandle = c.handle
            if len(chumglub+chandle) >= 350:
                try:
                    helpers.msg(self.client, "#pesterchum", chumglub)
                except socket.error:
                    self.parent.setConnectionBroken()
                chumglub = "GETMOOD "
            chumglub += chandle
        if chumglub != "GETMOOD ":
            try:
                helpers.msg(self.client, "#pesterchum", chumglub)
            except socket.error:
                self.parent.setConnectionBroken()

    #def isOn(self, *chums):
    #    isonNicks = ""
    #    for c in chums:
    #        chandle = c.handle
    #        if len(chandle) >= 200:
    #            try:
    #                self.client.send("ISON", ":%s" % (isonNicks))
    #            except socket.error:
    #                self.parent.setConnectionBroken()
    #            isonNicks = ""
    #        isonNicks += " " + chandle
    #    if isonNicks != "":
    #        try:
    #            self.client.send("ISON", ":%s" % (isonNicks))
    #        except socket.error:
    #            self.parent.setConnectionBroken()
