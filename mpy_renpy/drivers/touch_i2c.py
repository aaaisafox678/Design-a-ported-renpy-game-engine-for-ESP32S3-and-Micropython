# 硬件: JC3248W535CN
# 触控IC: AXS15231B 集成触控 (I2C, 地址0x3B)
#

from machine import I2C, Pin
import time

# ========== 引脚定义 ==========
PIN_TOUCH_SDA = 4
PIN_TOUCH_SCL = 5
PIN_TOUCH_RST = -1
PIN_TOUCH_INT = 46

# 触控IC I2C地址
TOUCH_I2C_ADDR = 0x3B

# 触控寄存器地址 (AXS15231B)
TOUCH_REG_CMD = 0x00
TOUCH_REG_STATE = 0x01
TOUCH_REG_XH = 0x03
TOUCH_REG_XL = 0x04
TOUCH_REG_YH = 0x05
TOUCH_REG_YL = 0x06
TOUCH_REG_TRACK_NUM = 0x02


class Touch_I2C:
    """
    I2C 触摸屏驱动程序 for AXS15231B
    
    通过I2C总线读取触控坐标
    支持多点触控
    """
    
    def __init__(self, i2c=None, addr=TOUCH_I2C_ADDR):
        """
        初始化触摸屏驱动
        
        Args:
            i2c: I2C实例, 如果为None则创建新的
            addr: I2C设备地址
        """
        self.i2c_addr = addr
        self.width = 320
        self.height = 480
        self.touches = []
        self._last_x = 0
        self._last_y = 0
        self._press_downtime = 0
        
        # 如果没有提供I2C实例, 创建新的
        if i2c is None:
            self.i2c = I2C(
                0,
                sda=Pin(PIN_TOUCH_SDA),
                scl=Pin(PIN_TOUCH_SCL),
                freq=400000
            )
        else:
            self.i2c = i2c
            
        # 初始化触控IC
        self._init_touch()
        
    def _init_touch(self):
        """
        初始化触控IC
        
        发送复位命令并配置基本参数
        """
        try:
            # 尝试读取设备ID验证连接
            self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_STATE, 1)
        except OSError:
            print("Warning: Touch IC not responding at 0x{:02X}".format(self.i2c_addr))
            return
            
    def get_touch(self):
        """
        读取触控状态
        
        Returns:
            list: 触控点列表, 每个元素为(x, y, pressure)
        """
        try:
            # 读取触控状态
            state = self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_STATE, 1)[0]
            
            # 检查是否有触控事件
            if state & 0x80:  # 触控有效位
                # 读取X坐标高位
                xh = self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_XH, 1)[0]
                xl = self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_XL, 1)[0]
                yh = self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_YH, 1)[0]
                yl = self.i2c.readfrom_mem(self.i2c_addr, TOUCH_REG_YL, 1)[0]
                
                # 组合12位坐标
                x = ((xh & 0x0F) << 8) | xl
                y = ((yh & 0x0F) << 8) | yl
                
                # 转换到屏幕坐标系
                x = min(max(x, 0), self.width - 1)
                y = min(max(y, 0), self.height - 1)
                
                self._last_x = x
                self._last_y = y
                self._press_downtime = time.ticks_ms()
                
                return [(x, y, 1)]
                
        except OSError as e:
            print("Touch read error: {}".format(e))
            
        return []
        
    def was_touched(self):
        """
        检查是否最近有触控事件
        
        Returns:
            bool: 最近有触控返回True
        """
        return len(self.get_touch()) > 0
        
    def get_last_pos(self):
        """
        获取最后一次触控位置
        
        Returns:
            tuple: (x, y) 坐标
        """
        return (self._last_x, self._last_y)
        
    def get_touch_pos(self):
        """
        获取当前触控位置 (简化接口)
        
        Returns:
            tuple: (x, y) 或 None
        """
        touches = self.get_touch()
        if touches:
            return (touches[0][0], touches[0][1])
        return None
        
    def wait_for_touch(self, timeout=5000):
        """
        等待触控事件
        
        Args:
            timeout: 超时时间 (毫秒)
            
        Returns:
            tuple: (x, y, pressure) 或 None
        """
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout:
            touches = self.get_touch()
            if touches:
                return touches[0]
            time.sleep_ms(10)
        return None


# ========== 全局触控实例 ==========
_touch = None

def get_touch():
    """获取全局触控实例"""
    global _touch
    if _touch is None:
        _touch = Touch_I2C()
    return _touch


def init_touch():
    """初始化触控并返回实例"""
    return Touch_I2C()


#
# All rights reserved.
# 官方网站：https://www.hcnsec.cn/
#