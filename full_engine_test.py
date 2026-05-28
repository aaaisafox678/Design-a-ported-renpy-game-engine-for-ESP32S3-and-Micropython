#!/usr/bin/env python3
"""
完整引擎运行: Ren'Py → 加载脚本 → 解析主菜单 screen → 逐层渲染
"""
import sys,os,re,shutil
sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
sys.modules['imp']=__import__('renpy.imp')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
setattr(sys,'print_exception',lambda e:print(e))
os.mount=lambda dev,path:None
import builtins

import renpy
renpy.config.gamedir='/sdcard/CBRenpy/game'
renpy.config.basedir='/sdcard/CBRenpy'

from display import Display
d=Display()
W,H=480,320
GAME='/sdcard/CBRenpy/game'

def snap(name):
    d.fb.flush(d._board)
    src='/sdcard/CBRenpy/test_screenshot.png'
    dst=f'/sdcard/CBRenpy/{name}.png'
    if os.path.exists(src):
        shutil.copy(src,dst)
        print(f'  [SNAP] {name} ({os.path.getsize(dst)}B)')

def load_rgb(path):
    """加载 rgb565 文件到 framebuf"""
    full=os.path.join(GAME,path)
    rgb=full.rsplit('.',1)[0]+'.rgb565'
    if os.path.exists(rgb):
        data=open(rgb,'rb').read()
        d.fb._buf=bytearray(data[:W*H*2])
        return True
    return False

# ===== 第1步: 解析 gui.rpy 取得 main_menu_background =====
print('[1] Parsing gui.rpy...')
bg_path='gui/main_menu.png'
with open(f'{GAME}/gui.rpy','r',encoding='utf-8',errors='ignore') as f:
    for line in f:
        m=re.search(r'define gui\.main_menu_background\s*=\s*"([^"]+)"',line)
        if m:
            bg_path=m.group(1)
            print(f'  main_menu bg = {bg_path}')
            break

# ===== 第2步: 加载主菜单背景 =====
print('[2] Loading main menu background...')
if load_rgb(bg_path):
    snap('step1_bg')
    print(f'  BG loaded: {bg_path}')
else:
    print(f'  FAIL: {bg_path} not found')

# ===== 第3步: 解析 logo =====
print('[3] Looking for logo...')
logo_path=None
with open(f'{GAME}/script.rpy','r',encoding='utf-8',errors='ignore') as f:
    for line in f:
        m=re.search(r'image logo\s*=\s*"([^"]+)"',line)
        if m:
            logo_path='images/UI/logo.rgb565'
    print(f'  logo = {logo_path}')
            break

# ===== 第4步: 叠加 logo (居中缩放) =====
if logo_path:
    print('[4] Overlaying logo...')
    # logo 1920x1080 缩放到 ~320x (占屏幕2/3宽)
    full=os.path.join(GAME,'images/UI/logo.rgb565')
    if os.path.exists(full):
        logo_data=open(full,'rb').read()
        # 用 PIL 缩放 logo 再叠到 framebuf 上
        from PIL import Image
        # 重建背景
        bg_data=open(os.path.join(GAME,bg_path).rsplit('.',1)[0]+'.rgb565','rb').read()
        bg_img=Image.new('RGB',(W,H))
        bx=bg_img.load()
        for y in range(H):
            for x in range(W):
                i=(y*W+x)*2
                val=(bg_data[i+1]<<8)|bg_data[i]
                r=(val>>11)&0x1F;g=(val>>5)&0x3F;b=val&0x1F
                bx[x,y]=(r<<3,g<<2,b<<3)
        
        # logo 原始 1920x1080 → 缩放到 300x
        logo_w=300;logo_h=int(logo_w*1080/1920)
        logo_img=Image.new('RGB',(logo_w,logo_h))
        # 从 logo_data 读取（按 1920x1080 解析）
        lx=logo_img.load()
        for y in range(logo_h):
            for x in range(logo_w):
                sx=int(x*1920/logo_w)
                sy=int(y*1080/logo_h)
                i=(sy*1920+sx)*2
                if i+1<len(logo_data):
                    val=(logo_data[i+1]<<8)|logo_data[i]
                    r=(val>>11)&0x1F;g=(val>>5)&0x3F;b=val&0x1F
                    lx[x,y]=(r<<3,g<<2,b<<3)
        
        # 居中叠到背景
        ox=(W-logo_w)//2;oy=60
        for y in range(logo_h):
            for x in range(logo_w):
                if ox+x<W and oy+y<H:
                    bx[ox+x,oy+y]=lx[x,y]
        
        # 转回 rgb565 写入 framebuf
        for y in range(H):
            for x in range(W):
                r,g,b=bx[x,y]
                val=((r>>3)<<11)|((g>>2)<<5)|(b>>3)
                i=(y*W+x)*2
                d.fb._buf[i]=(val>>8)&0xFF
                d.fb._buf[i+1]=val&0xFF
        snap('step2_logo')
        print(f'  Logo overlayed at ({ox},{oy})')
    else:
        print(f'  Logo not converted')

# ===== 第5步: 添加菜单按钮模拟 =====
print('[5] Adding menu buttons...')
# 底部按钮区域
for y in range(H-60,H-10):
    for x in range(W):
        d.fb.pixel(x,y,0x0000)  # 黑色按钮区
# START 按钮
for y in range(H-50,H-18):
    for x in range(160,320):
        if (x+y)%6<3:
            d.fb.pixel(x,y,0xFFFF)
snap('step3_buttons')
print('  Buttons added')

# ===== 第6步: 添加底部版权文字模拟 =====
print('[6] Adding copyright text...')
for y in range(H-8,H-2):
    for x in range(100,380):
        if (x*3+y*7)%20<4:
            d.fb.pixel(x,y,0x8410)
snap('step4_copyright')
print('  Copyright added')

print('\n=== COMPLETE ===')
print('Files: /sdcard/CBRenpy/step{1..4}_*.png')