import sys
from pathlib import Path

# 添加脚本路径到 sys.path
scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

from manager import SkillManager
from memory import GameMemory

def test_full_cycle():
    print("=== 开始全流程测试 ===")

    # 1. 初始化 SkillManager
    gm = SkillManager()
    print(f"已加载技能数量: {len(gm.active_skills)}")
    assert "protagonist-skill" in gm.active_skills

    # 2. 测试读取数据
    sheet = gm.get_skill_data("protagonist-skill", "character_sheet.md")
    print(f"读取主角卡成功，字符长度: {len(sheet)}")

    # 3. 测试剧情事件处理 (动态修改 + 长期记忆)
    test_location = "测试隐秘山谷"
    gm.process_story_event("travel", f"江未央来到了{test_location}。", {"location": test_location})

    # 验证文件是否修改
    updated_sheet = gm.get_skill_data("protagonist-skill", "character_sheet.md")
    assert test_location in updated_sheet
    print(f"动态修改位置验证成功: {test_location}")

    # 4. 验证记忆是否存入数据库
    memories = gm.memory.query_long_term("行踪")
    found = False
    for m in memories:
        if test_location in m[2]: # key_event 字段
            found = True
            break
    assert found
    print("记忆持久化验证成功。")

    # 5. 测试快照同步
    gm.sync_protagonist_to_memory()
    print("主角快照同步完成。")

    print("=== 测试完成，全流程通畅 ===")

if __name__ == "__main__":
    try:
        test_full_cycle()
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
