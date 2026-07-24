---
name: ideal-ppt-export
description: Use when P12 review is completed and export/delivery phase begins. Dual-pipeline export — HTML mode (Playwright → editable native PPTX) and Image mode (PNG → pixel-perfect image-based PPTX). Also exports PDF. Triggered by ideal-ppt-workflow at P13.
---

# Ideal PPT Export (P13)

导出交付 — 双管线导出：HTML 模式生成可编辑 PPTX；Image 模式生成像素级还原的图片型 PPTX。同时导出 PDF。

根据 `rendering_mode` 自动选择导出管线：
- **html**: HTML → Playwright 截图 → python-pptx native elements（可编辑文本框、形状、表格）
- **image**: PNG → python-pptx Image objects（不可编辑，但像素级还原）

## 角色定义

| 属性 | 值 |
|------|-----|
| 角色 | Export & Delivery Specialist |
| 输入工件 | HTML 模式：`html_output/*.html` + `notes/total.md`；Image 模式：`images_output/*.png` + `notes/total.md` |
| 输出工件 | `{topic-slug}.pptx` + `{topic-slug}.pdf` |

## 前置检查

- HTML 模式：`html_output/` 目录存在且包含 HTML 文件
- Image 模式：`images_output/` 目录存在且包含 PNG 文件
- P12 评审已完成
- `rendering_mode` 参数已确定（`html` 或 `image`）

## 依赖

- **Python 3.8+**
- **python-pptx**: `pip install python-pptx`
- **playwright**（HTML 模式）: `pip install playwright && playwright install chromium`
- **PyPDF2**: PDF 合并（`pip install PyPDF2`）
- **Pillow**（Image 模式）: `pip install Pillow`（用于读取 PNG 尺寸）

## 工作流程

### Step 1: 分割演讲备注（如存在）

如果 `notes/total.md` 存在，按页分割为独立文件：

```bash
python3 ${SKILL_DIR}/scripts/split-notes.py <slide-deck-dir>
```

如果 `notes/total.md` 不存在（P11.5 被 `skip_notes: true` 跳过），跳过此步骤。PPTX 将不包含 speaker notes，但导出流程正常继续。

### Step 2a: 导出 PPTX（HTML 模式）

**当 `rendering_mode = "html"` 时使用此管线。**

**核心方案：HTML → Playwright 截图 → python-pptx native elements，完全可编辑。**

```bash
python3 ${SKILL_DIR}/scripts/html-export.py <slide-deck-dir>
```

**工作原理**：
1. 用 Playwright (Chromium) 逐页渲染 `html_output/*.html`
2. 解析渲染后的 DOM 结构，提取文本框、形状、表格、图片等元素
3. 用 `python-pptx` 创建 PPTX，将元素转换为 native DrawingML 对象
4. 嵌入演讲备注（notesSlide XML）
5. 输出可编辑的 PPTX

**HTML → DrawingML 映射**：

| HTML/DOM 元素 | DrawingML 形状 | PPT 可编辑 |
|--------------|---------------|-----------|
| `<div>` (文本容器) | `<p:sp txBox="1">` + `<a:r>` | 文本框 |
| `<table>` | `<a:tbl>` | 表格 |
| `<img>` / background-image | `<p:pic>` | 图片 |
| CSS border/background | `<a:prstGeom prst="rect">` | 矩形/圆角矩形 |
| SVG inline shapes | `<a:custGeom>` (路径) | 自由形状 |

**坐标系统**：
- HTML 像素 → EMU: `px * 9525`（96 DPI）
- 使用 Playwright `getBoundingClientRect()` 获取精确坐标
- 文本对齐：CSS text-align → DrawingML alignment

**优势**：PPTX 中所有文本、形状均为 native 对象，可在 PowerPoint 中直接编辑。

### Step 2b: 导出 PPTX（图片模式）

**当 `rendering_mode = "image"` 时使用此管线。**

**核心方案：PNG → python-pptx Image objects，像素级还原，不可编辑。**

```bash
python3 ${SKILL_DIR}/scripts/image-export.py <slide-deck-dir>
```

**工作原理**：
1. 读取 `images_output/*.png`，按文件名序号排列
2. 用 Pillow 读取每张 PNG 的宽高，计算缩放比例
3. 用 `python-pptx` 创建 PPTX：
   - 设置画布尺寸（默认 16:9 = 12192000 x 6858000 EMU）
   - 对每张 PNG，添加空白幻灯片
   - 使用 `slide.shapes.add_picture()` 将 PNG 作为 Image 对象填满整张幻灯片
   - 保持图片宽高比，不留白边（使用 `crop` 或 `cover` 策略）
