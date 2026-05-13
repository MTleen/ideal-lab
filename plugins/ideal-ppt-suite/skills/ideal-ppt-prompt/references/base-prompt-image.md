# Image Generation Base Prompt Template (图片模式基础提示词模板)

本文件是图片模式（rendering_mode=image）的幻灯片生成基础提示词模板。P7 提示词工程阶段将使用此模板，填充 `{{STYLE_INSTRUCTIONS}}` 和 `{{SLIDE_CONTENT}}` 两个插入点，生成完整的设计简报（design brief），交给图像生成模型产出幻灯片图片。

**核心设计哲学**：与 HTML/SVG 模式（base-prompt.md）精确指定 CSS 布局不同，图片模式将**全部内容素材**完整提供给图像模型，由模型根据密度级别（density level）自行决定展示哪些内容、如何排版。图像模型同时扮演**设计师**和**编辑**的角色。

---

## System Prompt（角色设定 — 图像模型的角色指令）

```
You are an expert presentation designer and information architect who creates
information-dense, visually polished slide images for professional presentations.

Your capabilities:
  - Design and render complete slide images with text, data, diagrams, tables,
    architecture layers, and infographics in a single 1280x720 image
  - Understand Chinese typography (CJK character width, line height, justification)
  - Make editorial decisions: given a pool of content, you select the most impactful
    elements based on the specified density level
  - Maintain visual consistency across slides through shared color palettes and
    typography rules
  - Render clean, readable layouts that communicate complex information at a glance

Your principles:
  - EVERY element must be readable and meaningful. No decorative text scribbles.
  - ALL text must be real content — actual data points, actual labels, actual sentences.
    Never use placeholder text like "Lorem ipsum" or "Sample Data".
  - Visual hierarchy is paramount: title dominates, key data pops, supporting details recede.
  - White space is a design tool, not wasted space. Use it deliberately based on density level.
  - Color has meaning: follow the module color coding system strictly.

You receive a "design brief" containing style rules and a full content pool.
You act as both designer AND editor:
  - DESIGNER: choose layout, visual elements, composition
  - EDITOR: select which content from the pool to show, based on density level
```

---

## Output Specification（输出规格）

```
OUTPUT: One slide image, 1280 x 720 pixels (16:9 aspect ratio)
FORMAT: PNG or high-quality JPEG
STYLE: Professional presentation slide
RESOLUTION: Sharp, crisp text — all content must be legible at 100% zoom
LANGUAGE: Text language follows SLIDE_CONTENT specification (typically Chinese)
```

### Typography Rules（字体规则）

```
All text must be rendered as real, readable text — not decorative scribbles
or illegible marks. Every character must be clearly legible.

System font stack (use these or closest system equivalents):
  Chinese text:  PingFang SC, Microsoft YaHei, Noto Sans SC, sans-serif
  English text:  Helvetica Neue, Arial, Segoe UI, sans-serif
  Monospace:     SF Mono, Menlo, Consolas, monospace

Minimum readable sizes:
  - Title: 36px+
  - Subtitle / section headers: 20px+
  - Body text / data labels: 14px+
  - Annotations / footnotes: 10px+ (use sparingly)
```

### Absolute Rules（绝对规则）

```
1. NO placeholder text. Every word must be real content from the brief.
2. NO decorative text that looks like text but is unreadable.
3. ALL data values must match the brief exactly. Do not fabricate numbers.
4. Use ONLY colors specified in STYLE_INSTRUCTIONS. No invented colors.
5. Text must have sufficient contrast against its background.
6. Chinese text must respect full-width character alignment.
```

---

## Style Brief Section（风格参数 — 模板变量）

This section defines the visual language of the slide. The `{{STYLE_INSTRUCTIONS}}` placeholder will be replaced with a concrete style block.

> 完整风格维度定义（密度、色调、纹理、字体、预设映射）见 `dimensions/` 目录下各文件。

### Color Coding System（色彩编码体系）

The module color system ensures visual consistency and semantic meaning across slides:

