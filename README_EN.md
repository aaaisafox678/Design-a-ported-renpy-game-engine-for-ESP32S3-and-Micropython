# Micro-RenPy 7.4.11 — Ren'Py Visual Novel Engine for ESP32-S3

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![ESP32-S3](https://img.shields.io/badge/chip-ESP32--S3-red.svg)](https://www.espressif.com/en/products/socs/esp32-s3)
[![MicroPython](https://img.shields.io/badge/python-MicroPython-green.svg)](https://micropython.org/)

A lightweight **Ren'Py 7.4.11** port for **ESP32-S3** running **MicroPython**, designed to run visual novel games on embedded hardware.

> ⚠️ **Status: ~45% complete, largely AI-assisted. Not fully tested on real hardware. Contributors welcome!**

---

## Overview

Micro-RenPy brings the Ren'Py visual novel engine to ESP32-S3 microcontrollers. It supports script parsing, sprite display, audio mixing, video playback, and touch input — all within the tight memory constraints of embedded systems.

Currently targeting the **JC3248W535CN** board, but should be portable to other ESP32-S3 boards.

### Supported Media Formats

| Type | Format | Spec |
|------|--------|------|
| Video/CG | `.avi` | Motion JPEG Video, 480×320, 12fps |
| Video Audio | MP3 | 64 KB/s, mono, 48000 Hz |
| Images | `.rgb565` | Raw RGB565, 480×320 |
| Audio | `.pcm` | s16le mono, 48000Hz |
| Aspect Ratio | 16:9 → 480×270 | Centered with 25px black bars top/bottom |

### Memory Footprint

| State | PSRAM Used | Available |
|-------|-----------|-----------|
| Idle (framebuf only) | 0.3MB | 7.7MB |
| BGM + background | 1.0MB | 7.0MB |
| 3 characters + BGM | 2.2MB | 5.8MB |

---

## Tools

Convert Ren'Py game assets to ESP32-S3 compatible formats:

| Tool | Platform | Usage |
|------|----------|-------|
| `tools/convert.py` | Cross-platform | `python3 convert.py <src> <dst>` |
| `tools/convert.sh` | Linux/macOS | `bash convert.sh <src> <dst>` |
| `tools/convert.bat` | Windows | `convert.bat <src> <dst>` |
| `tools/fix_scripts.py` | Cross-platform | `python3 fix_scripts.py <game_dir>` |

**Requires: [ffmpeg](https://ffmpeg.org/)**

Options: `--width`, `--height`, `--fps`, `--aspect`, `--no-video`, `--no-audio`, `--no-image`

---

## Quick Start

### 1. Flash Firmware

| File | Address |
|------|---------|
| `firmware/bootloader.bin` | `0x0` |
| `firmware/partition-table.bin` | `0x8000` |
| `firmware/micropython.bin` | `0x10000` |

Flash Mode: **DIO** | Flash Size: **16MB** | Speed: **80MHz**

Hold BOOT → plug USB → release BOOT → flash → replug to boot.

### 2. Prepare TF Card

```
TF Card root/
├── micropython-renpy/    # Engine code
│   ├── main.py
│   ├── renpy/
│   └── lib/
└── game/                 # Converted game assets
    ├── images/           # .rgb565 + .avi
    ├── Audio/            # .pcm
    ├── Fonts/            # .ttf
    └── *.rpy             # Scripts (extensions fixed)
```

### 3. Convert Assets

```bash
python3 tools/convert.py original_game/ output_game/
python3 tools/fix_scripts.py output_game/
# Copy output_game/ to TF card
```

### 4. Run

Insert TF card, power on, connect serial (115200 baud):

```python
exec(open('/sdcard/micropython-renpy/main.py').read())
```

### 5. Auto-start (Optional)

Create `/sdcard/main.py` on the TF card:

```python
import sys; sys.path.insert(0, '/sdcard/micropython-renpy')
exec(open('/sdcard/micropython-renpy/main.py').read())
```

---

## Pinout (JC3248W535CN)

| Peripheral | Pins |
|------------|------|
| LCD CS/SCK/D0-D3 | 45/47/21,48,40,39 |
| LCD DC/BL | 8/1 |
| Touch SCL/SDA | 8/4 |
| Audio BCLK/LRCLK/DIN | 42/2/41 |
| SD Card CLK/CMD/D0 | 12/11/13 |

---

## Building Custom Firmware

To add JPEG/MJPEG hardware decoding, modify pinouts, or integrate C extensions:

```bash
git clone https://github.com/yaconsult/micropython-jc3248w535en.git
bash setup.sh
source ~/esp/esp-idf/export.sh
make BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT \
     USER_C_MODULES=~/Repos/micropython_esp_panel.cmake \
     -C ~/Repos/micropython/ports/esp32
```

---

## Contributing

Help wanted:

- [ ] Real hardware testing & feedback
- [ ] Cinepak/MJPEG C extension integration
- [ ] More board adaptations
- [ ] Performance optimization
- [ ] Documentation improvements

---

## License

MIT License. Based on Ren'Py 7.4.11 (MIT) and yaconsult/micropython-jc3248w535en (MIT).

---

## Acknowledgments

- [Ren'Py](https://renpy.org/) — Visual novel engine
- [MicroPython](https://micropython.org/) — Python for microcontrollers
- [yaconsult/micropython-jc3248w535en](https://github.com/yaconsult/micropython-jc3248w535en) — ESP32-S3 MicroPython firmware
- [moononournation/aviPlayer](https://github.com/moononournation/aviPlayer) — ESP32 AVI player