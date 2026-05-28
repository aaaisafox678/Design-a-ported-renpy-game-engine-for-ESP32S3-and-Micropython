import os
import gc


class ScriptParser:
    """
    RenPy风格脚本解析器
    
    解析类似RenPy的脚本文件, 将其转换为引擎可执行的动作序列
    """
    
    def __init__(self):
        """初始化解析器"""
        self._statements = []  # 解析后的语句列表
        self._current_label = None
        self._labels = {}      # 标签映射
        self._current_line = 0
        
    def parse(self, script_text):
        """
        解析脚本文本
        
        Args:
            script_text: 脚本文本内容
            
        Returns:
            语句列表
        """
        self._statements = []
        lines = script_text.split('\n')
        
        for i, line in enumerate(lines):
            self._current_line = i
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
                
            # 解析标签
            if line.endswith(':') and line.startswith('label '):
                label_name = line[6:].strip()
                self._labels[label_name] = len(self._statements)
                continue
                
            # 解析jump语句
            if line.startswith('jump '):
                self._statements.append({
                    'type': 'jump',
                    'label': line[5:].strip()
                })
                continue
                
            # 解析return语句
            if line == 'return':
                self._statements.append({'type': 'return'})
                continue
                
            # 解析show语句
            if line.startswith('show '):
                stmt = self._parse_show(line)
                if stmt:
                    self._statements.append(stmt)
                continue
                    
            # 解析scene语句
            if line.startswith('scene '):
                stmt = self._parse_scene(line)
                if stmt:
                    self._statements.append(stmt)
                continue
                    
            # 解析对话语句
            if '"' in line or "'" in line:
                stmt = self._parse_dialogue(line)
                if stmt:
                    self._statements.append(stmt)
                continue
                
            # 解析play语句
            if line.startswith('play '):
                stmt = self._parse_play(line)
                if stmt:
                    self._statements.append(stmt)
                continue
                    
            # 解析with语句(过渡)
            if line.startswith('with '):
                self._statements.append({
                    'type': 'transition',
                    'effect': line[5:].strip()
                })
                continue
                
            # 解析if/elif/else条件
            if line.startswith('if ') or line.startswith('elif '):
                self._statements.append({
                    'type': 'condition',
                    'condition': line
                })
                continue
                
            # 解析choice选择
            if line.startswith('"') and ':' in line:
                stmt = self._parse_choice(line)
                if stmt:
                    self._statements.append(stmt)
                continue
                    
            # 解析label标记
            if line.startswith('label '):
                label_name = line[6:].strip()
                self._labels[label_name] = len(self._statements)
                continue
                
        return self._statements
    
    def _parse_show(self, line):
        """解析show语句"""
        parts = line[5:].split()
        if len(parts) >= 2:
            return {
                'type': 'show',
                'character': parts[0],
                'image': parts[1] if len(parts) > 1 else None
            }
        return None
        
    def _parse_scene(self, line):
        """解析scene语句"""
        parts = line[6:].split()
        if parts:
            return {
                'type': 'scene',
                'background': parts[0] if parts else None
            }
        return None
        
    def _parse_dialogue(self, line):
        """解析对话语句"""
        # 格式: character "dialogue"
        # 或: "dialogue" (无说话人)
        parts = line.split('"')
        if len(parts) >= 2:
            speaker = parts[0].strip() if parts[0].strip() else None
            text = parts[1] if len(parts) > 1 else ''
            
            return {
                'type': 'dialogue',
                'speaker': speaker,
                'text': text
            }
        return None
        
    def _parse_play(self, line):
        """解析play语句"""
        parts = line[5:].split()
        if len(parts) >= 2:
            return {
                'type': 'play',
                'kind': parts[0],
                'file': parts[1]
            }
        return None
        
    def _parse_choice(self, line):
        """解析choice语句"""
        # 格式: "选项文本":
        parts = line.split('"')
        if len(parts) >= 2:
            text = parts[1]
            return {
                'type': 'choice',
                'text': text
            }
        return None
        
    def execute(self, statements):
        """
        执行语句列表
        
        Args:
            statements: 语句列表
            
        Returns:
            执行结果
        """
        for stmt in statements:
            yield stmt
            
    def load_script(self, filepath):
        """
        从文件加载并解析脚本
        
        Args:
            filepath: 脚本文件路径
            
        Returns:
            解析后的语句列表
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse(content)
        except (IOError, UnicodeDecodeError) as e:
            print("Failed to load script: {}".format(e))
            return []
            
    def get_labels(self):
        """获取所有标签"""
        return dict(self._labels)
        
    def find_label(self, label_name):
        """
        查找标签位置
        
        Args:
            label_name: 标签名称
            
        Returns:
            语句索引或-1
        """
        return self._labels.get(label_name, -1)


# 便捷函数
def parse_script(script_text):
    """解析脚本文本"""
    parser = ScriptParser()
    return parser.parse(script_text)

def load_script(filepath):
    """从文件加载脚本"""
    parser = ScriptParser()
    return parser.load_script(filepath)


#
# All rights reserved.
# 官方网站：https://www.hcnsec.cn/
#