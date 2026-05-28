"""MicroPython shim: preferences"""
class Preferences:
    def __init__(self):
        self.text_cps=40
        self.afm_time=15
        self.afm_enable=False
        self.fullscreen=False
        self.language=None
        self.wait_voice=True
        self.voice_sustain=False
        self.virtual_size=None
        self.physical_size=None
    def set_volume(self,c,v): pass
    def get_volume(self,c): return 1.0
    def check(self): return None
_preferences=Preferences()
