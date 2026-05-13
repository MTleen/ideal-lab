# Slide 16 — 四大工作流套件

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
Slide: 16 | Type: Content | Layout: bento-grid
Title: "四大工作流套件"

Narrative Goal:
  展示 4 个核心工作流套件——编排器 + Phase Skill 的组合，可一键全流程也可单步精细化。

Key Content:

2x2 Bento Grid (每个格子是一个工作流卡片):

Card 1 (左上, 工程蓝 #2563EB 顶栏):
  插件: ideal-dev-workflow (v1.1.0)
  Skill 数: 14 Skills
  定位: 15 阶段开发流程：从需求到交付

  核心阶段:
  需求 → 技术方案 → 编码计划 → 测试用例 → 开发执行 → 代码评审 → 测试执行 → 维基更新 → 成果提交

  适用场景:
  功能开发、Bug 修复、重构任务

  安装: claude plugin install ideal-dev-workflow@ideal-lab

Card 2 (右上, 绿色 #10B981 顶栏):
  插件: ideal-ppt-suite (v1.0.0)
  Skill 数: 9 Skills
  定位: PPT 全链路生成，17 种预设风格

  核心阶段:
  调研 → 策略（八确认） → 大纲（金字塔原理） → 提示词工程 → 生成 → AI 配图 → PPTX 导出

  适用场景:
  方案汇报、产品路演、培训课件

  安装: claude plugin install ideal-ppt-suite@ideal-lab

Card 3 (左下, 琥珀色 #D97706 顶栏):
  插件: ideal-document-workflow (v1.0.0)
  Skill 数: 8 Skills
  定位: 12 阶段结构化文档写作

  核心阶段:
  需求分析 → 大纲 → 任务拆分 → 并行写作 → 智能配图 → 渲染输出

  适用场景:
  技术文档、方案文档、知识沉淀

  安装: claude plugin install ideal-document-workflow@ideal-lab

Card 4 (右下, 紫色 #7C3AED 顶栏):
  插件: ideal-knowledge-base (v1.0.0)
  Skill 数: 6 Skills
  定位: 知识库构建编排

  核心阶段:
  材料分析 → 文档规划 → 并行生成 → 汇总评审

  适用场景:
  项目知识沉淀、团队 Wiki 构建、技术积累

  安装: claude plugin install ideal-knowledge-base@ideal-lab

Bottom note (12px, 深藏青):
  "四个套件共享相同的设计模式：手动模式下每阶段确认后推进，YOLO 模式下自动运行直到完成或触发熔断。"

Visual Description:
  - 2x2 网格，每个格子是一个工作流卡片
  - 每张卡片有不同颜色的顶部标题栏
  - 卡片内紧凑排列：版本、Skill数、阶段流程、场景、安装命令
  - 卡片间 16px 间距
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
