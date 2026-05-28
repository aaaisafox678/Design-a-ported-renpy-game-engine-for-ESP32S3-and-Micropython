import sys,os
sys.path.insert(0,'.')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
sys.modules['machine']=type(sys)('machine')
sys.modules['machine'].I2S=type('I2S',(),{'__init__':lambda*_:None,'write':lambda*_:None,'deinit':lambda*_:None})
sys.modules['machine'].Pin=type('Pin',(),{})
import renpy
print('version:',renpy.version_only)
print('screen:',renpy.config.screen_width,renpy.config.screen_height)
print('character:',hasattr(renpy,'character'))
print('audio:',hasattr(renpy,'audio'))
print('display:',hasattr(renpy,'display'))
print('store:',hasattr(renpy,'store'))
print('ALL GOOD')