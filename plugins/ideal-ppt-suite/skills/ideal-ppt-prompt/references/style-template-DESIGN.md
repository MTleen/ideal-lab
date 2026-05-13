# DESIGN.md 风格定义模板（PPT 适配版）

基于 Google Labs DESIGN.md 开源协议，适配为幻灯片风格定义格式。

## 格式规范

每个风格文件是一个自包含的 Markdown 文件，包含 YAML frontmatter（机器可读 token）+ Markdown body（人类可读设计 rationale）。

---

## 文件结构

```
---
version: alpha
name: {风格中文名}
description: {一句话描述适用场景}
colors:
  primary: "#{HEX}"
  secondary: "#{HEX}"
  tertiary: "#{HEX}"
  neutral: "#{HEX}"
  surface: "#{HEX}"
  on-surface: "#{HEX}"
  error: "#{HEX}"
  success: "#{HEX}"
  warning: "#{HEX}"
typography:
  display:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
  h1:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
  h2:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
  body:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
  label:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
  data-value:
    fontFamily: {字体}
    fontSize: {尺寸}
    fontWeight: {字重}
    lineHeight: {行高}
spacing:
  base: {基准间距}
  xs: {极小}
  sm: {小}
  md: {中}
  lg: {大}
  xl: {极大}
  gutter: {列间距}
  margin: {页边距}
rounded:
  sm: {小圆角}
  md: {中圆角}
  lg: {大圆角}
  full: 9999px
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "{colors.neutral}"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: {clean|grid|organic|pixel|paper}
  mood: {professional|warm|cool|vibrant|dark|neutral}
  typography-style: {geometric|humanist|handwritten|editorial|technical}
  density: {minimal|balanced|dense|ultra-dense}
  quality: {flat|soft-shadow|glassmorphism|neumorphism|layered-depth}
  spacing-level: {compact|standard|generous|editorial}
---

# {风格中文名}

## Overview

{品牌个性、目标受众、情感基调的 holistic 描述}

## Colors

{色板设计 rationale，每种颜色的语义角色和使用场景}

## Typography

{字体策略，标题/正文/数据/标签的字体选择和层级关系}

## Layout

{幻灯片布局策略：网格系统、间距节奏、边距规范}

## Elevation & Depth

{视觉层次如何传达：阴影系统、层叠关系、或扁平替代方案}

## Shapes

{形状语言：圆角大小、卡片轮廓、几何特征}

## Components

### Cards
{卡片样式规范}

### Tables
{表格样式规范}

### Charts
{图表样式规范}

### Icons
{图标风格规范}

## Do's and Don'ts

- Do: {设计准则}
- Don't: {设计禁忌}
```

---

## 与旧版风格文件的对比

| 旧版章节 | DESIGN.md 对应 | 说明 |
|----------|---------------|------|
 设计理念 | Overview | 扩展为品牌个性 + 受众 + 情感基调 |
| 背景 | Colors (surface) + Layout | 背景色归入 Colors，布局策略归入 Layout |
| 字体体系 | Typography | 结构化 token + prose 描述 |
| 色彩系统 | Colors | YAML token + Markdown 语义描述 |
| 视觉元素 | Components | 拆分为 Cards/Tables/Charts/Icons |
| 风格规则 | Do's and Don'ts | 保持为约束清单 |
| 适用场景 | description (frontmatter) | 前置到 YAML |
| — | Elevation & Depth | 新增：质感/深度系统 |
| — | Shapes | 新增：形状语言 |
| — | dimensions | 新增：机器可读的维度映射 |
