"""Provides functions for validating input from the server and other clients."""
# import re

# _color_rgb = re.compile(r"^\d{1,3},\d{1,3},\d{1,3}$")
# _color_hex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


def is_valid_mood(value: str):
    """Returns True if an unparsed value (str) is a valid mood index."""
    if value in [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
    ]:
        return True
    return False


def is_valid_rgb_color(value: str):
    """Returns True if an unparsed value (str) is a valid rgb color as "r,g,b".

    Yeah you could do this via re but this is faster."""
    if not isinstance(value, str):
        return False
    if 4 > len(value) > 11:
        return False
    components = value.split(",")
    if len(components) != 3:
        return False
    for component in components:
        if not component.isnumeric():
            return False
        if int(component) > 255:
            return False
    return True


"""
def is_valid_rgb_color(value: str):
    "Returns True if an unparsed value (str) is a valid rgb color."
    if re.search(_color_rgb, value):
        return True
    return False

    
def is_valid_hex_color(value: str):
    "Returns True if an unparsed value (str) is a valid hex color."
    if re.search(_color_hex, value):
        return True
    return False
"""
