"""
武侠世界叙事初始化脚本

功能：
1. 从 world_narratives.md 中随机选取一条世界叙事
2. 从 chapter_narratives.md 中随机选取一条章节叙事
3. 组合生成初始叙事上下文
4. 将结果写入 character_sheet.md 的"初始叙事"字段

用法：
python narrative_initializer.py
python narrative_initializer.py --force  # 强制重新生成
"""

import os
import sys
import random
import argparse
import re
from pathlib import Path
from datetime import datetime

# 定义根路径
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
WORLD_NARRATIVES_PATH = BASE_DIR / ".agent" / "skills" / "world-logic" / "references" / "world_narratives.md"
CHAPTER_NARRATIVES_PATH = BASE_DIR / ".agent" / "skills" / "world-logic" / "references" / "chapter_narratives.md"
CHARACTER_SHEET_PATH = BASE_DIR / ".agent" / "skills" / "protagonist-skill" / "references" / "character_sheet.md"


def parse_narratives(file_path: Path) -> dict:
    """解析叙事文件，返回 {序号: {标题, 内容, 原始段落}}"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    narratives = {}
    current_idx = 0

    # 按行分割，找到所有叙事标题行
    lines = content.split('\n')
    current_title = None
    current_lines = []

    for line in lines:
        # 检查是否是新的叙事标题 (## 壹、 或 ## 一、 或 ## 1、 等格式)
        stripped = line.strip()
        if stripped.startswith('## '):
            # 中文大写数字前缀
            cn_prefixes = ['壹、', '贰、', '叁、', '肆、', '伍、', '陆、', '柒、', '捌、', '玖、', '拾、']
            # 中文小写数字前缀
            cn_small_prefixes = ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、']

            found = False
            for prefix in cn_prefixes + cn_small_prefixes:
                if prefix in stripped:
                    title_start = stripped.find(prefix) + len(prefix)
                    title = stripped[title_start:].strip()

                    # 保存之前的叙事
                    if current_title is not None:
                        narratives[current_idx] = {
                            'title': current_title,
                            'content': '\n'.join(current_lines).strip(),
                            'full': '\n'.join(current_lines).strip()
                        }
                        current_idx += 1

                    # 开始新的叙事
                    current_title = title
                    current_lines = []
                    found = True
                    break

            if not found:
                # 检查阿拉伯数字开头
                m = re.match(r'^##\s+(\d+)[、\.]\s+(.+)$', stripped)
                if m:
                    # 保存之前的叙事
                    if current_title is not None:
                        narratives[current_idx] = {
                            'title': current_title,
                            'content': '\n'.join(current_lines).strip(),
                            'full': '\n'.join(current_lines).strip()
                        }
                        current_idx += 1

                    # 开始新的叙事
                    current_title = m.group(2)
                    current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    # 保存最后一个叙事
    if current_title is not None:
        narratives[current_idx] = {
            'title': current_title,
            'content': '\n'.join(current_lines).strip(),
            'full': '\n'.join(current_lines).strip()
        }

    return narratives


def select_random_narrative(narratives: dict, exclude: list = None) -> tuple:
    """随机选择一条叙事，返回 (序号, 叙事内容)"""
    exclude = exclude or []
    keys = [k for k in narratives.keys() if k not in exclude]
    if not keys:
        return None, None
    selected_key = random.choice(keys)
    return selected_key, narratives[selected_key]


def generate_initial_clue(world_narrative: dict, chapter_narrative: dict, protagonist_info: dict) -> str:
    """根据世界叙事和章节叙事，动态生成初始线索"""

    protagonist_name = protagonist_info.get('name', '???')
    background = protagonist_info.get('background', '市井游侠')
    birthplace = protagonist_info.get('birthplace', '大研镇')

    # 提取世界叙事的核心主题
    world_title = world_narrative['title']
    chapter_title = chapter_narrative['title']

    # 生成初始线索模板
    clues = [
        f"那日，你在{birthplace}的酒馆中无意间听到的对话，似乎与「{world_title}」的传闻有关...",
        f"据传「{world_title}」的秘密即将在江湖上掀起波澜，而你——{protagonist_name}，似乎命中注定要卷入其中。",
        f"你出身{background}，在{birthplace}闯荡时，偶然得知了「{world_title}」的蛛丝马迹...",
        f"江湖中人皆知「{world_title}」，而「{chapter_title}」的故事，正要从你说起。",
        f"你带着一身本事离开{birthplace}，却不知自己的命运已与「{world_title}」紧紧相连..."
    ]

    return random.choice(clues)


def format_combined_narrative(world: dict, chapter: dict, clue: str, protagonist_info: dict) -> str:
    """格式化组合叙事输出"""

    output = f"""
# 初始叙事上下文

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 世界级叙事

### {world['title']}

{world['content']}

---

## 章节级叙事

### {chapter['title']}

{chapter['content']}

---

## 初始线索

