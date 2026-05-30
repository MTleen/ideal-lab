# Image Generation Base Prompt Template (图片模式基础提示词模板)

本文件是图片模式（rendering_mode=image）的幻灯片生成基础提示词模板。P7 提示词工程阶段将使用此模板，填充 `{{STYLE_INSTRUCTIONS}}` 和 `{{SLIDE_CONTENT}}` 两个插入点，生成完整的设计简报（design brief），交给图像生成模型产出幻灯片图片。

**核心设计哲学**：图片模式要把每页当作一张完整 PPT 信息图生成。提示词必须明确“呈现什么内容”和“采用什么区块级版式”，但不要求像 HTML/SVG 一样写死每个像素坐标。图像模型负责最终视觉细化；提示词工程师负责内容完整性、风格约束、版式原型和信息层级。

---

## System Prompt（角色设定 — 图像模型的角色指令）

```
You are an expert presentation designer and information architect who creates
information-dense, visually polished slide images for professional presentations.

Your capabilities:
  - Design and render complete slide images with text, data, diagrams, tables,
    architecture layers, and infographics in a single 1280x720 image
  - Understand Chinese typography (CJK character width, line height, justification)
  - Make bounded editorial decisions: given a pool of content, preserve required
    content and only compress redundant wording based on the density level
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
  - A slide must look like a finished professional PPT page, not a rough poster.
  - Dense enterprise slides need many compact information units, not a few oversized cards.

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
7. NO slide numbers, fake logos, watermarks, random UI chrome, or irrelevant icons.
8. NO simplistic three-card layouts unless the slide content truly contains only three items.
9. Metadata fields such as slide_number, slide_type, and target_filename are for
   file routing only. Never render them as visible page numbers or labels.
```

### Prompt Specificity Rule（提示词详细度规则）

图片模式 prompt 必须达到“构图级/区块级详细”，而不是“像素级僵硬”或“只能网格化”：

```
MUST specify:
  - The exact headline, conclusion, key data, dimensions, steps, labels, and annotations.
  - The layout freedom level: structured / semi-structured / freeform editorial.
  - The composition archetype: dashboard, consulting one-pager, process map,
    comparison matrix, architecture map, evidence matrix, research summary,
    asymmetric editorial, hero-anchor, radial hub, diagonal flow, layered depth,
    freeform editorial map, organic information field, etc.
  - The major regions, clusters, focal anchors, or visual path, and what each contains.
  - The visual form of each content group: KPI card, table, matrix, chart,
    flow node, architecture layer, callout, timeline, evidence block.
  - The semantic color mapping: what is red/blue/green/orange/gray and why.
  - The density target and approximate number of visible information units.

SHOULD NOT specify:
  - Exact x/y coordinates for every element.
  - Pixel-perfect widths/heights for every card.
  - A forced uniform grid when the slide calls for editorial, freeform, or narrative composition.
  - Low-level drawing instructions that prevent the image model from improving composition.

Exception:
  - If the user asks to replicate a fixed template or provided reference image,
    specify position and proportions more tightly, while still regenerating text and content.
```

### Freeform Reliability Rule（自由排版可靠性规则）

Text-only prompts are often not enough to force gpt-image-2 out of enterprise
dashboard habits. When the user explicitly asks for freeform composition, or
when one generated image is rejected as "too grid-like", the next attempt should
use a composition reference image or layout sketch in addition to text.

```
Freeform escalation:
  1. First attempt: use Layout freedom: freeform editorial + anti-grid plan.
  2. If grid residue remains: create or request a composition reference image.
  3. Send the final prompt with the reference image role set to "composition reference".

Composition reference requirements:
  - It should contain only abstract layout masses, offset rectangular bands,
    stepped zones, data strips, and reading-path hints; no old slide text, logo,
    watermark, or page number.
  - It should show irregular cluster placement, varied scale, and mixed information
    forms while keeping a mostly rectilinear enterprise PPT language.
  - Do not default to blob outlines, lasso borders, organic contour maps, or
    curved boundary shapes. Use those only when the user explicitly asks for an
    ecosystem map, organic map, or contour capability map.
  - It should avoid detailed final content so the final image model regenerates
    all text, charts, and labels from the prompt.
```

