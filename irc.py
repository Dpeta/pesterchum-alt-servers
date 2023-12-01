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
from scripts.services import SERVICES


class PesterIRC(QtCore.QThread):
    """Class for making a thread that manages the connection to server."""

    def __init__(
        self,
        window,
        server: str,
        port: int,
        ssl: bool,
        password="",
        verify_hostname=True,
    ):
        QtCore.QThread.__init__(self)
        self.mainwindow = window

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server  # Server to connect to.
        self.port = port  # Port on server to connect to.
        self.password = password  # Optional password for PASS.
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

        # Dict for connection server commands/replies to handling functions.
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
            "902": self._sasl_skill_issue,  # ERR_NICKLOCKED, account is not available...
            "903": self._saslsuccess,  # We did a SASL!! woo yeah!! (RPL_SASLSUCCESS)
            "904": self._sasl_skill_issue,  # oh no,,, cringe,,, (ERR_SASLFAIL)
            "905": self._sasl_skill_issue,  # ERR_SASLTOOLONG, we don't split so end.
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
            "authenticate": self._authenticate,  # IRCv3 SASL authentication
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

        if self.password:
            self._send_irc.pass_(self.password)

        # Negotiate capabilities
        self._send_irc.cap("REQ", "message-tags")
        self._send_irc.cap(
            "REQ",
            "draft/metadata-notify-2",  # <--- Not required for the unreal5 module.
        )
        self._send_irc.cap("REQ", "pesterchum-tag")  # <--- Currently not using this
        self._send_irc.cap("REQ", "twitch.tv/membership")  # Twitch silly

        # This should not be here.
        profile = self.mainwindow.profile()
        # Do SASL!!
        self._send_irc.cap("REQ", "sasl")
        if self.mainwindow.userprofile.getAutoIdentify():
            # Send plain, send end later when 903 or 904 is received.
            self._send_irc.authenticate("PLAIN")
            # Always call CAP END after 5 seconds.
            self.cap_negotation_started.emit()
        else:
            # Without SASL, end caps here.
            self._send_irc.cap("END")

        # Send NICK & USER :3
        self._send_irc.nick(profile.handle)
        self._send_irc.user("pcc31", "pcc31")

    def _conn_generator(self):
        """Returns a generator object."""
        try:
            buffer = b""
            while not self._end:
                try:
                    buffer += self.socket.recv(1024)
                except OSError as socket_exception:
                    PchumLog.warning(
                        "Socket exception in conn_generator: '%s'.", socket_exception
                    )
                    if self._end:
                        break
                    raise socket_exception
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
            except OSError as exception:
                PchumLog.info(
                    "Error while shutting down socket, already broken? %s", exception
                )
            try:
                self.socket.close()
            except OSError as exception:
                PchumLog.info(
                    "Error while closing socket, already broken? %s", exception
                )

    def irc_connect(self):
        """Try to connect and signal for connect-anyway prompt on cert fail."""
        try:
            self._connect(self.verify_hostname)
        except SSLCertVerificationError as ssl_cert_fail:
            # Ask if users wants to connect anyway
            self.askToConnect.emit(ssl_cert_fail)
            raise ssl_cert_fail
        self._conn = self._conn_generator()

    def set_connection_broken(self):
        """Called when the connection is broken."""
        PchumLog.critical("set_connection_broken() got called, disconnecting.")
        self.disconnect_irc()

    def end_cap_negotiation(self):
        """Send CAP END to end capability negotation.

        Called from SASL-related functions here,
        but also from a timer on the main thread that always triggers after 5 seconds.
        """
        if not self.registered_irc:
            self._send_irc.cap("END")

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
            self._conn = self._conn_generator()
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
                except OSError as socket_exception:
                    PchumLog.warning(socket_exception)
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
        self._send_irc.metadata("*", "set", "color", color.name())
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
            self._send_irc.away("Idle")
        else:
            self._send_irc.away()

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

    @QtCore.pyqtSlot(str)
    def send_nick(self, nick: str):
        self._send_irc.nick(nick)

    @QtCore.pyqtSlot(str)
    def send_authenticate(self, msg):
        """Called from main thread via signal, send requirements."""
        self._send_irc.authenticate(msg)

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
            try:
                if QtGui.QColor.isValidColorName(value):
                    color = QtGui.QColor.fromString(value)
                else:
                    color = QtGui.QColor(0, 0, 0)
            except AttributeError:
                # PyQt5?
                color = QtGui.QColor(value)
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
        self.stop_irc = ""
        for param in params:
            if param:
                self.stop_irc += " " + param.strip()
        self.stop_irc = self.stop_irc.strip()
        self.disconnect_irc()

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

    def _kick(self, channel_operator, channel, handle, reason):
        """'KICK' message from server, someone got kicked from a channel."""
        channel_operator_nick = channel_operator[0 : channel_operator.find("!")]
        self.userPresentUpdate.emit(
            handle, channel, f"kick:{channel_operator_nick}:{reason}"
        )
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

    def _mode(self, op, channel, mode_msg, *handles):
        """'MODE' message from server, a user or a channel's mode changed.

        This and the functions it calls to in the main thread seem pretty broken,
        modes that aren't internally tracked aren't updated correctly."""

        if not handles:  # len 0
            handles = [""]

        # Channel section
        # Okay so, as I understand it channel modes will always be applied to a
        # channel even if the commands also sets a mode to a user.
        # So "MODE #channel +ro handleHandle" will set +r to channel #channel
        # as well as set +o to handleHandle.
        #
        # EXPIRIMENTAL FIX
        # No clue how stable this is,
        # but since it doesn't seem to cause a crash it's probably an improvement.
        # This might be clunky with non-unrealircd IRC servers
        channel_mode = ""
        unrealircd_channel_modes = "cCdfGHikKLlmMNnOPpQRrsSTtVzZ"
        if any(md in mode_msg for md in unrealircd_channel_modes):
            PchumLog.debug("Channel mode in string.")
            modes = list(self.mainwindow.modes)
            for md in unrealircd_channel_modes:
                if mode_msg.find(md) != -1:  # -1 means not found
                    if mode_msg[0] == "+":
                        modes.extend(md)
                        channel_mode = "+" + md
                    elif mode_msg[0] == "-":
                        try:
                            modes.remove(md)
                            channel_mode = "-" + md
                        except ValueError:
                            PchumLog.warning(
                                "Can't remove channel mode that isn't set."
                            )
                    self.userPresentUpdate.emit("", channel, f"{channel_mode}:{op}")
                    mode_msg = mode_msg.replace(md, "")
            modes.sort()
            self.mainwindow.modes = "+" + "".join(modes)

        modes = []
        cur = "+"
        for l in mode_msg:
            if l in ["+", "-"]:
                cur = l
            else:
                modes.append(f"{cur}{l}")
        for index, mode in enumerate(modes):
            # Server-set usermodes don't need to be passed.
            if not (handles == [""]) & (("x" in mode) | ("z" in mode) | ("o" in mode)):
                try:
                    self.userPresentUpdate.emit(handles[index], channel, f"{mode}:{op}")
                except IndexError as index_except:
                    PchumLog.exception("modeSetIndexError: %s", index_except)

    def _invite(self, sender, _you, channel):
        """'INVITE' message from server, someone invited us to a channel.

        Pizza party everyone invited!!!"""
        handle = sender.split("!")[0]
        self.inviteReceived.emit(handle, channel)

    def _nick(self, oldnick, newnick, _hopcount=0):
        """'NICK' message from server, signifies a nick change.

        Is send when our or someone else's nick got changed willingly or unwillingly."""
        PchumLog.debug("NICK change from '%s' to '%s'.", oldnick, newnick)
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
        # Get mood
        mood = profile.mood.value_str()
        # Moods via metadata
        self._send_irc.metadata("*", "sub", "mood")
        self._send_irc.metadata("*", "set", "mood", mood)
        # Color via metadata
        self._send_irc.metadata("*", "sub", "color")
        self._send_irc.metadata("*", "set", "color", profile.color.name())
        # Backwards compatible moods
        if self.mainwindow.config.irc_compatibility_mode():
            return
        self._send_irc.join("#pesterchum")
        self._send_irc.privmsg("#pesterchum", f"MOOD >{mood}")

    def _featurelist(self, _target, _handle, *params):
        """Numerical reply 005 RPL_ISUPPORT to communicate supported server features.

        Not in the original specification.
        Metadata support could be confirmed via CAP ACK/CAP NEK.
        """
        features = params[:-1]
        PchumLog.info("Server _featurelist: %s", features)
        if not self.metadata_supported:
            if any(feature.startswith("METADATA") for feature in features):
                PchumLog.info("Server supports metadata.")
                self.metadata_supported = True

    def _cap(self, server, nick, subcommand, tag):
        """IRCv3 capabilities command from server.

        See: https://ircv3.net/specs/extensions/capability-negotiation
        """
        PchumLog.info("CAP %s %s %s %s", server, nick, subcommand, tag)
        if subcommand.casefold() == "nak" and tag.casefold() == "sasl":
            # SASL isn't supported, end CAP negotation.
            self._send_irc.cap("END")

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
        namelist = None
        try:
            namelist = self.channelnames[channel]
        except KeyError:
            # EON seems to return with wrong capitalization sometimes?
            for channel_name in self.channelnames:
                if channel.casefold() == channel_name.casefold():
                    channel = channel_name
                    namelist = self.channelnames[channel]
        if channel in self.channelnames:
            self.channelnames.pop(channel)
        if not namelist:
            return
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
        self.disconnect_irc()

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

    def _authenticate(self, _, token):
        """Handle IRCv3 SASL authneticate command from server."""
        if token == "+":
            # Try to send password now
            self._send_irc.authenticate(
                nick=self.mainwindow.profile().handle,
                password=self.mainwindow.userprofile.getNickServPass(),
            )

    def _sasl_skill_issue(self, *_msg):
        """Handles all responses from server that indicate SASL authentication failed.

        Replies that indicate we can't authenticate include: 902, 904, 905.
        Aborts SASL by sending CAP END, ending capability negotiation."""
        self.end_cap_negotiation()

    def _saslsuccess(self, *_msg):
        """Handle 'RPL_SASLSUCCESS' reply from server, SASL authentication succeeded! woo yeah!!"""
        self.end_cap_negotiation()

    moodUpdated = QtCore.pyqtSignal(str, Mood)
    colorUpdated = QtCore.pyqtSignal(str, QtGui.QColor)
    messageReceived = QtCore.pyqtSignal(str, str)
    memoReceived = QtCore.pyqtSignal(str, str, str)
    noticeReceived = QtCore.pyqtSignal(str, str)
    inviteReceived = QtCore.pyqtSignal(str, str)
    timeCommand = QtCore.pyqtSignal(str, str, str)
    namesReceived = QtCore.pyqtSignal(str, PesterList)
    channelListReceived = QtCore.pyqtSignal(PesterList)
    nickCollision = QtCore.pyqtSignal(str, str)
    getSvsnickedOn = QtCore.pyqtSignal(str, str)
    myHandleChanged = QtCore.pyqtSignal(str)
    chanInviteOnly = QtCore.pyqtSignal(str)
    modesUpdated = QtCore.pyqtSignal(str, str)
    connected = QtCore.pyqtSignal()
    askToConnect = QtCore.pyqtSignal(Exception)
    userPresentUpdate = QtCore.pyqtSignal(str, str, str)
    cannotSendToChan = QtCore.pyqtSignal(str, str)
    signal_forbiddenchannel = QtCore.pyqtSignal(str, str)
    cap_negotation_started = QtCore.pyqtSignal()
