---
version: alpha
name: 复古风格
description: 复古做旧纸张美学，适用于历史与探险风格的演示，唤起发现、传承与永恒知识之感
colors:
  primary: "#2D5A3D"
  secondary: "#1E3A5F"
  tertiary: "#722F37"
  neutral: "#6B4423"
  surface: "#F5E6D3"
  on-surface: "#3D2914"
  error: "#722F37"
  success: "#2D5A3D"
  warning: "#C9A227"
typography:
  display:
    fontFamily: "Garamond, Baskerville, 'Times New Roman', serif"
    fontSize: "64px"
    fontWeight: "700"
    lineHeight: "1.1"
  h1:
    fontFamily: "Garamond, Baskerville, 'Times New Roman', serif"
    fontSize: "44px"
    fontWeight: "700"
    lineHeight: "1.15"
  h2:
    fontFamily: "Garamond, Baskerville, 'Times New Roman', serif"
    fontSize: "28px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "Garamond, Baskerville, 'Times New Roman', serif"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.7"
  label:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "12px"
    fontWeight: "500"
    lineHeight: "1.4"
  data-value:
    fontFamily: "Garamond, Baskerville, 'Times New Roman', serif"
    fontSize: "32px"
    fontWeight: "700"
    lineHeight: "1.2"
spacing:
  base: "8px"
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "40px"
  xl: "64px"
  gutter: "32px"
  margin: "48px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "#FFF8DC"
    rowAltBackgroundColor: "#FFF8DC"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: paper
  mood: warm
  typography-style: editorial
  density: balanced
  quality: flat
  spacing-level: generous
---

# 复古风格

## Overview

复古风格以怀旧做旧纸张美学为核心，灵感源自探险家日志、古旧地图与博物馆展品。品牌个性庄重、有历史感且充满叙事张力，目标受众为历史爱好者、博物馆观众、旅行探险内容与 heritage 品牌受众。情感基调温暖、 discovery-oriented 且 timeless，通过厚重的纸张纹理、咖啡渍与磨损边缘，将观众带入一段关于发现与传承的时空旅程。

## Colors

色板以做旧羊皮纸（#F5E6D3）为表面基底，备选背景使用乌贼墨色奶油（#FFF8DC），营造历史文献的真实纸张感。深棕色（#3D2914）作为表面文字色，中棕色（#6B4423）用于批注与辅助文字。森林绿（#2D5A3D）用于地图与自然元素，藏青色（#1E3A5F）用于海洋与线条，酒红色（#722F37）用于强调与边框，金色（#C9A227）用于高亮与指南针。乌贼黑（#3D3D3D）用于精细细节。整体色调严格限定在暖 sepia 范围内，拒绝冷色与明亮现代色。

## Typography

字体策略采用经典衬线体（Garamond、Baskerville 或类似）作为标题，具有历史感、优雅且权威，可包含装饰性花饰。地图标签与批注使用紧缩衬线体或干净无衬线体，符合时代风格。正文使用可读性强的衬线体，遵循传统书籍排版，行高宽松以提供舒适的阅读体验。层级关系：Display（64px 历史标题） > H1（44px 章节标题） > H2（28px 子标题） > Body（16px 正文） > Label（12px 地图标签/批注）。数据值使用 32px 粗衬线体，保持与标题一致的历史权威感。

## Layout

采用 balanced 密度与 generous 间距节奏。幻灯片边距 48px，gutter 32px。布局偏好层叠拼贴构图，古董地图占据主要画面，路线线与地标穿插其中。罗盘玫瑰与航海元素置于角落或边缘。标本绘图（植物、动物、化石）以网格或散落方式排列。手写风格批注以倾斜角度覆盖于图像之上，绳索、皮革与黄铜装饰图案作为边框或分隔线。

## Elevation & Depth

视觉层次通过纸张层叠、拼贴关系与风化纹理传达，完全扁平（flat quality）。无数字阴影、无渐变、无立体效果。深度感来源于不同纸张层的前后叠加（如地图叠在信纸上）、复古照片风格相框的物理边框错觉，以及纹理浓淡变化带来的视觉起伏。咖啡渍、折痕与磨损边缘本身就是深度的叙事性表达。

## Shapes

形状语言以古典、庄重为主，同时带有岁月的柔和。中等圆角（md: 8px）用于卡片与相框，大圆角（12px）用于主要容器，但整体仍以直角与古典曲线为主。地图边框可使用装饰性的 rope 或 brass 图案。相框带有复古的厚重感与轻微的不规则边缘。线条可带有手绘的轻微抖动，拒绝数字化的完美直线。

## Components

### Cards
卡片背景使用做旧羊皮纸（surface），边框采用中棕色（neutral），中等圆角（8px）与宽松内边距（40px）。卡片可承载古旧地图片段、探险日志页面或标本绘图，边缘可带有轻微的磨损与不规则效果。

### Tables
表格使用森林绿（primary）作为表头背景，乌贼墨色奶油（#FFF8DC）作为表头文字色，交替行使用乌贼墨色奶油（#FFF8DC）。表格线条使用中棕色或乌贼黑，保持历史文献的庄重感。表头可使用古典的上下边框线装饰。

### Charts
图表网格线使用中棕色（neutral），数据系列依次使用森林绿、藏青色、酒红色、金色。图表应以手绘地图或航海图风格呈现，坐标轴可带有纬度/经度样式的刻度，数据点以图标（如船只、指南针）标记。

### Icons
图标采用手绘风格或古典版画风格，线条带有轻微的不规则与粗细变化。可包含罗盘玫瑰、船只、望远镜、羽毛笔、旧式相机等历史符号。图标可带有 sepia 色调或羊皮纸底色，保持与整体风格一致的古董气质。

## Do's and Don'ts

- Do: 始终应用一致的做旧纹理
- Do: 使用符合时代的视觉语言
- Do: 在相关处包含地图与旅程元素
- Do: 创建层叠拼贴构图
- Do: 保持温暖的乌贼色调色板
- Don't: 使用现代数字风格
- Don't: 创建清晰锐利的边缘
- Don't: 使用冷调或明亮色彩
- Don't: 添加当代元素
- Don't: 添加页码、页脚或徽标