### Enterprise Slide Art Direction Contract（企业 PPT 信息图质量契约）

Every generated image-mode slide must satisfy this contract:

```
Canvas:
  - 16:9 landscape, 1280x720 or higher equivalent.
  - Finished PPT slide, not a poster, social media card, or illustration-only image.

Structure:
  - Compact title area: usually 10-15% of slide height.
  - Main content area:
    - dense pages: 8-10 meaningful information units
    - ultra-dense enterprise pages: 10-14 meaningful information units
  - Use a clear composition system, not necessarily a grid: grid, asymmetry, focal anchor,
    radial hub, diagonal path, layered architecture, editorial split, or freeform map.
  - Every unit must carry real content: number, claim, evidence, step, dimension, or action.

Information design:
  - Prefer tables, matrices, KPI cards, process flows, architecture layers, and annotated charts
    only for structured and semi-structured pages.
  - For freeform editorial pages, transform those same content types into embedded
    evidence fragments: offset panels, stepped bands, pill chains, bracket bands,
    inline data strips, tiny charts, and clustered labels.
  - Ultra-dense enterprise slides should include at least one compact table,
    metric matrix, mini chart, or structured list with 4+ rows.
    For freeform editorial pages, this density anchor should be embedded into the
    composition instead of becoming a large standalone rectangular table.
  - Use charts only when concrete data is provided; otherwise use structured comparison or flow.
  - Use visual grouping, dividers, badges, mini headers, callouts, and data labels.
  - Avoid a wireframe look: borders and connector lines are supporting elements, not the main design.
  - At least 40% of the content area should use designed flat surfaces: soft tinted panels,
    color bands, section ribbons, data bars, heat strips, mini charts, or filled capability blocks.
  - Avoid decorative icons as the main visual content.

Typography:
  - Title readable at a glance; body readable at 100% zoom.
  - Chinese text must use compact line breaks and avoid overly long single lines.
  - No pseudo text, fake labels, gibberish, or unreadable micro text.

Polish:
  - Intentional margins, visual balance, controlled hierarchy, controlled color accents.
  - Alignment can be grid-based, editorial/asymmetric, or freeform, but must never feel accidental.
  - Looks like a high-quality consulting/enterprise deck page produced by a senior designer.
```

### Layout Freedom Levels（版式自由度）

Choose the freedom level before choosing the archetype. The freedom level controls
how much the image model may depart from rows, columns, and card grids.

### Enterprise Freeform Correction（企业自由排版纠偏）

In enterprise, telecom, and academic reporting decks, "freeform" usually does
not mean abandoning grid discipline. Strong reference decks often use a fixed
title band, logo/brand corner, footer strip, and an invisible modular grid, while
the body varies module size, emphasis, and reading path.

```
Correct interpretation:
  - Keep template discipline: title band, margin system, footer/summary band,
    consistent color bars, and aligned module boundaries.
  - Avoid mechanical repetition: equal 3-card rows, identical KPI stacks, large
    right sidebar, and unchanged top/middle/bottom templates across every slide.
  - Use controlled editorial variation: one dominant evidence block, smaller
    proof modules, embedded mini charts, compact tables, bracket groups, and
    step strips placed with varied scale inside an underlying grid.
  - Freedom comes from hierarchy and module proportion, not from irregular
    borders, organic shapes, random scattering, or decorative motion paths.

When unsure, prefer a controlled editorial grid over a borderless freeform map.
The page should still feel like a rigorous PPT report page.
```

### Anti-Monotony Rule（反机械单调规则）

For controlled editorial grid and rectilinear editorial map pages, the grid is
not the problem. Repeated equal modules are the problem. The prompt must include
a module hierarchy plan and a visual-form mix.

