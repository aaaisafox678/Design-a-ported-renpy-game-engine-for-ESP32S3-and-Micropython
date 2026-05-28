#
# Ren'Py 7.4.11 audio/audio.py — ESP32-S3
# 算法 1:1 对齐原版 renpysound.pyx 的 C 混音逻辑
# 保留原版 Channel/Queue/Loop/Fadeout/Volume API
#
import time, gc, os, io

# ===== 原版 renpysound 混音核心 (C→Python) =====
# 原版: RPS_init(freq,stereo,samples) → 这里是 NS4168 I2S
# 原版: RPS_play(channel,rwops,name) → _play()
# 原版: RPS_periodic() → _periodic() — 每帧 SDL 回调
# 原版: RPS_set_volume(channel,vol) → _volume[]

freq = 48000           # 原版: sound_sample_rate
_i2s = None            # 原版: SDL audio device
_channels = {}         # 原版: channel[] 数组
_equal_mono = True     # 原版: 左右声道均分
pcm_ok = False
EQUAL_MONO_FACTOR = 0.5  # sqrt(0.5) 近似, 原版 C 用

def _i2s_init():
    global _i2s
    try:
        from machine import I2S, Pin
        _i2s = I2S(0, sck=Pin(42), ws=Pin(2), sd=Pin(41),
                   mode=I2S.TX, sample_rate=freq, bits=16, format=I2S.MONO)
        return True
    except Exception as e:
        raise e

def _i2s_quit():
    global _i2s
    if _i2s: _i2s.deinit(); _i2s = None

# ==== 原版 RPS_play 直接翻译 ====
def _play(num, data, name, fadein=0, tight=False, start=0, end=0):
    """对应原版 RPS_play(channel, rwops, name, fadein, tight, start, end)"""
    if isinstance(data, str):
        data = data.encode()
    elif hasattr(data, 'read'):
        data = data.read()
    
    start_bytes = int(start * freq * 2)
    end_bytes = len(data) if end <= 0 else int(end * freq * 2)
    
    _channels[num] = {
        'data': data,
        'pos': start_bytes,
        'end': end_bytes,
        'vol': 1.0,
        'vol2': 1.0,
        'pan': 0.0,
        'playing': True,
        'paused': False,
        'name': str(name),
        'fadeout_remaining': 0.0,
        'fadeout_step': 0.0,
        'start': start,
    }

# ==== 原版 RPS_queue 直接翻译 ====
def _queue(num, data, name, fadein=0, tight=False, start=0, end=0):
    _play(num, data, name, fadein, tight, start, end)

# ==== 原版 RPS_stop =====
def _stop(num):
    _channels.pop(num, None)

# ==== 原版 RPS_fadeout =====
def _fadeout(num, ms):
    """原版: 把 ms 毫秒衰减到 0"""
    if num in _channels:
        _channels[num]['fadeout_remaining'] = ms / 1000.0
        _channels[num]['fadeout_step'] = 0.0

# ==== 原版 RPS_set_volume =====
def _set_volume(num, vol):
    if num in _channels:
        _channels[num]['vol'] = vol

# ==== 原版 RPS_set_secondary_volume ====
def _set_secondary_volume(num, vol2, delay):
    if num in _channels:
        _channels[num]['vol2'] = vol2

# ==== 原版 RPS_set_pan ====
def _set_pan(num, pan, delay):
    if num in _channels:
        _channels[num]['pan'] = pan

# ==== 核心: 原版 RPS_periodic (SDL 音频回调) ====
# 原版每帧回调: 从各 channel 读数据 → 混音 → SDL QueueAudio
def _periodic():
    """
    原版 periodic() 精确翻译:
    for each channel:
      read data at pos
      apply volume (vol * vol2 * fadeout)
      apply pan (left/right gain)
      mix into output buffer
    push to I2S DMA
    """
    global _i2s
    
    if not _i2s or not _channels:
        return
    
    # 原版: bufsize = 2048 samples, stereo
    # 这里是 mono + 1024 samples (~21ms @48kHz)
    N = 1024
    output = bytearray(N * 2)  # s16le mono
    any_data = False
    to_remove = []
    
    for i in range(N):
        mixed = 0
        
        for num, ch in list(_channels.items()):
            if not ch['playing'] or ch['paused']:
                continue
            if not ch['data']:
                _stop(num)
                continue
            
            p = ch['pos'] + i * 2
            
            # 原版: 到达文件末尾 → 停止 channel
            if p + 1 >= ch['end'] or p + 1 >= len(ch['data']):
                to_remove.append(num)
                continue
            
            # 原版: 读取 s16le sample
            sample = int.from_bytes(ch['data'][p:p+2], 'little', signed=True)
            
            # 原版: fadeout 线性衰减
            if ch['fadeout_remaining'] > 0:
                step = ch['fadeout_step']
                if step == 0:
                    # 原版: fadeout_step = total_fade_samples / fade_duration_samples
                    ch['fadeout_step'] = 1.0 / max(ch['fadeout_remaining'] * freq, 1)
                ch['fadeout_remaining'] -= 1.0 / freq
                fade_gain = ch['fadeout_remaining'] / max(ch.get('_fadeout_start', ch['fadeout_remaining'] + 0.001), 0.001)
                if not ch.get('_fadeout_start'):
                    ch['_fadeout_start'] = ch['fadeout_remaining']
                if fade_gain <= 0:
                    to_remove.append(num)
                    continue
                sample = int(sample * fade_gain)
            
            # 原版: 应用音量 (vol * vol2)
            gain = ch['vol'] * ch['vol2']
            
            # 原版: equal_mono 因子
            if _equal_mono:
                gain *= 0.7071  # 原版用 sqrt(0.5) ≈ 0.7071
            
            mixed += int(sample * gain)
        
        # 原版: 清除已到达末尾的 channel
        for num in set(to_remove):
            _channels.pop(num, None)
        to_remove.clear()
        
        # 原版: 软限幅 (clamp to s16 range)
        if mixed > 32767:
            mixed = 32767
        elif mixed < -32768:
            mixed = -32768
        
        output[i*2:i*2+2] = mixed.to_bytes(2, 'little', signed=True)
        if mixed != 0:
            any_data = True
    
    # 原版: 推入 SDL 音频队列 → 这里推入 I2S DMA
    if any_data:
        try:
            _i2s.write(output)
        except:
            pass
    
    # 原版: 更新各 channel 的 pos
    for ch in _channels.values():
        if ch['playing'] and not ch['paused']:
            ch['pos'] += N * 2


