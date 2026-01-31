---
name: world-logic
description: 处理《河洛群侠传》MUD 文本江湖的空间节点系统（Spatial Node System）与时间轮转系统（Time-State System）。负责房间描述、方位导航、昼夜交替动作以及基于时间的事件触发。
---

# 文本江湖：空间与时间逻辑 (World Logic)

本 Skill 是文本江湖的底层架构，决定了玩家如何感知世界和时间的流动。

## 1. 空间节点系统 (Spatial Node System)

世界由相互连接的“房间（Room）”组成。每个导航动作（move north/south/east/west）都会改变当前所在的节点。

### 核心属性
- **环境描述 (Description)**：通过精炼的文字展现视觉感知。
- **出口方向 (Exits)**：定义可通行方位。
- **对象与互动 (Interactions)**：房间内的物品、NPC 或可搜索点。
- **隐藏判定**：部分对象（如埋藏的铁石）需通过 `search` 或 `look` 动作发现。

### 地理档案参考
- **区域划分**：具体房间细节见 [references/spatial_nodes.md](references/spatial_nodes.md)。
- **核心中心**：拱石村、漱玉矶、大研镇、武当山、少林寺、天水城、名剑山庄、十万大山等。
- **区域内容**：每个区域包含资源分布、常驻 NPC、相关势力等完整信息。

## 2. 时间轮转系统 (Time-State System)

游戏内置全局时钟，昼夜交替影响 NPC 行为和剧情触发。

### 时段划分
- **白天 (Day)**：NPC 正常活动，店铺营业。
- **黑夜 (Night)**：特殊 NPC（如盗墓兄弟）出现，视野受限，潜行加成。

### 逻辑触发
- 每次玩家执行移动或长时间动作，时钟推进。
- 具体时间影响表见 [references/time_events.md](references/time_events.md)。

## 3. 交互指令集 (Interaction Parser)

将视觉操作转化为文本指令：
- `look [target]`：观察环境或特定对象。
- `search [ground/object]`：搜寻隐藏物。
- `gather/mine`：采集资源。
- `jump up / climb`：地形穿越（需轻功判定）。

## 4. 江湖律令 (World Rules)
定义了人格、善恶、势力及奇遇的底层逻辑，确保世界运行符合武侠逻辑。
见 [references/world_rules.md](references/world_rules.md)。

## 5. 蝴蝶效应与因果联动 (Butterfly Effect & Causality)
> **必须遵守 (Mandatory)**
生成剧情内容**之前**，必须执行以下检查流程：
1. **检索因果链**: 读取 `world-logic/references/causality_chain.md`，检查当前场景或涉及人物是否存在已种下的“蝴蝶之种”。
2. **判定连锁反应**:
   - 若当前剧情处于“风暴预警”范围，强制触发对应的分支情节。
   - 根据历史抉择的“因果值”，调整当前互动的难度、报酬或NPC态度。
3. **记录新种**: 玩家做出重大决策后，必须立即在 `causality_chain.md` 中新增记录，并标记为“已种下”。
4. **变局触发**: 当全局“因果值”累积达到特定阈值（如50），在当前章节强制嵌入“江湖大变局”叙事。

## 6. 河图洛书碎片触发规则 (Hetu Luoshu Triggers)
> **必须遵守 (Mandatory)**
当主角进入碎片所在区域时，必须执行以下检查流程：
1. **位置匹配**: 检查当前位置是否为碎片分布点（参照 `references/spatial_nodes.md` 中的碎片分布总览）。
2. **条件判定**: 验证主角是否满足该碎片的前置条件（装备、属性、任务进度等）。
3. **碎片叙事**: 若满足条件，从 `story-engine/references/hetu_luoshu.md` 读取对应碎片的专属叙事模板。
4. **状态更新**:
   - 将碎片添加至 `character_sheet.md` 背包。
   - 应用碎片属性加成。
   - 更新 `hetu_luoshu.md` 中的收集状态。
5. **线索生成**: 若主角持有【河图·乾位残片】，在相邻区域存在未收集碎片时，生成感应描述。

## 7. 门派势力系统 (Sect & Faction System)
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

## 资源参考
- [空间节点数据](references/spatial_nodes.md)
- [门派势力档案](references/sect_list.md)
- [时间事件逻辑](references/time_events.md)
- [江湖律令法则](references/world_rules.md)
