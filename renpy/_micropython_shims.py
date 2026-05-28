#
# MicroPython 适配层 - 替换所有 .pyx (Cython) 模块
# 为每个 Cython 模块提供纯 Python 等价物或空实现
#

# ===== display/render.pyx 替代 =====
class Render:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.children = []
        self.blits = []
    def blit(self, source, pos):
        self.blits.append((source, pos))
    def canvas(self):
        return None
    def subsurface(self, rect):
        return Render(rect[2], rect[3])
    def surface(self):
        return None

# ===== display/matrix.pyx 替代 =====
class Matrix:
    def __init__(self):
        self.data = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    def __mul__(self, other):
        return self

# ===== display/accelerator.pyx 替代 =====
def render_round(x):
    return int(x + 0.5) if x >= 0 else int(x - 0.5)

# ===== audio/renpysound.pyx 替代 =====
def get_sound_sample_rate():
    return 48000

# ===== gl2/*.pyx 替代 =====
class GL2Draw:
    def __init__(self): pass
    def start(self): pass
    def end(self): pass

class GL2Texture:
    def __init__(self): pass
    def bind(self): pass

class GL2Shader:
    def __init__(self): pass
    def use(self): pass

class GL2Model:
    def __init__(self): pass

class GL2Polygon:
    def __init__(self): pass

class GL2Mesh:
    def __init__(self): pass

class GL2Mesh2:
    pass

class GL2Mesh3:
    pass

# ===== pydict.pyx 替代 =====
def pydict_new():
    return {}

# ===== parsersupport.pyx 替代 =====
def parse_string(s):
    return s

# ===== style.pyx 替代 =====
class Style:
    def __init__(self, style=None):
        self.style = style
    def __getattr__(self, name):
        return None

# ===== cslots.pyx 替代 =====
# 使用普通 __slots__ 即可

# ===== tfd.pyx 替代 =====
def tfd_function():
    pass

# ===== encryption.pyx 替代 =====
def encrypt(data):
    return data

def decrypt(data):
    return data