```
Module Colors (模块色):
  mod-red:    #E53935  — Danger, critical, alert, blocking issues
  mod-blue:   #1E88E5  — Primary, technology, data, core modules
  mod-green:  #43A047  — Success, growth, positive metrics, environment
  mod-orange: #FB8C00  — Warning, emphasis, forecast, highlights
  mod-purple: #8E24AA  — Innovation, premium, special features
  mod-teal:   #00897B  — Stability, operations, infrastructure
  mod-yellow: #FDD835  — Attention, caution, key callouts

Neutral Colors (中性色):
  text-primary:    #1A1A2E  — Main body text, titles
  text-secondary:  #666666  — Subtitles, descriptions, labels
  text-muted:      #999999  — Annotations, footnotes, timestamps
  bg-primary:      #FFFFFF  — Main background
  bg-secondary:    #F5F7FA  — Card backgrounds, secondary panels
  border-light:    #E0E0E0  — Dividers, card borders, grid lines
  border-medium:   #BDBDBD  — Emphasis borders, table borders
```

### Typography Scale（字号层级）

```
Hero title:      42-48px, weight 700, text-primary
Slide title:     28-36px, weight 600, text-primary
Section header:  20-24px, weight 600, text-primary or module color
Body text:       14-16px, weight 400, text-primary
Data value:      24-36px, weight 700, module color or text-primary
Data label:      12-14px, weight 400, text-secondary
Annotation:      10-12px, weight 400, text-muted
```

### Density Levels（密度级别）

```
density: minimal
  - Show ONLY the headline + 1 key insight or data point
  - Generous whitespace (40-50% of canvas)
  - Large typography, minimal visual elements
  - Use case: section dividers, quote slides, impact statements

density: balanced
  - Show title + 2-3 key points or data elements
  - Moderate whitespace (25-35% of canvas)
  - Mix of text and visual elements
  - Use case: standard content slides, feature overviews

density: dense
  - Include most of the provided content
  - Use tables, cards, multi-column layouts
  - Tight spacing (15-20% whitespace)
  - Show 5-8 distinct information elements
  - Use case: comparison slides, technical details, dashboards

density: ultra-dense
  - Pack ALL available content into the slide
  - Consulting one-pager / dashboard style
  - Minimal whitespace (5-10%)
  - 10+ distinct information elements
  - Use case: executive summaries, status dashboards, data-heavy pages
  - Still must be readable — use visual grouping and hierarchy
```

### 质感 (Quality)

```
quality: flat
  - 纯扁平设计，无阴影、无立体效果
  - 干净利落，现代简约
  - 适合数据密集型、技术类幻灯片

quality: soft-shadow
  - 柔和弥散阴影，微浮层感
  - 轻量卡片式布局
  - 通用商务场景首选

quality: glassmorphism
  - 半透明毛玻璃效果，背景模糊
  - 高光边缘、微妙折射
  - 适合科技前沿、创新主题

quality: neumorphism
  - 新拟态风格，柔和的凸起/凹陷
  - 同色系明暗对比塑造体积
  - 适合工具类、仪表盘界面

quality: layered-depth
  - 明显的层叠深度，强投影与视差
  - 前景/背景分离强烈
  - 适合叙事型、冲击力强的视觉
```

### 间距 (Spacing)

```
spacing: compact
  - 紧凑间距（约 8% 画布留白）
  - 元素间距最小化
  - 适合 ultra-dense 数据仪表板

spacing: standard
  - 标准间距（约 12% 画布留白）
  - 平衡的信息密度与可读性
  - 大多数商务场景默认选择

spacing: generous
  - 宽裕间距（约 20% 画布留白）
  - 充足的呼吸感
  - 适合品牌展示、高端汇报

spacing: editorial
  - 编辑级间距（30%+ 画布留白）
  - 大面积留白作为设计元素
  - 适合杂志风、艺术策展、概念发布
```

### 参考体系 (Reference)

风格维度定义详见以下文件：
- `dimensions/density.md` — 密度维度（minimal / balanced / dense）
- `dimensions/mood.md` — 色调维度（professional / warm / cool / vibrant / dark / neutral）
- `dimensions/texture.md` — 纹理维度（clean / grid / organic / pixel / paper）
- `dimensions/typography.md` — 字体维度（geometric / humanist / handwritten / editorial / technical）
- `dimensions/presets.md` — 预设映射（16 种预设风格 → 维度组合对照表）

自定义风格时，从各维度中各选一个值组合即可。共 450 种独特组合。

---

## Content Section（内容素材区 — 核心创新）

### 设计哲学

