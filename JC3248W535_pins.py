#
# JC3248W535CN 引脚定义（基于官方 Demo pincfg.h 验证）
# 来源: /storage/emulated/0/JC3248W535CN/1-Demo/Demo_Arduino/DEMO_MP3/pincfg.h
#

# === LCD QSPI (AXS15231B) ===
TFT_CS   = 45
TFT_SCK  = 47
TFT_D0   = 21
TFT_D1   = 48
TFT_D2   = 40
TFT_D3   = 39
TFT_DC   = 8
TFT_TE   = 38
TFT_BL   = 1
TFT_RST  = -1

# === Touch I2C (AXS15231B 集成触控, 地址 0x3B) ===
TOUCH_SCL = 8   # 与 TFT_DC 共用!
TOUCH_SDA = 4
TOUCH_INT = 3
TOUCH_RST = -1

# === SD_MMC (SD卡, 1-bit 模式) ===
SD_CLK = 12
SD_CMD = 11
SD_D0  = 13

# === NS4168 I2S 音频 ===
I2S_BCK  = 42
I2S_LCK  = 2
I2S_DIN  = 41

# === 电池 ADC ===
BAT_ADC = 5
