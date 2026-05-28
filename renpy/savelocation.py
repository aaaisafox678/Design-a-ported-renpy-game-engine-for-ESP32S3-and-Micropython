"""MicroPython shim: savelocation"""
def init(): pass
def get_save_files(): return []
def get_save_path(slot): return '/sdcard/saves/slot%d'%slot
