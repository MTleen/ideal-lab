# Ideal Best Practices — Visual Design System

版本：1.0 | 状态：待确认 | 基于 DESIGN.md v1.0 + impeccable brand register

---

## 一、设计方向

### 1.1 场景锚点

> 一位技术负责人在明亮的办公室角落里，对同事说"你等等，我给你看一个东西"——然后把屏幕转向对方，开始滚动一个结构清晰、视觉干净的最佳实践展示站。

两个用户场景决定了一切设计决策：

| 场景 | 用户 | 设备 | 行为 |
|------|------|------|------|
| **浏览发现** | 非技术管理者 | iPad / 大屏手机 | 看 Plugin 是什么、解决什么问题 |
| **深入查看** | 技术负责人 | 14-16 寸笔记本 | 看 Skill 细节、复制安装命令 |

### 1.2 风格关键词

**Structured · Sharp · Warm**

| 关键词 | 含义 | 不允许 |
|--------|------|--------|
| Structured | 信息层级清晰，导航可见，每个 Plugin 页有固定骨架 | 松散的信息堆砌 |
| Sharp | 锐利的排版对比度，明确的色块划分，不为装饰而模糊 | 模糊的新变、玻璃态 |
| Warm | 不冷，不像 CI/CD dashboard。是通过字体的人情味和间距的呼吸感传递的 | 纯灰、纯黑、纯白 |

### 1.3 风格参考

- **Linear 的排版自信** — 一个字重足够大的标题撑起整个 Hero，不堆元素
- **Stripe Atlas 的信息结构** — 长滚动，每 fold 只讲一件事
- **Vercel 模板市场的卡片密度** — 在浏览态提供刚好足够的信息，不过载

### 1.4 反风格声明

具体地说，以下内容**不会出现**在这个站点中：

- 圆角大图标放在每段文字上面
- 三列 icon + title + description 的 SaaS 卡片
- 渐变色文字
- Side-stripe 彩色左边框卡片
- Hero 区域一个大数字 + 小标签 + 渐变色背景

---

## 二、颜色系统

### 2.1 策略

**Committed**。Indigo 不仅仅是一个"强调色"——它携带品牌。在 Hero 区域、导航选中态、CTA 按钮、分类标签选中态中使用，占总视觉面积 30-40%。

### 2.2 主色

```
--brand-50:  oklch(0.96 0.01 270)
--brand-100: oklch(0.91 0.02 270)
--brand-200: oklch(0.82 0.04 270)
--brand-300: oklch(0.72 0.07 270)
--brand-400: oklch(0.62 0.10 270)
--brand-500: oklch(0.52 0.14 270)   # #4f46e5 equivalent — primary
--brand-600: oklch(0.45 0.13 270)
--brand-700: oklch(0.38 0.11 270)
--brand-800: oklch(0.28 0.08 270)
--brand-900: oklch(0.18 0.04 270)
```

### 2.3 语义色

```
--success: oklch(0.55 0.16 145)   # green
--warning: oklch(0.60 0.16 85)    # amber
--error:   oklch(0.50 0.18 25)    # red
--info:    oklch(0.55 0.12 235)   # sky
```

### 2.4 中性色（Light）

```
--surface-0:  oklch(0.99 0.001 270)   # 页面背景 — 不纯白，微暖
--surface-1:  oklch(0.97 0.002 270)   # 卡片背景
--surface-2:  oklch(0.93 0.003 270)   # hover 背景
--surface-3:  oklch(0.88 0.004 270)   # 选中/激活背景

--text-0:     oklch(0.12 0.005 270)   # 主文字 — 不纯黑
--text-1:     oklch(0.38 0.006 270)   # 次要文字
--text-2:     oklch(0.58 0.005 270)   # 辅助文字
--text-3:     oklch(0.78 0.003 270)   # 禁用/占位

--border-0:   oklch(0.88 0.005 270)   # 默认边框
--border-1:   oklch(0.80 0.006 270)   # hover 边框
```

### 2.5 中性色（Dark）

