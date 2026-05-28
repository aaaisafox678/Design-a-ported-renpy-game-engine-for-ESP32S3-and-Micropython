#
# MicroPython stub for pygame_sdl2
# 提供 Ren'Py 需要的全部 SDL API
#

USEREVENT = 24
KEYDOWN = 2
KEYUP = 3
MOUSEMOTION = 4
MOUSEBUTTONDOWN = 5
MOUSEBUTTONUP = 6
VIDEORESIZE = 12
QUIT = 256
SRCALPHA = 0x00010000

class Surface:
    def __init__(s, size, flags=0):
        s.w, s.h = size
        s._data = bytearray(s.w * s.h * 4)
    def get_size(s): return (s.w, s.h)
    def get_width(s): return s.w
    def get_height(s): return s.h
    def fill(s, color): pass
    def blit(s, src, pos): pass
    def subsurface(s, rect): return Surface((rect[2], rect[3]))
    def copy(s): return Surface((s.w, s.h))

class Rect:
    def __init__(s, *a): s.x, s.y, s.w, s.h = (a[0],a[1],a[2],a[3]) if len(a)==4 else (0,0,0,0)

class display:
    @staticmethod
    def set_mode(size, flags=0, depth=0): return Surface(size)
    @staticmethod
    def set_caption(title): pass
    @staticmethod
    def set_icon(icon): pass
    @staticmethod
    def flip(): pass
    @staticmethod
    def update(rect=None): pass
    @staticmethod
    def get_surface(): return Surface((320, 480))

class event:
    _queue = []
    @staticmethod
    def get(): return []
    @staticmethod
    def pump(): pass
    @staticmethod
    def register(*a): pass
    @staticmethod
    def peek(): return []
    @staticmethod
    def poll(): return None
    @staticmethod
    def wait(): return None
    @staticmethod
    def get_standard_events(*a): return []
    @staticmethod
    def clear(): pass
    class Event:
        def __init__(s, type=0, **kw): s.type = type; s.__dict__.update(kw)

class image:
    @staticmethod
    def load(fn): return Surface((1, 1))
    @staticmethod
    def save(surf, fn): pass

class transform:
    @staticmethod
    def scale(surf, size): return Surface(size)
    @staticmethod
    def rotate(surf, angle): return surf
    @staticmethod
    def smoothscale(surf, size): return Surface(size)

class time:
    @staticmethod
    def get_ticks(): return 0
    @staticmethod
    def wait(ms): pass
    class Clock:
        def tick(s, fps): return 16
        def get_fps(s): return 60

class mouse:
    @staticmethod
    def get_pos(): return (0, 0)
    @staticmethod
    def set_visible(v): pass

class key:
    @staticmethod
    def get_pressed(): return []
    @staticmethod
    def get_mods(): return 0
    KMOD_SHIFT = 1
    KMOD_CTRL = 64

class font:
    class Font:
        def __init__(s, fn, size): pass
        def render(s, text, aa, color): return Surface((1, 1))

class mixer:
    @staticmethod
    def init(f=48000, s=-16, c=2): pass
    @staticmethod
    def quit(): pass
    class Sound:
        def __init__(s, f): pass
        def play(s, l=0): pass
    class music:
        @staticmethod
        def load(f): pass
        @staticmethod
        def play(l=0): pass
        @staticmethod
        def stop(): pass
        @staticmethod
        def pause(): pass
        @staticmethod
        def unpause(): pass
        @staticmethod
        def fadeout(t): pass
        @staticmethod
        def set_volume(v): pass
        @staticmethod
        def get_volume(): return 1.0
        @staticmethod
        def get_busy(): return False

class joystick:
    class Joystick:
        def __init__(s, i): pass
        def init(s): pass
        def quit(s): pass

class controller:
    class Controller:
        def __init__(s, i): pass

class draw:
    @staticmethod
    def rect(surf, color, rect, w=0): pass
    @staticmethod
    def line(surf, color, start, end, w=1): pass

class gfxdraw:
    @staticmethod
    def pixel(s, x, y, c): pass

# 常量
HWSURFACE = 1
DOUBLEBUF = 0x40000000
FULLSCREEN = 0x80000000
RESIZABLE = 0x10
APP_TERMINATING = 0x100
APP_WILLENTERBACKGROUND = 0x101
APP_DIDENTERBACKGROUND = 0x102
APP_WILLENTERFOREGROUND = 0x103
APP_DIDENTERFOREGROUND = 0x104
APP_LOWMEMORY = 0x105
WINDOWEVENT = 0x200
WINDOWEVENT_SHOWN = 1
WINDOWEVENT_HIDDEN = 2
WINDOWEVENT_EXPOSED = 3
WINDOWEVENT_MOVED = 4
WINDOWEVENT_RESIZED = 5
WINDOWEVENT_SIZE_CHANGED = 6
WINDOWEVENT_MINIMIZED = 7
WINDOWEVENT_MAXIMIZED = 8
WINDOWEVENT_RESTORED = 9
WINDOWEVENT_ENTER = 10
WINDOWEVENT_LEAVE = 11
WINDOWEVENT_FOCUS_GAINED = 12
WINDOWEVENT_FOCUS_LOST = 13
WINDOWEVENT_CLOSE = 14
WINDOWEVENT_TAKE_FOCUS = 15
WINDOWEVENT_HIT_TEST = 16
SETVIDEORESIZE = 13
SYSWMEVENT = 0x201
TEXTEDITING = 0x302
TEXTINPUT = 0x303
K_UNKNOWN = 0
CONTROLLERDEVICEADDED = 0x700
CONTROLLERDEVICEREMOVED = 0x701
CONTROLLERAXISMOTION = 0x702
CONTROLLERBUTTONDOWN = 0x703
CONTROLLERBUTTONUP = 0x704

# 初始化
def init(): pass
def quit(): pass

# ===== 万能容错: 所有缺失属性返回0 =====
import sys
_self = sys.modules[__name__]
class _SDLModule(type(sys)):
    def __getattr__(cls, name):
        if name.startswith('__'): raise AttributeError(name)
        return 0
_self.__class__ = _SDLModule