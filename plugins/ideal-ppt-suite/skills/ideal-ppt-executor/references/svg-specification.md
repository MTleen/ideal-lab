# SVG 技术规范 — PPT 兼容可编辑子集

> 本规范定义了生成 PPT 兼容 SVG 时必须遵守的全部技术规则。

## 1. 画布与根元素

### 1.1 viewBox 规范

```xml
<!-- 16:9 标准画布（默认） -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">

<!-- 4:3 画布 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720">
```

- viewBox 必须与 design-spec 中定义的画布尺寸一致
- 不设置 width/height 属性，让 PPT 自适应缩放
- xmlns 声明必须包含

### 1.2 背景元素

```xml
<!-- 背景必须使用 rect 覆盖整个画布 -->
<rect width="1280" height="720" fill="#FFFFFF"/>
```

- 背景色从 design-spec 获取
- 背景矩形必须是 SVG 的第一个子元素（ defs 之后）

## 2. 禁止特性清单（Banned Features）

以下 SVG 特性**不可协商**，严禁在任何生成内容中使用：

### 2.1 禁止的元素（Banned Elements）

| 元素 | 原因 |
|------|------|
| `<filter>` 及所有 `fe*` 原语 | PPT 不支持 SVG filter，导致渲染失败 |
| `<mask>` | PPT 兼容性差，可能丢失遮罩内容 |
| `<clipPath>` | PPT 不支持 SVG clip，内容会被裁切异常 |
| `<pattern>` | PPT 不支持 SVG pattern 填充 |
| `<foreignObject>` | PPT 完全不支持，内容不渲染 |
| `<style>` | PPT 忽略内嵌/外部 CSS |
| `<symbol>` + `<use>` | 部分版本 PPT 不支持 |
| `<textPath>` | PPT 不支持文字沿路径排列 |
| `<animate>` / `<animateTransform>` | PPT 不执行 SVG 动画 |
| `<script>` | 安全风险，PPT 不执行脚本 |
| `<marker>` | PPT 不支持 SVG marker |
| `<iframe>` | 安全风险，不适用 |
| `<cursor>` | 无意义，PPT 不使用 |
| `<view>` | PPT 不支持 |

### 2.2 禁止的属性（Banned Attributes）

| 属性 | 原因 |
|------|------|
| `filter="url(#...)"` | 关联 banned filter 元素 |
| `mask="url(#...)"` | 关联 banned mask 元素 |
| `clip-path="url(#...)"` | 关联 banned clipPath 元素 |
| `marker-start/mid/end` | 关联 banned marker 元素 |
| `class="..."` | PPT 不处理 CSS class |
| `style="..."` | 内联 style 仅允许简单属性，避免复杂声明 |

### 2.3 禁止的 CSS 特性

| 特性 | 原因 |
|------|------|
| `@font-face` | PPT 无法加载外部字体 |
| 外部 CSS 文件引用 | PPT 不读取外部样式表 |
| CSS 变量 (`var(--x)`) | PPT 不支持 |
| CSS calc() / clamp() | PPT 不支持 |

## 3. PPT 兼容替代方案

### 3.1 透明度

```
禁止: fill="rgba(26, 86, 219, 0.8)"
替代: fill="#1A56DB" fill-opacity="0.8"

禁止: stroke="rgba(0, 0, 0, 0.3)"
替代: stroke="#000000" stroke-opacity="0.3"
```

### 3.2 群组透明度

```
禁止:
<g opacity="0.5">
  <rect fill="#1A56DB" .../>
  <text fill="#FFFFFF" ...>文字</text>
</g>

替代:
<g>
  <rect fill="#1A56DB" fill-opacity="0.5" .../>
  <text fill="#FFFFFF" fill-opacity="0.5" ...>文字</text>
</g>
```

每个子元素单独设置 `fill-opacity` 或 `stroke-opacity`。

### 3.3 图片透明度（Image Opacity）

