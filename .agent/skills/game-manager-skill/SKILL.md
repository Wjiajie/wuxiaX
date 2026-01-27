---
name: game-manager-skill
description: 游戏状态流转与逻辑主控。负责存档、读档、全局状态同步以及游戏初始化与重置逻辑。
---

# 游戏主控技能 (Game Manager Skill)

## 概述
本技能是整个武侠世界的“天道”，负责管理所有 Skill 的生命周期、状态持久化以及世界线的重置工作。

## 核心职责
1. **持久化管理**：通过 `persistence.py` 驱动 SQLite 存档与读档。
   - **SQLite 中心化**: 所有 Skill 的 `references/` 数据在存档时必须同步至 `assets/saves/wuxiaX.db`。
   - **差异同步原则**: 读档时，必须以数据库为准，自动识别并强制覆盖本地有差异的 Skill 实体文件。
   - **指令调用**:
     - `/game-save`: 触发全量数据库存档。
     - `/game-load`: 从数据库恢复状态。
2. **全局同步**：确保所有 Skill 实体文件（.md）与中心数据库保持 100% 同步。
3. **世界重置**：处理 `/game-restart` 指令，通过 `reset_game_state()` 还原所有数据至初始模板。

## 指令逻辑：/game-restart
当玩家输入重置指令时，必须执行以下流程：
1. **物理重置**：调用 `python .agent/skills/game-manager-skill/scripts/manager.py --reset`。
   - 这将还原所有 `references/*.md` 至初始模板，并清空数据库与章节历史。
2. **建立新缘**：物理重置完成后，说书人（story-engine）**必须立刻**发起引导式对话：
   - 确定主角的基本属性（姓名、性别、出身）。
   - 让玩家选择性格特质（正、邪、狂、狷倾向）。
   - 选择初始武学流派。
   - 设定世界难度。
3. **铭刻初始**：将玩家的选择写入 `protagonist-skill/references/character_sheet.md`，然后正式开启“圣堂觉醒”第一回。

## 脚本索引
- `scripts/manager.py`: 核心管理逻辑。
- `scripts/persistence.py`: 数据持久化接口。
- `scripts/db_init.py`: 数据库初始化。
