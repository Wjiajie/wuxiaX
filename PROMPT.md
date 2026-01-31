# 任务：完善地理区域与门派架构 (World Logic & Sect Integrity)

## 背景
NPC 名录 (`npc_list.md`) 已经通过融合《逸剑风云决》与《河洛群侠传》得到了极大扩充，但底层的地理空间 (`spatial_nodes.md`) 和门派设定尚未同步更新，导致新加入的 NPC 缺乏对应的环境支撑。

## 目标
根据最新的 NPC 数据，反向推导并补全地理与门派信息，构建一个逻辑自洽的宏大江湖。

## 执行步骤

### 1. 区域信息补全
**目标文件**: `.agent/skills/world-logic/references/spatial_nodes.md`
**数据源**: `.agent/skills/npc-skill/templates/npc_list.md`

遍历 `npc_list.md` 中涉及的所有地理标签（如“中原”、“西北”、“南疆”等），在 `spatial_nodes.md` 中补充或完善对应条目。
每个区域需包含以下维度：
- **资源 (Resources)**: 该区域特有的采集物（参照河洛设定，如玄铁、毒虫、特产酒类）。
- **相关 NPC (Related NPCs)**: 列出常驻此区域的核心 NPC 列表（自动同步 `npc_list.md` 的归属）。
- **兽王分布 (Beast Kings)**: 根据 `npc-skill/references/beast_kings.md`，将兽王标记在对应的区域节点中，作为危险或探索要素。
- **相关势力 (Related Factions)**: 该区域包含的门派、村落或城镇（如天水城之于神鹰门）。

### 2. 建立门派档案
**目标文件**: `.agent/skills/world-logic/references/sect_list.md` (新增)

创建一个全新的门派档案文件，详细描述江湖中的各大势力：
- **核心门派**: 武当、少林、丐帮、名剑山庄、神鹰门、五仙教、俏梦阁、赋闲书院、淘石帮。
- **Mod/隐世势力**: 圣堂、长生殿、雪山派、西域魔教。
- **档案结构**:
  - 门派名称与宗旨
  - 所在区域 (Linked Spatial Node)
  - 核心武学 (Linked Martial Arts)
  - 代表人物 (Linked NPCs)
  - 势力关系 (友好/敌对)

### 3. 更新 Skill 引用
**目标文件**: `.agent/skills/world-logic/SKILL.md`

在 `world-logic` 的 SKILL 定义中增加对新数据的引用：
- 在“地理档案参考”部分，明确 `spatial_nodes.md` 已包含 NPC 和资源分布。
- 新增“门派势力系统”章节，引用 `references/sect_list.md`，说明门派对江湖生态的影响。

## 验收标准
- `spatial_nodes.md` 覆盖所有 NPC 所在的区域，无“悬空”角色。
- `sect_list.md` 包含至少 30 个主要门派的详细设定。
- 所有地理和门派描述均符合《逸剑》与《河洛》的融合世界观。
