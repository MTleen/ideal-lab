# Slide 18 — 两大开发辅助

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
Slide: 18 | Type: Content | Layout: two-columns
Title: "两大开发辅助"

Narrative Goal:
  介绍两个面向开发者的辅助工具——Ralph 做任务澄清，Maintainer 做仓库维护。

Key Content:

Left Column (50%, 工程蓝 #2563EB 顶栏):
  工具: ideal-ralph (v0.6.0)
  定位: 苏格拉底式任务澄清 + 持久小步迭代验证循环

  核心理念:
  "先想清楚再动手"

  工作流程:
  Step 1: 通过对话引导你明确任务
    - 输入是什么
    - 输出是什么
    - 验收标准是什么
    - 实施方式是什么
  Step 2: 生成任务合约 (contract)
  Step 3: 持久迭代循环逐步执行
    - 每一步验证是否满足验收标准

  关键特点:
  - 不隶属于 ideal-dev-workflow
  - 独立编排器，可调用任何 Skill 完成工作
  - 适合需要反复确认方向的复杂任务

  安装:
  claude plugin install ideal-ralph@ideal-lab
  调用: /ideal-ralph:ideal-ralph

Right Column (50%, 绿色 #10B981 顶栏):
  工具: ideal-lab-maintainer (v1.1.0)
  定位: ideal-lab 仓库维护工具

  四个核心能力:

  1. commit
     自动检测改动、生成 changeset、bump 版本

  2. add-skill
     新增 Skill 模板

  3. release
     发布流程

  4. validate
     校验所有插件结构完整性

  目标用户:
  ideal-lab 的开发者和管理员

  安装:
  claude plugin install ideal-lab-maintainer@ideal-lab
  调用: /ideal-lab-maintainer:ideal-lab-maintainer

Visual Description:
  - 左右两列等宽
  - 左列工程蓝色调，右列绿色调
  - 每列顶部彩色标题栏
  - 列内用步骤/列表紧凑排列
  - 代码块用深色背景白色等宽字体
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
