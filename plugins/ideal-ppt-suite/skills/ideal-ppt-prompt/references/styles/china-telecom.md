---
version: beta
name: 电信高信息密度风格
description: 面向中国电信、央企政企汇报、算力云网、安全、AI 与行业解决方案的高信息密度 PPT 风格。
colors:
  primary: "#C41E24"
  secondary: "#005BAC"
  tertiary: "#25364D"
  neutral: "#6B7280"
  surface: "#F8FAFC"
  on-surface: "#1F2937"
  error: "#DC2626"
  success: "#059669"
  warning: "#D97706"
typography:
  display:
    fontFamily: "Noto Sans SC / PingFang SC / Microsoft YaHei"
    fontSize: "38px"
    fontWeight: "750"
    lineHeight: "1.15"
  h1:
    fontFamily: "Noto Sans SC / PingFang SC / Microsoft YaHei"
    fontSize: "30px"
    fontWeight: "750"
    lineHeight: "1.2"
  h2:
    fontFamily: "Noto Sans SC / PingFang SC / Microsoft YaHei"
    fontSize: "18px"
    fontWeight: "650"
    lineHeight: "1.25"
  body:
    fontFamily: "Noto Sans SC / PingFang SC / Microsoft YaHei"
    fontSize: "13px"
    fontWeight: "400"
    lineHeight: "1.42"
  label:
    fontFamily: "Noto Sans SC / PingFang SC / Microsoft YaHei"
    fontSize: "10px"
    fontWeight: "500"
    lineHeight: "1.25"
  data-value:
    fontFamily: "DIN / Inter / Noto Sans SC"
    fontSize: "22px"
    fontWeight: "750"
    lineHeight: "1.1"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "18px"
  xl: "24px"
  gutter: "14px"
  margin: "24px"
rounded:
  sm: "2px"
  md: "4px"
  lg: "6px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "#E5E7EB"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "#FFFFFF"
    rowAltBackgroundColor: "{colors.surface}"
  chart:
    gridColor: "#E5E7EB"
    dataColors: ["#C41E24", "#005BAC", "#25364D", "#059669", "#D97706", "#DC2626"]
dimensions:
  texture: clean
  mood: professional
  typography-style: geometric
  density: ultra-dense
  quality: soft-shadow
  spacing-level: compact
---

# 电信高信息密度风格

## Overview

电信高信息密度风格服务于企业汇报和政企技术方案，不是通用“红蓝商务风”。它应呈现为成熟、克制、偏平面的咨询级 one-pager：信息多但秩序强，红色做品牌锚点和结论强调，蓝色做技术模块和数据分区，深灰蓝负责稳定画面。可以有非对称构图和轻微层次，但不能变成炫技海报、3D 平台或强透视科技广告。画面可以使用用户提供的电信 PPT 背景图作为底层参考，但文字、图表、卡片必须重新排版生成。

## Reference Image Handling

当用户提供电信 PPT 背景图、母版截图或品牌参考图时：

- 参考图只用于继承背景质感、红蓝比例、标题栏气质、装饰线条和空间节奏。
- 不要复制参考图中的旧文字、logo、水印、页码或无关图表。
- 如果参考图是背景图，生成页应保留类似的浅灰科技底纹、红色角标、蓝色结构线或顶部/底部品牌带，但内容层必须按当前页重新组织。
- 如果参考图是自由排版布局草图，只继承非网格构图节奏、平直几何区块、信息簇大小差异和阅读路径；不得复制草图中的占位文字或把草图当成最终内容。除非用户明确要求“生态地图/有机地图/轮廓能力图”，不要把自由排版解释成不规则曲线边框。
- 如果参考图与当前内容冲突，以当前页内容可读性优先，参考图只作为风格锚点。

## Prompt Intent

图片生成 prompt 必须写清楚每页的内容、构图原型和信息单元。推荐粒度是“构图级布局 + 每个信息单元清单 + 视觉编码规则”：

- 需要明确标题、副标题、核心结论、关键数据、流程步骤、对比维度或架构层级。
- 需要明确版式自由度：structured / semi-structured / freeform editorial。用户要求“自由排版”“不规整”“更有设计感”“不要网格”时，优先使用 freeform editorial。
- 需要明确采用哪种构图原型，可以是规整型，也可以是非规整型，例如 dashboard、consulting one-pager、architecture map、comparison matrix、process map、hero-anchor、asymmetric editorial、diagonal flow、radial hub、layered depth、rectilinear editorial map、freeform editorial map。
- 不需要把每个元素写成绝对坐标，除非用户要求复刻固定模板。
- 非规整构图应保持平面、克制和真实汇报感，避免明显 3D、漂浮透视、强斜切、霓虹光效或营销海报感。
- 用户说“自由排版”时，默认含义是版心、尺度、错位、层级和阅读路径更自由，不是默认使用曲线边框、泡泡轮廓、套索形状或有机地图。
- 若 freeform editorial 生成后仍明显网格化，下一轮不要继续堆叠文字禁令；应生成或使用一张 `freeform layout sketch` 作为 composition reference，再由 gpt-image-2 按当前内容重绘。

