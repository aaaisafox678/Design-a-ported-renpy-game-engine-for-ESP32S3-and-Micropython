#
# MicroPython shim for renpy/display/render.pyx
# 核心渲染系统 - 纯Python替代
#

import collections
import gc
import math
import time

# ===== 全局状态 =====
render_cache = collections.defaultdict(dict)
redraw_queue = []
screen_render = None
live_renders = []
frame_time = 0
per_frame = False
sizing = False
models = False

# ===== 常量 =====
DISSOLVE = 1
IMAGEDISSOLVE = 2
PIXELLATE = 3
FLATTEN = 4

IDENTITY = None  # 由 Matrix 模块设置

class Render:
    """渲染对象"""
    __slots__ = ('width', 'height', 'children', 'blits', 'mesh', 'reverse',
                 'xoffset', 'yoffset', 'clipping', 'operation', 'operation_complete',
                 'operation_parameter', 'alpha', 'over', 'properties')

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.children = []
        self.blits = []
        self.mesh = False
        self.reverse = None
        self.xoffset = 0
        self.yoffset = 0
        self.clipping = False
        self.operation = 0
        self.operation_complete = 0
        self.operation_parameter = 0
        self.alpha = 1.0
        self.over = 0
        self.properties = {}

    def blit(self, source, pos, main=False):
        self.blits.append((source, pos, main))

    def canvas(self):
        return None

    def subsurface(self, rect, focus=False):
        rv = Render(rect[2], rect[3])
        rv.xoffset = rect[0]
        rv.yoffset = rect[1]
        return rv

    def surface(self):
        return None

    def place(self, d, x=0, y=0, width=None, height=None, st=None, at=None, render=None):
        if render is None:
            render = d.render(width or self.width, height or self.height, st or 0, at or 0)
        if render is not None:
            self.children.append((x, y, render))

    def render_to_texture(self, alpha):
        return None

    def kills(self, d):
        pass

    def is_pixel_opaque(self, x, y):
        return True

    def zoom(self, xzoom, yzoom):
        pass

    def scale(self, factor):
        self.width = int(self.width * factor)
        self.height = int(self.height * factor)
        for i, (x, y, child) in enumerate(self.children):
            self.children[i] = (int(x * factor), int(y * factor), child)
        for i, (s, pos, main) in enumerate(self.blits):
            self.blits[i] = (s, (int(pos[0] * factor), int(pos[1] * factor)), main)

    def __repr__(self):
        return "<Render {}x{}>".format(self.width, self.height)


class Matrix2D:
    def __init__(self, data=None):
        if data is None:
            self.data = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        elif len(data) == 4:
            self.data = [float(data[0]), float(data[1]), 0.0, float(data[2]), float(data[3]), 0.0]
        else:
            self.data = [float(x) for x in data[:6]]

    def __mul__(self, other):
        if isinstance(other, Matrix2D):
            a = self.data
            b = other.data
            return Matrix2D([
                a[0]*b[0] + a[1]*b[3], a[0]*b[1] + a[1]*b[4], 0.0,
                a[3]*b[0] + a[4]*b[3], a[3]*b[1] + a[4]*b[4], 0.0
            ])
        return other

IDENTITY = Matrix2D([1, 0, 0, 0, 1, 0])

def adjust_render_cache_times(old_time, new_time):
    pass

def mark_sweep():
    global live_renders
    live_renders = []

def render(d, width, height, st, at):
    try:
        return d.render(width, height, st, at)
    except:
        return Render(width, height)

def check_redraws(now, draw):
    pass