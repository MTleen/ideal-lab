---
name: ideal-flow-control
description: "Use when managing workflow phase transitions and state control. Triggers on: 流程状态、阶段推进、下一阶段、YOLO模式、自动迭代、工作流编排、flow state、phase control. This is the orchestration protocol — it defines how the main agent routes between phases, when to invoke phase skills, and how to coordinate the YOLO review team."
---

> **主智能体（Claude Code 会话）职责：仅编排，不执行。所有阶段内的工作（读文件、做调研、写文档）全部由 Phase Skill 通过 sub-agent 完成。**

# ideal-flow-control（流程编排协议）

## 角色定位

**主智能体 = 编排器（Orchestrator）**，永远不直接执行工作。

### 主智能体只做三件事

1. **读取** `流程状态.md`，确定当前阶段
2. **调用** Phase Skill（作为 team lead 调度 sub-agent 完成所有工作）
3. **更新** `流程状态.md`，推进到下一阶段

### 主智能体绝对不做

- ❌ 读取项目文件（代码、文档）
- ❌ 做代码分析、架构设计、风险评估
- ❌ 写文档内容
- ❌ 做技术决策
- ❌ 验证构建结果

所有上述工作由 Phase Skill 内部 spawn 的 sub-agent 完成。

---

## 核心原则

### 两种执行模式

主智能体有两种执行模式，由流程状态.md 中的 `yolo_mode` 字段控制：

| 模式 | yolo_mode | 行为 |
|------|-----------|------|
| **手动模式** | `false` | 每次阶段完成后停下来，等待用户确认后再推进 |
| **自动循环模式** | `true` | 阶段完成后不停止，自动推进直到流程完成（P15）或熔断 |

### 手动模式行为（yolo_mode: false）

```
1. 读取 流程状态.md → current_phase
2. 判断阶段类型
   ┌─────────────────────────────────────┐
   │ 产物阶段（P1/P3/P5/P7/P9/P11/P13）  │
   │   → 调用 Phase Skill                 │
   │   → 等待 Skill 返回                  │
   │   → 验证产物文件存在                │
   │   → 更新 current_phase               │
   │   → ⏸ 停下来等待用户确认            │
   ├─────────────────────────────────────┤
   │ 评审阶段（P2/P4/P6/P8/P10/P12/P14） │
   │   → 展示摘要 → 询问 YOLO → 等确认   │
   ├─────────────────────────────────────┤
   │ 交付阶段（P15）                      │
   │   → 调用 ideal-delivery             │
   │   → ⏸ 停下来等待用户确认            │
   └─────────────────────────────────────┘
```

### 自动循环模式行为（yolo_mode: true）— 核心优化

**主智能体在 YOLO 模式下是"永不停歇的循环器"**。阶段完成后**立即回到起点**，不等待用户输入，直到流程终止。

```
YOLO 自动循环：

循环（永不停止，除非满足终止条件）：
  1. 读取 流程状态.md → current_phase, status, yolo_mode
  2. 检查终止条件（见下方）→ 满足则输出结果，停止循环
  3. 确定当前阶段 X = 第一个未完成的阶段
     （遍历 P1→P2→...→P15，查找第一个状态不为 completed/approved 的阶段）
     ⚠️ 序列完整性校验：X 序号 <= current_phase → 前置阶段被跳过，输出警告并停住
  4. 如果 X 是产物阶段（P1/P3/P5/P7/P9/P11/P13）：
       → 调用 Phase Skill（内部 spawn sub-agent 完成所有工作）
       → 等待 Skill 返回
       → 验证产物文件存在且非空
       → 更新 flow state：X > current_phase 时才推进 current_phase → X，状态设为 completed/approved
       → 立即回到循环起点（步骤 1）
  5. 如果 X 是评审阶段（P2/P4/P6/P8/P10/P12/P14）：
       → 调用 panel-review（yolo_mode: true, review_target: {产物文件路径}, product_type: {见下方映射表}, phase: X）
       → 等待评审结果
       → 解析报告末尾的 JSON 判定块
       → 如果 verdict=="pass" → 更新为 approved（current_phase 不回退）→ 立即回到循环起点
       → 如果 verdict=="fail" 且同一阶段连续失败次数 < 3：
           → 根据 fatal 发现调用对应 Phase Skill 修复产物
           → 重新调用 panel-review（Phase 5 重审语义）
           → 重试计数 +1
       → 如果 verdict=="fail" 且连续失败 >= 3 次 → 输出熔断报告 → 停止循环，等待人工介入
  6. 如果 X 是交付阶段（P15）：
       → 调用 ideal-delivery
       → 等待完成
       → 更新状态为 "已完成"
       → 输出流程完成摘要 → 停止循环
```

**步骤 3 的阶段序列完整性校验（新增）**：

