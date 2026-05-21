---
name: story-display-skill
description: 负责小说情节的持久化写入、生成校验以及终端的完整展示。通过 TUI 沉浸式阅读器呈现万字剧情。
---

# 小说情节展示技能 (Story Display Skill)

## 概述
本技能是”万言小说”最后落地的关键环节。它通过”写入 -> 校验 -> TUI 展示”的闭环，确保每一回剧情都能安全存盘并以沉浸式阅读体验呈现在玩家终端上。

## 核心职责
1. **稳健写入**：将 `story-engine` 生成的内容写入 `./history/chapters/`。
2. **落盘校验**：写入后通过脚本检测文件是否存在且字节数正常。
3. **TUI 沉浸展示**：基于 `rich` 库启动交互式阅读器，支持分页翻页、关键词高亮。

## TUI 阅读器功能
- **分页浏览**：PageUp/PageDown/方向键翻页
- **关键词高亮**：武学名(青)、武器名(黄)、地名(绿)、人名(紫)、境界(红)
- **进度指示**：底部显示当前页码和阅读进度
- **快捷键**：
  - `↑/b/k` - 上一页
  - `↓/f/j/空格` - 下一页
  - `g/G` - 跳转首/末页
  - `q/ESC` - 退出

## 使用流程
1. 当一章剧情生成完毕后，调用：
   `python .agent/skills/story-display-skill/scripts/display_chapter.py --chapter <N> --content “<CONTENT>” --finalize`
2. 脚本会自动处理写入、校验并启动 TUI 阅读器
3. 如需禁用 TUI 使用传统模式，添加 `--no-tui` 参数

## 脚本索引
- `scripts/display_chapter.py`: 处理核心写入、校验与展示分发
- `scripts/tui_viewer.py`: TUI 沉浸式阅读器实现
