#!/usr/bin/env python3
"""加载 游戏 主菜单背景 — 验证最终画面"""
import sys,os,shutil
sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
sys.modules['imp']=__import__('renpy.imp')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
setattr(sys,'print_exception',lambda e:print(e))
os.mount=lambda dev,path:None

from display import Display
d=Display()
GAME='/sdcard/CBRenpy/game'

def snap(name):
    d.fb.flush(d._board)
    src='/sdcard/CBRenpy/test_screenshot.png'
    dst='/sdcard/CBRenpy/'+name+'.png'
    if os.path.exists(src):
        shutil.copy(src,dst)
        print(f'  [SNAP] {name}')

# 主菜单背景
bg=os.path.join(GAME,'gui/main_menu.png')
rgb=bg.rsplit('.',1)[0]+'.rgb565'
print('主菜单 bg:',rgb,os.path.exists(rgb))

if os.path.exists(rgb):
    data=open(rgb,'rb').read()
    d.fb._buf=bytearray(data[:480*320*2])
    snap('main_menu_background')
    print('[OK] Main menu background loaded!')
else:
    print('[SKIP] main_menu.png not converted')

# 验证尺寸
from PIL import Image
img=Image.open('/sdcard/CBRenpy/main_menu_background.png')
print(f'Size: {img.size}')
print(f'Center pixel: {img.getpixel((240,160))}')
print('DONE')