# Micro-RenPy 冻结模块清单
# 这些模块将被编译为bytecode并冻结到firmware中

import micropython

# 硬件驱动
upip_import("machine")
upip_import("time")
upip_import("framebuf")

# RenPy引擎核心模块
# module("mpy_renpy/drivers/lcd_qspi")
# module("mpy_renpy/drivers/touch_i2c")
# module("mpy_renpy/drivers/audio_i2s")
# module("mpy_renpy/drivers/sdcard")

# RenPy引擎
# module("mpy_renpy/renpy_engine/__init__")
# module("mpy_renpy/renpy_engine/script")
# module("mpy_renpy/renpy_engine/scene")
# module("mpy_renpy/renpy_engine/character")
# module("mpy_renpy/renpy_engine/display")
# module("mpy_renpy/renpy_engine/audio")
# module("mpy_renpy/renpy_engine/input")
# module("mpy_renpy/renpy_engine/transition")
