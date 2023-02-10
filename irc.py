"""Provides classes and functions for communicating with an IRC server.

References for the IRC protocol:
 - Original IRC protocol specification: https://www.rfc-editor.org/rfc/rfc1459
 - Updated IRC Client specification: https://www.rfc-editor.org/rfc/rfc2812
 - Modern IRC client protocol writeup: https://modern.ircdocs.horse
 - IRCv3 protocol additions: https://ircv3.net/irc/
 - Draft of metadata specification: https://gist.github.com/k4bek4be/92c2937cefd49990fbebd001faf2b237

Some code in this file may be based on the oyoyo IRC library,
the license notice included with oyoyo source files is indented here:
    
    # Copyright (c) 2008 Duncan Fordyce
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    # The above copyright notice and this permission notice shall be included in
    #  all copies or substantial portions of the Software.
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    # THE SOFTWARE.

"""
import sys
import socket
import random
import datetime
import logging
from ssl import SSLEOFError, SSLCertVerificationError

try:
    from PyQt6 import QtCore, QtGui
except ImportError:
    print("PyQt5 fallback (irc.py)")
    from PyQt5 import QtCore, QtGui

from mood import Mood
from dataobjs import PesterProfile
from generic import PesterList
from version import _pcVersion
from scripts.irc_protocol import SendIRC, parse_irc_line
from scripts.ssl_context import get_ssl_context

PchumLog = logging.getLogger("pchumLogger")
SERVICES = [
    "nickserv",
    "chanserv",
    "memoserv",
    "operserv",
    "helpserv",
    "hostserv",
    "botserv",
]