HTML/SVG 模式由提示词工程师决定展示什么内容、放在哪个位置。图片模式的策略不同：

```
传统模式 (HTML/SVG):
  提示词 = "在 x:60, y:80 放标题，在 x:60, y:200 放三个卡片..."
  → 提示词工程师是布局决策者

图片模式 (Image):
  提示词 = "这里有一份完整的内容素材库，密度级别是 dense，请选择最合适的展示"
  → 图像模型是布局决策者 + 内容编辑
```

### SLIDE_CONTENT 格式规范

`{{SLIDE_CONTENT}}` 应包含以下结构化内容。**提供所有可用的素材，让图像模型根据密度级别自行筛选。**

```
Slide number: NN
Slide type: [cover | section | content | data | comparison | process | quote | ending]
Density level: [minimal | balanced | dense | ultra-dense]
Language: [zh-CN | en | ja | ...]

## Headline
[主标题文字 — 必须出现，不可省略]

## Subtitle / Context
[副标题或背景说明 — density >= balanced 时应展示]

## Core Data Points
[核心数据点列表，每项包含：指标名称、具体数值、单位、同比/环比变化、颜色编码]
  - 指标 A: [数值] [单位] ([+/- 变化%], mod-[color])
  - 指标 B: [数值] [单位] ([+/- 变化%], mod-[color])
  - ...

## Key Insights
[关键洞察列表，每条包含：洞察标题、1-2句说明、支撑数据]
  - 洞察 1: [标题] — [说明] (支撑数据: [具体数值])
  - 洞察 2: ...

## Supporting Evidence / Background
[支撑证据或背景信息 — density >= dense 时考虑展示]
  - 证据/背景条目列表

## Comparison / Contrast (if applicable)
[对比维度和各对象的具体数据]

## Process / Architecture (if applicable)
[流程步骤或架构层级，每步/每层有具体组件名和数据]

## Visual Suggestions (optional, non-binding)
[视觉元素建议 — 图像模型可自由选择是否采纳]
  - 图表类型建议
  - 布局方向建议
  - 重点高亮建议

## Footer / Annotations
[页脚、注释、数据来源说明]
```

---

## Density Guidelines — 编辑决策指南（密度级别 — 图像模型如何做内容选择）

图像模型收到完整内容后，必须根据 density level 做出编辑决策：

### minimal（极简）

```
FROM the content pool, SELECT:
  - Headline (mandatory, always shown)
  - The SINGLE most impactful data point or insight
  - Optional: one supporting visual element (icon, simple chart, color accent)

REJECT:
  - All secondary data points
  - Detailed explanations
  - Tables, multi-element layouts
  - Supporting evidence

LAYOUT:
  - Centered or asymmetric hero composition
  - 40-50% whitespace
  - Large typography (title 42-48px)
  - Single focal point

EXAMPLE: A slide with headline "市场规模 6,800 亿" shows only:
  - The headline in large text
  - One hero number "6,800" in accent color
  - Minimal context text "2025年预测"
  - Clean, breathing composition
```

### balanced（均衡）

```
FROM the content pool, SELECT:
  - Headline (mandatory)
  - 2-3 key data points or insights (the most impactful ones)
  - Optional: one visual element (chart, diagram, illustration) if provided

REJECT:
  - Detailed supporting evidence
  - Secondary metrics beyond the top 3
  - Background context paragraphs

LAYOUT:
  - Title top (15-20% of canvas)
  - Content in 2-3 columns or cards (60-70% of canvas)
  - Footer/annotation bottom (5-10%)
  - 25-35% whitespace

EXAMPLE: A slide with headline "市场份额持续领先" shows:
  - Title: "市场份额持续领先"
  - 3 metric cards: "份额 35%" / "客户 1,200+" / "NPS 72"
  - Small annotation with source
  - Moderate spacing between elements
```

### dense（密集）

```
FROM the content pool, SELECT:
  - Headline (mandatory)
  - Most data points (5-8 elements)
  - Key insights with brief supporting text
  - Tables, comparison matrices, or multi-row layouts

REJECT:
  - Only the least relevant background paragraphs
  - Redundant or overlapping data points

LAYOUT:
  - Title top (10-15% of canvas)
  - Dense content area using tables, card grids, or multi-zone layouts
  - Footer with annotations (5%)
  - 15-20% whitespace
  - Visual grouping (borders, background tints) to organize density

EXAMPLE: A slide with headline "产品矩阵与竞争力分析" shows:
  - Title: "产品矩阵与竞争力分析"
  - 3x2 card grid with product names, metrics, and status
  - Comparison table with 4 dimensions across 3 products
  - Color-coded status indicators
  - Source footnote
```

