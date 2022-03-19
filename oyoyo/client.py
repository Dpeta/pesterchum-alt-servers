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
_datadir = ostools.getDataDir()
logging.config.fileConfig(_datadir + "logging.ini")
PchumLog = logging.getLogger('pchumLogger')

import logging
import socket
import sys
import time
import os
import traceback
import ssl
import json
import select

from oyoyo.parse import *
from oyoyo import helpers
from oyoyo.cmdhandler import CommandError

class IRCClientError(Exception):
    pass


class IRCClient:
    """ IRC Client class. This handles one connection to a server.
    This can be used either with or without IRCApp ( see connect() docs )
    """

    def __init__(self, cmd_handler, **kwargs):
        """ the first argument should be an object with attributes/methods named 
        as the irc commands. You may subclass from one of the classes in 
        oyoyo.cmdhandler for convenience but it is not required. The 
        methods should have arguments (prefix, args). prefix is 
        normally the sender of the command. args is a list of arguments.
        Its recommened you subclass oyoyo.cmdhandler.DefaultCommandHandler, 
        this class provides defaults for callbacks that are required for 
        normal IRC operation.

        all other arguments should be keyword arguments. The most commonly
        used will be nick, host and port. You can also specify an "on connect"
        callback. ( check the source for others )

        Warning: By default this class will not block on socket operations, this 
        means if you use a plain while loop your app will consume 100% cpu.
        To enable blocking pass blocking=True. 

        >>> class My_Handler(DefaultCommandHandler):
        ...     def privmsg(self, prefix, command, args):
        ...         print "%s said %s" % (prefix, args[1])
        ...
        >>> def connect_callback(c):
        ...     helpers.join(c, '#myroom')
        ...
        >>> cli = IRCClient(My_Handler,
        ...     host="irc.freenode.net",
        ...     port=6667,
        ...     nick="myname",
        ...     connect_cb=connect_callback)
        ...
        >>> cli_con = cli.connect()
        >>> while 1:
        ...     cli_con.next()
        ...
        """

        # This should be moved to profiles
        
        with open(_datadir + "server.json", "r") as server_file:
            read_file = server_file.read()
            server_file.close()
            server_obj = json.loads(read_file)
        TLS = server_obj['TLS']
        #print("TLS-status is: " + str(TLS))
        if TLS == False:
            #print("false")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.context = ssl.create_default_context()
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE
            self.bare_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = self.context.wrap_socket(self.bare_socket)
            #self.socket.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        self.blocking = True
        self.socket.setblocking(self.blocking)
        
        self.nick = None
        self.real_name = None
        self.host = None
        self.port = None
        self.connect_cb = None
        self.timeout = None

        self.__dict__.update(kwargs)
        self.command_handler = cmd_handler(self)

        self._end = False

    def send(self, *args, **kwargs):
        """ send a message to the connected server. all arguments are joined
        with a space for convenience, for example the following are identical 
        
        >>> cli.send("JOIN %s" % some_room)
        >>> cli.send("JOIN", some_room)

        In python 2, all args must be of type str or unicode, *BUT* if they are
          unicode they will be converted to str with the encoding specified by
          the 'encoding' keyword argument (default 'utf8').
        In python 3, all args must be of type str or bytes, *BUT* if they are
          str they will be converted to bytes with the encoding specified by the
          'encoding' keyword argument (default 'utf8'). 
        """
        # Convert all args to bytes if not already
        encoding = kwargs.get('encoding') or 'utf8'
        bargs = []
        for arg in args:
            if isinstance(arg, str):
                bargs.append(bytes(arg, encoding))
            elif isinstance(arg, bytes):
                bargs.append(arg)
            elif type(arg).__name__ == 'unicode':
                bargs.append(arg.encode(encoding))
            else:
                PchumLog.warning('Refusing to send one of the args from provided: %s'% repr([(type(arg), arg) for arg in args]))
                raise IRCClientError('Refusing to send one of the args from provided: %s'
                                     % repr([(type(arg), arg) for arg in args]))

        msg = bytes(" ", "UTF-8").join(bargs)
        PchumLog.info('---> send "%s"' % msg)
        try:
            # Extra block to give a failed write another try, causes a reconnect otherwise
            retry = 0
            while retry < 5:
                try:
                    ready_to_read, ready_to_write, in_error = select.select([], [self.socket], [])
                    PchumLog.debug("ready_to_write (len %s): " % str(len(ready_to_write)) + str(ready_to_write))
                    #ready_to_write[0].sendall(msg + bytes("\r\n", "UTF-8"))
                    for x in ready_to_write:
                        x.sendall(msg + bytes("\r\n", "UTF-8"))
                    break
                except (socket.error, ValueError) as e:# "file descriptor cannot be a negative integer"
                    retry += 1
                    PchumLog.warning("socket.error (retry %s) %s" % (str(retry), str(e)))
        except socket.error as se:
            PchumLog.warning("socket.error %s" % str(se))
            try:  # a little dance of compatibility to get the errno
                errno = se.errno
            except AttributeError:
                errno = se[0]                    
            if not self.blocking and errno == 11:
                pass
            else:
                raise se

    def connect(self):
        """ initiates the connection to the server set in self.host:self.port 
        """

        PchumLog.info('connecting to %s:%s' % (self.host, self.port))
        self.socket.connect(("%s" % self.host, self.port))
        if not self.blocking:
            self.socket.setblocking(0)
        if self.timeout:
            self.socket.settimeout(self.timeout)
        helpers.nick(self, self.nick)
        helpers.user(self, self.nick, self.real_name)

        if self.connect_cb:
            self.connect_cb(self)
            
    def conn(self):
        """returns a generator object. """
        try:
            buffer = bytes()
            while not self._end:
                try:
                    ready_to_read, ready_to_write, in_error = select.select([self.socket], [], []) # Don't wanna cause an unnecessary timeout
                                                                                                        # Though this could probably be 90
                    PchumLog.debug("ready_to_read (len %s): " % len(ready_to_read) + str(ready_to_read))
                    for x in ready_to_read:
                        buffer += x.recv(1024)
                    #print("pre-recv")
                    #buffer += self.socket.recv(1024)
                    #print("post-recv")
                    #print(buffer)
                    #raise socket.timeout
                except socket.timeout as e:
                    PchumLog.warning("timeout in client.py, " + str(e))
                    if self._end:
                        break
                    raise e
                except (socket.error, ValueError) as e:
                    PchumLog.warning("conn socket.error %s in %s" % (e, self))
                    if self._end:
                        break
                    try:  # a little dance of compatibility to get the errno
                        errno = e.errno
                    except AttributeError:
                        errno = e[0]                        
                    if not self.blocking and errno == 11:
                        pass
                    else:
                        raise e
                else:
                    if self._end:
                        break
                    PchumLog.debug("pre buffer check, len(buffer) = " + str(len(buffer)))
                    if len(buffer) == 0 and self.blocking:
                        PchumLog.debug("len(buffer) = 0")
                        raise socket.error("Connection closed")

                    data = buffer.split(bytes("\n", "UTF-8"))
                    buffer = data.pop()

                    PchumLog.debug("data = " + str(data))

                    for el in data:
                        PchumLog.debug("el=%s, data=%s" % (el,data))
                        prefix, command, args = parse_raw_irc_command(el)
                        try:
                            self.command_handler.run(command, prefix, *args)
                        except CommandError as e:
                            PchumLog.debug("CommandError %s" % str(e))

                yield True
        except socket.timeout as se:
            PchumLog.debug("passing timeout")
            raise se
        except socket.error as se:
            PchumLog.debug("problem: %s" % (str(se)))
            if self.socket:
                PchumLog.info('error: closing socket')
                self.socket.close()
            raise se
        except Exception as e:
            PchumLog.debug("other exception: %s" % str(e))
            raise e
        else:
            PchumLog.debug("ending while, end is %s" % self._end)
            if self.socket: 
                PchumLog.info('finished: closing socket')
                self.socket.close()
            yield False
    def close(self):
        # with extreme prejudice
        if self.socket:
            PchumLog.info('shutdown socket')
            #print("shutdown socket")
            self._end = True
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                PchumLog.warning("Error while shutting down socket, already broken? %s" % str(e))                
            try:
                self.socket.close()
            except OSError as e:
                PchumLog.warning("Error while closing socket, already broken? %s" % str(e))   

    def quit(self, msg):
        PchumLog.info("QUIT")
        self.socket.sendall(bytes(msg + "\n", "UTF-8"))
        
