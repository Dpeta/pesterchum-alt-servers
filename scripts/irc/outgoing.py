"""Class and functions for sending outgoing IRC commands."""
import logging

log = logging.getLogger("pchumLogger")


class SendIRC:
    """Provides functions for outgoing IRC commands."""

    def __init__(self):
        self.socket = None  # INET socket connected with server.

    def send(self, *args: str, text=None):
        """Send a command to the IRC server.

        Takes either a string or a list of strings.
        The 'text' argument is for the final parameter, which can have spaces."""
        # Return if disconnected
        if not self.socket or self.socket.fileno() == -1:
            log.error(
                "Send attempted while disconnected, args: %s, text: %s.", args, text
            )
            return

        command = ""
        # Convert command arguments to a single string if passed.
        if args:
            command += " ".join(args)
        # If text is passed, add ':' to imply everything after it is one parameter.
        if text:
            command += f" :{text}"
        # Add characters for end of line in IRC.
        command += "\r\n"
        # UTF-8 is the prefered encoding in 2023.
        outgoing_bytes = command.encode(encoding="utf-8", errors="replace")

        try:
            log.debug("Sending: %s", command)
            self.socket.send(outgoing_bytes)
        except OSError:
            log.exception("Error while sending: '%s'", command.strip())
            self.socket.close()

    def ping(self, token):
        """Send PING command to server to check for connectivity."""
        self.send("PING", text=token)

    def pong(self, token):
        """Send PONG command to reply to server PING."""
        self.send("PONG", token)

    def nick(self, nick):
        """Send USER command to communicate nick to server."""
        self.send("NICK", nick)

    def user(self, username, realname):
        """Send USER command to communicate username and realname to server."""
        self.send("USER", username, "0", "*", text=realname)

    def privmsg(self, target, text):
        """Send PRIVMSG command to send a message."""
        for line in text.split("\n"):
            self.send("PRIVMSG", target, text=line)

    def names(self, channel):
        """Send NAMES command to view channel members."""
        self.send("NAMES", channel)

    def kick(self, channel, user, reason=""):
        """Send KICK command to force user from channel."""
        if reason:
            self.send(f"KICK {channel} {user}", text=reason)
        else:
            self.send(f"KICK {channel} {user}")

    def mode(self, target, modestring="", mode_arguments=""):
        """Set or remove modes from target."""
        outgoing_mode = " ".join([target, modestring, mode_arguments]).strip()
        self.send("MODE", outgoing_mode)

    def ctcp(self, target, command, msg=""):
        """Send Client-to-Client Protocol message."""
        outgoing_ctcp = " ".join(
            [command, msg]
        ).strip()  # Extra spaces break protocol, so strip.
        self.privmsg(target, f"\x01{outgoing_ctcp}\x01")

    def metadata(self, target, subcommand, *params):
        """Send Metadata command to get or set metadata.

        See IRC metadata draft specification:
        https://gist.github.com/k4bek4be/92c2937cefd49990fbebd001faf2b237
        """
        self.send("METADATA", target, subcommand, *params)

    def cap(self, subcommand, *params):
        """Send IRCv3 CAP command for capability negotiation.

        See: https://ircv3.net/specs/extensions/capability-negotiation.html"""
        self.send("CAP", subcommand, *params)

    def join(self, channel, key=""):
        """Send JOIN command to join a channel/memo.

        Keys or joining multiple channels is possible in the specification, but unused.
        """
        channel_and_key = " ".join([channel, key]).strip()
        self.send("JOIN", channel_and_key)

    def part(self, channel):
        """Send PART command to leave a channel/memo.

        Providing a reason or leaving multiple channels is possible in the specification.
        """
        self.send("PART", channel)

    def notice(self, target, text):
        """Send a NOTICE to a user or channel."""
        self.send("NOTICE", target, text=text)

    def invite(self, nick, channel):
        """Send INVITE command to invite a user to a channel."""
        self.send("INVITE", nick, channel)

    def away(self, text=None):
        """AWAY command to mark client as away or no longer away.

        No 'text' parameter means the client is no longer away."""
        if text:
            self.send("AWAY", text=text)
        else:
            self.send("AWAY")

    def list(self):
        """Send LIST command to get list of channels."""
        self.send("LIST")

    def quit(self, reason=""):
        """Send QUIT to terminate connection."""
        self.send("QUIT", text=reason)