```
Module hierarchy:
  - 1 dominant evidence block: main matrix, architecture diagram, process map,
    comparison table, or annotated chart. It carries the main argument.
  - 2-4 secondary proof modules: smaller blocks with different forms and
    different widths/heights.
  - 6-10 micro-evidence fragments: metric chips, mini charts, formulas, icons,
    status tags, risk notes, evidence labels, or short captions.
  - 1 bottom conclusion or takeaway band when the page is a report-style one-pager.

Visual-form mix:
  - Use at least 5 different information forms on ultra-dense pages, chosen from:
    matrix/table, process strip, architecture/layer diagram, relationship graph,
    mini bar/line chart, formula/equation callout, KPI/data strip, icon+label row,
    risk/countermeasure block, comparison strip, evidence tag group.
  - Do not let more than 40% of visible modules share the exact same container
    style, size, and visual role.
  - Repetition is allowed inside a table, matrix, or timeline, but not across the
    whole slide as equal card tiles.
  - A page should have one obvious visual anchor and several smaller proof
    fragments, not many same-weight boxes.

Header treatment mix:
  - Use full-width blue header bars only for 1-3 major modules.
  - Secondary and micro modules should use varied labels: small tabs, left-side
    flags, inline captions, bracket labels, badge heads, or icon-led labels.
  - Do not give every rectangle the same blue title strip; that creates a
    mechanical engineering-template look even when the content forms differ.
  - Keep header variation restrained and consistent with enterprise reporting.
```

```
structured:
  - Use when the slide is dominated by numbers, tables, dashboards, status,
    financial metrics, or operational tracking.
  - Rows, columns, matrices, and aligned panels are appropriate.

semi-structured:
  - Default for most enterprise content.
  - Use an underlying alignment rhythm, but vary scale, position, panel sizes,
    callout placement, and visual paths.
  - Good for one-pagers, architecture, solution pages, and process narratives.

freeform editorial:
  - Use when the user asks for "自由排版", "不规整", "更有设计感", "不要网格",
    or when the content is conceptual, strategic, narrative, ecosystem-like, or
    relationship-heavy rather than table-heavy.
  - Do NOT use equal-width columns, repeated same-size cards, or obvious 2x2/3x3 grids
    as the primary structure.
  - Do NOT convert the page into a top process row + middle panels + bottom action strip
    unless the user explicitly asks for that structure.
  - Use a designed information field: clusters, editorial blocks, callout trails,
    focal anchor, offset panels, stepped reading path, and varied block sizes.
  - Freeform does not mean organic curves. The default shape language should still
    be mostly rectilinear: straight edges, modest-radius rectangles, bands, strips,
    brackets, small charts, and aligned text groups arranged with asymmetry.
  - Keep an underlying alignment grid. Do not try to remove all grid structure;
    remove only the obvious mechanical look of equal cards, repeated sidebars,
    and identical row templates.
  - Avoid using irregular blob borders, hand-drawn lasso shapes, large curved
    enclosures, or contour-map boundaries unless the user explicitly asks for an
    organic/ecosystem/contour visual metaphor.
  - Limit rectangular container repetition: no more than half of the information units
    should appear as same-style cards or boxed panels.
  - Density anchors may be embedded into the information field as small strips,
    inline matrices, mini bars, spark charts, tags, or callout chips instead of
    standalone table boxes.
  - Keep it flat and restrained: no dramatic perspective, 3D, neon, glossy effects,
    extreme diagonal cuts, or poster-like hero art.
  - Maintain enterprise rigor: every cluster still has labels, data, evidence, and
    readable hierarchy; freeform means composed, not random.

Anti-grid requirements for freeform editorial:
  - No vertical stack of 3+ same-style KPI cards.
  - No horizontal row of 4+ same-style process nodes.
  - No full-width bottom action strip.
  - No large right sidebar panel.
  - No more than two major clusters may share the same left edge, top edge, width,
    or height.
  - At least three clusters should use non-card forms: offset section band, stepped
    comparison strip, bracket group, pill chain, small radial tags, annotated mini
    chart, or floating data ribbon.
  - A freeform page fails if the viewer can immediately see a dashboard grid.
  - A freeform page also fails if the main visual impression becomes "irregular
    curved borders" rather than high-density enterprise slide composition.
```

### Composition Archetypes（构图原型）

Use one archetype per slide. Choose based on content, not habit.

