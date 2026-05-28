#pragma once

// ========== CPU & Clock ==========
#define MICROPY_HW_CLK_FREQ               (240000000L)
#define MICROPY_PY_FLOAT                  (1)
#define MICROPY_PY_FROZENSETS             (1)

// ========== MCUSPI (QSPI for PSRAM & LCD) ==========
// ESP32-S3 使用 MSPI 作为 QSPI 总线
// LCD 和 PSRAM 共享 QSPI 总线
#define MICROPY_HW_SPI_MOSI               (21)  // QSPI D0
#define MICROPY_HW_SPI_MISO               (19)  // QSPI D1 (复用)
#define MICROPY_HW_SPI_SCLK               (17)  // QSPI SCLK
#define MICROPY_HW_SPI_CS                 (18)  // QSPI CS

// ========== LVGL 显示缓冲 ==========
// 320x480 屏幕, RGB565 = 2 bytes/pixel
// 使用一半屏幕缓冲以节省SRAM
#define MICROPY_HW_LVGL_HOR_RES           (320)
#define MICROPY_HW_LVGL_VER_RES           (480)
#define MICROPY_HW_LVGL_BUF_HEIGHT        (240)  // 一半高度
#define MICROPY_HW_LVGL_DOUBLE_BUFFER     (1)

// ========== PSRAM ==========
// ESP32-S3 连接 Octal PSRAM
#define MICROPY_HW_ENABLE_PSRAM           (1)
#define MICROPY_HEAP_PSRAM                (1)

// ========== I2C 总线 (触摸屏 + 外部设备) ==========
#define MICROPY_HW_I2C0_SDA               (4)
#define MICROPY_HW_I2C0_SCL               (5)
#define MICROPY_HW_I2C0_FREQ              (400000)

// ========== SPI 总线 (独立SPI用于LCD) ==========
// 注意: LCD使用独立的SPI2_HOST而非MSPI
#define MICROPY_HW_LCD_SPI_HOST           (SPI2_HOST)
#define MICROPY_HW_LCD_SPI_SCLK           (47)
#define MICROPY_HW_LCD_SPI_MOSI           (48)
#define MICROPY_HW_LCD_SPI_MISO           ((gpio_num_t)-1)  // QSPI模式不需要MISO

// ========== LCD 引脚 ==========
#define MICROPY_HW_LCD_CS                 (45)
#define MICROPY_HW_LCD_DC                 (8)
#define MICROPY_HW_LCD_RST                ((gpio_num_t)-1)  // 无复位
#define MICROPY_HW_LCD_BL                 (1)   // 背光PWM
#define MICROPY_HW_LCD_TE                 (38)  // Tearing Effect 垂直同步

// ========== QSPI LCD 数据引脚 ==========
#define MICROPY_HW_LCD_QSPI_D0            (21)
#define MICROPY_HW_LCD_QSPI_D1            (48)
#define MICROPY_HW_LCD_QSPI_D2            (40)
#define MICROPY_HW_LCD_QSPI_D3            (39)

// ========== 触摸屏 I2C ==========
#define MICROPY_HW_TOUCH_I2C_SDA          (4)
#define MICROPY_HW_TOUCH_I2C_SCL          (5)
#define MICROPY_HW_TOUCH_RST              ((gpio_num_t)-1)
#define MICROPY_HW_TOUCH_INT              (46)

// ========== I2S 音频 ==========
#define MICROPY_HW_I2S_PORT               (I2S_NUM_0)
#define MICROPY_HW_I2S_BCLK               (7)
#define MICROPY_HW_I2S_LRCLK              (6)
#define MICROPY_HW_I2S_DATA               (15)
#define MICROPY_HW_I2S_DUMMY              (14)
#define MICROPY_HW_I2S_FREQ               (48000)  // 48kHz

// ========== SD Card ==========
#define MICROPY_HW_SD_CLK                 (12)
#define MICROPY_HW_SD_CMD                 (11)
#define MICROPY_HW_SD_DAT0                (13)
#define MICROPY_HW_SD_DAT1                (20)
#define MICROPY_HW_SD_DAT2                (3)
#define MICROPY_HW_SD_DAT3                (42)
#define MICROPY_HW_SD_CS                  (41)

// ========== USB ==========
#define MICROPY_HW_USB_PID                (0x8047)
#define MICROPY_HW_USB_VID                (0x303A)  // Espressif

// ========== 内存配置 ==========
#define MICROPY_HEAP_SIZE                 (0x200000)  // 2MB heap in SRAM
#define MICROPY_PY_BUILTINS_HELP          (0)  // 节省空间
#define MICROPY_PY_BUILTINS_HELP_TEXT     (0)
#define MICROPY_PY_BUILTINS_STR_UNICODE   (1)
#define MICROPY_PY___FILE__               (1)

// ========== 文件系统 ==========
#define MICROPY_VFS_FAT                   (1)
#define MICROPY_VFS_LFS1                  (0)
#define MICROPY_VFS_LFS2                  (0)
#define MICROPY_PY_OS_STATV               (1)
#define MICROPY_PY_OS_PATH_BASENAME       (1)
#define MICROPY_PY_OS_PATH_DIR            (1)
#define MICROPY_PY_OS_LISTDIR             (1)
#define MICROPY_PY_OS_UNAME               (1)

// ========== 网络 (可选, 节省空间可以关闭) ==========
#define MICROPY_PY_NETWORK                (1)
#define MICROPY_PY_NETWORK_HOSTNAME_DEFAULT   ("Micro-RenPy")

// ========== 音频支持 ==========
#define MICROPY_PY_MICROPYTHON_MEM_INFO   (1)
#define MICROPY_PY_UTIME_MPFR             (1)

// ========== RenPy 引擎扩展 ==========
// 自定义模块
#define MICROPY_PORT_RENPY_MODULES        (1)
#define MICROPY_PORT_RENPY_MAX_CHARS      (65536)
#define MICROPY_PORT_RENPY_MAX_SPRITES    (16)
#define MICROPY_PORT_RENPY_MAX_SCENES     (64)
#define MICROPY_PORT_RENPY_MAX_AUDIO_CHANNELS (4)

// ========== Python 扩展 ==========
#define MICROPY_PY_BUILTINS_RANGE_CONST_ARGS  (1)
#define MICROPY_PY_BUILTINS_ROUND_INT       (1)
#define MICROPY_PY_GENERATOR_PEND_THROW     (1)
#define MICROPY_PY_FUNCS                    (1)
#define MICROPY_PY_DELATTR_SETATTR          (1)

// ========== 裁剪选项 (节省内存) ==========
#define MICROPY_OPT_CACHE_MAP_LOOKUP_IN_BYTECODE  (1)
#define MICROPY_ENABLE_GC                   (1)
#define MICROPY_ENABLE_FINALISER            (0)  // 关闭以节省内存
#define MICROPY_STACK_CHECK                 (0)  // 关闭以节省内存

/*
 * All rights reserved.
 * 官方网站：https://www.hcnsec.cn/
 */