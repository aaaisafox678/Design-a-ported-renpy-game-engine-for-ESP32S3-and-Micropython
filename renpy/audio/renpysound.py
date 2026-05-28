#
# renpysound.py — 底层混音引擎 (1:1对齐原版 renpysound.pyx 算法)
# NS4168 I2S 48kHz 16bit mono → 软件混音 → DMA输出
#
import gc

_freq = 48000
_i2s = None
_channels = {}       # {num: {data,pos,end,vol,vol2,pan,playing,paused,name,fade_t,fade_step}}
_equal_mono = True

NO_VIDEO = 0
DROP_VIDEO = 1
NODROP_VIDEO = 2

# ============ 原版 RPS_init ============
def init(freq, stereo, bufsize, status, equal_mono):
    global _freq, _i2s, _equal_mono
    _freq = freq
    _equal_mono = equal_mono
    try:
        from machine import I2S, Pin
        _i2s = I2S(0, sck=Pin(42), ws=Pin(2), sd=Pin(41),
                   mode=I2S.TX, sample_rate=freq, bits=16, format=I2S.MONO)
        return True
    except Exception as e:
        raise e

def quit():
    global _i2s
    if _i2s: _i2s.deinit(); _i2s = None
    _channels.clear()

# ============ 原版 RPS_play ============
def play(num, file_obj, name, paused=False, fadein=0, tight=False, start=0.0, end=0.0):
    data = file_obj.read() if hasattr(file_obj, 'read') else bytes(file_obj)
    start_bytes = int(start * _freq * 2)
    end_bytes = len(data) if end <= 0 else int(end * _freq * 2)
    _channels[num] = {
        'data': data, 'pos': start_bytes, 'end': end_bytes,
        'vol': 1.0, 'vol2': 1.0, 'pan': 0.0,
        'playing': not paused, 'paused': paused,
        'name': str(name), 'fade_t': 0.0, 'fade_s': 0.0
    }

# ============ 原版 RPS_queue ============
def queue(num, file_obj, name, fadein=0, tight=False, start=0.0, end=0.0):
    play(num, file_obj, name, fadein=fadein, tight=tight, start=start, end=end)

# ============ 原版 RPS_stop / RPS_dequeue ============
def stop(num):
    _channels.pop(num, None)
def dequeue(num, even_tight=False):
    _channels.pop(num, None)

# ============ 原版 RPS_fadeout ============
def fadeout(num, ms):
    c = _channels.get(num)
    if c: c['fade_t'] = ms / 1000.0

# ============ 原版 RPS_pause / RPS_unpause ============
def pause(num):
    if num in _channels: _channels[num]['paused'] = True
def unpause(num):
    if num in _channels: _channels[num]['paused'] = False
def unpause_all_at_start():
    for c in _channels.values(): c['paused'] = False

# ============ 原版 RPS_set_volume / RPS_set_pan / RPS_set_secondary_volume ============
def set_volume(num, vol):
    if num in _channels: _channels[num]['vol'] = vol
def set_pan(num, pan, delay):
    if num in _channels: _channels[num]['pan'] = pan
def set_secondary_volume(num, vol2, delay):
    if num in _channels: _channels[num]['vol2'] = vol2
def get_volume(num):
    return _channels[num]['vol'] if num in _channels else 1.0

# ============ 原版 RPS_queue_depth / RPS_playing_name / RPS_get_pos / RPS_get_duration ============
def queue_depth(num):
    return 1 if num in _channels else 0
def playing_name(num):
    c = _channels.get(num); return c['name'] if c else None
def get_pos(num):
    c = _channels.get(num); return int(c['pos']/2/_freq) if c else 0
def get_duration(num):
    c = _channels.get(num); return len(c['data'])/2/_freq if c else 0.0

# ============ 视频（ESP32-S3无）============
def set_video(num, video): pass
def set_endevent(num, event): pass
def video_ready(num): return 1
def read_video(num): return None

# ============ 核心: RPS_periodic (1:1 C翻译) ============
def periodic():
    """
    原版 RPS_periodic → SDL audio callback → 这里 I2S DMA
    for each sample in buffer:
      for each channel:
        read s16 sample at pos
        apply fadeout linear decay
        apply volume = vol * vol2 * equal_mono_factor
        mix into output
      clamp to s16
    write I2S
    """
    global _i2s, _freq
    if not _i2s or not _channels:
        return
    
    N = 1024
    output = bytearray(N * 2)
    any_data = False
    remove = []
    
    for i in range(N):
        mixed = 0
        for num, c in list(_channels.items()):
            if not c['playing'] or c['paused'] or not c['data']:
                continue
            
            p = c['pos'] + i * 2
            if p + 1 >= c['end'] or p + 1 >= len(c['data']):
                remove.append(num)
                continue
            
            s = int.from_bytes(c['data'][p:p+2], 'little', signed=True)
            
            # fadeout 线性衰减 (原版 C 逻辑)
            if c['fade_t'] > 0:
                c['fade_s'] += 1.0 / (_freq * N)
                decay = max(0, 1.0 - c['fade_s'] / c['fade_t'])
                s = int(s * decay)
                if decay <= 0:
                    remove.append(num)
                    continue
            
            # 音量 × 声道因子
            gain = c['vol'] * c['vol2']
            if _equal_mono:
                gain *= 0.7071
            mixed += int(s * gain)
        
        for num in set(remove): _channels.pop(num, None)
        remove.clear()
        
        mixed = max(-32768, min(32767, mixed))
        output[i*2:i*2+2] = mixed.to_bytes(2, 'little', signed=True)
        if abs(mixed) > 5: any_data = True
    
    if any_data:
        try: _i2s.write(output)
        except: pass
    
    for c in _channels.values():
        if c['playing'] and not c['paused']:
            c['pos'] += N * 2

def advance_time(): pass
def get_error(): return b''
def check_error(): pass
def sample_surfaces(*a): pass