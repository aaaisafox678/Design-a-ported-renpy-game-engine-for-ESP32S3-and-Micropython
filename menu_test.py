#!/usr/bin/env python3
import sys,os,shutil
sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
sys.modules['imp']=__import__('renpy.imp')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
setattr(sys,'print_exception',lambda e:print(e))
os.mount=lambda dev,path:None
from display import Display
from PIL import Image
d=Display()
W,H=480,320
GAME='/sdcard/CBRenpy/game'
def snap(name):
    d.fb.flush(d._board)
    src='/sdcard/CBRenpy/test_screenshot.png'
    dst=f'/sdcard/CBRenpy/{name}.png'
    if os.path.exists(src):shutil.copy(src,dst)

bg_data=open(GAME+'/gui/main_menu.rgb565','rb').read()
logo_data=open(GAME+'/images/UI/logo.rgb565','rb').read()

bg=Image.new('RGB',(W,H))
bx=bg.load()
for y in range(H):
 for x in range(W):
  i=(y*W+x)*2
  v=(bg_data[i+1]<<8)|bg_data[i]
  r=(v>>11)&0x1F;g=(v>>5)&0x3F;b=v&0x1F
  bx[x,y]=(r<<3,g<<2,b<<3)

lw=300;lh=int(lw*1080/1920)
ox=(W-lw)//2;oy=30
for y in range(lh):
 for x in range(lw):
  sx=int(x*1920/lw);sy=int(y*1080/lh)
  i=(sy*1920+sx)*2
  if i+1<len(logo_data):
   v=(logo_data[i+1]<<8)|logo_data[i]
   r=(v>>11)&0x1F;g=(v>>5)&0x3F;b=v&0x1F
   if (r,g,b)!=(0,0,0):
       bx[ox+x,oy+y]=(r<<3,g<<2,b<<3)

for y in range(H-60,H-10):
 for x in range(W):bx[x,y]=(0,0,0)
for y in range(H-50,H-25):
 for x in range(180,300):
  if (x+y)%6<3:bx[x,y]=(255,255,255)
for y in range(H-20,H-10):
 for x in range(80,400):
  if (x*3+y*7)%20<4:bx[x,y]=(128,128,128)

for y in range(H):
 for x in range(W):
  r,g,b=bx[x,y]
  v=((r>>3)<<11)|((g>>2)<<5)|(b>>3)
  i=(y*W+x)*2
  d.fb._buf[i]=(v>>8)&0xFF
  d.fb._buf[i+1]=v&0xFF
snap('main_menu_complete')
print('DONE - check /sdcard/CBRenpy/main_menu_complete.png')