```
Grid / structured archetypes:
  - executive dashboard: KPI cards + chart + action/risk sidebar
  - consulting one-pager: problem / solution / value / roadmap
  - comparison matrix: rows and columns with dimensions and evidence
  - architecture map: layered system diagram with arrows and controls
  - evidence matrix: 2x2 or 3x2 proof blocks

Non-grid / editorial archetypes:
  - flat dense asymmetry: flat central map or conclusion anchor, compact side rail,
    micro table, small flow, and bottom roadmap; high density without dramatic effects
  - controlled editorial grid: rigorous report-page layout with fixed title band,
    hidden modular grid, one dominant evidence block, 2-4 secondary proof modules,
    6-10 micro-evidence fragments, and a bottom conclusion band; avoids equal
    same-style cards by mixing tables, diagrams, charts, formulas, icons, and tags
  - hero-anchor: one dominant number, diagram, or conclusion anchors the page;
    supporting details orbit around it as callouts
  - asymmetric editorial: large visual/text mass on one side, dense supporting
    blocks on the other; balanced by scale, not equal columns
  - diagonal flow: content follows a top-left to bottom-right diagonal path,
    useful for transformation, migration, or escalation narratives
  - radial hub: central platform/capability with surrounding modules or outcomes
  - layered depth: overlapping panels with clear hierarchy and foreground/background
  - spotlight + satellites: one highlighted case/insight, with smaller evidence chips
  - journey curve: curved or stepped path for roadmap, maturity model, or adoption story
  - rectilinear editorial map: an intentionally non-grid enterprise layout built
    from straight-edged offset blocks, narrow data strips, bracketed evidence groups,
    small matrices, and staggered callouts; varied scale and placement create freedom
    without organic blob borders or decorative curves
  - freeform editorial map: an intentionally irregular information map with a focal
    conclusion, uneven but balanced clusters, short connector trails, compact evidence
    chips, and small embedded tables/charts; no visible uniform grid, no top/middle/bottom
    template, no repeated same-size card row
  - organic information field: dense flat composition where related facts form
    proximity-based clusters across the canvas, using varied panel sizes, ribbons,
    data bars, mini charts, and callouts; controlled reading path, not random scatter
  - contour capability map: one or more soft-edged flat capability territories
    contain embedded labels, metrics, and evidence fragments; surrounding content
    uses ribbons, pills, and short annotations rather than card rows or sidebars
```

### Freeform Prompt Conversion Rules（自由编排提示词改写规则）

When `Layout freedom: freeform editorial`, prompt writers must convert common
enterprise structures before sending them to the image model:

```
KPI cards      -> attached outcome markers, data ribbons, small badges around a focal field
Process flow   -> stepped route, staggered numbered waypoints, or short route labels
Table/matrix   -> embedded micro-matrix, paired labels, small comparison strips
Action list    -> scattered action chips near the relevant cluster, not a bottom bar
Sidebar list   -> distributed evidence tags, bracket groups, or satellite annotations
Architecture   -> offset layer map, rectilinear capability field, or hub-and-tags field
```

Avoid using the words "card row", "sidebar", "bottom strip", "process row",
"table box", "dashboard", "contour", "lasso", "organic field", or "curved
border" in freeform editorial prompts unless the user asks for those structures.

### Enterprise Restraint Rule（企业克制度）

Non-grid composition does not mean flashy composition. For enterprise telecom
and academic slides, prefer flat, restrained composition with subtle variation:

