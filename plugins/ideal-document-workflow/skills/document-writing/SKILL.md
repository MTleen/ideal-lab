---
name: document-writing
description: |
  结构化文档 P7 并行写作阶段。当需要根据大纲和任务拆分执行并行写作时使用。
  触发场景：(1) workflow 调用本 skill (2) 用户要求"写章节"、"开始写作"
  核心功能：基于写作任务卡执行内容写作，使用 What-Why-How 模式确保内容完整。
io:
  inputs:
    - name: task_split
      source: task-split.task_split
    - name: requirement_doc
      source: requirement-analysis.requirement_doc
  outputs:
    - name: sections
      path: "sections/"
      type: markdown
---

# Document Writing (P7)

## Overview

根据任务拆分结果，执行并行写作，生成各章节的 Markdown 内容。

**核心原则：**
- 内容真实，不虚构信息
- 所有引用标注来源
- 使用 What-Why-How 模式确保内容完整
- **严格遵循写作风格规范**（详见 @references/writing_style_guide.md）
- **按需调研，不强制但可用**

## 输入

- P3-任务拆分.md（任务卡片）
- P1-需求分析.md（背景信息）
- P2-大纲.md（结构参考）
- 项目目录和文档名称
- 原始材料路径（可选，用于本地调研）

## 调研决策

**按需调研**：每个任务写作之前，判断是否需要调研。

### 判断逻辑

```
任务需要线上调研？
├── 技术细节需要外部验证 → 调用 ideal-deep-research
├── 竞品信息需要补充 → 调用 ideal-deep-research
└── 不需要

任务需要本地调研？
├── 需要从源码提取技术细节 → 读取源码
├── 需要从设计文档提取信息 → 读取文档
└── 不需要（P2/P3 阶段已完成调研）
```

### 调研类型

| 类型 | 触发条件 | 执行方式 |
|------|---------|---------|
| **线上调研** | 技术细节验证、竞品对比、行业背景 | 调用 `ideal-deep-research` |
| **本地调研** | 需要从源码/设计文档提取信息 | 读取对应文件 |

### 调研执行时机

调研可以发生在：
1. **任务开始前** — 针对整个任务的需要
2. **写作过程中** — 针对特定技术点/功能点的需要

```
调研流程（按需）：

每个任务卡片：
  1. 分析任务需求
  2. 判断是否需要调研
  3. 如果需要线上调研 → 调用 ideal-deep-research
  4. 如果需要本地调研 → 读取源码/文档
  5. 基于调研结果写作
```

## 写作模式

### What-Why-How 模式

每个功能点/技术选型使用此模式：

```
**[内容]是什么**
[Technology/功能]是一种[Definition]。

**[为什么选择]**
选择它是因为[Reason 1]、[Reason 2]和[Reason 3]。

**[如何实现]**
在实现上，将[Implementation Details]。

**[优势]**
这种方案的优势在于[Advantage 1]和[Advantage 2]。
```

### 比较模式

```
**[传统方法]**
[传统 Approach] + [局限性]

**[本方案]**
[Our Approach] + [优势]

**[对比结果]**
[量化对比]
```

### 分层架构模式

```
**[整体架构]**
[高层概述]

**[第一层]**
[Layer 1] - [功能] - [技术选型]

**[第二层]**
[Layer 2] - [功能] - [技术选型]

**[层间交互]**
[层之间如何交互]
```

## 输出

`{项目目录}/文档产出/sections/{章节文件名}.md`

## 执行步骤

### Step 1: 读取任务卡片

从 P3-任务拆分.md 读取任务列表，选定要执行的任务。

### Step 2: 收集上下文

收集任务所需的上下文信息：
- 来源需求（P1-需求分析.md）
- 上级概述（P2-大纲.md）
- 同级任务标题（避免重复）

### Step 3: 判断调研需求

```
对于当前任务：
  分析任务中的写作要点

  如果有"需要线上调研"的需求：
    → 调用 ideal-deep-research
    → 等待研究结果

  如果有"需要本地调研"的需求：
    → 读取对应源码/文档
    → 提取所需信息

  如果都不需要：
    → 直接进入 Step 4
```

### Step 4: 执行写作

按照任务卡片的写作要点执行写作：
1. 使用 What-Why-How 模式
2. **严格遵循 @references/writing_style_guide.md 中的写作风格规范**
3. 引用来源标注
4. 保持与大纲一致

### Step 5: 保存文件

保存到 `{项目目录}/文档产出/sections/{章节文件名}.md`

## 质量检查

写作完成后，按 @references/writing_style_guide.md 中的质量检查清单逐项自检。

## 参考文档

- **@references/writing_style_guide.md** — 完整写作风格规范（含常见问题修复）
