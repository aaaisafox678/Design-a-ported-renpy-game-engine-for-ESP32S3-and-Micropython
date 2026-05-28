# MicroPython shim for renpy/text/textsupport.pyx
# 提供 Glyph, Line, tokenize, SPLIT_* 常量等

SPLIT_NONE = 0
SPLIT_INSTEAD = 1
SPLIT_BEFORE = 2
RUBY_TOP = 1
RUBY_ALT = 2

TEXT = 1
TAG = 2
PARAGRAPH = 3
DISPLAYABLE = 4

class Glyph:
    __slots__ = ('character','time','variation','split','delta_x_offset',
                 'advance','width','ascent','descent')
    def __init__(self):
        self.character = ''
        self.time = 0.0
        self.variation = 0
        self.split = SPLIT_NONE
        self.delta_x_offset = 0
        self.advance = 0
        self.width = 0
        self.ascent = 0
        self.descent = 0
    def __repr__(self):
        return "<Glyph {0!r}>".format(self.character)

class Line:
    __slots__ = ('y','height','glyphs','eop')
    def __init__(self, y, height, glyphs):
        self.y = y
        self.height = height
        self.glyphs = glyphs
        self.eop = False
    def __repr__(self):
        return "<Line y={0}, height={1}>".format(self.y, self.height)

MAX_WIDTH = 8192

def tokenize(s):
    rv = []
    buf = ''
    state = 1  # TEXT_STATE
    for c in s:
        if state == 1:  # TEXT
            if c == '\n':
                if buf:
                    rv.append((TEXT, buf))
                rv.append((PARAGRAPH, ''))
                buf = ''
                continue
            elif c == '{':
                state = 2  # LEFT_BRACE
                continue
            else:
                buf += c
                continue
        elif state == 2:  # LEFT_BRACE
            if c == '{':
                buf += c
                state = 1
                continue
            else:
                if buf:
                    rv.append((TEXT, buf))
                buf = c
                state = 3  # TAG
                continue
        elif state == 3:  # TAG
            if c == '}':
                rv.append((TAG, buf))
                buf = ''
                state = 1
                continue
            else:
                buf += c
                continue
    if buf:
        rv.append((TEXT, buf))
    return rv