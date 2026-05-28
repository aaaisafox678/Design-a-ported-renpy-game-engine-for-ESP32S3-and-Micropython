"""MicroPython shim: scale"""
def real_bounds(w,h,rw,rh): return (0,0,w,h)
def scale(w,h,rw,rh): return (rw,rh)
