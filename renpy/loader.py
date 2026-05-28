#
# Ren'Py 7.4.11 loader — TF卡资源加载（带自动格式降级）
#
# PNG/JPG → .rgb565 (ffmpeg预转的320x480 raw RGB565)
# OGG     → .pcm   (ffmpeg预转的48kHz 16bit mono PCM)
# WEBM    → .mjpeg (ffmpeg预转的MJPEG视频)
# 其他    → 直接读
#
import os

GAME_DIR = "/sdcard/CBRenpy/game"

# 格式降级表
FALLBACK = {
    '.png': '.rgb565',
    '.jpg': '.rgb565',
    '.jpeg': '.rgb565',
    '.ogg': '.pcm',
    '.webm': '.avi',
    '.mp4': '.avi',
    '.avi': '.avi',
}

_cache = {}

def loadable(name):
    """文件是否可加载"""
    return resolve(name) is not None

def resolve(name):
    """解析真实路径（自动降级）"""
    full = os.path.join(GAME_DIR, name)
    try:
        if os.path.isfile(full):
            return full
    except:
        pass
    ext = '.' + name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    fb = FALLBACK.get(ext)
    if fb:
        alt = os.path.join(GAME_DIR, name.rsplit('.', 1)[0] + fb)
        try:
            if os.path.isfile(alt):
                return alt
        except:
            pass
    return None

def open(name, mode='rb'):
    p = resolve(name)
    if p:
        return __builtins__.open(p, mode)
    raise OSError("not found: " + name)

def read(name):
    p = resolve(name)
    if p:
        with __builtins__.open(p, 'rb') as f:
            return f.read()
    return None

def read_image_rgb565(name):
    """读图片 → (480, 320, bytearray)"""
    import gc
    gc.collect()
    data = read(name)
    if data:
        return (480, 320, data)
    return None

def read_audio_pcm(name):
    """读音频 → bytes"""
    return read(name)

def listdir(path):
    try:
        return os.listdir(os.path.join(GAME_DIR, path))
    except:
        return []