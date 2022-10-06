import random


def upperrep(text):
    return text.upper()


upperrep.command = "upper"


def lowerrep(text):
    return text.lower()


lowerrep.command = "lower"


def scramblerep(text):
    return "".join(random.sample(text, len(text)))


scramblerep.command = "scramble"


def reverserep(text):
    return text[::-1]


reverserep.command = "reverse"
