---
name: combat-engine
description: 驱动《河洛群侠传》MUD 的回合制战斗系统。管理精力（AP）消耗、连击、反击、卸力判定，以及基于感悟系统的复合战斗文本生成。
---

# 战斗引擎 (Combat Engine)

## 1. 精力系统 (Action Points)
- 每个招式消耗固定 AP。
- 每回合开始根据【轻功】或【感悟】回复 AP。

## 2. 核心判定 (Combat Logic)
- **连击 (Combo)**: “动”系核心，攻击后一定概率再次出手、回复 AP。
- **反击 (Counter)**: “静”系核心，受击后尝试自动出招。
- **卸力 (Deflect)**: “柔”系核心，减免伤害并转移给周围敌人。
- **暴击 (Critical)**: “刚”系核心，造成爆发性伤害。

## 3. 方位与虚招
- **背击/侧击**: “巧”系核心，增加伤害或触发特殊效果。
- **虚招**: 扰乱敌人防御。

## 4. 文字战斗流程
1. 系统提示当前回合（Player/NPC Turn）。
2. 输入招式指令（如：`use yelllow_ball_punching`）。
3. 根据 [insight-skill] 计算加成。
4. 输出一段动态叙事性的武侠动作描写。

## 资源参考
- [数值演算公式](references/formulas.md)
