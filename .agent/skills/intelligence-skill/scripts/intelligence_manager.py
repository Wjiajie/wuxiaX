"""
江湖情报管理脚本 (Intelligence Manager)
负责情报的生成、更新、查询和状态管理
"""

import os
import re
import argparse
import sys
import io
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 强制使用 UTF-8 编码以解决乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 获取项目根目录
SKILL_ROOT = Path(__file__).parent.parent
INTEL_DB_PATH = SKILL_ROOT / "references" / "intelligence_database.md"

# 情报类型
INTEL_TYPES = ["门派动态", "江湖传闻", "神秘事件", "人物行踪", "宝物线索"]

# 情报等级
INTEL_LEVELS = ["普通", "重要", "机密", "传说"]

# 情报状态
INTEL_STATUS = ["活跃", "已失效", "已验证", "已验证为假"]

# 权重配置
INTEL_WEIGHTS = {
    "门派动态": 30,
    "江湖传闻": 25,
    "神秘事件": 15,
    "人物行踪": 15,
    "宝物线索": 15
}

# 地域列表（示例）
LOCATIONS = [
    "武当山", "少林寺", "大研镇", "漱玉矶", "丈人村", "拱石村", "极北雪域",
    "南疆", "白马居", "噶玛寺", "西湖畔", "黄山", "峨眉山", "昆仑山",
    "江南水乡", "西域", "东海之滨"
]

# 情报模板库（用于生成随机情报）
INTEL_TEMPLATES = {
    "门派动态": [
        "{sect}今日传出{event}",
        "{sect}派人前往{location}执行任务",
        "{sect}内部发生人事变动",
        "{sect}与{sect2}的关系出现新变化"
    ],
    "江湖传闻": [
        "在{location}听到关于{subject}的传闻",
        "酒肆里有人谈论{subject}",
        "商队带回{subject}的消息",
        "路人纷纷讨论{subject}"
    ],
    "神秘事件": [
        "{location}近日出现{phenomenon}",
        "{location}发现{discovery}",
        "{time}时分，{location}传出{sound}",
        "在{location}目击{phenomenon}"
    ],
    "人物行踪": [
        "{figure}现身{location}",
        "{figure}在{location}停留",
        "有人目击{figure}路过{location}",
        "{figure}被看到前往{location}"
    ],
    "宝物线索": [
        "传闻{location}可能藏有{treasure}",
        "在{location}发现{clue}",
        "古籍记载{treasure}可能位于{location}",
        "{treasure}的线索指向{location}"
    ]
}

# 门派列表
SECTS = [
    "武当派", "少林寺", "丐帮", "名剑山庄", "神鹰门", "神殿",
    "长生殿", "五仙教", "俏梦阁", "马帮", "赋闲书院", "采玉帮"
]

# 关键词库
KEYWORDS = {
    "event": ["新进展", "重要消息", "人事变动", "武林大会筹备", "秘术研究"],
    "subject": ["神秘高手", "暗杀事件", "宝藏传闻", "异象", "失踪案"],
    "figure": ["百晓生", "丐帮帮主", "名剑山庄庄主", "武当掌门"],
    "phenomenon": ["异象", "奇异光效", "不明现象", "超自然事件"],
    "discovery": ["古代遗迹", "神秘痕迹", "未被记录的机关", "古老符文"],
    "sound": ["奇怪声响", "低鸣", "机械运作声", "叹息声"],
    "time": ["子夜", "黎明前", "黄昏", "正午"],
    "treasure": ["秘籍", "神兵", "珍稀药材", "古物", "藏宝图"],
    "clue": ["可疑标记", "古老线索", "晦涩文字", "残缺图谱"]
}


def parse_intel_database() -> Dict:
    """解析情报数据库"""
    if not INTEL_DB_PATH.exists():
        return {"current_date": "", "active": [], "archived": []}

    content = INTEL_DB_PATH.read_text(encoding="utf-8")

    # 提取当前日期
    date_match = re.search(r"## 当前日期情报 \((\d{4}-\d{2}-\d{2})\)", content)
    current_date = date_match.group(1) if date_match else ""

    # 提取活跃情报（简化解析，实际应用中需要更复杂的表格解析）
    intel_data = {
        "current_date": current_date,
        "active": [],
        "archived": []
    }

    return intel_data


def read_intel_database() -> str:
    """读取情报数据库全文"""
    if not INTEL_DB_PATH.exists():
        return ""
    return INTEL_DB_PATH.read_text(encoding="utf-8")


def generate_intel_id(intel_date: str, count: int) -> str:
    """生成情报ID"""
    return f"INT-{intel_date.replace('-', '')}-{count:03d}"


