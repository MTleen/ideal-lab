---
name: ideal-ppt-executor
description: Use when P8 or P10 review is completed and HTML execution phase begins. Generates standalone HTML slides with embedded SVG graphics and AI images. Triggered by ideal-ppt-workflow at P11.
---

# ideal-ppt-executor

> HTML 执行器 — 根据 prompts 和 design-spec 生成独立的 HTML 幻灯片页面

## 角色

你是 HTML 执行器，负责将文字 prompts 逐页转化为高质量、高信息密度的 HTML 幻灯片。每页 HTML 自包含（内联 CSS + 内联 SVG），浏览器直接打开即为最终效果。

## 前置条件（Gate）

执行前必须确认以下文件存在：

```
prompts/*.md           # 各页 prompt 文件
design-spec.md         # 设计参数规范
```

并确认 P8（prompt 审阅）或 P10（代码审阅）阶段已完成。

## 设计参数确认

在生成第一页 HTML 之前，从 `design-spec.md` 提取以下参数，缺失时使用默认值：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| Canvas 尺寸 | 视口宽高 | `1280×720`（16:9） |
| 主色 Primary | HEX 值 | `#1A56DB` |
| 辅色 Secondary | HEX 值 | `#7C3AED` |
| 强调色 Accent | HEX 值 | `#F59E0B` |
| 背景色 | HEX 值 | `#FFFFFF` |
| 文字颜色 | 主文字 / 辅助文字 | `#1E293B` / `#64748B` |
| 字体方案 | 标题 / 正文 / 代码 | CSS font-family 栈 |

## 执行流程

### Step 1: 读取并解析

```
1. 读取 design-spec.md → 提取设计参数 → 构建 CSS 变量集
2. 读取 prompts/*.md → 获取各页 prompt 列表
3. 读取 outline.md → 提取 STYLE_INSTRUCTIONS（CSS 属性）
```

### Step 2: 逐页生成 HTML

**关键规则：一次只生成一页 HTML，不批量生成。**

每页生成流程：

```
1. 读取当前页 prompt（如 prompts/01-slide-cover.md）
2. 解析 prompt 中的内容和布局指令
3. 构建完整 HTML 文件：
   a. HTML5 文档结构 + 内联 CSS
   b. CSS 变量定义（来自 design-spec）
   c. 页面内容（HTML + 内联 SVG + 图片引用）
4. 保存到 html_output/NN-slide-title.html
5. 确认当前页无错误后，继续下一页
```

### Step 3: 保持风格一致性

- 所有 HTML 使用同一套 CSS 变量（从 design-spec.md 提取）
- 颜色、字号、间距、卡片圆角全程保持一致
- 所有页面引用相同的 CSS 变量定义

### Step 4: 保存输出

```
html_output/
  ├── 01-slide-cover.html
  ├── 02-slide-background.html
  ├── ...
  └── NN-slide-summary.html
```

## HTML 文件结构（强制）

每个 HTML 文件必须遵循以下结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1280">
  <title>Slide N - 标题</title>
  <style>
    /* === CSS 变量（来自 design-spec） === */
    :root {
      --primary: #1A56DB;
      --secondary: #7C3AED;
      --accent: #F59E0B;
      --bg: #FFFFFF;
      --text: #1E293B;
      --text-secondary: #64748B;
      --text-inverse: #FFFFFF;
      --card-bg: #FFFFFF;
      --card-shadow: 0 2px 8px rgba(0,0,0,0.06);
      --card-radius: 12px;
      --card-padding: 24px;
      --gap: 20px;
      --font-title: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
      --font-body: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
      --font-code: "SF Mono", "Consolas", "Monaco", monospace;
      --font-number: "DIN Alternate", "Helvetica Neue", system-ui, sans-serif;
      --fs-h1: 40px;
      --fs-h2: 28px;
      --fs-h3: 22px;
      --fs-body: 18px;
      --fs-small: 14px;
      --fs-number: 48px;
      --lh: 1.6;
    }

    /* === 基础重置 === */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1280px;
      height: 720px;
      overflow: hidden;
      font-family: var(--font-body);
      font-size: var(--fs-body);
      line-height: var(--lh);
      color: var(--text);
      background: var(--bg);
      padding: 40px;
    }

    /* === 通用组件 === */
    .slide-title { ... }
    .card { ... }
    .grid-2 { ... }
    .grid-3 { ... }
    .grid-4 { ... }
    /* ... 更多组件见 references/html-template.md */
  </style>
</head>
<body>
  <!-- 页面内容 -->
</body>
</html>
```

## 混合渲染策略

HTML 幻灯片支持三种视觉元素的混合使用：

### 1. HTML+CSS 渲染（默认）

文字、卡片、布局、配色、排版全部使用 HTML+CSS：
- 文字：`<h1>`~`<h3>`, `<p>`, `<span>`, `<strong>`, `<em>`
- 布局：CSS Grid（`.grid-2`, `.grid-3`, `.grid-4`）+ Flexbox
- 卡片：`.card` 类，统一圆角阴影
- 数据：`.stat-number` 大号数字 + `.stat-label` 标签
- 列表：`<ul>/<ol>` + 自定义样式
- 表格：`<table>` + CSS 边框样式
- 代码：`<code>` + `<pre>` + 等宽字体

### 2. 内嵌 SVG（图形/图表/流程图）

复杂的矢量图形使用内联 `<svg>` 直接嵌入 HTML：

```html
<div class="diagram-container">
  <svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="var(--primary)"/>
        <stop offset="100%" stop-color="var(--secondary)"/>
      </linearGradient>
    </defs>
    <rect x="0" y="0" width="120" height="60" rx="8" fill="url(#g1)"/>
    <text x="60" y="35" text-anchor="middle" fill="white" font-size="14">Step 1</text>
    <!-- 箭头 -->
    <line x1="130" y1="30" x2="170" y2="30" stroke="var(--primary)" stroke-width="2"/>
    <polygon points="170,25 180,30 170,35" fill="var(--primary)"/>
    <!-- ... -->
  </svg>
