---
description: 当和用户对话时，都会检查此描述
---

## 入口
你总是需要加载 ./agent/rules/story-gen-rules.md,来检查这个游戏的核心理念。

## 指令系统
需要识别下面的几个重要指令
/game-save: 保存当前的状态表，你需要用一个专门的skills来处理场景数据的本地持久化，包括更新相关的skills，以及长期记忆的存储（本地数据库）。
/game-load: 读取本地数据库最新的存储，加载相关的skills，方便继续游戏。
/game-restart: 重新开始游戏新一轮游戏，你需要设计一个skills，来和玩家交互，初始化主角的属性和最开始的场景。
/game-setting: 暂时退出游戏的剧情生成，根据和玩家的交互来修改对应的skills。