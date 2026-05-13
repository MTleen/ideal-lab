# Slide 17 — 三大独立工具

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
Slide: 17 | Type: Content | Layout: three-columns
Title: "三大独立工具"

Narrative Goal:
  介绍 3 个独立工具——它们不属于工作流套件，但提供重要的单点能力。

Key Content:

Three Columns (各占 33%):

Column 1 (工程蓝 #2563EB 顶栏):
  工具: ideal-deep-research (v1.0.0)
  定位: 企业级深度调研

  4 种深度模式:
  - quick: 2-5 分钟快速扫描
  - standard: 5-10 分钟标准调研（默认）
  - deep: 10-20 分钟深度分析
  - ultradeep: 20-45 分钟全面审查

  调研管道 (8 阶段):
  SCOPE → PLAN → RETRIEVE → TRIANGULATE → OUTLINE → SYNTHESIZE → CRITIQUE → REFINE → PACKAGE

  质量要求:
  - 覆盖 10+ 信息源
  - 每条结论至少 3 条引用
  - 对信息源做可信度评分

  适用场景:
  竞品分析、技术选型、趋势调研

  安装:
  claude plugin install ideal-deep-research@ideal-lab
  调用: /ideal-deep-research:deep-research

Column 2 (绿色 #10B981 顶栏):
  工具: baoyu-image-gen (v1.0.0)
  定位: 多 Provider AI 图片生成

  支持的 Provider:
  - OpenAI (DALL-E)
  - Google (Imagen)
  - DashScope (通义万相)

  特点:
  - 按需切换 Provider
  - 统一调用接口

  适用场景:
  文档配图、PPT 插图、营销素材

  安装:
  claude plugin install baoyu-image-gen@ideal-lab
  调用: /baoyu-image-gen:baoyu-image-gen

Column 3 (琥珀色 #D97706 顶栏):
  工具: ideal-dify-generator (v1.0.0)
  定位: Dify 工作流 DSL 生成与校验

  能力:
  - 从需求描述出发
  - 自动生成 Dify DSL 规范的 YAML 配置
  - 语法校验 + 逻辑检查

  适用场景:
  快速搭建 Dify 工作流

  安装:
  claude plugin install ideal-dify-generator@ideal-lab
  调用: /ideal-dify-generator:ideal-dify-generator

Visual Description:
  - 3 列等宽布局
  - 每列顶部有不同颜色的标题栏
  - 列内紧凑排列：版本、模式/Provider/能力、场景、安装命令
  - ideal-deep-research 列内容最多，调研管道用小字水平排列
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
