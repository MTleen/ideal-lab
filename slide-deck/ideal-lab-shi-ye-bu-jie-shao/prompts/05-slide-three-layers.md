# Slide 05 — Plugin → Skill → References 三层架构

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
Slide: 05 | Type: Content | Layout: hierarchical-layers
Title: "Plugin → Skill → References 三层架构"

Narrative Goal:
  清晰展示 ideal-lab 的三层结构设计——每一层职责明确、自包含。

Key Content:

Left Section (60% width) — 三层纵向层级图:

Layer 1 (最上层, 工程蓝 #2563EB 背景, 白字):
  "Plugin（插件）"
  说明: "最大的能力单元，每个 Plugin 对应一个独立工作领域"
  示例标签: [ideal-dev-workflow] [ideal-ppt-suite] [ideal-document-workflow]
  特征: "Plugin 之间完全解耦，按需安装，不需要全量部署"

  ↓ 包含

Layer 2 (中间层, 深藏青 #1E3A5F 背景, 白字):
  "Skill（技能）"
  说明: "Plugin 内的执行单元，每个 Skill 做一件事"
  定义: "通过 SKILL.md 定义'做什么'和'怎么做'"
  特征: "一个 Plugin 下多个 Skill 按流程编排，形成完整工作流"

  ↓ 读取

Layer 3 (最下层, 浅灰蓝 #F0F4F8 背景, 深藏青字):
  "References / Scripts"
  references/: "参考文档（写作规范、模板、技术规格）"
  scripts/: "执行脚本（格式校验、文件转换、自动化工具）"
  特征: "Skill 执行时读取这些资源，确保输出符合预设标准"

Right Section (40% width) — 两个要点卡片:

Card 1: "透明可审计"
  - 任何 Skill 的行为通过阅读 SKILL.md 完整了解
  - 不需要逆向工程
  - 版本可追溯，变更可对比

Card 2: "职责分离"
  - Plugin 管领域边界
  - Skill 管具体执行
  - References 管标准资源
  - 三层独立迭代，互不影响

Visual Description:
  - 左侧是三层嵌套的层级图，每层用不同颜色区分
  - 层与层之间用向下箭头连接，标注关系（包含/读取）
  - 每层内部有具体说明文字和示例标签
  - 右侧两张卡片，浅灰蓝背景，顶部工程蓝标题栏
  - 整体白色背景
```

---

Produce the HTML now. Raw HTML only.
