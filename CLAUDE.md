# CLAUDE.md - 武侠游戏 (Wuxia RPG) 架构准则

此文件定义了本项目的核心架构与运转逻辑，是 Claude Code 的“指南针”。

## 1. 核心运转机制：Agent Skills
本项目采用模块化的 **Agent Skills** 架构。所有游戏实体（主角、NPC、规则、地理）均为独立 Skill。

### 1.1 技能结构标准 (`.agent/skills/`)
每个 Skill 必须包含：
- `SKILL.md`: 当前 Skill 的专业指令与业务逻辑约束。
- `references/`: 核心数据表 (.md)。
- `scripts/`: 驱动逻辑与数据校验脚本。

## 2. 叙事工作流 (Narrative Workflow)
生成任何剧情前，必须遵循以下闭环：

1. **前置校测 (Prep)**: 
   - 调用 `story-prep-skill` 获取当前主角、NPC 及环境的快照。
2. **文本生成 (Engine)**: 
   - 由 `story-engine` 基于快照生成万字情节，杜绝概括性占位符。
3. **写入与展示 (Display)**: 
   - 调用 `story-display-skill` 将情节写入文件、校验成功后通过原生终端指令展示。
4. **全局同步 (Sync)**: 
   - 触发 `game-manager-skill` 的同步钩子，根据剧情更新各 Skill 数据。

## 3. 原子化持久化 (Atomic Persistence)
为了防止数据损坏或路径幻觉，存档与读档必须遵循以下原则：

- **SQLite 中心化**: 所有 Skill 的 `references/` 数据在存档时必须同步至 `.agent/skills/game-manager-skill/assets/saves/wuxiaX.db`。
- **差异同步原则**: 读档时，必须以数据库为准，自动识别并强制覆盖本地有差异的 Skill 实体文件（由 `manager.py` 处理）。
- **指令调用**:
  - `/game-save`: 触发全量数据库存档。
  - `/game-load`: 从数据库恢复状态。

## 4. 维护规范
- **业务细节下沉**: 具体的武学数值、NPC 好感度逻辑、空间节点详情必须保留在各自 Skill 的文档中，`CLAUDE.md` 不记录具体数值。
- **原子更新**: 修改 `references/` 必须即时，并确保存档时被正确捕捉。

> [!IMPORTANT]
> **严禁路径幻觉**。所有持久化写入必须通过相应 Skill 的脚本接口执行。