| 场景 | 检测逻辑 | 处理方式 |
|------|----------|----------|
| X 序号 == current_phase + 1 | 正常，下一阶段 | 继续执行 |
| X 序号 <= current_phase | **前置阶段被跳过** | 输出警告：跳过了 P{current_phase} 之前的某些阶段，停止循环，等待人工确认 |

**终止条件**（满足任一即停止）：
- `status: 已完成` 或 `status: 已交付`
- P15 阶段已完成（current_phase = P15 且评审通过）
- `panel-review` 返回 fail 且连续 3 轮失败 → 停止循环，报告未解决问题

**关键原则**：YOLO 模式下，主智能体在每次阶段完成后**立即回到循环起点**，不输出"等待用户确认"之类的提示，不停下来。循环直到终止条件满足。

---

## 阶段类型定义

| 类型 | 阶段 | 主智能体行为 |
|------|------|-------------|
| **产物阶段** | P1, P3, P5, P7, P9, P11, P13 | 调用 Phase Skill，等待完成，更新 flow state |
| **评审阶段** | P2, P4, P6, P8, P10, P12, P14 | YOLO/人工评审处理 |
| **交付阶段** | P15 | 触发 ideal-delivery |

---

## 评审阶段 → product_type 映射

YOLO 模式下调用 panel-review 时，需传递 `product_type` 参数以指导攻击面选择：

| 评审阶段 | 对应产物阶段 | product_type |
|----------|-------------|-------------|
| P2 | P1 | `requirements_doc` |
| P4 | P3 | `solution_doc` |
| P6 | P5 | `dev_plan` |
| P8 | P7 | `test_cases` |
| P10 | P9 | `code` |
| P12 | P11 | `test_results` |
| P14 | P13 | `wiki` |

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

### 主智能体调用流程（每次只推进一个阶段）

```
1. 读取 flow state → current_phase = X
2. 确定 Phase Skill 名称
3. 调用 Skill（Skill 内部 spawn sub-agent 完成所有工作）
4. 等待 Skill 返回执行摘要
5. 验证产物文件存在且非空
6. 更新 flow state：current_phase → X+1，status 更新
7. 继续循环
```

### Phase Skill 职责边界

Phase Skill 是 **team lead**，它负责：

| Phase Skill 负责 | Phase Skill 不负责 |
|------------------|-------------------|
| 读取 P1 等前置文档 | 更新 flow state |
| spawn sub-agent 调研和分析 | 验证前置条件 |
| spawn sub-agent 写文档 | 决定评审结果 |
| 写入产物文件 | 调度其他 Phase Skill |
| 返回执行摘要 | |

---

## Git Worktree 协议

### 基本原则

**整个迭代生命周期（P1 ~ P15）必须在独立的 Git Worktree 中执行**，禁止在 main 分支或 release 分支上直接进行任何迭代相关工作。

### Worktree 路径规范

```
<repo_toplevel>/worktrees/<branch>
```

| 组成部分 | 说明 |
|----------|------|
| `repo_toplevel` | `git rev-parse --show-toplevel`（仓库根目录） |
| `branch` | 功能分支名（sanitized，`/` 替换为 `-`） |

**示例**：
- 仓库路径：`/Users/foo/projects/IdealClaw`
- 功能分支：`feature/mat5-multi-layer-memory`
- Worktree 路径：`/Users/foo/projects/IdealClaw/worktrees/feature-mat5-multi-layer-memory`

### 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能分支 | `feature/<short-name>` | `feature/mat5-multi-layer-memory` |
| 修复分支 | `fix/<short-name>` | `fix/chat-api-timeout` |
| 重构分支 | `refactor/<short-name>` | `refactor/session-manager` |

> **short-name 规则**：需求 ID（如 MAT-5）+ 简短描述，不超过 50 字符

### 流程状态 Worktree 字段

在 `流程状态.md` 的 YAML frontmatter 中记录 `worktree` 字段：

```yaml
---
requirement_name: {需求名称}
current_phase: P5
status: in_progress
yolo_mode: false
worktree:
  branch: feature/mat5-multi-layer-memory
  path: /Users/foo/projects/IdealClaw/worktrees/feature-mat5-multi-layer-memory
  created_at: {YYYY-MM-DD}
created_at: {创建时间}
updated_at: {更新时间}
---
```

### Worktree 执行时机

```
[创建 worktree，分支名 feature/<short-name>]
    ↓
P1 需求编写 → P2 需求评审 → P3 技术方案 → P4 方案评审 → ... → P14 维基评审
    ↓
[P15 成果提交后删除 worktree]
```

**注意**：Worktree 在 **P1 开始前创建**，整个迭代生命周期（包含调研、文档编写、编码、测试）都在 worktree 中进行。

### 前置检测：已在 worktree 则复用（不新建）

