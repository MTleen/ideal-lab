---
name: ideal-ppt-prompt
description: Use when P5 outline review is completed and prompt engineering phase begins. Supports dual rendering modes — html (CSS layout prompts) and image (content-rich image generation prompts). Triggered by ideal-ppt-workflow at P7.
---

# ideal-ppt-prompt

## 角色定义

**提示词工程师 (Prompt Engineer)**

将幻灯片大纲转换为自包含的生成提示词。根据渲染模式（rendering_mode）分为两条路径：

- **html 模式**：生成精确的 CSS Grid 布局指令提示词，交给 HTML 渲染引擎产出幻灯片
- **image 模式**：生成内容丰富的图像生成提示词，交给图像模型产出幻灯片图片

每个提示词必须独立完整，无需任何外部上下文即可产出最终幻灯片。

---

## 前置门控

| 检查项 | 条件 | 验证方式 |
|--------|------|----------|
| P5 产物 | `outline.md` 存在且非空 | `test -f outline.md && test -s outline.md` |
| P3 产物 | `design-spec.md`（策略阶段的设计规格）存在且非空 | `test -f design-spec.md && test -s design-spec.md` |
| P6 评审 | 大纲审核已通过（`approved` 或 `auto_approved`） | 读取 `流程状态.md` 确认 P6 状态 |
| 工作目录 | 当前项目目录下存在 `prompts/` 目录或可创建 | `mkdir -p prompts` |

若门控未通过，输出缺失项清单，提示用户完成前置阶段后重试。

---

## 工作流程

### Step 1: 读取源文件并提取关键信息

1. 读取 `流程状态.md`，提取 **rendering_mode**（取值为 `html` 或 `image`）。该值决定后续所有步骤走哪条路径。

2. 读取 `outline.md`，提取以下内容：
   - **STYLE_INSTRUCTIONS 块**：从大纲文件头部的风格指令区域提取，包含配色、字体、布局规则
   - **幻灯片列表**：每页幻灯片的编号、标题、类型、内容摘要、布局建议、备注
   - **全局参数**：总页数、叙事弧线、风格预设名称

3. 读取 `design-spec.md`，提取以下内容：
   - **视觉主题参数**：主色 / 辅助色 / 强调色的 HEX 值
   - **字体系统**：标题字体、正文字体、强调字体及字号层级
   - **排版原则**：对齐规则、间距体系、视觉层次
   - **技术约束**：SVG 兼容性规则、画布尺寸
   - **图标使用规格**：图标风格和用法
   - **设计检查清单**：每页必须满足的设计规范

4. 合并两份文件的信息，形成每个提示词所需的完整风格参数集。

### Rendering Mode 分支

根据 `rendering_mode` 选择不同的参考文档和提示词构建策略：

| 维度 | rendering_mode=html | rendering_mode=image |
|------|---------------------|----------------------|
| 参考模板 | `references/base-prompt.md` | `references/base-prompt-image.md` |
| 提示词重点 | 精确的 CSS Grid 布局指令、定位、间距 | 完整内容素材 + 风格简报 + 密度等级 |
| STYLE_INSTRUCTIONS | CSS Custom Properties（颜色变量、字体栈、间距规则） | Style Brief（两种企业风格之一 + 可选参考图约束） |
| SLIDE_CONTENT | 精选内容子集，配合布局指令 | **全部相关内容**，但必须标明 required / optional |
| 布局决策 | 由提示词明确指定（卡片位置、尺寸） | 由提示词指定构图原型和信息单元，图像模型做视觉细化 |
| 输出清单 | `html-generation-manifest.json` | `image-generation-manifest.json` |

### Step 2: 为每页幻灯片生成提示词

对 `outline.md` 中的每一页幻灯片执行以下操作：

1. **确定幻灯片元数据**：
   - 编号（NN，两位数，如 01、02）
   - 标题（从大纲提取，转为 URL-safe slug）
   - 类型（cover / section / content / data / comparison / process / quote / ending）
   - 目标文件名（html 模式：`NN-slide-{slug}.html`，image 模式：`NN-slide-{slug}.png`）

