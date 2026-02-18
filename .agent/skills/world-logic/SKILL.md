---
name: world-logic
description: 负责构建宏大的武侠文本江湖。处理区域地理（Spatial Nodes）、门派势力（Sect System）与时间流转（Time-State）。核心职责包括维护世界观的一致性，确保 NPC、地理与门派信息的准确检索与调用。
---

# 文本江湖：空间与时间逻辑 (World Logic)

本 Skill 是文本江湖的底层架构，决定了玩家如何感知世界和时间的流动。

## 1. 空间节点系统 (Spatial Node System)

世界由相互连接的“区域（Region）”组成。玩家通过指令在不同区域间穿梭，无需关注具体的东南西北方位。

### 核心属性
- **环境描述 (Description)**：通过精炼的文字展现视觉感知。
- **出口方向 (Exits)**：定义可通行方位。
- **对象与互动 (Interactions)**：房间内的物品、NPC 或可搜索点。
- **隐藏判定**：部分对象（如埋藏的铁石）需通过 `search` 或 `look` 动作发现。

### 地理档案参考
详细的区域划分与内容设定，请直接参考 [references/spatial_nodes.md](references/spatial_nodes.md)。

## 2. 时间轮转系统 (Time-State System)

游戏内置全局时钟，昼夜交替影响 NPC 行为和剧情触发。

### 时段划分
- **白天 (Day)**：NPC 正常活动，店铺营业。
- **黑夜 (Night)**：特殊 NPC（如盗墓兄弟）出现，视野受限，潜行加成。

### 逻辑触发
- 每次玩家执行移动或长时间动作，时钟推进。
- 具体时间影响表见 [references/time_events.md](references/time_events.md)。
- 每日卯时（日出）自动触发情报更新：
  `python .agent/skills/intelligence-skill/scripts/intelligence_manager.py --update_daily`
- 玩家可通过"查看情报"指令手动获取最新情报

## 3. 交互指令集 (Interaction Parser)

将视觉操作转化为文本指令：
- `look [target]`：观察环境或特定对象。
- `search [ground/object]`：搜寻隐藏物。
- `gather/mine`：采集资源。
- `jump up / climb`：地形穿越（需轻功判定）。

## 4. 江湖律令 (World Rules)
定义了人格、善恶、势力及奇遇的底层逻辑，确保世界运行符合武侠逻辑。
见 [references/world_rules.md](references/world_rules.md)。


## 5. 门派势力系统 (Sect & Faction System)
> **必须遵守 (Mandatory)**

门派势力是江湖生态的核心组成部分，影响 NPC 行为、剧情走向和玩家声望。

### 势力分类
- **正道门派**：武当、少林、丐帮、名剑山庄、赋闲书院等，侠义为先
- **中立势力**：神鹰门、马帮、采玉帮、俏梦阁等，利益优先
- **邪道势力**：五仙教、西域魔教、长生殿等，各有所图
- **隐世势力**：圣堂、先民部落、雪山派等，远离尘世

### 势力交互规则
1. **声望影响**：玩家行为会改变与各势力的关系，影响 NPC 态度和任务获取
2. **门派冲突**：部分门派存在敌对关系，帮助一方可能得罪另一方
3. **势力领地**：进入门派领地时，根据声望触发不同的遭遇事件
4. **门派武学**：高声望可解锁门派秘传武学和装备

### 势力档案参考
完整的门派设定见 [references/sect_list.md](references/sect_list.md)，包含：
- 34 个主要门派的详细档案
- 势力关系网络图
- 核心武学与代表人物

## 6. 信息检索协定 (Information Retrieval Protocol)
> **必须遵守 (Mandatory)**

当故事发展涉及以下要素时，**必须**优先检索对应的档案库，以确保世界观的连贯性：

### 8.1 涉足新区域 (Entering Regions)
当主角抵达或提及某个地名时：
1. **检索目标**: `world-logic/references/spatial_nodes.md`
2. **提取要素**:
   - **环境特征**: 确保描写符合（如“雪山峭壁”不能写成“郁郁葱葱”）。
   - **资源分布**: 确认该地特产（如“五毒虫”仅在南疆）。
   - **兽王威胁**: 检查该区域是否有兽王盘踞（如“白马居”附近的狼王）。
   - **常驻 NPC**: 确认谁是这里的地头蛇。

### 8.2 遭遇 NPC (Encountering NPCs)
当主角与 NPC 互动时：
1. **检索目标**: `npc-skill/references/npc_list.md`
2. **提取要素**:
   - **身份与性格**: 确保言行一致。
   - **美学与生理** (女性): 若涉及细致描写，必须引用档案中的“美学采样”与“生理快照”。
   - **门派归属**: 确认其背后的势力立场。

### 8.3 门派交互 (Sect Interactions)
当主角与门派发生关联（拜访、冲突、任务）时：
1. **检索目标**: `world-logic/references/sect_list.md`
2. **提取要素**:
   - **所处据点**: 确认门派的具体位置。
   - **外交立场**: 确认该门派是正是邪，与主角当前声望是否冲突。
   - **核心武学**: 确保战斗或切磋时使用的招式符合门派传承。

## 资源参考
- [空间节点数据](references/spatial_nodes.md)
- [门派势力档案](references/sect_list.md)
- [时间事件逻辑](references/time_events.md)
- [江湖律令法则](references/world_rules.md)
- [情报系统](../intelligence-skill/SKILL.md)
