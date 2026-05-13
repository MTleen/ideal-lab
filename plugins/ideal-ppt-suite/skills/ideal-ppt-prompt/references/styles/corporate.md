---
version: alpha
name: 商务风格
description: 专业商务风格，海军蓝/金色配色，结构化布局，传达能力、可靠性和机构公信力。适用于商务演示、投资人路演、季度报告、执行摘要和客户提案。
colors:
  primary: "#C9A227"
  secondary: "#3D5A80"
  tertiary: "#F3F4F6"
  neutral: "#E5E7EB"
  surface: "#FFFFFF"
  on-surface: "#1E3A5F"
  error: "#DC2626"
  success: "#059669"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "Inter / SF Pro"
    fontSize: "44pt"
    fontWeight: 600
    lineHeight: 1.1
  h1:
    fontFamily: "Inter / SF Pro"
    fontSize: "32pt"
    fontWeight: 600
    lineHeight: 1.15
  h2:
    fontFamily: "Inter / SF Pro"
    fontSize: "22pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "Source Sans Pro"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter / SF Pro"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Inter / SF Pro"
    fontSize: "20pt"
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
  sm: 4
  md: 8
  lg: 12
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.on-surface}"
    headerTextColor: "{colors.surface}"
    rowAltBackgroundColor: "{colors.tertiary}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: professional
  typography-style: geometric
  density: balanced
  quality: soft-shadow
  spacing-level: standard
---

# 商务风格

## Overview

商务风格以干净的线条、结构化的布局和得体的商务精致感为核心。传达能力、可靠性和机构公信力。通过谨慎运用留白和精致的色彩选择，在 professionalism 与亲和力之间取得平衡。品牌个性专业、可信、稳重，目标受众为高管、投资人和企业客户，情感基调自信、权威、可信赖。

## Colors

色板以纯白为基底，海军蓝和金色构建专业感：
- **纯白 (#FFFFFF)**：幻灯片主背景，最大化专业感。
- **海军蓝 (#1E3A5F)**：标题、关键文字，传达权威与稳重。
- **深灰 (#4A5568)**：正文，提供舒适的阅读体验。
- **金色 (#C9A227)**：高端高亮、强调，策略性地用于关键数据。
- **浅海军蓝 (#3D5A80)**：辅助元素，提供深色的结构支撑。
- **商务绿 (#059669)**：正面指标。
- **商务红 (#DC2626)**：注意项。
- **浅灰 (#F3F4F6)**：背景分区，微妙的区域划分。

## Typography

字体策略采用现代几何无衬线与人文主义无衬线的组合：
- **标题**：现代几何无衬线字体（Inter、SF Pro 或类似字体）。干净、专业且高度易读。传达能力和当代商务感知。中等至半粗字重。
- **正文**：人文主义无衬线字体（Source Sans Pro 风格）。友好而专业，针对阅读理解进行了优化。常规字重，舒适的行高。
- **标签/数据**：Inter / SF Pro 中等字重，保证小字号下的清晰度。

## Layout

幻灯片布局策略遵循结构化网格系统：
- 结构化网格布局，所有元素对齐一致。
- 留白策略性运用，在 professionalism 与亲和力之间取得平衡。
- 进度条、指标展示和时间线图形等结构化元素有序排列。

## Elevation & Depth

视觉层次通过细微的阴影增加深度：
- 极细微的阴影增加深度感，保持极简。
- 卡片和容器使用 subtle 的 box-shadow，不喧宾夺主。
- 层级通过色块和间距建立，而非强烈的立体效果。

## Shapes

形状语言干净、专业、克制：
- 圆角使用中小尺寸（4-12px），保持专业感。
- 结构化网格中的矩形和线条为主。
- 不使用圆润的 blob 形状或有机形态。

## Components

### Cards
卡片使用白色背景，搭配浅灰边框，中小圆角（8px）。内部内容对齐严格遵循网格，金色用于关键数据高亮。

### Tables
表格使用海军蓝表头搭配白字，交替行使用浅灰底色。线条精确，单元格对齐严格，圆角克制。

### Charts
图表采用干净的数据可视化风格，网格线使用浅灰，数据系列使用金色、浅海军蓝、浅灰。不使用3D效果或渐变。

### Icons
图标风格为专业描边风格，线条粗细一致，几何简洁。禁止使用俏皮或随意的元素。

## Do's and Don'ts

- Do: 保持清晰的视觉层级
- Do: 使用一致的网格对齐
- Do: 策略性地应用强调色（金色用于强调）
- Do: 保持数据可视化干净易读
- Do: 使用专业的描边图标
- Don't: 使用俏皮或随意的元素
- Don't: 应用沉重的装饰效果
- Don't: 混用过多强调色
- Don't: 幻灯片信息过于拥挤
- Don't: 使用非正式的插画风格
- Don't: 添加幻灯片编号、页脚或标志
