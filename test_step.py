#!/usr/bin/env python3
"""逐步调试导入"""
import sys,os
sys.path.insert(0,'.')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')

try:
    import renpy.compat
    print('[1] compat OK')
except Exception as e:
    print(f'[1] compat FAIL: {e}')

try:
    import renpy.config
    print('[2] config OK')
except Exception as e:
    print(f'[2] config FAIL: {e}')
    import traceback; traceback.print_exc()

try:
    import renpy.log
    print('[3] log OK')
except Exception as e:
    print(f'[3] log FAIL: {e}')

try:
    import renpy.object
    print('[4] object OK')
except Exception as e:
    print(f'[4] object FAIL: {e}')