2. **构建提示词内容（按 rendering_mode 分支）**：

   #### rendering_mode=html

   基于模板 `references/base-prompt.md`，填充以下两个插入点：
   - **STYLE_INSTRUCTIONS**：CSS Custom Properties — 从 design-spec.md 提取的视觉参数（颜色变量、字体栈、间距规则、排版约束）
   - **SLIDE CONTENT**：从 outline.md 提取的精选内容子集（标题、正文、数据、视觉描述），配合 CSS Grid 布局指令精确指定卡片位置和尺寸

   #### rendering_mode=image

   基于模板 `references/base-prompt-image.md`，填充以下两个插入点：
   - **STYLE_INSTRUCTIONS**：Style Brief — 视觉风格描述，引用预设风格或从维度组合。格式要求包含：
     - 预设风格：仅允许 `scientific`（学术风格）或 `china-telecom`（电信高信息密度风格）
     - 质感（quality）：flat / soft-shadow / glassmorphism / neumorphism / layered-depth
     - 间距（spacing）：compact / standard / generous / editorial
     - 配色方案（主色/辅色/强调色/文字色/模块色）
     - 字体体系（标题/正文/数据字体）
     - 视觉元素规则（卡片样式、表格样式、图标风格）
     - 可选参考图片约束：当 `style_reference.type=image` 时，写明参考图承担的角色（背景风格/品牌母版/版式参考）以及禁止复制的旧文字、logo、水印、页码

     格式示例：
     ```
     Style Brief:
     - 预设风格：电信高信息密度风格（china-telecom）— 央企政企汇报、红蓝品牌节奏、高密度 one-pager
     - 质感：soft-shadow（柔和阴影，微浮层感）
     - 间距：compact（标题区 10-15%，主体区最大化）
     - 主色调：电信红 #C41E24 / 科技蓝 #005BAC / 深灰蓝 #25364D
     - 背景色：#F8FAFC 或参考图中的浅灰科技背景
     - 字体：标题 28-32px 粗体无衬线 / 正文 12-14px / 数据 20-24px
     - 卡片：浅灰白填充 + 细边框 + 小圆角 + 轻投影
     - 表格：红色表头、蓝色关键数据、浅灰交替行
     - 参考图：如有电信 PPT 背景图，只继承背景质感、红蓝比例、标题栏和装饰线；禁止复制旧文字、logo、水印、页码
     ```
   - **SLIDE_CONTENT**：从 outline.md 提取该页全部相关内容，并标明 required / optional。必须包含：
     - Headline / Subtitle / Core conclusion
     - Density level 和 required visible information units（dense 8-10 个，ultra-dense 10-14 个）
     - Layout freedom（`structured` / `semi-structured` / `freeform editorial`）：用户要求“自由排版”“不规整”“更有设计感”“不要网格”时必须使用 `freeform editorial`
     - Composition archetype（可为规整型或非规整型；电信/学术高密汇报默认优先用 `controlled editorial grid` 或 `flat dense asymmetry`；用户嫌规整时优先切到 `rectilinear editorial map`，再按内容选择 `freeform editorial map`；也可用 executive dashboard / consulting one-pager / architecture map / hero-anchor / asymmetric editorial / diagonal flow / radial hub / layered depth / journey curve 等）
     - 每个主要信息单元的内容清单、视觉形态、色彩语义、焦点层级和阅读动线
     - 若为 `controlled editorial grid` 或 `rectilinear editorial map`，必须写明 `module hierarchy plan`（1 个主证据块 + 2-4 个辅助证明块 + 6-10 个微证据碎片 + 可选底部结论条）、`visual-form mix`（至少 5 种信息形态，例如矩阵、流程、架构图、关系图、迷你图表、公式、KPI 条、图标行、风险块、证据标签）和 `header treatment mix`（至少 3 种标题/标签处理，避免所有模块同样蓝色标题条）
     - 若为 freeform editorial，必须写明 `anti-grid plan`：如何避免等宽列、同尺寸卡片、明显网格、左侧 KPI 竖排、右侧大侧栏、横向流程节点和“顶部流程 + 中部卡片 + 底部行动条”模板，同时保留信息密度与阅读动线；密度锚点可拆成嵌入式微矩阵、小横条、迷你图表、标签组和短注释
     - 若上一轮 image 输出仍明显网格化，必须在 Reference Image Instructions 中要求使用或生成 `freeform layout sketch` 作为 composition reference；不要只追加更多文字禁令
     - 所有数据点、要点、流程步骤、对比维度、架构层级

   **关键判断**：图片模式 prompt 不是只给素材让模型自由发挥，也不是把每个元素写成绝对坐标，更不是强制所有页面使用规整网格。正确粒度是“内容全量明确 + 版式自由度明确 + 构图原型明确 + 信息单元明确 + anti-monotony / anti-grid plan 明确 + 风格强约束 + 视觉细节交给 gpt-image-2 优化”。电信/学术高密页的目标不是消灭网格，而是消灭机械等分和同形重复。用户反馈“太规整”时，先判断问题是“所有模块等大同权”还是“确实需要概念自由图”。多数企业页应保留隐形网格、标题带、底部结论条和模块纪律，并切到 `controlled editorial grid` 或 `rectilinear editorial map`：用 1 个主证据块、2-4 个辅助证明块、6-10 个微证据碎片、至少 5 种信息形态、不等大信息簇、平直错位区块、阶梯动线、嵌入式微矩阵/迷你图表/证据 chips 的组合，同时明确禁止等宽列、同尺寸卡片、左侧 KPI 竖排、横向流程节点、右侧栏和常规上中下模板。不要把自由排版默认写成曲线边框、泡泡轮廓、套索形状或有机地图；只有用户明确要求“生态地图/有机地图/轮廓能力图”时才使用这些形态。

