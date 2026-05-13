# Slide 23 — 推荐起步路径

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
Slide: 23 | Type: Content | Layout: three-columns
Title: "推荐起步路径"

Narrative Goal:
  为三种角色提供具体的 3 步起步路径，让受众知道"下一步做什么"。

Key Content:

Three Columns (各占 33%):

Column 1 (工程蓝 #2563EB 顶栏):
  角色: "开发工程师"

  Step 1:
    安装 ideal-ralph
    用它澄清一个你手头任务的验收标准
    体验"先想清楚再动手"

  →

  Step 2:
    安装 ideal-dev-workflow
    选一个小功能任务走一遍完整流程
    体验 15 阶段开发流程

  →

  Step 3:
    体验 ideal-yolo 的多视角自动评审
    对比人工评审的差异
    感受评审团队的威力

Column 2 (绿色 #10B981 顶栏):
  角色: "产品/管理"

  Step 1:
    安装 ideal-deep-research
    选一个你关心的行业话题
    做一次 standard 模式调研

  →

  Step 2:
    安装 ideal-ppt-suite
    基于调研结果生成一份汇报 PPT
    体验 17 种预设风格

  →

  Step 3:
    尝试 YOLO 模式
    体验从调研到 PPT 的全自动流程
    感受一键生成的效率

Column 3 (琥珀色 #D97706 顶栏):
  角色: "技术写作"

  Step 1:
    安装 ideal-document-workflow
    选一个你正在写的文档走一遍完整流程
    体验 12 阶段文档写作

  →

  Step 2:
    重点关注评审环节
    读者、作者、专家三个视角分别给出了什么反馈
    理解评审设计的价值

  →

  Step 3:
    安装 ideal-knowledge-base
    尝试从现有项目材料中构建知识库
    体验知识沉淀流程

Visual Description:
  - 3 列等宽布局
  - 每列顶部有不同颜色的标题栏，标注角色名
  - 每列内 3 步垂直流程，步骤之间用向下箭头连接
  - 每步是一个小卡片，内有操作和体验目标
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
