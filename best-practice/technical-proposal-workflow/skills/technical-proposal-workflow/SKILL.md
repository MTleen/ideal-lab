---
name: technical-proposal-workflow
description: |
  技术方案撰写编排工作流。当用户需要根据需求文档编写技术方案时使用。
  触发场景：(1) 用户要求"写技术方案"、"编写技术标书" (2) 用户提供了需求文档希望生成完整技术方案
  核心功能：协调各阶段 skill 完成需求分析→大纲生成→任务拆分→并行写作→配图→合并输出。
  各阶段之间设有审核关卡（AskUserQuestion），需要人工确认后方可进入下一阶段。
  本 skill 为编排器，负责阶段流转和状态管理，各阶段实现详见独立 skills。
---

# Technical Proposal Workflow

## Overview

技术方案撰写编排工作流，协调多个 specialized skills 完成从需求到 Word 交付物的全流程。

**核心原则：每个阶段完成后必须经过人工审核，确认通过后才能进入下一阶段。**

**阶段 Skills 映射：**

| 阶段 | Skill | 产出 | 审核要点 |
|------|-------|------|----------|
| P1 | `technical-proposal-analysis` | P1-需求分析.md | 功能/非功能需求是否完整、用户是否认可 |
| P2 | `technical-proposal-outline` | P2-技术方案大纲.md | 章节结构是否合理、篇幅分配是否恰当 |
| P3 | `technical-proposal-task-split` | P3-任务拆分计划.md | 任务划分是否合理、并行度是否充足 |
| P4 | `technical-proposal-writing` | sections/*.md | 内容是否符合大纲、写作质量是否达标 |
| P5 | `technical-proposal-illustration` | sections/*.md + images/ | 配图是否恰当、位置是否正确 |
| P6 | `technical-proposal-merge` | 最终方案.docx | 文档格式是否符合规范、内容是否完整 |

## 使用方式

### 1. 初始化项目

首次使用时，需要指定项目信息：

```bash
# 用户指定
项目目录：国航智能体/
方案名称：IT运维助手技术方案
```

### 2. 阶段执行模式

本 workflow 采用**阶段制执行 + 审核制流转**：

1. **读取状态** — 读取 `流程状态.md` 获取当前阶段
2. **执行阶段** — 调用对应的 phase skill 生成产出
3. **人工审核** — 输出审核要点，等待用户确认（使用 AskUserQuestion）
4. **更新状态** — 用户确认后更新流程状态，进入下一阶段
5. **循环** — 重复步骤 1-4，直到所有阶段完成

**重要：步骤 3 的审核是强制性的，AI 不会自动跳到下一阶段。**

### 3. 流程状态文件

**位置：** `{项目目录}/项目文档/技术方案/流程状态.md`

```yaml
---
project_dir: {项目目录}
project_name: {方案名称}
current_phase: P1
status: pending_review
created_at: {创建时间}
updated_at: {更新时间}
review_phase: P1
---

## 阶段状态

| 阶段 | 状态 | 完成时间 | 产出 |
|------|------|----------|------|
| P1 需求分析 | ⏳ 待审核 | - | P1-需求分析.md |
| P2 大纲生成 | ⏳ pending | - | P2-技术方案大纲.md |
| P3 任务拆分 | ⏳ pending | - | P3-任务拆分计划.md |
| P4 并行写作 | ⏳ pending | - | sections/ |
| P5 智能配图 | ⏳ pending | - | sections/ + images/ |
| P6 文档合并 | ⏳ pending | - | 最终方案.docx |
```

## 目录结构

```
{项目目录}/
└── 项目文档/
    └── 技术方案/
        ├── 流程状态.md
        ├── P1-需求分析.md
        ├── P2-技术方案大纲.md
        ├── P3-任务拆分计划.md
        ├── P4-评审交流.md
        ├── P5-评审交流.md
        ├── sections/
        ├── images/
        └── 最终方案.docx
```

## 完整执行流程

### Step 1: 检查项目状态

1. 检查 `{项目目录}/项目文档/技术方案/流程状态.md` 是否存在
2. 如果不存在，创建新项目（生成初始 `流程状态.md`）
3. 如果存在，读取当前阶段 `current_phase`

### Step 2: 执行当前阶段

根据 `current_phase` 调用对应的 skill：

```
P1 → technical-proposal-analysis
P2 → technical-proposal-outline
P3 → technical-proposal-task-split
P4 → technical-proposal-writing
P5 → technical-proposal-illustration
P6 → technical-proposal-merge
```

阶段执行完成后，**必须立即进入 Step 3 审核环节，不得自动进入下一阶段。**

### Step 3: 人工审核（强制关卡）

阶段产出生成后，使用 `AskUserQuestion` 工具向用户展示审核要点并请求确认：

**审核选项设计（统一模板）：**

```json
{
  "header": "审核确认",
  "question": "【{phase}阶段产出已生成】\n\n请审阅以下产出，确认是否通过：\n\n📄 产出文件：{output_file}\n📝 审核要点：{review_points}\n\n如有问题请选择「需要修改」，我会指出具体问题；\n确认无误后选择「通过」，进入下一阶段。",
  "options": [
    {"label": "通过，进入下一阶段", "description": "产出符合要求，继续执行 workflow"},
    {"label": "需要修改", "description": "有问题需要修正，请详细说明"}
  ],
  "multiSelect": false
}
```

**各阶段审核要点：**

| 阶段 | 产出文件 | 审核要点 |
|------|----------|----------|
| P1 | P1-需求分析.md | 功能需求是否覆盖所有用例？非功能需求（性能/安全/可靠性）是否明确？是否有遗漏的业务场景？ |
| P2 | P2-技术方案大纲.md | 章节结构是否合理？每章篇幅是否符合要求？核心章节是否有遗漏？ |
| P3 | P3-任务拆分计划.md | 任务粒度是否恰当？并行度是否足够？依赖关系是否正确？写作要求中是否包含技术调研前置要求和公式规范要求？ |
| P4 | sections/*.md | 内容是否与大纲一致？写作风格是否符合规范？是否存在事实错误或逻辑问题？每个章节是否包含技术调研段落？涉及计算/评估的章节是否包含公式？ |
| P5 | sections/*.md + images/ | 配图是否与内容相关？图表说明是否清晰？是否有冗余或无关图片？ |
| P6 | 最终方案.docx | 格式是否符合规范？目录、页眉页脚是否正确？内容是否有遗漏？ |

### Step 4: 处理审核结果

**如果用户选择「通过」：**
1. 更新 `流程状态.md` 中该阶段状态为 ✅ completed
2. `current_phase` +1
3. `status` 设为 `pending_review`
4. `review_phase` 设为当前阶段
5. 返回 Step 1 继续

**如果用户选择「需要修改」：**
1. 记录用户反馈的问题
2. 调用对应 phase skill 进行修改
3. 修改完成后重新进入 Step 3 审核
4. 每次修改后都必须再次审核，不得跳过

### Step 5: 完成

所有阶段（ P1-P6）状态均为 ✅ completed 时，输出最终文档路径并通知用户。

## 状态流转图

```
[初始化] → P1执行 → [审核关卡] → 通过? ─┐
                                      ↓否
           ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
           ↓是
P2执行 → [审核关卡] → 通过? ─┐
                            ↓否
...
P6执行 → [审核关卡] → 通过? ─┐
                            ↓否
           ← ← ← ← ← ← ← ← ← ←
           ↓是
        [完成]
```

## 阶段跳过与回退

### 跳过阶段（谨慎使用）

用户可以显式指定跳过某个已完成或不需要的阶段：
- `--skip-p4` 跳过并行写作（使用已有 sections/）
- 跳过前需要确认：用户提供已有文件、或明确授权使用旧版本

### 回退到上一阶段

用户可以要求回退到之前的阶段重新修改：
- 状态文件中记录回退历史
- 后续阶段的状态自动降级为需重新执行

## 流程状态字段说明

| 字段 | 说明 |
|------|------|
| `current_phase` | 当前待执行的阶段编号（P1-P6） |
| `status` | `pending_review`=待审核, `in_progress`=执行中, `completed`=全部完成 |
| `review_phase` | 当前正在审核的阶段编号 |
| 阶段状态 | ⏳ pending=待执行, ⏳ 进行中=执行中, ✅ completed=已完成, ❌ 需修改=审核未通过 |

## 相关 Skills

- `technical-proposal-analysis` - P1 需求分析
- `technical-proposal-outline` - P2 大纲生成
- `technical-proposal-task-split` - P3 任务拆分
- `technical-proposal-writing` - P4 并行写作
- `technical-proposal-illustration` - P5 智能配图
- `technical-proposal-merge` - P6 文档合并
