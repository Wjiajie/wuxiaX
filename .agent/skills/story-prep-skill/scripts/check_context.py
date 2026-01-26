import os
import re
from pathlib import Path

# 定义根路径
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
SKILLS_DIR = BASE_DIR / ".agent" / "skills"

def get_protagonist_status():
    path = SKILLS_DIR / "protagonist-skill" / "references" / "character_sheet.md"
    if not path.exists():
        return "主角状态：未知"
    
    content = path.read_text(encoding="utf-8")
    # 提取核心数据
    hp = re.search(r"气血 \(HP\)\*\*：(.*?)\n", content)
    mp = re.search(r"内力 \(MP\)\*\*：(.*?)\n", content)
    loc = re.search(r"当前位置\*\*：(.*?)$", content, re.M)
    personality = re.search(r"人格倾向\*\*：(.*?)$", content, re.M)
    
    return f"""
[主角状态]
- 位置：{loc.group(1).strip() if loc else "未知"}
- 气血/内力：{hp.group(1).strip() if hp else "未知"} / {mp.group(1).strip() if mp else "未知"}
- 性格倾向：{personality.group(1).strip() if personality else "未知"}
"""

def get_nearby_npcs(location):
    path = SKILLS_DIR / "npc-skill" / "references" / "npc_list.md"
    if not path.exists():
        return ""
    
    content = path.read_text(encoding="utf-8")
    # 寻找主角队友
    teammates = re.findall(r"### \d+\. (.*?)\n.*?好感度\*\*：(\d+ \(.*?\))", content, re.S)
    
    # 这里的 location 匹配逻辑可以更复杂，目前示例简单化
    return "\n[附近/在队 NPC]\n" + "\n".join([f"- {t[0]}: 好感度 {t[1]}" for t in teammates])

def get_environment_info(location):
    path = SKILLS_DIR / "world-logic" / "references" / "spatial_nodes.md"
    if not path.exists():
        return ""
    
    content = path.read_text(encoding="utf-8")
    # 提取对应地点的描述
    match = re.search(rf"## .*?{location}.*?\n(.*?)\n##", content, re.S)
    if match:
        return f"\n[环境摘要]\n{match.group(1).strip()}"
    return ""

def main():
    print(">>> 正在执行故事生成前置校测...\n")
    
    p_status = get_protagonist_status()
    print(p_status)
    
    # 获取当前位置
    loc_match = re.search(r"位置：(.*?)$", p_status, re.M)
    current_loc = loc_match.group(1) if loc_match else ""
    
    # 如果位置包含子区域，提取主区域名用于环境检索
    main_loc = current_loc.split("·")[0] if "·" in current_loc else current_loc
    
    print(get_nearby_npcs(main_loc))
    print(get_environment_info(main_loc))
    
    print("\n>>> 校测完毕，可以开始叙事。")

if __name__ == "__main__":
    main()
