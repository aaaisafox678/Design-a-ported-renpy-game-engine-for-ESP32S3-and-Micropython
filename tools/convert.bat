@echo off
REM =============================================
REM Micro-RenPy 资源转换工具 (Windows版)
REM =============================================
REM 将 Ren'Py 游戏资源批量转换为 ESP32-S3 兼容格式
REM
REM 用法:
REM   convert.bat <游戏目录> <输出目录>
REM
REM 依赖: ffmpeg (需在 PATH 中)
REM   下载: https://ffmpeg.org/download.html
REM   或: winget install ffmpeg
REM =============================================

setlocal enabledelayedexpansion

if "%~1"=="" (echo 用法: convert.bat 源目录 输出目录 & exit /b 1)
if "%~2"=="" (echo 用法: convert.bat 源目录 输出目录 & exit /b 1)

set SRC=%~1
set DST=%~2
set FPS=12
set W=480
set H=320
set AR=48000

REM 16:9 内容高度 + 黑边
set /a CONTENT_H=%W% * 9 / 16
set /a PAD_TOP=(%H% - %CONTENT_H%) / 2
set VFILTER=scale=%W%:%CONTENT_H%:force_original_aspect_ratio=decrease,pad=%W%:%H%:0:%PAD_TOP%:black

echo ========================================
echo Micro-RenPy 资源转换工具 (Windows)
echo 源目录: %SRC%
echo 输出:   %DST%
echo 尺寸:   %W%x%H% (16:9 居中 + 黑边)
echo 视频:   %FPS%fps MJPEG+MP3
echo 音频:   %AR%Hz mono PCM
echo ========================================
echo.

REM 检查 ffmpeg
where ffmpeg >nul 2>&1 || (echo [ERROR] 需要 ffmpeg! 从 https://ffmpeg.org/download.html 下载 & exit /b 1)

if not exist "%DST%" mkdir "%DST%"

REM 图片
echo ^>^>^> 图片转换 (.png/.jpg -^> .rgb565)...
for /r "%SRC%" %%f in (*.png *.jpg *.jpeg) do (
    set "rel=%%f"
    set "rel=!rel:%SRC%\=!"
    set "out=%DST%\!rel:.png=.rgb565!"
    set "out=!out:.jpg=.rgb565!"
    set "out=!out:.jpeg=.rgb565!"
    if not exist "!out!" (
        mkdir "!out!\.." 2>nul
        ffmpeg -y -i "%%f" -vf "%VFILTER%" -pix_fmt rgb565 -vframes 1 -f rawvideo "!out!" 2>nul
    )
)
echo   图片完成

REM 音频
echo ^>^>^> 音频转换 (.ogg/.mp3 -^> .pcm)...
for /r "%SRC%" %%f in (*.ogg *.mp3 *.wav) do (
    set "rel=%%f"
    set "rel=!rel:%SRC%\=!"
    set "out=%DST%\!rel:.ogg=.pcm!"
    set "out=!out:.mp3=.pcm!"
    set "out=!out:.wav=.pcm!"
    if not exist "!out!" (
        mkdir "!out!\.." 2>nul
        ffmpeg -y -i "%%f" -ar %AR% -ac 1 -f s16le "!out!" 2>nul
    )
)
echo   音频完成

REM 视频
echo ^>^>^> 视频转换 (.webm/.mp4 -^> .avi)...
for /r "%SRC%" %%f in (*.webm *.mp4 *.avi) do (
    set "rel=%%f"
    set "rel=!rel:%SRC%\=!"
    set "out=%DST%\!rel:.webm=.avi!"
    set "out=!out:.mp4=.avi!"
    set "out=!out:.avi=.avi!"
    if not exist "!out!" (
        mkdir "!out!\.." 2>nul
        ffmpeg -y -i "%%f" -vf "%VFILTER%" -r %FPS% -c:v mjpeg -q:v 7 -c:a mp3 -ab 64k -ar 48000 -ac 1 -pix_fmt yuvj420p "!out!" 2>nul
    )
)
echo   视频完成

echo.
echo ========================================
echo 转换完成!
echo ========================================

endlocal