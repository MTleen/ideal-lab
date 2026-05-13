# Slide 19 — 按角色推荐插件

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
Slide: 19 | Type: Content | Layout: comparison-matrix
Title: "按角色推荐插件"

Narrative Goal:
  让不同角色的受众快速找到适合自己的插件组合和起步路径。

Key Content:

Full-width comparison table:

Table Header (工程蓝背景, 白字):
  角色 | 推荐插件 | 起步建议

Row 1 (浅灰蓝交替行):
  开发工程师
  | ideal-dev-workflow + ideal-ralph + ideal-lab-maintainer
  | 先用 ralph 澄清一个开发任务的验收标准，再体验 dev-workflow 的完整流程

Row 2:
  产品经理
  | ideal-ppt-suite + ideal-deep-research
  | 先用 deep-research 做一次竞品调研，再用 ppt-suite 生成汇报 PPT

Row 3 (浅灰蓝交替行):
  技术写作
  | ideal-document-workflow + ideal-knowledge-base
  | 先用 document-workflow 写一份简短文档，体验评审机制

Row 4:
  项目经理
  | ideal-deep-research + ideal-ppt-suite + ideal-document-workflow
  | 用 deep-research 做项目前期调研，用 ppt-suite 做里程碑汇报

Right Side — 补充卡片 (如果空间允许):

Card: "组合使用建议"
  典型组合 1: deep-research → ppt-suite
    先调研再汇报
  典型组合 2: ralph → dev-workflow
    先澄清再开发
  典型组合 3: document-workflow → knowledge-base
    先写文档再沉淀知识

Visual Description:
  - 全宽对比表格，4 行
  - 交替浅灰蓝背景
  - 每行内容充实：角色名 + 插件列表 + 具体起步建议
  - 表格占页面主要面积
  - 右侧或底部补充组合建议卡片
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