## Reference Deck Diagnosis

典型电信/学术高密度汇报页并不是“无网格自由排版”。它通常是：

- 原生 PPT 层只保留标题、页眉、页码或 logo，主体是一张完整信息图图片。
- 页面有强模板：红色标题、顶部品牌色带、右上角标识、底部总结/指标条、统一蓝色模块标题。
- 主体有隐形网格：2-3 个大区块、若干小证明块、微表格、流程条、图标说明、公式/图谱/柱状图混排。
- 好看的关键是多尺度信息层级，而不是不规则外形：大图/大矩阵负责主叙事，小卡/标签/图标负责证据，底部条负责结论收束。
- “不死板”来自模块比例变化、局部错位、图文混排和跨区箭头；不是来自曲线边框、随机散点或完全脱离对齐。

因此，电信高信息密度风格默认应追求“强模板下的编辑式变化”，而不是反网格。只有在用户明确要求概念地图、生态图或能力地形时，才使用有机/轮廓类构图。

## Anti-Monotony Requirements

电信高密页必须显式规划“主次证据层级”和“视觉形态混合”，否则模型容易退回统一矩形模块：

- 每页应有 1 个主证据块：主矩阵、主流程、主架构图、主对比表或主图谱，承担本页论证主线。
- 应有 2-4 个辅助证明块：风险、治理、指标、场景、技术组件、验证结果等，尺寸和形态不能全部相同。
- 应有 6-10 个微证据碎片：指标 chip、迷你柱状图/折线图、公式、图标标签、证据 tag、风险提示、短注释。
- ultra-dense 页面至少混合 5 种信息形态：矩阵/表格、流程条、架构/层级图、关系图、迷你图表、公式、KPI 条、图标行、风险应对块、对比条、证据标签组。
- 不要让超过 40% 的可见模块共享完全相同的容器样式、尺寸和视觉角色。
- 全宽蓝色模块标题条只用于 1-3 个主模块；辅助模块和微证据应使用小 tab、左侧旗标、inline caption、badge label、bracket label 或图标引导标签。
- 不要让所有矩形模块都拥有同样的蓝色标题条，否则即使内容丰富，也会显得像机械工程模板。
- 如果页面看起来单调，优先增加微图表、公式/机制片段、关系小图、证据 tag 和主次尺度差异，而不是加入曲线边框或装饰背景。

## Visual System

- 16:9 横版，默认 1280x720。
- 标题区占画面 10%-15%，不能用超大标题浪费空间。
- 主体区必须有高密度信息：dense 页面 8-10 个信息单元，ultra-dense 页面 10-14 个信息单元。常见为 KPI 卡、流程节点、对比表、架构层、风险提示、行动项、结论锚点、环绕 callout、层叠面板。
- 每页至少包含一个“密度锚点”：紧凑对比表、指标矩阵、4+ 行结构化清单、迷你趋势图或 5+ 节点流程图。不能只靠几个大面板撑版面。
- 正文区允许 11-12px 标签和 12-13px 正文，但必须可读；通过小标题、色条、细线和留白分组，而不是减少内容。
- 页面不能像线框图。边框和连接线只能辅助分组，不能成为主要视觉语言。至少 40% 内容区应由浅色填充面、红蓝色带、数据条、分区底色、迷你图表、填充型能力模块构成。
- 卡片使用浅灰白或浅蓝灰填充、细边框、小圆角、轻投影；每张卡片要有标题、数据或结论，不能只是空线框或图标。
- 红色面积控制在 8%-15%，用于结论、关键数字、风险或标题锚点；蓝色用于技术链路、云网算力、安全、AI 模块。
- 背景可有极浅科技线条、网格、点阵或弧线，但不得抢文字。
- 深度只能是浅层次：轻投影、轻微重叠、浅色分区、细线连接。不要使用明显 3D 透视、悬浮平台、玻璃质感、高光或强渐变。

## Layout Archetypes

