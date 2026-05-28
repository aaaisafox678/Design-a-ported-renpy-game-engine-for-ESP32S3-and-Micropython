# MicroPython shim
style_functions = {}
def register_style_function(name,fn):
    style_functions[name]=fn
