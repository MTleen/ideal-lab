---
version: alpha
name: 矢量插画风格
description: 扁平矢量插画风格，清晰的黑色描边搭配复古柔和配色，适用于教育演示、创意提案与儿童内容
colors:
  primary: "#E07A5F"
  secondary: "#81B29A"
  tertiary: "#F2CC8F"
  neutral: "#2D2D2D"
  surface: "#F5F0E6"
  on-surface: "#1A1A1A"
  error: "#E07A5F"
  success: "#81B29A"
  warning: "#F2CC8F"
typography:
  display:
    fontFamily: "Georgia, 'Playfair Display', serif"
    fontSize: "64px"
    fontWeight: "700"
    lineHeight: "1.1"
  h1:
    fontFamily: "Georgia, 'Playfair Display', serif"
    fontSize: "44px"
    fontWeight: "700"
    lineHeight: "1.15"
  h2:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "28px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.6"
  label:
    fontFamily: "system-ui, -apple-system, sans-serif"
    fontSize: "12px"
    fontWeight: "600"
    lineHeight: "1.4"
  data-value:
    fontFamily: "Georgia, 'Playfair Display', serif"
    fontSize: "32px"
    fontWeight: "700"
    lineHeight: "1.2"
spacing:
  base: "8px"
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "40px"
  xl: "56px"
  gutter: "32px"
  margin: "48px"
rounded:
  sm: "8px"
  md: "16px"
  lg: "24px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  table:
    headerBackgroundColor: "{colors.primary}"
    headerTextColor: "{colors.on-surface}"
    rowAltBackgroundColor: "#FFF8E7"
  chart:
    gridColor: "{colors.neutral}"
    dataColors: ["{colors.primary}", "{colors.secondary}", "{colors.tertiary}", "{colors.success}", "{colors.warning}", "{colors.error}"]
dimensions:
  texture: clean
  mood: vibrant
  typography-style: humanist
  density: balanced
  quality: flat
  spacing-level: generous
---

# 矢量插画风格

## Overview

矢量插画风格以扁平矢量美学为核心，所有元素均有清晰、统一粗细的黑色描边。品牌个性可爱、俏皮且亲切友好，目标受众为教育机构、创意提案者与儿童内容创作者。情感基调温暖、 approachable 且充满玩具模型般的趣味，通过几何简化将复杂物体还原为基础形状，营造填色绘本般的视觉体验。宽幅横向构图效果良好，适合全景式场景叙事。

## Colors

色板以奶油米白（#F5F0E6）为表面基底，营造复古印刷品的温暖怀旧感。深炭灰（#2D2D2D）承担所有元素的统一描边角色，是此风格最标志性的视觉常量。黑色（#1A1A1A）用于标题与正文文字。强调色系统采用珊瑚红（#E07A5F）传递温暖与活力，薄荷绿（#81B29A）用于自然元素，芥末黄（#F2CC8F）用于高亮与能量，焦橙色（#D4764A）作为第三强调，岩蓝（#577590）提供冷调平衡与科技感。整体色调柔和、复古，拒绝高饱和的现代数字色。

## Typography

字体策略采用大号粗体复古衬线体（如 Georgia、Playfair Display）作为标题，传递权威与优雅，参考经典广告海报的字形气质。副标题使用全大写无衬线体，置于彩色矩形块内，形成标签式外观，与块色形成高对比。正文使用干净的几何无衬线体（如 system-ui），保证可读性，字重始终一致。层级关系：Display（64px 展示标题） > H1（44px 页面标题） > H2（28px 副标题/标签块） > Body（16px 正文） > Label（12px 标注）。数据值使用 32px 粗衬线体，呼应标题的复古权威感。

## Layout

采用 balanced 密度与 generous 间距节奏。幻灯片边距 48px，gutter 32px。布局偏好宽幅横向构图，元素通过层叠与重叠营造 2.5D 透视深度。树木简化为棒棒糖形或三角形，建筑简化为矩形块配网格窗户，人物为简单几何图形配极少面部细节。装饰几何元素（太阳光芒、胶囊形云朵、圆点、星星）散布于画面间隙，增添 playful 氛围。

## Elevation & Depth

视觉层次完全扁平（flat quality），通过层叠、重叠与统一描边传达深度。无渐变、无写实阴影、无三维效果。深度感来源于前景/中景/背景的元素层叠关系，以及 2.5D 透视（类等轴测但更自由）带来的空间错觉。所有元素在 z 轴上的关系通过遮挡而非阴影表达，保持填色绘本式的二维纯粹性。

## Shapes

形状语言以简化几何为主，同时保持友好与圆润。大圆角（lg: 24px）用于卡片与主要容器，次要元素使用中等圆角（16px）。所有物体均有闭合黑色描边（填色绘本风格），线条粗细统一。圆角线端，避免尖锐棱角。树木为棒棒糖或三角形，建筑为矩形块，云朵为胶囊形，太阳为圆形配放射线。拒绝复杂的有机曲线，坚持基础几何的可爱简化。

## Components

### Cards
卡片背景使用奶油米白（surface），边框采用深炭灰（neutral）的统一粗细描边，大圆角（24px）与宽松内边距（40px）。卡片可承载全景插画场景，边缘保持清晰的闭合描边，内部填充单一柔和色块。

### Tables
表格使用珊瑚红（primary）作为表头背景，黑色（on-surface）作为表头文字色，交替行使用浅奶油色（#FFF8E7）。表格单元格带有统一的深炭灰边框，表头可使用彩色矩形块样式呼应副标题设计语言。

### Charts
图表网格线使用深炭灰（neutral），数据系列依次使用珊瑚红、薄荷绿、芥末黄、焦橙色、岩蓝。图表元素（柱形、饼图切片、折线）均带有统一的黑色描边，内部为纯色填充，拒绝渐变与平滑曲线。坐标轴与刻度线同样带有描边。

### Icons
图标采用填色绘本风格，闭合黑色描边，内部纯色填充。线条粗细与插画元素保持一致。可包含简化的人物、建筑、自然元素与几何装饰符号。所有图标可爱、几何化，面部细节极少，保持与整体风格一致的语言。

## Do's and Don'ts

- Do: 始终保持一致的描边粗细
- Do: 使用柔和、复古的配色
- Do: 将所有物体简化为基础几何图形
- Do: 通过层叠营造深度
- Do: 添加俏皮的装饰元素
- Don't: 使用渐变或写实阴影
- Don't: 创建写实元素
- Don't: 使用细线或变化不一的线宽
- Don't: 包含复杂精细的插画
- Don't: 添加页码、页脚或徽标
