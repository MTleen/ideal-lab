---
name: ideal-ppt-export
description: Use when P12 review is completed and export/delivery phase begins. Converts HTML slides to editable PPTX (native shapes/text/tables) and PDF. Triggered by ideal-ppt-workflow at P13.
---

# Ideal PPT Export (P13)

导出交付 — 将 HTML 幻灯片解析转换为**可编辑** PPTX（原生形状/文本框/表格）和 PDF。

## 角色定义

| 属性 | 值 |
|------|-----|
| 角色 | Export & Delivery Specialist |
| 输入工件 | `html_output/*.html` + `notes/total.md` |
| 输出工件 | `{topic-slug}.pptx`（可编辑）+ `{topic-slug}.pdf` |

## 前置检查

- `html_output/` 目录存在且包含 HTML 文件
- P12 评审已完成

## 依赖

- **Python 3.8+**
- **python-pptx**: `pip install python-pptx`
- **beautifulsoup4**: `pip install beautifulsoup4`（HTML 解析）
- **Playwright**（PDF 导出用）: `pip install playwright && playwright install chromium`

## 工作流程

### Step 1: 验证 HTML 文件

确认所有 HTML 文件有效：
- `body` 元素有 `width: 1280px; height: 720px`
- 内容非空

### Step 2: 导出 PPTX（原生元素模式）

**核心方案：HTML DOM → python-pptx 原生形状/文本框/表格，完全可编辑。**

```bash
python3 ${SKILL_DIR}/scripts/html-to-pptx-native.py html_output/ -o {topic-slug}.pptx
```

**HTML → PPTX 元素映射**：

| HTML 元素/CSS 类 | PPTX 原生元素 | 说明 |
|-------------------|--------------|------|
| `<h1>` | TextBox + 大号加粗字体 | 页面标题 |
| `<h2>` / `<h3>` | TextBox + 中号字体 | 卡片/模块标题 |
| `<p>` / `<span>` | TextBox + 正文字体 | 正文文本 |
| `.card` / `.layer` | Rectangle + TextBox | 卡片/层容器 |
| `.stat-number` | TextBox + 超大号加粗字体 | KPI 数字 |
| `.stat-label` | TextBox + 小号字体 | KPI 标签 |
| `<ul>` / `<ol>` | TextBox + 项目符号 | 列表 |
| `<table>` | Table（python-pptx 原生表格） | 数据表格 |
| `.badge` / `.tag` | Rectangle（小号圆角）+ TextBox | 标签/徽章 |
| `.arrow-row` / 流程箭头 | Line + Freeform | 流程连线 |
| 内嵌 `<svg>` | 截图后作为 Image 嵌入 | SVG 图形（不可编辑，但清晰） |
| `<img>` | Image 嵌入 | AI 生成图片 |

**坐标转换**：

- HTML px → PPTX EMU: `px * 9525`（96 DPI 标准）
- HTML (0,0) 在左上角 → PPTX 也是左上角
- PPTX 页面尺寸：`Inches(13.333) × Inches(7.5)` = 1280×720 px 映射
- 元素位置：读取 HTML `getBoundingClientRect()` 的 x/y/width/height

**文本映射规则**：

```
HTML font-size: 56px  → PPTX Pt(42)    # 封面标题
HTML font-size: 36px  → PPTX Pt(27)    # 页面标题
HTML font-size: 24px  → PPTX Pt(18)    # 章节标题
HTML font-size: 20px  → PPTX Pt(15)    # 卡片标题
HTML font-size: 16px  → PPTX Pt(12)    # 正文
HTML font-size: 14px  → PPTX Pt(10.5)  # 辅助文字
HTML font-size: 12px  → PPTX Pt(9)     # 脚注
HTML font-size: 40px+ → PPTX Pt(30+)   # KPI 数字

HTML font-weight: 700  → bold
HTML font-weight: 600  → bold
HTML font-weight: 400  → normal

HTML color: var(--primary) → 读取 CSS 变量值转为 RGBColor
HTML color: #1A56DB       → RGBColor(0x1A, 0x56, 0xDB)
```

**实现方式**：

脚本使用 Playwright 渲染 HTML 并提取每个元素的 `getBoundingClientRect()`，然后用 python-pptx 创建对应的原生元素：

1. Playwright 打开 HTML，执行 JS 提取所有可见元素的 bbox 和样式
2. 读取 CSS 变量值（`:root` 上计算后的值）
3. 按层级创建 PPTX 元素：背景矩形 → 卡片矩形 → 文本框 → 表格 → 图片
4. SVG 元素单独截图为 PNG，作为 Image 嵌入

### Step 3: 分割演讲备注

```bash
python3 ${SKILL_DIR}/scripts/split-notes.py <slide-deck-dir>
```

### Step 4: 导出 PDF

```bash
python3 ${SKILL_DIR}/scripts/html-to-pdf.py html_output/ -o {topic-slug}.pdf
```

使用 Playwright 将每页 HTML 渲染为单页 PDF，合并输出。

### Step 5: 交付摘要

输出交付报告：

```markdown
## 交付完成

主题：{主题}
幻灯片：共 N 页

交付物：
- HTML 源文件：html_output/*.html
- PPTX：{topic-slug}.pptx（可编辑：原生文本框/形状/表格）
- PDF：{topic-slug}.pdf
- 演讲备注：notes/*.md
```

## 输出目录结构

```
slide-deck/{topic-slug}/
├── html_output/
│   ├── 01-slide-cover.html
│   └── ...
├── notes/
│   └── total.md
├── {topic-slug}.pptx    ← 可编辑
└── {topic-slug}.pdf
```

## 错误处理

| 错误 | 处理 |
|------|------|
| Playwright 未安装 | 提示安装 |
| beautifulsoup4 未安装 | 提示 `pip install beautifulsoup4` |
| HTML 解析失败 | 报告错误元素，跳过该页 |
| PPTX 元素创建失败 | fallback 为截图模式（不可编辑） |