创建 worktree 前，先检测当前是否已在 worktree 中（典型场景：被 `ideal-agent-loop` outer loop 在 goal worktree 内调用，或迭代中断后恢复）：

```bash
pwd | grep -q worktrees && git branch --show-current | grep -qE '^(feature|fix|refactor)/'
```

- **命中（已在 worktree）** → 跳过创建，复用当前 worktree，`流程状态.md` 的 `worktree` 字段填当前分支与路径。不重复 `git worktree add`，不建孤儿 worktree。
- **未命中（不在 worktree）** → 继续下方「创建 Worktree」。

> 此 guard 让 flow-control 能在被 ideal-agent-loop goal worktree 复用时正确识别并复用，也支持迭代中断后在已有 worktree 内续跑，避免重复创建。

### 创建 Worktree

```bash
# 计算 worktree 路径
REPO_PATH=$(git rev-parse --show-toplevel)
BRANCH="feature/mat5-multi-layer-memory"
SANITIZED_BRANCH=$(echo "$BRANCH" | sed 's/\//-/g')
WORKTREE_PATH="$REPO_PATH/worktrees/$SANITIZED_BRANCH"

# 创建 worktree
mkdir -p "$REPO_PATH/worktrees"
git worktree add -b "$BRANCH" "$WORKTREE_PATH"
```

### 初始化流程状态.md（P1 开始前，必须）

> 自 ideal-requirement 解耦后，`流程状态.md` 的初始化由 flow-control 负责（requirement 只落盘需求文档）。

创建 worktree 后、调用 ideal-requirement（P1）前，flow-control 必须初始化迭代目录的 `流程状态.md`：

1. 确定迭代目录：`docs/迭代/{YYYY-MM-DD}-{需求名称}/`（或 `docs/项目迭代/`）
2. 写入初始 `流程状态.md`（YAML frontmatter + 阶段状态表），`worktree` 字段填入刚创建的 worktree 分支与路径，`current_phase: P1`、`status: in_progress`
3. 随后调用 ideal-requirement 执行 P1 需求澄清与落盘

### 自动切换（关键）

**创建或识别到 worktree 后，必须立即切换进去**：

```
1. 检查当前是否在 worktree 中：
   pwd | grep worktrees
   git branch --show-current | grep -E '^feature/|^fix/|^refactor/'

2. 如不在 worktree 中，切换到 worktree 目录：
   cd /path/to/repo/worktrees/feature-{short-name}

3. 验证切换成功：
   pwd  # 确认路径包含 worktrees
   git branch --show-current  # 确认是 feature/xxx 分支
```

**重要**：切换到 worktree 后，后续所有操作都在 worktree 分支上执行，直到 P15 完成后才退出。**必须使用 `cd` 命令真正切换目录，而不仅仅是创建 worktree**。

### 质量检查清单（Worktree）

- [ ] P1 开始前已创建 worktree
- [ ] **已使用 `cd` 切换到 worktree 目录**
- [ ] 当前分支是 feature/fix/refactor 分支，不是 main/release
- [ ] `流程状态.md` 中已记录 worktree 路径
- [ ] P15 完成后已删除 worktree
- [ ] Worktree 删除后才能合并主分支

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
worktree:
  branch: feature/{short-name}
  path: {repoRoot}/worktrees/feature-{short-name}
  created_at: {YYYY-MM-DD}
