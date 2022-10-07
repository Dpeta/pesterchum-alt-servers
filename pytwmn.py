import os
import socket


class TwmnError(Exception):
    UNWN_ERR = -1
    NO_TWMND = -2
    NO_CONF = -3

    def __init__(self, code):
        self.code = code

    def __str__(self):
        if self.code == TwmnError.NO_TWMND:
            return "Unable to connect to twmnd"
        elif self.code == TwmnError.NO_CONF:
            return "Could not find twmn configuration file"
        else:
            return "Unknown twmn error"


def confExists():
    try:
        from xdg import BaseDirectory

        return os.path.join(BaseDirectory.xdg_config_home, "twmn/twmn.conf")
    except:
        return False


def init(host="127.0.0.1", port=None):
    if not port:
        port = 9797
        try:
            fn = confExists()
            if not fn:
                return False
            with open(fn) as f:
                for line in f.readlines():
                    if line.startswith("port=") and line[5:-1].isdigit():
                        port = int(line[5:-1])
                        break
        except IOError:
            raise TwmnError(TwmnError.NO_CONF)
    if type(port) == type(str()):
        port = int(port)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))


class Notification(object):
    def __init__(self, title="", msg="", icon=""):
        self.title = str(title)
        self.msg = str(msg)
        if icon.startswith("file://"):
            icon = icon[7:]
        self.icon = icon
        self.time = None

    def set_duration(self, time):
        self.time = time

    def show(self):
        try:
            if self.time is None:
                s.send(
                    "<root><title>" + self.title + "</title>"
                    "<content>" + self.msg + "</content>"
                    "<icon>" + self.icon + "</icon></root>"
                )
            else:
                s.send(
                    "<root><title>" + self.title + "</title>"
                    "<content>" + self.msg + "</content>"
                    "<icon>" + self.icon + "</icon>"
                    "<duration>" + str(self.time) + "</duration></root>"
                )
        except:
            raise TwmnError(TwmnError.NO_TWMND)


if __name__ == "__main__":
    init()
    n = Notification("PyTwmn", "This is a notification!")
    n.set_duration(1000)
    n.show()
