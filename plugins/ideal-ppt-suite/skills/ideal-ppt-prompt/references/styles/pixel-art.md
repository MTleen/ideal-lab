---
version: alpha
name: 像素风格
description: 复古 8-bit 像素艺术美学，怀旧的游戏视觉风格，适用于游戏演示、技术教程与开发者演讲
colors:
  primary: "#00FFFF"
  secondary: "#FF00FF"
  tertiary: "#00FF00"
  neutral: "#E6E6FA"
  surface: "#87CEEB"
  on-surface: "#1A1A2E"
  error: "#FF0000"
  success: "#00FF00"
  warning: "#FFFF00"
typography:
  display:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "48px"
    fontWeight: "700"
    lineHeight: "1.2"
  h1:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "32px"
    fontWeight: "700"
    lineHeight: "1.2"
  h2:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "24px"
    fontWeight: "700"
    lineHeight: "1.3"
  body:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.5"
  label:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "12px"
    fontWeight: "400"
    lineHeight: "1.4"
  data-value:
    fontFamily: "'Courier New', 'Press Start 2P', monospace"
    fontSize: "28px"
    fontWeight: "700"
    lineHeight: "1.2"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  gutter: "24px"
  margin: "32px"
rounded:
  sm: "0px"
  md: "0px"
  lg: "0px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.on-surface}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.on-surface}"
    headerTextColor: "{colors.surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "{colors.on-surface}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: pixel
  mood: vibrant
  typography-style: technical
  density: balanced
  quality: flat
  spacing-level: standard
---

# 像素风格

## Overview

像素风格以经典的 8-bit 和 16-bit 游戏时代为灵感，品牌个性 playful、复古且充满开发者文化气质。目标受众为游戏从业者、技术教程观众与复古文化爱好者。情感基调趣味、怀旧且立即 recognizable，通过块状像素、有限调色板与简单的几何形状，将复杂信息转化为游戏化的视觉语言。

## Colors

色板以浅蓝（#87CEEB）为表面基底，备选背景使用柔和薰衣草紫（#E6E6FA），提供两种复古游戏场景感。深海军蓝（#1A1A2E）作为表面文字色，确保在明亮背景上的高可读性。像素绿（#00FF00）用于成功与高亮，像素红（#FF0000）用于警示与强调，像素黄（#FFFF00）用于警告与能量，像素青（#00FFFF）用于信息与科技元素，像素洋红（#FF00FF）用于特殊元素。每页限制在 16-32 色调色板内。

## Typography

字体策略采用像素化位图字体风格， chunky、blocky 的字母形态带有可见的像素结构。标题全大写以获得最大可读性，渲染为实际的像素艺术而非平滑矢量。正文使用更小的像素字体，保持一致的 8x8 或 16x16 字符网格。有限抗锯齿以保持复古感。层级关系：Display（48px 像素标题） > H1（32px） > H2（24px） > Body（16px） > Label（12px）。所有字号均为 4 的倍数，对齐像素网格。

## Layout

采用 balanced 密度与 standard 间距节奏。幻灯片边距 32px，gutter 24px。布局遵循块状网格逻辑，元素以 8px 或 16px 的倍数对齐。文字气泡与对话框使用像素边框，进度条由 chunky 像素段组成。8-bit 装饰元素（星星、爱心、箭头）散布于内容间隙，强化游戏化氛围。

## Elevation & Depth

视觉层次完全扁平（flat quality），通过颜色对比与像素块的位置关系传达深度。抖动图案（dithering）用于颜色过渡与阴影区域，替代平滑渐变。无投影、无渐变、无抗锯齿。深度感来源于层叠的像素平面与有限的色调明暗变化，忠实还原早期游戏机的视觉限制。

## Shapes

形状语言以 blocky 几何为主。所有圆角为 0px，保持纯粹的像素块感。文字气泡、卡片、按钮均为直角矩形，边框由可见的像素线条构成。简单图标（记事本、复选框、齿轮、火箭、播放按钮）以 8-bit 形式渲染，轮廓由方形像素组成。拒绝任何曲线或平滑边缘。

## Components

### Cards
卡片背景使用浅蓝（surface），边框采用深海军蓝（on-surface）的粗像素线，无圆角（0px），中等内边距（16px）。卡片边缘由可见的像素块构成，可带有 8-bit 风格的装饰性边角图案。

### Tables
表格使用深海军蓝（on-surface）作为表头背景，浅蓝（surface）作为表头文字色，交替行使用柔和薰衣草紫（neutral）。表格线条为粗像素网格，单元格严格对齐像素边界。

### Charts
图表网格线使用深海军蓝（on-surface），数据系列依次使用像素青、像素洋红、像素绿、像素黄、像素红。图表元素以块状像素柱、折线或饼图呈现，拒绝平滑曲线与抗锯齿。坐标轴刻度为块状像素标记。

### Icons
图标采用 8-bit 风格，由可见的像素网格组成。线条 chunky，最小可见单元为单个像素。可包含星星、爱心、箭头、宝箱、心形等经典游戏符号。所有图标保持 16x16 或 32x32 的像素尺寸规范。

## Do's and Don'ts

- Do: 始终维持一致的像素网格
- Do: 使用有限的调色板（最多 16-32 色）
- Do: 创建块状几何形状
- Do: 在适当的地方添加怀旧游戏元素
- Do: 使用抖动实现颜色过渡
- Don't: 使用平滑渐变或抗锯齿
- Don't: 创建照片级写实元素
- Don't: 使用细线或精细细节
- Don't: 添加现代光泽效果
- Don't: 添加幻灯片编号、页脚或标志
