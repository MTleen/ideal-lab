# AI 图像生成指南

## 提示词模板

### Background（背景图）

```
{subject}, abstract background, {primary_color} and {secondary_color} gradient,
low contrast details, soft shapes, reserve center area for text overlay,
professional quality, {canvas_ratio} aspect ratio
```

**要点**：
- 抽象为主，避免具象内容干扰文字
- 使用 design-spec 的主色/辅色
- 低对比度细节，确保文字可读
- 预留中心区域用于文字叠加

### Photography（实景照片）

```
{subject}, professional photography, natural lighting, {composition},
shallow depth of field, high resolution, {canvas_ratio} aspect ratio
```

**要点**：
- 真实感，非 AI 过度渲染
- 自然光影
- 与内容主题直接相关

### Illustration（插画）

```
{subject}, flat illustration style, vector graphics, {color_palette},
clean lines, minimalist design, white background, {canvas_ratio} aspect ratio
```

**要点**：
- 扁平矢量风格
- 配色与 design-spec 一致
- 简洁线条，避免过度细节

### Diagram（图表）

```
{subject}, technical diagram, clean schematic style, {color_scheme},
labeled components, arrows showing flow, minimalist, {canvas_ratio} aspect ratio
```

**要点**：
- 技术图表风格
- 清晰的线条和标注
- 流程方向明确

### Decorative Pattern（装饰纹理）

```
{subject}, subtle decorative pattern, {color_scheme}, low contrast,
geometric shapes, seamless texture, background element, {canvas_ratio} aspect ratio
```

**要点**：
- 微妙含蓄，不抢夺注意力
- 辅助性质
- 与整体风格协调

## 纵横比指南

| 目标用途 | 推荐比例 | 说明 |
|---------|---------|------|
| PPT 16:9 背景 | 16:9 (1.78:1) | 全页背景 |
| PPT 16:9 插图 | 4:3 或 3:2 | 内容区域配图 |
| PPT 4:3 背景 | 4:3 (1.33:1) | 全页背景 |
| 小红书 | 3:4 | 竖版内容 |
| Story | 9:16 | 竖版全屏 |

## 风格统一策略

同一演示文稿的所有生成图像应保持：
1. **色彩统一**：使用 design-spec 的配色方案
2. **风格统一**：同一类型图像使用相同的风格关键词
3. **质量统一**：相同的质量后缀（如 "professional quality, high resolution"）

## 负面提示词

通用负面提示词（避免不希望出现的内容）：
```
text, watermark, logo, blurry, low quality, distorted, oversaturated,
cluttered, dark shadows, harsh contrast
```

背景图额外负面提示词：
```
people, faces, specific objects, readable text, busy details
```
