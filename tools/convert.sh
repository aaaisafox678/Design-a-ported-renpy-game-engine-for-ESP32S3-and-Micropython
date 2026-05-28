#!/bin/bash
# =============================================
# Micro-RenPy 资源转换工具 (Linux版)
# =============================================
# 将 Ren'Py 游戏资源批量转换为 ESP32-S3 兼容格式
#
# 用法:
#   bash convert.sh <游戏目录> <输出目录>
#
# 选项 (环境变量):
#   NO_VIDEO=1   跳过视频
#   NO_AUDIO=1   跳过音频
#   NO_IMAGE=1   跳过图片
#   FPS=12       视频帧率
#   WIDTH=480    输出宽度
#   HEIGHT=320   输出高度
#
# 依赖: ffmpeg
#   Ubuntu/Debian: sudo apt install ffmpeg
#   Arch:          sudo pacman -S ffmpeg
# =============================================

set -e

# 参数
SRC="${1:?请指定源目录}"
DST="${2:?请指定输出目录}"
FPS="${FPS:-12}"
W="${WIDTH:-480}"
H="${HEIGHT:-320}"
AR="${AUDIO_RATE:-48000}"

# 16:9 内容高度 + 黑边
CONTENT_H=$((W * 9 / 16))
PAD_TOP=$(((H - CONTENT_H) / 2))
VFILTER="scale=${W}:${CONTENT_H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:0:${PAD_TOP}:black"

echo "========================================"
echo "Micro-RenPy 资源转换工具 (Linux)"
echo "源目录: $SRC"
echo "输出:   $DST"
echo "尺寸:   ${W}x${H} (16:9 居中 + 黑边)"
echo "视频:   ${FPS}fps MJPEG+MP3"
echo "音频:   ${AR}Hz mono PCM"
echo "========================================"
echo ""

mkdir -p "$DST"

N=0; IMG=0; AUD=0; VID=0; CP=0; SK=0; ER=0

# 检测 ffmpeg
command -v ffmpeg >/dev/null 2>&1 || { echo "[ERROR] 需要 ffmpeg!"; exit 1; }

# 图片转换
if [ "${NO_IMAGE:-0}" != "1" ]; then
    echo ">>> 图片转换 (.png/.jpg → .rgb565)..."
    find "$SRC" \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -print0 2>/dev/null | \
    while IFS= read -r -d '' f; do
        rel="${f#$SRC/}"
        out="$DST/${rel%.*}.rgb565"
        [ -f "$out" ] && { SK=$((SK+1)); continue; }
        mkdir -p "$(dirname "$out")"
        ffmpeg -y -i "$f" -vf "$VFILTER" -pix_fmt rgb565 -vframes 1 -f rawvideo "$out" 2>/dev/null && IMG=$((IMG+1)) || ER=$((ER+1))
        N=$((N+1)); [ $((N%200)) -eq 0 ] && echo "  $N 文件..."
    done
    echo "  图片完成"
fi

# 音频转换
if [ "${NO_AUDIO:-0}" != "1" ]; then
    echo ">>> 音频转换 (.ogg/.mp3/.wav → .pcm)..."
    find "$SRC" \( -name "*.ogg" -o -name "*.mp3" -o -name "*.wav" \) -print0 2>/dev/null | \
    while IFS= read -r -d '' f; do
        rel="${f#$SRC/}"
        out="$DST/${rel%.*}.pcm"
        [ -f "$out" ] && { SK=$((SK+1)); continue; }
        mkdir -p "$(dirname "$out")"
        ffmpeg -y -i "$f" -ar "$AR" -ac 1 -f s16le "$out" 2>/dev/null && AUD=$((AUD+1)) || ER=$((ER+1))
    done
    echo "  音频完成"
fi

# 视频转换
if [ "${NO_VIDEO:-0}" != "1" ]; then
    echo ">>> 视频转换 (.webm/.mp4 → .avi)..."
    find "$SRC" \( -name "*.webm" -o -name "*.mp4" -o -name "*.avi" \) -print0 2>/dev/null | \
    while IFS= read -r -d '' f; do
        rel="${f#$SRC/}"
        out="$DST/${rel%.*}.avi"
        [ -f "$out" ] && { SK=$((SK+1)); continue; }
        mkdir -p "$(dirname "$out")"
        # 检查是否有音频
        has_audio=$(ffprobe -v quiet -select_streams a -show_entries stream=codec_type -of csv=p=0 "$f" 2>/dev/null)
        if [ -n "$has_audio" ]; then
            ffmpeg -y -i "$f" -vf "$VFILTER" -r "$FPS" -c:v mjpeg -q:v 7 -c:a mp3 -ab 64k -ar 48000 -ac 1 -pix_fmt yuvj420p "$out" 2>/dev/null
        else
            ffmpeg -y -i "$f" -vf "$VFILTER" -r "$FPS" -c:v mjpeg -q:v 7 -an -pix_fmt yuvj420p "$out" 2>/dev/null
        fi
        [ $? -eq 0 ] && VID=$((VID+1)) || ER=$((ER+1))
    done
    echo "  视频完成"
fi

echo ""
echo "========================================"
echo "转换完成!"
echo "  图片: $IMG | 音频: $AUD | 视频: $VID"
echo "  复制: $CP | 跳过: $SK | 失败: $ER"
echo "========================================"