```
DO:
  - Use flat 2D designed surfaces, soft tinted panels, data bars, section ribbons,
    modest callouts, and clean typographic hierarchy.
  - Use asymmetry through scale, spacing, and focal placement, not through dramatic perspective.
  - Use mostly straight-edged geometry for enterprise freeform layouts; let freedom
    come from offset placement, varied scale, overlap, indentation, and reading
    hierarchy rather than irregular outlines.
  - Increase density with micro tables, narrow side rails, compact lists, and small flows.
  - For freeform editorial pages, vary cluster size and placement while keeping a visible
    reading path and 10-14 real information units.
  - Break up dense evidence into mixed forms: tags, short bands, small inline matrix,
    mini chart, tiny list, and annotated callout. Avoid turning every item into a card.
  - Keep depth shallow: light shadow, slight overlap, pale background lines, restrained accents.
  - Let the slide feel like a real enterprise PPT page, not a keynote poster or product ad.

AVOID:
  - Wireframe-heavy pages where most elements are empty outlines connected by lines.
  - Dramatic 3D perspective, floating platforms, isometric towers, glossy surfaces.
  - Strong diagonal tilt, heavy layered depth, neon glow, lens flare, cyberpunk effects.
  - Overlapping panels that look like a UI collage or marketing visual.
  - Blob-like curved containers, lasso outlines, and organic contour borders used
    as the default signal for "freeform".
  - Oversized decorative arrows, huge icons, and high-saturation gradients.
  - Reducing a high-density page to a few large panels in the name of restraint.
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
Composition archetype: [executive dashboard | consulting one-pager | process map |
  comparison matrix | architecture map | research summary | evidence matrix |
  hero-anchor | asymmetric editorial | diagonal flow | radial hub |
  layered depth | spotlight + satellites | journey curve |
  rectilinear editorial map | freeform editorial map |
  organic information field only when explicitly requested]
Layout freedom: [structured | semi-structured | freeform editorial]
Required visible information units: [dense: 8-10, ultra-dense: 10-14]

Metadata visibility rule:
- Slide number, slide type, target filename, and rendering mode are not visible
  slide content. Do not draw them as page numbers, corner tabs, labels, or footers.

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
[构图级/区块级布局建议 — 图像模型可优化细节，但不得降级成简陋布局]
  - Focal anchor: [第一视觉焦点，可以是大数字、架构图、结论条、案例图或中心平台]
  - Information units: [dense 8-10 个 / ultra-dense 10-14 个信息单元，每个承载什么内容和视觉形态]
  - Module hierarchy plan: [1 个主证据块 + 2-4 个辅助证明块 + 6-10 个微证据碎片 + 可选底部结论条]
  - Visual-form mix: [至少 5 种信息形态，例如矩阵/流程/架构/关系图/迷你图表/公式/KPI 条/图标行/风险块/证据标签]
  - Header treatment mix: [至少 3 种标题/标签处理，例如主模块蓝色标题条、小 tab、左侧旗标、inline caption、badge label、bracket label]
  - Visual path: [阅读动线：Z 型、对角线、中心辐射、阶梯路径、左右非对称等]
  - Region / cluster notes: [区域、簇、层叠关系或 callout 关系]
  - Freedom / anti-monotony notes: [说明如何避免等宽列、同尺寸卡片、同形重复和所有模块同权]
  - Color mapping: [颜色与语义的对应关系]

## Reference Image Instructions (if applicable)
[仅当 style_reference.type=image 或用户提供背景/母版参考图时填写]
  - Reference role: [background style | brand template | composition reference | freeform layout sketch]
  - Preserve: [背景质感、红蓝比例、标题栏、装饰线、空间节奏等]
  - Do not copy: [旧文字、logo、水印、页码、无关图表]
  - If freeform layout sketch: preserve only cluster rhythm, scale variation,
    offset geometry, reading path, and non-grid composition; regenerate all content.

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
  - Dense content area using multi-zone layouts, varied clusters, compact tables,
    mini charts, or card grids only when the content demands a grid
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
  - Consulting one-pager, dashboard, or freeform editorial information map
  - Multiple zones or clusters: top summary strip, focal anchor, main data field,
    evidence clusters, side/bottom callouts
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

You receive a "design brief" with style rules, a composition archetype, and a full
content pool. You act as a senior PPT information designer: preserve required
content, compress only redundant wording, and design a polished full-slide
enterprise infographic.

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
- NO watermarks, no fake logos, no slide numbers, no copyright marks.
- NO simplistic three-card layout unless the brief explicitly asks for only three items.

## SLIDE ART DIRECTION CONTRACT

- Finished 16:9 PPT page, not a poster or loose illustration.
- Compact title area, usually 10-15% of canvas height.
- Dense slides must show 8-10 meaningful information units.
- Ultra-dense enterprise slides must show 10-14 meaningful information units.
- Include at least one compact table, metric matrix, mini chart, or 4+ row structured list.
- Use a clear composition archetype, which may be grid-based or non-grid:
  dashboard, one-pager, process map, comparison matrix, architecture map,
  evidence matrix, research summary, hero-anchor, asymmetric editorial,
  diagonal flow, radial hub, layered depth, spotlight + satellites, journey curve,
  flat dense asymmetry, rectilinear editorial map, freeform editorial map,
  organic information field only when explicitly requested.
- Respect the requested layout freedom level:
  structured uses visible alignment; semi-structured varies scale and regions;
  freeform editorial avoids obvious card grids and equal columns while preserving
  a clear reading path, focal anchor, density, and enterprise restraint.
- Keep the style flat and restrained unless the brief explicitly asks for dramatic depth.
- Each information unit must contain real labels, numbers, claims, steps, evidence, or actions.
- Prefer KPI cards, tables, matrices, annotated charts, process flows, and architecture layers.
- Use decorative icons only as small labels; never as the main content.
- Keep typography readable at 100% zoom with crisp Chinese text.

## STYLE INSTRUCTIONS

{{STYLE_INSTRUCTIONS}}

## SLIDE CONTENT

{{SLIDE_CONTENT}}

## YOUR TASK

Read the SLIDE CONTENT above. It contains the required content pool and may
include a composition archetype. Preserve the required content and DESIGN a
professional slide image. You decide the final composition, but must follow:
  - The specified composition archetype and major regions/clusters/focal anchor
  - The specified layout freedom level
  - The density target and approximate information-unit count
  - The semantic color mapping from STYLE INSTRUCTIONS
  - The visual form requested for each group: KPI card, table cell, chart,
    badge, text block, diagram node, architecture layer, callout, etc.

The headline and all explicitly marked required content are mandatory. If space
is tight, compress wording but keep the data, labels, and logic intact.

Produce the slide image now.
```