created_at: {创建时间}
updated_at: {更新时间}
---
```

## 阶段状态

| 阶段 | 状态 | 更新时间 | 评审意见 |
|------|------|----------|----------|
| P1 需求编写 | ✅ completed | {时间} | - |
| P2 需求评审 | ⏳ pending | - | - |
| P3 技术方案 | ⏳ pending | - | - |
| P4 方案评审 | ⏳ pending | - | - |
| ... | ... | ... | ... |
| P15 成果提交 | ⏳ pending | - | - |

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
| P2 → P3 | P2 approved | 展示摘要 → 询问 YOLO → 人工确认"通过" | 自动调用 panel-review |
| P3 → P4 | P3 completed | 自动 | 自动 |
| P4 → P5 | P4 approved | 人工说"通过" | 自动调用 panel-review |
| P5 → P6 | P5 completed | 自动 | 自动 |
| P6 → P7 | P6 approved | 人工说"通过" | 自动调用 panel-review |
| P7 → P8 | P7 completed | 自动 | 自动 |
| P8 → P9 | P8 approved | 人工说"通过" | 自动调用 panel-review |
| P9 → P10 | P9 completed | 自动 | 自动 |
| P10 → P11 | P10 approved | 人工说"通过" | 自动调用 panel-review |
| P11 → P12 | P11 completed | 自动 | 自动 |
| P12 → P13 | P12 approved | 人工说"通过" | 自动调用 panel-review |
| P13 → P14 | P13 completed | 自动 | 自动 |
| P14 → P15 | P14 approved | 自动 | 自动，触发 ideal-delivery |

---

## 评审阶段处理

### YOLO 自动循环模式（`yolo_mode: true`）

YOLO 模式下，主智能体永不停止，直到流程完成或熔断：

1. **产物阶段完成 → 自动推进**：调用对应 Phase Skill，完成后立即更新 flow state 并进入下一阶段
2. **评审阶段**：自动调用 `panel-review` 执行评审
   - `panel-review` 返回 verdict=="pass" → 更新为 approved，立即推进到下一阶段
   - `panel-review` 返回 verdict=="fail" 且连续 3 轮失败 → 输出熔断报告，停止循环，等待人工介入
3. **P15 交付阶段**：调用 `ideal-delivery`，完成后更新状态为"已完成"，输出流程完成摘要

**熔断处理**：当评审返回熔断信号时，主智能体停止循环，输出完整的熔断报告（包括未解决的问题列表），等待人工处理。人工介入后，可选择：
- 修复问题后继续（保持 YOLO 模式）
- 切换回手动模式
- 中止流程

### 人工模式（默认，`yolo_mode: false`）

```
1. 产物阶段完成后 → 停下来，展示产物摘要
2. 评审阶段完成后：
   a) 展示评审摘要
   b) 询问是否进入 YOLO 模式（见下方选项）
   c) 等待用户响应：
      - "通过" / "ok" / "approved" → 更新为 approved，推进下一阶段（保持人工模式）
      - "YOLO" / "启用 YOLO" / "yolo" → yolo_mode 改为 true → 输出"YOLO 模式已启用，后续自动推进"，继续推进
      - "通过，YOLO" → 同时更新 approved + yolo_mode: true
      - 其他反馈 → 记录反馈，等待进一步指示
```

**YOLO 模式提示词（每次评审阶段必须展示）**：

```
评审摘要已生成。
请选择后续处理方式：
  1. [通过] — 继续下一阶段（保持手动模式）
  2. [通过，启用 YOLO] — 通过并启用 YOLO 模式，后续评审自动推进
  3. [启用 YOLO] — 不通过评审但启用 YOLO 模式，让 AI 自动迭代修复
  4. [其他反馈] — 提供具体修改意见
```

**切换到 YOLO 模式**：修改流程状态.md 中 `yolo_mode: false` → `yolo_mode: true`，后续所有评审阶段自动走 panel-review，无需再次触发。

---

## 质量检查清单

### YOLO 模式下每次循环迭代必须验证

- [ ] flow state 文件格式正确（YAML frontmatter 有效）
- [ ] **阶段序列完整性：查找到的第一个未完成阶段序号 <= current_phase + 1**
- [ ] 当前阶段的前置条件已满足（completed/approved）
- [ ] 产物文件已写入正确路径
- [ ] 产物内容非空
- [ ] 时间戳已更新
- [ ] 流程状态.md 中状态字段正确反映当前阶段
- [ ] 熔断信号被正确识别并处理（停止循环，报告问题）
- [ ] 流程完成时输出完整执行摘要
- [ ] **当前在 worktree 中执行（pwd 包含 worktrees）**

### 通用质量要求

- [ ] P2 评审阶段已展示 YOLO 模式选项提示
- [ ] 主智能体未直接执行任何阶段内工作（全部由 Skill 调度 sub-agent 完成）
- [ ] YOLO 模式下阶段完成后立即回到循环起点，不停下来等待用户
- [ ] P1 开始前已创建 worktree（路径格式：`<repo_toplevel>/worktrees/<branch>`）
- [ ] **已使用 `cd` 切换到 worktree 目录**
- [ ] 当前分支是 feature/fix/refactor 分支，不是 main/release
- [ ] `流程状态.md` 中已记录 worktree 路径

---

## 异常处理

| 场景 | 处理 |
|------|------|
| Phase Skill 调用失败（超时/错误） | 输出错误信息，标记当前阶段为 blocked，停止循环等待人工介入 |
| `流程状态.md` 不存在或格式损坏 | 输出错误："流程状态文件缺失或损坏，请从 P1 重新初始化"，停止 |
| Worktree 创建失败（分支已存在/权限不足） | 输出具体错误原因，让用户选择：手动创建 / 切换已有 worktree / 跳过 worktree 在当前位置执行 |
| Worktree 目录不存在（被手动删除） | 重新创建 worktree 或提示用户手动恢复 |
| YOLO 循环内同一阶段连续 3 次重试仍失败 | 标记该阶段为 blocked，输出熔断报告，停止循环 |
| 评审阶段 panel-review 不可用 | 退化为人工评审模式，展示产物摘要并等待用户确认 |
| 产物文件写入后为空 | 不推进 current_phase，标记阶段为 revision，提示 Phase Skill 重新执行 |
