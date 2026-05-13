---
version: alpha
name: 动画风格
description: 魔幻手绘动画风格，灵感源自经典奇幻插画与故事书美学，适用于教育内容、儿童演示与故事讲述
colors:
  primary: "#F4D03F"
  secondary: "#E8A0BF"
  tertiary: "#87A96B"
  neutral: "#5D4E37"
  surface: "#E8F4FC"
  on-surface: "#2D5A3D"
  error: "#F08080"
  success: "#87A96B"
  warning: "#F4D03F"
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "72px"
    fontWeight: "700"
    lineHeight: "1.1"
  h1:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "48px"
    fontWeight: "700"
    lineHeight: "1.2"
  h2:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "32px"
    fontWeight: "600"
    lineHeight: "1.3"
  body:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: "400"
    lineHeight: "1.7"
  label:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: "500"
    lineHeight: "1.4"
  data-value:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "36px"
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
  sm: "8px"
  md: "16px"
  lg: "24px"
  full: "9999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.tertiary}"
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
  texture: organic
  mood: vibrant
  typography-style: handwritten
  density: minimal
  quality: flat
  spacing-level: generous
---

# 动画风格

## Overview

动画风格以魔幻手绘美学为核心，灵感源自经典迪士尼、吉卜力工作室及欧洲故事书插画。品牌个性温暖、友好且富有想象力，目标受众为儿童教育、创意工作坊与家庭友好型活动。情感基调迷人、怀旧且情感充沛，通过柔和的水彩质感、有机形状与故事书叙事营造沉浸式体验。整体气质拒绝冷酷与机械，拥抱有机与生命感。

## Colors

色板以柔和天蓝（#E8F4FC）为基底表面色，营造开放、梦幻的视觉氛围。备选背景使用暖奶油色（#FFF8E7），为不同页面提供温和的色温变化。主强调色金黄（#F4D03F）承担魔法与高亮语义，玫瑰粉（#E8A0BF）传递温暖与魅力，鼠尾草绿（#87A96B）用于自然元素。深森林绿（#2D5A3D）作为表面文字色，与暖棕（#5D4E37）形成温和对比。珊瑚色（#F08080）用于错误状态，整体色调避免冷色，保持邀请感。

## Typography

字体策略采用 whimsical 衬线体或装饰性手写风格作为标题字体，略带弧度与有机感，传递童话书标题般的温暖性格。正文使用圆润无衬线体或休闲手写风格，在保持故事书美学的同时确保可读性。层级关系：Display（72px 展示标题） > H1（48px 页面标题） > H2（32px 章节标题） > Body（18px 正文） > Label（14px 标签），数据值使用 36px 粗衬线体增强视觉分量。行高宽松，给予文字充分的呼吸空间。

## Layout

采用 minimal 密度与 generous 间距节奏。幻灯片边距宽松（48px），内容区域留有充足的呼吸空间。元素通过前景/背景层叠营造故事书般的场景深度。中央插画角色作为视觉焦点，小型陪伴生物与魔法悬浮物体围绕其分布。避免密集的网格堆叠，让装饰元素（星星、闪光、花朵、树叶）自然散布于画面边缘。

## Elevation & Depth

视觉层次通过层叠关系与柔和阴影传达，而非强烈的投影。扁平质感（flat quality）配合水彩洗染纹理，元素之间以前景/背景的前后关系建立深度。装饰性的星星、闪光与悬浮物体在 z 轴上浮动，营造轻柔的纵深感。无玻璃拟态或新拟态效果，深度感来源于绘画的透视法则而非数字阴影。

## Shapes

形状语言以有机、柔和为主。大圆角（lg: 24px）用于卡片与容器，模拟绘本插画的温柔轮廓。避免生硬的几何形状与锐利棱角。主题化内容容器（如箱子、挎包、卷轴盒）采用手绘曲线，整体轮廓充满故事感。线条末端圆润，拒绝机械直角。

## Components

### Cards
卡片背景使用柔和天蓝（surface），边框采用鼠尾草绿（tertiary），大圆角（24px）与宽松内边距（40px）。卡片可承载故事书场景或角色插画，边缘可带有轻微的水彩溢出效果，避免锐利的裁切感。

### Tables
表格使用金黄色（primary）作为表头背景，深森林绿（on-surface）作为表头文字色，交替行使用暖奶油色（#FFF8E7）降低视觉疲劳。表格在此风格中使用频率较低，出现时需保持简洁与装饰性平衡，避免冰冷的网格感。

### Charts
图表网格线使用暖棕色（neutral），数据系列依次使用金黄、玫瑰粉、鼠尾草绿、天蓝、珊瑚色。图表应以插画化方式呈现，元素可带有手绘描边与填充，避免冷酷的默认样式。

### Icons
图标采用手绘风格，线条柔和、带有轻微的粗细变化。可包含星星、花朵、树叶、魔法光球等叙事性符号。所有图标应维持故事书的 whimsical 气质，拒绝几何精确的人机界面符号。

## Do's and Don'ts

- Do: 创建温暖、诱人的构图
- Do: 使用柔和边缘和绘画质感
- Do: 包含迷人的角色插画
- Do: 添加魔法装饰点缀
- Do: 保持故事书叙事感
- Don't: 使用生硬的几何形状
- Don't: 创建黑暗或恐吓性的图像
- Don't: 添加照片级写实元素
- Don't: 使用冷色调配色
- Don't: 添加幻灯片编号、页脚或标志
