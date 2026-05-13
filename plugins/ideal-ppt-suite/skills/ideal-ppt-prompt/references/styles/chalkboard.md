---
version: alpha
name: 黑板风格
description: 经典教室黑板美学，搭配手绘粉笔插画，怀旧的教育氛围与温暖的彩色粉笔质感。适用于教育演示、课堂内容、教程和非正式学习分享。
colors:
  primary: "#FFE566"
  secondary: "#FF9999"
  tertiary: "#66B3FF"
  neutral: "#2D2D2D"
  surface: "#1A1A1A"
  on-surface: "#F5F5F5"
  error: "#FFB366"
  success: "#90EE90"
  warning: "#FFB366"
typography:
  display:
    fontFamily: "手绘粉笔字风格"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 1.1
  h1:
    fontFamily: "手绘粉笔字风格"
    fontSize: "36pt"
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: "手绘粉笔字风格"
    fontSize: "24pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "整洁粉笔手写体"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "整洁粉笔手写体"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "手绘粉笔字风格"
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
  sm: 4
  md: 8
  lg: 16
  full: 9999px
components:
  card:
    backgroundColor: "{colors.neutral}"
    borderColor: "#3D3D3D"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "#3D3D3D"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: organic
  mood: warm
  typography-style: handwritten
  density: balanced
  quality: flat
  spacing-level: generous
---

# 黑板风格

## Overview

黑板风格以经典教室黑板美学为核心，搭配手绘粉笔插画，营造怀旧的教育氛围。不完美的潦草线条捕捉传统教学的温暖，彩色粉笔在保持真实黑板体验的同时创造视觉层级。品牌个性温暖、亲和、教育感强，目标受众为学生、教育工作者和培训参与者，情感基调友好、亲切、略带俏皮。

## Colors

色板围绕真实黑板体验构建：
- **黑板黑 (#1A1A1A)**：主背景，模拟真实黑板。
- **绿黑色 (#1C2B1C)**：传统绿色黑板备选。
- **粉笔白 (#F5F5F5)**：主文字与轮廓线，模拟粉笔书写效果。
- **粉笔黄 (#FFE566)**：高亮与强调，模拟黄色粉笔。
- **粉笔粉 (#FF9999)**：次级高亮，柔和的粉色粉笔质感。
- **粉笔蓝 (#66B3FF)**：图表与链接，蓝色粉笔元素。
- **粉笔绿 (#90EE90)**：成功与自然，绿色粉笔元素。
- **粉笔橙 (#FFB366)**：警告与能量，橙色粉笔元素。

## Typography

字体策略追求真实的手写粉笔质感：
- **标题**：手绘粉笔字风格，粗体、略微不均匀的笔画，带有可见的粉笔质感。不完美的基线增添真实感。白色或亮色彩粉笔用于强调。
- **正文**：更整洁的粉笔手写体以保证可读性，字号一致但带有自然变化。浅粉笔质感，笔画比标题更细。
- **标签/数据**：整洁粉笔手写体，保持可读性的同时带有手绘温度。

## Layout

幻灯片布局策略模拟黑板板书：
- 布局相对自由，模仿教师在黑板上的书写习惯。
- 标题区偏上居中或偏左，正文内容分区排列。
- 涂鸦、星星、箭头、下划线等装饰元素散布其间，增添课堂氛围。

## Elevation & Depth

视觉层次通过粉笔质感和层叠涂鸦传达：
- 不使用阴影系统，完全依赖粉笔颜色深浅和线条粗细建立层次。
- 文字和关键元素周围的粉笔粉尘效果增添真实感。
- 板擦痕迹和粉笔残留纹理提供有机的纹理深度。

## Shapes

形状语言体现手绘粉笔的不完美：
- 手绘粉笔插画，带有潦草不完美的线条。
- 圆角柔和，不使用锐利的几何形状（圆角: 4-16px）。
- 简笔画和简单图标，带有手绘质感的连接线。

## Components

### Cards
卡片使用深灰底色（#2D2D2D），模拟黑板上的分区。边框使用略浅的灰色，圆角柔和。内容使用粉笔白或彩色粉笔书写。

### Tables
表格使用粉笔黄表头搭配黑板背景白字，交替行使用深灰色。线条带有轻微手绘抖动，不使用完美直线。

### Charts
图表采用手绘风格的数据可视化，网格线使用深灰色，数据系列依次使用粉笔黄、粉笔粉、粉笔蓝、粉笔绿、粉笔橙。线条带有手绘质感。

### Icons
图标风格为手绘简笔画，带有潦草不完美的线条和粉笔粉尘效果。包含星星、箭头、下划线、圆圈、对勾等课堂涂鸦元素。

## Do's and Don'ts

- Do: 所有元素保持真实的粉笔质感
- Do: 始终使用不完美的手绘品质
- Do: 添加细微的粉笔粉尘和涂抹效果
- Do: 用多种颜色创建视觉层级
- Do: 包含俏皮的涂鸦和注释
- Don't: 使用完美的几何形状
- Don't: 创建干净的数字化线条
- Don't: 添加照片级写实元素
- Don't: 使用渐变或光泽效果
- Don't: 添加幻灯片编号、页脚或标志