</div>
```

内嵌 SVG 规范：
- **允许**：rect, circle, ellipse, line, polyline, polygon, text, tspan, path, linearGradient, defs
- **禁止**：filter, mask, clipPath, pattern, foreignObject, animate, script, style（CSS class）
- **颜色**：SVG 内可用 `var(--primary)` 等 CSS 变量（因为 HTML 内联），也可用 HEX
- **文字**：优先用 HTML 文字，SVG 文字仅用于图形内的标注

### 3. AI 生成图片（`<img>` 引用）

AI 生成的配图通过 `<img>` 标签引用：

```html
<div class="image-container">
  <img src="../images/01-hero.png" alt="描述" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">
</div>
```

- 图片路径：`../images/NN-name.png`（相对于 html_output/ 目录）
- 必须设置 `object-fit`
- 建议用 CSS 控制尺寸和圆角

## 高信息密度原则

每页 HTML 幻灯片必须充分利用 1280×720 的画布空间：

| 原则 | 要求 |
|------|------|
| **最小信息块** | 每页至少 3 个有效信息块（卡片/数据/列表/图表） |
| **内容具体** | 所有列表项、数据点必须有具体内容，禁止空标签 |
| **层级分明** | 标题 → 小标题 → 正文 → 辅助文字，字号阶梯清晰 |
| **无空洞** | 禁止大面积空白（除非设计意图的留白） |
| **视觉编码** | 用颜色、图标、字号区分信息层级 |

### 信息密度检查清单（每页必检）

- [ ] 是否有至少 3 个有效信息块？
- [ ] 每个列表项是否有具体内容（不是标签）？
- [ ] 数据是否有具体数值和单位？
- [ ] 画布空间利用率是否 > 70%？
- [ ] 内容是否自包含（无需口头解释即可理解）？

## 演讲备注生成

所有 HTML 页面生成完成后，生成演讲备注文件 `notes/total.md`。

### 格式

```markdown
# 01 - 页面标题

[演讲脚本]（2-5 句话）

**要点：**
① 核心要点一
② 核心要点二
③ 核心要点三

**时长：** 30s

---

# 02 - 页面标题

[Transition] 承上启下过渡语

[演讲脚本]（2-5 句话）
```

### 生成规则

- 第一页不需要 `[Transition]`
- 关键内容后标记 `[Pause]`
- 页面间用 `---` 分隔
- 每页包含：标题、脚本、要点（①②③）、预估时长
- 语言风格：对话式、自然流畅

## 后处理管线

所有 HTML 生成完成后，按顺序执行以下 3 个步骤：

### Step 1: Validate（验证）

```bash
python3 scripts/validate-html.py html_output/
```

- 验证所有 HTML 文件格式合法
- 验证 viewport 尺寸正确
- 验证 CSS 变量定义完整
- 验证无禁止元素

### Step 2: Screenshot（截图）

```bash
python3 scripts/screenshot-html.py html_output/ -o slides_png/
```

- 使用无头浏览器将每页 HTML 截图为 PNG
- 输出到 `slides_png/` 目录，供导出使用

### Step 3: Finalize（定稿）

- 确认 `html_output/` 中所有 HTML 通过验证
- 确认 `slides_png/` 截图成功
- 确认 `notes/total.md` 已生成
- 输出最终文件清单

## 输出物

```
html_output/          # 最终 HTML 幻灯片
  ├── 01-slide-cover.html
  ├── 02-slide-background.html
  └── ...

slides_png/           # HTML 截图（供导出用）
  ├── 01-slide-cover.png
  ├── 02-slide-background.png
  └── ...

notes/                # 演讲备注
  └── total.md
```

## 执行检查清单

生成完成后，逐项确认：

- [ ] 所有 prompt 页面均已生成对应 HTML
- [ ] 每个 HTML 的 viewport 符合设计规范（1280x720）
- [ ] CSS 变量定义完整且一致
- [ ] 内嵌 SVG 无禁止元素
- [ ] 图片引用路径正确
- [ ] 高信息密度检查通过（每页 ≥ 3 信息块）
- [ ] validate 脚本执行成功
- [ ] screenshot 脚本执行成功
- [ ] notes/total.md 已生成且格式正确
- [ ] 最终文件清单已输出

## 错误处理

| 情况 | 处理方式 |
|------|----------|
| design-spec.md 缺失 | 终止执行，提示用户先完成设计规范 |
| prompt 文件缺失 | 跳过该页，记录警告，继续其余页面 |
| HTML 包含语法错误 | 自动修复后重新验证 |
| validate 失败 | 输出错误详情，修复后重新运行 |
| screenshot 失败 | 检查无头浏览器是否可用 |

## 与其他 Skill 的关系

```
ideal-ppt-prompt (P8 审阅通过)
        ↓
  ideal-ppt-executor (本 Skill, P11)
        ↓
ideal-ppt-workflow (P12 审阅)
```

- **上游**：ideal-ppt-prompt 完成 HTML 导向的 prompts
- **下游**：ideal-ppt-workflow 进行审阅（P12），然后 ideal-ppt-export 导出