4. 从 `notes/total.md` 读取对应页的备注，嵌入为 speaker notes
5. 输出 PPTX

**关键代码逻辑**：

```python
from pptx import Presentation
from pptx.util import Inches, Emu

prs = Presentation()
prs.slide_width = Emu(12192000)   # 16:9
prs.slide_height = Emu(6858000)

for png_path in sorted(png_files):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

    # Fill entire slide area
    slide.shapes.add_picture(
        str(png_path),
        left=Emu(0),
        top=Emu(0),
        width=prs.slide_width,
        height=prs.slide_height
    )

    # Add speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = get_notes_for_slide(page_number)
```

**与 HTML 模式的对比**：

| 维度 | HTML 模式 (Step 2a) | Image 模式 (Step 2b) |
|------|--------------------|--------------------|
| 输入 | `html_output/*.html` | `images_output/*.png` |
| PPTX 内容 | native 文本框、形状、表格 | 整页图片（Image 对象） |
| 可编辑性 | 完全可编辑 | 不可编辑（图片） |
| 视觉还原度 | 依赖 DOM 解析精度 | 像素级还原 |
| 实现复杂度 | 高（需 DOM 解析 + 元素映射） | 低（直接嵌入图片） |
| 适用场景 | 需要后续编辑 PPTX | 只需展示，不编辑 |

### Step 3: 导出 PDF

```bash
python3 ${SKILL_DIR}/scripts/merge-to-pdf.py <slide-deck-dir>
```

**HTML 模式流程**：
1. Playwright 将每个 HTML 页面渲染为单页 PDF
2. `PyPDF2` 合并所有页面为一个 PDF

**Image 模式流程**：
1. PNG 图片已经是最终渲染结果
2. 使用 Pillow / reportlab 将每张 PNG 嵌入 PDF 页面
3. `PyPDF2` 合并所有页面为一个 PDF

### Step 4: 交付摘要

输出交付报告：

```markdown
## 交付完成

主题：{主题}
风格：{预设名称}
渲染模式：{rendering_mode}
幻灯片：共 N 页

交付物：
- PPTX：{topic-slug}.pptx（{rendering_mode} 模式，{可编辑/图片嵌入}）
- PDF：{topic-slug}.pdf
- 演讲备注：notes/*.md
- HTML 源文件：html_output/*.html（如 HTML 模式）
- PNG 渲染图：images_output/*.png（如 Image 模式）
```

## 文件发现规则

- HTML 文件正则：`^(\d+)-slide-.*\.html$`
- PNG 文件正则：`^(\d+)-slide-.*\.png$`
- 按序号排序
- 备注文件匹配：`notes/total.md` 或 `notes/NN_*.md`

## 输出目录结构

```
<slide-deck-dir>/
├── html_output/           # HTML 模式的输入
│   ├── 01-slide-title.html
│   ├── 02-slide-content.html
│   └── ...
├── images_output/         # Image 模式的输入
│   ├── 01-slide-title.png
│   ├── 02-slide-content.png
│   └── ...
├── notes/
│   ├── total.md
│   ├── 01_*.md
│   └── ...
├── {topic-slug}.pptx      # 最终 PPTX
└── {topic-slug}.pdf       # 最终 PDF
```

## 错误处理

| 错误 | 处理 |
|------|------|
| HTML 模式 DOM 解析失败 | 报告错误元素，跳过该元素继续 |
| Image 模式 PNG 文件不存在 | 报告缺失文件路径，跳过该页继续 |
| Image 模式 PNG 文件损坏（Pillow 无法读取） | 报告损坏文件，跳过该页继续 |
| python-pptx 未安装 | 提示 `pip install python-pptx` |
| playwright 未安装（HTML 模式） | 提示 `pip install playwright && playwright install chromium` |
| Pillow 未安装（Image 模式） | 提示 `pip install Pillow` |
| PyPDF2 未安装 | PDF 导出跳过，仅导出 PPTX |
| HTML 文件为空或格式错误 | 报告具体问题，跳过该页 |
| 渲染模式未指定 | 默认使用 `html` 模式，并输出警告 |
| 图片路径包含特殊字符 | 使用 `pathlib.Path` 处理，避免编码问题 |
