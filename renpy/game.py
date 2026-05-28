"""MicroPython shim: game"""
class Game:
    def __init__(self): pass
_contexts = []
_game = Game()
def context(i): return _game
