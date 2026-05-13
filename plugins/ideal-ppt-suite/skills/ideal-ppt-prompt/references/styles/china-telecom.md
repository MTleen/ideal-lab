---
version: alpha
name: 中国电信风格
description: 面向央企汇报、政企解决方案与技术路演的稳重科技风格，以电信红与科技蓝构建红蓝双色体系。
colors:
  primary: "#C41E24"
  secondary: "#005BAC"
  tertiary: "#2D3748"
  neutral: "#6B7280"
  surface: "#F8FAFC"
  on-surface: "#1F2937"
  error: "#DC2626"
  success: "#059669"
  warning: "#D97706"
typography:
  display:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "40px"
    fontWeight: "700"
    lineHeight: "1.2"
  h1:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "32px"
    fontWeight: "700"
    lineHeight: "1.25"
  h2:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "24px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.5"
  label:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "11px"
    fontWeight: "500"
    lineHeight: "1.4"
  data-value:
    fontFamily: "Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "22px"
    fontWeight: "700"
    lineHeight: "1.2"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  gutter: "16px"
  margin: "24px"
rounded:
  sm: "2px"
  md: "4px"
  lg: "8px"
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
    dataColors:
      - "{colors.primary}"
      - "{colors.secondary}"
      - "{colors.tertiary}"
      - "{colors.success}"
      - "{colors.warning}"
      - "{colors.error}"
dimensions:
  texture: clean
  mood: professional
  typography-style: geometric
  density: dense
  quality: soft-shadow
  spacing-level: standard
---

# 中国电信风格

## Overview

中国电信风格面向央企汇报、政企解决方案、技术路演等正式商务场景。整体基调稳重权威、理性克制，通过电信红与科技蓝的双色体系传递"红色基因 + 科技蓝"的品牌认知。受众为政府领导、企业决策者与行业技术专家，因此设计必须在高密度信息下保持清晰秩序，以几何化的视觉语言体现央企的专业性、可信感与技术领先性。情感基调为冷静、自信、精密，拒绝轻浮与过度装饰。

## Colors

色板围绕"红动蓝静"的对比节奏构建，通过冷暖对冲实现视觉锚定与信息分区。

- **电信红（#C41E24）——主色**：承担视觉锚点与品牌识别功能。用于核心结论、关键数据高亮、主标题强调、重要按钮与行动号召元素。在页面中占比控制在 10%-15%，以点睛方式出现。
- **科技蓝（#005BAC）——辅色**：用于技术模块分区、图表数据系列、信息架构的冷色平衡。在复杂图表中作为第二数据系列色，或与主色共同构成双色对比。在页面中占比约 10%。
- **深灰蓝（#2D3748）——三级色**：用于辅助文字、次要标签、深色区块背景与第三级信息层级。在复杂布局中建立沉稳的第三极，避免红蓝对冲造成的视觉疲劳。
- **中性灰（#6B7280）**：负责分割线、边框、禁用状态、图表网格线与次要说明文字。作为调和色降低整体饱和度，维持专业克制感。
- **浅灰白（#F8FAFC）——表面色**：提供干净、不带冷暖倾向的画布，用于卡片背景、表格交替行与页面底层。比纯白更柔和，减少长时间观看的刺眼感。
- **深墨色（#1F2937）——表面文字色**：用于正文阅读与标题，保证高对比度下的可读性。
- **语义色**：成功绿（#059669）用于正向指标与完成状态；警告橙（#D97706）用于风险提示与待处理事项；错误红（#DC2626）用于异常状态，与主色区分使用。

## Typography

字体策略采用几何无衬线体系（Noto Sans SC / 思源黑体 / PingFang SC），以冷峻理性的字形匹配科技央企气质。笔画末端干净、字腔开放，确保在密集排版与小字号下的高可读性。

- **Display（40px / Bold / line-height 1.2）**：页面主标题，用于封面、章节过渡页。在极少数场景下可使用电信红作为强调色，通常保持深墨色。
- **H1（32px / Bold / line-height 1.25）**：幻灯片内页主标题，建立最清晰的信息层级。
- **H2（24px / SemiBold / line-height 1.3）**：模块标题或卡片标题，划分信息区块。
- **Body（14px / Regular / line-height 1.5）**：正文与描述性文字，是密集信息页面的主要字号。
- **Label（11px / Medium / line-height 1.4）**：辅助标签、图注、数据来源、时间戳等元信息，通常配合中性灰使用。
- **Data-value（22px / Bold / line-height 1.2）**：关键业绩指标（KPI）、技术参数、核心统计数据。常与电信红或科技蓝搭配，形成视觉焦点。

行高采用紧凑比例（1.2-1.5），优先在有限版面容纳更多信息。中西文混排时，英文与数字使用同等字重的无衬线西文字体（如 Inter、Roboto），保持视觉统一。

## Layout

采用 12 列网格系统，gutter 16px，页面边距 24px。高密度场景下允许信息模块紧密排列，但所有间距必须严格遵循 4px 倍数系统（4px / 8px / 16px / 24px / 32px），通过数学一致性避免视觉混乱。

- **页面结构**：每页典型承载 3-5 个信息模块。标题区（H1 + 副标题）占据顶部 15%-20% 高度，内容区按网格等分或 1:2 / 2:1 比例排布。
- **Z 型动线**：高密度页面中，信息按左上（核心结论）→ 右上（关键数据）→ 左下（支撑论据）→ 右下（补充说明）的 Z 型动线组织，符合中文阅读与汇报场景的认知习惯。
- **分隔策略**：模块间优先使用 1px #E5E7EB 实线边框或 16px 间距进行分隔。卡片容器化是处理复杂信息的核心手段——将同类信息封装在统一卡片内，外部通过 gutter 与 margin 保持呼吸感。

