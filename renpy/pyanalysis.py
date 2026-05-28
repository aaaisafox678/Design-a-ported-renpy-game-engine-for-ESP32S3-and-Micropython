"""MicroPython shim: pyanalysis"""
GLOBAL_CONST = 0
pure_functions=set()
def pure(fn): return fn
class Analysis:
    def is_constant_expr(self, *a): return False
    def is_pure(self, *a): return False
