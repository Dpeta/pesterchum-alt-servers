import sys
from .helpers import msg

# NickServ basic functions
_nickservfuncs = (
    'register',
    'group',
    'glist',
    'identify',
    'access',
    'drop',
    'recover',
    'release',
    'sendpass',
    'ghost',
    'alist',
    'info',
    'list',
    'logout',
    'status',
    'update'
)

# NickServ SET functions
_nickservsetfuncs = (
    'display',
    'password',
    'language',
    'url',
    'email',
    'icq',
    'greet',
    'kill',
    'secure',
    'private',
    'hide',
    'msg',
    'autoop'
)

# ChanServ basic functions
_chanservfuncs = (
    'register',
    'identify',
    'sop',
    'aop',
    'hop',
    'vop',
    'access',
    'levels',
    'akick',
    'drop',
    'sendpass',
    'ban',
    'unban',
    'clear',
    'owner',
    'deowner',
    'protect',
    'deprotect',
    'op',
    'deop',
    'halfop',
    'dehalfop',
    'voice',
    'devoice',
    'getkey',
    'invite',
    'kick',
    'list',
    'logout',
    'topic',
    'info',
    'appendtopic',
    'enforce'
)

_chanservsetfuncs = (
    'founder',
    'successor',
    'password',
    'desc',
    'url',
    'email',
    'entrymsg',
    'bantype',
    'mlock',
    'keeptopic',
    'opnotice',
    'peace',
    'private',
    'restricted',
    'secure',
    'secureops',
    'securefounder',
    'signkick',
    'topiclock',
    'xop'
)

def _addServ(serv, funcs, prefix=""):
    def simplecmd(cmd_name):
        if prefix:
            cmd_name = prefix.upper() + " " + cmd_name
        def f(cli, *args):
            print(cmd_name, " ".join(args))
            #cli.send(cmd_name, serv.name, *args)
        return f
    for t in funcs:
        setattr(serv, t, simplecmd(t.upper()))

class NickServ(object):
    def __init__(self, nick="NickServ"):
        self.name = nick
        _addServ(self, _nickservfuncs)
        _addServ(self, _nickservsetfuncs, "set")

class ChanServ(object):
    def __init__(self, nick="ChanServ"):
        self.name = nick
        _addServ(self, _chanservfuncs)
        _addServ(self, _chanservsetfuncs, "set")
