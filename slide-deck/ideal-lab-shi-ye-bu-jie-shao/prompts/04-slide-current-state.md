# Slide 04 — ideal-lab 今天的样子

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
Slide: 04 | Type: Content | Layout: dashboard
Title: "ideal-lab 今天的样子"

Narrative Goal:
  一页展示 ideal-lab 的全貌——数字、价值链、覆盖范围一目了然。

Key Content:

Top Row — 3 KPI Cards (占页面 25%):
  Card 1: "9" — 个插件 (工程蓝大字 36px)
  Card 2: "42" — 个 Skill (工程蓝大字 36px)
  Card 3: "1" — 句话定位: "从日常工作中沉淀的 Claude Code 最佳实践插件库"

Middle Section — 价值链流程 (占页面 35%):
  水平 4 步流程:
  Step 1: "标准化" — 浅灰蓝底
    描述: "把反复验证有效的做法固化为标准流程，避免每次重新摸索"
  → 箭头
  Step 2: "可复用" — 浅灰蓝底
    描述: "标准化之后的流程变成 Skill，任何项目都可以直接调用"
  → 箭头
  Step 3: "质量保障" — 浅灰蓝底
    描述: "每个工作流内嵌评审和校验环节，不依赖个人的认真程度"
  → 箭头
  Step 4: "持续迭代" — 浅灰蓝底
    描述: "在使用中发现更好的做法，更新 Skill，所有使用者同步受益"

Bottom Section — 覆盖场景 Grid (占页面 35%, 2 rows x 3 cols):
  Row 1:
    - 开发流程 (ideal-dev-workflow)
    - PPT 生成 (ideal-ppt-suite)
    - 文档写作 (ideal-document-workflow)
  Row 2:
    - 知识库构建 (ideal-knowledge-base)
    - 深度调研 (ideal-deep-research)
    - 更多场景持续扩展中...

Visual Description:
  - 顶部 3 张 KPI 卡片水平排列，白色背景，工程蓝数字
  - 中部价值链用 4 个方框 + 箭头展示，方框内有关键词和一行描述
  - 底部 6 个小色块卡片，2 行 3 列网格，每个标注插件名和场景
  - 整体白色背景，结构清晰
```

---

Produce the HTML now. Raw HTML only.
