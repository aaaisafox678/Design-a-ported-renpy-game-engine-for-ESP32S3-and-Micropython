#!/usr/bin/env python3
"""
Micro-RenPy 脚本后缀替换工具
===============================
自动将 Ren'Py .rpy 脚本中的资源引用替换为 ESP32-S3 兼容后缀:

  .png / .jpg / .jpeg  →  .rgb565
  .ogg / .mp3 / .wav   →  .pcm
  .webm / .mp4 / .mkv  →  .avi

用法:
  python3 fix_scripts.py <游戏目录>
  python3 fix_scripts.py <游戏目录> --dry-run   (仅预览, 不修改)

Windows:
  python fix_scripts.py game/

Linux:
  python3 fix_scripts.py ./game/
"""

import os
import re
import sys
import argparse
from pathlib import Path

# 后缀映射
REPLACEMENTS = {
    '.png': '.rgb565',
    '.jpg': '.rgb565',
    '.jpeg': '.rgb565',
    '.ogg': '.pcm',
    '.mp3': '.pcm',
    '.wav': '.pcm',
    '.flac': '.pcm',
    '.webm': '.avi',
    '.mp4': '.avi',
    '.mkv': '.avi',
}

# 匹配脚本中的引用: "path/to/file.ext"
RE_PATTERN = re.compile(r'\.(png|jpg|jpeg|ogg|mp3|wav|flac|webm|mp4|mkv)"', re.IGNORECASE)


def fix_script(filepath, dry_run=False):
    """替换单个脚本文件中的后缀"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  [SKIP] {filepath}: {e}")
        return 0

    count = 0
    new_content = content

    for old_ext, new_ext in REPLACEMENTS.items():
        pattern = re.escape(old_ext) + r'"'
        replacement = new_ext + '"'
        c = len(re.findall(pattern, new_content, re.IGNORECASE))
        if c > 0:
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            count += c

    if count == 0:
        return 0

    if not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"  [ERROR] {filepath}: {e}")
            return 0

    return count


def main():
    parser = argparse.ArgumentParser(description="Micro-RenPy 脚本后缀替换工具")
    parser.add_argument("directory", help="游戏目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不修改文件")
    parser.add_argument("--rpa", action="store_true", help="扫描 .rpa 文件")
    args = parser.parse_args()

    game_dir = Path(args.directory)
    if not game_dir.is_dir():
        print(f"[ERROR] 目录不存在: {game_dir}")
        sys.exit(1)

    print("=" * 60)
    print("Micro-RenPy 脚本后缀替换工具")
    print(f"目录: {game_dir}")
    if args.dry_run:
        print("模式: 仅预览 (--dry-run)")
    print("=" * 60)

    total_files = 0
    total_replacements = 0

    for root, dirs, files in os.walk(game_dir):
        for fname in files:
            if not fname.endswith('.rpy'):
                continue
            filepath = os.path.join(root, fname)
            count = fix_script(filepath, args.dry_run)
            if count > 0:
                rel = os.path.relpath(filepath, game_dir)
                print(f"  {rel}: {count} 处替换")
                total_files += 1
                total_replacements += count

    print("\n" + "=" * 60)
    print(f"完成! 修改了 {total_files} 个文件, 共 {total_replacements} 处替换")
    if args.dry_run:
        print("(仅预览模式, 未实际修改)")
    print("=" * 60)


if __name__ == "__main__":
    main()