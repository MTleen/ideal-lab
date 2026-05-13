---
version: alpha
name: 极简风格
description: 超干净的主旨演讲风格，最大化留白与禅意般的简洁。适用于高管简报、主旨演讲、高端品牌沟通、投资人会议和高层战略。
colors:
  primary: "#2563EB"
  secondary: "#6B7280"
  tertiary: "#E5E7EB"
  neutral: "#F3F4F6"
  surface: "#FFFFFF"
  on-surface: "#1A1A1A"
  error: "#EF4444"
  success: "#10B981"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "56pt"
    fontWeight: 300
    lineHeight: 1.1
  h1:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "42pt"
    fontWeight: 300
    lineHeight: 1.15
  h2:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "28pt"
    fontWeight: 400
    lineHeight: 1.2
  body:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "16pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "12pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "SF Pro Display / Inter / Helvetica Neue"
    fontSize: "24pt"
    fontWeight: 300
    lineHeight: 1.2
spacing:
  base: 8
  xs: 8
  sm: 16
  md: 24
  lg: 40
  xl: 64
  gutter: 40
  margin: "15%"
rounded:
  sm: 0
  md: 0
  lg: 0
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.tertiary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.on-surface}"
    headerTextColor: "{colors.surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "{colors.tertiary}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: neutral
  typography-style: geometric
  density: minimal
  quality: flat
  spacing-level: editorial
---

# 极简风格

## Overview

最大化留白与最少元素。禅意般的简洁，每个元素都有其存在的理由。高端、精致的美学，适合高管受众。少即是多——不断删减，直到无法再减任何东西。品牌个性克制、精致、权威，目标受众为高管、董事会成员和战略决策者，情感基调平静、专注、高级。

## Colors

色板极致克制，以纯白为基底，单一强调色节制使用：
- **纯白 (#FFFFFF)**：主背景，绝对干净，无颗粒或图案。
- **近黑色 (#1A1A1A)**：标题与正文，提供高对比度阅读体验。
- **中灰 (#6B7280)**：说明文字、元数据，次要信息层级。
- **单一品牌色 (#2563EB)**：仅一种强调色，节制使用，仅在必要时出现。
- **浅灰 (#E5E7EB)**：微妙的分隔线，发丝般纤细的分隔。
- **极浅灰 (#F3F4F6)**：交替行或极简背景分区。

## Typography

字体策略采用干净几何无衬线，轻字重体现优雅克制：
- **标题**：SF Pro Display、Inter 或 Helvetica Neue 等干净几何无衬线字体。轻到中等字重，体现优雅的克制。宽裕的字间距，大字号以产生冲击力，但不使用粗体。
- **正文**：与标题同一家族，更轻的字重。字号对比最小，整体感觉干净、通透。
- **标签/数据**：同一家族中等字重，小字号下保持清晰度。

## Layout

幻灯片布局策略以留白为核心设计元素：
- 宽裕的边距（各边至少 15%），最大化呼吸空间。
- 居中或左对齐布局，避免复杂的多栏结构。
- 每页文字极简（10 词或以内），元素之间创造充足的呼吸空间。
- 使用比例建立层级，而非颜色或装饰。
- 仅在必要时使用简单几何形状。

## Elevation & Depth

视觉层次完全通过扁平化的留白和比例传达：
- 不使用阴影系统，绝对扁平设计。
- 层次通过字号比例、间距节奏和色块对比建立。
- 细发丝规则线提供微妙的分隔，不增加视觉重量。
- 单色系或灰度数据可视化，避免多色干扰。

## Shapes

形状语言体现极致的几何克制：
- 直角为主，不使用圆角（rounded: 0）。
- 仅在必要时使用简单几何形状。
- 细线条和矩形构成全部视觉元素。
- 禁止使用任何装饰性形状或有机形态。

## Components

### Cards
卡片极少使用，出现时采用纯白背景，搭配极浅灰边框或发丝分隔线，直角轮廓。内部留白极大，内容极度精简。

### Tables
表格极少使用，出现时采用近黑表头搭配白字，交替行使用极浅灰底色。线条纤细如发丝，单元格对齐严格，无圆角。

### Charts
数据可视化采用单色系或灰度，极简风格。仅在绝对必要时使用图表，且保持单色。不使用3D效果、渐变或多色数据系列。

### Icons
图标风格为极简几何图标，仅在绝对必要时使用。禁止使用任何图标或插画，除非它们对传达信息至关重要。

## Do's and Don'ts

- Do: 将空白视为设计元素
- Do: 仅使用单一强调色
- Do: 保持文字极简（每页 10 词或以内）
- Do: 元素之间创造呼吸空间
- Do: 使用比例建立层级
- Don't: 用装饰填充空白
- Don't: 使用多种强调色
- Don't: 除非必要，否则添加图标或插画
- Don't: 创建密集的信息布局
- Don't: 添加幻灯片编号、页脚或标志
