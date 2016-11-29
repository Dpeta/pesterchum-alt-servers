# -*- coding=UTF-8; tab-width: 4 -*-
from __future__ import division

__all__ = ["Color"]

# Copied from my old Textsub script. Please forgive the mess, and keep in mind
# that this may be phased out in the future.



from .dep.attrdict import AttrDict

import collections
import functools
import sys

# Python 3 checking
if sys.version_info[0] == 2:
    basestr = basestring
else:
    basestr = str



# A named tuple for containing CIE L*a*b* (CIELAB) information.
# NOTE TO THOSE MAINTAINING: If you don't know what that means, you're going to
# hate yourself *and* me if you try to edit this. I know I did when I wrote it.
LabTuple = collections.namedtuple("LabTuple", ['L', 'a', 'b'])
class Color(object):
    # The threshold at which to consider two colors noticeably different, even
    # if only barely
    jnd = 2.3
    # TODO: Either subclass (this is probably best) or add a .native_type; in
    # the case of the former, just make sure each type is geared towards using
    # a certain kind of color space as a starting point, e.g. RGB, XYZ, HSV,
    # CIELAB, etc...
    # TODO: color_for_name()
    # TODO: Split __init__, partly using __new__, so the former just has to do
    # conversions
    def __init__(self, *args, **kwargs):
        self.ccode = ''
        self.closest_name = self.name = None
        nargs = len(args)
        if nargs == 1:
            # Make this a little easier to type out by reducing what we need to
            # work with
            arg = args[0]
            if isinstance(arg, int):
                # Assume we were passed a raw hexadecimal value
                # Again, handle this the easy way
                arg = "#%06X" % arg
            # Using 'if' instead of 'elif' here allows us to fall through from
            # the above, which is, of course, quite useful in this situation
            if isinstance(arg, basestr):
                # If it's a string, we've probably got a hex code, but check
                # anyway just in case
                if arg.startswith('#'):
                    self.hexstr = self.sanitize_hex(arg)
                    rgb = self.hexstr_to_rgb(self.hexstr)
                    self.red, self.green, self.blue = rgb
                    ##return
                # TODO: This.
                elif (arg.startswith('\003') and len(arg) > 1
                    or len(arg) < 3 and arg.isdigit()):
                    # We have an IRC-style color code
                    arg = arg.lstrip('\003')
                    # Just in case
                    arg = arg.split(',')[0]
                    cnum = int(arg)
                    try: color = _irc_colors[cnum]
                    except LookupError:
                        raise ValueError("No color for ccode %r found" % cnum)
                    # We found a color; fall through and so on
                    arg = color
                else:
                    # Presumably we have a color name
                    name = arg.lower()
                    try: color = _svg_colors[name]
                    except LookupError:
                        raise ValueError("No color with name %r found" % name)
                    # We found a color; fall through so we make this one a copy
                    arg = color
            if isinstance(arg, Color):
                # We were passed a Color object - just duplicate it.
                # For now, we'll do things the cheap way....
                self.red, self.green, self.blue = arg.to_rgb_tuple()
                self.hexstr = arg.hexstr
                self.closest_name = arg.closest_name
                self.name = arg.name
                self.ccode = arg.ccode
        elif nargs == 3:
            # Assume we've got RGB
            # Map to abs() so we can't get messed up results due to negatives
            args = list(map(abs, args))
            self.red, self.green, self.blue = args
            # Convert for the hex code
            self.hexstr = self.rgb_to_hexstr(*args)
            ##return
        else:
            # We don't know how to handle the value we recieved....
            raise ValueError
        # Otherwise, calculate XYZ for this
        self.x, self.y, self.z = self.rgb_to_xyz(*self.to_rgb_tuple())
        # Calculate the LAB color
        self.cielab = LabTuple(*self.xyz_to_cielab(*self.to_xyz_tuple()))
        if not self.closest_name: self.closest_name = self.get_svg_name()
        if not self.ccode: self.ccode = self.get_ccode()

    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other): return not self.__eq__(other)
    def __sub__(self, other):
        if not isinstance(other, Color): raise TypeError
        return self.distance(other)

    def __hash__(self):
        ##result = map(hash, [
        ##      str(self).upper(),
        ##      self.red, self.green, self.blue
        ##  ])
        # 2012-12-08T13:34-07:00: This should improve accuracy
        result = map(hash, self.cielab)
        result = functools.reduce(lambda x, y: x ^ y, result)
        return result

        # Before the change on 2012-12-08, the above was equivalent to the old
        # code, which was this:
        ##result =  hash(str(self).upper())
        ##result ^= self.red
        ##result ^= self.green
        ##result ^= self.blue
        ##return result
    def __repr__(self):
        ##return "%s(%r)" % (type(self).__name__, str(self))
        return "%s(%r)" % (type(self).__name__,
            self.reduce_hexstr(self.hexstr))
    def __str__(self):
        ##return self.reduce_hexstr(self.hexstr)
        return self.name()

    # Builtins
    # These were yanked from Hostmask and changed around a bit
    def __getitem__(self, ind): return (self.red, self.green, self.blue)[ind]
    def __iter__(self):
        targs = (self.red, self.green, self.blue)
        for t in targs:
            yield t
        # If we got here, we're out of attributes to provide
        raise StopIteration
    ##def __len__(self):
    ##  # Acceptable so long as we're returning RGB like we currently (at TOW)
    ##  # are
    ##  return 3

    @classmethod
    def from_ccode(cls, ccode):
        if isinstance(ccode, basestr):
            # We were passed a string
            ccode = ccode.lstrip('\003')
            ccode = ccode.split(',')
            if len(ccode) < 2:
                fg = ccode[0]
                bg = None
            else:
                fg, bg = ccode
            try:
                fg = int(fg)
            except ValueError:
                # We started with a string to the effect of ",00"
                fg = -1
            try:
                bg = int(bg)
            except (ValueError, TypeError):
                # We started with a string to the effect of "00,", or it didn't
                # have a comma
                bg = -1
        else:
            fg = ccode
            bg = -1

        try:
            fg = _irc_colors[fg]
        except LookupError:
            # We had a string to the effect of ",00", or the color code
            # couldn't be found
            # TODO: Consider making a ValueError return a different value?
            fg = None
        else:
            fg = Color(fg)
        try:
            bg = _irc_colors[bg]
        except LookupError:
            # See above note.
            bg = None
        else:
            bg = Color(bg)
        ##if bg: return fg, bg
        return fg, bg

    def get_ccode(self):
        closest, cldist = None, None
        targs = _irc_colors

        for code, other in targs.items():
            dist = self - other
            ##if (not strict and dist > self.jnd) or dist == 0:
            if dist == 0:
                # We have a perfect match!
                # Just return the relevant color code right now
                return "%02d" % code
            if cldist is None or cldist > dist:
                closest, cldist = "%02d" % code, dist
        # We've found the closest matching color code; return it
        return closest

    def get_svg_name(self, strict=False):
        closest, cldist = None, None
        targs = _svg_colors

        for name, other in targs.items():
            dist = self - other
            if (not strict and dist > self.jnd) or dist == 0:
                # The difference is below the Just-Noticeable Difference
                # threshold, or we have a perfect match; consider them roughly
                # the same
                return name
            if cldist is None or cldist > dist:
                closest, cldist = name, dist
        # We've found the closest matching color name; return it
        return closest

    ##def name(self): return self.closest_name

    def distance(self, other):
        # CIELAB distance, adapted from distance() and checked vs. Wikipedia:
        # http://en.wikipedia.org/wiki/Color_difference
        slab, olab = self.to_cielab_tuple(), other.to_cielab_tuple()
        # Calculate the distance between the points for each
        dist = map(lambda p1, p2: (p2 - p1)**2, slab, olab)
        # Add the results up, and sqrt to compensate for earlier squaring
        dist = sum(dist) ** .5
        return dist

    def rgb_distance(self, other):
        # The older version of distance().
        ##r1, r2 = self.red, other.red
        ##g1, g2 = self.green, other.green
        ##b1, b2 = self.blue, other.blue
        srgb, orgb = self.to_rgb_tuple(), other.to_rgb_tuple()
        ### Subtract the RGBs from each other (i.e. r1 - r2, g1 - g2, b1 - b2)
        ##dist = map(operator.sub, srgb, orgb)
        ### Square the results from the above
        ##dist = [x**2 for x in dist]
        # Do what we WOULD have done in those two lines with a single one
        dist = map(lambda x1, x2: (x1 - x2)**2, srgb, orgb)
        # Add the results up
        dist = sum(dist)
        # Fetch the square root to compensate for the earlier squaring
        dist **= .5
        return dist

    @classmethod
    def hexstr_to_rgb(cls, hexstr):
        hexstr = cls.sanitize_hex(hexstr)
        hexstr = hexstr.lstrip('#')
        if len(hexstr) == 3:
            # NOTE: This will presently never happen, due to the way
            # sanitize_hex works.
            # We have something like '#FEF', which means '#FFEEFF'. Expand it
            # first.
            # Multiplying each element by 17 expands it. Dividing it does the
            # opposite.
            result = tuple( (int(h, 16) * 17) for h in hexstr )
        else:
            # This is ugly, but the purpose is simple and it's accomplished in
            # a single line...it just runs through the string, picking two
            # characters at a time and converting them from hex values to ints.
            result = tuple(
                    int(hexstr[i:i+2], 16) for i in range(0, len(hexstr), 2)
                    )
        return result


    @staticmethod
    def rgb_to_hexstr(red, green, blue, compress=False):
        rgb = [red, green, blue]
        rgb = map(abs, rgb)
        result = []
        for c in rgb:
            c = "%02X" % c
            # Append to our result
            result.append(c)
        if compress:
            # Try to compress this down from six characters to three.
            # Basically the same thing as reduce_hexstr. Might make it use that
            # later.
            for h in result:
                if h[0] != h[1]:
                    # We can't compress this; alas.
                    # Break out so we don't go to the 'else' segment.
                    break
            else:
                # All of our codes were doubles; compress them all down.
                result = [h[0] for h in result]
        # Join and return the result
        return '#' + ''.join(result)

    # These next two are from http://www.easyrgb.com/index.php?X=MATH
    @staticmethod
    def rgb_to_xyz(red, green, blue):
        rgb = [red, green, blue]
        for i, n in enumerate(rgb):
            n /= 255
            if n > 0.04045: n = ( ( n + 0.055 ) / 1.055 ) ** 2.4
            else: n /= 12.92
            rgb[i] = n * 100
        r, g, b = rgb
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        ##x = 0.436052025   * r + 0.385081593   * g + 0.143087414   * b
        ##y = 0.222491598   * r + 0.71688606    * g + 0.060621486   * b
        ##z = 0.013929122   * r + 0.097097002   * g + 0.71418547    * b
        return x, y, z
    @staticmethod
    def xyz_to_cielab(x, y, z):
        # Reference X, Y, and Z
        refs = [95.047, 100.000, 108.883]
        ref_x, ref_y, ref_z = refs
        ##xyz = [x / ref_x, y / ref_y, z / ref_z]
        xyz = [x, y, z]
        for i, n in enumerate(xyz):
            n /= refs[i]
            if n > 0.008856: n **= 1/3
            else:
                n *= 7.787
                n += 16/116
            xyz[i] = n
        x, y, z = xyz
        l = (y*116) - 16
        a = (x - y) * 500
        b = (y - z) * 200
        return l, a, b

    @staticmethod
    def reduce_hexstr(hexstr):
        """Attempt to reduce a six-character hexadecimal color code down to a
        four-character one."""
        orig = hexstr
        hexstr = hexstr.lstrip('#')
        strlen = len(hexstr)
        h = hexstr.upper()
        for i in range(0, strlen, 2):
            if h[i] != h[i+1]:
                # We found a match that wouldn't work; give back the old value.
                return orig
        else:
            # All of these can be reduced; do so and return.
            return '#' + hexstr[::2]


    @staticmethod
    def sanitize_hex(hexstr):
        orig = hexstr
        hexstr = hexstr.upper()
        # We don't need the leading hash mark for now
        hexstr = hexstr.lstrip('#')
        strlen = len(hexstr)
        if strlen == 6:
            # We just need to test this for validity. Fall through to the end.
            pass
        elif strlen == 3:
            # We have a short (CSS style) code; duplicate all of the characters
            hexstr = [c + c for c in hexstr]
            hexstr = ''.join(hexstr)
        else:
            raise ValueError(
                    "Invalid hexadecimal value provided: %s" % orig
                    )
        try:
            # Make sure it works/is readable (no invalid characters).
            int(hexstr, 16)
        except ValueError:
            raise ValueError(
                    "Invalid hexadecimal value provided: %s" % orig
                    )
        return '#' + hexstr

    def to_cielab_tuple(self):
        # For now, just return the stored CIELAB tuple
        return self.cielab
    def to_rgb_tuple(self): return (self.red, self.green, self.blue)
    # 2012-12-05T17:40:39-07:00: Changed 'self.blue' to 'self.z' like it SHOULD
    # have been in the FIRST place. Ugh. How did I fuck THAT one up?
    def to_xyz_tuple(self): return (self.x, self.y, self.z)

