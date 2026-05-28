"""MicroPython shim: curry"""
class Curry:
    def __init__(s,fn): s.fn=fn
    def __call__(s,*a,**k):
        def call(*a2,**k2):
            return s.fn(*(a+a2),**dict(list(k.items())+list(k2.items())))
        return call
def curry(fn): return Curry(fn)