> *{clue}*

---

## 主角信息

- **姓名**: {protagonist_info.get('name', '???')}
- **背景**: {protagonist_info.get('background', '???')}
- **出生地**: {protagonist_info.get('birthplace', '???')}
- **初始情节**: {protagonist_info.get('initial_event', '???')}

---

## 叙事组合说明

本游戏的叙事基调为「{world['title']}」与「{chapter['title']}」的组合。
世界叙事定义了游戏的宏观背景与长线冲突，章节叙事则定义了主角的初始故事线。
两者交织，将构建出独一无二的江湖传奇。

"""

    return output.strip()


def read_character_sheet() -> dict:
    """读取角色资料卡获取主角信息"""
    if not CHARACTER_SHEET_PATH.exists():
        return {}

    with open(CHARACTER_SHEET_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    info = {}

    # 解析关键字段
    patterns = {
        'name': r'\*\*姓名\*\*[：:]\s*(.+)',
        'background': r'\*\*背景\*\*[：:]\s*(.+)',
        'birthplace': r'\*\*出生地\*\*[：:]\s*(.+)',
        'initial_event': r'\*\*初始情节\*\*[：:]\s*(.+)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            info[key] = match.group(1).strip()

    return info


def append_to_character_sheet(combined_narrative: str) -> bool:
    """追加组合叙事到角色资料卡"""

    if not CHARACTER_SHEET_PATH.exists():
        print(f"!!! 角色资料卡不存在: {CHARACTER_SHEET_PATH}")
        return False

    try:
        with open(CHARACTER_SHEET_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查是否已有初始叙事
        if "初始叙事上下文" in content:
            # 替换已存在的初始叙事部分
            pattern = r'\n---\n# 初始叙事上下文.*?(?=\n---\n## 资源参考|\Z)'
            content = re.sub(pattern, f'\n---\n{combined_narrative}\n---', content, flags=re.DOTALL)
        else:
            # 在资源参考之前追加
            if "## 资源参考" in content:
                content = content.replace("## 资源参考", f"{combined_narrative}\n---\n\n## 资源参考")
            else:
                content += f"\n\n{combined_narrative}\n"

        with open(CHARACTER_SHEET_PATH, "w", encoding="utf-8") as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"!!! 写入角色资料卡失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="武侠世界叙事初始化工具")
    parser.add_argument("--force", action="store_true", help="强制重新生成，覆盖已有叙事")
    parser.add_argument("--world-only", action="store_true", help="仅显示世界叙事选择")
    parser.add_argument("--chapter-only", action="store_true", help="仅显示章节叙事选择")

    args = parser.parse_args()

    # 设置随机种子以便复现（可选）
    # random.seed(42)

    # 检查文件是否存在
    if not WORLD_NARRATIVES_PATH.exists():
        print(f"!!! 世界叙事文件不存在: {WORLD_NARRATIVES_PATH}")
        sys.exit(1)
    if not CHAPTER_NARRATIVES_PATH.exists():
        print(f"!!! 章节叙事文件不存在: {CHAPTER_NARRATIVES_PATH}")
        sys.exit(1)

    # 解析叙事文件
    print(">>> 正在加载叙事库...")
    world_narratives = parse_narratives(WORLD_NARRATIVES_PATH)
    chapter_narratives = parse_narratives(CHAPTER_NARRATIVES_PATH)

    print(f"    已加载 {len(world_narratives)} 条世界叙事")
    print(f"    已加载 {len(chapter_narratives)} 条章节叙事")

    # 读取角色信息
    protagonist_info = read_character_sheet()
    if not protagonist_info:
        print("!!! 无法读取角色信息，请先完成角色创建")
        protagonist_info = {'name': '???', 'background': '???', 'birthplace': '???'}

    # 随机选择
    world_idx, selected_world = select_random_narrative(world_narratives)
    chapter_idx, selected_chapter = select_random_narrative(chapter_narratives)

    # 生成初始线索
    clue = generate_initial_clue(selected_world, selected_chapter, protagonist_info)

    # 格式化输出
    combined = format_combined_narrative(selected_world, selected_chapter, clue, protagonist_info)

    print("\n" + "="*60)
    print("          武侠世界叙事初始化完成")
    print("="*60)
    print(f"\n【世界叙事】{selected_world['title']}")
    print(f"【章节叙事】{selected_chapter['title']}")
    print(f"\n【初始线索】{clue}")

    if args.world_only:
        print("\n--- 世界叙事完整内容 ---")
        print(selected_world['full'])
        return

    if args.chapter_only:
        print("\n--- 章节叙事完整内容 ---")
        print(selected_chapter['full'])
        return

    # 写入角色资料卡
    if append_to_character_sheet(combined):
        print(f"\n>>> 已将组合叙事追加至: {CHARACTER_SHEET_PATH}")
    else:
        print(f"\n!!! 写入失败，请手动检查")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
