import sys
def find_module(name, path=None): return None
def load_module(name, file, pathname, description): raise ImportError(name)
def new_module(name): return type(sys)(name)
def lock_held(): return False
def acquire_lock(): pass
def release_lock(): pass
def get_magic(): return b""
