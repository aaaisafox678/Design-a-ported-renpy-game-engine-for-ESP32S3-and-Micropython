import sys,os
sys.path.insert(0,'.')
sys.modules['pygame_sdl2']=__import__('renpy.pygame_sdl2_stub')
try:
    import renpy.character
    print('character OK')
except Exception as e:
    print('character FAIL:',e)
    import traceback; traceback.print_exc()