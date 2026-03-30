---
name: technical-proposal-merge
description: |
  技术方案 P6 文档合并阶段。当需要将各章节 md 合并为最终 Word 文档时使用。
  触发场景：(1) workflow 调用本 skill (2) 用户要求"合并文档"、"生成 Word"
  产出：最终方案.docx
  参考：technical-proposal-style 的 markdown_to_word.md 规范
---

# Technical Proposal Merge (P6)

## Overview

将 sections/ 目录下的各章节 md 文件合并，转换为 Word 文档。转换过程参考 `technical-proposal-style` 的 `markdown_to_word.md` 规范。

## 输入

- `sections/*.md`（各章节文件）
- 项目目录和方案名称

## 输出

`{项目目录}/项目文档/技术方案/最终方案.docx`

## 脚本转换方式（推荐）

本 skill 内置转换脚本，优先使用脚本执行转换：

```bash
./scripts/markdown_to_word.sh -o 最终方案.docx sections/
```

### 输入模式

脚本支持两种输入模式：

**目录模式**（合并目录下所有 .md 文件）：
```bash
./scripts/markdown_to_word.sh -o 输出文件.docx sections/
```

**单文件模式**（直接转换单个合并后的 .md）：
```bash
./scripts/markdown_to_word.sh -o 输出文件.docx 合并内容.md
```

### 脚本处理流程

| 步骤 | 操作 | 说明 |
|------|------|------|
| 步骤1 | 合并/读取文件 | 单文件直接读取；目录模式按文件名排序合并 |
| 步骤2 | 预处理 Markdown | 清理 \\newpage、水平线、空行、表格格式（**数学公式不做预处理**） |
| 步骤3 | Pandoc 转换 | pandoc 直接将 LaTeX 转换为 OMML（Word 原生数学格式） |
| 步骤4 | Word 后处理 | 字体/字号/行距/首行缩进/表格居中 + **公式 fallback 处理** |
| 步骤5 | 清理临时文件 | 删除中间产物 |

### 依赖

- `pandoc`：`brew install pandoc`
- `python-docx`：`pip3 install python-docx`

---

## Word 文档格式标准

### 字体规范

| 元素 | 中文字体 | 英文字体 | 字号 | 颜色 |
|-----|---------|---------|------|------|
| 正文 | 宋体 | Times New Roman | 小四（12pt） | 黑色 |
| 一级标题 | 黑体 | Arial | 三号（16pt） | 黑色 |
| 二级标题 | 黑体 | Arial | 四号（14pt） | 黑色 |
| 三级标题 | 黑体 | Arial | 小四（12pt） | 黑色 |
| 表格内容 | 宋体 | Times New Roman | 五号（10.5pt） | 黑色 |

### 段落格式

| 元素 | 行距 | 首行缩进 | 段前 | 段后 |
|-----|------|---------|------|------|
| 正文 | 1.5 倍 | 2 字符 | 0 | 0 |
| 一级标题 | 1.5 倍 | 无 | 0 | 0 |
| 二级标题 | 1.5 倍 | 无 | 0 | 0 |
| 三级标题 | 1.5 倍 | 无 | 0 | 0 |
| 表格内容 | 单倍 | 无 | 0 | 0 |

### 表格格式

| 要求 | 说明 |
|-----|------|
| 表格对齐 | 居中 |
| 单元格对齐 | 居中 |
| 表头 | 加粗，居中 |
| 表格标题 | 表格上方，格式：**表X-Y 表格名称** |

### 页面设置

| 项目 | 值 |
|-----|-----|
| 纸张大小 | A4 |
| 页边距 | 上下左右各 2.54cm（1英寸） |

---

## 执行步骤

### 1. 确定输入

根据 sections/ 目录是否存在决定输入模式：
- 存在 sections/ 目录 → 使用目录模式
- 不存在 sections/ 目录 → 使用单文件模式（用户提供合并好的 md）

### 2. 执行脚本

```bash
cd {项目目录}/项目文档/技术方案/
./scripts/markdown_to_word.sh -o 最终方案.docx sections/
```

### 3. 验证输出

检查生成的文件：
- 文件是否存在
- 章节标题是否正确（一级标题分页）
- 表格是否居中、表头是否加粗

---

## 常见问题处理

### 问题1：表格未正确转换

**原因**：表格头行与分隔行之间有空行

**解决**：脚本预处理自动修复，无需手动处理

### 问题2：python-docx 未安装

**现象**：脚本输出 `警告: python-docx 未安装，跳过后处理`

**解决**：`pip3 install python-docx`，然后重新运行脚本

### 问题3：pandoc 未安装

**现象**：`错误: pandoc 未安装`

**解决**：`brew install pandoc`

### 问题4：出现 `\newpage` 文本

**原因**：预处理时未删除

**解决**：脚本预处理自动删除

### 问题5：公式显示为原始 LaTeX 代码（如 `\frac{...}`）

**原因**：该公式语法 pandoc 不支持，fallback 处理未能正确转换

**解决**：
1. 检查 markdown 源文件中的公式语法
2. 参考 `technical-proposal-writing` skill 中的公式写作规范
3. 将不支持的语法（如 `\begin{cases}`）改为 pandoc 兼容写法
4. 重新运行 P6 合并

### 数学公式处理说明

Pandoc 将标准 LaTeX 公式直接转换为 Word OMML 格式，无需预处理。

**Pandoc 直接支持（推荐）：**
- `\frac{a}{b}`、`x_i`、`x^{2}`、`\sum`、`\int`
- `\tau`、`\gamma`、`\alpha` 等希腊字母
- `\max`、`\min`、`\sin`、`\cos` 等函数名

**Pandoc 不支持（会 fallback 为 Unicode 文本）：**
- `\begin{cases}...\end{cases}` — 分段函数环境


---

## 最终交付

```
{项目目录}/
└── 项目文档/
    └── 技术方案/
        ├── 流程状态.md          # ✅ 已完成
        ├── P1-需求分析.md       # ✅
        ├── P2-技术方案大纲.md   # ✅
        ├── P3-任务拆分计划.md   # ✅
        ├── sections/            # ✅
        └── 最终方案.docx        # ✅ 最终交付物
```

## 任务统计

输出统计信息：
- 子任务数
- 总字数
- 配图数
- 耗时

## 示例输出

```
✅ 技术方案撰写完成
├── 国航智能体/项目文档/技术方案/最终方案.docx
└── 任务统计
    ├── 子任务数：7
    ├── 总字数：15234
    ├── 配图数：4
    └── 耗时：约15分钟
```
