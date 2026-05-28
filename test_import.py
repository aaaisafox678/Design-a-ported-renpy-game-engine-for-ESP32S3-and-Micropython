#!/usr/bin/env python3
"""模拟 MicroPython 环境测试 Ren'Py 导入链"""
import sys,os
sys.path.insert(0,'.')

# 欺骗: pygame_sdl2 stub
import renpy.pygame_sdl2_stub as ps
sys.modules['pygame_sdl2']=ps
sys.modules['pygame_sdl2_stub']=ps

# 欺骗: machine (MicroPython)
class FakeMachine:
    class Pin: pass
    class I2S:
        def __init__(*a,**k): pass
        def write(*a): pass
        def deinit(*a): pass
    class SDCard: pass
sys.modules['machine']=FakeMachine()

import time
print("=== Ren'Py 导入链测试 ===")
t0=time.time()

try:
    import renpy
    print(f"[OK] renpy import ({time.time()-t0:.1f}s)")
    print(f"     version: {renpy.version_only}")
    print(f"     screen: {renpy.config.screen_width}x{renpy.config.screen_height}")
    
    print(f"  renpy.config OK")
    print(f"  renpy.character OK" if hasattr(renpy,'character') else "  MISS character")
    
    print("\n[OK] 导入链基本通畅")
except Exception as e:
    print(f"\n[FAIL] {e}")
    import traceback
    traceback.print_exc()