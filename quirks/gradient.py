import re

def rainbow(text):
    """Example implementation of a gradient function,
    distributes colors over text, accounting for links and smilies.

    Add it as:
        Regexp Replace
        Regexp:         ^(.*)$
        Replace With:   rainbow(\1)
    
    To customize it:
     1. Copy this function.
     2. Replace the hex colors in 'gradient' below with your own colors.
     3. Replace 'rainbow' above and below with something more fitting :3
    
    There's lots of implementations of this that predate mine,
    see: https://paste.0xfc.de/?e60df5a155e93583#AmcgN9cRnCcBycmVMvw6KJ1YLKPXGbaSzZLbgAhoNCQD
            ^ There's more useful info here too :3c
    """
    # Values of 'gradient' can be any amount of hex/RGB colors.
    gradient = ["#ff0000",
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
                "#ff0080"]
    
    # Set base distribution of colors over text,
    # stored as list of lists.
    color_and_position = []
    for color in range(0, len(gradient)):
        ratio = len(text) / len(gradient)  # To account for text length.
        color_and_position.append(
            [gradient[color],
             round(color * ratio)])

    # Iterate through match object representing all hyperlinks in text,
    # if a color tag is going to be placed within it,
    # move its position to after the link.
    for match in re.finditer(_urlre, text):
        for cp in color_and_position:
            if ((cp[1] >= match.start())  # cp[1] is pos
                and (cp[1] <= match.end())):
                cp[1] = match.end() + 1  # Move to 1 character after link.
    for match in re.finditer(_url2re, text):
        for cp in color_and_position:
            if ((cp[1] >= match.start())
                and (cp[1] <= match.end())):
                cp[1] = match.end() + 1
    # Roughly the same thing but for smilies,
    # there's no template so they need to be checked individually.
    for smiley in smilelist:
        for match in re.finditer(smiley, text):
            for cp in color_and_position:
                if ((cp[1] >= match.start())
                    and (cp[1] <= match.end())):
                    cp[1] = match.end() + 1
    
    # Iterate through characters in text and write them to the output,
    # if a color tag should be placed, add it before the character.
    output = ''
    for char in range(0, len(text)):
        # Add color if at position.
        for cp in color_and_position:
            # cp[0] is color
            # cp[1] is pos
            if char == cp[1]:
                # Add closing bracket for previous color.
                output += "</c>"
                # Add color
                output += "<c=%s>" % cp[0]
        # Add character.
        output += text[char]
    return output
rainbow.command = "rainbow"

# These can't always be imported from their original functions,
# since those functions won't always be accessible from builds.
_urlre = re.compile(r"(?i)(?:^|(?<=\s))(?:(?:https?|ftp)://|magnet:)[^\s]+")
_url2re = re.compile(r"(?i)(?<!//)\bwww\.[^\s]+?\.")
smilelist = [':rancorous:',
             ':apple:',
             ':bathearst:',
             ':cathearst:',
             ':woeful:',
             ':sorrow:',
             ':pleasant:',
             ':blueghost:',
             ':slimer:',
             ':candycorn:',
             ':cheer:',
             ':duhjohn:',
             ':datrump:',
             ':facepalm:',
             ':bonk:',
             ':mspa:',
             ':gun:',
             ':cal:',
             ':amazedfirman:',
             ':amazed:',
             ':chummy:',
             ':cool:',
             ':smooth:',
             ':distraughtfirman',
             ':distraught:',
             ':insolent:',
             ':bemused:',
             ':3:',
             ':mystified:',
             ':pranky:',
             ':tense:',
             ':record:',
             ':squiddle:',
             ':tab:',
             ':beetip:',
             ':flipout:',
             ':befuddled:',
             ':pumpkin:',
             ':trollcool:',
             ':jadecry:',
             ':ecstatic:',
             ':relaxed:',
             ':discontent:',
             ':devious:',
             ':sleek:',
             ':detestful:',
             ':mirthful:',
             ':manipulative:',
             ':vigorous:',
             ':perky:',
             ':acceptant:',
             ':olliesouty:',
             ':billiards:',
             ':billiardslarge:',
             ':whatdidyoudo:',
             ':brocool:',
             ':trollbro:',
             ':playagame:',
             ':trollc00l:',
             ':suckers:',
             ':scorpio:',
             ':shades:',
             ':honk:']
