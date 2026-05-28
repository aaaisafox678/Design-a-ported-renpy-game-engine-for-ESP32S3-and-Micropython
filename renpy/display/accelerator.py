#
# MicroPython shim: accelerator.pyx → accelerator.py
#

def transform_render(self, widtho, heighto, st, at):
    from renpy.display.render import Render
    rv = Render(widtho, heighto)
    return rv

def render_round(x):
    return int(x + 0.5) if x >= 0 else int(x - 0.5)