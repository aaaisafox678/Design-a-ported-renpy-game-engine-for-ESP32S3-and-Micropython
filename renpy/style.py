# MicroPython shim for renpy/style.pyx
import renpy
styles = {}
style_properties = {}
prefix_priority = {}
index = 0
def get_style(name):
    nametuple = (name,)
    rv = styles.get(nametuple)
    if rv is not None:
        return rv
    start, _mid, end = name.partition("_")
    if not end:
        raise Exception("Style %r does not exist." % name)
    if not start:
        _start, _mid, end = name[1:].partition("_")
        if not end:
            raise Exception("Style %r does not exist." % name)
        end = "_" + end
    try:
        parent = get_style(end)
    except:
        raise Exception("Style %r does not exist." % name)
    rv = Style(parent, name=nametuple)
    styles[nametuple] = rv
    return rv

class StyleCore:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.properties = {}
        self.index = 0

class Style(StyleCore):
    def __init__(self, parent=None, name=None):
        super().__init__(parent, name)
    def __getattr__(self, name):
        if name in self.properties:
            return self.properties[name]
        if self.parent:
            return getattr(self.parent, name, None)
        return None
    def __setattr__(self, name, value):
        if name in ('parent','name','properties','index'):
            super().__setattr__(name, value)
        else:
            self.properties[name] = value
    def add_prefix(self, prefix, priority):
        pass
    def resolve_prefix(self, prefix):
        return self
    def inspect(self):
        return {}
    def clear(self):
        self.properties = {}

def reset():
    global styles
    styles = {}
    default = Style(name=('default',))
    styles[('default',)] = default
    styles[('say_label',)] = Style(default, name=('say_label',))
    styles[('say_dialogue',)] = Style(default, name=('say_dialogue',))
    styles[('say_window',)] = Style(default, name=('say_window',))
    styles[('button',)] = Style(default, name=('button',))
    styles[('button_text',)] = Style(default, name=('button_text',))

reset()

# 模拟 Cython 的 style.pxd 导出
def define_style(name, parent='default'):
    p = get_style(parent) if parent in styles else get_style('default')
    s = Style(p, name=(name,))
    styles[(name,)] = s
    return s