def calculate_expiry_date(start_date: str, days: int) -> str:
    """计算过期日期"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    expiry = start + timedelta(days=days)
    return expiry.strftime("%Y-%m-%d")


def select_intel_type() -> str:
    """根据权重选择情报类型"""
    import random

    # 权重总数
    total_weight = sum(INTEL_WEIGHTS.values())

    # 随机选择
    rand = random.randint(1, total_weight)
    current_weight = 0

    for intel_type, weight in INTEL_WEIGHTS.items():
        current_weight += weight
        if rand <= current_weight:
            return intel_type

    return "门派动态"  # 默认


def select_intel_level() -> str:
    """选择情报等级（主要生成普通和重要）"""
    import random

    # 基础概率：普通60%，重要30%，机密8%，传说2%
    rand = random.random()

    if rand < 0.60:
        return "普通"
    elif rand < 0.90:
        return "重要"
    elif rand < 0.98:
        return "机密"
    else:
        return "传说"


def select_location() -> str:
    """随机选择地域"""
    import random
    return random.choice(LOCATIONS)


def fill_template(intel_type: str) -> Dict:
    """填充情报模板"""
    import random

    template = random.choice(INTEL_TEMPLATES[intel_type])

    # 随机选择参数
    params = {}
    if "{sect}" in template:
        params["sect"] = random.choice(SECTS)
        params["sect2"] = random.choice([s for s in SECTS if s != params["sect"]])
    if "{location}" in template:
        params["location"] = select_location()
    for key in KEYWORDS:
        if "{" + key + "}" in template:
            params[key] = random.choice(KEYWORDS[key])

    # 填充模板
    content = template.format(**params)

    # 生成详情（内容扩展）
    details = f"详细情报：{content}。此情报尚未得到完全证实，建议前往相关地点调查。"

    return {
        "content": content,
        "details": details,
        "location": params.get("location", "")
    }


def generate_daily_intellignce() -> List[Dict]:
    """生成每日情报"""
    import random

    intel_count = random.randint(3, 6)  # 每日生成3-6条情报
    intel_list = []

    today = datetime.now().strftime("%Y-%m-%d")

    # 至少有一条重要情报
    for i in range(intel_count):
        intel_type = select_intel_type()
        intel_level = select_intel_level()

        # 最后一条如果不是重要或更高级，强制升为重要
        if i == intel_count - 1 and intel_level == "普通":
            intel_level = "重要"

        intel_data = fill_template(intel_type)

        days_valid = random.randint(2, 5)
        if intel_level == "机密":
            days_valid = random.randint(3, 7)
        elif intel_level == "传说":
            days_valid = 999  # 永久有效

        intel_entry = {
            "id": generate_intel_id(today, i + 1),
            "type": intel_type,
            "level": intel_level,
            "content": intel_data["content"][:50],  # 截取前50字作为简短描述
            "details": intel_data["details"],
            "valid_from": today,
            "valid_to": calculate_expiry_date(today, days_valid),
            "location": intel_data["location"],
            "status": "活跃",
            "related_quest": "-"
        }

        intel_list.append(intel_entry)

    return intel_list


def update_daily_intelligence():
    """更新每日情报"""
    import random

    content = read_intel_database()
    today = datetime.now().strftime("%Y-%m-%d")

    # 生成新情报
    new_intels = generate_daily_intellignce()

    # 构建新的活跃情报表格
    active_sections = {
        "门派动态": [],
        "江湖传闻": [],
        "神秘事件": [],
        "人物行踪": [],
        "宝物线索": []
    }

    for intel in new_intels:
        intel_row = f"| **{intel['id']}** | {intel['type']} | {intel['level']} | {intel['content']} | {intel['valid_from']}至{intel['valid_to']} | {intel['location']} | {intel['status']} | {intel['related_quest']} |"
        active_sections[intel['type']].append(intel_row)

    # 构建Markdown内容
    new_content = f"""# 江湖情报数据库 (Intelligence Database)

此档案记录江湖中的各类情报，每日随时间流逝自动更新。

---

## 情报元数据 (Metadata)

| 字段 | 说明 | 格式示例 |
| :--- | :--- | :--- |
| ID | 唯一标识符 | INT-20260213-001 |
| 类型 | 门派动态/江湖传闻/神秘事件/人物行踪/宝物线索 | 门派动态 |
| 等级 | 普通/重要/机密/传说 | 重要 |
| 内容 | 简短描述（列表展示用） | 少林寺收异域弟子 |
| 详情 | 完整描述（详情展示用） | 详细内容... |
| 有效期 | 生成日期+持续时间 | 2026-02-13至2026-02-16 |
| 地域 | 关联位置 | 少林寺 |
| 状态 | 活跃/已失效/已验证/已验证为假 | 活跃 |
| 关联任务 | 触发的支线任务ID | - |

---

## 当前日期情报 ({today})

### 活跃情报 (Active Intelligence)

"""

    # 添加各类型情报
    for intel_type in INTEL_TYPES:
        new_content += f"#### {intel_type}\n\n"

        if active_sections[intel_type]:
            new_content += "| ID | 类型 | 等级 | 内容 | 有效期 | 地域 | 状态 | 关联任务 |\n"
            new_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

            for row in active_sections[intel_type]:
                new_content += row + "\n\n"
                # 添加详情
                intel_id = row.split("|")[1].strip().replace("**", "")
                intel_obj = next((i for i in new_intels if i['id'] == intel_id), None)
                if intel_obj:
                    new_content += f"**详情**：{intel_obj['details']} \n\n---\n\n"
        else:
            new_content += "暂无\n\n---\n\n"

    # 添加其他章节
    new_content += """### 已触发情报任务 (Triggered Quests)