# All of these are effectively equivalent to the Qt-provided colors, so they
# could be phased out - but there's no need to, yet.
_svg_colors = AttrDict()
_irc_colors = {}
_svg_colors.update({
    "aliceblue":            Color(240, 248, 255),
    "antiquewhite":         Color(250, 235, 215),
    "aqua":                 Color(  0, 255, 255),
    "aquamarine":           Color(127, 255, 212),
    "azure":                Color(240, 255, 255),
    "beige":                Color(245, 245, 220),
    "bisque":               Color(255, 228, 196),
    "black":                Color(  0,   0,   0),
    "blanchedalmond":       Color(255, 235, 205),
    "blue":                 Color(  0,   0, 255),
    "blueviolet":           Color(138,  43, 226),
    "brown":                Color(165,  42,  42),
    "burlywood":            Color(222, 184, 135),
    "cadetblue":            Color( 95, 158, 160),
    "chartreuse":           Color(127, 255,   0),
    "chocolate":            Color(210, 105,  30),
    "coral":                Color(255, 127,  80),
    "cornflowerblue":       Color(100, 149, 237),
    "cornsilk":             Color(255, 248, 220),
    "crimson":              Color(220,  20,  60),
    "cyan":                 Color(  0, 255, 255),
    "darkblue":             Color(  0,   0, 139),
    "darkcyan":             Color(  0, 139, 139),
    "darkgoldenrod":        Color(184, 134,  11),
    "darkgray":             Color(169, 169, 169),
    "darkgreen":            Color(  0, 100,   0),
    "darkgrey":             Color(169, 169, 169),
    "darkkhaki":            Color(189, 183, 107),
    "darkmagenta":          Color(139,   0, 139),
    "darkolivegreen":       Color( 85, 107,  47),
    "darkorange":           Color(255, 140,   0),
    "darkorchid":           Color(153,  50, 204),
    "darkred":              Color(139,   0,   0),
    "darksalmon":           Color(233, 150, 122),
    "darkseagreen":         Color(143, 188, 143),
    "darkslateblue":        Color( 72,  61, 139),
    "darkslategray":        Color( 47,  79,  79),
    "darkslategrey":        Color( 47,  79,  79),
    "darkturquoise":        Color(  0, 206, 209),
    "darkviolet":           Color(148,   0, 211),
    "deeppink":             Color(255,  20, 147),
    "deepskyblue":          Color(  0, 191, 255),
    "dimgray":              Color(105, 105, 105),
    "dimgrey":              Color(105, 105, 105),
    "dodgerblue":           Color( 30, 144, 255),
    "firebrick":            Color(178,  34,  34),
    "floralwhite":          Color(255, 250, 240),
    "forestgreen":          Color( 34, 139,  34),
    "fuchsia":              Color(255,   0, 255),
    "gainsboro":            Color(220, 220, 220),
    "ghostwhite":           Color(248, 248, 255),
    "gold":                 Color(255, 215,   0),
    "goldenrod":            Color(218, 165,  32),
    "gray":                 Color(128, 128, 128),
    "grey":                 Color(128, 128, 128),
    "green":                Color(  0, 128,   0),
    "greenyellow":          Color(173, 255,  47),
    "honeydew":             Color(240, 255, 240),
    "hotpink":              Color(255, 105, 180),
    "indianred":            Color(205,  92,  92),
    "indigo":               Color( 75,   0, 130),
    "ivory":                Color(255, 255, 240),
    "khaki":                Color(240, 230, 140),
    "lavender":             Color(230, 230, 250),
    "lavenderblush":        Color(255, 240, 245),
    "lawngreen":            Color(124, 252,   0),
    "lemonchiffon":         Color(255, 250, 205),
    "lightblue":            Color(173, 216, 230),
    "lightcoral":           Color(240, 128, 128),
    "lightcyan":            Color(224, 255, 255),
    "lightgoldenrodyellow": Color(250, 250, 210),
    "lightgray":            Color(211, 211, 211),
    "lightgreen":           Color(144, 238, 144),
    "lightgrey":            Color(211, 211, 211),
    "lightpink":            Color(255, 182, 193),
    "lightsalmon":          Color(255, 160, 122),
    "lightseagreen":        Color( 32, 178, 170),
    "lightskyblue":         Color(135, 206, 250),
    "lightslategray":       Color(119, 136, 153),
    "lightslategrey":       Color(119, 136, 153),
    "lightsteelblue":       Color(176, 196, 222),
    "lightyellow":          Color(255, 255, 224),
    "lime":                 Color(  0, 255,   0),
    "limegreen":            Color( 50, 205,  50),
    "linen":                Color(250, 240, 230),
    "magenta":              Color(255,   0, 255),
    "maroon":               Color(128,   0,   0),
    "mediumaquamarine":     Color(102, 205, 170),
    "mediumblue":           Color(  0,   0, 205),
    "mediumorchid":         Color(186,  85, 211),
    "mediumpurple":         Color(147, 112, 219),
    "mediumseagreen":       Color( 60, 179, 113),
    "mediumslateblue":      Color(123, 104, 238),
    "mediumspringgreen":    Color(  0, 250, 154),
    "mediumturquoise":      Color( 72, 209, 204),
    "mediumvioletred":      Color(199,  21, 133),
    "midnightblue":         Color( 25,  25, 112),
    "mintcream":            Color(245, 255, 250),
    "mistyrose":            Color(255, 228, 225),
    "moccasin":             Color(255, 228, 181),
    "navajowhite":          Color(255, 222, 173),
    "navy":                 Color(  0,   0, 128),
    "oldlace":              Color(253, 245, 230),
    "olive":                Color(128, 128,   0),
    "olivedrab":            Color(107, 142,  35),
    "orange":               Color(255, 165,   0),
    "orangered":            Color(255,  69,   0),
    "orchid":               Color(218, 112, 214),
    "palegoldenrod":        Color(238, 232, 170),
    "palegreen":            Color(152, 251, 152),
    "paleturquoise":        Color(175, 238, 238),
    "palevioletred":        Color(219, 112, 147),
    "papayawhip":           Color(255, 239, 213),
    "peachpuff":            Color(255, 218, 185),
    "peru":                 Color(205, 133,  63),
    "pink":                 Color(255, 192, 203),
    "plum":                 Color(221, 160, 221),
    "powderblue":           Color(176, 224, 230),
    "purple":               Color(128,   0, 128),
    "red":                  Color(255,   0,   0),
    "rosybrown":            Color(188, 143, 143),
    "royalblue":            Color( 65, 105, 225),
    "saddlebrown":          Color(139,  69,  19),
    "salmon":               Color(250, 128, 114),
    "sandybrown":           Color(244, 164,  96),
    "seagreen":             Color( 46, 139,  87),
    "seashell":             Color(255, 245, 238),
    "sienna":               Color(160,  82,  45),
    "silver":               Color(192, 192, 192),
    "skyblue":              Color(135, 206, 235),
    "slateblue":            Color(106,  90, 205),
    "slategray":            Color(112, 128, 144),
    "slategrey":            Color(112, 128, 144),
    "snow":                 Color(255, 250, 250),
    "springgreen":          Color(  0, 255, 127),
    "steelblue":            Color( 70, 130, 180),
    "tan":                  Color(210, 180, 140),
    "teal":                 Color(  0, 128, 128),
    "thistle":              Color(216, 191, 216),
    "tomato":               Color(255,  99,  71),
    "turquoise":            Color( 64, 224, 208),
    "violet":               Color(238, 130, 238),
    "wheat":                Color(245, 222, 179),
    "white":                Color(255, 255, 255),
    "whitesmoke":           Color(245, 245, 245),
    "yellow":               Color(255, 255,   0),
    "yellowgreen":          Color(154, 205,  50)
    })
