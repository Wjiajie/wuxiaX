---
name: story-prep-skill
description: 专门用于故事情节生成前的前置准备工作。通过 Python 脚本检测主角状态、NPC 状态及当前环境因素，为叙事提供精确的上下文快照。
---

# 故事生成前置准备 (Story Preparation Skill)

## 概述
本技能负责在 `story-engine` 开始构思故事情节之前，对当前江湖世界进行一次“体检”。它采集所有必要的状态数据，合成一份“叙事上下文快照”，确保说书人的叙事不偏离事实。

## 核心职责
1. **状态校测**：运行 `scripts/check_context.py`，实时解析主角属性、地理位置、伤病情况。
2. **NPC 侦测**：检索当前场景中存在的 NPC，获取其好感度等级及当前状态（如是否重伤、是否有未完成交互）。
3. **环境判定**：读取空间节点信息，确认当前时间（昼夜）、资源状况及潜在的事件触发条件。

## 使用流程
1. 在任何剧情生成行为开始之前，**必须**先调用本技能的脚本：
   `python .agent/skills/story-prep-skill/scripts/check_context.py`
2. 读取脚本输出的内容。
3. 将输出的内容作为“当前世界状态”输入给 `story-engine` 的 Prompt 头部。

## 脚本索引
- `scripts/check_context.py`: 执行全量状态扫描。
