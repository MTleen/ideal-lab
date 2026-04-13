# Bento Grid 布局 SVG 渲染指南

> 本指南描述如何在 SVG 中渲染 Bento Grid 风格的卡片布局，确保 PPT 兼容性和视觉一致性。

## 1. 设计原则

Bento Grid 的核心思想是：将内容组织为不同大小的矩形卡片，形成类似便当盒的网格布局。

关键原则：
- **一致性**：所有卡片使用相同的圆角、阴影、内边距
- **对齐**：卡片边缘严格对齐，间距统一
- **层次**：通过卡片大小区分内容主次
- **留白**：卡片间距保持均匀，避免拥挤感

## 2. 基础卡片元素

### 2.1 卡片结构

每张卡片由两层组成：阴影层 + 主体层。

```xml
<!-- 卡片阴影（偏移 2px，半透明黑色） -->
<rect x="42" y="62" width="580" height="280" rx="12" ry="12"
      fill="#000000" fill-opacity="0.06"/>

<!-- 卡片主体 -->
<rect x="40" y="60" width="580" height="280" rx="12" ry="12"
      fill="#FFFFFF"/>
```

### 2.2 卡片参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 圆角 | `rx="12" ry="12"` | 统一圆角半径 |
| 间距 | 20px - 24px | 卡片之间的间距 |
| 内边距 | 20px - 24px | 卡片内容到卡片边缘的距离 |
| 阴影偏移 | 2px | 阴影与主体的偏移量 |
| 阴影透明度 | 0.06 - 0.10 | 阴影深度 |
| 背景色 | `#FFFFFF` | 默认白色卡片 |

### 2.3 卡片内容布局

```xml
<!-- 卡片组 -->
<g>
  <!-- 阴影 -->
  <rect x="42" y="62" width="580" height="280" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <!-- 主体 -->
  <rect x="40" y="60" width="580" height="280" rx="12" ry="12"
        fill="#FFFFFF"/>

  <!-- 卡片头部（标题） -->
  <text x="60" y="96" font-family="Microsoft YaHei" font-size="20"
        font-weight="600" fill="#1E293B">卡片标题</text>

  <!-- 分隔线（可选） -->
  <line x1="60" y1="108" x2="600" y2="108" stroke="#E2E8F0" stroke-width="1"/>

  <!-- 卡片正文 -->
  <text font-family="Microsoft YaHei" font-size="16" fill="#64748B">
    <tspan x="60" y="136">描述文字第一行</tspan>
    <tspan x="60" dy="24">描述文字第二行</tspan>
    <tspan x="60" dy="24">描述文字第三行</tspan>
  </text>
</g>
```

## 3. 常用布局模式

以下提供基于 1280x720 画布的坐标参考。

### 3.1 两列等宽布局（2-Column Equal）

```
+-------------------+ gap +-------------------+
|                   |     |                   |
|    Card A         |     |    Card B         |
|    580×560        |     |    580×560        |
|                   |     |                   |
+-------------------+     +-------------------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| A | 40 | 80 | 580 | 560 |
| B | 660 | 80 | 580 | 560 |

### 3.2 三列等宽布局（3-Column Equal）

```
+----------+ gap +----------+ gap +----------+
|          |     |          |     |          |
|  Card A  |     |  Card B  |     |  Card C  |
|  380×560 |     |  380×560 |     |  380×560 |
|          |     |          |     |          |
+----------+     +----------+     +----------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| A | 40 | 80 | 380 | 560 |
| B | 440 | 80 | 380 | 560 |
| C | 840 | 80 | 380 | 560 |

### 3.3 Hero + Grid（主角卡 + 网格）

```
+-------------------------------------------+
|                                           |
|            Hero Card                      |
|            1200×280                       |
|                                           |
+-------------------------------------------+
+----------+ gap +----------+ gap +----------+
|          |     |          |     |          |
|  Card B  |     |  Card C  |     |  Card D  |
|  380×260 |     |  380×260 |     | 380×260  |
|          |     |          |     |          |
+----------+     +----------+     +----------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| Hero | 40 | 60 | 1200 | 280 |
| B | 40 | 360 | 380 | 280 |
| C | 440 | 360 | 380 | 280 |
| D | 840 | 360 | 380 | 280 |

### 3.4 侧边栏布局（Sidebar + Content）

```
+----------+ gap +---------------------------+
|          |     |                           |
|  Sidebar |     |     Main Content          |
|  300×560 |     |     920×560               |
|          |     |                           |
+----------+     +---------------------------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| Sidebar | 40 | 80 | 300 | 560 |
| Main | 360 | 80 | 880 | 560 |

### 3.5 不对称两列（Asymmetric 2-Column）

```
+----------------+ gap +---------------------------+
|                |     |                           |
|   Card A       |     |     Card B                |
|   400×560      |     |     820×560               |
|                |     |                           |
+----------------+     +---------------------------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| A | 40 | 80 | 400 | 560 |
| B | 460 | 80 | 780 | 560 |

### 3.6 四宫格布局（2x2 Grid）

```
+-------------------+ gap +-------------------+
|                   |     |                   |
|    Card A         |     |    Card B         |
|    580×260        |     |    580×260        |
|                   |     |                   |
+-------------------+     +-------------------+
+-------------------+     +-------------------+
|                   |     |                   |
|    Card C         |     |    Card D         |
|    580×260        |     |    580×260        |
|                   |     |                   |
+-------------------+     +-------------------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| A | 40 | 80 | 580 | 260 |
| B | 660 | 80 | 580 | 260 |
| C | 40 | 360 | 580 | 260 |
| D | 660 | 360 | 580 | 260 |

