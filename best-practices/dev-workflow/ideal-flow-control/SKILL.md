---
name: ideal-flow-control
description: Use when managing workflow phase transitions and state control. This is the orchestration protocol — it defines how the main agent routes between phases, when to invoke phase skills, and how to coordinate the YOLO review team. Handle with care: state updates here drive the entire workflow.
---

> **agents**: Orchestrator skill — 不通过 Task 工具调度子代理，由主智能体直接执行。

# ideal-flow-control（流程编排协议）

## 角色定位

flow-control **不是执行者**，而是**编排协议**。

它定义了三件事：
1. **当前阶段是什么** — 通过读取 `流程状态.md`
2. **应该做什么** — 执行阶段产物，或等待评审
3. **如何推进** — 调用 Phase Skill，或协调 Review Team

**主智能体（Claude Code 会话）**只负责协调流程走向：
- 读取 flow state，判定当前阶段类型
- 调用 Phase Skill 或 ideal-yolo
- 更新 flow state 的 current_phase
- **不负责**：实际评审判断、决定是否修改文档（全部由 Review Team 内部处理）

**主智能体**（Claude Code 会话）按照本协议执行，每次只推进一个阶段。

---

## 核心原则

主智能体行为循环：

```
读取流程状态 → 判定当前阶段类型
       ↓
┌─────────────────────────────────┐
│  yolo_mode = true？              │
│    → 评审阶段？直接调用 ideal-yolo │
│    → 执行阶段？调用 Phase Skill   │
│    → P15？调用 ideal-delivery   │
├─────────────────────────────────┤
│  yolo_mode = false（人工模式）？  │
│  ┌──────────────────────────────┤
│  │ 执行阶段？                    │
│  │   → 调用 Phase Skill        │
│  │   → 验证产物文件已写入       │
│  │   → 更新 current_phase      │
│  ├──────────────────────────────┤
│  │ 评审阶段？                   │
│  │   → 展示产物摘要            │
│  │   → 等待用户响应            │
│  │   · "通过" → approved       │
│  │   · "YOLO" → 切换为 YOLO 模式│
│  │   · 其他反馈 → 记录反馈     │
│  └──────────────────────────────┤
└─────────────────────────────────┘
```

**YOLO 模式全流程自动化**：一旦 `yolo_mode: true`，所有评审阶段自动调用 `ideal-yolo`，无需人工介入。主智能体持续推进直到 P15 完成或遇到熔断。

---

## 阶段类型定义

| 类型 | 阶段 | 主智能体行为 |
|------|------|-------------|
| **产物阶段** | P1, P3, P5, P7, P9, P11, P13 | 调用 Phase Skill，生成产物文件 |
| **评审阶段** | P2, P4, P6, P8, P10, P12, P14 | 等待评审，通过后推进 |
| **交付阶段** | P15 | 触发 ideal-delivery |

---

## Phase Skill 调用协议

### 阶段 → Skill 映射

| 阶段 | Phase Skill |
|------|-------------|
| P1 | `ideal-requirement` |
| P3 | `ideal-dev-solution` |
| P5 | `ideal-dev-plan` |
| P7 | `ideal-test-case` |
| P9 | `ideal-dev-exec` |
| P11 | `ideal-test-exec` |
| P13 | `ideal-wiki` |

### 调用流程

```
1. 读取 flow state，获取 current_phase
2. 根据 current_phase 确定调用的 Phase Skill
3. 读取前置阶段产物和项目上下文
4. 调用 Phase Skill（通过 Task 工具）
5. Phase Skill 返回后：
   - 验证产物文件已写入正确路径
   - 更新 flow state：current_phase 指向下一个阶段
   - 判断下一阶段类型并进入对应处理
```

### Phase Skill 职责边界

| Phase Skill 负责 | Phase Skill 不负责 |
|------------------|-------------------|
| 加载所需上下文 | 更新 flow state |
| 调度子智能体执行任务 | 验证前置条件 |
| 将产物写入文件系统 | 协调评审 |
| 返回执行摘要 | |

---

## 流程状态文件协议

**路径**：`docs/迭代/{需求名称}/流程状态.md`

**格式**：

```yaml
---
requirement_name: {需求名称}
current_phase: P1
status: in_progress
yolo_mode: false
created_at: {创建时间}
updated_at: {更新时间}
---

## 阶段状态

| 阶段 | 状态 | 更新时间 | 评审意见 |
|------|------|----------|----------|
| P1 需求编写 | ✅ completed | {时间} | - |
| P2 需求评审 | ⏳ pending | - | - |
```

**状态枚举**：

| 值 | 含义 |
|----|------|
| `pending` | 未开始 |
| `in_progress` | 进行中 |
| `completed` | 已完成 |
| `approved` | 评审通过 |
| `blocked` | 被阻塞 |

**阶段推进规则**：

| 当前阶段 | 前置条件 | 人工模式推进动作 | YOLO 模式推进动作 |
|----------|----------|------------------|------------------|
| P1 → P2 | P1 completed | 自动 | 自动 |
| P2 → P3 | P2 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P3 → P4 | P3 completed | 自动 | 自动 |
| P4 → P5 | P4 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P5 → P6 | P5 completed | 自动 | 自动 |
| P6 → P7 | P6 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P7 → P8 | P7 completed | 自动 | 自动 |
| P8 → P9 | P8 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P9 → P10 | P9 completed | 自动 | 自动 |
| P10 → P11 | P10 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P11 → P12 | P11 completed | 自动 | 自动 |
| P12 → P13 | P12 approved | 人工说"通过" | 自动调用 ideal-yolo |
| P13 → P14 | P13 completed | 自动 | 自动 |
| P14 → P15 | P14 approved | 自动 | 自动，触发 ideal-delivery |

> **关键区别**：YOLO 模式下，评审阶段无需等待人工响应，自动调用 `ideal-yolo` 推进。

---

## 评审阶段处理

**YOLO 模式**（`yolo_mode: true`）：

- 主智能体自动调用 `ideal-yolo` 执行评审，无需人工介入
- `ideal-yolo` 返回"通过"→ 更新评审阶段为 approved，推进下一阶段
- `ideal-yolo` 返回"熔断"→ 报告未解决问题，流程暂停，等待人工介入
- 熔断之外，主智能体持续推进直到 P15 完成

**人工模式**（默认，`yolo_mode: false`）：

```
1. 展示当前阶段产物摘要
2. 等待用户响应：
   - "通过" / "ok" / "approved" → 更新评审阶段为 approved，推进下一阶段
   - "YOLO" / "启用 YOLO" → 将流程状态.md 中 yolo_mode 改为 true，继续推进
   - 其他反馈 → 记录反馈，等待进一步指示
```

**切换到 YOLO 模式**：修改流程状态.md 中 `yolo_mode: false` → `yolo_mode: true`，后续所有评审阶段自动走 ideal-yolo，无需再次触发。

---

## 质量检查清单

每次推进阶段前必须验证：

- [ ] flow state 文件格式正确（YAML frontmatter 有效）
- [ ] 前置阶段状态为 completed 或 approved
- [ ] 产物文件已写入正确路径
- [ ] 产物内容非空
- [ ] 时间戳已更新
