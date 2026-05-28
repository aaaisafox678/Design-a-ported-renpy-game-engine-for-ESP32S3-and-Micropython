# Micro-RenPy 7.4.11 — ESP32-S3 Ren'Py 视觉小说引擎移植

一个专门为搭载 **MicroPython** 的 **ESP32-S3** 芯片移植的 **Ren'Py 视觉小说游戏引擎**。

> 当前状态：45% AI 辅助开发，尚未经过完整实测。欢迎各位一起参与移植！

---

## 简介

Micro-RenPy 是 Ren'Py 7.4.11 的轻量级 MicroPython 移植，目标是让视觉小说游戏运行在 ESP32-S3 这类嵌入式平台上。目前专门为 JC3248W535CN 开发板移植，也可移植到其它 ESP32-S3 板子。

### 资源格式

| 类型 | 格式 | 规格 |
|------|------|------|
| 视频/CG | `.avi` | Motion JPEG Video, 480x320, 12fps |
| 视频音频 | MP3 | 64 KB/s, 单声道, 48000 Hz |
| 图片 | `.rgb565` | 480x320 raw RGB565 |
| 音频 | `.pcm` | s16le mono 48000Hz |
| 宽高比处理 | 16:9 -> 480x270 | 上下各 25 行黑边 |

---

## 工具

| 工具 | 平台 | 用法 |
|------|------|------|
| `tools/convert.py` | 通用 | `python3 convert.py 源目录 输出目录` |
| `tools/convert.sh` | Linux | `bash convert.sh 源目录 输出目录` |
| `tools/convert.bat` | Windows | `convert.bat 源目录 输出目录` |
| `tools/fix_scripts.py` | 通用 | `python3 fix_scripts.py game/` |

依赖: ffmpeg

---

## 快速开始

### 1. 烧录固件

| 文件 | 地址 |
|------|------|
| `firmware/bootloader.bin` | `0x0` |
| `firmware/partition-table.bin` | `0x8000` |
| `firmware/micropython.bin` | `0x10000` |

DIO / 16MB / 80MHz。按住 BOOT -> 插 USB -> 松 BOOT -> 烧录。

### 2. 准备 TF 卡

```
TF卡根目录/
├── micropython-renpy/    # 项目代码
└── game/                 # 游戏资源 (转换后)
    ├── images/           # .rgb565 + .avi
    ├── Audio/            # .pcm
    ├── Fonts/            # .ttf
    └── *.rpy             # 脚本
```

### 3. 转换资源

```bash
python3 tools/convert.py 原始game/ 输出game/
python3 tools/fix_scripts.py 输出game/
```

### 4. 启动

TF卡插入，上电，串口连接(115200):

```python
exec(open('/sdcard/micropython-renpy/main.py').read())
```

### 5. 自启动(可选)

TF卡根目录创建 `main.py`:

```python
import sys; sys.path.insert(0, '/sdcard/micropython-renpy')
exec(open('/sdcard/micropython-renpy/main.py').read())
```

---

## 引脚定义 (JC3248W535CN)

| 外设 | 引脚 |
|------|------|
| LCD CS/SCK/D0-D3 | 45/47/21,48,40,39 |
| LCD DC/BL | 8/1 |
| 触控 SCL/SDA | 8/4 |
| 音频 BCLK/LRCLK/DIN | 42/2/41 |
| SD卡 CLK/CMD/D0 | 12/11/13 |

---

## 编译自定义固件

参考 yaconsult 构建指南:

```bash
git clone https://github.com/yaconsult/micropython-jc3248w535en.git
bash setup.sh
source ~/esp/esp-idf/export.sh
make BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT \
     USER_C_MODULES=~/Repos/micropython_esp_panel.cmake \
     -C ~/Repos/micropython/ports/esp32
```

---

## 贡献

特别需要帮助: 真机实测反馈 / Cinepak C 扩展集成 / 更多板型适配 / 性能优化

---

## 许可

基于 Ren'Py 7.4.11 (MIT) / yaconsult 固件 (MIT)  
