import sys,os,gc
sys.path.insert(0,'.')

# ==== 加载 CPython 测试环境 shim ====
exec(open('test_env_shim.py').read())

# 注册缺失模块
import renpy.imp;sys.modules['imp']=renpy.imp
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')

gc.collect()
print('[MEM] OK')

# ==== 测试 1: 导入 Ren'Py ====
import renpy
print('[1] RenPy import OK -',renpy.version_only)

# ==== 测试 2: 渲染测试图片到 framebuf ====
print('[2] Rendering test image...')
from display import Display
d = Display(brightness=80)
d.fb.fill(d.BLACK)

# 画一些测试元素
for i in range(16):
    bar_w = 480//16
    # RGB color bars
    r=(i*16)&0xFF;g=(i*8)&0xFF;b=(i*4)&0xFF
    c = ((r>>3)<<11)|((g>>2)<<5)|(b>>3)
    for y in range(50):
        for x in range(i*bar_w, (i+1)*bar_w):
            d.fb.pixel(x, y+20, c)

# 文字区域
d.fb.fill_rect = lambda x,y,w,h,color: None  # 简化
d.show()
print('[2] Test image saved to /sdcard/CBRenpy/test_screenshot.png')

# ==== 测试 3: 加载真实 rgb565 图片 ====
print('[3] Loading real game image...')
bg_path = '/sdcard/CBRenpy/game/images/BGs/alley_day.rgb565'
if os.path.exists(bg_path):
    data = open(bg_path,'rb').read()
    d.fb._buf = bytearray(data[:480*320*2])
    d.show()
    print('[3] Loaded alley_day.rgb565 (480x320 16:9 with black bars)')
else:
    # 尝试其他图片
    import glob
    pics = glob.glob('/sdcard/CBRenpy/game/images/BGs/*.rgb565')[:3]
    if pics:
        data = open(pics[0],'rb').read()
        d.fb._buf = bytearray(data[:480*320*2])
        d.show()
        print('[3] Loaded:',os.path.basename(pics[0]))
    else:
        print('[3] No game images found')

# ==== 测试 4: 跑 main.py ====
print('[4] Running main.py...')
try:
    exec(open('main.py').read())
    print('[4] main.py completed')
except Exception as e:
    print('[4] main.py error:',e)
    import traceback;traceback.print_exc()

print('=== ALL TESTS DONE ===')