```
--surface-0:  oklch(0.12 0.010 270)   # slate-900 like
--surface-1:  oklch(0.17 0.012 270)   # slate-800 like
--surface-2:  oklch(0.22 0.014 270)   # slate-700 like
--surface-3:  oklch(0.28 0.015 270)

--text-0:     oklch(0.95 0.003 270)
--text-1:     oklch(0.72 0.006 270)
--text-2:     oklch(0.52 0.008 270)
--text-3:     oklch(0.38 0.010 270)

--border-0:   oklch(0.25 0.012 270)
--border-1:   oklch(0.35 0.013 270)
```

### 2.6 分类色（Plugin 卡片 + 筛选标签）

每个 category 一个色标，用于卡片顶部条和筛选标签：

| Category | 色 | 用途 |
|----------|----|------|
| `development` | `oklch(0.55 0.16 270)` indigo | 开发类 plugin |
| `content` | `oklch(0.55 0.12 180)` teal | 内容生成类 |
| `research` | `oklch(0.55 0.16 55)` amber | 调研分析类 |
| `knowledge` | `oklch(0.55 0.12 100)` lime | 知识库类 |
| `tooling` | `oklch(0.48 0.08 290)` violet | 工具类 |

---

## 三、字体系统

### 3.1 选择过程

品牌声音词汇：**structured · sharp · warm**

物理物参考：1970 年代末 Bell Labs 技术备忘录 — 干净、严谨的排版，但充满人类的好奇心。不是冷冰冰的规格说明书。

反身拒绝：
- Inter → 训练数据默认值，拒绝
- Space Grotesk → 同上，拒绝
- DM Sans → 同上，拒绝
- IBM Plex Sans → 拒绝
- JetBrains Mono 用于代码 → **允许**（代码块本质需要 mono）

最终选择：**Satoshi**（Fontshare，免费可变字体）作为唯一的品牌字体家族。

理由：Satoshi 有 7 个字重（300-900），几何骨架但带人文暖度，在 bold/extrabold 时有强烈的排版存在感，在 regular 时阅读舒适。一个家族就够了——用一个 committed family 比两个 timid family 更有力量。

### 3.2 字体栈

```css
--font-display: 'Satoshi', system-ui, -apple-system, sans-serif;
--font-body:    'Satoshi', system-ui, -apple-system, sans-serif;
--font-mono:    'JetBrains Mono', 'SF Mono', 'Cascadia Code', ui-monospace, monospace;
```

### 3.3 字号阶梯（`clamp()` 流体）

| Token | 最小 | 首选 | 最大 | 用途 |
|-------|------|------|------|------|
| `hero` | `clamp(48px, 8vw, 96px)` | — | — | 首页 Hero 标题 |
| `h1` | `clamp(36px, 5vw, 64px)` | — | — | Plugin 详情页标题 |
| `h2` | `clamp(28px, 3.5vw, 40px)` | — | — | 段落标题 |
| `h3` | `clamp(22px, 2.5vw, 28px)` | — | — | 卡片标题 |
| `body-lg` | `clamp(17px, 2vw, 20px)` | — | — | Hero 副标题、lead |
| `body` | 16px | — | — | 正文 |
| `body-sm` | 14px | — | — | 辅助文字、Badge |
| `caption` | 12px | — | — | 时间戳、版本号 |
| `code` | 14px | — | — | 安装命令 |

### 3.4 字重使用

| 语境 | 字重 | 说明 |
|------|------|------|
| Hero 标题 | 800-900 | `font-extrabold` / `font-black` |
| h1/h2 | 700 | `font-bold` |
| h3 卡片标题 | 600 | `font-semibold` |
| 正文 | 400 | `font-normal` |
| 导航/Badge/标签 | 500 | `font-medium` |
| 代码 | 400 | `font-normal` |

---

## 四、页面布局规范

### 4.1 首页布局

