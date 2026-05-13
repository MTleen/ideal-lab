---
version: alpha
name: 编辑信息图风格
description: 现代杂志风格编辑信息图，清晰的视觉叙事将复杂信息转化为易消化的叙事。适用于科技解释、科学传播、研究摘要和政策简报。
colors:
  primary: "#2563EB"
  secondary: "#F97316"
  tertiary: "#10B981"
  neutral: "#D1D5DB"
  surface: "#FFFFFF"
  on-surface: "#1A1A1A"
  error: "#EF4444"
  success: "#10B981"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "Playfair Display / Source Serif Pro"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 1.1
  h1:
    fontFamily: "Playfair Display / Source Serif Pro"
    fontSize: "36pt"
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: "Playfair Display / Source Serif Pro"
    fontSize: "24pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "Source Sans Pro / Open Sans"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Source Sans Pro / Open Sans"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Playfair Display / Source Serif Pro"
    fontSize: "20pt"
    fontWeight: 700
    lineHeight: 1.2
spacing:
  base: 4
  xs: 2
  sm: 4
  md: 8
  lg: 16
  xl: 32
  gutter: 16
  margin: "5%"
rounded:
  sm: 2
  md: 4
  lg: 8
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "#FFFFFF"
    rowAltBackgroundColor: "#F8F9FA"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: cool
  typography-style: editorial
  density: dense
  quality: soft-shadow
  spacing-level: compact
---

# 编辑信息图风格

## Overview

编辑信息图风格追求高端杂志解释类美学，清晰的视觉叙事将复杂信息转化为易消化的叙事。干净的插画、结构化的布局、专业的排版，参考 Wired、The Verge 或高端科学出版物的品质。品牌个性专业、清晰、权威，目标受众为科技从业者、研究人员和知识工作者，情感基调理性、可信、精致。

## Colors

色板以干净的白色为基底，搭配编辑级强调色：
- **纯白 (#FFFFFF)**：主背景，营造杂志印刷感。
- **浅灰 (#F8F9FA)**：分区背景，提供微妙的层次区分。
- **近黑色 (#1A1A1A)**：标题与正文，高对比度确保可读性。
- **深灰 (#4A5568)**：说明文字、元数据、辅助信息。
- **编辑蓝 (#2563EB)**：主强调色，专业、可信的蓝色调。
- **珊瑚橙 (#F97316)**：次强调色，为信息增添活力。
- **祖母绿 (#10B981)**：正面元素、成功状态。
- **琥珀色 (#F59E0B)**：警告与注意。
- **中灰 (#D1D5DB)**：分隔线与分区边界。

## Typography

字体策略追求编辑级的精致与清晰层级：
- **标题**：粗体展示衬线体或现代无衬线体，强烈的视觉存在感。干净的字母形态，带有编辑级的精致感。大字号以产生冲击力。
- **小标题**：半粗无衬线体用于章节标题，与正文有清晰的层级区分。整篇风格一致。
- **正文**：针对阅读优化的人文主义无衬线体，干净、专业、易读。舒适的行高 (1.6)。
- **标签/数据**：衬线体或现代无衬线体，保持编辑风格一致性。

## Layout

幻灯片布局策略追求信息密度与叙事清晰度的平衡：
- 结构化的多分区布局，每个区域承载特定的信息单元。
- 关键洞察的标注框突出核心结论。
- 紧凑的间距系统最大化信息密度，同时保持可读性。
- 宽裕的边距（5%）在有限空间内创造杂志级呼吸感。

## Elevation & Depth

视觉层次通过柔和的阴影和分层传达：
- 卡片与标注框使用柔和的弥散阴影，创造微妙的层级感。
- 分区背景色（浅灰与纯白交替）提供扁平化的深度区分。
- 不使用强烈的3D效果或渐变，保持编辑排版的干净感。

## Shapes

形状语言干净、精确、现代：
- 小圆角（2-8px）保持现代感，不过于柔和。
- 几何形状为主，线条清晰锐利。
- 流程图和方向层级使用简洁的箭头与连接线。

## Components

### Cards
卡片使用纯白背景，搭配中灰边框，小圆角（4px）。内部包含关键洞察或数据亮点，使用编辑蓝或珊瑚橙作为点缀。阴影柔和弥散。

### Tables
表格使用编辑蓝表头搭配白字，交替行使用浅灰色。线条清晰，不使用强烈边框，保持杂志排版感。

### Charts
图表采用扁平化数据可视化风格，网格线使用中灰色，数据系列使用编辑蓝、珊瑚橙、祖母绿等编辑级色彩。不使用3D效果或渐变。

### Icons
图标风格为干净的扁平插画风格（非照片），基于图标的数据可视化。抽象概念的视觉隐喻，线条简洁、几何感强。

## Do's and Don'ts

- Do: 创建清晰的视觉叙事流
- Do: 使用结构化的多分区布局
- Do: 为关键洞察包含标注框
- Do: 为复杂概念设计视觉隐喻
- Do: 保持杂志级的高品质打磨
- Don't: 使用摄影图像
- Don't: 创建杂乱密集的布局
- Don't: 混用过多视觉风格
- Don't: 添加无目的的装饰元素
- Don't: 添加幻灯片编号、页脚或标志