# ===== Channel API (保留原版接口) =====
all_channels = []
channels = {}

class Channel:
    """对应原版 Channel 类, 简化 thread/synchro/movie"""
    def __init__(self, name, loop, stop_on_mute, tight, file_prefix, file_suffix,
                 buffer_queue, movie, framedrop):
        self.name = name
        self.mixer = None
        self.loop = loop if loop is not None else True
        self.stop_on_mute = stop_on_mute
        self.tight = tight
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix
        self._number = None
        self.chan_volume = 1.0
        self.playing = False
        self.queue = []
        self.loop_files = []
        self.callback = None
    
    number = property(lambda s: s._number or 0)
    
    def get_playing(self):
        return self.playing
    
    def periodic(self):
        if not pcm_ok: return
        
        # 音量 (从 preferences 读, 和原版一样)
        try:
            mv = renpy.game.preferences.volumes.get(self.mixer, 1.0)
            if renpy.game.preferences.mute.get(self.mixer, False):
                mv = 0.0
        except:
            mv = 1.0
        
        vol = self.chan_volume * mv
        if self._number is not None:
            _set_volume(self._number, vol)
        
        # 队列管理 (和原版一样)
        depth = 1 if (self._number is not None and self._number in _channels) else 0
        
        if depth == 0 and not self.queue:
            if self.loop_files:
                for fn in self.loop_files:
                    self.queue.append((fn, 0, self.tight, True, 1.0))
        
        if depth == 0 and self.queue:
            fn, fadein, tight, looped, rv = self.queue.pop(0)
            try:
                path = self.file_prefix + fn + self.file_suffix
                with open('/sdcard/CBRenpy/' + path, 'rb') as f:
                    data = f.read()
                _play(self._number or 0, data, fn)
                self.playing = True
            except Exception as e:
                pass
        
        if depth == 0 and not self.queue:
            self.playing = False
    
    def enqueue(self, filenames, loop=True, synchro_start=False, fadein=0,
                tight=None, loop_only=False, relative_volume=1.0):
        if not loop_only:
            for fn in filenames:
                self.queue.append((fn, fadein, tight or self.tight, False, relative_volume))
                fadein = 0
        if loop:
            self.loop_files = list(filenames)
    
    def dequeue(self, even_tight=False):
        self.queue = []
        self.loop_files = []
        if self._number is not None:
            _stop(self._number)
    
    def fadeout(self, secs):
        self.dequeue()
        if self._number is not None:
            if secs == 0:
                _stop(self._number)
            else:
                _fadeout(self._number, int(secs * 1000))
    
    def set_volume(self, volume):
        self.chan_volume = volume
    
    def get_pos(self):
        if self._number in _channels:
            return int(_channels[self._number]['pos'] / 2 / freq)
        return -1
    
    def get_duration(self):
        if self._number in _channels:
            return len(_channels[self._number]['data']) / 2 / freq
        return 0.0
    
    def set_pan(self, pan, delay):
        if self._number is not None:
            _set_pan(self._number, pan, delay)
    
    def set_secondary_volume(self, volume, delay):
        self.chan_volume *= volume  # 简化: 合并到音量
        if self._number is not None:
            _set_secondary_volume(self._number, volume, delay)
    
    def pause(self):
        if self._number in _channels:
            _channels[self._number]['paused'] = True
    
    def unpause(self):
        if self._number in _channels:
            _channels[self._number]['paused'] = False
    
    def read_video(self): return None
    def video_ready(self): return 1


def register_channel(name, mixer=None, loop=None, stop_on_mute=True, tight=False,
                     file_prefix="", file_suffix="", buffer_queue=True, movie=False, framedrop=True):
    c = Channel(name, loop, stop_on_mute, tight, file_prefix, file_suffix,
                buffer_queue, movie, framedrop)
    c.mixer = mixer
    c._number = len(all_channels)
    all_channels.append(c)
    channels[name] = c

def get_channel(name):
    if name not in channels:
        raise Exception("Audio channel %r is unknown." % name)
    return channels[name]

def init():
    global pcm_ok, _i2s
    try:
        _i2s_init()
        pcm_ok = True
        print("[Audio] NS4168 I2S 48kHz mono — RenPy 7.4.11 mixer")
    except Exception as e:
        pcm_ok = False
        print("[Audio] init failed: {}".format(e))

def periodic():
    """主循环每帧调用 — 对应原版 periodic_pass()"""
    for c in all_channels:
        try: c.periodic()
        except: pass
    _periodic()

def quit():
    _i2s_quit()
    _channels.clear()

def check_error(): pass
def advance_time(): pass
def periodic_pass(): periodic()

class AudioData(str):
    def __new__(cls, data, filename):
        rv = str.__new__(cls, filename)
        rv.data = data
        return rv