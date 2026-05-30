---
version: beta
name: 学术风格
description: 面向论文汇报、课题答辩、研究综述和技术研究报告的严谨高信息密度风格。
colors:
  primary: "#1F4E79"
  secondary: "#2F6F73"
  tertiary: "#6B7280"
  neutral: "#D7DEE8"
  surface: "#FFFFFF"
  on-surface: "#172033"
  error: "#B91C1C"
  success: "#047857"
  warning: "#B45309"
typography:
  display:
    fontFamily: "Source Han Serif SC / Noto Serif SC / Times New Roman"
    fontSize: "34px"
    fontWeight: "700"
    lineHeight: "1.18"
  h1:
    fontFamily: "Source Han Serif SC / Noto Serif SC / Times New Roman"
    fontSize: "28px"
    fontWeight: "700"
    lineHeight: "1.22"
  h2:
    fontFamily: "Source Han Sans SC / Noto Sans SC / Arial"
    fontSize: "18px"
    fontWeight: "650"
    lineHeight: "1.3"
  body:
    fontFamily: "Source Han Sans SC / Noto Sans SC / Arial"
    fontSize: "13px"
    fontWeight: "400"
    lineHeight: "1.45"
  label:
    fontFamily: "Source Han Sans SC / Noto Sans SC / Arial"
    fontSize: "10px"
    fontWeight: "500"
    lineHeight: "1.3"
  data-value:
    fontFamily: "Inter / Source Han Sans SC / Arial"
    fontSize: "20px"
    fontWeight: "700"
    lineHeight: "1.15"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "18px"
  xl: "24px"
  gutter: "14px"
  margin: "28px"
rounded:
  sm: "2px"
  md: "4px"
  lg: "6px"
  full: "9999px"
components:
  card:
    backgroundColor: "#FFFFFF"
    borderColor: "#D7DEE8"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "#1F4E79"
    headerTextColor: "#FFFFFF"
    rowAltBackgroundColor: "#F5F8FB"
  chart:
    gridColor: "#D7DEE8"
    dataColors: ["#1F4E79", "#2F6F73", "#7C3AED", "#047857", "#B45309", "#B91C1C"]
dimensions:
  texture: clean
  mood: cool
  typography-style: technical
  density: dense
  quality: flat
  spacing-level: compact
---

# 学术风格

## Overview

学术风格用于研究型内容，不做演讲装饰页，而是把论文、数据、方法、实验、结论转化成可阅读的研究简报。画面应像高质量 conference slide 或 Nature/IEEE 风格研究摘要页：严谨、克制、信息密度高，所有图形都服务于论证链。

## Prompt Intent

当使用本风格写图片生成 prompt 时，必须明确每页要呈现的研究问题、方法、关键变量、结果数据和结论。布局描述应达到“构图级/区块级详细”：说明页面的焦点、区域、信息单元、图表或流程如何组织。不要写死每个像素坐标，除非该页需要复刻固定模板。

## Visual System

- 背景以纯白或极浅蓝灰为主，禁止花哨纹理、渐变大背景和装饰插画。
- 标题区紧凑，正文区最大化留给研究内容。
- 常用结构：左侧研究问题/假设，中央方法流程或模型结构，右侧结果图表与结论；或顶部结论条 + 下方 2x2 证据矩阵。
- 图表必须有轴、单位、图例、数据标签或显著性标注；不能只画“趋势感”。
- 方法流程必须包含真实步骤和变量名，如“样本纳入 → 特征提取 → 模型训练 → 外部验证”。

## Typography

标题可使用清晰衬线体营造论文感，正文、标签、图表文字使用无衬线体保证小字号可读。字号层级必须克制：页面标题 26-32px，小节标题 16-18px，正文 12-14px，图注与标签 9-11px。

## Layout Archetypes

- **Research summary**: 顶部一句结论，左侧研究问题与贡献，右侧关键图表，下方方法和限制。
- **Method pipeline**: 横向 4-6 步流程，每步含输入、处理动作、输出，不允许空标签。
- **Evidence matrix**: 2x2 或 3x2 卡片矩阵，每格展示实验、指标、结论和支撑数据。
- **Paper comparison**: 表格比较方法、数据集、指标、优点、局限。
- **Mechanism diagram**: 中央机制图，四周 callout 标注变量、路径、结果。
- **Hero result**: 一个核心结果图或关键数值占据视觉中心，四周放置方法、样本、结论和限制 callout。
- **Asymmetric paper brief**: 左侧大图/机制图，右侧窄栏承载贡献、指标和局限，形成论文摘要式非对称构图。
- **Radial mechanism**: 中央变量、机制或模型为 hub，周围连接输入、调节因素、输出和证据。
- **Diagonal hypothesis-to-result**: 从左上研究假设到右下结果结论的斜向动线。

## Do's and Don'ts

- Do: 用图表、表格、流程和注释建立论证链。
- Do: 保留必要数据、单位、样本量、指标名称和来源。
- Do: 使用细线、浅边框和小圆角保持学术克制。
- Don't: 用大图标、大插画或空洞概念图替代研究内容。
- Don't: 生成无法阅读的伪文字、伪公式或伪坐标轴。
- Don't: 为了美观删除关键变量、对照组、限制条件或来源说明。
