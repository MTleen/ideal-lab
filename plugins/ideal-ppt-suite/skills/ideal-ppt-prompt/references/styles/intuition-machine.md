---
version: alpha
name: 直觉机器风格
description: 技术简报信息图风格，带有做旧纸张纹理与双语解释性文本框，适用于技术解释、学术演示与知识文档
colors:
  primary: "#2F7373"
  secondary: "#8B7355"
  tertiary: "#722F37"
  neutral: "#5D3A3A"
  surface: "#F5F0E6"
  on-surface: "#1A1A1A"
  error: "#722F37"
  success: "#2F7373"
  warning: "#8B7355"
typography:
  display:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "40px"
    fontWeight: "700"
    lineHeight: "1.15"
  h1:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "28px"
    fontWeight: "700"
    lineHeight: "1.2"
  h2:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "20px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.5"
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
  margin: "20px"
rounded:
  sm: "2px"
  md: "4px"
  lg: "8px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "#F5F0E1"
    rowAltBackgroundColor: "#F5F0E1"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: cool
  typography-style: technical
  density: dense
  quality: soft-shadow
  spacing-level: compact
---

# 直觉机器风格

## Overview

直觉机器风格是一种学术/技术简报演示风格，拒绝艺术化 3D 渲染，拥抱干净的 2D 或等轴测技术插画。品牌个性理性、权威且信息密集，目标受众为技术从业者、学术研究者与双语知识工作者。情感基调冷静、精确且值得信赖，通过复古蓝图美学与现代清晰度的结合，将复杂概念拆解为可理解的模块。

## Colors

色板以做旧奶油色（#F5F0E6）为表面基底，营造复古技术印刷品的温暖纸张感。暖白色（#F5F0E1）用于蓝图纸张效果与交替行背景。深褐红（#5D3A3A）作为标题与强调文字色，近黑色（#1A1A1A）用于正文文本框内容。青色（#2F7373）承担主插画语义，暖棕色（#8B7355）用于辅助元素，褐红（#722F37）用于标题强调。深炭灰（#2D2D2D）勾勒所有元素轮廓，维持统一的线框感。

## Typography

字体策略采用粗体展示字体作为标题，深褐红色，主标题使用全大写加方括号格式，英文副标题位于下方较小字号。技术权威感与复古特征并存。双语标注标签使用干净的无衬线体，格式为"英文术语 中文翻译"，与背景形成高对比。文本框内容使用干净的几何无衬线体，小字号下保持可读性，全篇字重一致。层级关系：Display（40px 主标题） > H1（28px 章节标题） > H2（20px 子标题） > Body（14px 文本框内容） > Label（11px 双语标签）。

## Layout

采用 dense 密度与 compact 间距节奏。幻灯片边距紧凑（20px）， gutter 仅 16px，最大化内容承载面积。布局以分割或三联画为主：视觉居左/中，文本居右/下。每页包含 3-5 个解释性文本框，底部设置"核心引言"框承载核心洞察。信息密集但视觉层级清晰，通过留白与分组避免混乱。

## Elevation & Depth

视觉层次通过柔和的投影（soft-shadow quality）与清晰的层级分组传达。元素之间保持干净的 2D 关系，等轴测插画提供有限的立体感。无渐变、无光泽、无玻璃拟态。深度感来源于分割布局的空间组织，而非三维渲染。所有元素带有干净的黑色轮廓线，强化扁平但层次分明的技术图纸感。

## Shapes

形状语言以几何、精确为主。小圆角（md: 4px）用于文本框与容器，保持技术文档的克制感。等轴测方块、矩形网格与流程图节点构成主要形状库。线条笔直、棱角分明，拒绝有机曲线。标注框与引线采用直角转折，符合工程图纸规范。

## Components

### Cards
卡片背景使用做旧奶油色（surface），边框采用深褐红（neutral），小圆角（4px）与中等内边距（12px）。卡片通常以文本框形式出现，承载来源材料的实质性内容，边缘干净无装饰。

### Tables
表格使用青色（primary）作为表头背景，暖白色（#F5F0E1）作为表头文字色以保证对比，交替行使用暖白色（#F5F0E1）降低视觉疲劳。表格线条使用深炭灰，保持技术文档的精确感。

### Charts
图表网格线使用深褐红（neutral），数据系列依次使用青色、暖棕色、褐红。图表应以 2D 平面或等轴测方式呈现，元素带有清晰的黑色轮廓，拒绝立体渲染与渐变填充。

### Icons
图标采用扁平 2D 或等轴测风格，线条为干净的黑色轮廓，内部填充单一色块。可包含电路、齿轮、流程图等与技术主题相关的符号。图标尺寸适中，配合双语标注标签使用。

## Do's and Don'ts

- Do: 包含 3-5 个带有来源材料实质性内容的文本框
- Do: 关键元素使用双语标签（英文 + 中文）
- Do: 添加与主题相关的褪色主题背景图案
- Do: 始终贯穿做旧纸张纹理
- Do: 用分割布局创建清晰的视觉层级
- Don't: 创建照片级写实渲染或艺术化 3D 场景
- Don't: 幻灯片缺乏解释性文字内容
- Don't: 在角落添加标题块或印章
- Don't: 使用渐变或光泽效果
- Don't: 添加幻灯片编号、页脚或标志
