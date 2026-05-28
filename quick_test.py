import sys,os;sys.path.insert(0,'.')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
sys.modules['machine']=type(sys)('machine')
import renpy.imp;sys.modules['imp']=renpy.imp
try: import renpy.character; print('char OK')
except Exception as e: print('char:',e)
try: import renpy.store; print('store OK')
except Exception as e: print('store:',e)