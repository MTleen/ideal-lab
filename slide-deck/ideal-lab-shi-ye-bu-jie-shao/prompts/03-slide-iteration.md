# Slide 03 — 踩坑→总结→固化→复用→再迭代

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
Slide: 03 | Type: Content | Layout: linear-progression
Title: "踩坑 → 总结 → 固化 → 复用 → 再迭代"

Narrative Goal:
  展示 ideal-lab 的核心成长方法论——不是先画架构图再填内容，而是从痛点出发逐步生长。

Key Content:

Top Section — Horizontal 5-step progression (占页面 35%):
  Step 1: "踩坑" — 红色 (#EF4444) 节点
    标注: "AI 输出质量不稳定"
  → 箭头
  Step 2: "总结" — 琥珀色节点
    标注: "发现薄弱点，总结原因"
  → 箭头
  Step 3: "固化" — 工程蓝 (#2563EB) 节点
    标注: "写成规范、流程、模板"
  → 箭头
  Step 4: "复用" — 绿色 (#10B981) 节点
    标注: "下次直接调用，质量提升"
  → 箭头
  Step 5: "再迭代" — 深藏青 (#1E3A5F) 节点
    标注: "发现更好的做法，更新 Skill"

  右侧循环箭头: 从 Step 5 回到 Step 1（虚线，表示持续循环）

Bottom Section — 3 concrete examples (占页面 60%, 3 cards):

Card 1 (浅灰蓝背景):
  标题: "写作规范是怎么来的"
  内容:
  - 第一次用 AI 写文档：结构松散、深度不足
  - 原因：提示词不够具体（缺结构、深度、读者定义）
  - 固化：整理写作规范，下次直接喂给 AI
  - 结果：输出质量立刻提升一个档次

Card 2 (浅灰蓝背景):
  标题: "17 种 PPT 风格是怎么来的"
  内容:
  - 在实际做 PPT 过程中，发现不同场景需要不同视觉策略
  - 逐一沉淀为预设风格，形成 ideal-ppt-suite 的 17 种风格

Card 3 (浅灰蓝背景):
  标题: "4 种调研深度是怎么来的"
  内容:
  - 调研任务的时间预算和深度要求差异很大
  - quick 模式和 ultradeep 模式面向完全不同的使用场景
  - 逐一沉淀为 ideal-deep-research 的 4 种深度模式

Visual Description:
  - 顶部是水平流程图，5 个圆角矩形节点，箭头连接
  - 每个节点内部有两行文字：步骤名（大字）+ 标注（小字）
  - 底部 3 张等宽卡片并排，每张卡片顶部有工程蓝色标题栏
  - 卡片内用紧凑列表，13px 字体
```

---

Produce the HTML now. Raw HTML only.
