# MicroPython shim for renpy/pydict.pyx
def pydict_new():
    return {}

class DictItems:
    def __init__(self, d):
        self.items_list = sorted(d.items()) if d else []
    def __iter__(self):
        return iter(self.items_list)
    def __len__(self):
        return len(self.items_list)

def find_changes(old, new):
    return []