---
version: alpha
name: 科学风格
description: 教育科学插画风格，用于通路、流程和技术示意图，适用于生物讲座、医学教育与学术会议
colors:
  primary: "#0D9488"
  secondary: "#3B82F6"
  tertiary: "#8B5CF6"
  neutral: "#475569"
  surface: "#FAFAFA"
  on-surface: "#1E293B"
  error: "#EF4444"
  success: "#22C55E"
  warning: "#F59E0B"
typography:
  display:
    fontFamily: "'Times New Roman', Times, serif"
    fontSize: "44px"
    fontWeight: "700"
    lineHeight: "1.15"
  h1:
    fontFamily: "'Times New Roman', Times, serif"
    fontSize: "28px"
    fontWeight: "700"
    lineHeight: "1.2"
  h2:
    fontFamily: "'Times New Roman', Times, serif"
    fontSize: "20px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "'Times New Roman', Times, serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.6"
  label:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "11px"
    fontWeight: "500"
    lineHeight: "1.3"
  data-value:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "20px"
    fontWeight: "700"
    lineHeight: "1.2"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  gutter: "16px"
  margin: "24px"
rounded:
  sm: "2px"
  md: "4px"
  lg: "6px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "#FFFFFF"
    rowAltBackgroundColor: "#F0F4F8"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: cool
  typography-style: technical
  density: dense
  quality: flat
  spacing-level: compact
---

# 科学风格

## Overview

科学风格以学术科学插画美学为核心，适用于生物通路、化学过程与技术系统的精确表达。品牌个性严谨、客观且教育导向，目标受众为生物学与医学学生、研究者及科学会议听众。情感基调冷静、清晰且权威，通过教科书品质的示意图与学术期刊级别的标注规范，将复杂的科学概念转化为易理解的视觉叙事。

## Colors

色板以米白（#FAFAFA）为表面基底，备选背景使用浅蓝灰（#F0F4F8），营造实验室与出版物般的清洁感。深岩灰（#1E293B）作为表面文字色，中灰（#475569）用于注释与标签。通路色系统采用青色（#0D9488）作为主通路，蓝色（#3B82F6）作为次级通路，紫色（#8B5CF6）作为第三通路。琥珀色（#F59E0B）用于生物膜结构，红色（#EF4444）用于关键分子与警示，绿色（#22C55E）用于产物与正向输出。整体色调冷静、功能性强，色彩分配严格对应科学语义。

## Typography

字体策略采用 Times New Roman 风格的干净衬线体作为标题与正文，营造正式的学术出版感。主标题使用粗体，专业且权威。示意图标签与注释使用无衬线体，清晰且在小字号下可读。正文段落使用衬线体，项目符号和列表使用无衬线体，遵循学术出版物的排版惯例。层级关系：Display（44px 标题） > H1（28px 章节） > H2（20px 子标题） > Body（14px 正文/段落） > Label（11px 标签/注释）。数据值使用 20px 粗体无衬线体，在图表中突出关键数值。

## Layout

采用 dense 密度与 compact 间距节奏。幻灯片边距 24px，gutter 16px，最大化示意图的展示面积。水平膜或结构基座作为画面的组织轴心，模块化组件沿基座分布。流程箭头明确指示电子、质子或分子的运动方向。编号步骤序列从左至右或从上至下排列，过程摘要框置于右下角或底部。关键分子使用 callout 标注突出。

## Elevation & Depth

视觉层次完全扁平（flat quality），通过精确的线条权重、颜色分区与空间位置传达深度。无阴影、无渐变、无三维效果。深度感来源于剖面与通路的前后关系、水平基座的上下分层，以及流程箭头的方向性引导。化学公式与分子符号的层级通过字号与颜色区分，而非立体渲染。

## Shapes

形状语言以精确、几何为主。极小圆角（sm: 2px）用于过程摘要框与容器，保持科学图表的克制感。膜结构使用水平带状矩形，模块化组件为圆角矩形或标准几何形状。流动箭头为标准三角箭头，线宽一致。分子符号使用标准化学记号线框。所有形状边缘清晰，拒绝有机曲线与装饰性变形。

## Components

### Cards
卡片背景使用米白（surface），边框采用中灰（neutral），极小圆角（2px）与小内边距（8px）。卡片通常以过程摘要框或关键分子 callout 的形式出现，边缘干净，无多余装饰。

### Tables
表格使用青色（primary）作为表头背景，白色（#FFFFFF）作为表头文字色，交替行使用浅蓝灰（#F0F4F8）。表格线条使用 1px 中灰细线，保持学术出版物的精确感。表头文字左对齐或居中对齐，数据列右对齐。

### Charts
图表网格线使用中灰（neutral），数据系列依次使用青色、蓝色、紫色、绿色、琥珀色、红色。图表类型以线图、柱状图或通路图为主，坐标轴刻度清晰，数据点使用几何标记。拒绝立体效果与渐变填充，保持教科书插画的平面精确性。

### Icons
图标采用极简的几何线框风格，线宽统一。可包含分子、原子、箭头、烧杯、DNA 双螺旋等科学符号。图标无填充或仅使用浅色填充，保持与示意图一致的语言。所有图标精确、无装饰。

## Do's and Don'ts

- Do: 使用精确、一致的线宽
- Do: 清晰标注所有组件
- Do: 用箭头展示方向性流动
- Do: 在相关处包含化学/分子符号
- Do: 创建清晰的编号序列
- Don't: 使用装饰性插画
- Don't: 创建不精确或艺术化的示意图
- Don't: 遗漏重要标签
- Don't: 使用不一致的视觉语言
- Don't: 添加幻灯片编号、页脚或标志
