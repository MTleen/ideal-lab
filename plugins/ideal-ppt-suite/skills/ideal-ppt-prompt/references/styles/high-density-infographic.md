---
version: alpha
name: 高密度信息图
description: 适用于生成信息密度高、技术演示或企业产品介绍的幻灯片。咨询公司风格，搭配有意义的信息图表。
colors:
  primary: "#2563EB"
  secondary: "#1E3A5F"
  tertiary: "#F0F4F8"
  neutral: "#E2E8F0"
  surface: "#FFFFFF"
  on-surface: "#1E3A5F"
  error: "#EF4444"
  success: "#10B981"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "32pt"
    fontWeight: 700
    lineHeight: 1.2
  h1:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "24pt"
    fontWeight: 700
    lineHeight: 1.2
  h2:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "16pt"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "12pt"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "10pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Inter / Microsoft YaHei"
    fontSize: "16pt"
    fontWeight: 600
    lineHeight: 1.2
spacing:
  base: 4
  xs: 2
  sm: 4
  md: 8
  lg: 12
  xl: 24
  gutter: 16
  margin: "8%"
rounded:
  sm: 2
  md: 4
  lg: 6
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.surface}"
    rowAltBackgroundColor: "{colors.tertiary}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: cool
  typography-style: technical
  density: dense
  quality: flat
  spacing-level: compact
---

# 高密度信息图

## Overview

专业咨询风格搭配有意义的信息图表。核心理念是内容驱动密度：信息密度来自实际文字和数据，而非视觉装饰。流程图、对比图、趋势图等辅助理解，但禁止装饰性插图。干净排版配合纯白背景，用色块和分隔线组织结构。小字体高密度，以较小字号容纳更多内容。品牌个性专业、分析性强、数据导向，目标受众为技术决策者、企业客户和咨询受众，情感基调理性、精确、高效。

## Colors

色板以纯白为基底，深藏青与工程蓝构建技术专业感：
- **纯白 (#FFFFFF)**：幻灯片主背景，无任何背景纹理或网格线。
- **浅灰蓝 (#F0F4F8)**：卡片填充与交替行底色，微妙的区域划分。
- **浅灰 (#E2E8F0)**：边框与分隔线，卡片边框和网格线。
- **深藏青 (#1E3A5F)**：标题与重要文字，传达权威与稳重。
- **工程蓝 (#2563EB)**：高亮、关键数据、章节头，主强调色。
- **灰色 (#64748B)**：副文字与元数据，次要信息层级。
- **绿色 (#10B981)**：正面/成功指标。
- **橙色 (#F59E0B)**：警告与注意事项。
- **红色 (#EF4444)**：问题/风险指示。
- **浅绿 (#E8F4E8)**：正面指示背景。
- **浅红 (#FEE8E8)**：负面指示背景。

## Typography

字体策略采用粗体无衬线为主，紧凑行距以最大化信息密度：
- **标题**：Bold Sans-Serif（SimHei / Microsoft YaHei 或 Inter），粗体，字形清晰，在小字号下保持可读性。
- **正文**：Clean Sans-Serif（Inter 或类似字体），常规字重，针对屏幕阅读优化。
- **字号层级**：偏小以容纳更多内容。幻灯片标题 28-32pt，卡片/小节标题 16-18pt，正文 12-14pt，数据标签/注释 10-12pt。
- **行距**：1.2-1.4（紧凑），在有限空间内最大化内容展示。

## Layout

幻灯片布局策略以信息密度最大化为核心：
- 16:9 宽屏比例，纯白背景，边距 8-10%，内容充实但不拥挤。
- 标题占用空间小，内容区域最大化，把空间留给实质内容。
- 每页 6-8 个要点或等量的图表+文字组合。
- 图文混排：文字块与图表在同一页共存。
- 表格优于段落：结构化信息优先用表格展示。
- 箭头优于文字：用箭头符号替代连接词。

## Elevation & Depth

视觉层次完全通过扁平化的色块、线条和间距传达：
- 不使用阴影系统，完全扁平设计。
- 依赖色块对比（浅灰蓝卡片 vs 纯白背景）建立层级。
- 彩色顶部标题栏为卡片提供清晰的视觉锚点。
- 流程图中的节点和箭头提供结构深度。

## Shapes

形状语言简洁、功能导向、几何精确：
- 小圆角（2-6px），保持技术性但不生硬。
- 流程图节点使用矩形，箭头为直线+简洁箭头样式。
- 色块卡片使用彩色顶部标题栏，下方为内容区域。
- 不使用圆润的有机形状或装饰性 blob。

## Components

### Cards
色块卡片使用纯白背景，搭配浅灰边框，小圆角（4px）。顶部使用工程蓝或深藏青标题栏（白字），下方内容区域紧凑排列。内部填充采用浅灰蓝或纯白，要点列表缩进一致。

### Tables
结构化表格使用工程蓝表头搭配白字，交替行使用浅灰蓝底色。单元格对齐严格，线条精确。表格中展示多维度信息，优于纯文字段落。

### Charts
数据图表必须有数据标签。柱状图用于对比数值，趋势线展示变化，饼图展示占比。图表风格干净极简，网格线使用浅灰，不使用3D效果或渐变。

### Icons
图标风格为功能性几何图标，线条简洁。严格禁止使用装饰性图标或 clipart（时钟、大脑、灯泡、齿轮、人物剪影等）。

## Do's and Don'ts

- Do: 使用有意义的图表辅助理解（流程图、对比图、趋势图）
- Do: 节点内必须有文字标签，箭头简洁（直线+箭头）
- Do: 空间不够时缩小字号，不要删减内容
- Do: 空间太多时增加有意义的图表或补充数据
- Do: 表格优于段落，用结构化方式展示信息
- Don't: 使用装饰性图标或 clipart
- Don't: 添加背景网格线或蓝图纹理
- Don't: 使用伪代码装饰作为填充
- Don't: 使用与内容无关的抽象插画
- Don't: 同一数据用不同形式重复呈现
- Don't: 添加幻灯片编号、页脚或标志
