# Slide 20 — 前置条件与安装

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
Slide: 20 | Type: Content | Layout: linear-progression
Title: "前置条件与安装"

Narrative Goal:
  展示从零开始安装 ideal-lab 的完整步骤——前置检查、添加源、安装插件。

Key Content:

Left Section (35%) — 前置条件检查:

Card (浅灰蓝背景):
  标题: "前置条件"

  Checklist:
  ✓ Claude Code 已安装
    验证: 终端运行 claude --version 可以输出版本号

  ✓ Anthropic API Key 已配置
    说明: Claude Code 首次启动时会引导你配置 API Key

  底部标注 (绿色):
    "以上条件已满足 → 直接进入安装"

Right Section (65%) — 3-step installation flow:

Step 1 (工程蓝顶栏):
  标题: "添加 Marketplace 源"
  代码块:
    claude plugin marketplace add https://github.com/MTleen/ideal-lab
  预期输出:
    ✓ Marketplace "ideal-lab" added successfully
      Source: https://github.com/MTleen/ideal-lab
      Plugins available: 9

→ 箭头

Step 2 (工程蓝顶栏):
  标题: "安装插件（推荐起步）"
  代码块:
    # 推荐：文档写作工作流（8 个 Skill）
    claude plugin install ideal-document-workflow@ideal-lab

    # 或者：深度调研工具
    claude plugin install ideal-deep-research@ideal-lab

    # 或者：PPT 全链路（9 个 Skill）
    claude plugin install ideal-ppt-suite@ideal-lab
  说明: "安装后 Skill 自动加载，无需额外配置"

→ 箭头

Step 3 (绿色 #10B981 顶栏):
  标题: "安装完成"
  ✓ Skill 自动加载
  ✓ 通过斜杠命令调用
  ✓ 无需额外配置

Visual Description:
  - 左侧前置条件卡片，用绿色勾号标记已满足条件
  - 右侧 3 步垂直流程，步骤之间用箭头连接
  - 代码块用深色背景白色等宽字体
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
