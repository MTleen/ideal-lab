# Slide 22 — 进阶用法与常见问题

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
Slide: 22 | Type: Content | Layout: bullet-list
Title: "进阶用法与常见问题"

Narrative Goal:
  覆盖进阶用法和常见问题，让受众知道如何深入使用 ideal-lab。

Key Content:

Left Section (45%) — 进阶用法:

Card 1 (工程蓝顶栏):
  标题: "YOLO 模式自动推进"

  说明: 信任 AI 判断，不想逐阶段手动确认

  启动方式:
    /ideal-document-workflow:ideal-document-workflow YOLO 模式，帮我写一份...

  行为:
  - 工作流自动推进
  - 直到完成或触发熔断
  - 发现 P0 级问题才停下来

Card 2 (工程蓝顶栏):
  标题: "多插件组合"

  典型组合: 先调研再输出

  第一步:
    /ideal-deep-research:deep-research 调研 2025 年主流 LLM 应用开发框架对比，standard 模式

  第二步:
    /ideal-ppt-suite:ideal-ppt-workflow 基于上面的调研结果，生成一份"LLM 应用开发框架选型"汇报 PPT

Right Section (55%) — 常见问题 (FAQ):

Q&A 列表 (紧凑排列):

Q1: 安装失败怎么办？
A: 运行 claude --version 检查版本。更新 Claude Code 后重试。确认网络可以访问 GitHub。

Q2: 如何更新已安装的插件？
A: 重新运行安装命令即可覆盖更新:
   claude plugin install ideal-document-workflow@ideal-lab

Q3: 可以只安装单个 Skill 吗？
A: 目前不支持。插件是安装的最小单位，但安装后你可以只使用其中某个 Skill。

Q4: 输出格式支持哪些？
A: 文档类默认 Markdown。PPT 套件输出 PPTX。调研工具输出 Markdown 调研报告。可按需指定其他格式。

Q5: 数据安全如何保障？
A: 所有任务在本地 Claude Code 环境中执行，代码和文档不会上传到 ideal-lab 仓库。API 调用走 Anthropic 官方通道。

Visual Description:
  - 左侧两张进阶用法卡片
  - 右侧 FAQ 列表，Q 用工程蓝色加粗，A 用深藏青
  - FAQ 用紧凑间距
  - 白色背景
```

---

Produce the HTML now. Raw HTML only.
