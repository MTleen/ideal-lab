# 混合渲染指南 — HTML + 内嵌 SVG + AI 图片

> 本指南说明如何在 HTML 幻灯片中混合使用三种渲染方式，实现最佳视觉效果和信息密度。

## 1. 渲染方式选择决策

```
需要渲染什么？
├─ 文字/列表/卡片/数据 → HTML+CSS（默认）
├─ 流程图/架构图/示意图 → 内嵌 SVG
├─ 配图/照片/插画 → AI 生成图片（<img>）
└─ 复杂图表（甘特图/时间线） → 内嵌 SVG
```

## 2. HTML+CSS 渲染（默认，优先使用）

适用于：文字排版、卡片布局、数据展示、列表、表格、进度条

### 优势
- CSS Grid/Flexbox 布局，精确定位
- 中文字体支持优秀（system font stack）
- 自动文字换行，无需手动计算 tspan
- CSS 变量实现全局主题
- box-shadow / border-radius 等现代 CSS

### 示例：数据仪表盘

```html
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 20px;">
  <div class="stat-card">
    <div class="stat-number">99.9%</div>
    <div class="stat-label">服务可用性 SLA</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">50M+</div>
    <div class="stat-label">月活跃用户</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">42%</div>
    <div class="stat-label">同比增长</div>
    <div class="stat-change up">↑ 12% vs Q3</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">2.3s</div>
    <div class="stat-label">平均响应时间</div>
  </div>
</div>
```

## 3. 内嵌 SVG 渲染

适用于：流程图、架构图、概念关系图、时间线、技术示意图

### 使用规则

1. SVG 只用于**纯图形**，文字优先用 HTML
2. SVG 内嵌在 `<div>` 容器中，通过 CSS 控制大小
3. SVG 使用 `viewBox` 保持矢量可缩放
4. SVG 内可引用 CSS 变量（`var(--primary)`）

### 内嵌 SVG 规范

```html
<div class="diagram" style="width: 100%; display: flex; justify-content: center;">
  <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg"
       style="width: 100%; max-height: 300px;">
    <!-- 渐变定义 -->
    <defs>
      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#1A56DB"/>
        <stop offset="100%" stop-color="#7C3AED"/>
      </linearGradient>
    </defs>

    <!-- 流程节点 -->
    <rect x="0" y="100" width="160" height="80" rx="8" fill="#1A56DB"/>
    <text x="80" y="145" text-anchor="middle" fill="white"
          font-size="14" font-family="Microsoft YaHei">数据采集</text>

    <!-- 箭头 -->
    <line x1="170" y1="140" x2="210" y2="140" stroke="#1A56DB" stroke-width="2"/>
    <polygon points="210,135 220,140 210,145" fill="#1A56DB"/>

    <!-- 更多节点... -->
  </svg>
</div>
```

### SVG 内允许的元素

| 元素 | 用途 |
|------|------|
| `<rect>` | 矩形（圆角矩形） |
| `<circle>` / `<ellipse>` | 圆/椭圆 |
| `<line>` / `<polyline>` / `<polygon>` | 线条/多边形 |
| `<path>` | 贝塞尔曲线、复杂路径 |
| `<text>` / `<tspan>` | 图形内标注文字 |
| `<linearGradient>` / `<stop>` | 渐变填充 |
| `<defs>` | 定义区 |
| `<g>` | 分组 |
| `<image>` | 嵌入图片（相对路径） |

### SVG 内禁止的元素

| 禁止项 | 原因 |
|--------|------|
| `<filter>` | 截图时可能不渲染 |
| `<mask>` / `<clipPath>` | 截图兼容性差 |
| `<foreignObject>` | 无头浏览器支持不一致 |
| `<animate>` | 截图无法捕获 |
| `<script>` | 安全风险 |

### 示例：三层架构图

