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

import logging
import logging.config

import ostools
from oyoyo.ircevents import numeric_events

_datadir = ostools.getDataDir()
logging.config.fileConfig(_datadir + "logging.ini")
PchumLog = logging.getLogger('pchumLogger')

def parse_raw_irc_command(element):
    print(element)
    """
    This function parses a raw irc command and returns a tuple
    of (prefix, command, args).
    The following is a psuedo BNF of the input text:

    <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
    <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
    <command>  ::= <letter> { <letter> } | <number> <number> <number>
    <SPACE>    ::= ' ' { ' ' }
    <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]

    <middle>   ::= <Any *non-empty* sequence of octets not including SPACE
                   or NUL or CR or LF, the first of which may not be ':'>
    <trailing> ::= <Any, possibly *empty*, sequence of octets not including
                     NUL or CR or LF>

    <crlf>     ::= CR LF
    """
    """
    When message-tags are enabled, the message pseudo-BNF,
    as defined in RFC 1459, section 2.3.1 is extended as follows:

    <message>       ::= ['@' <tags> <SPACE>] [':' <prefix> <SPACE> ] <command> [params] <crlf>
    <tags>          ::= <tag> [';' <tag>]*
    <tag>           ::= <key> ['=' <escaped_value>]
    <key>           ::= [ <client_prefix> ] [ <vendor> '/' ] <key_name>
    <client_prefix> ::= '+'
    <key_name>      ::= <non-empty sequence of ascii letters, digits, hyphens ('-')>
    <escaped_value> ::= <sequence of zero or more utf8 characters except NUL, CR, LF, semicolon (`;`) and SPACE>
    <vendor>        ::= <host>


    """
    
    try:
        element = element.decode("utf-8")
    except UnicodeDecodeError as e:
        PchumLog.debug("utf-8 error %s" % str(e))
        element = element.decode("latin-1", 'replace')
    
    parts = element.strip().split(" ")
    if parts[0].startswith(':'):
        tags = None
        prefix = parts[0][1:]
        command = parts[1]
        args = parts[2:]
    elif parts[0].startswith('@'):
        # Message tag
        tags = parts[0]
        prefix = parts[1][1:]
        command = parts[2]
        args = parts[3:]
    else:
        tags = None
        prefix = None
        command = parts[0]
        args = parts[1:]

    if command.isdigit():
        try:
            command = numeric_events[command]
        except KeyError:
            PchumLog.info('unknown numeric event %s' % command)
    command = command.lower()

    if args[0].startswith(':'):
        args = [" ".join(args)[1:]]
    else:
        for idx, arg in enumerate(args):
            if arg.startswith(':'):
                args = args[:idx] + [" ".join(args[idx:])[1:]]
                break

    return (tags, prefix, command, args)


def parse_nick(name):
    """ parse a nickname and return a tuple of (nick, mode, user, host)

    <nick> [ '!' [<mode> = ] <user> ] [ '@' <host> ]
    """

    try:
        nick, rest = name.split('!')
    except ValueError:
        return (name, None, None, None)
    try:
        mode, rest = rest.split('=')
    except ValueError:
        mode, rest = None, rest
    try:
        user, host = rest.split('@')
    except ValueError:
        return (name, mode, rest, None)

    return (name, mode, user, host)
 
