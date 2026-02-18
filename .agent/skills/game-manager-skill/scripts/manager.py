import os
import json
import re
from pathlib import Path
from datetime import datetime
from persistence import save_game, load_game
from memory import GameMemory

class SkillRegistry:
    """
    功法名册：管理所有已登记的 Agent Skills 及其元数据。
    """
    def __init__(self, skills_dir):
        self.skills_dir = skills_dir
        self.registry = {}
        self.load_registry()

    def load_registry(self):
        """扫描并加载所有技能的元数据"""
        if not self.skills_dir.exists():
            return
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if skill_md.exists():
                    # 这里可以解析 YAML 元数据，暂时简单记录
                    self.registry[skill_path.name] = {
                        "path": skill_path,
                        "references": [f.name for f in (skill_path / "references").glob("*.md")] if (skill_path / "references").exists() else [],
                        "has_scripts": (skill_path / "scripts").exists()
                    }

    def get_skill(self, name):
        return self.registry.get(name)

class SkillManager:
    """
    造化主控：通过 SkillRegistry 动态管理所有 Agent Skills。
    """
    def __init__(self):
        # __file__ 为 .../.agent/skills/game-manager-skill/scripts/manager.py
        # .parent.parent.parent.parent 为 .agent 目录
        # .parent.parent.parent.parent.parent 为项目根目录
        self.base_dir = Path(__file__).parent.parent.parent.parent.parent
        self.skills_dir = self.base_dir / ".agent" / "skills"
        self.registry = SkillRegistry(self.skills_dir)
        self.memory = GameMemory()
        self.active_skills = self.registry.registry # 兼容旧接口

    def get_skill_data(self, skill_name, reference_file):
        """读取指定技能的参考数据内容"""
        if skill_name not in self.active_skills:
            return None

        target_path = self.active_skills[skill_name]["path"] / "references" / reference_file
        if target_path.exists():
            return target_path.read_text(encoding="utf-8")
        return None

    def update_skill_data(self, skill_name, reference_file, new_content):
        """落笔修改指定技能的参考数据，并记录变动至记忆"""
        if skill_name not in self.active_skills:
            print(f"错误：未发现功法 {skill_name}")
            return False

        ref_dir = self.active_skills[skill_name]["path"] / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        target_path = ref_dir / reference_file

        # 记录变动前的记忆（可选）
        old_content = target_path.read_text(encoding="utf-8") if target_path.exists() else "（新创）"

        target_path.write_text(new_content, encoding="utf-8")

        # 铭刻变动记忆
        self.memory.add_long_term(
            "世界变动",
            f"修改了 {skill_name} 的 {reference_file}",
            f"旧貌：{old_content[:50]}... 新颜：{new_content[:50]}..."
        )
        return True

    def take_global_snapshot(self):
        """
        遍览诸般功法，摄取当前世界所有 Skill 的状态快照。
        """
        snapshot = {
            "skills": {},
            "world_time": datetime.now().isoformat()
        }
        for skill_name, info in self.active_skills.items():
            snapshot["skills"][skill_name] = {}
            ref_dir = info["path"] / "references"
            if ref_dir.exists():
                for ref_file in ref_dir.glob("*.md"):
                    content = ref_file.read_text(encoding="utf-8")
                    snapshot["skills"][skill_name][ref_file.name] = content
        
        # 摄取短期记忆作为剧情衔接
        snapshot["memory"] = {
            "short_term": self.memory.short_term,
            "last_log": self.memory.short_term[-1]["narrative"] if self.memory.short_term else ""
        }
        return snapshot

    def apply_global_snapshot(self, snapshot):
        """
        万法归宗：将快照中的数据回写到各 Skill 的 references 目录（差异对比机制）。
        """
        if not snapshot or "skills" not in snapshot:
            return False

        print(">>> 正在核对世界线差异...")
        for skill_name, files in snapshot["skills"].items():
            for filename, content in files.items():
                target_path = self.active_skills.get(skill_name, {}).get("path")
                if target_path:
                    target_file = target_path / "references" / filename
                    # 差异判定
                    if target_file.exists():
                        current_content = target_file.read_text(encoding="utf-8")
                        if current_content != content:
                            print(f"检测到差异：{skill_name}/{filename}，正在同步至数据库版本。")
                            self.update_skill_data(skill_name, filename, content)
                    else:
                        print(f"补全缺失文件：{skill_name}/{filename}")
                        self.update_skill_data(skill_name, filename, content)
        
        # 恢复短期记忆
        if "memory" in snapshot and "short_term" in snapshot["memory"]:
            self.memory.short_term = snapshot["memory"]["short_term"]
            
        return True

    def execute_full_save(self, chapter="未知", location="未知"):
        """执行完整存档：抓取所有 Skill 状态并存入 SQLite 数据库"""
        data = self.take_global_snapshot()
        # 自动尝试从小模块提取位置
        if location == "未知":
            sheet = self.get_skill_data("protagonist-skill", "character_sheet.md")
            loc_match = re.search(r"当前位置\*\*：(.*?)$", sheet, re.M) if sheet else None
            location = loc_match.group(1) if loc_match else "未知"

        return save_game(data, chapter=chapter, location=location)

    def execute_full_load(self, save_id=None):
        """执行完整读档：从本地数据库恢复数据并同步至各 Skill 目录"""
        data = load_game(save_id)
        if data:
            return self.apply_global_snapshot(data)
        return False

    def reset_game_state(self):
        """
        万象更新：重置游戏世界至初始状态。
        1. 从 templates 目录还原 references。
        2. 清空存档数据库。
        3. 清空历史章节。
        """
        print(">>> 正在初始化江湖世界...")

        # 1. 还原模板
        for skill_name, info in self.active_skills.items():
            template_dir = info["path"] / "templates"
            if template_dir.exists():
                for template_file in template_dir.glob("*.md"):
                    content = template_file.read_text(encoding="utf-8")
                    self.update_skill_data(skill_name, template_file.name, content)
                    print(f"  - 已重置功法数据：{skill_name}/{template_file.name}")

        # 2. 清空存档数据库
        from persistence import DB_PATH
        if DB_PATH.exists():
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM game_saves")
            conn.commit()
            conn.close()
            print("  - 已清除所有江湖存档。")

        # 3. 清空历史章节
        chapters_dir = self.base_dir / "history" / "chapters"
        if chapters_dir.exists():
            for chapter_file in chapters_dir.glob("*.md"):
                chapter_file.unlink()
            print("  - 已粉碎所有历史残章。")

        # 4. 重置记忆
        self.memory.short_term = []
        # 可以选择是否清空长期记忆数据库，目前保留
        
        print("\n>>> 江湖已重置，乾坤再启。")
        return True

    def trigger_global_sync(self):
        """
        全局同步钩子：章节结束后检索所有 Skill 是否需要更新。
        """
        print(">>> 正在触发全局同步校验...")
        if self.sync_protagonist_to_memory():
            print("  - 主角[江未央]状态同步成功。")
        self.sync_intelligence_system()

        # 可以在此扩展其他 NPC 或物品的同步逻辑
        print("\n>>> 全局同步校验完成，江湖因果已锁定。")
        return True

    def check_story_content(self, content):
        """
        文案质量校检：
        1. 检测是否存在 (省略/略写/...) 等占位符。
        2. 检测总字数是否达到 5,000 字标准。
        """
        errors = []

        # 1. 占位符检测 (针对常见的中英文括号省略表达)
        placeholders = [
            r"\(.*?省略.*?\)", r"（.*?省略.*?）",
            r"\(.*?略写.*?\)", r"（.*?略写.*?）",
            r"\(.*?待续.*?\)", r"（.*?待续.*?）",
            r"省略后续", r"后续细节", r"字细节"
        ]
        for pattern in placeholders:
            if re.search(pattern, content):
                errors.append(f"检测到占位符/略写痕迹：'{re.search(pattern, content).group()}'。请展开描写，严禁使用概括性描述替代正文。")

        # 2. 字数检测
        char_count = len(content)
        if char_count < 5000:
            errors.append(f"当前文案长度为 {char_count} 字，未达到 5,000 字的最低标准。请继续扩充细节、心理描写、环境烘托或支线对话。")

        if errors:
            print("\n[ERROR] 文案校验未通过：")
            for err in errors:
                print(f"  - {err}")
            return False

        print(f"\n[SUCCESS] 文案校验通过！总长度：{char_count} 字。")
        return True

    def sync_protagonist_to_memory(self):
        """将主角当前状态快照同步至记忆库"""
        content = self.get_skill_data("protagonist-skill", "character_sheet.md")
        if content:
            # 提取核心数据用于记忆显示
            hp_match = re.search(r"气血 \(HP\)\*\*：(\d+) / (\d+)", content)
            location_match = re.search(r"当前位置\*\*：(.*?)$", content, re.M)

            data = {
                "hp": hp_match.group(1) if hp_match else "未知",
                "location": location_match.group(1) if location_match else "未知",
                "full_sheet": content
            }
            self.memory.save_entity_state("protagonist", data)
            print(f"  - 已捕捉神识快照：位置[{data['location']}] 气血[{data['hp']}]")
            return True
        return False

    def sync_intelligence_system(self):
        """
        情报系统同步钩子：检查并更新情报系统状态
        """
        print(">>> 正在同步江湖情报系统...")

        # 获取最新情报列表（通过调用 intelligence_manager.py）
        import subprocess
        result = subprocess.run(
            ["python", ".agent/skills/intelligence-skill/scripts/intelligence_manager.py", "--list"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        print(f"  - 情报系统状态：{result.stdout[:200] if result.stdout else '无情报'}")
        print("\n>>> 江湖情报同步完成。")
        return True

    def process_story_event(self, event_type, description, impact_data=None):
        """
        根据剧情发展动态驱动技能数据修改。
        event_type: 事件类型（如 'combat_result', 'travel', 'item_get'）
        """
        self.memory.add_short_term(description)

        if event_type == "travel" and impact_data:
            new_location = impact_data.get("location")
            # 修改主角技能中的位置
            sheet = self.get_skill_data("protagonist-skill", "character_sheet.md")
            if sheet:
                new_sheet = re.sub(r"- \*\*当前位置\*\*：(.*?)$", f"- **当前位置**：{new_location}", sheet, flags=re.M)
                self.update_skill_data("protagonist-skill", "character_sheet.md", new_sheet)
                self.memory.add_long_term("行踪", f"抵达了 {new_location}", description)

if __name__ == "__main__":
    import os
    import sys
    import io
    # 强制设置 stdout 编码为 utf-8 以支持特殊字符和中文输出
    if os.name == 'nt':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    import argparse
    parser = argparse.ArgumentParser(description="游戏主控逻辑接口")
    parser.add_argument("--reset", action="store_true", help="重置江湖世界至初始状态")
    parser.add_argument("--sync", action="store_true", help="执行全局同步校验")
    parser.add_argument("--save", action="store_true", help="执行全量存档")
    parser.add_argument("--load", action="store_true", help="从最新存档读档")
    parser.add_argument("--check-story", type=str, help="校验故事文案质量与长度")

    args = parser.parse_args()
    gm = SkillManager()

    if args.reset:
        gm.reset_game_state()
    elif args.sync:
        gm.trigger_global_sync()
    elif args.save:
        gm.execute_full_save()
    elif args.load:
        gm.execute_full_load()
    elif args.check_story:
        if not gm.check_story_content(args.check_story):
            sys.exit(1) # 校验失败退出码为 1
    else:
        # 默认测试：尝试读取主角卡
        sheet = gm.get_skill_data("protagonist-skill", "character_sheet.md")
        if sheet:
            print("主角卡读取成功。")
        # 模拟一段剧情变动
        # gm.process_story_event("travel", "江未央穿过石窟裂缝，来到了隐秘的『桃花坞』。", {"location": "桃花坞"})
        # print("剧情变动测试完成。")