```
禁止: <image opacity="0.5" .../>

替代: 在图片上方叠加一个半透明白色矩形
<image href="../images/photo.png" .../>
<rect fill="#FFFFFF" fill-opacity="0.5" x="..." y="..." width="..." height="..."/>
```

### 3.4 箭头（Arrows）

```
禁止: marker-end="url(#arrowhead)"

替代: 在线条末端手动绘制三角形
<polygon points="x1,y1 x2,y2 x3,y3" fill="#1A56DB"/>
```

### 3.5 文字换行（Line Breaks）

```
禁止: <foreignObject><p>第一行<br/>第二行</p></foreignObject>

替代: 使用 tspan
<text font-family="Microsoft YaHei" font-size="20" fill="#1E293B">
  <tspan x="40" y="100">第一行文字</tspan>
  <tspan x="40" dy="28">第二行文字</tspan>
</text>
```

### 3.6 卡片阴影（Card Shadow）

```
禁止: filter="url(#dropShadow)"

替代: 使用偏移的深色半透明矩形
<!-- shadow layer -->
<rect x="42" y="62" width="300" height="200" rx="12" ry="12"
      fill="#000000" fill-opacity="0.08"/>
<!-- card layer -->
<rect x="40" y="60" width="300" height="200" rx="12" ry="12"
      fill="#FFFFFF"/>
```

## 4. 允许的元素和属性

### 4.1 允许的元素

| 元素 | 用途 | 常用属性 |
|------|------|----------|
| `<svg>` | 根元素 | viewBox, xmlns |
| `<defs>` | 定义区 | id |
| `<linearGradient>` | 线性渐变 | id, x1, y1, x2, y2 |
| `<stop>` | 渐变停靠点 | offset, stop-color, stop-opacity |
| `<rect>` | 矩形 | x, y, width, height, rx, ry, fill, stroke, fill-opacity, stroke-opacity |
| `<circle>` | 圆形 | cx, cy, r, fill, stroke, fill-opacity, stroke-opacity |
| `<ellipse>` | 椭圆 | cx, cy, rx, ry, fill, stroke |
| `<line>` | 直线 | x1, y1, x2, y2, stroke, stroke-width |
| `<polyline>` | 折线 | points, fill, stroke, stroke-width |
| `<polygon>` | 多边形 | points, fill, stroke |
| `<text>` | 文本 | x, y, font-family, font-size, font-weight, fill, text-anchor |
| `<tspan>` | 文本片段 | x, dy, font-size, font-weight, fill |
| `<g>` | 分组 | id（仅用于标识） |
| `<image>` | 图片 | href（相对路径）, x, y, width, height, preserveAspectRatio |

### 4.2 允许的属性

- 定位：`x`, `y`, `dx`, `dy`, `cx`, `cy`, `rx`, `ry`, `r`
- 尺寸：`width`, `height`
- 填充：`fill`, `fill-opacity`, `fill-rule`
- 描边：`stroke`, `stroke-width`, `stroke-opacity`, `stroke-linecap`, `stroke-linejoin`, `stroke-dasharray`
- 字体：`font-family`, `font-size`, `font-weight`, `font-style`, `text-anchor`, `dominant-baseline`
- 其他：`viewBox`, `xmlns`, `preserveAspectRatio`, `points`
- 渐变：`offset`, `stop-color`, `stop-opacity`

## 5. 渐变使用规范

```xml
<!-- 正确：在 defs 中定义渐变 -->
<defs>
  <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1A56DB"/>
    <stop offset="100%" stop-color="#7C3AED"/>
  </linearGradient>
</defs>

<!-- 使用渐变 -->
<rect width="1280" height="720" fill="url(#bg-gradient)"/>
```

规则：
- 渐变只在 `<defs>` 中定义
- 仅使用 `<linearGradient>`
- 禁止 `<radialGradient>`（PPT 兼容性不稳定）
- `id` 只用于渐变引用，不用于 CSS 样式选择器

## 6. 字体规范

### 6.1 系统字体

