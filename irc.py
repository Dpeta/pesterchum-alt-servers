"""Provides classes and functions for communicating with an IRC server.

References for the IRC protocol:
 - Original IRC protocol specification: https://www.rfc-editor.org/rfc/rfc1459
 - Updated IRC Client specification: https://www.rfc-editor.org/rfc/rfc2812
 - Modern IRC client protocol writeup: https://modern.ircdocs.horse
 - IRCv3 protocol additions: https://ircv3.net/irc/
 - Draft of metadata spec: https://gist.github.com/k4bek4be/92c2937cefd49990fbebd001faf2b237

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
import socket
import random
import logging
from ssl import SSLCertVerificationError

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
from scripts.input_validation import is_valid_mood, is_valid_rgb_color

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

    def __init__(self, window, server: str, port: int, ssl: bool, verify_hostname=True):
        QtCore.QThread.__init__(self)
        self.mainwindow = window

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server  # Server to connect to.
        self.port = port  # Port on server to connect to.
        self.ssl = ssl  # Whether to connect over SSL/TLS.
        self.verify_hostname = (
            verify_hostname  # Whether to verify server hostname. (SSL-only)
        )

        self._send_irc = SendIRC()

        self.unresponsive = False
        self.registered_irc = False
        self.metadata_supported = False
        self.stop_irc = None
        self._conn = None
        self._end = False  # Set to True when ending connection.
        self.joined = False
        self.channelnames = {}
        self.channel_list = []
        self.channel_field = None

        self.commands = {
            "001": self._welcome,
            "005": self._featurelist,
            "221": self._umodeis,
            "321": self._liststart,
            "322": self._list,
            "323": self._listend,
            "324": self._channelmodeis,
            "353": self._namreply,
            "366": self._endofnames,
            "432": self._erroneusnickname,
            "433": self._nicknameinuse,
            "436": self._nickcollision,
            "448": self._forbiddenchannel,  # non-standard
            "473": self._inviteonlychan,
            "761": self._keyvalue,  # 7XX is ircv3 deprecated metadata spec
            "766": self._nomatchingkey,
            "768": self._keynotset,
            "769": self._keynopermission,
            "770": self._metadatasubok,
            "error": self._error,
            "join": self._join,
            "kick": self._kick,
            "mode": self._mode,
            "part": self._part,
            "ping": self._ping,
            "privmsg": self._privmsg,
            "notice": self._notice,
            "quit": self._quit,
            "invite": self._invite,
            "nick": self._nick,  # We can get svsnicked
            "metadata": self._metadata,  # Metadata specification
            "tagmsg": self._tagmsg,  # IRCv3 message tags extension
            "cap": self._cap,  # IRCv3 Client Capability Negotiation
        }

    def run(self):
        """Implements the main loop for the thread.

        This function reimplements QThread::run() and is ran after self.irc.start()
        is called on the main thread. Returning from this method ends the thread."""
        try:
            self.irc_connect()
        except OSError as socket_exception:
            self.stop_irc = socket_exception
            return
        while True:
            res = True
            try:
                PchumLog.debug("update_irc()")
                self.mainwindow.sincerecv = 0
                res = self.update_irc()
            except socket.timeout as timeout:
                PchumLog.debug("timeout in thread %s", self)
                self._close()
                self.stop_irc = f"{type(timeout)}, {timeout}"
                return
            except (OSError, IndexError, ValueError) as exception:
                self.stop_irc = f"{type(exception)}, {exception}"
                PchumLog.debug("Socket error, exiting thread.")
                return
            else:
                if not res:
                    PchumLog.debug("False Yield: %s, returning", res)
                    return

    def _connect(self, verify_hostname=True):
        """Initiates the connection to the server set in self.server:self.port
        self.ssl decides whether the connection uses ssl.

        Certificate validation when using SSL/TLS may be disabled by
        passing the 'verify_hostname' parameter. The user is asked if they
        want to disable it if this functions raises a certificate validation error,
        in which case the function may be called again with 'verify_hostname'."""
        PchumLog.info("Connecting to %s:%s", self.server, self.port)

        # Open connection
        plaintext_socket = socket.create_connection((self.server, self.port))

        if self.ssl:
            # Upgrade connection to use SSL/TLS if enabled
            context = get_ssl_context()
            context.check_hostname = verify_hostname
            self.socket = context.wrap_socket(
                plaintext_socket, server_hostname=self.server
            )
        else:
            # SSL/TLS is disabled, connection is plaintext
            self.socket = plaintext_socket

        self.socket.settimeout(90)
        self._send_irc.socket = self.socket

        self._send_irc.nick(self.mainwindow.profile().handle)
        self._send_irc.user("pcc31", "pcc31")

    def _conn_generator(self):
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
                                self._run_command(command, prefix, tags, *args)
                            else:
                                self._run_command(command, prefix, *args)
                yield True
        except OSError as socket_exception:
            PchumLog.warning(
                "OSError raised in _conn, closing socket. (%s)", socket_exception
            )
            self._close()
            raise socket_exception
        except Exception as exception:
            PchumLog.exception("Non-socket exception in _conn.")
            raise exception
        else:
            PchumLog.debug("Ending _conn while loop, end is %s.", self._end)
            self._close()
            yield False

    def _run_command(self, command, *args):
        """Finds and runs a command if it has a matching function in the self.commands dict."""
        PchumLog.debug("_run_command %s(%s)", command, args)
        if command in self.commands:
            command_function = self.commands[command]
        else:
            PchumLog.debug("No matching function for command: %s(%s)", command, args)
            return
        try:
            command_function(*args)
        except TypeError:
            PchumLog.exception(
                "Failed to pass command, did the server pass an unsupported paramater?"
            )
        except Exception:
            PchumLog.exception("Exception while parsing command.")

    def _close(self):
        """Kill the socket 'with extreme prejudice'."""
        if self.socket:
            PchumLog.info("_close() was called, shutting down socket.")
            self._end = True
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                PchumLog.info("Error while shutting down socket, already broken? %s", e)
            try:
                self.socket.close()
            except OSError as e:
                PchumLog.info("Error while closing socket, already broken? %s", e)

    def irc_connect(self):
        """Try to connect and signal for connect-anyway prompt on cert fail."""
        try:
            self._connect(self.verify_hostname)
        except SSLCertVerificationError as e:
            # Ask if users wants to connect anyway
            self.askToConnect.emit(e)
            raise e
        self._conn = self._conn_generator()

    def set_connection_broken(self):
        """Called when the connection is broken."""
        PchumLog.critical("set_connection_broken() got called, disconnecting.")
        self.disconnectIRC()

    @QtCore.pyqtSlot()
    def update_irc(self):
        """Get a silly scrunkler from the generator!!"""
        try:
            res = next(self._conn)
        except socket.timeout as socket_exception:
            if self.registered_irc:
                return True
            raise socket_exception
        except StopIteration:
            self._conn = self.conn_generator()
            return True
        else:
            return res

    @QtCore.pyqtSlot(PesterProfile)
    def get_mood(self, *chums):
        """Get mood via metadata if supported"""

        # Get via metadata or via legacy method
        if self.metadata_supported:
            # Metadata
            for chum in chums:
                try:
                    self._send_irc.metadata(chum.handle, "get", "mood")
                except OSError as e:
                    PchumLog.warning(e)
                    self.set_connection_broken()
        else:
            # Legacy
            PchumLog.warning(
                "Server doesn't seem to support metadata, using legacy GETMOOD."
            )
            chumglub = "GETMOOD "
            for chum in chums:
                if len(chumglub + chum.handle) >= 350:
                    try:
                        self._send_irc.privmsg("#pesterchum", chumglub)
                    except OSError as e:
                        PchumLog.warning(e)
                        self.set_connection_broken()
                    chumglub = "GETMOOD "
                # No point in GETMOOD-ing services
                if chum.handle.casefold() not in SERVICES:
                    chumglub += chum.handle
            if chumglub != "GETMOOD ":
                try:
                    self._send_irc.privmsg("#pesterchum", chumglub)
                except OSError as e:
                    PchumLog.warning(e)
                    self.set_connection_broken()

    @QtCore.pyqtSlot(PesterList)
    def get_moods(self, chums):
        """Get mood, slot is called from main thread."""
        self.get_mood(*chums)

    @QtCore.pyqtSlot(str, str)
    def send_notice(self, text, handle):
        """Send notice, slot is called from main thread."""
        self._send_irc.notice(handle, text)

    @QtCore.pyqtSlot(str, str)
    def send_message(self, text, handle):
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
                return [a]
            return l

        textl = splittext(textl)
        for t in textl:
            self._send_irc.privmsg(handle, t)

    @QtCore.pyqtSlot(str, str)
    def send_ctcp(self, handle, text):
        """Send CTCP message, slot is called from main thread."""
        self._send_irc.ctcp(handle, text)

    @QtCore.pyqtSlot(str, bool)
    def start_convo(self, handle, initiated):
        """Send convo begin message and color, slot is called from main thread."""
        self._send_irc.privmsg(handle, f"COLOR >{self.mainwindow.profile().colorcmd()}")
        if initiated:
            self._send_irc.privmsg(handle, "PESTERCHUM:BEGIN")

    @QtCore.pyqtSlot(str)
    def end_convo(self, handle):
        """Send convo cease message, slot is called from main thread."""
        self._send_irc.privmsg(handle, "PESTERCHUM:CEASE")

    @QtCore.pyqtSlot()
    def update_profile(self):
        """....update profile? this shouldn't be a thing."""
        self._send_irc.nick(self.mainwindow.profile().handle)
        self.mainwindow.closeConversations(True)
        self.mainwindow.doAutoIdentify()
        self.mainwindow.autoJoinDone = False
        self.mainwindow.doAutoJoins()
        self.updateMood()

    @QtCore.pyqtSlot()
    def update_mood(self):
        """Update and send mood, slot is called from main thread."""
        mood = self.mainwindow.profile().mood.value_str()
        # Moods via metadata
        self._send_irc.metadata("*", "set", "mood", mood)
        # Backwards compatibility
        self._send_irc.privmsg("#pesterchum", f"MOOD >{mood}")

    @QtCore.pyqtSlot()
    def update_color(self):
        """Update and send color, slot is called from main thread."""
        # Update color metadata field
        color = self.mainwindow.profile().color
        self._send_irc.metadata("*", "set", "color", str(color.name()))
        # Send color messages
        for convo in list(self.mainwindow.convos.keys()):
            self._send_irc.privmsg(
                convo,
                f"COLOR >{self.mainwindow.profile().colorcmd()}",
            )

    @QtCore.pyqtSlot(str)
    def blocked_chum(self, handle):
        """Send block message, slot is called from main thread."""
        self._send_irc.privmsg(handle, "PESTERCHUM:BLOCK")

    @QtCore.pyqtSlot(str)
    def unblocked_chum(self, handle):
        """Send unblock message, slot is called from main thread."""
        self._send_irc.privmsg(handle, "PESTERCHUM:UNBLOCK")

    @QtCore.pyqtSlot(str)
    def request_names(self, channel):
        """Send NAMES to request channel members, slot is called from main thread."""
        self._send_irc.names(channel)

    @QtCore.pyqtSlot()
    def request_channel_list(self):
        """Send LIST to request list of channels, slot is called from main thread."""
        self._send_irc.list()

    @QtCore.pyqtSlot(str)
    def join_channel(self, channel):
        """Send JOIN and MODE to join channel and get modes, slot is called from main thread."""
        self._send_irc.join(channel)
        self._send_irc.mode(channel)

    @QtCore.pyqtSlot(str)
    def left_channel(self, channel):
        """Send PART to leave channel, slot is called from main thread."""
        self._send_irc.part(channel)

    @QtCore.pyqtSlot(str, str, str)
    def kick_user(self, channel, user, reason=""):
        """Send KICK message to kick user from channel, slot is called from main thread."""
        self._send_irc.kick(channel, user, reason)

    @QtCore.pyqtSlot(str, str, str)
    def set_channel_mode(self, channel, mode, command):
        """Send MODE to set channel mode, slot is called from main thread."""
        self._send_irc.mode(channel, mode, command)

    @QtCore.pyqtSlot(str)
    def channel_names(self, channel):
        """Send block message, slot is called from main thread."""
        self._send_irc.names(channel)

    @QtCore.pyqtSlot(str, str)
    def invite_chum(self, handle, channel):
        """Send INVITE message to invite someone to a channel, slot is called from main thread."""
        self._send_irc.invite(handle, channel)

    @QtCore.pyqtSlot()
    def ping_server(self):
        """Send PING to server to verify connectivity, slot is called from main thread."""
        self._send_irc.ping("B33")

    @QtCore.pyqtSlot(bool)
    def set_away(self, away=True):
        """Send AWAY to update away status, slot is called from main thread."""
        if away:
            self.away("Idle")
        else:
            self.away()

    @QtCore.pyqtSlot(str, str)
    def kill_some_quirks(self, channel, handle):
        """Send NOQUIRKS ctcp message, disables quirks. Slot is called from main thread."""
        self._send_irc.ctcp(channel, "NOQUIRKS", handle)

    @QtCore.pyqtSlot()
    def disconnect_irc(self):
        """Send QUIT and close connection, slot is called from main thread."""
        self._send_irc.quit(f"{_pcVersion} <3")
        self._end = True
        self._close()

    def _notice(self, nick, chan, msg):
        """Standard IRC 'NOTICE' message, primarily used for automated replies from services."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "NOTICE %s :%s"', handle, msg)
        if (
            handle == "ChanServ"
            and chan == self.mainwindow.profile().handle
            and msg[0:2] == "[#"
        ):
            self.memoReceived.emit(msg[1 : msg.index("]")], handle, msg)
        else:
            self.noticeReceived.emit(handle, msg)

    def _metadata(self, _target, nick, key, _visibility, value):
        """METADATA DRAFT metadata message from server.

        The format of the METADATA server notication is:
        METADATA <Target> <Key> <Visibility> <Value>
        """
        if key.casefold() == "mood":
            if is_valid_mood(value[0]):
                mood = Mood(int(value[0]))
            else:
                PchumLog.warning(
                    "Mood index '%s' from '%s' is not valid.", value[0], nick
                )
                mood = Mood(0)
            self.moodUpdated.emit(nick, mood)
        elif key.casefold() == "color":
            if QtGui.QColor.isValidColorName(value):
                color = QtGui.QColor.fromString(value)
            else:
                color = QtGui.QColor(0, 0, 0)
            self.colorUpdated.emit(nick, color)

    def _tagmsg(self, prefix, tags, *args):
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
                    self._privmsg(prefix, args[0], msg)
                elif value.startswith("COLOR>"):
                    # Process like it's a COLOR >0,0,0 PRIVMSG
                    msg = value.replace(">", " >")
                    self._privmsg(prefix, args[0], msg)
                elif value.startswith("TIME>"):
                    # Process like it's a PESTERCHUM:TIME> PRIVMSG
                    msg = "PESTERCHUM:" + value
                    self._privmsg(prefix, args[0], msg)
                else:
                    # Invalid syntax
                    PchumLog.warning("TAGMSG with invalid syntax.")

    def _ping(self, _prefix, token):
        """'PING' command from server, we respond with PONG and a matching token."""
        self._send_irc.pong(token)

    def _error(self, *params):
        """'ERROR' message from server, the server is terminating our connection."""
        self.stop_irc = " ".join(params).strip()
        self.disconnectIRC()

    def __ctcp(self, nick: str, chan: str, msg: str):
        """Client-to-client protocol handling.

        Called by _privmsg. CTCP messages are PRIVMSG messages wrapped in '\x01' characters.
        """
        msg = msg.strip("\x01")  # We already know this is a CTCP message.
        handle = nick[0 : nick.find("!")]
        # ACTION, IRC /me (The CTCP kind)
        if msg.startswith("ACTION "):
            self._privmsg(nick, chan, f"/me {msg[7:]}")
        # VERSION, return version.
        elif msg.startswith("VERSION"):
            self._send_irc.ctcp_reply(handle, "VERSION", f"Pesterchum {_pcVersion}")
        # CLIENTINFO, return supported CTCP commands.
        elif msg.startswith("CLIENTINFO"):
            self._send_irc.ctcp_reply(
                handle,
                "CLIENTINFO",
                "ACTION VERSION CLIENTINFO PING SOURCE NOQUIRKS",
            )
        # PING, return pong.
        elif msg.startswith("PING"):
            self._send_irc.ctcp_reply(handle, "PING", msg[4:])
        # SOURCE, return source code link.
        elif msg.startswith("SOURCE"):
            self._send_irc.ctcp_reply(
                handle,
                "SOURCE",
                "https://github.com/Dpeta/pesterchum-alt-servers",
            )
        # ???
        else:
            PchumLog.warning("Unknown CTCP command '%s' from %s to %s", msg, nick, chan)

    def _privmsg(self, nick: str, chan: str, msg: str):
        """'PRIVMSG' message from server, the standard message."""
        if not msg:  # Length 0
            return
        handle = nick[0 : nick.find("!")]
        chan = (
            chan.lower()
        )  # Channel capitalization not guarenteed, casefold() too aggressive.

        # CTCP, indicated by a message wrapped in '\x01' characters.
        # Only checking for the first character is recommended by the protocol.
        if msg[0] == "\x01":
            self.__ctcp(nick, chan, msg)
            return

        if chan.startswith("#"):
            # PRIVMSG to chnnale
            if chan == "#pesterchum":
                # follow instructions
                if msg.startswith("MOOD >"):
                    if is_valid_mood(msg[6:]):
                        mood = Mood(int(msg[6:]))
                    else:
                        PchumLog.warning(
                            "Mood index '%s' from '%s' is not valid.", msg[6:], handle
                        )
                        mood = Mood(0)
                    self.moodUpdated.emit(handle, mood)
                elif msg.startswith("GETMOOD"):
                    mychumhandle = self.mainwindow.profile().handle
                    if mychumhandle in msg:
                        mymood = self.mainwindow.profile().mood.value_str()
                        self._send_irc.privmsg("#pesterchum", f"MOOD >{mymood}")
            else:
                if msg.startswith("PESTERCHUM:TIME>"):
                    self.timeCommand.emit(chan, handle, msg[16:])
                else:
                    self.memoReceived.emit(chan, handle, msg)
        else:
            # Direct person-to-person PRIVMSG messages
            if msg.startswith("COLOR >"):
                if is_valid_rgb_color(msg[7:]):
                    colors = msg[7:].split(",")
                    colors = [int(d) for d in colors]
                    color = QtGui.QColor(*colors)
                elif QtGui.QColor.isValidColorName(msg[7:]):
                    color = QtGui.QColor.fromString(msg[7:])
                else:
                    color = QtGui.QColor(0, 0, 0)
                self.colorUpdated.emit(handle, color)
            else:
                self.messageReceived.emit(handle, msg)

    def _quit(self, nick, reason):
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

    def _kick(self, opnick, channel, handle, reason):
        """'KICK' message from server, someone got kicked from a channel."""
        op = opnick[0 : opnick.find("!")]
        self.userPresentUpdate.emit(handle, channel, f"kick:{op}:{reason}")
        # ok i shouldnt be overloading that but am lazy

    def _part(self, nick, channel, _reason="nanchos"):
        """'PART' message from server, someone left a channel."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "PART %s: %s"', handle, channel)
        self.userPresentUpdate.emit(handle, channel, "left")
        if channel == "#pesterchum":
            self.moodUpdated.emit(handle, Mood("offline"))

    def _join(self, nick, channel):
        """'JOIN' message from server, someone joined a channel."""
        handle = nick[0 : nick.find("!")]
        PchumLog.info('---> recv "JOIN %s: %s"', handle, channel)
        self.userPresentUpdate.emit(handle, channel, "join")
        if channel == "#pesterchum":
            if handle == self.mainwindow.randhandler.randNick:
                self.mainwindow.randhandler.setRunning(True)
            self.moodUpdated.emit(handle, Mood("chummy"))

    def _mode(self, op, channel, mode, *handles):
        """'MODE' message from server, a user or a channel's mode changed.

        This and the functions it calls to in the main thread seem pretty broken,
        modes that aren't internally tracked aren't updated correctly."""

        if len(handles) <= 0:
            handles = [""]
        opnick = op[0 : op.find("!")]
        PchumLog.debug("opnick=" + opnick)

        self.modesUpdated.emit(channel, mode)

        # Channel section
        # Okay so, as I understand it channel modes will always be applied to a channel even if the commands also sets a mode to a user.
        # So "MODE #channel +ro handleHandle" will set +r to channel #channel as well as set +o to handleHandle
        # Therefore the bellow method causes a crash if both user and channel mode are being set in one command.

        # if op == channel or channel == self.parent.mainwindow.profile().handle:
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
        unrealircd_channel_modes = "cCdfGHikKLlmMNnOPpQRrsSTtVzZ"
        if any(md in mode for md in unrealircd_channel_modes):
            PchumLog.debug("Channel mode in string.")
            modes = list(self.mainwindow.modes)
            for md in unrealircd_channel_modes:
                if mode.find(md) != -1:  # -1 means not found
                    PchumLog.debug("md=" + md)
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
                    self.userPresentUpdate.emit(
                        "", channel, channel_mode + ":%s" % (op)
                    )
                    PchumLog.debug("pre-mode=" + str(mode))
                    mode = mode.replace(md, "")
                    PchumLog.debug("post-mode=" + str(mode))
            modes.sort()
            self.mainwindow.modes = "+" + "".join(modes)

        modes = []
        cur = "+"
        for l in mode:
            if l in ["+", "-"]:
                cur = l
            else:
                modes.append("{}{}".format(cur, l))
        for i, m in enumerate(modes):
            # Server-set usermodes don't need to be passed.
            if (handles == [""]) & (("x" in m) | ("z" in m) | ("o" in m)) != True:
                try:
                    self.userPresentUpdate.emit(handles[i], channel, m + ":%s" % (op))
                except IndexError as e:
                    PchumLog.exception("modeSetIndexError: %s" % e)
            # print("i = " + i)
            # print("m = " + m)
            # self.parent.userPresentUpdate.emit(handles[i], channel, m+":%s" % (op))
            # self.parent.userPresentUpdate.emit(handles[i], channel, m+":%s" % (op))
            # Passing an empty handle here might cause a crash.
            # except IndexError:
            # self.parent.userPresentUpdate.emit("", channel, m+":%s" % (op))

    def _invite(self, sender, _you, channel):
        """'INVITE' message from server, someone invited us to a channel.

        Pizza party everyone invited!!!"""
        handle = sender.split("!")[0]
        self.inviteReceived.emit(handle, channel)

    def _nick(self, oldnick, newnick, _hopcount=0):
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
            self.get_mood(newchum)
        if oldhandle == self.mainwindow.randhandler.randNick:
            self.mainwindow.randhandler.setRunning(False)
        elif newnick == self.mainwindow.randhandler.randNick:
            self.mainwindow.randhandler.setRunning(True)

    def _welcome(self, _server, _nick, _msg):
        """Numeric reply 001 RPL_WELCOME, send when we've connected to the server."""
        self.registered_irc = (
            True  # Registered as in, the server has accepted our nick & user.
        )
        self.connected.emit()  # Alert main thread that we've connected.
        profile = self.mainwindow.profile()
        if not self.mainwindow.config.lowBandwidth():
            # Negotiate capabilities
            self._send_irc.cap("REQ", "message-tags")
            self._send_irc.cap(
                "REQ", "draft/metadata-notify-2"
            )  # <--- Not required in the unreal5 module implementation
            self._send_irc.cap("REQ", "pesterchum-tag")  # <--- Currently not using this
            self._send_irc.join("#pesterchum")
            # Get mood
            mood = profile.mood.value_str()
            # Moods via metadata
            self._send_irc.metadata("*", "sub", "mood")
            self._send_irc.metadata("*", "set", "mood", mood)
            # Color via metadata
            self._send_irc.metadata("*", "sub", "color")
            self._send_irc.metadata("*", "set", "color", profile.color.name())
            # Backwards compatible moods
            self._send_irc.privmsg("#pesterchum", f"MOOD >{mood}")

    def _featurelist(self, _target, _handle, *params):
        """Numerical reply 005 RPL_ISUPPORT to communicate supported server features.

        Not in the original specification.
        Metadata support could be confirmed via CAP ACK/CAP NEK.
        """
        features = params[:-1]
        PchumLog.info("Server _featurelist: %s", features)
        for feature in features:
            if feature.casefold().startswith("metadata"):
                PchumLog.info("Server supports metadata.")
                self.metadata_supported = True

    def _cap(self, server, nick, subcommand, tag):
        """IRCv3 capabilities command from server.

        See: https://ircv3.net/specs/extensions/capability-negotiation
        """
        PchumLog.info("CAP %s %s %s %s", server, nick, subcommand, tag)
        # if tag == "message-tags":
        #    if subcommand == "ACK":

    def _umodeis(self, _server, _handle, modes):
        """Numeric reply 221 RPL_UMODEIS, shows us our user modes."""
        self.mainwindow.modes = modes

    def _liststart(self, _server, _handle, *info):
        """Numeric reply 321 RPL_LISTSTART, start of list of channels."""
        self.channel_list = []
        info = list(info)
        self.channel_field = info.index("Channel")  # dunno if this is protocol
        PchumLog.info('---> recv "CHANNELS: %s ', self.channel_field)

    def _list(self, _server, _handle, *info):
        """Numeric reply 322 RPL_LIST, returns part of the list of channels."""
        channel = info[self.channel_field]
        usercount = info[1]
        if channel not in self.channel_list and channel != "#pesterchum":
            self.channel_list.append((channel, usercount))
        PchumLog.info('---> recv "CHANNELS: %s ', channel)

    def _listend(self, _server, _handle, _msg):
        """Numeric reply 323 RPL_LISTEND, end of a series of LIST replies."""
        PchumLog.info('---> recv "CHANNELS END"')
        self.channelListReceived.emit(PesterList(self.channel_list))
        self.channel_list = []

    def _channelmodeis(self, _server, _handle, channel, modes, _mode_params=""):
        """Numeric reply 324 RPL_CHANNELMODEIS, gives channel modes."""
        PchumLog.debug("324 RPL_CHANNELMODEIS %s: %s", channel, modes)
        self.modesUpdated.emit(channel, modes)

    def _namreply(self, _server, _nick, _op, channel, names):
        """Numeric reply 353 RPL_NAMREPLY, part of a NAMES list of members, usually of a channel."""
        namelist = names.split(" ")
        PchumLog.info('---> recv "NAMES %s: %s names"', channel, len(namelist))
        if not hasattr(self, "channelnames"):
            self.channelnames = {}
        if channel not in self.channelnames:
            self.channelnames[channel] = []
        self.channelnames[channel].extend(namelist)

    def _endofnames(self, _server, _nick, channel, _msg):
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
            self.get_mood(*lesschums)

    def _cannotsendtochan(self, _server, _handle, channel, msg):
        """Numeric reply 404 ERR_CANNOTSENDTOCHAN, we aren't in the channel or don't have voice."""
        self.cannotSendToChan.emit(channel, msg)

    def _erroneusnickname(self, *args):
        """Numeric reply 432 ERR_ERRONEUSNICKNAME, we have a forbidden or protocol-breaking nick."""
        # Server is not allowing us to connect.
        reason = "Handle is not allowed on this server.\n" + " ".join(args)
        self.stop_irc = reason.strip()
        self.disconnectIRC()

    def _nicknameinuse(self, _server, _cmd, nick, _msg):
        """Numerical reply 433 ERR_NICKNAMEINUSE, raised when changing nick to nick in use."""
        self._reset_nick(nick)

    def _nickcollision(self, _server, _cmd, nick, _msg):
        """Numerical reply 436 ERR_NICKCOLLISION, raised during connect when nick is in use."""
        self._reset_nick(nick)

    def _reset_nick(self, oldnick):
        """Set our nick to a random pesterClient."""
        random_number = int(random.random() * 9999)  # Random int in range 0 <---> 9999
        newnick = f"pesterClient{random_number}"
        self._send_irc.nick(newnick)
        self.nickCollision.emit(oldnick, newnick)

    def _forbiddenchannel(self, _server, handle, channel, msg):
        """Numeric reply 448 'forbiddenchannel' reply, channel is forbidden.

        Not in the specification but used by UnrealIRCd."""
        self.signal_forbiddenchannel.emit(channel, msg)
        self.userPresentUpdate.emit(handle, channel, "left")

    def _inviteonlychan(self, _server, _handle, channel, _msg):
        """Numeric reply 473 ERR_INVITEONLYCHAN, can't join channel (+i)."""
        self.chanInviteOnly.emit(channel)

    def _keyvalue(self, _target, _handle_us, handle_owner, key, _visibility, *value):
        """METADATA DRAFT numeric reply 761 RPL_KEYVALUE, we received the value of a key.

        The format of the METADATA server notication is:
        METADATA <Target> <Key> <Visibility> <Value>
        """
        if key.casefold() == "mood":
            if is_valid_mood(value[0]):
                mood = Mood(int(value[0]))
            else:
                PchumLog.warning(
                    "Mood index '%s' from '%s' is not valid.", value[0], handle_owner
                )
                mood = Mood(0)
            self.moodUpdated.emit(handle_owner, mood)

    def _nomatchingkey(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 766 ERR_NOMATCHINGKEY, no matching key."""
        PchumLog.info("_nomatchingkey: %s", failed_handle)
        # No point in GETMOOD-ing services
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self._send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def _keynotset(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 768 ERR_KEYNOTSET, key isn't set."""
        PchumLog.info("_keynotset: %s", failed_handle)
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self._send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def _keynopermission(self, _target, _our_handle, failed_handle, _key, *_error):
        """METADATA DRAFT numeric reply 769 ERR_KEYNOPERMISSION, no permission for key."""
        PchumLog.info("_keynopermission: %s", failed_handle)
        # Fallback to the normal GETMOOD method if getting mood via metadata fails.
        if failed_handle.casefold() not in SERVICES:
            self._send_irc.privmsg("#pesterchum", f"GETMOOD {failed_handle}")

    def _metadatasubok(self, *params):
        """ "METADATA DRAFT numeric reply 770 RPL_METADATASUBOK, we subbed to a key."""
        PchumLog.info("_metadatasubok: %s", params)

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
    signal_forbiddenchannel = QtCore.pyqtSignal("QString", "QString")
