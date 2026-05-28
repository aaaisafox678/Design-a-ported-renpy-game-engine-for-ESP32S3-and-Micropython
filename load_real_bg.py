#!/usr/bin/env python3
"""加载 游戏 真实背景: campsite_day + dialogue box"""
import sys,os,re,shutil
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

# 加载 campsite_day
bg=os.path.join(GAME,'images/BGs/campsite_day.rgb565')
if os.path.exists(bg):
    data=open(bg,'rb').read()
    d.fb._buf=bytearray(data[:480*320*2])
    snap('bg_campsite_day')
    print('[OK] campsite_day loaded')

# 加载 entrance_day
bg2=os.path.join(GAME,'images/BGs/Entrance - Day.rgb565')
if os.path.exists(bg2):
    data=open(bg2,'rb').read()
    d.fb._buf=bytearray(data[:480*320*2])
    snap('bg_entrance_day')
    print('[OK] entrance_day loaded')

# 加载 campsite + 对话框覆盖
data=open(bg,'rb').read()
d.fb._buf=bytearray(data[:480*320*2])
for y in range(280,320):
    for x in range(480):
        d.fb.pixel(x,y,0x0000)
for y in range(285,310):
    for x in range(50,430):
        if (x*7+y*13)%30<8:
            d.fb.pixel(x,y,0xFFFF)
snap('bg_campsite_dialogue')
print('[OK] campsite + dialogue')

print('DONE - check /sdcard/CBRenpy/')