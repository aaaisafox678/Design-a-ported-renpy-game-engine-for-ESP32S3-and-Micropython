# MicroPython shim: GL draw - ESP32-S3 uses framebuf instead
import framebuf
_vsync = True
_frame_times = []
class GLDraw:
    def __init__(s,nm): s.gles=True; s.did_init=False; s.window=None; s.info={"renderer":nm}
    def init(s,*a): s.did_init=True
    def quit(s): pass
    def translate(s,*a): pass
    def draw_render_textures(s,*a): pass
    def set_rtt(s,*a): pass
class Rtt: pass
def gl_version(): return "2.1"
def gl_renderer(): return "ESP32-Framebuffer"
def gl_vendor(): return "Espressif"
