#
# test_env_shim.py — CPython 测试环境shim
# 模拟 MicroPython 的 display.py / framebuf / machine / esp_panel
# 让 CPython 也能完整运行 main.py + Ren'Py 引擎
#
import struct, os, sys
from PIL import Image

# ==== 模拟 machine ====
class _Pin:
    def __init__(self, num, mode=None): pass
class _I2S:
    def __init__(self, *a, **k): pass
    def write(self, data): pass
    def deinit(self): pass
class _SDCard:
    def __init__(self, *a, **k): self._mountpoint = '/tmp/sdcard'
sys.modules['machine'] = type(sys)('machine')
sys.modules['machine'].Pin = _Pin
sys.modules['machine'].I2S = _I2S
sys.modules['machine'].SDCard = _SDCard

# ==== 模拟 framebuf ====
class FrameBuffer:
    def __init__(self, buf, w, h, fmt=None):
        self.buf = buf
        self.width = w
        self.height = h
        self.fill_color = 0
    def fill(self, color):
        self.fill_color = color
    def pixel(self, x, y, color): pass
    def line(self, x1, y1, x2, y2, color): pass
    def rect(self, x, y, w, h, color, fill=False): pass
    def text(self, s, x, y, color=0xFFFF): pass
    def blit(self, fbuf, x, y): pass
    def scroll(self, dx, dy): pass
sys.modules['framebuf'] = type(sys)('framebuf')
sys.modules['framebuf'].FrameBuffer = FrameBuffer
sys.modules['framebuf'].RGB565 = True

# ==== 模拟 display.py (yaconsult 固件) ====
class RGB565Buffer:
    BLACK=0x0000;WHITE=0xFFFF;RED=0xF800;GREEN=0x07E0;BLUE=0x001F
    YELLOW=0xFFE0;CYAN=0x07FF;MAGENTA=0xF81F
    def __init__(self, w, h):
        self.width=w;self.height=h
        self._buf=bytearray(w*h*2)  # RGB565 raw
        for i in range(0,len(self._buf),2):
            self._buf[i]=0x00;self._buf[i+1]=0x00  # black
    def fill(self, color):
        hi=(color>>8)&0xFF;lo=color&0xFF
        for i in range(0,len(self._buf),2):
            self._buf[i]=hi;self._buf[i+1]=lo
    def pixel(self,x,y,color):
        if 0<=x<self.width and 0<=y<self.height:
            i=(y*self.width+x)*2
            self._buf[i]=(color>>8)&0xFF;self._buf[i+1]=color&0xFF
    def text(self,s,x,y,c): pass
    def line(self,*a): pass
    def rect(self,*a): pass
    def flush(self, board):
        """写截图"""
        img=Image.new('RGB',(self.width,self.height))
        px=img.load()
        for y in range(self.height):
            for x in range(self.width):
                i=(y*self.width+x)*2
                val=(self._buf[i+1]<<8)|self._buf[i]
                r=(val>>11)&0x1F;g=(val>>5)&0x3F;b=val&0x1F
                px[x,y]=(r<<3,g<<2,b<<3)
        img.save('/sdcard/CBRenpy/test_screenshot.png')
        print('[SCREENSHOT] saved')
    def flush_region(self, board, x, y, w, h):
        self.flush(board)

class Backlight:
    def __init__(self, pin=1): self._b=0
    def set(self, p): self._b=p
    def on(self): self._b=100
    def off(self): self._b=0

class Board:
    def __init__(self): pass
    def init(self): return True
    def begin(self): return True
    def get_width(self): return 480
    def get_height(self): return 320
    def read_touch(self): return []  # 无触控
    def draw_bitmap(self, x, y, w, h, buf): pass

sys.modules['esp_panel'] = type(sys)('esp_panel')
sys.modules['esp_panel'].Board = Board

class Display:
    BLACK=0x0000;WHITE=0xFFFF;RED=0xF800;GREEN=0x07E0;BLUE=0x001F
    YELLOW=0xFFE0;CYAN=0x07FF;MAGENTA=0xF81F
    def __init__(self, brightness=80):
        self._board=Board();self._board.init();self._board.begin()
        self.width=480;self.height=320
        self.backlight=Backlight();self.backlight.set(brightness)
        self.fb=RGB565Buffer(self.width,self.height)
    def fill(self, color): self.fb.fill(color); self.fb.flush(self._board)
    def show(self): self.fb.flush(self._board)
    def touch(self): return self._board.read_touch()
    def color(self,r,g,b): return ((r>>3)<<11)|((g>>2)<<5)|(b>>3)

# ==== 模拟 writer / fonts ====
class CWriter:
    def __init__(self, fb, font, verbose=False): self.fb=fb;self.font=font
    @staticmethod
    def set_textpos(fb, row, col): pass
    def setcolor(self, fg, bg): pass
    def printstring(self, s): pass

class Font:
    def __init__(self): pass

sys.modules['writer'] = type(sys)('writer')
sys.modules['writer'].CWriter = CWriter
sys.modules['writer'].Writer = CWriter
sys.modules['fonts'] = type(sys)('fonts')
sys.modules['fonts.sans16'] = Font()
sys.modules['fonts.sans24'] = Font()

sys.modules['display'] = type(sys)('display')
sys.modules['display'].Display = Display
sys.modules['display'].CWriter = CWriter