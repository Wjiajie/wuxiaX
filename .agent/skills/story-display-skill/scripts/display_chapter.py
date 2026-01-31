import os
import sys
import argparse
import subprocess
import textwrap
from pathlib import Path

# 定义根路径
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
CHAPTERS_DIR = BASE_DIR / "history" / "chapters"
MANAGER_SCRIPT = BASE_DIR / ".agent" / "skills" / "game-manager-skill" / "scripts" / "manager.py"

def ensure_dir():
    if not CHAPTERS_DIR.exists():
        CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

def write_and_verify(chapter_num, content, mode="w"):
    ensure_dir()
    file_path = CHAPTERS_DIR / f"chapter_{chapter_num}.md"

    # 写入内容 (w 为覆盖, a 为追加)
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(content)

    return file_path.exists(), file_path

def display_native(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if os.name == 'nt':
                import io
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

            wrapped_content = ""
            for line in content.splitlines():
                if line.strip():
                    wrapped_content += textwrap.fill(line, width=25) + "\n"
                else:
                    wrapped_content += "\n"

            print(wrapped_content)
    except Exception as e:
        print(f"!!! 读取或显示文件时出错: {e}")

def run_manager_check(file_path):
    """调用 manager.py 进行质量与字数校验"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 将内容通过命令行传递给 manager.py 进行校验
        # 注意：对于超长文本，命令行传参可能有上限，此处使用 subprocess 的 stdin 或直接在 Python 内部导入校验逻辑
        # 考虑到代码复用，我们这里尝试直接导入 manager 逻辑或调用脚本
        result = subprocess.run(
            [sys.executable, str(MANAGER_SCRIPT), "--check-story", content],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"!!! 校验过程发生异常: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="写入并展示小说章节 (支持分段追加与万言校验)")
    parser.add_argument("--chapter", type=str, help="章节编号")
    parser.add_argument("--content", type=str, help="章节内容")
    parser.add_argument("--append", action="store_true", help="追加模式 (不展示内容，默认行为)")
    parser.add_argument("--full", action="store_true", help="全量覆盖模式 (慎用，会抹除已有段落)")
    parser.add_argument("--finalize", action="store_true", help="完结并校验展示全文")
    parser.add_argument("--test", action="store_true", help="运行测试模式")

    args = parser.parse_args()

    if args.test:
        print(">>> 运行测试模式...")
        success, path = write_and_verify("test", "这是一段测试文字。")
        if success:
            display_native(path)
        return

    if not args.chapter:
        parser.print_help()
        return

    file_path = CHAPTERS_DIR / f"chapter_{args.chapter}.md"

    # 处理内容写入
    if args.content:
        # 默认使用追加模式，除非显式指定 --full
        mode = "w" if args.full else "a"
        success, path = write_and_verify(args.chapter, args.content, mode)
        if not success:
            print(f"!!! 错误：章节 {args.chapter} 写入失败。")
            sys.exit(1)

        # 如果不是 finalize 模式，默认不展示全文（即视为追加段落）
        if not args.finalize:
            char_count = file_path.stat().st_size // 3 # 粗略估计中文字数
            status = "已重置并写入" if args.full else "已追加"
            print(f">>> 段落{status}。当前章节预览长度：约 {file_path.stat().st_size} 字节。")
            return

    # 处理最终校验与展示
    if args.finalize:
        if not file_path.exists():
            print(f"!!! 错误：找不到章节文件 {file_path}")
            sys.exit(1)

        print(">>> 正在进行万言终审...")
        if run_manager_check(file_path):
            print("\n--- [万言第一回：终审通过，正式开讲] ---\n")
            display_native(file_path)
            print("\n--- [卷终] ---")
        else:
            print("\n[FAIL] 终审未通过！请继续扩充内容或修正略写占位符。")
            sys.exit(1)

if __name__ == "__main__":
    main()