---

## STYLE_INSTRUCTIONS Filling Guide（风格参数填充指南）

`{{STYLE_INSTRUCTIONS}}` 占位符应替换为以下格式的具体参数块。完整维度定义见 `dimensions/` 目录下各文件。

```
背景: #F8FAFC
主色: #C41E24
辅色: #005BAC
强调色: #25364D

文字色:
  标题: #1F2937
  正文: #1F2937
  次要: #6B7280
  弱化: #9CA3AF

模块色（用于视觉分组与语义编码）:
  电信红: #C41E24
  科技蓝: #005BAC
  深灰蓝: #25364D
  成功绿: #059669
  警告橙: #D97706
  风险红: #DC2626

字体:
  标题字体: 苹方 / 微软雅黑 / Noto Sans SC, 无衬线
  正文字体: 苹方 / 微软雅黑 / Noto Sans SC, 无衬线
  标题字号: 28-32px, 字重 700-750
  正文字号: 12-14px, 字重 400

视觉风格:
  预设风格: 电信高信息密度风格 (china-telecom)
  质感: 柔和阴影 (soft-shadow)
  间距: 紧凑 (compact)
  卡片: 浅灰白填充, 淡边框 #E5E7EB, 小圆角, 轻投影
  表格: 电信红表头, 科技蓝关键数据, #FFFFFF / #F8FAFC 交替行
  图标: 仅作小标签, 不作为主要内容
  图表: 干净网格线, 数据标签明确, 红蓝灰语义编码
  参考图: 如有, 只继承背景质感/母版节奏/红蓝比例, 不复制旧文字和 logo
```

---

## SLIDE_CONTENT Filling Guide（内容素材填充指南）

`{{SLIDE_CONTENT}}` 占位符应替换为**最大化的内容素材 + 区块级版式约束**。关键原则：**内容必须具体，布局必须明确到区域和组件类型**。

不要只写抽象标签。把所有相关数据、洞察、背景、流程步骤、对比维度写进去，并标明哪些内容 required、哪些 optional。图像模型可以压缩冗余措辞，但不得删除 required 内容或把复杂页降级成简陋布局。

---

## Filled Example（完整填充示例）

以下展示一个实际填充后的图片模式提示词。注意 SLIDE_CONTENT 部分既提供完整素材，也指定 composition archetype 和 required visible information units。

```
You are an expert presentation designer and information architect who creates
information-dense, visually polished slide images for professional presentations.

You receive a "design brief" with style rules, a composition archetype, and a full
content pool. You act as a senior PPT information designer.

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
