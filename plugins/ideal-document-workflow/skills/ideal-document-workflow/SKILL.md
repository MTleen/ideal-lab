---
name: ideal-document-workflow
description: |
  结构化文档写作编排工作流。当用户需要撰写结构化长文档（技术方案、知识库文档、汇报材料等）时使用。
  核心功能：协调各阶段 skill 完成需求分析→大纲生成→任务拆分→并行写作→配图→渲染输出。
  各阶段之间设有审核关卡，需要人工确认后方可进入下一阶段。
  本 skill 为编排器，负责阶段流转和状态管理，各阶段实现详见独立 skills。
---

# Ideal Document Workflow

## 角色定位

**主智能体 = 编排器（Orchestrator）**，永远不直接执行工作。

### 主智能体只做三件事

1. **读取** `流程状态.md`，确定当前阶段
2. **调用** Phase Skill（内部 spawn sub-agent 完成所有工作）
3. **更新** `流程状态.md`，推进到下一阶段

### 主智能体绝对不做

- ❌ 读取项目文件
- ❌ 做技术分析
- ❌ 写文档内容
- ❌ 做评审
- ❌ 修改文档

所有上述工作由 Phase Skill 或评审团队内部 spawn 的 sub-agent 完成。

---

## 核心原则

### 两种执行模式

主智能体有两种执行模式，由 `流程状态.md` 中的 `yolo_mode` 字段控制：

| 模式 | yolo_mode | 行为 |
|------|-----------|------|
| **手动模式** | `false` | 每次阶段完成后停下来，等待用户确认后再推进 |
| **YOLO模式** | `true` | 阶段完成后不停止，自动推进直到流程完成或熔断 |

### 产物阶段 vs 评审阶段

| 类型 | 阶段 | 主智能体行为 |
|------|------|-------------|
| **产物阶段** | P1, P3, P5, P7, P9, P11 | 调用 Phase Skill，等待完成，更新状态 |
| **评审阶段** | P2, P4, P6, P8, P10 | 调用评审团队，结果通过则 approved，熔断则停住 |

---

## 完整执行流程

### 手动模式行为（yolo_mode: false）

```
1. 读取 流程状态.md → current_phase
2. 判断阶段类型
   ┌─────────────────────────────────────┐
   │ 产物阶段（P1/P3/P5/P7/P9/P11）      │
   │   → 调用 Phase Skill                 │
   │   → 等待 Skill 返回                 │
   │   → 验证产物文件存在               │
   │   → 更新状态                       │
   │   → ⏸ 停下来等待用户确认         │
   ├─────────────────────────────────────┤
   │ 评审阶段（P2/P4/P6/P8/P10）        │
   │   → 调用评审团队                   │
   │   → 展示摘要 → 等待用户确认       │
   ├─────────────────────────────────────┤
   │ 交付阶段（P12）                    │
   │   → 调用 document-render           │
   │   → ⏸ 停下来等待用户确认         │
   └─────────────────────────────────────┘
```

### YOLO模式行为（yolo_mode: true）

**主智能体在 YOLO 模式下是"永不停歇的循环器"。**

```
YOLO 自动循环：

循环（永不停止，除非满足终止条件）：
  1. 读取 流程状态.md → current_phase, status, yolo_mode
  2. 检查终止条件 → 满足则输出结果，停止循环
  3. 确定当前阶段 X = 第一个未完成的阶段
     （遍历 P1→P2→...→P12，查找第一个状态不为 completed/approved 的阶段）
  4. 如果 X 是产物阶段：
       → 调用 Phase Skill
       → 等待完成
       → 验证产物文件存在且非空
       → 更新状态
       → 立即回到循环起点
  5. 如果 X 是评审阶段：
       → 调用 panel-review（yolo_mode: true, review_target: {产物路径}, product_type: {见下方映射表}, phase: X）
       → 等待评审结果，解析 JSON 判定块
       → 如果 verdict=="pass" → 更新为 approved → 立即回到循环起点
       → 如果 verdict=="fail":
           a. 将 panel-review 报告中的 fatal/severe 发现发给 modifier agent
           b. modifier 按 P0（fatal）/P1（severe）/P2（minor）规则修复文档
           c. 重新调用 panel-review（Phase 5 重审语义）
           d. 最多 3 轮
           e. 连续 3 轮 verdict=="fail" → 输出熔断报告 → 停止循环，等待人工介入
  6. 如果 X 是交付阶段（P12）：
       → 调用 document-render
       → 等待完成
       → 更新状态为 "已完成"
       → 输出流程完成摘要 → 停止循环
```

**终止条件**（满足任一即停止）：
- `status: 已完成` 或 `status: 已交付`
- P12 阶段已完成
- panel-review 返回 verdict=="fail" 且连续 3 轮失败 → 停止循环，报告未解决问题

---

## 评审机制：panel-review + modifier

### 架构

