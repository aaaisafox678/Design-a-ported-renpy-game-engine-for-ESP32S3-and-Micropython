#!/usr/bin/env python3
"""
Micro-RenPy 资源转换工具 (通用版)
===================================
将 Ren'Py 游戏资源批量转换为 ESP32-S3 MicroPython 兼容格式。

用法:
  python3 convert.py <游戏目录> <输出目录> [选项]

选项:
  --no-video      跳过视频转换
  --no-audio      跳过音频转换
  --no-image      跳过图片转换
  --fps N         视频帧率 (默认: 12)
  --width W       输出宽度 (默认: 480)
  --height H      输出高度 (默认: 320)
  --aspect W:H    目标宽高比 (默认: 16:9, 会在高度方向加黑边)

输出格式:
  .png/.jpg/.jpeg → .rgb565     (RGB565 raw像素, 直接灌入framebuf)
  .ogg/.mp3/.wav  → .pcm       (s16le mono 48kHz raw PCM, 直接灌入I2S)
  .webm/.mp4/.avi → .avi       (MJPEG + MP3, Motion JPEG Video)

依赖:
  ffmpeg (需在 PATH 中)
  Pillow (可选, 用于单张图片转换)

Windows 用户:
  安装 ffmpeg: https://ffmpeg.org/download.html
  或使用: winget install ffmpeg

Linux 用户:
  sudo apt install ffmpeg
  # 或
  sudo pacman -S ffmpeg
"""

import subprocess
import os
import sys
import argparse
import shutil
from pathlib import Path

# ===== 默认参数 =====
DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 320
DEFAULT_FPS = 12
DEFAULT_AUDIO_RATE = 48000
DEFAULT_AUDIO_CHANNELS = 1
TARGET_ASPECT = (16, 9)  # 宽:高

# ===== ffmpeg 检测 =====
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[ERROR] ffmpeg 未找到! 请先安装 ffmpeg:")
        print("  Windows: winget install ffmpeg  或 https://ffmpeg.org/download.html")
        print("  Linux:   sudo apt install ffmpeg")
        print("  macOS:   brew install ffmpeg")
        return False


# ===== 核心转换函数 =====
def convert_image(src, dst, width, height, target_aspect):
    """
    转换图片: PNG/JPG → RGB565
    保持原始宽高比, 加黑边
    """
    dst = Path(dst).with_suffix('.rgb565')
    if dst.exists():
        return "skip"

    dw, dh = width, height
    tw, th = target_aspect
    content_h = int(dw * th / tw)
    pad_top = int((dh - content_h) / 2)
    pad_bottom = dh - content_h - pad_top

    vf = f"scale={dw}:{content_h}:force_original_aspect_ratio=decrease,pad={dw}:{dh}:0:{pad_top}:black"

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", vf,
        "-pix_fmt", "rgb565",
        "-vframes", "1",
        "-f", "rawvideo",
        str(dst)
    ]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0:
        return "ok"
    return "fail"


def convert_audio(src, dst, rate=48000, channels=1):
    """
    转换音频: OGG/MP3/WAV → PCM s16le mono
    """
    dst = Path(dst).with_suffix('.pcm')
    if dst.exists():
        return "skip"

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-ar", str(rate),
        "-ac", str(channels),
        "-f", "s16le",
        str(dst)
    ]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0:
        return "ok"
    return "fail"


def convert_video(src, dst, width, height, fps, target_aspect, has_audio=True):
    """
    转换视频: WEBM/MP4 → AVI (MJPEG + MP3)
    """
    dst = Path(dst).with_suffix('.avi')
    if dst.exists():
        return "skip"

    dw, dh = width, height
    tw, th = target_aspect
    content_h = int(dw * th / tw)
    pad_top = int((dh - content_h) / 2)

    vf = f"scale={dw}:{content_h}:force_original_aspect_ratio=decrease,pad={dw}:{dh}:0:{pad_top}:black"

    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-c:v", "mjpeg", "-q:v", "7",
        "-vf", vf,
        "-r", str(fps),
        "-pix_fmt", "yuvj420p",
    ]

    if has_audio:
        cmd += ["-c:a", "mp3", "-ab", "64k", "-ar", "48000", "-ac", "1"]
    else:
        cmd += ["-an"]

    cmd.append(str(dst))

    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0:
        return "ok"
    return "fail"


def has_audio_stream(filepath):
    """检查视频文件是否有音频流"""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", str(filepath)],
            capture_output=True, text=True
        )
        import json
        data = json.loads(r.stdout)
        return any(s.get('codec_type') == 'audio' for s in data.get('streams', []))
    except:
        return False


