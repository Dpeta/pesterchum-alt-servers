"""This file contains an example of a gradient quirk function."""

import re
import itertools


def rainbow(text):
    """Example implementation of a gradient function,
    distributes colors over text, accounting for links,
    #memos, @handles, smilies.

    Add it as:
        Regexp Replace
        Regexp:         ^(.*)$
        Replace With:   rainbow(\1)

    To customize it:
     1. Copy this function.
     2. Replace the hex colors in 'gradient' below with your own colors.
     3. Replace 'rainbow' above and below with something more fitting :3

    You shouldn't enable the 'exclude links and smilies' option, this function
    already does that!

    There's lots of implementations of this that predate mine,
    see: https://paste.0xfc.de/?e60df5a155e93583#AmcgN9cRnCcBycmVMvw6KJ1YLKPXGbaSzZLbgAhoNCQD
            ^ There's more useful info here too :3c
    """
    # Values of 'gradient' can be any amount of hex/RGB colors.
    gradient = [
        "#ff0000",
        "#ff8000",
        "#ffff00",
        "#80ff00",
        "#00ff00",
        "#00ff80",
        "#00ffff",
        "#0080ff",
        "#0000ff",
        "#8000ff",
        "#ff00ff",
        "#ff0080",
    ]

    # Set base distribution of colors over text,
    # stored as list of lists.
    colors_and_positions = []
    for color_pos, color in enumerate(gradient):
        ratio = len(text) / len(gradient)  # To account for text length.
        colors_and_positions.append([color, round(color_pos * ratio)])

    # Iterate through match objects representing all links/smilies in text,
    # if a color tag is going to be placed within it,
    # move its position to after the link/smilies/thingy.
    match_chain = itertools.chain(
        re.finditer(_urlre, text),
        re.finditer(_smilere, text),
        re.finditer(_memore, text),
        re.finditer(_handlere, text),
        re.finditer(_alternian_begin, text),
        re.finditer(_alternian_end, text),
    )
    for match in match_chain:
        for color_and_position in colors_and_positions:
            # color_and_position[1] is pos
            if (
                color_and_position[1] >= match.start()
                and color_and_position[1] <= match.end()
            ):
                # Move to 1 character after link.
                color_and_position[1] = match.end() + 1

    # Iterate through characters in text and write them to the output,
    # if a color tag should be placed, add it before the character.
    output = ""
    for char_pos, char in enumerate(text):
        # Add color if at position.
        for color_and_position in colors_and_positions:
            # color_and_position[0] is color
            # color_and_position[1] is pos
            if char_pos == color_and_position[1]:
                # Add closing bracket for previous color.
                output += "</c>"
                # Add color
                output += f"<c={color_and_position[0]}>"
        # Add character.
        output += char
    return output


rainbow.command = "rainbow"

# These can't always be imported from their original functions,
# since those functions won't always be accessible from builds.

# List of smilies.
smiledict = {
    ":rancorous:": "pc_rancorous.png",
    ":apple:": "apple.png",
    ":bathearst:": "bathearst.png",
    ":cathearst:": "cathearst.png",
    ":woeful:": "pc_bemused.png",
    ":sorrow:": "blacktear.png",
    ":pleasant:": "pc_pleasant.png",
    ":blueghost:": "blueslimer.gif",
    ":slimer:": "slimer.gif",
    ":candycorn:": "candycorn.png",
    ":cheer:": "cheer.gif",
    ":duhjohn:": "confusedjohn.gif",
    ":datrump:": "datrump.png",
    ":facepalm:": "facepalm.png",
    ":bonk:": "headbonk.gif",
    ":mspa:": "mspa_face.png",
    ":gun:": "mspa_reader.gif",
    ":cal:": "lilcal.png",
    ":amazedfirman:": "pc_amazedfirman.png",
    ":amazed:": "pc_amazed.png",
    ":chummy:": "pc_chummy.png",
    ":cool:": "pccool.png",
    ":smooth:": "pccool.png",
    ":distraughtfirman:": "pc_distraughtfirman.png",
    ":distraught:": "pc_distraught.png",
    ":insolent:": "pc_insolent.png",
    ":bemused:": "pc_bemused.png",
    ":3:": "pckitty.png",
    ":mystified:": "pc_mystified.png",
    ":pranky:": "pc_pranky.png",
    ":tense:": "pc_tense.png",
    ":record:": "record.gif",
    ":squiddle:": "squiddle.gif",
    ":tab:": "tab.gif",
    ":beetip:": "theprofessor.png",
    ":flipout:": "weasel.gif",
    ":befuddled:": "what.png",
    ":pumpkin:": "whatpumpkin.png",
    ":trollcool:": "trollcool.png",
    ":jadecry:": "jadespritehead.gif",
    ":ecstatic:": "ecstatic.png",
    ":relaxed:": "relaxed.png",
    ":discontent:": "discontent.png",
    ":devious:": "devious.png",
    ":sleek:": "sleek.png",
    ":detestful:": "detestful.png",
    ":mirthful:": "mirthful.png",
    ":manipulative:": "manipulative.png",
    ":vigorous:": "vigorous.png",
    ":perky:": "perky.png",
    ":acceptant:": "acceptant.png",
    ":olliesouty:": "olliesouty.gif",
    ":billiards:": "poolballS.gif",
    ":billiardslarge:": "poolballL.gif",
    ":whatdidyoudo:": "whatdidyoudo.gif",
    ":brocool:": "pcstrider.png",
    ":trollbro:": "trollbro.png",
    ":playagame:": "saw.gif",
    ":trollc00l:": "trollc00l.gif",
    ":suckers:": "Suckers.gif",
    ":scorpio:": "scorpio.gif",
    ":shades:": "shades.png",
    ":honk:": "honk.png",
}
# Regular expression templates for detecting links/smilies.
_smilere = re.compile("|".join(list(smiledict.keys())))
_urlre = re.compile(r"(?i)(?:^|(?<=\s))(?:(?:https?|ftp)://|magnet:)[^\s]+")
_memore = re.compile(r"(\s|^)(#[A-Za-z0-9_]+)")
_handlere = re.compile(r"(\s|^)(@[A-Za-z0-9_]+)")
_alternian_begin = re.compile(r"<alt>")  # Matches get set to alternian font
_alternian_end = re.compile(r"</alt>")
