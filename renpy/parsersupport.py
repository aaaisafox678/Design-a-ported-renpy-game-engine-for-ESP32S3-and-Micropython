# MicroPython shim for renpy/parsersupport.pyx
def match_logical_word(s, pos):
    """匹配逻辑词边界"""
    if pos >= len(s):
        return ('', False, pos)
    c = s[pos]
    start = pos
    len_s = len(s)
    if c == ' ':
        pos += 1
        while pos < len_s and s[pos] == ' ':
            pos += 1
    elif ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9') or (c == '_'):
        pos += 1
        while pos < len_s:
            nc = s[pos]
            if ('a' <= nc <= 'z') or ('A' <= nc <= 'Z') or ('0' <= nc <= '9') or (nc == '_'):
                pos += 1
            else:
                break
    else:
        pos += 1
    word = s[start:pos]
    magic = len(word) >= 3 and word[:2] == '__'
    return word, magic, pos