- **Flat dense asymmetry（稳态默认）**: 平面中心能力图或结论锚点 + 一侧窄栏 + 一个微表格/指标矩阵 + 一个小流程 + 底部路线图。适合管理汇报、状态页和结构清晰的方案页。通过浅色面、色带、数据条、轻微错位和尺度差异打破网格感，但保持真实企业汇报页的克制和高密度。
- **Rectilinear editorial map（平直编辑式自由排版，默认推荐）**: 适合用户要求不规整、自由排版但仍希望企业 PPT 克制平面。使用不等宽/不等高的平直区块、错位色带、窄数据条、括号分组、嵌入式微矩阵、小图表和 staggered callout。自由感来自尺度差异、版心偏移、局部重叠、缩进和视觉动线，而不是曲线边框。禁止明显等宽列、同尺寸卡片矩阵、左侧 KPI 竖排、右侧大侧栏、横向流程节点和底部行动条。
- **Controlled editorial grid（受控编辑网格，高密汇报默认）**: 适合研究汇报、技术路线、方案论证、可行性分析等页面。保留标题带、模块边界、底部总结条和隐形网格；通过一个主图/主矩阵 + 2-4 个辅助证明块 + 若干指标/图标/公式碎片形成高密度。不要把“网格”视为错误，错误的是所有模块等大、同形、同权重。必须写出 module hierarchy plan 和 visual-form mix。
- **Freeform editorial map（自由编排备选）**: 适合概念关系复杂、策略类内容。画面不使用等宽列、同尺寸卡片、明显 2x2/3x3 网格，不能退回“顶部流程 + 中部卡片 + 底部行动条”的模板。用一个结论锚点、若干不等大的信息簇、短连接路径、嵌入式微表格/小图表/数据条/证据 chips 形成平面信息地图。自由编排必须有清晰阅读动线，不能随机散落。
- **Organic / contour map（有机/轮廓类，仅显式要求时使用）**: 只有用户明确要求“生态地图”“能力地形”“有机信息场”“轮廓能力图”时才用曲线边界、轮廓区或 lasso 形状。默认电信企业页不要用不规则曲线边框来表达自由排版。
- **Executive dashboard**: 顶部结论条 + 4 个 KPI + 主图表 + 风险/行动项侧栏。
- **Consulting one-pager**: 左侧问题/目标，中部解决方案结构，右侧价值与指标，底部推进路径。
- **Architecture map**: 分层架构图，包含接入层、平台层、能力层、应用层、安全运营层。
- **Process map**: 4-6 步横向流程，每步含输入、动作、输出和责任主体。
- **Comparison matrix**: 传统方案 vs 电信方案或多方案对比，必须有维度、数值和结论。
- **Industry solution page**: 行业痛点、能力组合、落地场景、成效指标四区联动。
- **Hero-anchor**: 一个大数字、中心架构或核心结论作为视觉锚点，周围用平面 callout 补充证据。
- **Asymmetric editorial**: 一侧大面积结论/图形，另一侧密集支撑信息，用尺度和留白取得平衡，保持平面。
- **Diagonal flow**: 信息沿轻微斜向推进，适合转型、迁移、升级路径；斜率要克制，不做强烈斜切构图。
- **Radial hub**: 中心平台能力向四周业务场景、模块或价值扩散，使用细线连接，不做 3D 中心岛。
- **Layered depth**: 用轻微重叠面板表达主次、阶段或能力堆栈，避免悬浮、强投影和玻璃质感。

## Do's and Don'ts

- Do: 用真实业务词、指标、模块名填满信息单元。
- Do: 增加微表格、指标矩阵、迷你流程、风险/行动项清单来提高真实信息密度。
- Do: 默认在 `semi-structured` 的 flat dense asymmetry 与 `freeform editorial` 的自由信息地图之间选择；用户嫌规整时必须切到 freeform editorial。
- Do: 用浅色填充面、红蓝色带、数据条、迷你图表和填充型模块提升设计感，避免只有线框和连接线。
- Do: 让图表、表格、流程和架构图承担主要视觉重量。
- Do: 需要更有设计感时使用非规整或自由编排构图，但必须保持阅读动线清晰、信息单元完整、企业克制。
- Do: 把“不要死板”优先理解为打破等分、等权、同形重复，而不是取消网格或改成曲线外框。
- Do: 为高密页显式混合至少 5 种信息形态，例如主矩阵、流程条、迷你图表、关系小图、公式/机制片段、指标条、风险块和证据标签。
- Do: 自由编排时把密度锚点嵌入信息场，例如小型横条、微矩阵、迷你柱条、标签组和短注释，而不是都做成独立大表格/大卡片。
- Do: 自由编排时优先使用平直错位区块、窄色带、数据飘带、胶囊标签、括号分组、散点式行动 chips、阶梯 waypoint，而不是 KPI 卡片、右侧栏、横向流程节点。
- Do: 保持平面、稳重、真实企业汇报感，使用轻微构图变化而非视觉特效。
- Do: 使用参考图片保持电信背景气质和红蓝品牌节奏。
- Don't: 生成只有 3 个大卡片、几个图标和空泛标题的简陋页。
- Don't: 用户要求自由排版时仍生成等宽三列、2x2/3x3 卡片矩阵、固定侧栏 + 底栏的模板化结构。
- Don't: 为了“不网格”而丢掉汇报页应有的标题带、模块纪律、对齐关系和底部结论收束。
- Don't: 让全页大部分模块都是同一种浅色矩形卡片 + 蓝色标题条；这会产生模板化工程汇报感。
- Don't: 用户要求自由排版时仍生成“上方流程、中间卡片、下方行动条”的常规企业模板。
- Don't: 自由编排页出现 3 个以上同样式 KPI 卡片竖排、4 个以上同样式流程节点横排、一个大右侧栏或全宽底栏。
- Don't: 把“自由排版”默认画成泡泡状、不规则曲线边框、套索轮廓或有机地形图。
- Don't: 生成线框图感很强的页面，避免大量空心矩形、细线连接和无填充模块。
- Don't: 大面积使用纯红背景或高饱和渐变，避免廉价宣传页感。
- Don't: 使用 3D 透视平台、霓虹光、强渐变、玻璃拟态、强阴影或科技广告式悬浮层。
- Don't: 使用卡通插画、emoji、伪文字、假 logo、页码或水印。