```
┌──────────────────────────────────────────────────┐
│  NAV (fixed, glass)                              │
│  Logo · 搜索 · Theme Toggle                      │
├──────────────────────────────────────────────────┤
│                                                  │
│  HERO (full-width, min-h: 60vh)                  │
│  ┌────────────────────────────────────────┐      │
│  │  标签: BEST PRACTICES                    │      │
│  │  h1: 将 Claude Code 工程方法论           │      │
│  │      沉淀为可分发的最佳实践               │      │
│  │  body-lg: 从需求到交付的完整链路...       │      │
│  │  [CTA: 浏览 Plugin]  [CTA: 如何安装]     │      │
│  └────────────────────────────────────────┘      │
│                                                  │
├──────────────────────────────────────────────────┤
│  FILTER BAR                                      │
│  [All] [Development] [Content] [Research] ...    │
│  ──────────────────────────────────────          │
│  🔍 Search plugins...                            │
├──────────────────────────────────────────────────┤
│                                                  │
│  PLUGIN GRID (auto-fill, minmax(320px, 1fr))     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Category │ │ Category │ │ Category │        │
│  │ 色标     │ │ 色标     │ │ 色标     │        │
│  │          │ │          │ │          │        │
│  │ Plugin   │ │ Plugin   │ │ Plugin   │        │
│  │ Name     │ │ Name     │ │ Name     │        │
│  │ Desc     │ │ Desc     │ │ Desc     │        │
│  │ [Skills] │ │ [Skills] │ │ [Skills] │        │
│  │ v1.0     │ │ v1.0     │ │ v1.0     │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│                                                  │
├──────────────────────────────────────────────────┤
│  FOOTER: GitHub · License · Made with Claude Code │
└──────────────────────────────────────────────────┘
```

### 4.2 首页网格

```
max-w: 1280px, mx-auto, px-6 (mobile) / px-8 (tablet) / px-12 (desktop)

Hero:     full-width bleed, 内部文字 max-w-[720px] 左对齐
Filter:   与 grid 对齐，搜索栏 max-w-[480px]
Grid:     repeat(auto-fill, minmax(320px, 1fr)), gap-6
Footer:   与 grid 对齐
```

### 4.3 Plugin 详情页布局

```
┌──────────────────────────────────────────────────┐
│  NAV                                             │
├──────────────────────────────────────────────────┤
│  ← Back to all plugins                           │
│                                                  │
│  HERO (min-h: 40vh)                              │
│  ┌────────────────────────────────────────┐      │
│  │ Category Badge                          │      │
│  │ h1: Plugin Name                         │      │
│  │ body-lg: 一句话价值主张                   │      │
│  │ [CTA: 安装命令] [GitHub →]               │      │
│  └────────────────────────────────────────┘      │
│                                                  │
│  PAIN POINTS (scroll-triggered reveal)            │
│  ┌───┐ ┌───┐ ┌───┐                              │
│  │ 1 │ │ 2 │ │ 3 │  (每张卡片揭示一个痛点)         │
│  └───┘ └───┘ └───┘                              │
│                                                  │
│  QUANTITATIVE DATA (if available)                 │
│  ┌──────────┬──────────┬──────────┐              │
│  │  62% ↓   │ <5%      │ 100%     │              │
│  │  总耗时   │  偏差率   │  可追溯   │              │
│  └──────────┴──────────┴──────────┘              │
│                                                  │
│  SKILL LIST                                      │
│  ┌────────────────────────────────────────┐      │
│  │ Skill Name  │ Phase │ Description       │      │
│  │ Skill Name  │ Phase │ Description       │      │
│  │ Skill Name  │ Phase │ Description       │      │
│  └────────────────────────────────────────┘      │
│  → Click to view full SKILL.md                   │
│                                                  │
│  META INFO                                       │
│  Version · Author · Keywords · GitHub Repo       │
│                                                  │
├──────────────────────────────────────────────────┤
│  FOOTER                                          │
└──────────────────────────────────────────────────┘
```

### 4.4 Skill 详情页布局

```
┌──────────────────────────────────────────────────┐
│  ← Back to Plugin                                │
│                                                  │
│  Skill Name  |  Phase Badge                      │
│  Description                                     │
│                                                  │
│  SKILL.MD RENDERED CONTENT                       │
│  (prose 风格，代码高亮，表格样式)                    │
│                                                  │
│  REFERENCES / SCRIPTS (侧栏或底部)                  │
│                                                  │
├──────────────────────────────────────────────────┤
```

---

## 五、组件设计规范

### 5.1 Plugin 卡片

```
┌─────────────────────────────────┐
│ ████████ (category 色 4px 顶条)  │
│                                 │
│ CATEGORY (10px, caps, muted)    │
│ Plugin Name (h3, 600w)          │
│ Description (body-sm, 2 lines)  │
│                                 │
│ ┌───────┐ ┌───────┐ ┌───┐      │
│ │ Skill │ │ Skill │ │+3 │      │
│ └───────┘ └───────┘ └───┘      │
│                                 │
│ v1.1.0 · author · ★ 11          │
└─────────────────────────────────┘

交互：
- hover: translateY(-4px) + shadow-lg, transition 200ms ease-out-expo
- focus-visible: ring-4 ring-brand/20, border-brand
```

