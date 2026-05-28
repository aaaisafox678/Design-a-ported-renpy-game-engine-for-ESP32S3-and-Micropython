import sys,os
sys.path.insert(0,'.')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
sys.modules['machine']=type(sys)('machine')
sys.modules['machine'].I2S=type('I2S',(),{'__init__':lambda*_:None,'write':lambda*_:None,'deinit':lambda*_:None})
sys.modules['machine'].Pin=type('Pin',(),{})
import renpy.imp; sys.modules['imp']=renpy.imp
import renpy
print('character:',hasattr(renpy,'character'))
print('store:',hasattr(renpy,'store'))
import renpy.loadsave
print('loadsave OK')