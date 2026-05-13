---
version: alpha
name: 暗色氛围风格
description: 深色情绪化美学，深邃色彩与发光强调元素，电影感暗色模式美学。适用于娱乐演示、音乐与音频内容、创意机构提案、晚间活动和高端品牌发布。
colors:
  primary: "#8B5CF6"
  secondary: "#06B6D4"
  tertiary: "#EC4899"
  neutral: "#2D3748"
  surface: "#0D0D1A"
  on-surface: "#FFFFFF"
  error: "#EF4444"
  success: "#22C55E"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "优雅衬线体 / 精致无衬线体"
    fontSize: "48pt"
    fontWeight: 600
    lineHeight: 1.1
  h1:
    fontFamily: "优雅衬线体 / 精致无衬线体"
    fontSize: "36pt"
    fontWeight: 600
    lineHeight: 1.15
  h2:
    fontFamily: "优雅衬线体 / 精致无衬线体"
    fontSize: "24pt"
    fontWeight: 500
    lineHeight: 1.2
  body:
    fontFamily: "干净无衬线体"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "干净无衬线体"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "优雅衬线体 / 精致无衬线体"
    fontSize: "20pt"
    fontWeight: 600
    lineHeight: 1.2
spacing:
  base: 8
  xs: 4
  sm: 8
  md: 16
  lg: 32
  xl: 64
  gutter: 32
  margin: "8%"
rounded:
  sm: 4
  md: 8
  lg: 16
  full: 9999px
components:
  card:
    backgroundColor: "#1A1A2E"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: dark
  typography-style: editorial
  density: balanced
  quality: layered-depth
  spacing-level: standard
---

# 暗色氛围风格

## Overview

暗色氛围风格以电影感暗色模式美学为核心，带有氛围深度。深紫、黑色和浓郁的阴影，搭配发光点缀创造戏剧化视觉对比。神秘、精致且视觉震撼。非常适合晚间活动、创意行业和高端品牌推广。品牌个性神秘、精致、戏剧化，目标受众为创意从业者、娱乐行业和高端品牌受众，情感基调沉浸、神秘、震撼。

## Colors

色板以深邃暗色为基底，搭配发光强调：
- **深紫黑 (#0D0D1A)**：主背景，营造深邃的暗色氛围。
- **浓郁海军蓝 (#1A1A2E)**：次级区域，提供深色层次。
- **纯白 (#FFFFFF)**：标题，与深色背景形成高对比。
- **浅灰 (#A0AEC0)**：正文，在深色背景上可读性强。
- **电光紫 (#8B5CF6)**：主发光色，霓虹风格高亮。
- **青蓝 (#06B6D4)**：次发光色，冷色调能量。
- **洋红粉 (#EC4899)**：第三强调色，暖色调点缀。
- **琥珀色 (#F59E0B)**：暖色高亮。
- **深灰 (#2D3748)**：分隔线、边框。

## Typography

字体策略追求高对比度与精致感：
- **标题**：优雅的衬线体或精致的无衬线体，浅色/白色。与深色背景形成高对比。中等至粗字重。字形可带有微妙的发光效果。
- **正文**：干净的无衬线体，浅灰或柔和白色。在深色背景上可读性强。常规字重，宽裕的行高。
- **标签/数据**：优雅衬线体或精致无衬线体，与标题风格一致。

## Layout

幻灯片布局策略追求戏剧化的视觉焦点：
- 深色背景最大化发光效果的视觉冲击。
- 关键元素居中或偏侧放置，形成戏剧化的视觉焦点。
- 宽裕的边距（8%）让深色背景充分呼吸。

## Elevation & Depth

视觉层次通过发光效果和渐变传达：
- 发光的强调元素和边框，节制地使用发光效果进行强调。
- 微妙的渐变背景，从边缘到中心创造氛围深度。
- 氛围雾气或粒子效果增添沉浸感。
- 带背光边缘的剪影创造戏剧化的轮廓。

## Shapes

形状语言神秘、有机、柔和：
- 圆角使用中大尺寸（4-16px），保持柔和感。
- 放射状光圈和光球等有机形状。
- 音频波形或声音可视化等动态形状。

## Components

### Cards
卡片使用浓郁海军蓝背景（#1A1A2E），搭配深灰边框，较大圆角（16px）。内部内容使用发光强调色点缀。

### Tables
表格使用电光紫表头搭配白字，交替行使用深灰色。在深色背景上保持可读性，不使用强烈的边框。

### Charts
图表采用暗色模式，网格线使用深灰色，数据系列使用电光紫、青蓝、洋红粉等发光色。不使用3D效果。

### Icons
图标风格为发光描边风格，带有霓虹效果。可使用音频波形、声音可视化等动态元素。

## Do's and Don'ts

- Do: 保持高对比度以确保可读性
- Do: 节制地使用发光效果进行强调
- Do: 用渐变创造氛围深度
- Do: 设计戏剧化的视觉焦点
- Do: 保持文字在深色背景上清晰锐利
- Don't: 过度使用霓虹效果（少即是多）
- Don't: 创建低对比度的文字组合
- Don't: 使用明亮的背景
- Don't: 添加杂乱繁忙的元素
- Don't: 添加幻灯片编号、页脚或标志
