import os
import re
import argparse
from pathlib import Path

# 获取项目根目录
SKILL_ROOT = Path(__file__).parent.parent
QUEST_LOG_PATH = SKILL_ROOT / "references" / "quest_log.md"

def parse_quest_log():
    if not QUEST_LOG_PATH.exists():
        return None
    
    content = QUEST_LOG_PATH.read_text(encoding="utf-8")
    return content

def update_quest(quest_name, status=None, progress=None, description=None):
    if not QUEST_LOG_PATH.exists():
        print(f"错误：未找到任务日志 {QUEST_LOG_PATH}")
        return False
    
    content = QUEST_LOG_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    found = False

    # 正则表达式匹配 Markdown 表格中的任务行
    # | **任务名称** | 描述 | 进度 | 状态 | 相关... |
    pattern = rf"\|\s*\*\*?{re.escape(quest_name)}\*\*?\s*\|"

    for line in lines:
        if re.search(pattern, line):
            found = True
            parts = [p.strip() for p in line.split("|")]
            # parts[0] 是空字符串（左侧 | 之前）
            # parts[1] 是任务名称
            # parts[2] 是描述
            # parts[3] 是进度
            # parts[4] 是状态
            
            if description:
                parts[2] = description
            if progress:
                parts[3] = progress
            if status:
                parts[4] = status
            
            new_line = "| " + " | ".join(parts[1:-1]) + " |"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if not found:
        print(f"未找到任务 '{quest_name}'，请手动添加或检查拼写。")
        return False

    QUEST_LOG_PATH.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"成功更新任务 '{quest_name}'。")
    return True

def add_quest(quest_name, description, progress, status, relations, category="Side"):
    content = QUEST_LOG_PATH.read_text(encoding="utf-8")
    
    # 确定插入位置
    if category == "Main":
        marker = "## 1. 主线任务"
    else:
        marker = "## 2. 支线任务"
    
    new_entry = f"| **{quest_name}** | {description} | {progress} | {status} | {relations} |"
    
    if marker in content:
        # 在标记后的表格下方添加
        lines = content.splitlines()
        inserted = False
        for i, line in enumerate(lines):
            if marker in line:
                # 寻找表格结束处（空行或下一个标题）
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == "" or lines[j].startswith("##"):
                        lines.insert(j, new_entry)
                        inserted = True
                        break
                if not inserted:
                    lines.append(new_entry)
                    inserted = True
                break
        
        # 处理“暂无”占位符
        if category == "Side" and "暂无" in content:
            content = content.replace("暂无\n", "")
            lines = content.splitlines() # 重新处理

        QUEST_LOG_PATH.write_text("\n".join(lines), encoding="utf-8")
        print(f"成功添加{category}任务 '{quest_name}'。")
        return True
    
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="任务日志管理工具")
    parser.add_argument("--update", type=str, help="任务名称")
    parser.add_argument("--status", type=str, help="新状态")
    parser.add_argument("--progress", type=str, help="新进度")
    parser.add_argument("--desc", type=str, help="新描述")
    
    parser.add_argument("--add", type=str, help="新任务名称")
    parser.add_argument("--category", type=str, choices=["Main", "Side"], default="Side")
    parser.add_argument("--relations", type=str, help="相关人物/地点")

    args = parser.parse_args()

    if args.update:
        update_quest(args.update, status=args.status, progress=args.progress, description=args.desc)
    elif args.add:
        add_quest(args.add, args.desc or "", args.progress or "刚开始", args.status or "进行中", args.relations or "未知", args.category)
