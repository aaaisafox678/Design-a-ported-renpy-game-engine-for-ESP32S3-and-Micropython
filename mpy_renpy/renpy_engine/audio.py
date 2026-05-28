import drivers.audio_i2s as audio_hw
import time


class AudioController:
    """
    音频控制器
    对齐 RenPy 的音频系统架构
    
    通道:
    - "audio"/"sfx": 音效
    - "music": 背景音乐  
    - "voice": 语音
    """
    
    def __init__(self):
        self._hw = audio_hw.Audio_NS4168()
        self._channels = {
            "audio": True,
            "music": True,
            "voice": True
        }
    
    def play_sound(self, filepath):
        """播放音效 (sfx channel)"""
        if self._channels.get("audio", True):
            self._hw.play_sound(filepath)
    
    def play_music(self, filepath, loop=False):
        """播放背景音乐 (music channel)"""
        if self._channels.get("music", True):
            self._hw.play_music(filepath, loop)
    
    def play_voice(self, filepath):
        """播放语音 (voice channel)"""
        if self._channels.get("voice", True):
            self._hw.play_voice(filepath)
    
    def stop(self, channel=None):
        """
        停止音频
        channel=None 则停止所有
        """
        self._hw.stop(channel)
    
    def mute(self, channel):
        """静音指定通道"""
        self._channels[channel] = False
    
    def unmute(self, channel):
        """取消静音"""
        self._channels[channel] = True


_audio = None

def get_audio():
    global _audio
    if _audio is None:
        _audio = AudioController()
    return _audio