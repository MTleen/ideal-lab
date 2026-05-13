# Slide 01 — Cover

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
DENSITY: Fill the canvas. Minimize unused whitespace. Match the content density of a consulting slide.
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
Slide: 01 | Type: Cover | Layout: title-hero

Title: "ideal-lab"
Subtitle: "从日常工作中沉淀的 Claude Code 最佳实践插件库"

Hero Area (center, large typography):
  - Main title: "ideal-lab" — 深藏青 (#1E3A5F), 48px, bold
  - Subtitle line: "从日常工作中沉淀的 Claude Code 最佳实践插件库" — 工程蓝 (#2563EB), 20px
  - Divider line: 80px wide, 工程蓝 (#2563EB), 2px

Key Metrics Row (bottom third, 4 data cards in a row):
  Card 1: "9" 个插件 — 工程蓝底色标签
  Card 2: "42" 个 Skill — 工程蓝底色标签
  Card 3: "4" 大工作流 — 工程蓝底色标签
  Card 4: "Plugin Marketplace" 分发 — 工程蓝底色标签

Footer (bottom, small):
  - "ideal-lab 事业部介绍" | 左对齐
  - 深藏青小字, 12px

Design Notes:
  - 白色主背景, 无纹理
  - 左侧可有一条窄竖线装饰 (工程蓝 4px宽, 贯穿全高)
  - 整体风格：干净、专业、技术感
  - 没有照片、没有装饰图标、没有渐变
```

---

Produce the HTML now. Raw HTML only.
