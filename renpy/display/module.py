"""MicroPython shim: renpy/display/module.py"""
def save_png(surf, fp, compression=3): pass
def load_png(fp): return None
def read_image(fp): return None
def set_title(title): pass
def get_info(): return {"renderer":"framebuf","resizable":False}
