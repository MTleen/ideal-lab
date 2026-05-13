---
version: alpha
name: 手绘笔记风格
description: 柔和的手绘插画风格，笔触放松，整体清新精致，兼具极简编辑美学与温暖亲切感。适用于教育内容、知识分享、技术讲解和友好型演示。
colors:
  primary: "#F4A261"
  secondary: "#E9C46A"
  tertiary: "#7EC8E3"
  neutral: "#D9D4C8"
  surface: "#FAF8F0"
  on-surface: "#2C3E50"
  error: "#A0522D"
  success: "#87A96B"
  warning: "#E9C46A"
typography:
  display:
    fontFamily: "粗体手写马克笔字体 / 卡通海报字体"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 1.1
  h1:
    fontFamily: "粗体手写马克笔字体 / 卡通海报字体"
    fontSize: "36pt"
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: "粗体手写马克笔字体 / 卡通海报字体"
    fontSize: "24pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "清晰手写圆体 / 硬笔手写体"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "清晰手写圆体 / 硬笔手写体"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "粗体手写马克笔字体 / 卡通海报字体"
    fontSize: "20pt"
    fontWeight: 700
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
  lg: 16
  full: 9999px
components:
  card:
    backgroundColor: "#F5F2E8"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "#F5F2E8"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: organic
  mood: warm
  typography-style: handwritten
  density: balanced
  quality: flat
  spacing-level: generous
---

# 手绘笔记风格

## Overview

手绘笔记风格以插画或手绘质感为核心，笔触柔和放松。整体风格清新、精致，采用极简编辑手法。强调精准、清晰与知性优雅，同时优先传递温暖、亲切与友好感。品牌个性亲和、创意、轻松，目标受众为学习者、教育者和知识分享者，情感基调温暖、友好、轻松。

## Colors

色板围绕温暖的米白纸质感构建：
- **暖调米白 (#FAF8F0)**：主背景，模拟优质纸张的温和色调。
- **深炭灰 (#2C3E50)**：标题与正文，高对比度确保可读性。
- **深棕色 (#4A4A4A)**：次要文字元素。
- **柔橙色 (#F4A261)**：高亮与强调，温暖的主色调。
- **芥末黄 (#E9C46A)**：次要高亮，阳光般的温暖感。
- **鼠尾草绿 (#87A96B)**：自然、成长概念。
- **浅蓝色 (#7EC8E3)**：科技、AI 元素。
- **红棕色 (#A0522D)**：土地、基础设施，也可用于错误状态。
- **暖灰 (#D9D4C8)**：分隔线、边框、次要背景。

## Typography

字体策略追求手绘质感与可读性的平衡：
- **标题**：粗体手写马克笔字体或卡通海报字体。基线略有不齐，营造有机感。笔画粗壮，边缘柔和。以手绘字母呈现，非打字效果。
- **正文**：清晰的手写圆体或硬笔风格，模拟日常笔记。字号一致，带有轻微自然变化。以随意手写呈现，清晰但不呆板。
- **标签/数据**：手写风格，保持手绘温度的同时确保数据可读性。

## Layout

幻灯片布局策略追求开阔、结构清晰且轻松：
- 版面开阔且结构清晰，避免过度拥挤。
- 标题区偏上，正文内容分区排列，留有充足的呼吸空间。
- 元素层叠时保留微妙重叠，增添手绘的随意感。

## Elevation & Depth

视觉层次通过手绘层叠和颜色区分传达：
- 不使用阴影系统，完全依赖颜色深浅和线条粗细建立层次。
- 连接线带有手绘波浪感，不必完全笔直。
- 元素层叠时保留微妙重叠，增添手绘的有机深度。

## Shapes

形状语言体现手绘的不完美与有机感：
- 手绘粉笔插画，带有潦草不完美的线条。
- 圆角柔和，不使用锐利的几何形状（圆角: 4-16px）。
- 简笔画和简单图标，带有手绘质感的连接线。
- 色彩填充无需完全填满轮廓，保留手绘的随意感。

## Components

### Cards
卡片使用米白色背景（#F5F2E8），搭配暖灰边框，柔和圆角（16px）。内容使用深炭灰书写，点缀柔橙色或芥末黄。边框可带有轻微手绘抖动。

### Tables
表格使用柔橙色表头搭配深炭灰字，交替行使用米白色。线条带有轻微手绘波浪感，不使用完美直线。

### Charts
图表采用手绘风格的数据可视化，网格线使用暖灰色，数据系列依次使用柔橙色、芥末黄、浅蓝色、鼠尾草绿、红棕色。线条带有手绘质感。

### Icons
图标风格为概念抽象图标，用于阐释思想而非写实场景。带有潦草不完美的线条和手绘波浪感。包含星星、螺旋线、下划线等涂鸦式装饰元素。

## Do's and Don'ts

- Do: 保持版面开阔且结构清晰
- Do: 强调信息层级与可读性
- Do: 所有元素采用手绘质感
- Do: 允许不完美——轻微抖动增添个性
- Do: 元素层叠时保留微妙重叠
- Don't: 使用完美的几何图形
- Don't: 创建写实元素
- Don't: 元素过度拥挤
- Don't: 使用纯白色背景
- Don't: 添加页码、页脚或徽标