for k, v in _svg_colors.items():
    v.closest_name = v.name = k

# 2012-12-08T14:29-07:00: Copied over from Colors.hexstr_for_ccodes in the main
# textsub file, and subsequently modified.
_irc_colors.update({
    # These are all taken from *MY* XChat settings - they aren't guaranteed to
    # please everyone!
    0:  Color(0xFFFFFF),
    1:  Color(0x1F1F1F),
    2:  Color(0x00007F),
    3:  Color(0x007F00),
    4:  Color(0xFF0000),
    5:  Color(0x7F0000),
    6:  Color(0x9C009C),
    7:  Color(0xFC7F00),
    8:  Color(0xFFFF00),
    9:  Color(0x00FC00),
    ##10:   Color(0x009393),
    10: Color(0x008282),
    11: Color(0x00FFFF),
    12: Color(0x0000FC),
    13: Color(0xFF00FF),
    14: Color(0x7F7F7F),
    15: Color(0xD2D2D2),
    # My local colors
    16: Color(0xCCCCCC),
    ##17:   Color(0x000000),    # Commented out 'til readability checks are in
    17: Color(0x1F1F1F),
    18: Color(0x000056),
    19: Color(0x008141),
    20: Color(0xE00707),
    21: Color(0xA10000),
    22: Color(0x6A006A),
    23: Color(0xA15000),
    24: Color(0xA1A100),
    25: Color(0x416600),
    ##26:   Color(0x008282),
    26: Color(0x005682),
    27: Color(0x00D5F2),
    28: Color(0x0715CD),
    29: Color(0x99004D),
    30: Color(0x323232),
    31: Color(0x929292),

    99: Color(0x999999)         # Until I think of a better solution to this
    })
for k, v in _irc_colors.items():
    v.ccode = "%02d" % k
del k, v