### 5.2 搜索栏

```
┌──────────────────────────────────────┐
│ 🔍 Search plugins...          ⌘K    │
└──────────────────────────────────────┘

尺寸: lg (h-12, 48px)
圆角: 16px (radius-lg)
背景: surface-1
边框: border-0, focus: border-brand
字号: 16px body
快捷键提示: 12px caption, 右对齐, 带键盘样式 badge
```

### 5.3 分类筛选标签

```
All  Development  Content  Research  Knowledge  Tooling

单个标签: px-4 py-1.5, rounded-full, h-8 (32px)
默认: surface-2 bg, text-1
选中: brand-500 bg, white text, font-medium
hover: surface-3 bg (非选中时)
transition: 150ms ease-out
```

### 5.4 CTA 按钮

```
Primary:   brand-500 bg, white text, shadow-primary, h-12, px-6, rounded-lg
Secondary: surface-2 bg, text-0, border border-0, h-12, px-6, rounded-lg
Ghost:     transparent, text-1, h-8, px-3, rounded-md

交互: hover 亮度 -8% / +8%, transition 150ms ease-out
focus: ring-4 ring-brand/20
```

### 5.5 安装命令

```
┌────────────────────────────────────────────┐
│  $ claude plugin marketplace add ...       │  📋
│  $ claude plugin install ...               │
└────────────────────────────────────────────┘

背景: surface-2 (light) / surface-1 (dark)
字体: JetBrains Mono 14px
圆角: 12px (radius-md)
右侧: 复制按钮 (icon button, h-8, 32px)
复制成功: 按钮变 success 色 + "Copied" tooltip, 2s 后恢复
```

### 5.6 元信息 Badge

```
版本: outline badge, border-0, text-2, 12px, h-6, rounded-sm
阶段: filled badge, 对应 category 色 15% opacity, 12px, h-6, rounded-sm
关键词: ghost badge, text-2, 12px
```

### 5.7 时间线（首页底部）

```
┌─────────────────────────────────────────┐
│  Recently Updated                       │
│                                         │
│  2 days ago  · ideal-dev-workflow v1.1  │
│  5 days ago  · ideal-ppt-suite v1.1     │
│  ...                                    │
└─────────────────────────────────────────┘

每行: flex, gap-3, py-2, border-bottom (最后一条无)
时间: 12px caption, text-2, 宽度固定 80px
内容: 14px body-sm, text-0, link 到 plugin 页
```

### 5.8 痛点卡（Plugin 详情页）

```
┌──────────────────────────────┐
│ 01                           │
│ 痛点标题 (h3, 600w)           │
│ 痛点描述 (body, text-1)       │
│                              │
│ ─────────────────────────── │
│ 解法：具体措施 (body-sm,     │
│       success 色)            │
└──────────────────────────────┘

数字: brand-500, 48px, 900w, 绝对定位左上
卡片: surface-1 bg, border border-0, rounded-lg, p-6
hover: shadow-md, 无位移 (不要动 layout)
动画: 首屏入场 stagger reveal, 每个间隔 120ms
```

---

## 六、动画规范

### 6.1 入场动画

**首页加载 (一次性，仅首屏)**：

```
顺序: Nav → Hero 文字 (stagger) → Filter Bar → 卡片 (stagger)
Hero 标题:  opacity 0→1, translateY 24px→0, 600ms, delay 0
Hero 副标题:  opacity 0→1, translateY 16px→0, 500ms, delay 120ms
Hero CTA:      opacity 0→1, translateY 12px→0, 400ms, delay 240ms
Filter Bar:    opacity 0→1, 400ms, delay 400ms
Card Grid:     opacity 0→1, translateY 20px→0, stagger 80ms

缓动: cubic-bezier(0.16, 1, 0.3, 1) — ease-out-expo
      不使用 ease-in-out / bounce / elastic
```

### 6.2 卡片 Hover