class IRCApp:
    """ This class manages several IRCClient instances without the use of threads.
    (Non-threaded) Timer functionality is also included.
    """

    class _ClientDesc:
        def __init__(self, **kwargs):
            self.con = None
            self.autoreconnect = False
            self.__dict__.update(kwargs)

    def __init__(self):
        self._clients = {}
        self._timers = []
        self.running = False
        self.sleep_time = 0.5

    def addClient(self, client, autoreconnect=False):
        """ add a client object to the application. setting autoreconnect
        to true will mean the application will attempt to reconnect the client
        after every disconnect. you can also set autoreconnect to a number 
        to specify how many reconnects should happen.

        warning: if you add a client that has blocking set to true,
        timers will no longer function properly """
        PchumLog.info('added client %s (ar=%s)' % (client, autoreconnect))
        self._clients[client] = self._ClientDesc(autoreconnect=autoreconnect)

    def addTimer(self, seconds, cb):
        """ add a timed callback. accuracy is not specified, you can only
        garuntee the callback will be called after seconds has passed.
        ( the only advantage to these timers is they dont use threads )
        """
        assert callable(cb)
        PchumLog.info('added timer to call %s in %ss' % (cb, seconds))
        self._timers.append((time.time() + seconds, cb))

    def run(self):
        """ run the application. this will block until stop() is called """
        # TODO: convert this to use generators too?
        self.running = True
        while self.running:
            found_one_alive = False

            for client, clientdesc in self._clients.items():
                if clientdesc.con is None:
                    clientdesc.con = client.connect()
                
                try:
                    next(clientdesc.con)
                except Exception as e:
                    PchumLog.error('client error %s' % str(e))
                    PchumLog.error(traceback.format_exc())
                    if clientdesc.autoreconnect:
                        clientdesc.con = None 
                        if isinstance(clientdesc.autoreconnect, (int, float)):
                            clientdesc.autoreconnect -= 1
                        found_one_alive = True
                    else:
                        clientdesc.con = False 
                else:
                    found_one_alive = True
                
            if not found_one_alive:
                PchumLog.info('nothing left alive... quiting')
                self.stop() 

            now = time.time()
            timers = self._timers[:]
            self._timers = []
            for target_time, cb in timers:
                if now > target_time:
                    PchumLog.info('calling timer cb %s' % cb)
                    cb()
                else:   
                    self._timers.append((target_time, cb))

            time.sleep(self.sleep_time)

    def stop(self):
        """ stop the application """
        self.running = False




