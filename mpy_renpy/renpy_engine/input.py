import drivers.touch_i2c as touch_driver
import time


class InputHandler:
    """输入处理器 - 对齐 RenPy 的输入系统"""
    
    def __init__(self):
        self._touch = touch_driver.Touch_I2C()
        self._last_touch = None
        self._click_count = 0
    
    def get_touch(self):
        """获取当前触控位置"""
        pos = self._touch.get_touch_pos()
        self._last_touch = pos
        return pos
    
    def wait_for_click(self, timeout=10000):
        """等待点击"""
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout:
            pos = self.get_touch()
            if pos:
                self._click_count += 1
                return pos
            time.sleep_ms(10)
        return None
    
    def was_clicked(self):
        """检查是否有点击"""
        return self.get_touch() is not None
    
    def get_click_count(self):
        return self._click_count


_input = None

def get_input():
    global _input
    if _input is None:
        _input = InputHandler()
    return _input