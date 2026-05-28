# MicroPython shim: uguu/uguu.pyx → uguu.py
# OpenGL wrapper - 全空实现 (ESP32-S3无GPU)

class ptr:
    def __init__(self, o=None, ro=True): self._o = o
def get_ptr(o): return ptr(o) if isinstance(o, ptr) else ptr(o)
class Buffer:
    def __init__(self, length, itemsize, format_str, readonly=True): pass
def setup_buffer(*a): pass
def clear_missing_functions(): pass
def check_missing_functions(required): return False
def proxy_return_string(s): return s

# GL 常量
GL_RGBA = 0x1908
GL_UNSIGNED_BYTE = 0x1401
GL_TEXTURE_2D = 0x0DE1
GL_FRAMEBUFFER = 0x8D40
GL_COLOR_ATTACHMENT0 = 0x8CE0
GL_FRAMEBUFFER_BINDING = 0x8CA6
GL_MAX_TEXTURE_SIZE = 0x0D33
GL_BLEND = 0x0BE2
GL_CULL_FACE = 0x0B44
GL_DEPTH_TEST = 0x0B71
GL_SCISSOR_TEST = 0x0C11
GL_STENCIL_TEST = 0x0B90
GL_NEAREST = 0x2600
GL_LINEAR = 0x2601
GL_TEXTURE_MAG_FILTER = 0x2800
GL_TEXTURE_MIN_FILTER = 0x2801