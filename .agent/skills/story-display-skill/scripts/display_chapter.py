import os
import sys
import argparse
import subprocess
from pathlib import Path

# 定义根路径
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
CHAPTERS_DIR = BASE_DIR / "history" / "chapters"

def ensure_dir():
    if not CHAPTERS_DIR.exists():
        CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

def write_and_verify(chapter_num, content):
    ensure_dir()
    file_path = CHAPTERS_DIR / f"chapter_{chapter_num}.txt"
    
    # 1. 尝试写入
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # 2. 校验是否存在且不为空
    if file_path.exists() and file_path.stat().st_size > 0:
        return True, file_path
    return False, file_path

import textwrap

def display_native(file_path):
    # 直接在 Python 中读取并打印，以更好地处理编码
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # 针对 Windows 环境，尝试强制输出为 utf-8
            if os.name == 'nt':
                import sys
                import io
                # 重新包装 stdout 以支持 utf-8 强制输出
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

            # 为移动端优化：自动换行处理
            # 考虑到中文字符宽度，设置较窄的换行宽度（如 25）
            wrapped_content = ""
            for line in content.splitlines():
                if line.strip():
                    wrapped_content += textwrap.fill(line, width=25) + "\n"
                else:
                    wrapped_content += "\n"

            print(wrapped_content)
    except Exception as e:
        print(f"!!! 读取或显示文件时出错: {e}")
        # 降级方案
        if os.name == 'nt':
            subprocess.run(["type", str(file_path)], shell=True, check=True)
        else:
            subprocess.run(["cat", str(file_path)], check=True)

def main():
    parser = argparse.ArgumentParser(description="写入并展示小说章节")
    parser.add_argument("--chapter", type=str, help="章节编号")
    parser.add_argument("--content", type=str, help="章节内容")
    parser.add_argument("--test", action="store_true", help="运行测试模式")
    
    args = parser.parse_args()
    
    if args.test:
        print(">>> 运行测试模式...")
        success, path = write_and_verify("test", "这是一段测试文字。功不唐捐，玉汝于成。")
        if success:
            print(f">>> 校验成功，文件位于：{path}\n")
            display_native(path)
        else:
            print(">>> 校验失败！")
        return

    if not args.chapter or not args.content:
        parser.print_help()
        return

    success, path = write_and_verify(args.chapter, args.content)
    if success:
        # print(f"\n--- [章节 {args.chapter} 写入成功] ---\n")
        display_native(path)
        print("\n--- [完] ---")
    else:
        print(f"!!! 错误：章节 {args.chapter} 写入校验失败，请检查磁盘空间或权限。")
        sys.exit(1)

if __name__ == "__main__":
    main()
