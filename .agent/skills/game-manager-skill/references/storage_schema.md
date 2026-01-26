# 存档数据结构规范 (Storage Schema)

本文件定义了 `/game-save` 指令执行时，游戏状态持久化的数据格式。数据主要存储为 JSON 格式。

## 核心数据对象

### 1. protagonist (主角)
从 `protagonist-skill/references/character_sheet.md` 提取。
- `name`: 姓名
- `attributes`: 核心属性 (力道, 身法, 内功等)
- `status`: 当前气血, 内力, 精力
- `skills`: 已学武学及进度
- `inventory`: 背包物品列表
- `plot_progress`: 当前位置, 主线任务状态

### 2. world (世界)
从 `world-logic/` 和 `spatial_nodes.md` 提取。
- `current_location`: 当前场景节点
- `environment_state`: 场景特殊状态 (如：圣堂石窟-已觉醒)

### 3. npc_states (NPC 状态)
- 记录已交互 NPC 的好感度、位置或生死状态。

### 4. memory (记忆)
- `last_narrative`: 存档前最后一段“说书人”的叙述（用于读档后的剧情衔接）。
- `key_events`: 影响后续剧情的关键决策点清单。

## 存储位置
- 存档文件路径: `.agent/skills/game-manager-skill/assets/saves/latest_save.json`
- 历史记录 (可选): `.agent/skills/game-manager-skill/assets/saves/save_{timestamp}.json`