3. **内容深度检查**：
   对每个提示词执行 `references/content-depth-rules.md` 中的检查清单，确保无抽象标签、无空列表、无占位符。

4. **保存提示词文件**：
   ```
   prompts/NN-slide-{slug}.md
   ```

### Step 3: 自包含验证

每个提示词文件必须通过以下完整性检查：

| 检查项 | 要求 |
|--------|------|
| 风格参数完整 | 包含完整的 STYLE_INSTRUCTIONS 块，颜色值、字体栈、间距规则全部具体 |
| 内容具体化 | 所有列表项有具体内容，无"如 XXX"、"待补充"等抽象标签 |
| 数据完整 | 所有数据点有具体数值和单位，无占位符 |
| 视觉描述具体 | 布局描述使用具体尺寸和位置，不使用"适当"、"合适"等模糊词 |
| 无外部依赖 | 提示词内不引用其他文件路径，不要求"参考上一页" |
| 幻灯片元数据 | 包含 slide_number、slide_type、target_filename 字段 |

**检查失败时**：重新生成该提示词，补充具体内容，直到通过所有检查。

### Step 4: 输出并汇总

1. 将所有提示词文件保存到 `prompts/` 目录
2. 运行 `scripts/generate-manifest.py` 生成清单文件：
   - rendering_mode=html → `prompts/html-generation-manifest.json`
   - rendering_mode=image → `prompts/image-generation-manifest.json`
3. 输出执行摘要：

```
P7 提示词工程完成（rendering_mode: {html|image}）

生成文件：
  prompts/01-slide-cover.md         — 封面
  prompts/02-slide-background.md    — 行业背景
  prompts/03-slide-data.md          — 核心数据
  ...
  prompts/12-slide-summary.md       — 总结

共 N 页提示词，全部通过自包含验证。
清单文件：prompts/{html|image}-generation-manifest.json
```

---

## 内容深度强制规则

**核心原则：提示词中禁止出现任何抽象标签或未具体化的内容。**

每条提示词在输出前必须通过以下检查（详见 `references/content-depth-rules.md`）：

### 检查清单

