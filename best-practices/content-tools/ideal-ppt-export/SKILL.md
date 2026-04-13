---
name: ideal-ppt-export
description: Use when P12 SVG review is completed and export/delivery phase begins. Converts SVG slides to editable PPTX and PDF. Triggered by ideal-ppt-workflow at P13.
---

# Ideal PPT Export (P13)

导出交付 — 将 SVG 幻灯片转换为可编辑 PPTX 和 PDF，生成最终交付物。

## 角色定义

| 属性 | 值 |
|------|-----|
| 角色 | Export & Delivery Specialist |
| 输入工件 | `svg_output/*.svg` 或 `svg_final/*.svg` + `notes/total.md` |
| 输出工件 | `{topic-slug}.pptx` + `{topic-slug}.pdf` |

## 前置检查

- `svg_output/` 或 `svg_final/` 目录存在且包含 SVG 文件
- P12 评审已完成

## 依赖

- **Python 3.8+**
- **python-pptx**: `pip install python-pptx`
- **rsvg-convert**: SVG 转 PNG（macOS: `brew install librsvg`）
- **PyPDF2**: PDF 合并（`pip install PyPDF2`）

## 工作流程

### Step 1: 验证 SVG 文件

确认所有 SVG 文件有效：
- viewBox 属性存在且正确
- 无禁止元素（clipPath, mask, style, foreignObject, script, animate）
- XML 合法（`&` 转义为 `&amp;` 等）
- 文件大小 > 0

### Step 2: 分割演讲备注

将 `notes/total.md` 按页分割为独立文件：

```bash
python3 ${SKILL_DIR}/scripts/split-notes.py <slide-deck-dir>
```

### Step 3: SVG 后处理（如未执行）

如果 `svg_final/` 目录不存在或为空，先将 `svg_output/` 复制到 `svg_final/`：

```bash
cp svg_output/*.svg svg_final/
```

同时修复 XML 实体转义（`&` → `&amp;`）：

```bash
python3 ${SKILL_DIR}/../ideal-ppt-executor/scripts/sanitize-svg.py svg_output/ -o svg_final/
```

### Step 4: 导出 PPTX（Native Shapes 模式）

**核心方案：SVG → DrawingML 原生形状，完全可编辑。**

使用 ppt-master 的 `svg_to_shapes.py` 将每个 SVG 元素转换为 DrawingML XML：

```bash
python3 ${SKILL_DIR}/scripts/native-export.py <slide-deck-dir>
```

**工作原理**：
1. 用 `python-pptx` 创建基础 PPTX（设置画布尺寸）
2. 解压 PPTX 为 ZIP
3. 对每个 SVG，调用 `svg_to_shapes.convert_svg_to_slide_shapes()` 生成 DrawingML XML
4. 用生成的 XML 替换幻灯片内容
5. 嵌入演讲备注（notesSlide XML）
6. 重新打包为 PPTX

**SVG → DrawingML 映射**：

| SVG 元素 | DrawingML 形状 | PPT 可编辑 |
|----------|---------------|-----------|
| `<rect>` | `<a:prstGeom prst="rect">` | 矩形/圆角矩形 |
| `<circle>` / `<ellipse>` | `<a:prstGeom prst="ellipse">` | 椭圆 |
| `<line>` | `<a:custGeom>` (moveTo + lnTo) | 自由线条 |
| `<polygon>` | `<a:custGeom>` (闭合路径) | 自由形状 |
| `<text>` | `<p:sp txBox="1">` + `<a:r>` | 文本框 |
| `<path>` | `<a:custGeom>` (贝塞尔曲线) | 自由形状 |

**坐标系统**：
- SVG 像素 → EMU: `px * 9525`（96 DPI）
- 文本 baseline 偏移：`y - fontSize * 0.85`
- text-anchor 对齐：start → l, middle → ctr, end → r

**Fallback**：如果 native 模式失败，fallback 到 SVG 嵌入模式（需右键"转换为形状"）。

### Step 5: 导出 PDF

```bash
python3 ${SKILL_DIR}/scripts/merge-to-pdf.py <slide-deck-dir>
```

**流程**：
1. `rsvg-convert` 将每个 SVG 转为单页 PDF
2. `PyPDF2` 合并所有页面为一个 PDF

### Step 6: 交付摘要

输出交付报告：

```markdown
## 交付完成

主题：{主题}
风格：{预设名称}
幻灯片：共 N 页

交付物：
- PPTX：{topic-slug}.pptx（可编辑）
- PDF：{topic-slug}.pdf
- 演讲备注：notes/*.md
- SVG 源文件：svg_final/*.svg
```

## 文件发现规则

- SVG 文件正则：`^(\d+)-slide-.*\.svg$`
- 按序号排序
- 备注文件匹配：`notes/total.md` 或 `notes/NN_*.md`

## 错误处理

| 错误 | 处理 |
|------|------|
| svg_to_shapes 转换失败 | 报告错误元素，跳过该元素继续 |
| python-pptx 未安装 | 提示 `pip install python-pptx` |
| rsvg-convert 未安装 | PDF 导出跳过，仅导出 PPTX |
| XML 解析错误 | 修复实体转义后重试 |
| SVG 验证失败 | 报告具体问题 |
