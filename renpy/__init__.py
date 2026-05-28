#!/usr/bin/env python3
#
# Micro-RenPy 7.4.11 for ESP32-S3 (JC3248W535CN)
# 
# 基于 Ren'Py 7.4.11 官方源码的 MicroPython 微缩移植
# 
# 硬件规格:
#   ESP32-S3-WROOM-1 (双核LX7 240MHz, 8MB PSRAM, 16MB Flash)
#   3.5" 320x480 QSPI TFT LCD (AXS15231B)
#   I2C 触控 (AXS15231B集成, 0x3B)
#   NS4168 I2S D类功放 (2.5W@4ohm, 8kHz-96kHz)
#   TF卡 SDIO (CMD/DAT0-3/CLK)
#
#
import sys, os, gc, time, math, random

# ===== 平台标识 =====
windows = False; macintosh = False; linux = False
android = False; ios = False; emscripten = False
mobile = True; macapp = False

# ===== 版本信息 (Ren'Py 7.4.11 "Lucky Beckoning Cat") =====
version_tuple = (7, 4, 11, 0)
version_name = "Lucky Beckoning Cat (MicroPython)"
version_only = "7.4.11.2266"
version = "Ren'Py " + version_only
script_version = 5003000
bytecode_version = 1
savegame_suffix = "-LT1.save"

# ===== Python 2/3 =====
PY2 = False; basestring = str
def bchr(x): return bytes([x])
def bord(x): return x if isinstance(x,int) else ord(x)
pystr = str

# ===== 恢复/备份系统(空) =====
class Backup: 
    def __init__(self): pass
    def restore(self): pass
backup = Backup()
session = {}; autoreload = False; safe_mode_checked = True

# ===== pickle =====
try: import pickle
except:
    class _Fake: 
        HIGHEST_PROTOCOL=2
        def dumps(s,o,p=None): return b''
        def loads(s,b): return {}
    pickle = _Fake()

# 兼容模块
_chash = {'renpy.display.text': None, 'renpy.styleclass': None, 'renpy.subprocess': None}

# === MicroPython 必须在所有 import 前注册的模块 ===
try:
    import renpy.pygame_sdl2_stub as _ps
    sys.modules['pygame_sdl2'] = _ps
    sys.modules['pygame_sdl2_stub'] = _ps
except: pass

def update_path(): pass

# ===== 日志 =====
def plog(level,even,*args): pass

# ===== 导入 ALL =====
def import_all():
    # MicroPython: 注册缺失的 CPython 模块
    import renpy.imp; sys.modules['imp'] = renpy.imp
    
    # 路径设置
    for p in ['/sdcard', '/sdcard/game', '/sdcard/micropython-renpy']:
        if p not in sys.path: sys.path.insert(0, p)
    
    i = lambda n: __import__(n, fromlist=['*'])

    # 核心层 — 按官方的 import_all 顺序
    import renpy.config
    import renpy.log
    import renpy.object
    import renpy.game
    import renpy.preferences
    import renpy.loader
    import renpy.pyanalysis
    import renpy.ast
    import renpy.atl
    import renpy.curry
    import renpy.color
    import renpy.easy
    import renpy.execution
    import renpy.loadsave
    import renpy.savelocation
    import renpy.persistent
    import renpy.parser
    import renpy.performance
    import renpy.pydict
    import renpy.python
    import renpy.script
    import renpy.statements
    import renpy.util
    import renpy.styledata
    
    import renpy.style
    _chash['renpy.styleclass'] = renpy.style
    
    import renpy.substitutions
    import renpy.translation
    
    # === display 层 ===
    import renpy.display.module
    import renpy.display.render
    import renpy.display.core
    import renpy.display.presplash
    import renpy.display.pgrender
    import renpy.display.scale
    
    import renpy.text
    import renpy.text.font
    import renpy.text.textsupport
    import renpy.text.texwrap
    import renpy.text.text
    import renpy.text.extras
    _chash['renpy.display.text'] = renpy.text.text
    
    # GL 层(空实现)
    import renpy.gl
    import renpy.gl2
    
    # display 子模块
    import renpy.display.layout
    import renpy.display.viewport
    import renpy.display.transform
    import renpy.display.motion
    import renpy.display.behavior
    import renpy.display.transition
    import renpy.display.movetransition
    import renpy.display.im
    import renpy.display.imagelike
    import renpy.display.image
    import renpy.display.video
    import renpy.display.focus
    import renpy.display.anim
    import renpy.display.particle
    import renpy.display.dragdrop
    import renpy.display.imagemap
    import renpy.display.predict
    import renpy.display.emulator
    import renpy.display.tts
    import renpy.display.gesture
    import renpy.display.model
    import renpy.display.screen
    import renpy.display.error
    
    # audio 层
    import renpy.audio
    import renpy.audio.audio
    import renpy.audio.music
    import renpy.audio.sound
    
    # UI + screen
    import renpy.ui
    import renpy.screenlang
    
    # sl2
    import renpy.sl2
    import renpy.sl2.slast
    import renpy.sl2.slparser
    import renpy.sl2.slproperties
    import renpy.sl2.sldisplayables
    
    # 工具
    import renpy.lint
    import renpy.warp
    import renpy.memory
    
    # exports + character（关键）
    import renpy.exports
    import renpy.character
    
    # GL2
    import renpy.gl2.gl2draw
    import renpy.gl2.gl2mesh
    import renpy.gl2.gl2model
    import renpy.gl2.gl2polygon
    import renpy.gl2.gl2shader
    import renpy.gl2.gl2texture
    import renpy.gl2.live2d
    
    # store
    import renpy.minstore
    import renpy.defaultstore
    import renpy.store
    
    global plog
    try: plog = renpy.performance.log
    except: pass
    
    post_import()

def post_import():
    renpy.python.create_store("store")
    renpy.store = sys.modules['store']
    renpy.exports.store = renpy.store
    sys.modules['renpy.store'] = sys.modules['store']
    
    for k,v in renpy.defaultstore.__dict__.items():
        renpy.store.__dict__.setdefault(k, v)
    renpy.store.eval = renpy.defaultstore.eval
    
    for k,v in list(globals().items()):
        vars(renpy.exports).setdefault(k, v)
    for n,m in _chash.items():
        if m: sys.modules[n] = m

# ===== 便捷 API =====
def is_init_phase(): return False
def variant(name): return name in ('small','touch','mobile')
def known_languages(): return {}
def image_exists(name): return renpy.loader.loadable(name) if 'loader' in dir(renpy) else False
def loadable(name): return os.path.exists('/sdcard/game/'+name)
def change_language(l,n): pass
def jump(label): renpy.exports.jump(label)
def call(label): renpy.exports.call(label)
def call_in_new_context(label): renpy.exports.call_in_new_context(label)
def run(action): action()
def free_memory(): gc.collect()
def random(): return random.random()
def pure(fn): return fn

# ===== 初始化 =====
try:
    import_all()
except Exception as e:
    print("renpy init: " + str(e))