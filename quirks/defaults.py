"""Default quirk functions that are always included with Pesterchum."""

import random


def upperrep(text: str):
    """Returns 'text' as uppercase."""
    return text.upper()


upperrep.command = "upper"


def lowerrep(text: str):
    """Returns 'text' as lowercase."""
    return text.lower()


lowerrep.command = "lower"


def scramblerep(text: str):
    """Returns 'text' randomly scrambled."""
    return "".join(random.sample(text, len(text)))


scramblerep.command = "scramble"


def reverserep(text: str):
    """Returns the reverse of 'text'."""
    return text[::-1]


reverserep.command = "reverse"
