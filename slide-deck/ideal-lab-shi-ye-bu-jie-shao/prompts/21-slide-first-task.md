# Slide 21 — 第一个任务：完整体验

## System Prompt

```
You are an expert presentation designer for technical/business reports.
Your slides are information-DENSE, structured, and data-driven.
Every element earns its place on the 1280x720 canvas.
```

## Output Rules

```
OUTPUT: One standalone HTML with inline CSS. No JS, no external resources.
CANVAS: body { width: 1280px; height: 720px; overflow: hidden; }
TEXT: ALL text must be real, readable HTML text — no SVG text for body copy
DENSITY: Fill the canvas. Minimize unused whitespace.
COLOR: Use CSS variables. Every color has a purpose.
FONT: System font stack: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif
```

---

## STYLE_INSTRUCTIONS

```
Design Aesthetic: Clean, digital precision with crisp edges. Cool analytical blues and grays. Technical sans-serif typography optimized for information density. Professional consulting-firm style with meaningful diagrams.

Background:
  Texture: Clean, pure white (#FFFFFF), no grid or texture
  Base Color: #FFFFFF

Typography:
  Headlines: Bold technical sans-serif with sharp geometric shapes, 28-32pt
  Body: Clean sans-serif, highly legible at 12-14pt for dense content
  Line height: 1.2-1.4 (compact)

Color Palette:
  Primary Text: 深藏青 (#1E3A5F) — 标题、重要文字
  Background: 白色 (#FFFFFF) — 主背景
  Accent 1: 工程蓝 (#2563EB) — 高亮、关键数据、章节头
  Accent 2: 浅灰蓝 (#F0F4F8) — 交替行、卡片填充
  Success: 绿色 (#10B981) — 正面指标
  Danger: 红色 (#EF4444) — 问题/风险

Visual Elements:
  - 流程图（节点内有文字标签，简洁箭头）
  - 对比布局（左右分栏，颜色区分）
  - 结构化表格（多维度信息）
  - 色块卡片（彩色顶部标题栏）
  - 层级/树状图（分类关系）
  严格禁止：装饰性图标、背景纹理、抽象插画

Density Guidelines:
  - 每页 6-8 个要点或等量图表+文字组合
  - 标题区精简，空间留给内容
  - 表格优于段落，箭头优于文字

Style Rules:
  Do: 保持一致的线条粗细，网格对齐，受限色板，清晰视觉层次
  Don't: 手绘元素，装饰性图标，背景纹理，圆形连接线，照片元素
```

---

## SLIDE CONTENT

```
Slide: 21 | Type: Content | Layout: linear-progression
Title: "第一个任务：完整体验"

Narrative Goal:
  用一个完整的 document-workflow 示例，展示"从一句话到交付物"的全过程。

Key Content:

Top — Input command (代码块):
  /ideal-document-workflow:ideal-document-workflow 帮我写一份"团队代码评审规范"介绍文档，目标读者是事业部开发团队，篇幅 1500 字左右

4-stage horizontal progression:

Stage 1 (工程蓝 #2563EB 顶栏):
  "阶段 1 — 需求确认"

  工作流行为:
  - 分析你的需求
  - 生成需求文档

  展示内容:
    需求分析完成，确认以下信息：
    - 文档主题：团队代码评审规范
    - 目标读者：事业部开发团队
    - 篇幅要求：约 1500 字
    - 写作风格：实用导向
    确认无误？(y/n，或补充修改意见)

  你的操作: 回复 y

→ 箭头

Stage 2 (深藏青 #1E3A5F 顶栏):
  "阶段 2 — 大纲审核"

  工作流行为:
  - 基于需求生成大纲
  - 暂停让你审核

  展示内容:
    大纲已生成：
    1. 为什么要做代码评审
    2. 评审流程（PR 提交 → 评审 → 修改 → 合并）
    3. 评审检查清单
    4. 常见问题与最佳实践
    确认大纲？(y/n，或补充修改意见)

  你的操作: 回复 y 或修改

→ 箭头

Stage 3 (浅灰蓝顶栏):
  "阶段 3 — 等待写作"

  工作流行为:
  - 并行写作各章节
  - 你不需要操作

  你的操作: 等待

→ 箭头

Stage 4 (绿色 #10B981 顶栏):
  "阶段 4 — 获得交付物"

  工作流行为:
  - 输出最终 Markdown 文档
  - 保存在你指定的路径

  预计耗时: 约 5-10 分钟
  你的参与: 2 个决策节点

Visual Description:
  - 顶部是用户输入命令的代码块
  - 中部是 4 个水平排列的阶段卡片，箭头连接
  - 每个阶段内展示具体的工作流行为和用户操作
  - 阶段 1 和 2 包含代码块样式的交互内容
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