class PesterIRC(QtCore.QThread):
    """Class for making a thread that manages the connection to server."""

    def __init__(self, config, window, verify_hostname=True):
        QtCore.QThread.__init__(self)
        self.mainwindow = window
        self.config = config
        self.unresponsive = False
        self.registeredIRC = False
        self.verify_hostname = verify_hostname
        self.metadata_supported = False
        self.stopIRC = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.config.server()
        self.port = self.config.port()
        self.ssl = self.config.ssl()
        self._end = False

        self.send_irc = SendIRC()

        self.conn = None

        self.joined = False
        self.channelnames = {}
        self.channel_list = []
        self.channel_field = None

        self.commands = {
            "001": self.welcome,
            "005": self.featurelist,
            "221": self.umodeis,
            "321": self.liststart,
            "322": self.list,
            "323": self.listend,
            "324": self.channelmodeis,
            "353": self.namreply,
            "366": self.endofnames,
            "432": self.erroneusnickname,
            "433": self.nicknameinuse,
            "436": self.nickcollision,
            "448": self.forbiddenchannel,  # non-standard
            "473": self.inviteonlychan,
            "761": self.keyvalue,  # 7XX is ircv3 deprecated metadata spec
            "766": self.nomatchingkey,
            "768": self.keynotset,
            "769": self.keynopermission,
            "770": self.metadatasubok,
            "error": self.error,
            "join": self.join,
            "kick": self.kick,
            "mode": self.mode,
            "part": self.part,
            "ping": self.ping,
            "privmsg": self.privmsg,
            "notice": self.notice,
            "quit": self.quit,
            "invite": self.invite,
            "nick": self.nick,  # We can get svsnicked
            "metadata": self.metadata,  # Metadata specification
            "tagmsg": self.tagmsg,  # IRCv3 message tags extension
            "cap": self.cap,  # IRCv3 Client Capability Negotiation
        }

    def connect(self, verify_hostname=True):
        """Initiates the connection to the server set in self.host:self.port
        self.ssl decides whether the connection uses ssl.

        Certificate validation when using SSL/TLS may be disabled by
        passing the 'verify_hostname' parameter. The user is asked if they
        want to disable it if this functions raises a certificate validation error,
        in which case the function may be called again with 'verify_hostname'."""
        PchumLog.info("Connecting to %s:%s", self.host, self.port)

        # Open connection
        plaintext_socket = socket.create_connection((self.host, self.port))

        if self.ssl:
            # Upgrade connection to use SSL/TLS if enabled
            context = get_ssl_context()
            context.check_hostname = verify_hostname
            self.socket = context.wrap_socket(
                plaintext_socket, server_hostname=self.host
            )
        else:
            # SSL/TLS is disabled, connection is plaintext
            self.socket = plaintext_socket

        self.socket.settimeout(90)
        self.send_irc.socket = self.socket

        self.send_irc.nick(self.mainwindow.profile().handle)
        self.send_irc.user("pcc31", "pcc31")
        # if self.connect_cb:
        #    self.connect_cb(self)

    def conn_generator(self):
        """Returns a generator object."""
        try:
            buffer = b""
            while not self._end:
                try:
                    buffer += self.socket.recv(1024)
                except OSError as e:
                    PchumLog.warning("conn_generator exception %s in %s", e, self)
                    if self._end:
                        break
                    raise e
                else:
                    if self._end:
                        break

                    split_buffer = buffer.split(b"\r\n")
                    buffer = b""
                    if split_buffer[-1]:
                        # Incomplete line, add it back to the buffer.
                        buffer = split_buffer.pop()

                    for line in split_buffer:
                        line = line.decode(encoding="utf-8", errors="replace")
                        tags, prefix, command, args = parse_irc_line(line)
                        if command:
                            # Only need tags with tagmsg
                            if command.casefold() == "tagmsg":
                                self.run_command(command, prefix, tags, *args)
                            else:
                                self.run_command(command, prefix, *args)

                yield True
        except socket.timeout as se:
            PchumLog.debug("passing timeout")
            raise se
        except (OSError, SSLEOFError) as se:
            PchumLog.warning("Problem: %s", se)
            if self.socket:
                PchumLog.info("Error: closing socket.")
                self.socket.close()
            raise se
        except Exception as e:
            PchumLog.exception("Non-socket exception in conn_generator().")
            raise e
        else:
            PchumLog.debug("Ending conn() while loop, end is %s.", self._end)
            if self.socket:
                PchumLog.info("Finished: closing socket.")
                self.socket.close()
            yield False

    def run_command(self, command, *args):
        """Finds and runs a command if it has a matching function in the self.command dict."""
        PchumLog.debug("run_command %s(%s)", command, args)
        if command in self.commands:
            command_function = self.commands[command]
        else:
            PchumLog.warning("No matching function for command: %s(%s)", command, args)
            return

        try:
            command_function(*args)
        except TypeError:
            PchumLog.exception(
                "Failed to pass command, did the server pass an unsupported paramater?"
            )
        except Exception:
            PchumLog.exception("Exception while parsing command.")

    def close(self):
        """Kill the socket 'with extreme prejudice'."""
        if self.socket:
            PchumLog.info("close() was called, shutting down socket.")
            self._end = True
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                PchumLog.info("Error while shutting down socket, already broken? %s", e)
            try:
                self.socket.close()
            except OSError as e:
                PchumLog.info("Error while closing socket, already broken? %s", e)

    def IRCConnect(self):
        try:
            self.connect(self.verify_hostname)
        except SSLCertVerificationError as e:
            # Ask if users wants to connect anyway
            self.askToConnect.emit(e)
            raise e
        self.conn = self.conn_generator()

    def run(self):
        """Connect and run update loop."""
        try:
            self.IRCConnect()
        except OSError as se:
            self.stopIRC = se
            return
        while True:
            res = True
            try:
                PchumLog.debug("updateIRC()")
                self.mainwindow.sincerecv = 0
                res = self.updateIRC()
            except socket.timeout as se:
                PchumLog.debug("timeout in thread %s", self)
                self.close()
                self.stopIRC = "{}, {}".format(type(se), se)
                return
            except (OSError, IndexError, ValueError) as se:
                self.stopIRC = "{}, {}".format(type(se), se)
                PchumLog.debug("Socket error, exiting thread.")
                return
            else:
                if not res:
                    PchumLog.debug("False Yield: %s, returning", res)
                    return
                
    def setConnectionBroken(self):
        """Called when the connection is broken."""
        PchumLog.critical("setConnectionBroken() got called, disconnecting.")
        self.disconnectIRC()

    @QtCore.pyqtSlot()
    def updateIRC(self):
        """Get a silly scrunkler from the generator!!"""
        try:
            res = next(self.conn)
        except socket.timeout as se:
            if self.registeredIRC:
                return True
            else:
                raise se
        except OSError as se:
            raise se
        except (OSError, ValueError, IndexError) as se:
            raise se
        except StopIteration:
            self.conn = self.conn_generator()
            return True
        else:
            return res

    @QtCore.pyqtSlot(PesterProfile)
    def getMood(self, *chums):
        """Get mood via metadata if supported"""

        # Get via metadata or via legacy method
        if self.metadata_supported:
            # Metadata
            for chum in chums:
                try:
                    self.send_irc.metadata(chum.handle, "get", "mood")
                except OSError as e:
                    PchumLog.warning(e)
                    self.setConnectionBroken()
        else:
            # Legacy
            PchumLog.warning(
                "Server doesn't seem to support metadata, using legacy GETMOOD."
            )
            chumglub = "GETMOOD "
            for chum in chums:
                if len(chumglub + chum.handle) >= 350:
                    try:
                        self.send_irc.privmsg("#pesterchum", chumglub)
                    except OSError as e:
                        PchumLog.warning(e)
                        self.setConnectionBroken()
                    chumglub = "GETMOOD "
                # No point in GETMOOD-ing services
                if chum.handle.casefold() not in SERVICES:
                    chumglub += chum.handle
            if chumglub != "GETMOOD ":
                try:
                    self.send_irc.privmsg("#pesterchum", chumglub)
                except OSError as e:
                    PchumLog.warning(e)
                    self.setConnectionBroken()

    @QtCore.pyqtSlot(PesterList)
    def getMoods(self, chums):
        self.getMood(*chums)

    @QtCore.pyqtSlot(str, str)
    def sendNotice(self, text, handle):
        self.send_irc.notice(handle, text)

    @QtCore.pyqtSlot(str, str)
    def sendMessage(self, text, handle):
        """......sends a message? this is a tad silly;;;"""
        textl = [text]

        def splittext(l):
            if len(l[0]) > 450:
                space = l[0].rfind(" ", 0, 430)
                if space == -1:
                    space = 450
                elif l[0][space + 1 : space + 5] == "</c>":
                    space = space + 4
                a = l[0][0 : space + 1]
                b = l[0][space + 1 :]
                if a.count("<c") > a.count("</c>"):
                    # oh god ctags will break!! D=
                    hanging = []
                    usedends = []
                    c = a.rfind("<c")
                    while c != -1:
                        d = a.find("</c>", c)
                        while d in usedends:
                            d = a.find("</c>", d + 1)
                        if d != -1:
                            usedends.append(d)
                        else:
                            f = a.find(">", c) + 1
                            hanging.append(a[c:f])
                        c = a.rfind("<c", 0, c)

                    # end all ctags in first part
                    for _ in range(a.count("<c") - a.count("</c>")):
                        a = a + "</c>"
                    # start them up again in the second part
                    for c in hanging:
                        b = c + b
                if b:  # len > 0
                    return [a] + splittext([b])
                else:
                    return [a]
            else:
                return l

        textl = splittext(textl)
        for t in textl:
            self.send_irc.privmsg(handle, t)

    @QtCore.pyqtSlot(str, str)
    def sendCTCP(self, handle, text):
        self.send_irc.ctcp(handle, text)

    @QtCore.pyqtSlot(str, bool)
    def startConvo(self, handle, initiated):
        self.send_irc.privmsg(handle, f"COLOR >{self.mainwindow.profile().colorcmd()}")
        if initiated:
            self.send_irc.privmsg(handle, "PESTERCHUM:BEGIN")

    @QtCore.pyqtSlot(str)
    def endConvo(self, handle):
        self.send_irc.privmsg(handle, "PESTERCHUM:CEASE")

    @QtCore.pyqtSlot()
    def updateProfile(self):
        self.send_irc.nick(self.mainwindow.profile().handle)
        self.mainwindow.closeConversations(True)
        self.mainwindow.doAutoIdentify()
        self.mainwindow.autoJoinDone = False
        self.mainwindow.doAutoJoins()
        self.updateMood()

    @QtCore.pyqtSlot()
    def updateMood(self):
        mood = str(self.mainwindow.profile().mood.value())
        # Moods via metadata
        self.send_irc.metadata("*", "set", "mood", mood)
        # Backwards compatibility
        self.send_irc.privmsg("#pesterchum", f"MOOD >{mood}")

    @QtCore.pyqtSlot()
    def updateColor(self):
        # Update color metadata field
        color = self.mainwindow.profile().color
        self.send_irc.metadata("*", "set", "color", str(color.name()))
        # Send color messages
        for convo in list(self.mainwindow.convos.keys()):
            self.send_irc.privmsg(
                convo,
                f"COLOR >{self.mainwindow.profile().colorcmd()}",
            )

    @QtCore.pyqtSlot(str)
    def blockedChum(self, handle):
        self.send_irc.privmsg(handle, "PESTERCHUM:BLOCK")

    @QtCore.pyqtSlot(str)
    def unblockedChum(self, handle):
        self.send_irc.privmsg(handle, "PESTERCHUM:UNBLOCK")

    @QtCore.pyqtSlot(str)
    def requestNames(self, channel):
        self.send_irc.names(channel)

    @QtCore.pyqtSlot()
    def requestChannelList(self):
        self.send_irc.list()

    @QtCore.pyqtSlot(str)
    def joinChannel(self, channel):
        self.send_irc.join(channel)
        self.send_irc.mode(channel)

    @QtCore.pyqtSlot(str)
    def leftChannel(self, channel):
        self.send_irc.part(channel)

    @QtCore.pyqtSlot(str, str, str)
    def kickUser(self, channel, user, reason=""):
        self.send_irc.kick(channel, user, reason)

    @QtCore.pyqtSlot(str, str, str)
    def setChannelMode(self, channel, mode, command):
        self.send_irc.mode(channel, mode, command)

    @QtCore.pyqtSlot(str)
    def channelNames(self, channel):
        self.send_irc.names(channel)

    @QtCore.pyqtSlot(str, str)
    def inviteChum(self, handle, channel):
        self.send_irc.invite(handle, channel)

    @QtCore.pyqtSlot()
    def pingServer(self):
        self.send_irc.ping("B33")

    @QtCore.pyqtSlot(bool)
    def setAway(self, away=True):
        if away:
            self.away("Idle")
        else:
            self.away()

    @QtCore.pyqtSlot(str, str)
    def killSomeQuirks(self, channel, handle):
        self.send_irc.ctcp(channel, "NOQUIRKS", handle)

    @QtCore.pyqtSlot()
    def disconnectIRC(self):
        self.send_irc.quit(f"{_pcVersion} <3")
        self._end = True
        self.close()

    def notice(self, nick, chan, msg):
        """Standard IRC 'NOTICE' message, primarily used for automated replies from services."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "NOTICE {} :{}"'.format(handle, msg))
        if (
            handle == "ChanServ"
            and chan == self.mainwindow.profile().handle
            and msg[0:2] == "[#"
        ):
            self.memoReceived.emit(msg[1 : msg.index("]")], handle, msg)
        else:
            self.noticeReceived.emit(handle, msg)

    def metadata(self, _target, nick, key, _visibility, value):
        """METADATA DRAFT metadata message from server.

        The format of the METADATA server notication is:
        METADATA <Target> <Key> <Visibility> <Value>
        """
        if key.casefold() == "mood":
            try:
                mood = Mood(int(value))
                self.moodUpdated.emit(nick, mood)
            except ValueError:
                PchumLog.warning("Invalid mood value, %s, %s", nick, mood)
        elif key.casefold() == "color":
            color = QtGui.QColor(value)  # Invalid color becomes rgb 0,0,0
            self.colorUpdated.emit(nick, color)

    def tagmsg(self, prefix, tags, *args):
        """IRCv3 'TAGMSG' message/command, contains a tag without a command.

        For reference see:
        https://ircv3.net/specs/extensions/message-tags.html#the-tagmsg-tag-only-message
        """
        PchumLog.info("TAGMSG: %s %s %s", prefix, tags, args)
        message_tags = tags[1:].split(";")
        for tag in message_tags:
            if tag.startswith("+pesterchum"):
                # Pesterchum tag
                try:
                    key, value = tag.split("=")
                except ValueError:
                    return
                PchumLog.info("Pesterchum tag: %s=%s", key, value)
                # PESTERCHUM: syntax check
                if value in [
                    "BEGIN",
                    "BLOCK",
                    "CEASE",
                    "BLOCK",
                    "BLOCKED",
                    "UNBLOCK",
                    "IDLE",
                    "ME",
                ]:
                    # Process like it's a PESTERCHUM: PRIVMSG
                    msg = "PESTERCHUM:" + value
                    self.privmsg(prefix, args[0], msg)
                elif value.startswith("COLOR>"):
                    # Process like it's a COLOR >0,0,0 PRIVMSG
                    msg = value.replace(">", " >")
                    self.privmsg(prefix, args[0], msg)
                elif value.startswith("TIME>"):
                    # Process like it's a PESTERCHUM:TIME> PRIVMSG
                    msg = "PESTERCHUM:" + value
                    self.privmsg(prefix, args[0], msg)
                else:
                    # Invalid syntax
                    PchumLog.warning("TAGMSG with invalid syntax.")

    def ping(self, _prefix, token):
        """'PING' command from server, we respond with PONG and a matching token."""
        self.send_irc.pong(token)

    def error(self, *params):
        """'ERROR' message from server, the server is terminating our connection."""
        self.stopIRC = " ".join(params).strip()
        self.disconnectIRC()

    def privmsg(self, nick, chan, msg):
        """'PRIVMSG' message from server, the standard message."""
        handle = nick[0 : nick.find("!")]
        if not msg:  # Length 0
            return
        # CTCP
        # ACTION, IRC /me (The CTCP kind)
        if msg[0:8] == "\x01ACTION ":
            msg = "/me" + msg[7:-1]
        # CTCPs that don't need to be shown
        elif msg[0] == "\x01":
            PchumLog.info('---> recv "CTCP %s :%s"', handle, msg[1:-1])
            # VERSION, return version
            if msg[1:-1].startswith("VERSION"):
                self.send_irc.ctcp(handle, "VERSION", "Pesterchum {_pcVersion}")
            # CLIENTINFO, return supported CTCP commands.
            elif msg[1:-1].startswith("CLIENTINFO"):
                self.send_irc.ctcp(
                    handle,
                    "CLIENTINFO",
                    "ACTION VERSION CLIENTINFO PING SOURCE NOQUIRKS GETMOOD",
                )
            # PING, return pong
            elif msg[1:-1].startswith("PING"):
                if len(msg[1:-1].split("PING ")) > 1:
                    self.send_irc.ctcp(handle, "PING", msg[1:-1].split("PING ")[1])
                else:
                    self.send_irc.ctcp(handle, "PING")
            # SOURCE, return source
            elif msg[1:-1].startswith("SOURCE"):
                self.send_irc.ctcp(
                    handle,
                    "SOURCE",
                    "https://github.com/Dpeta/pesterchum-alt-servers",
                )
            # ???
            elif msg[1:-1].startswith("NOQUIRKS") and chan[0] == "#":
                op = nick[0 : nick.find("!")]
                self.quirkDisable.emit(chan, msg[10:-1], op)
            # GETMOOD via CTCP
            elif msg[1:-1].startswith("GETMOOD"):
                # GETMOOD via CTCP
                # Maybe we can do moods like this in the future...
                mymood = self.mainwindow.profile().mood.value()
                self.send_irc.ctcp(handle, f"MOOD >{mymood}")
                # Backwards compatibility
                self.send_irc.privmsg(f"#pesterchum", f"MOOD >{mymood}")
            return

        if chan != "#pesterchum":
            # We don't need anywhere near that much spam.
            PchumLog.info('---> recv "PRIVMSG %s :%s"', handle, msg)

        if chan == "#pesterchum":
            # follow instructions
            if msg[0:6] == "MOOD >":
                try:
                    mood = Mood(int(msg[6:]))
                except ValueError:
                    mood = Mood(0)
                self.moodUpdated.emit(handle, mood)
            elif msg[0:7] == "GETMOOD":
                mychumhandle = self.mainwindow.profile().handle
                mymood = self.mainwindow.profile().mood.value()
                if msg.find(mychumhandle, 8) != -1:
                    self.send_irc.privmsg("#pesterchum", "MOOD >%d" % (mymood))
        elif chan[0] == "#":
            if msg[0:16] == "PESTERCHUM:TIME>":
                self.timeCommand.emit(chan, handle, msg[16:])
            else:
                self.memoReceived.emit(chan, handle, msg)
        else:
            # Normal PRIVMSG messages (the normal kind!!)
            if msg[0:7] == "COLOR >":
                colors = msg[7:].split(",")
                try:
                    colors = [int(d) for d in colors]
                except ValueError as e:
                    PchumLog.warning(e)
                    colors = [0, 0, 0]
                PchumLog.debug("colors: %s", colors)
                color = QtGui.QColor(*colors)
                self.colorUpdated.emit(handle, color)
            else:
                self.messageReceived.emit(handle, msg)

    def quit(self, nick, reason):
        """QUIT message from server, a client has quit the server."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "QUIT %s: %s"', handle, reason)
        if handle == self.mainwindow.randhandler.randNick:
            self.mainwindow.randhandler.setRunning(False)
        server = self.mainwindow.config.server()
        baseserver = server[server.rfind(".", 0, server.rfind(".")) :]
        if reason.count(baseserver) == 2:
            self.userPresentUpdate.emit(handle, "", "netsplit")
        else:
            self.userPresentUpdate.emit(handle, "", "quit")
        self.moodUpdated.emit(handle, Mood("offline"))

    def kick(self, opnick, channel, handle, reason):
        """'KICK' message from server, someone got kicked from a channel."""
        op = opnick[0 : opnick.find("!")]
        self.userPresentUpdate.emit(handle, channel, f"kick:{op}:{reason}")
        # ok i shouldnt be overloading that but am lazy

    def part(self, nick, channel, _reason="nanchos"):
        """'PART' message from server, someone left a channel."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "PART %s: %s"', handle, channel)
        self.userPresentUpdate.emit(handle, channel, "left")
        if channel == "#pesterchum":
            self.moodUpdated.emit(handle, Mood("offline"))

    def join(self, nick, channel):
        """'JOIN' message from server, someone joined a channel."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "JOIN %s: %s"', handle, channel)
        self.userPresentUpdate.emit(handle, channel, "join")
        if channel == "#pesterchum":
            if handle == self.mainwindow.randhandler.randNick:
                self.mainwindow.randhandler.setRunning(True)
            self.moodUpdated.emit(handle, Mood("chummy"))

    def mode(self, op, channel, mode, *handles):
        """'MODE' message from server, a user or a channel's mode changed."""
        PchumLog.debug(
            "mode(op=%s, channel=%s, mode=%s, handles=%s)", op, channel, mode, handles
        )
        if not handles:
            handles = [""]
        # opnick = op[0 : op.find("!")]
        # Channel section
        # This might be clunky with non-unrealircd IRC servers
        channel_mode = ""
        unrealircd_channel_modes = "cCdfGHikKLlmMNnOPpQRrsSTtVzZ"
        if any(md in mode for md in unrealircd_channel_modes):
            PchumLog.debug("Channel mode in string.")
            modes = list(self.mainwindow.modes)
            for md in unrealircd_channel_modes:
                if mode.find(md) != -1:  # -1 means not found
                    if mode[0] == "+":
                        modes.extend(md)
                        channel_mode = "+" + md
                    elif mode[0] == "-":
                        try:
                            modes.remove(md)
                            channel_mode = "-" + md
                        except ValueError:
                            PchumLog.warning(
                                "Can't remove channel mode that isn't set."
                            )
                    self.userPresentUpdate.emit("", channel, f"{channel_mode}:{op}")
                    PchumLog.debug("pre-mode=%s", mode)
                    mode = mode.replace(md, "")
                    PchumLog.debug("post-mode=%s", mode)
            modes.sort()
            self.mainwindow.modes = "+" + "".join(modes)

        modes = []
        cur = "+"
        for l in mode:
            if l in ["+", "-"]:
                cur = l
            else:
                modes.append(f"{cur}{l}")
        for i, m in enumerate(modes):
            # Server-set usermodes don't need to be passed.
            if handles == [""] and not ("x" in m or "z" in m or "o" in m or "x" in m):
                try:
                    self.userPresentUpdate.emit(handles[i], channel, m + f":{op}")
                except IndexError as e:
                    PchumLog.exception("modeSetIndexError: %s", e)

    def invite(self, sender, _you, channel):
        """'INVITE' message from server, someone invited us to a channel.

        Pizza party everyone invited!!!"""
        handle = sender.split("!")[0]
        self.inviteReceived.emit(handle, channel)

    def nick(self, oldnick, newnick, _hopcount=0):
        """'NICK' message from server, signifies a nick change.

        Is send when our or someone else's nick got changed willingly or unwillingly."""
        PchumLog.info(oldnick, newnick)
        # svsnick
        if oldnick == self.mainwindow.profile().handle:
            # Server changed our handle, svsnick?
            self.getSvsnickedOn.emit(oldnick, newnick)

        # etc.
        oldhandle = oldnick[0 : oldnick.find("!")]
        if self.mainwindow.profile().handle in [newnick, oldhandle]:
            self.myHandleChanged.emit(newnick)
        newchum = PesterProfile(newnick, chumdb=self.mainwindow.chumdb)
        self.moodUpdated.emit(oldhandle, Mood("offline"))
        self.userPresentUpdate.emit(f"{oldhandle}:{newnick}", "", "nick")
        if newnick in self.mainwindow.chumList.chums:
            self.getMood(newchum)
        if oldhandle == self.mainwindow.randhandler.randNick:
            self.mainwindow.randhandler.setRunning(False)
        elif newnick == self.mainwindow.randhandler.randNick:
            self.mainwindow.randhandler.setRunning(True)

    def welcome(self, _server, _nick, _msg):
        """Numeric reply 001 RPL_WELCOME, send when we've connected to the server."""
        self.registeredIRC = True  # Registered as in, the server has accepted our nick & user.
        self.connected.emit()  # Alert main thread that we've connected.
        profile = self.mainwindow.profile()
        if not self.mainwindow.config.lowBandwidth():
            # Negotiate capabilities
            self.send_irc.cap("REQ", "message-tags")
            self.send_irc.cap(
                self, "REQ", "draft/metadata-notify-2"
            )  # <--- Not required in the unreal5 module implementation
            self.send_irc.cap(
                self, "REQ", "pesterchum-tag"
            )  # <--- Currently not using this
            self.send_irc.join("#pesterchum")
            # Moods via metadata
            self.send_irc.metadata("*", "sub", "mood")
            self.send_irc.metadata("*", "set", "mood", str(profile.mood.value))
            # Color via metadata
            self.send_irc.metadata("*", "sub", "color")
            self.send_irc.metadata("*", "set", "color", profile.color.name())
            # Backwards compatible moods
            self.send_irc.privmsg("#pesterchum", f"MOOD >{profile.mymood}")

    def featurelist(self, _target, _handle, *params):
        """Numerical reply 005 RPL_ISUPPORT to communicate supported server features.

        Not in the original specification.
        Metadata support could be confirmed via CAP ACK/CAP NEK.
        """
        features = params[:-1]
        PchumLog.info("Server featurelist: %s", features)
        for feature in features:
            if feature.casefold().startswith("metadata"):
                PchumLog.info("Server supports metadata.")
                self.metadata_supported = True

    def cap(self, server, nick, subcommand, tag):
        """IRCv3 capabilities command from server.

        See: https://ircv3.net/specs/extensions/capability-negotiation
        """
        PchumLog.info("CAP %s %s %s %s", server, nick, subcommand, tag)
        # if tag == "message-tags":
        #    if subcommand == "ACK":

    def umodeis(self, _server, _handle, modes):
        """Numeric reply 221 RPL_UMODEIS, shows us our user modes."""
        self.mainwindow.modes = modes

    def liststart(self, _server, _handle, *info):
        """Numeric reply 321 RPL_LISTSTART, start of list of channels."""
        self.channel_list = []
        info = list(info)
        self.channel_field = info.index("Channel")  # dunno if this is protocol
        PchumLog.info('---> recv "CHANNELS: %s ', self.channel_field)

    def list(self, _server, _handle, *info):
        """Numeric reply 322 RPL_LIST, returns part of the list of channels."""
        channel = info[self.channel_field]
        usercount = info[1]
        if channel not in self.channel_list and channel != "#pesterchum":
            self.channel_list.append((channel, usercount))
        PchumLog.info('---> recv "CHANNELS: %s ', channel)

    def listend(self, _server, _handle, _msg):
        """Numeric reply 323 RPL_LISTEND, end of a series of LIST replies."""
        PchumLog.info('---> recv "CHANNELS END"')
        self.channelListReceived.emit(PesterList(self.channel_list))
        self.channel_list = []

    def channelmodeis(self, _server, _handle, channel, modes, _mode_params=""):
        """Numeric reply 324 RPL_CHANNELMODEIS, gives channel modes."""
        self.modesUpdated.emit(channel, modes)

    def namreply(self, _server, _nick, _op, channel, names):
        """Numeric reply 353 RPL_NAMREPLY, part of a NAMES list of members, usually of a channel."""
        namelist = names.split(" ")
        PchumLog.info('---> recv "NAMES %s: %s names"', channel, len(namelist))
        if not hasattr(self, "channelnames"):
            self.channelnames = {}
        if channel not in self.channelnames:
            self.channelnames[channel] = []
        self.channelnames[channel].extend(namelist)

    def endofnames(self, _server, _nick, channel, _msg):
        """Numeric reply 366 RPL_ENDOFNAMES, end of NAMES list of members, usually of a channel."""
        try:
            namelist = self.channelnames[channel]
        except KeyError:
            # EON seems to return with wrong capitalization sometimes?
            for channel_name in self.channelnames:
                if channel.casefold() == channel_name.casefold():
                    channel = channel_name
                    namelist = self.channelnames[channel]
        del self.channelnames[channel]
        self.namesReceived.emit(channel, PesterList(namelist))
        if channel == "#pesterchum" and not self.joined:
            self.joined = True
            self.mainwindow.randhandler.setRunning(
                self.mainwindow.randhandler.randNick in namelist
            )
            chums = self.mainwindow.chumList.chums
            lesschums = []
            for chum in chums:
                if chum.handle in namelist:
                    lesschums.append(chum)
            self.getMood(*lesschums)

    def cannotsendtochan(self, _server, _handle, channel, msg):
        """Numeric reply 404 ERR_CANNOTSENDTOCHAN, we aren't in the channel or don't have voice."""
        self.cannotSendToChan.emit(channel, msg)

    def erroneusnickname(self, *args):
        """Numeric reply 432 ERR_ERRONEUSNICKNAME, we have a forbidden or protocol-breaking nick."""
        # Server is not allowing us to connect.
        reason = "Handle is not allowed on this server.\n" + " ".join(args)
        self.stopIRC = reason.strip()
        self.disconnectIRC()

    def nicknameinuse(self, _server, _cmd, nick, _msg):
        """Numerical reply 433 ERR_NICKNAMEINUSE, raised when changing nick to nick in use."""
        self._reset_nick(nick)

    def nickcollision(self, _server, _cmd, nick, _msg):
        """Numerical reply 436 ERR_NICKCOLLISION, raised during connect when nick is in use."""
        self._reset_nick(nick)

    def _reset_nick(self, oldnick):
        """Set our nick to a random pesterClient."""
        random_number = int(
            random.random() * 9999
        )  # Random int in range 1000 <---> 9999
        newnick = f"pesterClient{random_number}"
        self.send_irc.nick(newnick)
        self.nickCollision.emit(oldnick, newnick)

    def forbiddenchannel(self, _server, handle, channel, msg):
        """Numeric reply 448 'forbiddenchannel' reply, channel is forbidden.

        Not in the specification but used by UnrealIRCd."""
        self.signal_forbiddenchannel.emit(channel, msg)
        self.userPresentUpdate.emit(handle, channel, "left")

    def inviteonlychan(self, _server, _handle, channel, _msg):
        """Numeric reply 473 ERR_INVITEONLYCHAN, can't join channel (+i)."""
        self.chanInviteOnly.emit(channel)

    def keyvalue(self, _target, _handle_us, handle_owner, key, _visibility, *value):
        """METADATA DRAFT numeric reply 761 RPL_KEYVALUE, we received the value of a key.

        The format of the METADATA server notication is:
        METADATA <Target> <Key> <Visibility> <Value>
        """
        if key == "mood":
            mood = Mood(int(value[0]))
            self.moodUpdated.emit(handle_owner, mood)

    def nomatchingkey(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 766 ERR_NOMATCHINGKEY, no matching key."""
        PchumLog.info("nomatchingkey: %s", failed_handle)
        # No point in GETMOOD-ing services
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self.send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def keynotset(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 768 ERR_KEYNOTSET, key isn't set."""
        PchumLog.info("nomatchingkey: %s", failed_handle)
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self.send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def keynopermission(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 769 ERR_KEYNOPERMISSION, no permission for key."""
        PchumLog.info("nomatchingkey: %s", failed_handle)
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self.send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def metadatasubok(self, *params):
        """ "METADATA DRAFT numeric reply 770 RPL_METADATASUBOK, we subbed to a key."""
        PchumLog.info("metadatasubok: %s", params)

    moodUpdated = QtCore.pyqtSignal("QString", Mood)
    colorUpdated = QtCore.pyqtSignal("QString", QtGui.QColor)
    messageReceived = QtCore.pyqtSignal("QString", "QString")
    memoReceived = QtCore.pyqtSignal("QString", "QString", "QString")
    noticeReceived = QtCore.pyqtSignal("QString", "QString")
    inviteReceived = QtCore.pyqtSignal("QString", "QString")
    timeCommand = QtCore.pyqtSignal("QString", "QString", "QString")
    namesReceived = QtCore.pyqtSignal("QString", PesterList)
    channelListReceived = QtCore.pyqtSignal(PesterList)
    nickCollision = QtCore.pyqtSignal("QString", "QString")
    getSvsnickedOn = QtCore.pyqtSignal("QString", "QString")
    myHandleChanged = QtCore.pyqtSignal("QString")
    chanInviteOnly = QtCore.pyqtSignal("QString")
    modesUpdated = QtCore.pyqtSignal("QString", "QString")
    connected = QtCore.pyqtSignal()
    askToConnect = QtCore.pyqtSignal(Exception)
    userPresentUpdate = QtCore.pyqtSignal("QString", "QString", "QString")
    cannotSendToChan = QtCore.pyqtSignal("QString", "QString")
    quirkDisable = QtCore.pyqtSignal("QString", "QString", "QString")
    signal_forbiddenchannel = QtCore.pyqtSignal("QString", "QString")