| 编号 | 规则 | 示例 |
|------|------|------|
| R1 | 列表必须包含每项的具体内容 | "三个核心指标：营收增长 42%、用户留存率 85%、NPS 72" |
| R2 | 机制/流程必须有具体步骤 | "Step 1 数据采集 → Step 2 特征工程 → Step 3 模型训练 → Step 4 结果评估" |
| R3 | 数据必须有实际数值和单位 | "市场规模 6,800 亿元" 而非 "市场规模巨大" |
| R4 | 对比必须有维度和具体内容 | "方案 A（成本低 30%，部署快 2 周）vs 方案 B（性能高 50%，可扩展性强）" |
| R5 | 视觉描述必须描述具体布局和数据排列 | "3 行卡片网格：第 1 行蓝色卡片..." |

### 反模式（必须避免）

```
BAD:  "展示三个关键指标"
BAD:  "流程图展示各阶段"
BAD:  "对比表格呈现差异"
BAD:  "适当的数据可视化"
BAD:  "参考行业数据"
```

### 正确模式（必须达到）

```
GOOD: "3 列数字卡片：左列 '#2196F3 蓝色卡片，数值 ¥2,380 万，标签 Q1 营收'，
       中列 '#4CAF50 绿色卡片，数值 92%，标签 客户满意度'，
       右列 '#FF9800 橙色卡片，数值 1,200+，标签 活跃客户数'"
```

---

## 提示词工程参考

本技能依赖以下参考文档：

### 核心模板

| 文档 | 用途 |
|------|------|
| `references/base-prompt.md` | HTML 模式基础提示词模板，包含精确布局指令（CSS Grid、定位、间距），两个插入点 |
| `references/base-prompt-image.md` | Image 模式基础提示词模板，包含内容简报 + 风格简报格式，两个插入点 |
| `references/prompt-engineering.md` | 提示词编写指南，结构规范和正反示例 |
| `references/content-depth-rules.md` | 内容深度规则，反抽象检查清单 |
| `scripts/generate-manifest.py` | 清单生成脚本，根据 rendering_mode 产出对应 manifest JSON |

### 风格体系（image 模式）

所有风格定义采用 **DESIGN.md** 格式（Google Labs 开源协议适配版），包含 YAML frontmatter（机器可读设计 token）+ Markdown body（人类可读设计 rationale）。

| 文档 | 用途 |
|------|------|
| `references/style-template-DESIGN.md` | DESIGN.md 格式规范模板，定义文件结构和必需字段 |
| `references/styles/scientific.md` | 学术风格定义（研究汇报、论文、实验、综述） |
| `references/styles/china-telecom.md` | 电信高信息密度风格定义（央企政企、云网算力、AI、安全、解决方案） |
| `references/dimensions/density.md` | 密度维度：minimal / balanced / dense / ultra-dense |
| `references/dimensions/mood.md` | 色调维度：professional / warm / cool / vibrant / dark / neutral |
| `references/dimensions/texture.md` | 纹理维度：clean / grid / organic / pixel / paper |
| `references/dimensions/typography.md` | 字体维度：geometric / humanist / handwritten / editorial / technical |
| `references/dimensions/presets.md` | 预设映射：scientific / china-telecom |

---

## 输出产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 提示词文件 | `prompts/NN-slide-{slug}.md` | 每页幻灯片一个，自包含的生成提示词 |
| 生成清单（html） | `prompts/html-generation-manifest.json` | HTML 模式提示词索引清单，供 P11 HTML 执行阶段使用 |
| 生成清单（image） | `prompts/image-generation-manifest.json` | Image 模式提示词索引清单，供 P11 图像执行阶段使用 |

### 提示词文件命名规范

```
prompts/
├── 01-slide-cover.md
├── 02-slide-industry-overview.md
├── 03-slide-market-data.md
├── 04-slide-core-product.md
├── 05-slide-architecture.md
├── 06-slide-comparison.md
├── 07-slide-case-study.md
├── 08-slide-roadmap.md
├── 09-slide-team.md
├── 10-slide-next-steps.md
└── {html|image}-generation-manifest.json
```

**命名规则**：
- 编号：两位数字，从 01 开始顺序编号
- 分隔符：`-slide-`
- Slug：英文小写，连字符分隔，取自标题关键词
- 扩展名：`.md`

