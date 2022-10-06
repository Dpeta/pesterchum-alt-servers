# Hardcoded messages that NickServ sends and what to display to the user instead

messages = {
    "Your nick isn't registered.": "",  # display the same
    "Password accepted - you are now recognized.": "",  # display the same
    "If you do not change within one minute, I will change your nick.": "You have 1 minute to identify.",
    "If you do not change within 20 seconds, I will change your nick.": "You have 20 seconds to identify.",
}


def translate(msg):
    if msg in messages:
        if messages[msg] == "":
            return msg
        return messages[msg]
    return None