评审分为两步：**panel-review 负责审查**（动态角色生成、多维攻击面），**modifier agent 负责修复**（读取审查报告、按优先级修改文档）。

### 评审阶段 → product_type 映射

| 评审阶段 | 对应产物阶段 | product_type | 产物文件 |
|----------|-------------|-------------|----------|
| P2 | P1 | `requirements_doc` | `P1-需求分析.md` |
| P4 | P3 | `document_outline` | `P2-大纲.md` |
| P6 | P5 | `task_split` | `P3-任务拆分.md` |
| P8 | P7 | `document_sections` | `sections/*.md` |
| P10 | P9 | `illustrated_doc` | `sections/*.md` + `images/` |

### 评审流程详解

```
评审阶段（P2/P4/P6/P8/P10）:

Step 1: 调用 panel-review（yolo_mode: true, review_target, product_type, phase）
  → panel-review 动态生成审查角色，执行多维攻击面审查
  → 输出报告 + JSON 判定块

Step 2: 解析 verdict
  → verdict=="pass" → approved → 继续下一个阶段
  → verdict=="fail" → 进入 Step 3

Step 3: modifier 修复（仅当 verdict=="fail"）
  → 将 panel-review 报告中的 fatal/severe 发现发给 modifier agent
  → modifier 按优先级分类：
      P0（fatal）：必须修复
      P1（severe）：应该修复
      P2（minor）：可跳过
  → modifier 直接编辑文档文件，输出修改报告

Step 4: 复查
  → 重新调用 panel-review（Phase 5 重审语义）
  → 验证修改后的文档

循环上限：最多 3 轮（Step 1→4 为 1 轮）
连续 3 轮 verdict=="fail" → 熔断 → 输出熔断报告 → 停止循环，等待人工介入
```

**⚠️ 关键警告**：评审阶段绝对不能跳过 modifier 直接进入下一产物阶段。modifier 必须：
1. 读取 panel-review 的报告（特别是 fatal/severe 发现）
2. 整合为统一的修改方案（区分 P0/P1/P2 优先级）
3. 执行文档修改
4. 等待复查确认

### 熔断机制

```
评审循环（最多3轮）：
  第1轮：panel-review → modifier 修复
         ↓
  第2轮：panel-review（重审）→ modifier 修复
         ↓
  第3轮：panel-review（重审）→ modifier 修复
         ↓
  如果 panel-review 仍然返回 verdict=="fail" → 熔断
```

**熔断后处理：** 输出熔断报告，停止循环，等待人工介入。

---

## 流程状态文件

**位置：** `{项目目录}/文档产出/流程状态.md`

```yaml
---
project_dir: {项目目录}
document_name: {文档名称}
document_type: {文档类型}
target_reader: {目标读者}
output_format: markdown  # markdown / docx / pptx
current_phase: P1
status: in_progress
yolo_mode: false
created_at: {创建时间}
updated_at: {更新时间}
---

## 阶段状态

| 阶段 | 类型 | 状态 | 完成时间 | 产出 |
|------|------|------|----------|------|
| P1 | 产物 | ⏳ pending | - | P1-需求分析.md |
| P2 | 评审 | ⏳ pending | - | - |
| P3 | 产物 | ⏳ pending | - | P2-大纲.md |
| P4 | 评审 | ⏳ pending | - | - |
| P5 | 产物 | ⏳ pending | - | P3-任务拆分.md |
| P6 | 评审 | ⏳ pending | - | - |
| P7 | 产物 | ⏳ pending | - | sections/ |
| P8 | 评审 | ⏳ pending | - | - |
| P9 | 产物 | ⏳ pending | - | sections/ + images/ |
| P10 | 评审 | ⏳ pending | - | - |
| P11 | 产物 | ⏳ pending | - | 最终交付物 |
| P12 | 交付 | ⏳ pending | - | - |

## 评审历史

| 阶段 | 轮次 | 评审结果 | 说明 |
|------|------|----------|------|
```

---

## 目录结构

```
{项目目录}/
└── 文档产出/
    ├── 流程状态.md
    ├── P1-需求分析.md
    ├── P2-大纲.md
    ├── P3-任务拆分.md
    ├── sections/
    ├── images/
    └── 最终交付物
```

---

## Phase Skill 映射

| 阶段 | Skill | 产出 |
|------|-------|------|
| P1 | `requirement-analysis` | P1-需求分析.md |
| P3 | `outline-generation` | P2-大纲.md |
| P5 | `task-split` | P3-任务拆分.md |
| P7 | `document-writing` | sections/*.md |
| P9 | `illustration` | sections/*.md + images/ |
| P11 | `document-render` | 最终交付物 |

---

## 相关 Skills

- `requirement-analysis` - P1 需求分析
- `outline-generation` - P3 大纲生成
- `task-split` - P5 任务拆分
- `document-writing` - P7 并行写作
- `illustration` - P9 智能配图
- `document-render` - P11 渲染输出
- `writing-skills` - 写作规范
