---
version: alpha
name: Notion风格
description: SaaS仪表板美学，聚焦干净数据与生产力工具样式。适用于产品演示、SaaS展示、指标仪表板、功能导览和B2B演示。
colors:
  primary: "#2383E2"
  secondary: "#0F7B6C"
  tertiary: "#F7F7F5"
  neutral: "#E5E5E5"
  surface: "#FFFFFF"
  on-surface: "#1F1F1F"
  error: "#E03E3E"
  success: "#0F7B6C"
  warning: "#DFAB01"
typography:
  display:
    fontFamily: "Inter / System UI"
    fontSize: "40pt"
    fontWeight: 600
    lineHeight: 1.1
  h1:
    fontFamily: "Inter / System UI"
    fontSize: "30pt"
    fontWeight: 600
    lineHeight: 1.15
  h2:
    fontFamily: "Inter / System UI"
    fontSize: "20pt"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "Inter / System UI"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter / System UI"
    fontSize: "11pt"
    fontWeight: 500
    lineHeight: 1.3
  data-value:
    fontFamily: "Inter / System UI"
    fontSize: "18pt"
    fontWeight: 600
    lineHeight: 1.2
spacing:
  base: 8
  xs: 4
  sm: 8
  md: 12
  lg: 20
  xl: 40
  gutter: 24
  margin: "10%"
rounded:
  sm: 3
  md: 6
  lg: 8
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.tertiary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "{colors.surface}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: neutral
  typography-style: geometric
  density: dense
  quality: soft-shadow
  spacing-level: standard
---

# Notion风格

## Overview

干净、功能性的 SaaS 界面美学。受仪表板启发的布局，清晰的数据层级。Notion、Linear 和现代生产力工具的样式。信息密集但组织有序。专业且值得信赖。品牌个性功能性、数据导向、可信赖，目标受众为产品团队、SaaS 客户和技术决策者，情感基调清晰、高效、专业。

## Colors

色板以浅灰和纯白为基底，Notion 蓝为核心强调色：
- **浅灰 (#F7F7F5)**：主背景，营造 SaaS 界面的柔和底色。
- **纯白 (#FFFFFF)**：内容卡片背景，在浅灰底色上形成层级。
- **近黑色 (#1F1F1F)**：标题与正文，提供高对比度阅读体验。
- **灰色 (#6B6B6B)**：元数据、标签，次要信息层级。
- **浅边框 (#E5E5E5)**：卡片边框、分隔线，微妙的结构划分。
- **Notion蓝 (#2383E2)**：链接、主操作、关键数据高亮。
- **成功绿 (#0F7B6C)**：正面指标、积极状态。
- **警示红 (#E03E3E)**：负面指标、错误状态。
- **警告黄 (#DFAB01)**：注意事项、警告状态。

## Typography

字体策略采用系统 UI 字体栈，功能性导向，针对屏幕阅读优化：
- **标题**：系统 UI 字体栈或 Inter。半粗字重用于强调，干净、功能性的字母形态，略微紧凑的字间距。
- **正文**：同一家族常规字重，针对屏幕阅读优化，舒适的行高（1.5-1.6）。
- **标签/数据**：Inter / System UI 中等字重，保证小字号下的清晰度。

## Layout

幻灯片布局策略遵循 SaaS 仪表板的卡片化组织：
- 基于卡片的内容组织，卡片在浅灰背景上形成清晰的视觉层级。
- 网格对齐，保持布局的一致性和可预测性。
- 信息密集但组织有序，数据层级清晰。
- 进度条、指标展示和标签芯片等功能性元素有序排列。

## Elevation & Depth

视觉层次通过 subtle 的阴影和边框传达：
- 卡片使用 subtle 的边框或极轻微的阴影，在浅灰背景上形成悬浮感。
- 层级通过卡片堆叠、边框对比和背景色差异建立。
- 不使用强烈的立体效果或渐变背景。
- 悬停状态样式微妙，不喧宾夺主。

## Shapes

形状语言功能性、几何简洁：
- 中小圆角（3-8px），保持 SaaS 界面的现代感。
- 基于卡片的矩形布局为主。
- 标签和标记芯片使用小圆角矩形。
- 不使用圆润的 blob 形状或有机形态。

## Components

### Cards
卡片使用纯白背景，搭配浅灰边框，中小圆角（6px）。内部内容对齐严格遵循网格，Notion蓝用于链接和主操作高亮。卡片可包含标题栏、内容区域和底部操作区。

### Tables
表格使用浅灰表头搭配近黑文字，交替行使用纯白底色。线条精确，单元格对齐严格，圆角克制。数据层级通过字号和颜色区分。

### Charts
图表采用干净的数据可视化风格，网格线使用浅灰，数据系列使用 Notion蓝、成功绿、警告黄、警示红。不使用3D效果或渐变。指标醒目展示，数据层级清晰。

### Icons
图标风格为功能性几何图标，线条简洁，基于图标的导航提示。禁止使用装饰性插画，所有图标必须服务于信息传达。

## Do's and Don'ts

- Do: 使用基于卡片的内容组织
- Do: 创建清晰的数据层级
- Do: 使用 subtle 的阴影和边框
- Do: 保持布局网格对齐
- Do: 醒目地展示指标
- Don't: 使用装饰性插画
- Don't: 添加渐变或复杂背景
- Don't: 创建艺术性布局
- Don't: 使用圆润的 blob 形状
- Don't: 添加幻灯片编号、页脚或标志