# ===== 主流程 =====
def main():
    parser = argparse.ArgumentParser(
        description="Micro-RenPy 资源转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 convert.py ./my_game ./output
  python3 convert.py ./my_game ./output --no-video --fps 15
  python3 convert.py ./my_game ./output --width 320 --height 240 --aspect 4:3
        """
    )
    parser.add_argument("source", help="源游戏目录")
    parser.add_argument("output", help="输出目录")
    parser.add_argument("--no-video", action="store_true", help="跳过视频转换")
    parser.add_argument("--no-audio", action="store_true", help="跳过音频转换")
    parser.add_argument("--no-image", action="store_true", help="跳过图片转换")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help=f"视频帧率 (默认: {DEFAULT_FPS})")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help=f"输出宽度 (默认: {DEFAULT_WIDTH})")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help=f"输出高度 (默认: {DEFAULT_HEIGHT})")
    parser.add_argument("--aspect", type=str, default=f"{TARGET_ASPECT[0]}:{TARGET_ASPECT[1]}",
                        help="目标宽高比 (默认: 16:9)")
    parser.add_argument("--audio-rate", type=int, default=DEFAULT_AUDIO_RATE,
                        help=f"音频采样率 (默认: {DEFAULT_AUDIO_RATE})")

    args = parser.parse_args()

    # 检查 ffmpeg
    if not check_ffmpeg():
        sys.exit(1)

    # 解析宽高比
    try:
        tw, th = map(int, args.aspect.split(":"))
    except:
        print("[ERROR] 无效的宽高比格式, 应为 W:H (如 16:9)")
        sys.exit(1)

    src_dir = Path(args.source)
    dst_dir = Path(args.output)

    if not src_dir.is_dir():
        print(f"[ERROR] 源目录不存在: {src_dir}")
        sys.exit(1)

    print("=" * 60)
    print("Micro-RenPy 资源转换工具")
    print(f"源目录:   {src_dir}")
    print(f"输出目录: {dst_dir}")
    print(f"输出尺寸: {args.width}x{args.height} (宽高比 {tw}:{th})")
    print(f"视频帧率: {args.fps} fps")
    print(f"音频采样: {args.audio_rate} Hz mono")
    print("=" * 60)

    # 后缀映射
    IMG_EXTS = {'.png', '.jpg', '.jpeg'}
    AUD_EXTS = {'.ogg', '.mp3', '.wav', '.flac'}
    VID_EXTS = {'.webm', '.mp4', '.avi', '.mkv'}
    COPY_EXTS = {'.rpy', '.rpyc', '.ttf', '.otf', '.txt', '.json', '.ico'}

    stats = {"img": 0, "aud": 0, "vid": 0, "copy": 0, "skip": 0, "fail": 0, "total": 0}

    for root, dirs, files in os.walk(src_dir):
        for fname in files:
            stats["total"] += 1
            src = Path(root) / fname
            rel = src.relative_to(src_dir)
            dst = dst_dir / rel
            ext = src.suffix.lower()

            dst.parent.mkdir(parents=True, exist_ok=True)

            if ext in IMG_EXTS and not args.no_image:
                r = convert_image(src, dst, args.width, args.height, (tw, th))
            elif ext in AUD_EXTS and not args.no_audio:
                r = convert_audio(src, dst, args.audio_rate)
            elif ext in VID_EXTS and not args.no_video:
                audio = has_audio_stream(src)
                r = convert_video(src, dst, args.width, args.height, args.fps, (tw, th), audio)
            elif ext in COPY_EXTS:
                if not dst.exists():
                    shutil.copy2(src, dst)
                    r = "copy"
                else:
                    r = "skip"
            else:
                r = "skip"

            stats[r] = stats.get(r, 0) + 1

            if stats["total"] % 200 == 0:
                print(f"  进度: {stats['total']} 文件 "
                      f"(图:{stats['img']} 音:{stats['aud']} 视:{stats['vid']} "
                      f"拷:{stats['copy']} 跳:{stats['skip']} 败:{stats['fail']})")

    print("\n" + "=" * 60)
    print("转换完成!")
    print(f"  总文件:   {stats['total']}")
    print(f"  图片转换: {stats['img']} 张  (.rgb565, {args.width}x{args.height})")
    print(f"  音频转换: {stats['aud']} 个  (.pcm, {args.audio_rate}Hz mono)")
    print(f"  视频转换: {stats['vid']} 个  (.avi, MJPEG+MP3)")
    print(f"  文件复制: {stats['copy']}")
    print(f"  跳过:     {stats['skip']}")
    print(f"  失败:     {stats['fail']}")
    print(f"  输出目录: {dst_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()