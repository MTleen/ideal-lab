---
version: alpha
name: 大胆编辑风格
description: 高冲击力的杂志编辑风格，视觉表达大胆鲜明，杂志封面级别的强视觉冲击力。适用于产品发布、营销演示、主题演讲、品牌展示和投资人路演。
colors:
  primary: "#3B82F6"
  secondary: "#FB923C"
  tertiary: "#EC4899"
  neutral: "#2D2D2D"
  surface: "#0A0A0A"
  on-surface: "#FFFFFF"
  error: "#EF4444"
  success: "#22C55E"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "Impact / Oswald Bold / Bebas Neue"
    fontSize: "72pt"
    fontWeight: 700
    lineHeight: 0.95
  h1:
    fontFamily: "Impact / Oswald Bold / Bebas Neue"
    fontSize: "56pt"
    fontWeight: 700
    lineHeight: 1.0
  h2:
    fontFamily: "Impact / Oswald Bold / Bebas Neue"
    fontSize: "36pt"
    fontWeight: 600
    lineHeight: 1.1
  body:
    fontFamily: "Inter / SF Pro / Helvetica Neue"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter / SF Pro / Helvetica Neue"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Impact / Oswald Bold / Bebas Neue"
    fontSize: "24pt"
    fontWeight: 700
    lineHeight: 1.1
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
  sm: 0
  md: 0
  lg: 0
  full: 9999px
components:
  card:
    backgroundColor: "{colors.neutral}"
    borderColor: "#3D3D3D"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "#3D3D3D"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: vibrant
  typography-style: editorial
  density: balanced
  quality: layered-depth
  spacing-level: editorial
---

# 大胆编辑风格

## Overview

大胆编辑风格追求杂志封面级别的强视觉冲击力。粗体字型和戏剧化对比，全出血图像和大面积色块营造主导气场。每一页幻灯片都如同高端出版物封面。品牌个性大胆、前卫、充满能量，目标受众为营销人员、创意从业者和投资人，情感基调激情、自信、震撼。

## Colors

色板以高对比度深色背景搭配多色强调：
- **深黑色 (#0A0A0A)**：主深色背景，营造戏剧化舞台。
- **深蓝 (#0F172A)**：备选深色背景。
- **纯白 (#FFFFFF)**：浅色模式背景，深色背景上的文字。
- **纯黑 (#000000)**：浅色背景上的文字。
- **电光蓝 (#3B82F6)**：主高亮，冷色调的能量。
- **亮橙色 (#FB923C)**：能量、紧迫感。
- **洋红 (#EC4899)**：创意、大胆点缀。
- **霓虹绿 (#22C55E)**：成功、增长。
- **紫罗兰 (#8B5CF6)**：创新、高端。

## Typography

字体策略追求极端的比例对比和最大冲击力：
- **标题**：粗体压缩字型，如 Impact、Oswald Bold 或 Bebas Neue。超大标题主导整个幻灯片。全大写以获得最大冲击力。紧凑字间距。
- **正文**：干净的无衬线字体，如 Inter、SF Pro 或 Helvetica Neue。正文使用中等字重。与背景形成高对比度。
- **标签/数据**：Impact / Oswald Bold，粗体数据展示，戏剧化的数字呈现。

## Layout

幻灯片布局策略如同杂志封面设计：
- 全出血图像或纯色背景，最大化视觉冲击。
- 负空间制造张力，极端的比例对比（超大标题，小正文）。
- 大胆的色块构图，动态对角线和斜角。

## Elevation & Depth

视觉层次通过戏剧化的光影和层叠传达：
- 高对比渐变（subtle，不刺眼）为背景增添氛围深度。
- 文字上的戏剧性光影效果，如聚光灯或背光。
- 动态对角线和斜角创造运动感。
- 大面积色块的层叠关系提供清晰的视觉层级。

## Shapes

形状语言硬朗、几何、大胆：
- 几何形状和大胆色块构成主要视觉元素。
- 直角为主，不使用圆角（rounded: 0），保持锐利边缘。
- 动态对角线和斜角打破常规矩形。

## Components

### Cards
卡片使用深灰或黑色背景，边框锐利（直角）。内部使用大面积色块或全出血图像。标题使用超大字号全大写。

### Tables
表格使用电光蓝表头搭配白字，交替行使用深灰色。线条锐利，不使用圆角，保持杂志排版感。

### Charts
图表采用极简风格，网格线使用深灰色，数据系列使用电光蓝、亮橙、洋红等高饱和度色彩。不使用3D效果。

### Icons
图标风格极简，以字体本身作为视觉元素。不使用装饰性图标，让内容直接发声。

## Do's and Don'ts

- Do: 使用极端的比例对比（超大标题，小正文）
- Do: 创建大胆的色块构图
- Do: 让负空间制造张力
- Do: 使用全出血背景
- Do: 让每一页都像杂志封面
- Don't: 使用柔和或低饱和颜色
- Don't: 添加不必要的装饰元素
- Don't: 创建繁杂拥挤的布局
- Don't: 使用细弱或精致的字体
- Don't: 添加幻灯片编号、页脚或标志
