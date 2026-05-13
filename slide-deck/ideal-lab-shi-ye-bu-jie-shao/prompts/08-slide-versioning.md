# Slide 08 — 版本管理与质量保障

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
Slide: 08 | Type: Content | Layout: comparison-matrix
Title: "版本管理与质量保障"

Narrative Goal:
  说明 ideal-lab 有严谨的版本管理和质量保障机制，不是随意发布的个人项目。

Key Content:

Left Section (55% width) — 版本策略表格:

Table Header (工程蓝背景, 白字):
  版本类型 | 标准 | 示例

Row 1 (浅灰蓝交替行):
  patch | 修 typo、补充说明、修脚本 bug | 1.0.0 → 1.0.1

Row 2:
  minor | 新增 Skill、可选配置、新 Provider | 1.0.0 → 1.1.0

Row 3 (浅灰蓝交替行):
  major | Skill 改名/删除、阶段编号变化、Schema 不兼容 | 1.0.0 → 2.0.0

Table note (小字):
  "Changeset 管理版本，GitHub Actions 自动化校验和发布"

Right Section (45% width) — 质量保障流程图:

Vertical flowchart:
  Node 1: "提交改动" — 深藏青背景
  ↓
  Node 2: "维护工具自动检测变更范围" — 浅灰蓝背景
  ↓
  Node 3: "生成 Changeset" — 浅灰蓝背景
  ↓
  Node 4: "Bump 版本号" — 浅灰蓝背景
  ↓
  Node 5: "CI 校验结构完整性" — 工程蓝背景
  ↓
  Node 6: "合并发布" — 绿色 (#10B981) 背景

Bottom Section — 两张要点卡片 (并排):

Card 1: "版本可追溯"
  - 任何 Skill 的任何一次变更都有记录
  - 可以回溯到具体的改动内容

Card 2: "更新可控"
  - minor 版本保证向后兼容
  - major 版本提前说明不兼容变更点
  - 给足迁移时间

Visual Description:
  - 左侧是结构化表格，3 行，交替浅灰蓝背景
  - 右侧是垂直流程图，6 个节点 + 箭头
  - 底部两张并排卡片
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
