#
# MicroPython 兼容层 - 替换 renpy/compat/__init__.py
# 移除 future/CPython-only 依赖，提供 MicroPython 等价物
#
PY2 = False
# 注意: 不要覆盖 str! 原版 compat 用 str = future.text_type 是因为 Python 2
# MicroPython(Python 3) 中 str 就是 unicode，无需替换
# str 保持内置 str 不变

basestring = str
pystr = str

def bchr(x):
    return bytes([x])

def bord(x):
    if isinstance(x, int):
        return x
    return ord(x)

def tobytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8')

chr = chr
unicode = str
range = range

# 内置 open 直接用 MicroPython 的
import builtins
open = builtins.open

# pickle 尝试加载
try:
    import pickle
except ImportError:
    try:
        import ujson as pickle
        pickle.dumps = pickle.dumps if hasattr(pickle,'dumps') else (lambda o,_=None: pickle.dumps(o))
        pickle.loads = pickle.loads
    except:
        class FakePickle:
            def dumps(self,o,p=None): return b''
            def loads(self,b): return {}
            HIGHEST_PROTOCOL = 2
        pickle = FakePickle()

# MicroPython 不支持正则的 Pattern 类型，忽略
try:
    import re
except:
    re = type(sys)('re')
    re.compile = lambda *a: None

__all__ = ["PY2","open","basestring","pystr","range","bord","bchr","tobytes","chr","unicode"]