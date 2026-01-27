---
name: quest-skill
description: 用于记录、追踪与更新游戏主线及支线任务的技能系统。
---

# 任务追踪系统 (Quest System)

## 概述
此技能负责维护主角在江湖中的所有任务进度，确保故事生成的连续性与一致性。它是“江湖百晓生”的核心组件，防止遗忘前尘往事。

## 核心职责
1. **任务记录**：在 `references/quest_log.md` 中维护主线与支线列表。
2. **状态更新**：根据剧情推演结果，实时更新任务的【触发】、【进行中】、【已完成】或【已失败】状态。
3. **因果联动**：将任务状态与 `world-logic/references/causality_chain.md` 进行关联。

## 交互准则
- 每次生成剧情前，必须读取 `references/quest_log.md` 以获知当前的因果节点。
- 剧情生成后，若涉及任务状态变更或新任务开启，必须调用 `scripts/quest_manager.py`：
  - 更新状态：`python .agent/skills/quest-skill/scripts/quest_manager.py --update "任务名" --status "已完成/已失败" --progress "具体进度描述"`
  - 添加新任务：`python .agent/skills/quest-skill/scripts/quest_manager.py --add "新任务名" --category "Main/Side" --desc "任务描述" --relations "相关人物/地点"`
- 剧情中涉及的关键抉择，必须通过上述脚本即时反馈至任务状态。
