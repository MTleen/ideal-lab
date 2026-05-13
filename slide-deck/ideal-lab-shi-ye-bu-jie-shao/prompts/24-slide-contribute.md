# Slide 24 — 反馈与共建

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
Slide: 24 | Type: Content | Layout: bullet-list
Title: "反馈与共建"

Narrative Goal:
  告诉受众如何参与 ideal-lab 的共建——反馈、贡献 Skill、分享经验。

Key Content:

Left Section (50%) — 三种参与方式:

Card 1 (工程蓝 #2563EB 顶栏):
  标题: "问题反馈"

  说明:
  - 使用过程中发现问题或有改进建议
  - 通过 GitHub Issue 描述你遇到的问题
  - 包含：使用场景、预期行为、实际行为、复现步骤

  参与门槛: 低
  适合: 所有使用者

Card 2 (绿色 #10B981 顶栏):
  标题: "Skill 共建"

  说明:
  - 如果你在日常工作中沉淀出了一套好用的流程
  - 按照 ideal-lab 的 Plugin 结构封装为新的 Skill
  - 通过 PR 提交

  参与门槛: 中
  适合: 有开发经验的同事

  共建流程:
  问题反馈 → 流程总结 → Skill 封装 → PR 提交 → 评审合并

Card 3 (琥珀色 #D97706 顶栏):
  标题: "经验分享"

  说明:
  - 使用 ideal-lab 产出的文档、PPT、调研报告
  - 这些本身就是最好的经验沉淀
  - 分享使用心得和最佳实践

  参与门槛: 低
  适合: 所有使用者

Right Section (50%) — 理念说明:

Card (浅灰蓝背景):
  标题: "ideal-lab 是持续迭代的活系统"

  核心理念:
  - 不是一次性的交付物，而是持续演进的平台
  - 每个使用者的反馈都是改进的输入
  - 每个人沉淀的流程都可以成为新的 Skill

  反馈循环图:
  使用 → 发现问题/更好的做法 → 反馈/贡献 → 更新 Skill → 所有人受益

  Key message (工程蓝大字):
  "你在使用中发现更好的做法，就是下一次迭代的起点。"

Visual Description:
  - 左侧 3 张参与方式卡片，不同颜色顶栏
  - 右侧理念说明卡片 + 反馈循环图
  - 反馈循环用 4 个节点 + 箭头的环形图表示
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
