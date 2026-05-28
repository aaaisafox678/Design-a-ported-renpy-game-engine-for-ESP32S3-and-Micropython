import os
import gc


class Scene:
    """
    场景对象
    
    表示视觉小说中的一个场景，包含背景、角色、特效等元素
    """
    
    def __init__(self, name, background=None):
        """
        初始化场景
        
        Args:
            name: 场景名称
            background: 背景图片路径
        """
        self.name = name
        self.background = background
        self.sprites = []      # 当前显示的角色/图像
        self.dialogue_text = ""
        self.music = None
        self.sfx = None
        self.variables = {}     # 场景局部变量
        
    def set_background(self, image_path):
        """设置背景图片"""
        self.background = image_path
        
    def add_sprite(self, sprite):
        """添加精灵(角色/图像)到场景"""
        self.sprites.append(sprite)
        
    def remove_sprite(self, name):
        """移除指定名称的精灵"""
        self.sprites = [s for s in self.sprites if s.name != name]
        
    def get_sprites(self):
        """获取所有精灵"""
        return self.sprites
    
    def clear(self):
        """清空场景"""
        self.sprites = []
        self.background = None
        self.dialogue_text = ""


class SceneManager:
    """
    场景管理器
    
    管理场景切换、当前场景状态、场景栈
    """
    
    def __init__(self):
        """初始化管理器"""
        self._scenes = {}           # 已加载的场景
        self._current_scene = None  # 当前场景
        self._scene_stack = []      # 场景栈 (用于后退)
        self._variables = {}        # 全局变量
        self._flags = {}            # 标记变量
        
    def register_scene(self, scene):
        """
        注册一个场景
        
        Args:
            scene: Scene对象
        """
        self._scenes[scene.name] = scene
        
    def load_scene(self, name):
        """
        加载场景
        
        Args:
            name: 场景名称
            
        Returns:
            Scene对象或None
        """
        if name not in self._scenes:
            print("Scene '{}' not found".format(name))
            return None
            
        # 保存当前场景到栈
        if self._current_scene:
            self._scene_stack.append(self._current_scene)
            
        self._current_scene = self._scenes[name]
        return self._current_scene
        
    def get_current_scene(self):
        """获取当前场景"""
        return self._current_scene
    
    def pop_scene(self):
        """
        从栈中弹出上一个场景
        
        Returns:
            上一个场景或None
        """
        if self._scene_stack:
            prev = self._scene_stack.pop()
            self._current_scene = prev
            return prev
        return None
    
    def go_back(self):
        """返回上一个场景"""
        prev = self.pop_scene()
        if prev:
            return prev
        return None
    
    def set_variable(self, name, value):
        """设置全局变量"""
        self._variables[name] = value
        
    def get_variable(self, name, default=None):
        """
        获取全局变量
        
        Args:
            name: 变量名
            default: 默认值
            
        Returns:
            变量值或默认值
        """
        return self._variables.get(name, default)
        
    def set_flag(self, name, value=True):
        """设置标记变量"""
        self._flags[name] = value
        
    def clear_flag(self, name):
        """清除标记变量"""
        self._flags.pop(name, None)
        
    def check_flag(self, name):
        """
        检查标记变量
        
        Returns:
            标记值或False
        """
        return self._flags.get(name, False)
    
    def memory_info(self):
        """获取内存使用信息"""
        gc.collect()
        return {
            'free_heap': gc.mem_free(),
            'allocated': gc.mem_alloc(),
            'scenes_loaded': len(self._scenes),
            'current_scene': self._current_scene.name if self._current_scene else None
        }


# 全局场景管理器实例
_manager = None

def get_scene_manager():
    """获取全局场景管理器"""
    global _manager
    if _manager is None:
        _manager = SceneManager()
    return _manager

def register_scene(scene):
    """注册场景到全局管理器"""
    get_scene_manager().register_scene(scene)

def load_scene(name):
    """加载场景"""
    return get_scene_manager().load_scene(name)

def get_current_scene():
    """获取当前场景"""
    return get_scene_manager().get_current_scene()

def go_back():
    """返回上一个场景"""
    return get_scene_manager().pop_scene()


#
# All rights reserved.
# 官方网站：https://www.hcnsec.cn/
#