```
标题: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif
正文: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif
英文: system-ui, -apple-system, "Segoe UI", sans-serif
代码: "SF Mono", "Consolas", "Monaco", monospace
数字: "DIN Alternate", "Helvetica Neue", system-ui, sans-serif
```

### 6.2 字号规范

| 类型 | 字号范围 | 建议 |
|------|----------|------|
| 页面标题 | 36px - 48px | 40px |
| 章节标题 | 28px - 36px | 32px |
| 小标题 | 22px - 28px | 24px |
| 正文 | 18px - 22px | 20px |
| 辅助文字 | 14px - 16px | 14px |
| 标注/脚注 | 12px - 14px | 12px |

### 6.3 字重

- 标题：`font-weight="600"` 或 `"bold"`
- 正文：`font-weight="400"` 或 `"normal"`
- 强调：`font-weight="500"` 或 `"600"`

## 7. 颜色规范

### 7.1 格式要求

- 所有颜色使用 HEX 格式：`#RRGGBB`
- 透明度使用独立属性：`fill-opacity="0.8"`
- **禁止** `rgba()`、`hsla()`、颜色名称（如 `red`）

### 7.2 配色示例

```xml
<!-- 主色 -->
<rect fill="#1A56DB"/>
<!-- 辅色 -->
<rect fill="#7C3AED"/>
<!-- 强调色 -->
<rect fill="#F59E0B"/>
<!-- 深色背景上的白色文字 -->
<text fill="#FFFFFF"/>
<!-- 浅色背景上的深色文字 -->
<text fill="#1E293B"/>
<!-- 辅助文字 -->
<text fill="#64748B"/>
```

## 8. 图片使用规范

```xml
<!-- 正确：相对路径引用 -->
<image href="../images/photo.png"
       x="40" y="60" width="400" height="300"
       preserveAspectRatio="xMidYMid slice"/>

<!-- 正确：项目内图片 -->
<image href="../images/logo.png"
       x="40" y="20" width="120" height="40"
       preserveAspectRatio="xMidYMid meet"/>
```

规则：
- 只使用相对路径 `../images/xxx.png`
- 禁止绝对 URL
- 禁止 data URI
- 必须设置 `preserveAspectRatio`
- 建议使用 `xMidYMid slice`（填满）或 `xMidYMid meet`（等比）

## 9. SVG 文件结构模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <!-- 定义区 -->
  <defs>
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A56DB"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1280" height="720" fill="url(#bg-gradient)"/>

  <!-- 内容区域 -->
  <g>
    <!-- 卡片阴影 -->
    <rect x="42" y="62" width="580" height="280" rx="12" ry="12"
          fill="#000000" fill-opacity="0.08"/>
    <!-- 卡片主体 -->
    <rect x="40" y="60" width="580" height="280" rx="12" ry="12"
          fill="#FFFFFF"/>

    <!-- 标题文字 -->
    <text x="60" y="100" font-family="Microsoft YaHei" font-size="24"
          font-weight="600" fill="#1E293B">卡片标题</text>

    <!-- 正文 -->
    <text font-family="Microsoft YaHei" font-size="18" fill="#64748B">
      <tspan x="60" y="140">描述文字第一行</tspan>
      <tspan x="60" dy="28">描述文字第二行</tspan>
    </text>
  </g>
</svg>
```

## 10. 常见错误及修正

| 错误写法 | 正确写法 | 说明 |
|----------|----------|------|
| `fill="rgba(0,0,0,0.5)"` | `fill="#000000" fill-opacity="0.5"` | 颜色格式 |
| `<g opacity="0.8">` | 每个子元素加 `fill-opacity="0.8"` | 群组透明度 |
| `<style>.cls{...}</style>` | 内联属性 `fill="#1A56DB"` | 样式方式 |
| `font-size: 20px` | `font-size="20"` | 属性语法 |
| `<br/>` in text | `<tspan dy="28">` | 换行方式 |
| `<img src="...">` | `<image href="...">` | 图片引用 |
| `filter="drop-shadow()"` | 手动绘制阴影矩形 | 阴影效果 |
