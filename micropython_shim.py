#
# MicroPython 适配层 for Ren'Py 7.4.11
# 提供 Python 2 兼容和 ESP32-S3 特殊处理
import sys
import os
import gc

# ===== Python 2/3 兼容 =====
PY2 = False
PY3 = True

# 兼容 Python 2 的 builtins
try:
    import builtins
except ImportError:
    builtins = __builtins__

# 确保 unicode 存在 (Python 2 特有)
try:
    unicode
except NameError:
    unicode = str

# 确保 basestring 存在
try:
    basestring
except NameError:
    basestring = str

# 兼容函数
def bchr(x):
    """bytes character"""
    if isinstance(x, str):
        return x
    return bytes([x])

def bord(x):
    """byte ordinal"""
    if isinstance(x, int):
        return x
    return ord(x)

def pystr(s):
    """Python string (Python 2/3 compat)"""
    return str(s)

# ===== 模拟缺失的模块 =====

# 模拟 pickle (MicroPython 可能没有)
try:
    import pickle
except ImportError:
    class _FakePickle:
        def dumps(self, obj):
            return str(obj)
        def loads(self, data):
            return eval(data)
    pickle = _FakePickle()

# 模拟 ctypes (MicroPython 没有)
try:
    import ctypes
except ImportError:
    class _FakeCTypes:
        class Structure:
            _fields_ = []
        c_ulong = int
        c_wchar = str
        c_ushort = int
        c_byte = int
    ctypes = _FakeCTypes()

# 模拟 platform
try:
    import platform
except ImportError:
    class _FakePlatform:
        def win32_ver(self):
            return (None,)
        def mac_ver(self):
            return (None,)
    platform = _FakePlatform()

# ===== 平台检测 =====
windows = False
macintosh = False
linux = False
android = False
ios = False
emscripten = False
mobile = True  # ESP32-S3 视为移动平台

# ===== TF卡路径配置 =====
GAME_DIR = "/sdcard/game"
RENPy_DIR = "/sdcard/renpy"
SAVES_DIR = "/sdcard/saves"
PERSISTENT_DIR = "/sdcard/persistent"

# ===== 内存优化策略 =====
# 1. 图片使用流式加载，不预加载
# 2. 音频使用 DMA 传输，不占 CPU
# 3. 脚本使用流式解析
# 4. 字体使用子集化渲染
# 5. 场景数据按需加载

# ===== 缓存配置 =====
_cache = {}
_cache_size = 0
CACHE_MAX_SIZE = 10  # 最多缓存10个文件

def cache_file(name, data):
    """缓存文件数据到 PSRAM"""
    global _cache_size
    if name in _cache:
        return
    size = len(data) if data else 0
    if _cache_size + size > CACHE_MAX_SIZE * 300 * 1024:  # 每个文件最大300KB
        _evict_one()
    _cache[name] = data
    _cache_size += size

def get_cached(name):
    """获取缓存的文件数据"""
    return _cache.get(name)

def _evict_one():
    """删除最旧的缓存"""
    global _cache_size
    if _cache:
        k = next(iter(_cache))
        s = len(_cache[k]) if _cache[k] else 0
        del _cache[k]
        _cache_size -= s

def clear_cache():
    """清空缓存"""
    global _cache_size
    _cache.clear()
    _cache_size = 0
    gc.collect()

# ===== 文件加载器 (TF卡优化) =====
def loadable(name):
    """检查文件是否可加载"""
    paths_to_try = [
        os.path.join(GAME_DIR, name),
        os.path.join(RENPy_DIR, name),
        name,
    ]
    for path in paths_to_try:
        try:
            return os.path.exists(path)
        except:
            pass
    return False

def open_file(name, mode='rb'):
    """打开文件（流式读取）"""
    paths_to_try = [
        os.path.join(GAME_DIR, name),
        os.path.join(RENPy_DIR, name),
        name,
    ]
    for path in paths_to_try:
        try:
            return open(path, mode)
        except:
            pass
    return None

def list_files(directory):
    """列出目录中的文件"""
    try:
        return os.listdir(os.path.join(GAME_DIR, directory))
    except:
        return []

def mkdir_p(path):
    """创建目录（如果不存在）"""
    try:
        os.makedirs(path)
    except:
        pass

def ensure_directories():
    """确保所有必要目录存在"""
    dirs = [
        GAME_DIR,
        RENPy_DIR,
        SAVES_DIR,
        PERSISTENT_DIR,
        os.path.join(GAME_DIR, "images"),
        os.path.join(GAME_DIR, "audio"),
        os.path.join(GAME_DIR, "scripts"),
        os.path.join(GAME_DIR, "saves"),
        os.path.join(GAME_DIR, "gui"),
        os.path.join(GAME_DIR, "Fonts"),
    ]
    for d in dirs:
        mkdir_p(d)

# 初始化目录
ensure_directories()

# ===== 性能优化 =====
def gc_collect():
    """手动触发垃圾回收"""
    gc.collect()

def get_free_memory():
    """获取可用内存（字节）"""
    try:
        return gc.mem_free()
    except:
        return 0

def get_allocated_memory():
    """获取已分配内存（字节）"""
    try:
        return gc.mem_alloc()
    except:
        return 0

# ===== 调试输出 =====
def debug_print(msg):
    """调试输出到串口"""
    print("[RenPy-MPy] " + str(msg))

def log_memory(label=""):
    """记录内存使用情况"""
    free = get_free_memory()
    alloc = get_allocated_memory()
    debug_print("{}: free={} alloc={}".format(label, free, alloc))