---

## 与其他阶段的关系

### 上游输入

| 来源阶段 | 产物 | 本阶段如何使用 |
|---------|------|---------------|
| P5 大纲生成 | `outline.md` | 提取每页幻灯片的结构、内容、类型 |
| P3 策略规划 | `design-spec.md` | 提取风格参数、配色、字体、排版规则 |

### 下游消费

| 目标阶段 | 本阶段产物 | 使用方式 |
|---------|----------|---------|
| P8 提示词审核 | `prompts/*.md` | 用户审核提示词质量和完整性 |
| P9 图像生成 | `prompts/*.md` | 提取需要配图的页面信息 |
| P11 HTML 执行 | `prompts/*.md` + `html-generation-manifest.json` | 逐页读取提示词渲染 HTML（html 模式） |
| P11 图像执行 | `prompts/*.md` + `image-generation-manifest.json` | 逐页读取提示词生成图像（image 模式） |

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| `outline.md` 不存在 | 输出错误：P5 大纲未生成，提示先完成 P5 |
| `design-spec.md` 不存在 | 输出错误：P3 策略未完成，提示先完成 P3 |
| `outline.md` 中某页内容为空 | 跳过该页，记录警告，继续处理其余页面 |
| 内容深度检查未通过 | 重新生成该页提示词，补充具体内容，最多重试 3 次 |
| `prompts/` 目录写入失败 | 检查权限，尝试创建目录，报告错误 |
| 提示词数量与大纲页数不匹配 | 报告差异，列出缺失或多余的页面编号 |

---

## 使用示例

### HTML 模式示例

```
输入：
  流程状态.md → rendering_mode=html
  outline.md（10 页幻灯片大纲）
  design-spec.md（电信高信息密度风格，红蓝配色，PingFang SC 字体）

处理流程：
  1. 读取 流程状态.md → rendering_mode=html
  2. 读取 outline.md → 提取 10 页幻灯片内容和 STYLE_INSTRUCTIONS
  3. 读取 design-spec.md → 提取 #005587 / #2196F3 / #FF9800 配色等
  4. 逐页生成提示词（base-prompt.md 模板）：
     - 01-slide-cover.md → 封面：CSS Grid 布局，标题居中，副标题下方
     - 02-slide-background.md → 背景：3 个行业数据卡片（精确 Grid 定位）
     - 03-slide-architecture.md → 架构图：4 层技术栈（每层具体组件名 + CSS 布局）
     ...
  5. 每页通过内容深度检查
  6. 保存到 prompts/ 目录
  7. 运行 generate-manifest.py → 生成 html-generation-manifest.json

输出：
  prompts/01-slide-cover.md ... prompts/10-slide-next-steps.md
  prompts/html-generation-manifest.json
```

### Image 模式示例

```
输入：
  流程状态.md → rendering_mode=image
  outline.md（10 页幻灯片大纲）
  styles/china-telecom.md（DESIGN.md 格式电信高信息密度风格定义，含完整 token）

处理流程：
  1. 读取 流程状态.md → rendering_mode=image
  2. 读取 outline.md → 提取 10 页幻灯片完整内容（不裁剪）
  3. 读取 styles/china-telecom.md → 解析 YAML frontmatter 提取颜色/字体/间距 token，
     读取 Markdown body 提取设计 rationale（Do/Don't、组件规范）
  4. 合并为 Style Brief，逐页生成提示词（base-prompt-image.md 模板）：
     - 01-slide-cover.md → 封面：完整标题 + 副标题 + 日期 + Style Brief
     - 02-slide-background.md → dashboard：全部数据点 + 趋势描述 + 6 个信息单元 + Style Brief
     - 03-slide-architecture.md → architecture map：4 层完整组件说明 + 连接关系 + Style Brief
     ...
  5. 每页通过内容深度检查
  6. 保存到 prompts/ 目录
  7. 运行 generate-manifest.py → 生成 image-generation-manifest.json

输出：
  prompts/01-slide-cover.md ... prompts/10-slide-next-steps.md
  prompts/image-generation-manifest.json
```
