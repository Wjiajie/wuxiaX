# CLAUDE.md - 武侠游戏 (Wuxia RPG) 架构准则

此文件定义了本项目的核心架构与运转逻辑，是 Claude Code 的“指南针”。

## 规则分布 (Rule Distribution)
本项目不再使用独立的 `rules/` 文件，核心业务规则已下沉至各 Skill。主要职能如下：

### 核心叙事与逻辑
- **story-engine**: 负责“说书人”叙事逻辑、情节生成及初始引导。
- **quest-skill**: 维护江湖任务志，确保因果连续性（Persistence of Narrative）。
- **world-logic**: 掌管江湖时空法则（地图/时间）及“蝴蝶效应”因果链。
- **game-manager-skill**: 控制游戏生命周期、存档/读档及全局状态同步。

### 角色与生态
- **protagonist-skill**: 维护主角属性、四维人格数值及河图洛书碎片加成。
- **npc-skill**: 管理 NPC 交互、好感度计算公式及队友羁绊系统。
- **combat-engine**: 处理回合制战斗判定（AP、连击、反击）。

### 成长与物品
- **martial-arts-skill** & **insight-skill**: 定义武学秘籍与感悟天赋体系。
- **item-skill** & **weapon-system**: 管理道具、传说武器锻造及耐久度。

## 0. 全局必须遵守规则 (Global Mandatory Rules)
1. **语言必须为中文**：任何时刻，请都用中文回答用户。
2. **Skill 优先**：当用户提出需求时，优先检索项目是否有相关的 skills (`.agent/skills`)，并严格遵循对应 SKILL.md 的流程。

## 1. 核心运转机制：Agent Skills
本项目采用模块化的 **Agent Skills** 架构。所有游戏实体（主角、NPC、规则、地理）均为独立 Skill。

### 1.1 技能结构标准 (`.agent/skills/`)
每个 Skill 必须包含：
- `SKILL.md`: 当前 Skill 的专业指令与业务逻辑约束。
- `references/`: 核心数据表 (.md)。
- `scripts/`: 驱动逻辑与数据校验脚本。

## 2. 叙事工作流 (Narrative Workflow)
生成任何剧情或章节前，必须遵循以下闭环：

0. **引擎加载 (Load Engine)**: 
   - **必须**优先读取 `story-engine/SKILL.md`。
1. **执行流程 (Execute Workflow)**:
   - 严格遵循 `story-engine/SKILL.md` 中的定义执行所有步骤（含状态判定、前置校测、写入展示与同步）。具体细节以该 Skill 文档为准，此处不作冗余记录。

## 3. 原子化持久化 (Atomic Persistence)
为了防止数据损坏或路径幻觉，存档与读档必须遵循以下原则：

为了防止数据损坏或路径幻觉，存档与读档必须遵循 `game-manager-skill/SKILL.md` 中的定义。
- **SQLite 中心化**: 严格以数据库为唯一真值来源。
- **原子操作**: 所有读写均由 `game-manager-skill` 提供的脚本接口完成。

## 4. 维护规范
- **业务细节下沉**: 具体的武学数值、NPC 好感度逻辑、空间节点详情必须保留在各自 Skill 的文档中，`CLAUDE.md` 不记录具体数值。
- **原子更新**: 修改 `references/` 必须即时，并确保存档时被正确捕捉。

> [!IMPORTANT]
> **严禁路径幻觉**。所有持久化写入必须通过相应 Skill 的脚本接口执行。
