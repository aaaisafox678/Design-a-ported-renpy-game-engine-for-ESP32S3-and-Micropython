import gc


class Character:
    """
    角色对象
    
    定义视觉小说中的一个角色, 包含姓名、对话框颜色、
    图像状态(表情)等信息
    """
    
    _registry = {}  # 角色注册表
    
    def __init__(self, name, color='#c8ffc8', image=None, images=None):
        """
        初始化角色
        
        Args:
            name: 角色显示名称
            color: 对话框颜色 (#RRGGBB)
            image: 默认图像路径
            images: 图像状态字典 {'happy': 'path/happy.png', 'sad': 'path/sad.png'}
        """
        self.name = name
        self.color = color
        self.default_image = image
        self.images = images or {}
        self.current_image = image
        self.current_state = 'default'
        
        # 注册到全局
        Character._registry[name] = self
        
    def set_image(self, state='default'):
        """
        设置角色图像状态
        
        Args:
            state: 状态名称 (如 'happy', 'sad')
        """
        if state in self.images:
            self.current_image = self.images[state]
            self.current_state = state
        elif state == 'default' and self.default_image:
            self.current_image = self.default_image
            self.current_state = 'default'
        
    def show(self, position='center'):
        """
        显示角色
        
        Args:
            position: 显示位置 ('left', 'center', 'right')
        """
        if self.current_image:
            pass  # 由渲染模块处理
            
    def hide(self):
        """隐藏角色"""
        self.current_image = None
        
    def get_color_hex(self):
        """
        获取颜色值作为整数
        
        Returns:
            整数值 0xRRGGBB
        """
        c = self.color
        if c.startswith('#'):
            return int(c[1:], 16)
        return 0xc8ffc8
        
    @classmethod
    def get_all(cls):
        """获取所有已注册角色"""
        return dict(cls._registry)
    
    @classmethod
    def get(cls, name):
        """
        获取已注册角色
        
        Args:
            name: 角色名称
            
        Returns:
            Character对象或None
        """
        return cls._registry.get(name)
    
    @classmethod
    def clear(cls):
        """清空所有角色注册"""
        cls._registry.clear()


class CharacterManager:
    """
    角色管理器
    
    管理游戏中所有角色的显示状态
    """
    
    def __init__(self):
        """初始化管理器"""
        self._displayed = {}  # 当前显示的角色: {name: position}
        self._max_sprites = 8  # 最大同时显示角色数
        
    def show_character(self, char, position='center'):
        """
        显示角色
        
        Args:
            char: Character对象
            position: 显示位置
        """
        if len(self._displayed) >= self._max_sprites:
            # 移除最早的角色
            oldest = next(iter(self._displayed))
            self.hide_character(oldest)
            
        self._displayed[char.name] = position
        char.show(position)
        
    def hide_character(self, name):
        """
        隐藏角色
        
        Args:
            name: 角色名称
        """
        char = Character.get(name)
        if char:
            char.hide()
            self._displayed.pop(name, None)
            
    def get_displayed(self):
        """获取当前显示的所有角色"""
        return dict(self._displayed)
        
    def clear_all(self):
        """隐藏所有角色"""
        for name in list(self._displayed.keys()):
            self.hide_character(name)


# 便捷函数
def Character(name, color='#c8ffc8', image=None, images=None):
    """
    创建角色 (RenPy风格的Character函数)
    
    Args:
        name: 角色名称
        color: 对话框颜色
        image: 默认图像路径
        images: 图像状态字典
        
    Returns:
        Character对象
        
    Example:
        e = Character('艾丽丝', color='#c8ffc8')
        d = Character('大卫', color='#ffc8c8')
    """
    return Character(name, color, image, images)


def show(char, position='center'):
    """显示角色"""
    if isinstance(char, Character):
        cm = CharacterManager()
        cm.show_character(char, position)
        
def hide(name):
    """隐藏角色"""
    if isinstance(name, str):
        cm = CharacterManager()
        cm.hide_character(name)


#
# All rights reserved.
# 官方网站：https://www.hcnsec.cn/
#