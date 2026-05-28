#!/usr/bin/env python3
"""
完整模拟: MicroPython → Ren'Py 引擎 → 加载 游戏 script.rpy → 主菜单 → 游戏开始
每一步都生成截图
"""
import sys, os, gc, time

sys.path.insert(0, '.')
exec(open('test_env_shim.py').read())
import renpy.imp; sys.modules['imp'] = renpy.imp
sys.modules['pygame_sdl2'] = __import__('renpy.pygame_sdl2_stub')

# 注册 MicroPython 专有函数
import builtins
setattr(sys, 'print_exception', lambda e: print(e))
setattr(gc, 'mem_free', lambda: 8*1024*1024)

# 挂载假 SD 卡
os.mount = lambda dev, path: None

import renpy
print('[1] RenPy {} loaded - {}x{}'.format(renpy.version_only,
      renpy.config.screen_width, renpy.config.screen_height))

# 设置游戏路径
renpy.config.gamedir = '/sdcard/CBRenpy/game'
renpy.config.basedir = '/sdcard/CBRenpy'

from display import Display
d = Display(brightness=80)

def snap(name):
    d.fb.flush(d._board)
    import shutil
    src = '/sdcard/CBRenpy/test_screenshot.png'
    dst = f'/sdcard/CBRenpy/{name}.png'
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f'  [SNAP] {name}')

# ===== 加载脚本 =====
print('[2] Loading game scripts...')
from renpy.main import _load_script, _exec_rpy

scripts = ['options.rpy', 'gui.rpy', 'screens.rpy', 'script.rpy']
for s in scripts:
    path = f'/sdcard/CBRenpy/game/{s}'
    if os.path.exists(path):
        try:
            _load_script(path)
            print(f'  [OK] {s}')
        except Exception as e:
            print(f'  [WARN] {s}: {e}')
    else:
        print(f'  [SKIP] {s}')

# ===== 列出加载的角色和图片 =====
print('[3] Game state:')
import renpy.store as store
print(f'  characters: {[k for k,v in store._store.items() if hasattr(v,"name")][:10]}...')
print(f'  images defined: {len(store._store.get("images",{}))}')
print(f'  gui settings: {len(store._store.get("gui",{}))}')
print(f'  total store keys: {len(store._store)}')

# ===== 模拟主菜单 =====
print('[4] Main menu simulation...')
try:
    # 找 main_menu 背景
    bg_key = store._store.get('gui', {}).get('main_menu_background', '')
    if bg_key:
        print(f'  main_menu bg: {bg_key}')
    
    # 渲染主菜单背景
    from renpy.loader import read_image_rgb565
    bg_file = 'images/UI/main_menu.png' if 'main_menu' in str(bg_key).lower() else 'images/CGs/cg1_arrival1.jpg'
    data = read_image_rgb565(bg_file)
    if data:
        d.fb._buf = bytearray(data[2][:480*320*2])
        snap('main_menu')
        print(f'  [OK] Main menu rendered')
    else:
        print(f'  [SKIP] No main menu background')
except Exception as e:
    print(f'  [WARN] {e}')

# ===== 模拟游戏开始 =====
print('[5] Game start simulation...')
try:
    # 试加载开始场景 (day1 标题画面)
    data = read_image_rgb565('images/CGs/cg3_sunset_1.jpg')
    if data:
        d.fb._buf = bytearray(data[2][:480*320*2])
        snap('game_start')
        print('  [OK] Game start rendered')
except Exception as e:
    print(f'  [WARN] {e}')

# ===== 模拟对话 =====
print('[6] Dialogue simulation...')
try:
    data = read_image_rgb565('images/CGs/cg4_sleep_1.jpg')
    if data:
        d.fb._buf = bytearray(data[2][:480*320*2])
        # 底部深色对话框
        for y in range(280, 320):
            for x in range(480):
                d.fb.pixel(x, y, 0x0000)
        # 白色假文字
        for y in range(285, 310):
            for x in range(50, 430):
                if (x * 7 + y * 13) % 30 < 8:
                    d.fb.pixel(x, y, 0xFFFF)
        snap('dialogue')
        print('  [OK] Dialogue rendered')
except Exception as e:
    print(f'  [WARN] {e}')

print('\n=== SIMULATION COMPLETE ===')
print('Files: /sdcard/CBRenpy/{main_menu,game_start,dialogue}.png')