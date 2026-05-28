#
# Ren'Py 7.4.11 store.py - MicroPython适配
# 这是游戏变量的核心存储模块
#
import sys
import gc

# 全局变量存储
_store = {}
_call_stack = []
_return = None
_args = None
_kwargs = None
_window = False
_window_subtitle = ''
_rollback = True
_skipping = True
_menu = False
main_menu = False
_autosave = True
_in_replay = None
default_transition = None
mouse_visible = True

# 持久化存储API
class PersistentData:
    def __init__(self):
        self._data = {}
        self.current_lang = "English"
        self.first_time = False
        self.voicereplay = False
        self._set_preferences = False
        self._gui_preference = {}
        self._gui_preference_default = {}
    
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        return self._data.get(name, None)
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

persistent = PersistentData()

# 偏好设置
class Preferences:
    def __init__(self):
        self.text_cps = 40
        self.afm_time = 15
        self.afm_enable = False
        self.fullscreen = False
        self.language = None
        self.wait_voice = True
        self.voice_sustain = False
        self.mouse_move = True
        self.show_empty_window = True
        self.emphasize_audio = False
        self.virtual_size = None
        self.physical_size = None
    
    def set_volume(self, channel, vol):
        setattr(self, 'vol_' + channel, vol)
    
    def get_volume(self, channel):
        return getattr(self, 'vol_' + channel, 1.0)
    
    def check(self):
        return None

_preferences = Preferences()

# 历史记录
_history_list = []
_history = False

# 初始化
def InitStore():
    global _store
    _store.clear()
    
    # 注入 renpy.exports 引用
    import renpy.exports as _exports
    _store['renpy'] = _exports
    
    # 核心运行时变量
    _store['_return'] = None
    _store['_args'] = None
    _store['_kwargs'] = None
    _store['_window'] = False
    _store['_window_subtitle'] = ''
    _store['_rollback'] = True
    _store['_skipping'] = True
    _store['_menu'] = False
    _store['main_menu'] = False
    _store['_autosave'] = True
    _store['_in_replay'] = None
    
    _store['persistent'] = persistent
    _store['_preferences'] = _preferences
    _store['preferences'] = _preferences
    _store['_history_list'] = _history_list
    _store['_history'] = _history
    
    # 默认过渡效果
    _store['default_transition'] = None
    _store['mouse_visible'] = True
    
    # 注册为 sys.modules
    sys.modules['store'] = type(sys)('store')
    sys.modules['store'].__dict__.update(_store)
    sys.modules['renpy.store'] = sys.modules['store']

# 导出
__all__ = ['_store', 'persistent', '_preferences', '_history_list', 
           'InitStore', 'main_menu', 'default_transition']