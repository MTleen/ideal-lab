# Dimension: Texture (质感)

5 种质感选项，定义页面的背景纹理和视觉触感。

---

## 1. Clean — 纯净

**视觉描述**：
无纹理的纯净背景，追求极致的简洁和现代感。背景使用纯色或极浅的渐变，不添加任何噪点、纹理或图案。

**背景处理**：
```
Background: 纯色 #FFFFFF 或单色渐变
Overlay: 无
Noise: 无
Pattern: 无
```

**适用场景**：
- 极简风格演示
- 科技/互联网公司
- 高端品牌展示
- 数据密集型报告

**搭配建议**：
- Mood: professional / cool / neutral
- Typography: geometric / editorial
- Density: minimal / balanced

---

## 2. Grid — 网格

**视觉描述**：
细微的网格线背景，营造技术制图和蓝图的感觉。网格线极浅，不干扰前景内容，但为页面增加结构感和秩序感。

**背景处理**：
```
Background: #FFFFFF 或 #F8F9FA
Grid Pattern: 细线网格
Grid Color: #E8E8E8 或 #F0F0F0
Grid Size: 20px × 20px 或 40px × 40px
Opacity: 30-50%
```

**CSS 参考**：
```css
background-image:
  linear-gradient(#E8E8E8 1px, transparent 1px),
  linear-gradient(90deg, #E8E8E8 1px, transparent 1px);
background-size: 40px 40px;
```

**适用场景**：
- 技术架构展示
- 蓝图风格
- 系统设计
- 工程类演示

**搭配建议**：
- Mood: professional / cool
- Typography: technical / geometric
- Density: balanced / dense

---

## 3. Organic — 有机

**视觉描述**：
柔和的有机形状和渐变，营造自然流动的感觉。使用不规则的色块、模糊边缘的渐变斑点，打破几何网格的僵硬感。

**背景处理**：
```
Background: 柔和渐变底色
Shapes: 椭圆形渐变色块 (blur 60-100px)
Colors: 浅色系 (Primary 和 Secondary 的极浅变体)
Opacity: 15-30%
Position: 随机但平衡分布
```

**CSS 参考**：
```css
background:
  radial-gradient(ellipse at 20% 50%, rgba(33,150,243,0.15) 0%, transparent 50%),
  radial-gradient(ellipse at 80% 20%, rgba(156,39,176,0.1) 0%, transparent 50%),
  #FFFFFF;
```

**适用场景**：
- 品牌展示
- 创意提案
- 教育/培训
- 生活方式

**搭配建议**：
- Mood: warm / vibrant
- Typography: humanist / handwritten
- Density: minimal / balanced

---

## 4. Pixel — 像素

**视觉描述**：
像素化的网格纹理，营造复古游戏和数字艺术的感觉。使用方块图案和明显的像素边界。

**背景处理**：
```
Background: 深色底 (#1A1A2E 或 #0F0F23)
Pixel Grid: 8px × 8px 或 16px × 16px 方块
Pixel Colors: 主题色的暗色变体
Opacity: 10-20% (作为纹理)
或 40-60% (作为主要视觉元素)
```

**CSS 参考**：
```css
background-image:
  linear-gradient(45deg, rgba(33,150,243,0.1) 25%, transparent 25%),
  linear-gradient(-45deg, rgba(33,150,243,0.1) 25%, transparent 25%),
  linear-gradient(45deg, transparent 75%, rgba(33,150,243,0.1) 75%),
  linear-gradient(-45deg, transparent 75%, rgba(33,150,243,0.1) 75%);
background-size: 16px 16px;
background-position: 0 0, 0 8px, 8px -8px, -8px 0;
```

**适用场景**：
- 游戏行业
- 像素风格设计
- 复古数字主题
- 创意/年轻化品牌

**搭配建议**：
- Mood: vibrant / dark
- Typography: geometric / technical
- Density: balanced / dense

---

## 5. Paper — 纸张

**视觉描述**：
模拟真实纸张的质感，带有细微的纤维纹理和温暖的底色。营造手工艺、传统和文化的感觉。

**背景处理**：
```
Background: #FAFAF5 (暖白) 或 #F5F0E8 (米色)
Texture: 细微噪点 (noise 2-3%)
Fiber: 纤维纹理 (optional SVG pattern)
Edge: 可选的轻微纸张边缘阴影
Tone: 偏暖色调
```

**CSS 参考**：
```css
background-color: #FAFAF5;
/* 使用 SVG noise filter 模拟纸张纹理 */
```

**适用场景**：
- 论文/学术演示
- 教育/培训
- 手绘风格
- 水彩风格
- 复古报纸风
- 文化/人文主题

**搭配建议**：
- Mood: warm / neutral
- Typography: editorial / handwritten / humanist
- Density: balanced

---

## 质感选择指南

| 风格关键词 | 推荐质感 |
|------------|----------|
| 现代、极简、科技 | Clean |
| 技术、蓝图、工程 | Grid |
| 自然、柔和、品牌 | Organic |
| 游戏、复古、数字 | Pixel |
| 传统、人文、学术 | Paper |
