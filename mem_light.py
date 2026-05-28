import sys,os,gc
sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
sys.modules['imp']=__import__('renpy.imp')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
os.mount=lambda dev,path:None
import tracemalloc;tracemalloc.start()
def m():return tracemalloc.get_traced_memory()[0]//1024

import renpy;renpy.config.gamedir='/sdcard/CBRenpy/game'
print(f'[renpy] {m()}KB')
from display import Display;d=Display()
print(f'[display] {m()}KB')

G='/sdcard/CBRenpy/game'

# 实战模拟: 背景1→释放→背景2→释放
bg=open(G+'/images/BGs/campsite_day.rgb565','rb').read()
print(f'[bg1] {m()}KB')
del bg;gc.collect()
print(f'[gc] {m()}KB')

bg2=open(G+'/images/BGs/Entrance - Day.rgb565','rb').read()
print(f'[bg2] {m()}KB')
del bg2;gc.collect()

logo=open(G+'/images/UI/logo.rgb565','rb').read()
print(f'[logo] {m()}KB')
del logo;gc.collect()

# 脚本流式(只500行)
with open(G+'/script.rpy','r') as f:
    for i,l in enumerate(f):
        if i>500:break
print(f'[script 500l] {m()}KB')
gc.collect()

# 音频
audio=open(G+'/Audio/BGM/016 - Sleeping time.pcm','rb').read()
print(f'[audio 730KB] {m()}KB')
# 模拟混音器: 不存全文件,只存当前通道块(100KB)
del audio;gc.collect()
print(f'[gc audio] {m()}KB')

gc.collect()
print(f'\n=== PEAK: {m()}KB = {m()/1024:.1f}MB / 8MB PSRAM ===')
print(f'=== SAFE: {(8-m()/1024):.1f}MB margin ===')