```
transform: translateY(-4px)
box-shadow: shadow-lg
transition: 200ms cubic-bezier(0.16, 1, 0.3, 1)

仅动画 transform + shadow，不动画 layout 属性
```

### 6.3 分类筛选切换

```
选中下划线: 从旧位置到新位置, 200ms ease-out
卡片出现/消失: opacity + scale(0.97→1 / 1→0.97), 150ms

使用 FLIP 或 framer-motion layoutId 实现
```

### 6.4 页面过渡

```
Plugin 列表 → Plugin 详情:
  列表退出: opacity 1→0, 100ms
  详情进入: opacity 0→1, translateY 16px→0, 300ms

使用 Next.js App Router 的 page transition 或 framer-motion AnimatePresence
```

### 6.5 痛点揭示动画 (Plugin 详情页)

```
Scroll-triggered:
  卡片进入 viewport 60% 时触发
  opacity 0→1, translateY 32px→0
  每张卡片 stagger 120ms
  使用 Intersection Observer + framer-motion
```

### 6.6 复制按钮反馈

```
点击: 
  图标 scale(1→0.9→1), 100ms
  图标颜色变为 success
  "Copied!" tooltip fade in, 2s 后 fade out
```

---

## 七、响应式策略

### 7.1 断点

| Token | 宽度 | 设备 |
|-------|------|------|
| `mobile` | < 640px | 手机竖屏 |
| `tablet` | 640-1024px | 平板 / 小笔记本 |
| `desktop` | ≥ 1024px | 大屏笔记本 / 显示器 |

### 7.2 各断点适配

**首页**：

| 元素 | Desktop (≥1024) | Tablet (640-1023) | Mobile (<640) |
|------|-----------------|-------------------|---------------|
| Hero 标题 | clamp(48, 8vw, 96) | clamp(36, 6vw, 64) | clamp(32, 8vw, 48) |
| Hero padding | py-32 px-12 | py-24 px-8 | py-20 px-6 |
| Plugin 网格 | 3 列 (minmax 320) | 2 列 | 1 列 |
| 搜索栏宽度 | max-w-[480px] | max-w-[360px] | full width |
| 筛选标签 | 水平滚动 | 水平滚动 | 水平滚动（可 swipe） |
| 导航 | 展开 | 展开 | Hamburger menu |

**Plugin 详情页**：

| 元素 | Desktop | Tablet | Mobile |
|------|---------|--------|--------|
| 痛点卡片 | 3 列网格 | 2 列 | 1 列堆叠 |
| 数据指标 | 4 列 | 2×2 网格 | 1 列堆叠 |
| Skill 列表 | 表格 | 表格 | 卡片形式（每行变卡片） |
| 安装命令 | 水平一行 | 水平（字号缩小） | 垂直堆叠 |

### 7.3 暗色模式

- 使用 CSS 自定义属性切换，不重写组件
- `prefers-color-scheme` 自动检测，导航栏提供手动切换
- 暗色模式下阴影减淡（`shadow-primary` 在暗色下用 `brand/15` 代替 `brand/20`）
- 代码块在两种模式下都用 `surface-2` 背景，保持一致可读性

---

## 八、设计 Token 命名规范

### CSS 变量命名

```
--bp-{category}         品牌/语义/中性
--bp-{component}-{prop}  组件级

示例:
--bp-brand-500          主色
--bp-surface-0          页面背景
--bp-card-radius        卡片圆角 = 12px
--bp-card-shadow        卡片阴影 = shadow-sm
--bp-code-bg            代码块背景
--bp-nav-height         导航栏高度 = 56px
```

---

## 九、实现优先级

| P | 内容 | 说明 |
|----|------|------|
| **P0** | 颜色系统 CSS 变量 + 字体加载 | 所有页面依赖 |
| **P0** | 首页 Hero + Plugin 卡片网格 + 筛选 | 核心浏览体验 |
| **P0** | Plugin 详情页基础骨架 | 深度查看 |
| **P1** | Skill 详情页 | Markdown 渲染 |
| **P1** | 搜索功能 (Fuse.js) | 客户端模糊搜索 |
| **P1** | 暗色模式 | Theme toggle |
| **P2** | 入场动画 | 首屏 stagger reveal |
| **P2** | 痛点揭示动画 | Scroll-triggered |
| **P2** | 响应式完整适配 | Mobile navigation |