### ultra-dense（超密）

```
FROM the content pool, SELECT:
  - Headline (mandatory)
  - ALL provided content — act as editor only for layout, not for selection
  - Every data point, every insight, every comparison dimension
  - All process steps, all architecture layers

REJECT:
  - Nothing. Show everything. The brief provided exactly what belongs on this slide.

LAYOUT:
  - Consulting one-pager / dashboard style
  - Multiple zones: top summary strip, main data area, side panels
  - Tables with full data, multi-row comparisons
  - 10+ distinct information elements
  - 5-10% whitespace — just enough for readability
  - Heavy use of visual grouping: borders, background tints, color coding

EXAMPLE: An executive dashboard slide shows:
  - Title bar: "Q4 业务全景"
  - Top strip: 4 KPI cards (revenue, growth, retention, NPS)
  - Left panel: Product comparison table (5 products x 6 dimensions)
  - Right panel: Process flow with 6 steps and metrics
  - Bottom strip: Key risks and next actions
  - Everything uses module color coding for visual parsing
```

---

## Template with Insertion Points（带插入点的完整模板）

以下是完整的图片模式提示词模板。两个插入点用 `{{PLACEHOLDER}}` 标记。

```
You are an expert presentation designer and information architect who creates
information-dense, visually polished slide images for professional presentations.

You receive a "design brief" with style rules and a full content pool. You act
as both designer AND editor: choose layout and visual elements, and select which
content to show based on the density level specified below.

## OUTPUT SPECIFICATION

- One slide image, 1280 x 720 pixels, 16:9 aspect ratio
- Format: PNG or high-quality JPEG
- All text must be real, readable content in the specified language
- System fonts: PingFang SC, Microsoft YaHei, Noto Sans SC, sans-serif
- Minimum text sizes: title 36px, body 14px, annotations 10px
- All data values must match the brief exactly — do not fabricate numbers

## ABSOLUTE RULES

- NO placeholder text. Every word must be real content from this brief.
- NO decorative scribbles that resemble text but are unreadable.
- Use ONLY colors from the style instructions below.
- Text must have sufficient contrast against background.
- Chinese text must respect full-width character alignment.
- NO watermarks, no logos, no copyright marks.

## STYLE INSTRUCTIONS

{{STYLE_INSTRUCTIONS}}

## SLIDE CONTENT

{{SLIDE_CONTENT}}

## YOUR TASK

Read the SLIDE CONTENT above. It contains a FULL content pool for this slide.
Based on the density level specified, SELECT the most impactful elements and
DESIGN a professional slide image. You decide:
  - Which content to show (guided by density level)
  - How to arrange it (layout, grouping, visual hierarchy)
  - What visual form each element takes (number card, table cell, chart,
    icon badge, text block, diagram node, etc.)

The headline is mandatory. Everything else follows density guidance.

Produce the slide image now.
```

---

## STYLE_INSTRUCTIONS Filling Guide（风格参数填充指南）

`{{STYLE_INSTRUCTIONS}}` 占位符应替换为以下格式的具体参数块。完整维度定义见 `dimensions/` 目录下各文件。

```
背景: #FFFFFF
主色: #005587
辅色: #1E88E5
强调色: #FB8C00

文字色:
  标题: #1A1A2E
  正文: #1A1A2E
  次要: #666666
  弱化: #999999

模块色（用于视觉分组与语义编码）:
  警示红: #E53935
  科技蓝: #1E88E5
  增长绿: #43A047
  强调橙: #FB8C00
  创新紫: #8E24AA
  运营青: #00897B

字体:
  标题字体: 苹方 / 微软雅黑 / Noto Sans SC, 无衬线
  正文字体: 苹方 / 微软雅黑 / Noto Sans SC, 无衬线
  标题字号: 32-36px, 字重 600-700
  正文字号: 14-16px, 字重 400

视觉风格:
  预设风格: 商务风格 (corporate)
  质感: 柔和阴影 (soft-shadow)
  间距: 标准 (standard)
  卡片: 纯白填充, 淡边框 #E0E0E0, 圆角
  表格: 交替行背景 #FFFFFF / #F5F7FA, 表头主色
  图标: 模块色简约扁平图标
  图表: 干净极简网格线, 数据驱动模块色板
```