暂无

---

## 历史情报 (Archived Intelligence)

### 已失效情报 (Expired)

暂无

### 已验证情报 (Verified)

暂无

### 已验证为假情报 (Verified False)

暂无

---

## 情报生成日志 (Intelligence Generation Log)

| 日期 | 生成数量 | 类型分布 | 最高等级 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| {today} | {count} | {type_dist} | {max_level} | 日常情报更新 |

---

## 情报查询命令

```bash
# 查看今日所有活跃情报
python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --list

# 查看特定情报详情
python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --show INT-20260213-001

# 更新每日情报
python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --update_daily

# 验证情报为真/假
python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --verify INT-20260213-002 --result true/false

# 标记情报已触发任务
python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --trigger INT-20260213-003 --task_id QUEST-001
```
"""

    # 统计数据
    count = len(new_intels)
    type_dist_str = " ".join([f"{t}:{len([i for i in new_intels if i['type']==t])}" for t in INTEL_TYPES])
    max_level = max([i['level'] for i in new_intels], key=lambda x: INTEL_LEVELS.index(x))

    new_content = new_content.format(
        today=today,
        count=count,
        type_dist=type_dist_str,
        max_level=max_level
    )

    INTEL_DB_PATH.write_text(new_content, encoding="utf-8")
    print(f"每日情报已更新（{today}）共 {count} 条")


def list_intelligence(type_filter: Optional[str] = None, level_filter: Optional[str] = None):
    """列出情报"""
    content = read_intel_database()

    # 查找活跃情报表格
    active_start = content.find("## 当前日期情报")
    if active_start == -1:
        print("未找到当前情报数据")
        return

    # 输出简略列表（简化实现）
    print("=== 今日活跃情报 ===")
    print(content[active_start:active_start+2000])  # 输出前2000字符作为预览


def show_intelligence_detail(intel_id: str):
    """显示情报详情"""
    content = read_intel_database()

    # 查找情报ID
    if intel_id not in content:
        print(f"未找到情报 ID: {intel_id}")
        return

    # 提取详情（简化实现）
    pattern = rf"\*\*{re.escape(intel_id)}\*\*.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?(\*\*详情\*\*：.*?)\n\n---"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        details = match.group(1).replace("**详情**：", "")
        print(f"情报详情（{intel_id}）：")
        print(details)
    else:
        # 备用方案：展示附近内容
        idx = content.find(intel_id)
        if idx != -1:
            print(f"情报信息（{intel_id}）：")
            print(content[idx:idx+500])


def verify_intelligence(intel_id: str, result: str):
    """验证情报真伪"""
    if result.lower() not in ["true", "false", "真", "假"]:
        print("验证结果必须是 true/false 或 真/假")
        return False

    new_status = "已验证" if result.lower() in ["true", "真"] else "已验证为假"

    content = read_intel_database()

    # 替换状态
    old_line = f"| **{intel_id}** |"
    parts = content.split(old_line)

    if len(parts) < 2:
        print(f"未找到情报 ID: {intel_id}")
        return False

    # 简化实现：显示结果
    print(f"情报 {intel_id} 已验证为：{new_status}")
    print("（完整状态更新需要更复杂的表格解析逻辑）")
    return True


def trigger_quest(intel_id: str, task_id: str):
    """标记情报已触发任务"""
    content = read_intel_database()

    if intel_id not in content:
        print(f"未找到情报 ID: {intel_id}")
        return False

    print(f"情报 {intel_id} 已关联任务：{task_id}")
    print("（完整关联更新需要更复杂的表格解析逻辑）")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="江湖情报管理工具")
    parser.add_argument("--update_daily", action="store_true", help="更新每日情报")
    parser.add_argument("--list", action="store_true", help="列出今日情报")
    parser.add_argument("--show", type=str, help="显示情报详情（情报ID）")
    parser.add_argument("--verify", type=str, help="验证情报（情报ID）")
    parser.add_argument("--result", type=str, help="验证结果（true/false）")
    parser.add_argument("--trigger", type=str, help="标记情报已触发任务（情报ID）")
    parser.add_argument("--task_id", type=str, help="任务ID")

    args = parser.parse_args()

    if args.update_daily:
        update_daily_intelligence()
    elif args.list:
        list_intelligence()
    elif args.show:
        show_intelligence_detail(args.show)
    elif args.verify:
        if args.result:
            verify_intelligence(args.verify, args.result)
        else:
            print("验证情报需要提供 --result 参数（true/false 或 真/假）")
    elif args.trigger:
        if args.task_id:
            trigger_quest(args.trigger, args.task_id)
        else:
            print("标记任务关联需要提供 --task_id 参数")
    else:
        parser.print_help()
