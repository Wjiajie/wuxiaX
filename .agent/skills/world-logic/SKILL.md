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
- **核心中心**：拱石村、漱玉矶、大研镇。

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

## 资源参考
- [空间节点数据](references/spatial_nodes.md)
- [时间事件逻辑](references/time_events.md)
- [江湖律令法则](references/world_rules.md)
