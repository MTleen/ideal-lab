---
version: alpha
name: 水彩风格
description: 温和的水彩美学，可见笔触与自然色彩晕染，手绘质感与温暖亲切的艺术精致感。适用于生活方式、健康养生、旅行指南和创意工作坊。
colors:
  primary: "#F4A261"
  secondary: "#E8A0A0"
  tertiary: "#87A96B"
  neutral: "#E5E0D5"
  surface: "#FAF8F0"
  on-surface: "#3D3D3D"
  error: "#C0392B"
  success: "#87A96B"
  warning: "#F4A261"
typography:
  display:
    fontFamily: "优雅手写体 / 毛笔手写体"
    fontSize: "48pt"
    fontWeight: 600
    lineHeight: 1.1
  h1:
    fontFamily: "优雅手写体 / 毛笔手写体"
    fontSize: "36pt"
    fontWeight: 600
    lineHeight: 1.15
  h2:
    fontFamily: "优雅手写体 / 毛笔手写体"
    fontSize: "24pt"
    fontWeight: 500
    lineHeight: 1.2
  body:
    fontFamily: "干净圆角无衬线体 / 随意手写风格"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "干净圆角无衬线体 / 随意手写风格"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "优雅手写体 / 毛笔手写体"
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
  gutter: 24
  margin: "12%"
rounded:
  sm: 8
  md: 16
  lg: 24
  full: 9999px
components:
  card:
    backgroundColor: "#FFF9E6"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "#FFF9E6"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: organic
  mood: warm
  typography-style: humanist
  density: minimal
  quality: flat
  spacing-level: editorial
---

# 水彩风格

## Overview

水彩风格以温和的水彩美学为核心，可见笔触与自然色彩晕染。手绘质感，边缘柔和，形状有机。温暖、亲切、艺术精致。将艺术表达与清晰的信息传递相结合。品牌个性艺术、自然、温暖，目标受众为生活方式爱好者、创意从业者和 wellness 受众，情感基调宁静、优雅、温馨。

## Colors

色板围绕温暖的纸张质感与自然水彩色调构建：
- **暖调米白 (#FAF8F0)**：主背景，模拟水彩纸的温和色调。
- **柔和奶油色 (#FFF9E6)**：备选背景，更温暖的奶油色调。
- **暖炭灰 (#3D3D3D)**：标题与正文，温暖的深灰色替代纯黑。
- **柔珊瑚色 (#F4A261)**：主温暖感，自然的水彩橙色调。
- **灰玫瑰色 (#E8A0A0)**：次温暖感，柔和的水彩粉红色。
- **鼠尾草绿 (#87A96B)**：自然、成长，温和的绿色水彩。
- **天蓝色 (#7EC8E3)**：水、宁静，清新的蓝色水彩。
- **柔薰衣草色 (#C5B4E3)**：强调、创意，梦幻的紫色调。
- **淡黄 (#FFF3C4)**：背景晕染，温暖的水彩底色。

## Typography

字体策略追求艺术感与功能性的融合：
- **标题**：优雅手写体或毛笔手写体用于标题。有机字形，自然变化。温暖、个性化的感觉。可呈现为实际手绘字体艺术效果。
- **正文**：干净的圆角无衬线体或随意手写风格。小字号下依然可读。在保持艺术整体性的同时兼具功能性。
- **标签/数据**：手写体或圆角无衬线体，保持水彩风格的艺术温度。

## Layout

幻灯片布局策略追求极简与优雅的平衡：
- 大面积留白，让水彩元素充分呼吸。
- 内容居中或偏侧放置，形成艺术画廊般的构图。
- 宽裕的边距（12%）和编辑级间距，营造高端艺术感。

## Elevation & Depth

视觉层次通过水彩晕染和色彩层次传达：
- 水彩晕染作为区域背景，创造自然的色彩深度。
- 所有元素的色彩晕染与柔和边缘，避免硬边。
- 不使用阴影系统，完全依赖水彩的透明度和色彩叠加建立层次。

## Shapes

形状语言柔和、有机、艺术化：
- 大圆角（8-24px），极度柔和，不使用锐利边缘。
- 水彩晕染的形状边界，颜色可超出锐利边缘。
- 自然元素：叶子、气泡、花朵等有机形状。

## Components

### Cards
卡片使用柔和奶油色背景（#FFF9E6），搭配暖灰边框，大圆角（24px）。内容使用暖炭灰书写，点缀柔珊瑚色或灰玫瑰色。背景可带有水彩晕染效果。

### Tables
表格使用柔珊瑚色表头搭配暖炭灰字，交替行使用柔和奶油色。线条柔和，边界可带有水彩晕染效果。

### Charts
图表采用手绘水彩风格的数据可视化，网格线使用暖灰色，数据系列使用柔珊瑚色、灰玫瑰色、鼠尾草绿等自然水彩色。不使用3D效果或硬边。

### Icons
图标风格为带可见笔触的插画图标。自然元素如叶子、气泡、花朵。小型表情丰富的人物插画。所有图标带有水彩填充的柔和边缘。

## Do's and Don'ts

- Do: 允许色彩晕染超出锐利边缘
- Do: 使用可见的笔触纹理
- Do: 创建柔和、有机的形状
- Do: 所有元素包含手绘质感
- Do: 保持温暖、诱人的配色
- Don't: 使用尖锐的几何图形
- Don't: 创建硬边或数字精确感
- Don't: 使用冷调或刺目色彩
- Don't: 添加摄影元素
- Don't: 添加页码、页脚或徽标