```html
<div class="card" style="grid-column: 1 / -1;">
  <div class="card-title">系统架构</div>
  <svg viewBox="0 0 1100 400" xmlns="http://www.w3.org/2000/svg"
       style="width: 100%;">
    <!-- 第一层：接入层 -->
    <rect x="50" y="20" width="1000" height="100" rx="8"
          fill="#1A56DB" fill-opacity="0.08"/>
    <text x="70" y="50" font-size="16" font-weight="600" fill="#1A56DB"
          font-family="Microsoft YaHei">接入层</text>
    <rect x="70" y="65" width="200" height="40" rx="6" fill="#1A56DB"/>
    <text x="170" y="91" text-anchor="middle" fill="white"
          font-size="13" font-family="Microsoft YaHei">API Gateway</text>
    <rect x="290" y="65" width="200" height="40" rx="6" fill="#1A56DB"/>
    <text x="390" y="91" text-anchor="middle" fill="white"
          font-size="13" font-family="Microsoft YaHei">Load Balancer</text>
    <rect x="510" y="65" width="200" height="40" rx="6" fill="#1A56DB"/>
    <text x="610" y="91" text-anchor="middle" fill="white"
          font-size="13" font-family="Microsoft YaHei">CDN</text>

    <!-- 向下箭头 -->
    <line x1="550" y1="125" x2="550" y2="155" stroke="#64748B" stroke-width="2"/>
    <polygon points="545,155 550,165 555,155" fill="#64748B"/>

    <!-- 第二层：业务层 -->
    <rect x="50" y="170" width="1000" height="100" rx="8"
          fill="#7C3AED" fill-opacity="0.08"/>
    <text x="70" y="200" font-size="16" font-weight="600" fill="#7C3AED"
          font-family="Microsoft YaHei">业务层</text>
    <!-- ...更多节点... -->

    <!-- 第三层：数据层 -->
    <rect x="50" y="320" width="1000" height="80" rx="8"
          fill="#F59E0B" fill-opacity="0.08"/>
    <!-- ...更多节点... -->
  </svg>
</div>
```

## 4. AI 生成图片

适用于：封面背景、产品截图、团队照片、场景插图

### 使用方式

```html
<div style="grid-column: 1 / 2;">
  <img src="../images/01-hero.png"
       alt="产品首页展示"
       style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;">
</div>
```

### 图片规格

| 用途 | 推荐尺寸 | object-fit |
|------|---------|-----------|
| 全宽 Banner | 1200×400 | `cover` |
| 卡片内配图 | 400×300 | `cover` |
| 侧边栏图 | 300×500 | `cover` |
| Logo/Icon | 80×80 | `contain` |

### 路径规则

- 相对于 `html_output/` 目录：`../images/NN-name.png`
- 禁止绝对 URL
- 禁止 data URI

## 5. 混合布局示例

### Hero + SVG 架构图 + 3 列数据

```html
<body>
  <div class="page-header"><h1>技术架构</h1></div>
  <div class="content" style="display: grid; grid-template-rows: 1fr auto; gap: 20px;">
    <!-- 上部：SVG 架构图 -->
    <div class="card">
      <svg viewBox="0 0 1100 280" ...>
        <!-- 架构图 SVG -->
      </svg>
    </div>
    <!-- 下部：3 列 KPI 数据 -->
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
      <div class="stat-card card">
        <div class="stat-number">99.9%</div>
        <div class="stat-label">系统可用性</div>
      </div>
      <div class="stat-card card">
        <div class="stat-number">&lt;50ms</div>
        <div class="stat-label">P99 延迟</div>
      </div>
      <div class="stat-card card">
        <div class="stat-number">10K+</div>
        <div class="stat-label">并发连接</div>
      </div>
    </div>
  </div>
</body>
```

### 左图右文 + AI 配图

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <!-- 左：AI 生成图片 -->
  <div>
    <img src="../images/03-product.png" alt="产品界面"
         style="width:100%; height:100%; object-fit:cover; border-radius:12px;">
  </div>
  <!-- 右：HTML 文字内容 -->
  <div class="card">
    <div class="card-title">核心功能</div>
    <ul class="content-list">
      <li>实时数据分析引擎</li>
      <li>智能告警与根因定位</li>
      <li>多维度交叉查询</li>
      <li>自定义仪表盘与报告</li>
    </ul>
  </div>
</div>
```

## 6. 截图兼容性注意事项

HTML 最终会通过无头浏览器截图为 PNG/PPTX，注意：

- CSS 变量在无头浏览器中正常支持
- `backdrop-filter`（毛玻璃效果）截图中可能不生效，避免使用
- `@font-face` 需要系统安装对应字体，优先使用 system font stack
- `position: sticky` 无效（单页固定尺寸），使用 absolute 或 grid 布局
- 确保 `body` 设置了固定 `width: 1280px; height: 720px`
- `overflow: hidden` 防止内容溢出