### 3.7 复杂混合布局（Complex Mix）

```
+-------------------+ gap +-------------------+
|                   |     |                   |
|    Card A         |     |    Card B         |
|    580×380        |     |    580×180        |
|                   |     +-------------------+
|                   |     +-------------------+
+-------------------+     |    Card C         |
+-------------------+     |    580×180        |
|    Card D         |     +-------------------+
|    580×160        |
+-------------------+
```

| 卡片 | x | y | width | height |
|------|-----|-----|-------|--------|
| A | 40 | 80 | 580 | 380 |
| B | 660 | 80 | 580 | 180 |
| C | 660 | 280 | 580 | 180 |
| D | 40 | 480 | 580 | 160 |

## 4. 彩色卡片变体

除了白色卡片，可以使用主色调的浅色变体作为卡片背景：

```xml
<!-- 主色浅色变体卡片 -->
<rect x="40" y="60" width="580" height="280" rx="12" ry="12"
      fill="#1A56DB" fill-opacity="0.08"/>

<!-- 强调色卡片 -->
<rect x="40" y="60" width="580" height="280" rx="12" ry="12"
      fill="#F59E0B" fill-opacity="0.10"/>

<!-- 深色卡片（深色主题） -->
<rect x="40" y="60" width="580" height="280" rx="12" ry="12"
      fill="#1E293B"/>
<!-- 深色卡片上的文字 -->
<text fill="#FFFFFF">...</text>
```

## 5. 完整示例

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <!-- 背景 -->
  <rect width="1280" height="720" fill="#F8FAFC"/>

  <!-- 页面标题 -->
  <text x="40" y="48" font-family="Microsoft YaHei" font-size="28"
        font-weight="600" fill="#1E293B">产品功能概览</text>

  <!-- Card A: Hero（大卡） -->
  <rect x="42" y="82" width="582" height="300" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <rect x="40" y="80" width="582" height="300" rx="12" ry="12"
        fill="#FFFFFF"/>
  <text x="64" y="118" font-family="Microsoft YaHei" font-size="22"
        font-weight="600" fill="#1A56DB">核心能力</text>
  <text font-family="Microsoft YaHei" font-size="16" fill="#64748B">
    <tspan x="64" y="152">智能分析引擎，覆盖全链路数据</tspan>
    <tspan x="64" dy="26">支持实时计算与历史趋势对比</tspan>
    <tspan x="64" dy="26">自定义指标与告警阈值设置</tspan>
  </text>

  <!-- Card B -->
  <rect x="662" y="82" width="582" height="300" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <rect x="660" y="80" width="582" height="300" rx="12" ry="12"
        fill="#FFFFFF"/>
  <text x="684" y="118" font-family="Microsoft YaHei" font-size="22"
        font-weight="600" fill="#1A56DB">扩展功能</text>
  <text font-family="Microsoft YaHei" font-size="16" fill="#64748B">
    <tspan x="684" y="152">多维度数据交叉分析</tspan>
    <tspan x="684" dy="26">一键生成可视化报告</tspan>
    <tspan x="684" dy="26">团队协作与权限管理</tspan>
  </text>

  <!-- Card C -->
  <rect x="42" y="422" width="382" height="260" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <rect x="40" y="420" width="382" height="260" rx="12" ry="12"
        fill="#FFFFFF"/>
  <text x="64" y="458" font-family="Microsoft YaHei" font-size="20"
        font-weight="600" fill="#1E293B">性能指标</text>
  <text x="64" y="490" font-family="Microsoft YaHei" font-size="48"
        font-weight="700" fill="#1A56DB">99.9%</text>
  <text x="64" y="520" font-family="Microsoft YaHei" font-size="14"
        fill="#64748B">服务可用性 SLA</text>

  <!-- Card D -->
  <rect x="442" y="422" width="382" height="260" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <rect x="440" y="420" width="382" height="260" rx="12" ry="12"
        fill="#FFFFFF"/>
  <text x="464" y="458" font-family="Microsoft YaHei" font-size="20"
        font-weight="600" fill="#1E293B">用户规模</text>
  <text x="464" y="490" font-family="Microsoft YaHei" font-size="48"
        font-weight="700" fill="#7C3AED">50M+</text>
  <text x="464" y="520" font-family="Microsoft YaHei" font-size="14"
        fill="#64748B">月活跃用户数</text>

  <!-- Card E -->
  <rect x="842" y="422" width="402" height="260" rx="12" ry="12"
        fill="#000000" fill-opacity="0.06"/>
  <rect x="840" y="420" width="402" height="260" rx="12" ry="12"
        fill="#1A56DB" fill-opacity="0.06"/>
  <text x="864" y="458" font-family="Microsoft YaHei" font-size="20"
        font-weight="600" fill="#1A56DB">持续进化</text>
  <text font-family="Microsoft YaHei" font-size="16" fill="#64748B">
    <tspan x="864" y="492">每周迭代更新</tspan>
    <tspan x="864" dy="26">社区驱动功能优先级</tspan>
    <tspan x="864" dy="26">开放 API 生态集成</tspan>
  </text>
</svg>
```

## 6. 注意事项

1. **坐标计算**：卡片 x/y 坐标 + width/height 不能超出画布边界（1280x720）
2. **间距统一**：同一页面中所有卡片间距必须相同（推荐 20px）
3. **圆角统一**：所有卡片圆角半径必须相同（推荐 12px）
4. **阴影方向**：阴影统一向右下偏移 2px
5. **内边距**：卡片内文字/元素的起始坐标 = 卡片坐标 + 内边距（推荐 24px）
6. **内容溢出**：确保文字和元素不超出卡片边界
