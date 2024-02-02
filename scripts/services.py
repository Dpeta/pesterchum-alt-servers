"""Lists, dicts, and functions related to services."""

from randomer import RANDNICK

# List of all common services bots. (for .casefold() matching)
# Services packages that provide the bot are in the same-line comments.
SERVICES = [
    "nickserv",  # Anope/Atheme/X3/DalekIRC
    "chanserv",  # Anope/Atheme/X3/DalekIRC
    "memoserv",  # Anope/Atheme
    "operserv",  # Anope/Atheme/DalekIRC
    "helpserv",  # Anope/Atheme/X3
    "hostserv",  # Anope/Atheme
    "botserv",  # Anope/Atheme/DalekIRC
    "global",  # Anope/Atheme/DalekIRC
    "alis",  # Atheme
    "chanfix",  # Atheme
    "gameserv",  # Atheme
    "groupserv",  # Atheme
    "infoserv",  # Atheme
    "statserv",  # Atheme
    "userserv",  # Atheme
    "authserv",  # X3
    "opserv",  # X3
    "metaserv",  # DalekIRC
    "bbserv",  # DalekIRC
]
# Pesterchum bots
CUSTOMBOTS = ["calsprite", RANDNICK.casefold()]
# All bots
BOTNAMES = SERVICES + CUSTOMBOTS

# Hardcoded messages that NickServ sends and what to display to the user instead
nickserv_messages = {
    "Your nick isn't registered.": "",  # display the same
    "Password accepted - you are now recognized.": "",  # display the same
    "If you do not change within one minute, I will change your nick.": "You have 1 minute to identify.",
    "If you do not change within 20 seconds, I will change your nick.": "You have 20 seconds to identify.",
}


def translate_nickserv_msg(msg):
    if msg in nickserv_messages:
        if not nickserv_messages[msg]:  # == "":
            return msg
        return nickserv_messages[msg]
    return None
