---
name: document-render
description: |
  文档渲染输出阶段。将 Markdown 中间件渲染为指定格式的最终交付物。
  触发场景：(1) workflow 调用本 skill (2) 用户要求"生成 Word"、"生成 PPT"、"导出文档"
  产出：最终交付物（markdown/docx/pptx）
io:
  inputs:
    - name: sections
      source: document-writing.sections
  outputs:
    - name: final_doc
      type: docx_or_pptx
---

# Document Render (P6)

## Overview

将 `sections/` 目录下的 Markdown 中间件渲染为最终交付物，支持多种输出格式。

**核心原则：Markdown 中间件必须永久保留，渲染只是按需生成不同格式。**

## 支持的输出格式

| 格式 | 说明 | 渲染方式 |
|------|------|----------|
| `markdown` | 直接使用 sections/ 目录的 md 文件 | 无需渲染，保持原样 |
| `docx` | Microsoft Word 文档 | Pandoc + python-docx |
| `pptx` | PowerPoint 演示文稿 | PptxGenJS |

## 输入

- `sections/*.md`（各章节 Markdown 文件）
- `images/`（配图目录，如有）
- 项目目录、文档名称
- 输出格式（markdown/docx/pptx）

## 输出

`{项目目录}/文档产出/最终交付物`

## 执行步骤

### Step 1: 确定输出格式

读取 `流程状态.md` 中的 `output_format` 字段，确定输出格式。

### Step 2: 根据格式执行渲染

#### Markdown 格式（默认）

无需渲染，直接使用 sections/ 目录：

```bash
# 验证 sections/ 目录存在且内容完整
ls -la {项目目录}/文档产出/sections/
```

#### Docx 格式

**输入模式：**

| 模式 | 条件 | 处理方式 |
|------|------|----------|
| 目录模式 | sections/ 目录存在 | 将目录下所有 .md 文件按文件名排序依次合并 |
| 单文件模式 | sections/ 不存在或用户直接提供 md 文件 | 直接处理单个 md 文件 |

**目录模式合并规则：**

1. **扫描**：收集 `sections/` 目录下所有 `.md` 文件
2. **排序**：按文件名升序排列（如 `01-概述.md`、`02-技术架构.md`、`03-功能清单.md`）
3. **拼接**：依次读取每个文件，相邻文件之间用空行分隔
4. **输出**：生成一个完整的 Markdown 文本用于后续转换

**执行脚本：**

```bash
cd {项目目录}/文档产出/
./scripts/markdown_to_word.sh -o 最终文档.docx sections/
```

**脚本处理流程：**

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 合并文件 | 目录模式按文件名排序依次合并；单文件模式直接读取 |
| 2 | 预处理 Markdown | 清理 \newpage、水平线、空行、表格格式 |
| 3 | Pandoc 转换 | LaTeX 公式转为 OMML（Word 原生数学格式） |
| 4 | Word 后处理 | 字体/字号/行距/首行缩进/表格居中 |
| 5 | 清理临时文件 | 删除中间产物 |

#### Pptx 格式

使用 PptxGenJS 生成演示文稿：

```bash
cd {项目目录}/文档产出/
./scripts/markdown_to_pptx.sh -o 最终演示.pptx sections/
```

### Step 3: 验证输出

检查生成的文件：
- 文件是否存在
- 内容是否完整
- 格式是否正确

## 依赖

| 工具 | 安装方式 |
|------|----------|
| `pandoc` | `brew install pandoc` |
| `python-docx` | `pip3 install python-docx` |

## 格式标准

### Word 文档格式标准

**字体规范：**

| 元素 | 中文字体 | 英文字体 | 字号 |
|-----|---------|---------|------|
| 正文 | 宋体 | Times New Roman | 小四（12pt） |
| 一级标题 | 黑体 | Arial | 三号（16pt） |
| 二级标题 | 黑体 | Arial | 四号（14pt） |
| 三级标题 | 黑体 | Arial | 小四（12pt） |
| 表格内容 | 宋体 | Times New Roman | 五号（10.5pt） |

**段落格式：**

| 元素 | 行距 | 首行缩进 | 段前 | 段后 |
|-----|------|---------|------|------|
| 正文 | 1.5 倍 | 2 字符 | 0 | 0 |
| 标题 | 1.5 倍 | 无 | 0 | 0 |
| 表格内容 | 单倍 | 无 | 0 | 0 |

**表格格式：**
- 表格居中
- 单元格居中
- 表头加粗、居中
- 表格标题：表格上方，格式：**表X-Y 表格名称**

**页面设置：**
- 纸张大小：A4
- 页边距：上下左右各 2.54cm

## 常见问题处理

### 问题1：pandoc 未安装

**现象**：`错误: pandoc 未安装`

**解决**：`brew install pandoc`

### 问题2：python-docx 未安装

**现象**：`警告: python-docx 未安装，跳过后处理`

**解决**：`pip3 install python-docx`

### 问题3：公式显示为原始 LaTeX 代码

**原因**：公式语法 pandoc 不支持

**解决**：
1. 检查 Markdown 源文件中的公式语法
2. 将不支持的语法改为 pandoc 兼容写法
3. 重新运行渲染

### 问题4：表格未正确转换

**原因**：表格头行与分隔行之间有空行

**解决**：脚本预处理自动修复，无需手动处理

## 最终交付结构

```
{项目目录}/
└── 文档产出/
    ├── 流程状态.md          # ✅ 已完成
    ├── P1-需求分析.md       # ✅
    ├── P2-大纲.md           # ✅
    ├── P3-任务拆分.md       # ✅
    ├── sections/            # ✅ Markdown 中间件（永久存档）
    ├── images/              # ✅ 配图（如有）
    └── 最终交付物            # ✅（根据 output_format 生成）
```

## 任务统计

输出统计信息：
- 子任务数
- 总字数
- 配图数
- 耗时

## 示例输出

```
✅ 文档渲染完成
├── 国航智能体/文档产出/最终文档.docx
└── 任务统计
    ├── 子任务数：7
    ├── 总字数：15234
    ├── 配图数：4
    └── 耗时：约1分钟
```
