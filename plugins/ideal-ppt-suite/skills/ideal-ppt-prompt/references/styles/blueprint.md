---
version: alpha
name: 蓝图风格
description: 精确的技术蓝图风格，搭配专业的分析级视觉呈现。适用于技术架构、系统设计、数据分析、工程文档和流程图。
colors:
  primary: "#2563EB"
  secondary: "#1E3A5F"
  tertiary: "#BFDBFE"
  neutral: "#E5E5E5"
  surface: "#FAF8F5"
  on-surface: "#334155"
  error: "#DC2626"
  success: "#10B981"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "Neue Haas Grotesk Display Pro"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 1.1
  h1:
    fontFamily: "Neue Haas Grotesk Display Pro"
    fontSize: "36pt"
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: "Neue Haas Grotesk Display Pro"
    fontSize: "24pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "Tiempos Text"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Neue Haas Grotesk Display Pro"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Neue Haas Grotesk Display Pro"
    fontSize: "18pt"
    fontWeight: 600
    lineHeight: 1.2
spacing:
  base: 8
  xs: 4
  sm: 8
  md: 16
  lg: 24
  xl: 48
  gutter: 32
  margin: "10%"
rounded:
  sm: 0
  md: 0
  lg: 0
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
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: grid
  mood: cool
  typography-style: technical
  density: balanced
  quality: soft-shadow
  spacing-level: standard
---

# 蓝图风格

## Overview

蓝图风格以干净、结构化的视觉隐喻为核心，运用蓝图、图表和示意图构建精确、分析性强且美学精致的幻灯片。信息以三联画或网格布局呈现，具有工程级的精准度。品牌个性偏向技术权威与专业精确，目标受众为工程师、架构师和数据分析师，情感基调冷静、理性、可信赖。

## Colors

色板设计克制且统一，以蓝图纸色为基底：
- **蓝图纸色 (#FAF8F5)**：主背景，营造工程图纸的底纸质感。
- **浅灰 (#E5E5E5)**：背景网格线，为画面提供隐性的结构锚点。
- **深岩灰 (#334155)**：标题与正文，提供高对比度的专业文字阅读体验。
- **工程蓝 (#2563EB)**：主强调色，用于关键元素、高亮和核心数据。
- **海军蓝 (#1E3A5F)**：辅助元素，提供深色的结构支撑。
- **浅蓝 (#BFDBFE)**：背景填充色，用于次级区域或图表填充。
- **琥珀色 (#F59E0B)**：警告与强调点，在需要引起注意时使用。
- **成功绿 (#10B981)**：正面指标与成功状态。
- **错误红 (#DC2626)**：错误状态与风险指示。

## Typography

字体策略采用无衬线与衬线的经典组合，兼顾技术感与编辑级品质：
- **标题**：Neue Haas Grotesk Display Pro 或类似干净无衬线字体，粗体，字形精确，字间距一致，具有技术性、权威感。
- **正文**：Tiempos Text 或类似优雅衬线字体，干净，小字号下可读性强，专业的编辑级品质。
- **标签/数据**：Neue Haas Grotesk Display Pro 中号字重，保证小字号下的清晰度。

## Layout

幻灯片布局策略遵循严格的工程网格系统：
- 内容以三联画或网格布局呈现，具有工程级的精准度。
- 所有元素使用网格对齐，连接线仅使用直线或90度折线。
- 通过比例建立清晰的视觉层级，留白克制但有序。
- 适度边距（10%），内容结构化排列。

## Elevation & Depth

视觉层次通过极轻微的阴影和几何精度传达：
- 极轻微的阴影增加深度感，保持蓝图的技术感与扁平美学平衡。
- 完全依赖线宽、比例和色块构建层次。
- 技术绘图风格的细线作业和尺寸线作为视觉引导工具。
- 剖面式示意图和等轴测/正交投影提供空间深度感。

## Shapes

形状语言体现工程精确：
- 所有形状使用几何精度，线条精确，描边粗细一致。
- 直角为主，不使用圆角（rounded: 0）。
- 技术示意图和干净的矢量图形构成主要视觉元素。

## Components

### Cards
卡片使用蓝图纸色背景，搭配浅灰边框，直角轮廓，内部对齐严格遵循网格。内容区域使用工程蓝作为顶部标题栏或左侧强调条。

### Tables
表格使用工程蓝表头搭配白字，交替行使用浅灰底色。线条精确，单元格对齐严格，无圆角。

### Charts
图表采用干净、极简的数据可视化风格，网格线使用浅灰，数据系列依次使用工程蓝、海军蓝、浅蓝、琥珀色。不使用3D效果或渐变。

### Icons
图标风格为描边风格的技术示意图，线条粗细一致，仅使用直线或90度折线连接。禁止使用手绘或有机形状。

## Do's and Don'ts

- Do: 始终维持一致的线宽
- Do: 所有元素使用网格对齐
- Do: 保持配色克制且统一
- Do: 通过比例建立清晰的视觉层级
- Do: 所有形状使用几何精度
- Don't: 使用手绘或有机形状
- Don't: 添加装饰性花饰
- Don't: 使用曲线连接线
- Don't: 包含摄影元素
- Don't: 添加幻灯片编号、页脚或标志
