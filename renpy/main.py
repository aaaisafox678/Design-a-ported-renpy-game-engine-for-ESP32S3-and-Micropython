#
# Ren'Py 7.4.11 main.py — ESP32-S3 入口 + 视频帧播放器
#
import gc, time, sys, os

def main(restart=False):
    import renpy, renpy.config as config, renpy.store as store
    
    print("Micro-RenPy {} 启动".format(renpy.version_only))
    print("屏幕: {}x{}".format(config.screen_width, config.screen_height))
    
    config.gamedir = "/sdcard/CBRenpy/game"
    config.basedir = "/sdcard/CBRenpy"
    
    # === 1. 加载脚本 (流式) ===
    for fn in ['gui.rpy','options.rpy','screens.rpy','script.rpy']:
        _load_script_stream(os.path.join(config.gamedir, fn))
    
    # === 2. 播放开场视频 (如果有) ===
    _play_video_if_exists(config.gamedir + '/video/opening.raw')
    
    # === 3. 显示主菜单 ===
    _show_main_menu()
    
    # === 4. 交互循环 ===
    _interact_loop()


def _load_script_stream(path):
    """流式加载: 只读 define/default/image/$ 行"""
    try:
        with open(path, 'r') as f:
            for line in f:
                s = line.strip()
                if not s or s[0] == '#': continue
                if s.startswith(('define ','default ','image ')):
                    _exec_single_line(s)
                elif s.startswith('$ '):
                    try: exec(s[2:], globals())
                    except: pass
        gc.collect()
    except OSError:
        pass

def _exec_single_line(line):
    import renpy.config as config
    rest = line.split(None, 1)[1] if ' ' in line else ''
    if '=' not in rest: return
    name, val = rest.split('=', 1)
    name, val = name.strip(), val.strip().strip('"').strip("'")
    
    if name.startswith('config.'):
        try: setattr(config, name[7:], val)
        except: pass
    elif name.startswith('gui.'):
        import renpy.store as store
        store._store.setdefault('gui', {})
        try: store._store['gui'][name[4:]] = val
        except: pass
    elif line.startswith('image '):
        import renpy.store as store
        store._store.setdefault('images', {})
        store._store['images'][name] = val

def _play_video_if_exists(basepath):
    """同步播放 raw 视频帧 + PCM 音频"""
    vid = basepath + '.raw'
    aud = basepath + '.pcm'
    if not os.path.exists(vid):
        return
    
    try:
        from display import Display
        d = Display(brightness=80)
    except:
        return
    
    # 音频(如果有)
    audio_data = None
    if os.path.exists(aud):
        audio_data = open(aud, 'rb').read()
        import renpy.audio.renpysound as rps
        try: rps.init(48000, 2, 2048, False, True)
        except: pass
        rps.play(0, audio_data, 'opening')
    
    # 视频
    data = open(vid, 'rb').read()
    frames = len(data) // 307200
    FRAME_MS = 200  # 5fps = 200ms
    
    t0 = time.ticks_ms()
    for i in range(frames):
        offset = i * 307200
        d.fb._buf = bytearray(data[offset:offset+307200])
        d.show()
        
        # 保持帧率
        elapsed = time.ticks_diff(time.ticks_ms(), t0)
        target = (i + 1) * FRAME_MS
        if elapsed < target:
            time.sleep_ms(target - elapsed)
    
    # 清理
    del data; gc.collect()
    if audio_data:
        rps.stop(0)
        del audio_data; gc.collect()

def _show_main_menu():
    """显示主菜单: 背景 + logo 叠层"""
    try:
        from display import Display
        d = Display(brightness=80)
    except:
        return
    
    GAME = '/sdcard/CBRenpy/game'
    bg_path = GAME + '/gui/main_menu.rgb565'
    logo_path = GAME + '/images/UI/logo.rgb565'
    
    if os.path.exists(bg_path):
        data = open(bg_path, 'rb').read()
        d.fb._buf = bytearray(data[:307200])
        d.show()
    gc.collect()

def _interact_loop():
    """简化交互: 等待触摸然后循环"""
    try:
        from display import Display
        d = Display(brightness=80)
    except:
        d = None
    
    print(">>> 交互循环启动 <<<")
    
    if d:
        while True:
            pts = d.touch()
            if pts:
                print("Touch:", pts)
            time.sleep(0.1)