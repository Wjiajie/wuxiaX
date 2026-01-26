---
name: weapon-system
description: 管理武侠游戏中的武器系统，包括锻造、耐久度损耗及维修逻辑。当涉及玩家打造神兵、战斗中武器受损、或寻找铁匠修理武器时调用。
---

# 武器系统 (Weapon System)

本技能负责处理江湖中所有与神兵利器相关的核心逻辑。

## 核心功能

1. **武器锻造 (Forging)**：基于材料质量和铁匠等级生成武器属性。
2. **耐久度系统 (Durability)**：记录武器使用过程中的损耗及折损判定。
3. **修理与保养 (Repair)**：恢复耐久度及其对属性的影响。

## 武器属性结构 (Schema)
武器对象应包含以下属性：
- `id`: 唯一标识符
- `name`: 名称
- `base_damage`: 基础伤害
- `durability`: 当前耐久
- `max_durability`: 耐久上限
- `quality`: 品级（凡铁、利器、神兵）

## 损耗逻辑判定
具体计算公式见 [references/logic.md](references/logic.md)。
在战斗生成中，若触发“格挡”或“硬碰硬”，需调用脚本进行损耗计算。

## 接入说明
使用时需确保 `protagonist-skill` 中的背包数据包含上述结构。