## Elevation & Depth

使用 subtle 的 soft-shadow 系统建立层次，拒绝 heavy drop shadow、玻璃拟态（glassmorphism）与新拟态（neumorphism），保持央企业务的严肃感与实体感。

- **默认层级**：卡片与浮动模块使用 `0 2px 8px rgba(0, 0, 0, 0.08)` 的轻量投影，在纯白或浅灰白背景上形成几乎不可见但可感知的抬升。
- **强调层级**：hover 状态、下拉面板或临时浮层提升至 `0 4px 16px rgba(0, 0, 0, 0.12)`。
- **层级逻辑**：信息深度主要通过颜色对比（红/蓝/灰的明度与饱和度差异）、边框分隔与背景色差异（纯白 vs. 浅灰白）实现。阴影仅作为辅助的深度暗示，绝不成为主导视觉元素。

## Shapes

以几何直边与精确小圆角为特征，强调理性、秩序与现代工业感。

- **卡片与容器**：采用 4px 圆角（rounded.md），在保持现代 UI 感的同时不过分活泼。
- **标签与徽章**：使用 2px 圆角（rounded.sm），接近直角但略带柔和。
- **按钮与交互元素**：统一使用 4px 圆角，与卡片保持一致。
- **图表几何**：柱状图与条形图采用 2px 圆角；折线图使用 2px 线宽配合实心圆点（4-6px）标记；饼图/环形图扇区间使用 2px 白色间隙分隔。
- **禁止项**：拒绝大圆角（>8px）、有机曲线、手绘元素、卡通插画或任何不规则 blob 形状，这些与 geometric 风格及央企气质严重冲突。

## Components

### Cards

卡片是信息容器化的核心组件。背景色为浅灰白（#F8FAFC），边框为 1px #E5E7EB，圆角 4px，内边距 16px。为强化中国电信品牌识别，卡片标题区左侧可添加 3px 宽、24px 高的电信红竖条作为视觉标识。hover 状态下，边框色过渡至中性灰（#6B7280），或叠加轻量投影（0 2px 8px rgba(0,0,0,0.08)）。卡片内信息按 "Label + Data-value + Body" 三层结构垂直排列，间距 8px。

### Tables

表格用于结构化数据展示。表头背景使用电信红（#C41E24），文字为纯白（#FFFFFF），字体 14px Medium，行高 44px。数据行背景交替使用纯白（#FFFFFF）与浅灰白（#F8FAFC），文字深墨色（#1F2937），行高 40px。单元格边框为 1px #E5E7EB，关键数据单元格可使用科技蓝（#005BAC）文字标注。表格整体无外边框，通过横向分割线实现轻盈感。密集场景下允许 12px 字号，但需保证行高不低于 36px。

### Charts

图表风格遵循 "去装饰、重数据" 原则。网格线使用 #E5E7EB（1px 实线或虚线），坐标轴文字为 11px 中性灰。数据系列按以下顺序分配颜色：
1. 电信红（#C41E24）——主指标
2. 科技蓝（#005BAC）——对比指标
3. 深灰蓝（#2D3748）——第三指标
4. 成功绿（#059669）
5. 警告橙（#D97706）
6. 错误红（#DC2626）

折线图线宽 2px，数据点直径 6px；柱状图柱间距为柱宽的 30%，圆角 2px；饼图/环形图扇区间距 2px（白色间隙）；面积图填充透明度 15%。图例置于图表上方或右侧，Label 字号 11px。

### Icons

采用线性图标风格，stroke 宽度 1.5px，端点（stroke-linecap）与连接点（stroke-linejoin）为圆角（round），保持与字体一致的几何感与精密感。图标尺寸规格：16px（标签内）、20px（按钮/列表）、24px（空状态/装饰）。图标颜色跟随语义上下文：主操作与核心结论使用电信红，技术模块与数据可视化使用科技蓝，辅助信息与禁用状态使用中性灰。禁止使用面性图标、多色图标或插画风格图标。

## Do's and Don'ts

- Do: 保持红蓝双色体系的平衡——红色用于强调与结论，蓝色用于技术与分区，两者面积占比接近 1:1
- Do: 在高密度布局中使用严格的 4px 倍数间距网格，确保信息密集但不混乱
- Do: 关键数据使用 Data-value（22px Bold）与电信红组合，形成一页之内最强的视觉焦点
- Do: 复杂信息通过卡片容器化、边框分隔与背景色差异（纯白 vs. 浅灰白）保持可读性
- Do: 汇报场景下优先使用横向对比（柱状图、条形图）与趋势折线，符合政企决策者的阅读预期
- Don't: 以蓝色作为主色或大面积背景色——蓝色是中国电信的辅色，红色才是品牌主色
- Don't: 使用高饱和度渐变、霓虹色、暖色渐变（如紫红渐变、橙红渐变），破坏央企稳重与克制感
- Don't: 使用大圆角（>8px）、手绘元素、卡通插画、emoji 或不规则有机形状，与 geometric 风格及央企身份冲突
- Don't: 在单页中让红、蓝、橙三种高饱和度颜色同时大面积出现，避免视觉嘈杂
- Don't: 阴影过重或滥用投影，禁止玻璃拟态、新拟态等过度质感效果