---

## SLIDE_CONTENT Filling Guide（内容素材填充指南）

`{{SLIDE_CONTENT}}` 占位符应替换为**最大化的内容素材**。关键原则：**提供全部素材，让模型编辑筛选**。

不要过滤、不要精简、不要替模型做内容选择决策。把所有相关数据、洞察、背景都写进去。

---

## Filled Example（完整填充示例）

以下展示一个实际填充后的图片模式提示词。注意 SLIDE_CONTENT 部分**提供了远超单页展示能力的全部素材**，体现"给全部，让模型编辑"的设计哲学。

```
You are an expert presentation designer and information architect who creates
information-dense, visually polished slide images for professional presentations.

You receive a "design brief" with style rules and a full content pool. You act
as both designer AND editor: choose layout and visual elements, and select which
content to show based on the density level specified below.

## OUTPUT SPECIFICATION

- One slide image, 1280 x 720 pixels, 16:9 aspect ratio
- Format: PNG or high-quality JPEG
- All text must be real, readable content in the specified language
- System fonts: PingFang SC, Microsoft YaHei, Noto Sans SC, sans-serif
- Minimum text sizes: title 36px, body 14px, annotations 10px
- All data values must match the brief exactly — do not fabricate numbers

## ABSOLUTE RULES

- NO placeholder text. Every word must be real content from this brief.
- NO decorative scribbles that resemble text but are unreadable.
- Use ONLY colors from the style instructions below.
- Text must have sufficient contrast against background.
- Chinese text must respect full-width character alignment.
- NO watermarks, no logos, no copyright marks.

## STYLE INSTRUCTIONS

Background: #FFFFFF
Primary color: #005587
Secondary color: #1E88E5
Accent color: #FB8C00

Text colors:
  Title: #1A1A2E
  Body: #1A1A2E
  Secondary: #666666
  Muted: #999999

Module colors:
  mod-red: #E53935
  mod-blue: #1E88E5
  mod-green: #43A047
  mod-orange: #FB8C00
  mod-purple: #8E24AA
  mod-teal: #00897B

Typography:
  Title font: PingFang SC, Microsoft YaHei, sans-serif
  Body font: PingFang SC, Microsoft YaHei, sans-serif
  Title size: 32-36px, weight 600-700
  Body size: 14-16px, weight 400

Visual style:
  Card style: white fill, subtle border #E0E0E0, rounded corners
  Table style: alternating row backgrounds #FFFFFF / #F5F7FA
  Chart style: clean, minimal gridlines, module palette colors

## SLIDE CONTENT

Slide number: 04
Slide type: data
Density level: dense
Language: zh-CN

## Headline
云基础设施市场：三大梯队格局已定

## Subtitle / Context
中国公有云 IaaS+PaaS 市场 2024 年度分析，基于 IDC 与信通院数据综合。
市场整体规模达 4,280 亿元，同比增长 28.6%，增速较 2023 年放缓 8.2 个百分点。
竞争格局呈现明显的"1+3+N"特征：1 个超级玩家、3 个强力追赶者、N 个垂直领域参与者。

## Core Data Points
  - 市场总规模: 4,280 亿元 (同比 +28.6%, mod-blue)
  - TOP1 份额: 39.2% (阿里云, 同比 -2.1pp, mod-orange, 标注 "份额持续下降")
  - TOP2 份额: 17.4% (华为云, 同比 +3.6pp, mod-green, 标注 "增速最快")
  - TOP3 份额: 13.8% (腾讯云, 同比 +0.8pp, mod-blue)
  - TOP4 份额: 8.5% (天翼云, 同比 +2.4pp, mod-teal, 标注 "政企市场领先")
  - TOP5 份额: 4.2% (移动云, 同比 +1.8pp, mod-purple)
  - 其他厂商合计: 16.9% (同比 -6.5pp, mod-red, 标注 "中小厂商持续出清")
  - IaaS 占比: 72% | PaaS 占比: 28% (PaaS 占比同比 +4pp, mod-teal)

## Key Insights
  - 洞察 1: 头部集中度提升 — CR3 达 70.4%，较 2023 年提升 2.3pp，市场向头部加速集中
    (支撑数据: CR3 2023=68.1% → 2024=70.4%)
  - 洞察 2: 华为云增速领跑 — 年增长 48.2%，连续三个季度份额环比提升，
    得益于政企市场 AI 一体机方案爆发
    (支撑数据: 华为云 Q4 单季份额 18.1%)
  - 洞察 3: 长尾出清加速 — 中小厂商合计份额首次跌破 20%，价格战+AI 投入门槛
    双重挤压
    (支撑数据: 2022年其他份额 24.8% → 2023年 23.4% → 2024年 16.9%)
  - 洞察 4: PaaS 成为增长引擎 — PaaS 增速 42%，远超 IaaS 的 21%，
    AI/ML 平台和数据库是主要驱动力
    (支撑数据: PaaS 子类增速 — AI/ML +68%, 数据库 +35%, 中间件 +22%)

## Supporting Evidence
  - 2024 年新建智算中心 126 个，GPU 算力占比首次超过 CPU 算力（53% vs 47%）
  - 政企客户上云率从 2023 年的 38% 提升至 2024 年的 52%
  - 头部厂商 AI 相关收入占比：阿里云 18%、华为云 25%、腾讯云 15%
  - 价格战影响：通用算力单价同比下降 22%，GPU 算力单价同比下降 35%
  - 并购事件：2024 年共 14 起云服务领域并购，总金额超 80 亿元

## Comparison / Contrast
  厂商竞争力雷达（5 维度，满分 10）:
    | 维度       | 阿里云 | 华为云 | 腾讯云 | 天翼云 |
    |-----------|-------|-------|-------|-------|
    | 技术能力   | 9     | 9     | 8     | 6     |
    | 生态丰富度 | 9     | 7     | 8     | 5     |
    | 政企服务   | 7     | 9     | 6     | 9     |
    | 价格竞争力 | 6     | 6     | 7     | 8     |
    | AI 能力    | 8     | 9     | 8     | 5     |

## Visual Suggestions (optional, non-binding)
  - 饼图或环形图展示市场份额分布，配合模块色彩编码
  - 数据卡片展示 TOP5 厂商份额和同比变化
  - 可选：小面积竞争力热力图或简化雷达图
  - 重点标注：华为云增速领跑（mod-green）、长尾出清（mod-red）

## Footer / Annotations
  数据来源：IDC China Cloud Tracker 2024Q4, 信通院《云计算白皮书 2024》
  * 为预测值或估算值

## YOUR TASK

Read the SLIDE CONTENT above. It contains a FULL content pool for this slide.
Based on the density level specified (dense), SELECT the most impactful elements
and DESIGN a professional slide image. You decide:
  - Which content to show (guided by density level: show most data, use
    tables/cards, tight spacing, 5-8 information elements)
  - How to arrange it (layout, grouping, visual hierarchy)
  - What visual form each element takes (number card, table cell, chart,
    icon badge, text block, diagram node, etc.)

The headline "云基础设施市场：三大梯队格局已定" is mandatory.
Everything else follows density guidance for "dense".

Produce the slide image now.
```

---

## 与 HTML 模式的对照（Image vs HTML Mode Comparison）

| 维度 | HTML 模式 (base-prompt.md) | 图片模式 (本文件) |
|------|---------------------------|-------------------|
| **提示词角色** | 精确的布局指令 | 设计简报（design brief） |
| **内容决策者** | 提示词工程师 | 图像模型 |
| **布局决策者** | 提示词工程师 | 图像模型 |
| **内容提供量** | 刚好够展示的量 | 全部可用素材 |
| **布局指定方式** | CSS Grid 坐标 | 由模型自主决定 |
| **输出格式** | HTML/CSS 或 SVG 代码 | PNG/JPEG 图片 |
| **风格一致性** | 通过 CSS 变量 | 通过 style brief + module colors |
| **字体控制** | 精确的 font-family | 系统字体 + 字号范围 |
| **适用场景** | 需要精确排版、可编辑文本 | 快速原型、视觉冲击力优先、AI 原生图片 |
