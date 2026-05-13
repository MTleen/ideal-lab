# Slide 06 — 一个 Plugin 里面有什么

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
Slide: 06 | Type: Content | Layout: tree-branching
Title: "一个 Plugin 里面有什么"

Narrative Goal:
  用树状结构展示 Plugin 的内部文件组成，让受众理解每个文件的角色。

Key Content:

Center — 树状结构图 (从上到下):

Root Node (工程蓝 #2563EB 背景, 白字):
  "ideal-document-workflow/" (示例 Plugin)
  标注: "plugin.json — 插件元数据（名称、版本、描述）"

Branch 1 (深藏青背景):
  "skills/" 目录
    ├─ Sub-branch 1a: "ideal-document-workflow/"
    │   ├─ "SKILL.md" — 编排器 Skill，定义流程调度逻辑
    │   └─ "references/" — 编排器参考文档
    │
    ├─ Sub-branch 1b: "requirement-analysis/"
    │   ├─ "SKILL.md" — P1 需求分析 Skill
    │   └─ "references/" — 需求分析模板
    │
    ├─ Sub-branch 1c: "outline-generation/"
    │   ├─ "SKILL.md" — P3 大纲生成 Skill
    │   └─ "references/" — 大纲结构模板
    │
    ├─ Sub-branch 1d: "document-writing/"
    │   ├─ "SKILL.md" — P7 并行写作 Skill
    │   └─ "references/" — 写作风格规范
    │
    └─ "...更多 Skill..."

Right Side — 注释卡片:

Card 1: "SKILL.md 的作用"
  - 定义 Skill 的触发条件
  - 定义执行步骤和输出格式
  - 定义调用的 references 和 scripts
  - 相当于 Skill 的"说明书"

Card 2: "references/ 的作用"
  - 写作规范、模板、技术规格
  - 纯文本 Markdown 格式
  - 版本可追溯，变更可对比

Card 3: "scripts/ 的作用"
  - 格式校验脚本
  - 文件转换脚本
  - 自动化工具脚本

Visual Description:
  - 左侧 65% 是树状结构图，用连线表示层级关系
  - 每个节点是圆角矩形，内有文件名和简短说明
  - 右侧 35% 是 3 张竖排卡片
  - 工程蓝连线，深藏青节点文字
  - 白色背景，浅灰蓝区分不同层级
```

---

Produce the HTML now. Raw HTML only.
