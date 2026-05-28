"""快速测试 - 直接生成截图并验证"""
import sys,os
sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
import renpy.imp;sys.modules['imp']=renpy.imp
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')

from display import Display
d = Display(brightness=80)

# 截图1: 色条
for i in range(16):
    bw=d.width//16
    rv=(i*16)&0xFF;gv=(i*8)&0xFF;bv=(i*4)&0xFF
    c=((rv>>3)<<11)|((gv>>2)<<5)|(bv>>3)
    for y in range(80,240):
        for x in range(i*bw,(i+1)*bw):
            d.fb.pixel(x,y,c)
d.fb.flush(d._board)
os.rename('/sdcard/CBRenpy/test_screenshot.png','/sdcard/CBRenpy/shot1_bars.png')
print('[1] bars OK')

# 截图2: 真实游戏背景
bg='/sdcard/CBRenpy/game/images/BGs/alley_day.rgb565'
if os.path.exists(bg):
    data=open(bg,'rb').read()
    d.fb._buf=bytearray(data[:d.width*d.height*2])
    d.fb.flush(d._board)
    os.rename('/sdcard/CBRenpy/test_screenshot.png','/sdcard/CBRenpy/shot2_bg.png')
    print('[2] bg OK')
else:
    print('[2] bg missing, skip')

# 截图3: 游戏界面模拟
if os.path.exists(bg):
    data=open(bg,'rb').read()
    d.fb._buf=bytearray(data[:d.width*d.height*2])
    for y in range(d.height-40,d.height):
        for x in range(d.width):
            d.fb.pixel(x,y,0x2104)
    for y in range(d.height-35,d.height-10):
        for x in range(100,d.width-100):
            if (x+y)%8<4:d.fb.pixel(x,y,0xFFFF)
    d.fb.flush(d._board)
    os.rename('/sdcard/CBRenpy/test_screenshot.png','/sdcard/CBRenpy/shot3_ui.png')
    print('[3] ui OK')

from PIL import Image
for s in ['shot1_bars','shot2_bg','shot3_ui']:
    p=f'/sdcard/CBRenpy/{s}.png'
    if os.path.exists(p):
        img=Image.open(p)
        px=img.getpixel((100,100))
        print(f'{s}: {img.size} px(100,100)={px}')
print('DONE')