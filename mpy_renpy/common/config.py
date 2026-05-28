# ========== 屏幕配置 ==========
screen_width = 320
screen_height = 480

# ========== 音频配置 ==========
sound = True
sound_sample_rate = 48000
fadeout_audio = 0.016

# ========== 渲染配置 ==========
gl_enable = True
renderer = "auto"
framerate = 60
image_cache_size_mb = 2  # ESP32-S3内存限制
image_cache_size = 1

# ========== 游戏信息 ==========
name = "Micro-RenPy Demo"
version = "1.0"
gamedir = ""
basedir = "/"
renpy_base = "/mpy_renpy"

# ========== 层配置 (对齐RenPy层系统) ==========
layers = ["master", "transient", "screens", "overlay"]
transient_layers = ["transient"]
overlay_layers = ["overlay"]
top_layers = ["top"]
bottom_layers = ["bottom"]
sticky_layers = ["master"]

# ========== 对话和菜单配置 ==========
say_layer = "screens"
choice_layer = "screens"

# ========== 滚动和跳过配置 ==========
allow_skipping = True
fast_skipping = False
skipping = None
skip_delay = 5

# ========== 回滚配置 ==========
rollback_enabled = True
rollback_length = 128
hard_rollback_limit = 100

# ========== 自动保存配置 ==========
has_autosave = True
autosave_slots = 5
autosave_frequency = 100
autosave_on_choice = True
autosave_on_input = True

# ========== 调试配置 ==========
debug = False
debug_sound = False
developer = False
original_developer = False

# ========== 过渡效果配置 ==========
enable_fast_dissolve = True
load_before_transition = True
implicit_with_none = True

# ========== 字体配置 ==========
font_replacement_map = {}
preload_fonts = []

# ========== 文本配置 ==========
text_layout = None
afm_characters = 150  # 适配320px屏幕
afm_bonus = 15

# ========== GC配置 (ESP32-S3内存管理) ==========
manage_gc = True
gc_thresholds = (5000, 10, 10)
idle_gc_count = 500

# ========== 音频通道配置 ==========
play_channel = "audio"
movie_mixer = "music"
auto_channels = {"audio": ("sfx", "", "")}
voice_mixers = ["voice"]
emphasize_audio_channels = ["voice"]
emphasize_audio_volume = 0.8
emphasize_audio_time = 0.5

# ========== 搜索路径 ==========
search_prefixes = [""]
archives = []
searchpath = []

# ========== 关键回调 (对齐RenPy架构) ==========
scene = None
show = None
hide = None
character_callback = None
with_callback = None
periodic_callback = None

# ========== 自定义 RenPy 兼容函数 ==========
def locked():
    """检查配置是否已锁定"""
    return False

def mode(mode_name):
    """获取当前模式"""
    return None

def notify(message):
    """发送通知"""
    pass

def log(message):
    """写入日志"""
    pass

# ========== 锁定配置 ==========
locked = False
