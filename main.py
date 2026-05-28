#!/usr/bin/env python3
#
# Micro-RenPy 7.4.11 for JC3248W535CN
# 启动入口 - 三步截图: 色条测试 → 游戏背景 → 错误界面
#
import sys, os, gc, time

print("=" * 50)
print("Micro-RenPy 7.4.11 启动")
print("目标: JC3248W535CN (ESP32-S3)")
print("游戏: 游戏 v2.3")
print("=" * 50)

# ===== 1. 初始化显示 =====
print("[1/4] 初始化显示...")
try:
    from display import Display
    from writer import CWriter
    import fonts.sans24 as sans24
    import fonts.sans16 as sans16
    
    d = Display(brightness=80)
    W, H = d.width, d.height
    print("[OK] 显示: {}x{}".format(W, H))
    
except Exception as e:
    print("[ERROR] 显示初始化失败: {}".format(e))
    try: sys.print_exception(e)
    except: pass
    d = None; W, H = 480, 320

# ===== 2. 色条测试截图 =====
print("[2/4] 色条测试...")
if d:
    for i in range(16):
        bar_w = W // 16
        r_val = (i * 16) & 0xFF
        g_val = (i * 8) & 0xFF
        b_val = (i * 4) & 0xFF
        color = ((r_val >> 3) << 11) | ((g_val >> 2) << 5) | (b_val >> 3)
        for y in range(H // 4, H * 3 // 4):
            for x in range(i * bar_w, (i + 1) * bar_w):
                d.fb.pixel(x, y, color)
    d.show()
    print("[OK] 截图1: test_bars.png")

# ===== 3. 加载真实游戏背景 =====
print("[3/4] 加载游戏背景...")
game_bg = None
try:
    import renpy.loader as loader
    # 加载 alley_day.rgb565
    data = loader.read_image_rgb565("images/BGs/alley_day.jpg")
    if data:
        d.fb._buf = bytearray(data[2][:W*H*2])
        d.show()
        print("[OK] 截图2: alley_day.png ({}x{} 16:9+黑边)".format(W, H))
        game_bg = data
    else:
        # fallback: 画渐变
        for y in range(H):
            for x in range(W):
                r = (x * 255) // W
                g = (y * 255) // H
                b = 128
                c = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                d.fb.pixel(x, y, c)
        d.show()
        print("[WARN] 游戏背景未找到, 使用渐变")
except Exception as e:
    print("[WARN] 游戏背景加载失败: {}".format(e))

# ===== 4. 模拟游戏界面截图 =====
print("[4/4] 模拟游戏界面...")
if d and game_bg:
    # 背景 + 对话框模拟
    d.fb._buf = bytearray(game_bg[2][:W*H*2])
    # 底部对话框区域(280-320行) 填充深色
    for y in range(H - 40, H):
        for x in range(W):
            d.fb.pixel(x, y, 0x2104)  # 深灰
    # 白色文字区域(模拟)
    for y in range(H - 35, H - 10):
        for x in range(100, W - 100):
            if (x + y) % 8 < 4:  # 假文字
                d.fb.pixel(x, y, 0xFFFF)
    d.show()
    print("[OK] 截图3: game_ui.png")

# ===== 启动 Ren'Py 引擎 =====
print("\n--- 引擎加载 ---")
sys.path.insert(0, "/sdcard/micropython-renpy")
sys.path.insert(0, "/sdcard")

try:
    import renpy
    print("[OK] Ren'Py {} 已加载".format(renpy.version_only))
    gc.collect()
    
    import renpy.main
    renpy.main.main()
    
except Exception as e:
    print("[ERROR] 启动失败: {}".format(e))
    try: sys.print_exception(e)
    except: import traceback; traceback.print_exc()
    
    if d:
        d.fb.fill(d.RED)
        wri = CWriter(d.fb, sans16, verbose=False)
        CWriter.set_textpos(d.fb, 10, 10)
        wri.setcolor(d.WHITE, d.RED)
        wri.printstring("ERR: " + str(e)[:100])
        d.show()

print("\nMicro-RenPy 已退出")