# Slide 07 — Marketplace 三步安装

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
Slide: 07 | Type: Content | Layout: linear-progression
Title: "Marketplace 三步安装"

Narrative Goal:
  展示从零开始使用 ideal-lab 只需三步——添加源、安装插件、调用命令。

Key Content:

Horizontal 3-step progression (每步占 33%, 浅灰蓝卡片):

Step 1 Card (工程蓝顶栏):
  标题: "第一步：添加 Marketplace 源"
  代码块 (深藏青背景, 白色等宽字体):
    claude plugin marketplace add https://github.com/MTleen/ideal-lab
  说明:
    - 告诉 Claude Code 从哪里获取插件清单和安装包
    - 只需执行一次

→ 大箭头连接

Step 2 Card (工程蓝顶栏):
  标题: "第二步：按需安装插件"
  代码块:
    # 文档写作工作流（8 个 Skill）
    claude plugin install ideal-document-workflow@ideal-lab

    # 深度调研工具
    claude plugin install ideal-deep-research@ideal-lab

    # PPT 全链路（9 个 Skill）
    claude plugin install ideal-ppt-suite@ideal-lab
  说明:
    - 每个插件独立安装，用哪个装哪个
    - 不需要全量安装

→ 大箭头连接

Step 3 Card (工程蓝顶栏):
  标题: "第三步：斜杠命令调用"
  代码块:
    /ideal-document-workflow:ideal-document-workflow
    /ideal-deep-research:deep-research
    /ideal-ppt-suite:ideal-ppt-workflow
  说明:
    - 安装后 Skill 自动加载
    - 调用编排器即可自动走完整个流程

Bottom note (工程蓝小字, 12px):
  "每个工作流插件都有编排器 Skill，调用编排器即可自动走完整个流程，无需逐阶段手动触发。"

Visual Description:
  - 3 张等宽卡片水平排列，之间用粗箭头连接
  - 每张卡片顶部工程蓝色标题栏，白色标题文字
  - 卡片内代码块用深色背景 + 白色等宽字体
  - 代码块下方是简洁的说明文字
  - 白色页面背景
```

---

Produce the HTML now. Raw HTML only.
