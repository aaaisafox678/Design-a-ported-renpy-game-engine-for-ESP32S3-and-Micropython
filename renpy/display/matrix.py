#
# MicroPython shim: matrix.pyx → matrix.py
# 4x4 矩阵 - 对齐 Ren'Py 7.4.11 Matrix API
#

class Matrix:
    __slots__ = ('_m',)
    
    def __init__(self, l=None):
        self._m = [0.0]*16
        self._m[0] = self._m[5] = self._m[10] = self._m[15] = 1.0
        if l is not None:
            self._load(l)

    def _load(self, l):
        if len(l) == 4:
            self._m[0], self._m[1], self._m[4], self._m[5] = [float(v) for v in l]
        elif len(l) == 9:
            for i, v in enumerate(l):
                self._m[(i//3)*4 + (i%3)] = float(v)
        elif len(l) == 16:
            self._m = [float(v) for v in l]

    def __mul__(self, other):
        if isinstance(other, Matrix):
            r = Matrix()
            for i in range(4):
                for j in range(4):
                    s = 0.0
                    for k in range(4):
                        s += self._m[i*4+k] * other._m[k*4+j]
                    r._m[i*4+j] = s
            return r
        return other

    def __getitem__(self, idx):
        return self._m[idx]

    def __setitem__(self, idx, val):
        self._m[idx] = float(val)

    def __repr__(self):
        return "Matrix({0})".format(self._m)

    def inverse(self):
        return Matrix()

    @staticmethod
    def identity():
        return Matrix()

    @staticmethod
    def perspective(width, height, near, far, fov):
        return Matrix()

    @staticmethod
    def screen(width, height):
        return Matrix()

    @staticmethod
    def ortho(left, right, bottom, top, near, far):
        return Matrix()

    @staticmethod
    def translate(x, y, z):
        m = Matrix()
        m._m[3] = float(x)
        m._m[7] = float(y)
        m._m[11] = float(z)
        return m

    @staticmethod
    def rotate(x, y, z):
        return Matrix()

    @staticmethod
    def scale(x, y, z):
        m = Matrix()
        m._m[0] = float(x)
        m._m[5] = float(y)
        m._m[10] = float(z)
        return m

    @staticmethod
    def color(c):
        return Matrix()

    @staticmethod
    def brightness(b):
        return Matrix()

    @staticmethod
    def saturation(level, desat=None):
        return Matrix()

    @staticmethod
    def hue(h):
        return Matrix()

    @staticmethod
    def tint(color):
        return Matrix()

    @staticmethod
    def invert_alpha():
        return Matrix()

    @staticmethod
    def opacity(o):
        return Matrix()