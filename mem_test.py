#!/usr/bin/env python3
"""模拟 ESP32-S3 真实内存占用"""
import sys,os,gc,time

sys.path.insert(0,'.')
exec(open('test_env_shim.py').read())
sys.modules['imp']=__import__('renpy.imp')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
os.mount=lambda dev,path:None

# 模拟 MicroPython 内存统计
import tracemalloc
tracemalloc.start()

def mem_used():
    cur,_ = tracemalloc.get_traced_memory()
    return cur

def status(msg):
    print(f'  [{mem_used()//1024:>5}KB] {msg}')

print("=== ESP32-S3 内存模拟 (模拟 PSRAM 8MB) ===")
status("导入 renpy 前")

import renpy
renpy.config.gamedir='/sdcard/CBRenpy/game'
status("renpy 导入后")

from display import Display
d=Display(brightness=80)
status("Display 初始化 (含 300KB framebuf) ")

GAME='/sdcard/CBRenpy/game'

# 测试1: 加载背景
bg=open(GAME+'/gui/main_menu.rgb565','rb').read()
status("加载 main_menu 背景 (300KB)")
bg2=open(GAME+'/images/BGs/campsite_day.rgb565','rb').read()
status("加载 campsite_day 背景 (300KB)")

# 测试2: 加载logo
logo=open(GAME+'/images/UI/logo.rgb565','rb').read()
status("加载 logo (300KB)")

# 测试3: 模拟角色立绘
try:
    sprite=open(GAME+'/images/Sprites/Faces/keitaro1_f_smile1.png', 'rb').read()
    status("加载 keitaro 立绘")
except:
    status("加载立绘 (跳过，使用logo)")

# 测试4: 加载音频 (PCM)
try:
    import glob
    pcm_files=sorted([f for f in os.listdir(GAME+'/Audio/BGM') if f.endswith('.pcm')])
    if pcm_files:
        audio=open(GAME+'/Audio/BGM/'+pcm_files[0],'rb').read()
        status(f"加载 BGM: {pcm_files[0]} ({len(audio)//1024}KB)")
except Exception as e:
    status(f"音频: {e}")

# 测试5: 模拟 render.py 缓存
status("导入 renpy.display.render")
import renpy.display.render
r=renpy.display.render.Render(480,320)
status("创建 Render 对象")

# 测试6: 模拟场景切换 (GC test)
for i in range(5):
    d.fb._buf=bytearray(bg[:300*1024])  # 只取300KB
    gc.collect()
status(f"5次 GC 后")

# 测试7: 加载 script.rpy 解析
sc=open(GAME+'/script.rpy','r').read()
status(f"读取 script.rpy ({len(sc)//1024}KB)")

# 测试8: 混音器占用
import renpy.audio.renpysound as rps
rps.init(48000,2,2048,False,True)
# 模拟3通道
rps.play(0,io.BytesIO(audio[:100000]) if 'audio' in dir() else io.BytesIO(bg[:100000]), 'test')
rps.play(1,io.BytesIO(bg[:50000]), 'sfx')
status("混音器 2通道 + 缓冲区")

peak=mem_used()
print(f"\n=== 峰值内存: {peak//1024}KB ≈ {peak/1024/1024:.1f}MB ===")
print(f"=== ESP32-S3 可用: 8MB PSRAM, 安全余量: {8-peak/1024/1024:.1f}MB ===")

del bg,bg2,logo,sc
gc.collect()
status("清理后")

tracemalloc.stop()