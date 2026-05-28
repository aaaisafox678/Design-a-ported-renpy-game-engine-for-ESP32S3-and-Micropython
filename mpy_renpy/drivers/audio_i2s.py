# 硬件: JC3248W535CN
# 音频IC: NS4168 单声道D类功放, I2S输入, 2.5W@4Ω
# 特性:
#   - I2S 数字音频输入 (BCLK延迟1个时钟)
#   - 内置DAC
#   - 采样率: 8kHz - 96kHz
#   - 无需MCLK
#   - CTRL引脚设置左右声道
#   - 防失真NCN功能
#   - 无需输出滤波器

from machine import I2S, Pin
import time

# ========== NS4168 引脚定义 ==========
# ESP32-S3 I2S引脚 (可根据实际板子修改)
PIN_I2S_BCLK = 7
PIN_I2S_LRCLK = 6
PIN_I2S_DATA = 15

# NS4168 规格
NS4168_SAMPLE_RATE = 48000  # 48kHz (支持8k-96kHz)
NS4168_BITS = 16            # 16位采样
NS4168_CHANNELS = 1         # 单声道
NS4168_POWER = 2.5          # 2.5W @ 4Ω, 5V

# I2S格式 (对齐NS4168要求)
# NS4168: BCLK延迟一个时钟的I2S格式

class Audio_NS4168:
    """
    NS4168 I2S 音频驱动
    
    支持:
    - 2.5W D类功放输出
    - I2S数字音频输入
    - 内置防失真NCN
    - 采样率 8kHz-96kHz
    """
    
    def __init__(self, sample_rate=NS4168_SAMPLE_RATE, bits=NS4168_BITS):
        self.sample_rate = sample_rate
        self.bits = bits
        self._is_playing = False
        self._volume = 1.0
        
        try:
            self.i2s = I2S(
                0,
                sck=Pin(PIN_I2S_BCLK),
                ws=Pin(PIN_I2S_LRCLK),
                sd=Pin(PIN_I2S_DATA),
                mode=I2S.TX,
                sample_rate=sample_rate,
                bits=bits,
                format=I2S.MONO,
            )
            print("NS4168 Audio initialized: {}Hz, {}bit".format(sample_rate, bits))
        except Exception as e:
            print("NS4168 init failed: {}".format(e))
            self.i2s = None
    
    def play_sound(self, filepath):
        """播放音效"""
        if not self.i2s:
            return
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                self.i2s.write(data)
        except:
            pass
    
    def play_music(self, filepath, loop=False):
        """播放背景音乐"""
        self.play_sound(filepath)
    
    def play_voice(self, filepath):
        """播放语音"""
        self.play_sound(filepath)
    
    def stop(self, channel=None):
        """停止所有音频"""
        self._is_playing = False
        if self.i2s:
            self.i2s.deinit()
    
    def set_volume(self, vol):
        self._volume = max(0.0, min(1.0, vol))
    
    def get_volume(self):
        return self._volume