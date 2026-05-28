import time
import os
import gc

# 尝试导入硬件驱动
try:
    from drivers.lcd_qspi import LCD_QSPI, COLOR_BLACK, COLOR_WHITE, COLOR_GRAY
    LCD_AVAILABLE = True
except ImportError:
    LCD_AVAILABLE = False
    
try:
    from drivers.touch_i2c import Touch_I2C
    TOUCH_AVAILABLE = True
except ImportError:
    TOUCH_AVAILABLE = False


class Display:
    """
    显示渲染器
    
    负责将RenPy引擎的场景、角色、对话框绘制到屏幕
    使用LVGL或framebuf进行渲染
    """
    
    def __init__(self, width=320, height=480):
        """
        初始化显示器
        
        Args:
            width: 屏幕宽度
            height: 屏幕高度
        """
        self.width = width
        self.height = height
        self._lcd = None
        self._touch = None
        self._text_buf = bytearray(4096)  # 文本缓冲区
        self._dirty = True
        self._dialogue_box = {
            'y': 320,      # 对话框起始Y坐标
            'height': 160, # 对话框高度
            'bg_color': 0x0000,
            'text_color': 0xFFFF,
            'font_size': 1
        }
        
        if LCD_AVAILABLE:
            self._lcd = LCD_QSPI()
        if TOUCH_AVAILABLE:
            self._touch = Touch_I2C()
            
    def _ensure_lcd(self):
        """确保LCD已初始化"""
        if self._lcd is None and LCD_AVAILABLE:
            self._lcd = LCD_QSPI()
            
    def clear(self):
        """清空屏幕"""
        self._ensure_lcd()
        if self._lcd:
            self._lcd.fill(COLOR_BLACK)
            self._lcd.show()
        self._dirty = False
        
    def draw_text(self, text, x=10, y=330, color=None, size=1):
        """
        绘制文本
        
        Args:
            text: 要显示的文本
            x: X坐标
            y: Y坐标
            color: 文本颜色
            size: 字体大小
        """
        self._ensure_lcd()
        # 简化: 使用framebuf绘制
        # 实际需要使用LVGL或自定义字体渲染
        pass
        
    def draw_dialogue_box(self, speaker='', text=''):
        """
        绘制对话框
        
        Args:
            speaker: 说话人名称
            text: 对话内容
        """
        self._ensure_lcd()
        if not self._lcd:
            return
            
        db = self._dialogue_box
        box_y = db['y']
        box_h = db['height']
        
        # 绘制对话框背景
        self._lcd.fill_rect(0, box_y, self.width, box_h, 0x0000)
        self._lcd.rect(2, box_y + 2, self.width - 4, box_h - 4, 0x8410)
        
        # 绘制说话人名称 (如果有)
        if speaker:
            # 简化的名称显示
            pass
            
        # 绘制对话文本
        if text:
            # 需要实现文本换行和绘制
            # 这里使用简化方法
            pass
            
        self._dirty = True
        
    def draw_background(self, image_path):
        """
        绘制背景图片
        
        Args:
            image_path: 图片文件路径
        """
        self._ensure_lcd()
        if not self._lcd:
            return
            
        try:
            # 尝试加载并绘制图片
            # 支持PNG/JPG格式
            # 由于资源限制, 图片需要预缩放
            with open(image_path, 'rb') as f:
                data = f.read()
                # 图片绘制需要专门的解码器
                # 这里简化处理
        except (IOError, OSError):
            # 文件不存在, 用纯色背景
            self._lcd.fill_rect(0, 0, self.width, 320, 0x1B5E20)
            
    def draw_sprite(self, image_path, x=0, y=0):
        """
        绘制角色精灵
        
        Args:
            image_path: 角色图片路径
            x: X坐标
            y: Y坐标
        """
        self._ensure_lcd()
        # 简化处理
        pass
        
    def update(self):
        """更新显示"""
        if self._dirty and self._lcd:
            self._lcd.show()
            self._dirty = False
            
    def wait_for_input(self, timeout=10000):
        """
        等待用户输入
        
        Args:
            timeout: 超时时间 (毫秒)
            
        Returns:
            tuple: (x, y) 触控坐标, 无触控返回None
        """
        if not self._touch:
            time.sleep_ms(100)
            return None
            
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout:
            pos = self._touch.get_touch_pos()
            if pos:
                return pos
            time.sleep_ms(10)
        return None
        
    def get_touch_pos(self):
        """
        获取当前触控位置
        
        Returns:
            tuple: (x, y) 或 None
        """
        if self._touch:
            return self._touch.get_touch_pos()
        return None
        
    def draw_choice(self, choices, x=20, y_start=340):
        """
        绘制选项列表
        
        Args:
            choices: 选项列表
            x: 起始X坐标
            y_start: 起始Y坐标
            
        Returns:
            选择的索引, -1表示超时
        """
        self._ensure_lcd()
        selected = -1
        
        for i, choice in enumerate(choices):
            y = y_start + i * 30
            # 绘制选项背景
            self._lcd.fill_rect(x, y, self.width - x - 20, 28, 0x0000)
            self._lcd.rect(x, y, self.width - x - 20, 28, 0x07E0)
            
            # 绘制选项文本
            pass
            
        return selected
        
    def transition(self, effect='dissolve', duration=500):
        """
        场景过渡效果
        
        Args:
            effect: 效果类型 ('dissolve', 'fade', 'push')
            duration: 持续时间 (毫秒)
        """
        if effect == 'fade':
            # 淡入淡出效果
            if self._lcd:
                self._lcd.fill(COLOR_BLACK)
                self._lcd.show()
                time.sleep_ms(duration // 2)
                self._lcd.fill(COLOR_WHITE)
                self._lcd.show()
                time.sleep_ms(duration // 2)
        elif effect == 'dissolve':
            # 溶解效果 (简化)
            time.sleep_ms(duration)
            
    def info(self):
        """获取显示信息"""
        info = {
            'resolution': (self.width, self.height),
            'lcd': self._lcd is not None,
            'touch': self._touch is not None
        }
        gc.collect()
        info['free_memory'] = gc.mem_free()
        return info


# 全局显示实例
_display = None

def get_display():
    """获取全局显示实例"""
    global _display
    if _display is None:
        _display = Display()
    return _display

def init_display():
    """初始化显示并返回实例"""
    return Display()


#
# All rights reserved.
# 官方网站：https://www.hcnsec.cn/
#