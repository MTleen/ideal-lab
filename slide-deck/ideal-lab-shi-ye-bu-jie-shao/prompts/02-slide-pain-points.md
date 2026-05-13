# Slide 02 — 真实场景里的反复困扰

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
Slide: 02 | Type: Content | Layout: bullet-list
Title: "真实场景里的反复困扰"

Narrative Goal:
  让受众立即产生共鸣——这些痛点是日常工作中真实存在的，不是假设。

Key Content (4 pain-point cards arranged in 2x2 grid):

Row 1, Card 1 (red left border, danger color):
  标题: "技术方案写作"
  内容:
  - 从空白文档到初稿往往需要大半天
  - 反复修改结构、补充论据、调整措辞
  - 改完一版回头看，逻辑链条又断了

Row 1, Card 2 (red left border, danger color):
  标题: "PPT 制作"
  内容:
  - 从零开始排版、选风格、配图
  - 一份 20 页的汇报材料吃掉两三天
  - 排版耗时远超内容本身

Row 2, Card 3 (red left border, danger color):
  标题: "代码评审"
  内容:
  - 常常变成"扫一眼、打个 LGTM"的走过场
  - 没有结构化的评审框架
  - 质量完全依赖个人经验和投入时间

Row 2, Card 4 (red left border, danger color):
  标题: "经验传承"
  内容:
  - 一个项目踩过的坑，下一个项目从头再来
  - 总结的写法、验证过的方案没有系统化保留
  - 团队知识随人员流动而流失

Bottom quote (工程蓝斜体, 14px):
  "这些不是假设性的场景，是我在日常工作中反复遇到的困扰。"

Visual Description:
  - 2x2 网格布局，每个卡片占 50% 宽度
  - 每个卡片顶部有红色 (#EF4444) 标题栏，白色文字
  - 卡片内用紧凑列表展示具体痛点
  - 卡片之间有 16px 间距
  - 整体浅灰蓝 (#F0F4F8) 背景
```

---

Produce the HTML now. Raw HTML only.
