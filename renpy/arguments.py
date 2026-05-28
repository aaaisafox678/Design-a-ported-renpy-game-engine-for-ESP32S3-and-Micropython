"""MicroPython shim: arguments"""
_ARGUMENTS = {}
def register_command(name, func): _ARGUMENTS[name]=func
def post_init(): pass
