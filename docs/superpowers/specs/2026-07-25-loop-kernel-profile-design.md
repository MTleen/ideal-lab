# ideal-agent-loop / ideal-backlog 2.0：Loop Kernel + Profile 设计

- **日期**：2026-07-25
- **状态**：方向已确认，待实施
- **涉及插件**：`ideal-agent-loop`、`ideal-backlog`
- **当前基线**：`ideal-agent-loop@1.2.0`、`ideal-backlog@1.1.0`
- **设计来源**：IdealClaw 开发闭环、私有学术生产 Loop、OpenAI / Anthropic / GitHub Agent 工程实践

---

## 1. 背景

现有两个插件已经具备可复用 Loop 的雏形：

- `ideal-backlog` 维护 Goal、优先级、执行状态、质量状态、证据和 reopen 记录。
- `ideal-agent-loop` 提供外层需求池消费、内层验收标准迭代、worktree 隔离和质量闭环。

但当前契约仍然以软件开发为中心：

1. worktree、merge gate 和 `ideal-dev-workflow` 接近硬编码。
2. 内层循环以逐条 criterion 修复为主，没有显式 Stage Task DAG。
3. Markdown、`.agent-loop/` JSON 和派生文档可能形成多套状态真相。
4. Stop Hook 强调持续运行，不能自然表达 `waiting`、`human_gate` 和无工作可做。
5. Skill 路由依赖自然语言约定，缺少机器可检查的 capability contract。
6. 执行、验证、验收之间缺少统一的不可变 Run Envelope。
7. 评审失败可能继续派生评审或验证建设任务，产生“为了验证而验证”的递归。

本设计将两插件重构为通用控制面，使新领域能够通过 Profile 快速建立可靠 Loop，而不是复制一套新的 controller。

---

## 2. 设计原则

### 2.1 Kernel 保持小而稳定

Kernel 只实现 Goal、Stage、Task、Capability、Run、Gate、Checkpoint、Reopen 等通用原语。论文、开发、文档等领域阶段不进入 Kernel。

这符合 Anthropic 的“优先使用简单、可组合模式”原则，也符合 OpenAI 从单 Agent、清晰工具和明确退出条件逐步增加编排复杂度的建议。

### 2.2 Backlog 是唯一 Goal 真相

`ideal-backlog` 是 Goal 状态、当前阶段、阻塞原因和质量结论的唯一机器事实源。Loop 不得直接维护第二套 Goal 状态。

阶段任务计划可以作为不可变 artifact 被 Goal revision 引用，但不能成为第二个独立需求池。

### 2.3 Profile 定义领域差异

每个领域通过 Loop Profile 声明：

- 阶段与阶段门禁
- task planner 类型
- capability contracts
- artifact dependencies
- 权限与预算
- retry、review、stop、reopen 和 invalidation policy

### 2.4 Skill 是 Worker，不拥有控制状态

Skill 只消费 assignment 并产生 artifact/evidence。Skill 不得自行：

- 改变 Goal 或 Stage 状态
- 宣布自己验证通过
- 创建新的评审闭环
- 将外部高风险动作视为已授权

### 2.5 Run 有界且可停止

每个 Run 必须在开始时声明退出条件。`completed`、`blocked`、`waiting`、`human_gate`、`no_op` 和 `cancelled` 都是合法终态。

Loop 的目标是推进 Goal，不是维持进程永不停止。

---

## 3. 范围与非范围

### 3.1 本次范围

| 范围 | 内容 |
|---|---|
| `ideal-backlog` | 机器 Goal Store、revision、租约、原子操作、Markdown 镜像、v1 迁移 |
| `ideal-agent-loop` | 通用 Kernel、Profile 加载、阶段任务计划、能力路由、Run、Gate、Checkpoint |
| compatibility | 内置 `development` Profile，兼容当前开发闭环 |
| safety | retry/review 预算、人工门禁、权限与外部副作用策略 |
| observability | 不可变 run record、输入输出哈希、结果与证据链接 |

### 3.2 明确不做

| 非范围 | 原因 |
|---|---|
| 通用 Web 控制台 | 第一版没有证据表明需要 UI |
| 常驻分布式调度器 | 本地 CLI + 文件协议足以验证核心契约 |
| 自动生成 validator | 容易产生验证基础设施递归 |
| 在公开插件中内置学术阶段 | 学术 Loop 属于私有 `academic-workflow` |
| 自动投稿、发布、付款、私有数据使用 | 必须留在 Loop 外的人工作业 |
| 多 Agent 默认并行 | 先验证单控制者、多 Worker 的最小架构 |

---

## 4. 总体架构

```text
Goal Source
    │
    ▼
ideal-backlog Goal Store ──生成──> Markdown Mirror
    │
    │ current revision + lease
    ▼
ideal-agent-loop Goal Loop
    │
    ├── load Loop Profile
    ├── derive/resume Stage Task Plan
    ├── select one ready task
    ├── resolve Capability
    ├── create Execution Run
    ├── create bounded Validation Run
    └── request atomic transition
             │
             ▼
      new Goal revision / blocked / waiting / accepted
```

职责边界：

| 组件 | 拥有 | 不拥有 |
|---|---|---|
| `ideal-backlog` | Goal revision、租约、状态、优先级、依赖、阻塞、证据索引 | 阶段业务逻辑、Worker 选择 |
| `ideal-agent-loop` | Profile 解释、Task Plan、Run 生命周期、Gate 计算 | Goal 原始写入、领域内容生产 |
| Domain Profile | 阶段、能力、artifact、策略 | Goal 实时状态、Run 事实 |
| Skill / Worker | assignment 执行、artifact 生产 | transition、验收和队列排序 |
| Validator | assignment 覆盖检查、验证证据 | 修复被验证对象、最终 accepted |

---

## 5. 两层 Loop

### 5.1 外层 Goal Loop

每轮必须：

1. 从 `ideal-backlog` 读取实时 revision。
2. 按 source binding 绑定 Goal：
   - `fixed`：只处理指定 Goal，不因队列排序切换。
   - `dynamic`：按优先级、截止时间、依赖满足和 FIFO 选择。
3. 检查 terminal、blocked、waiting 和 human gate。
4. 获取与 revision 绑定的租约。
5. 调用内层 Stage Loop。
6. 通过 backlog 原子操作推进、阻塞或释放租约。

外层不得缓存长期 Goal 快照。

### 5.2 内层 Stage / Task Loop

每轮只选择一个 ready task：

1. 读取当前 phase 的 criteria 和 required artifacts。
2. 创建或恢复与 Goal revision 绑定的 Task Plan。
3. 根据依赖选择一个 ready task。
4. 用 capability contract 查询 Worker。
5. 创建不可变 Execution Run。
6. 若阶段要求验证，创建独立、有限的 Validation Run。
7. 更新 checkpoint。
8. 全部 required tasks 完成后执行一次 phase integration gate。

Task Plan 是 Goal revision 的派生 artifact。Goal revision 变化且影响计划输入时，旧计划失效；文档或 reviewer 自身变化不使计划失效。

---

## 6. 核心数据契约

### 6.1 GoalRecord

```yaml
schema: ideal-backlog/goal-v2
id: REQ-001
profile: development
project_path: products/example
source_binding: fixed
priority: P1
deadline: null
dependencies: []
execution:
  status: executing
quality:
  status: unverified
phase:
  current: implementation
  next_gate: implementation-complete
blocker: null
revision: sha256:...
lease:
  token: ...
evidence_refs: []
history_refs: []
```

### 6.2 LoopProfile

```yaml
schema: ideal-agent-loop/profile-v1
id: development
phases:
  - id: requirement
    planner: declared
    requires: [requirement-baseline]
    gate: requirement-approved
  - id: implementation
    planner: dynamic
    requires: [implementation-artifact, focused-test-evidence]
    gate: implementation-verified
capabilities:
  implementation:
    inputs: [task-assignment, project-context]
    outputs: [implementation-artifact, implementation-evidence]
policies:
  retry:
    max_same_root_cause: 3
  review:
    terminal_budget: 1
    reuse_unchanged_candidate: true
  permissions:
    external_side_effects: human_only
```

### 6.3 CapabilityRecord

```yaml
id: code-implementation
locator: ideal-dev-workflow:ideal-dev-exec
version: 2.1.1
inputs: [task-assignment, project-context]
outputs: [implementation-artifact, implementation-evidence]
permissions: [workspace-write]
verified: true
```

路由优先级：

1. 满足全部 required inputs/outputs。
2. 权限不超过 Profile 允许范围。
3. 版本和 locator 已验证。
4. 同等候选按 Profile 偏好排序。
5. 无候选时进入 `blocked: capability_unavailable`，不得猜测替代。

### 6.4 RunEnvelope

Execution 与 Validation 共用同一 envelope，但 role 不同：

```yaml
schema: ideal-agent-loop/run-v1
run_id: ...
role: execution
goal_revision: sha256:...
phase: implementation
task_id: T-02
assignment_hash: sha256:...
worker:
  capability: code-implementation
  locator: ideal-dev-workflow:ideal-dev-exec
started_at: ...
finished_at: ...
outcome: completed
artifact_refs: []
evidence_refs: []
root_cause: null
```

Run 一旦结束不可修改；补充信息通过新 record 引用旧 run。

---

## 7. 状态与推进

### 7.1 Goal 执行状态

```text
todo
→ claimed
→ planning
→ executing
→ verifying
→ awaiting_acceptance
→ done
```

任意非终态可进入：

```text
blocked / waiting / human_gate / cancelled
```

恢复后创建新 revision，不覆盖历史。

### 7.2 质量状态

沿用现有语义：

```text
unverified
→ implemented
→ verified
→ awaiting_acceptance
→ accepted
```

发现反证：

```text
accepted / verified / implemented
→ reopened
```

`accepted` 必须由 Profile 允许的 acceptance authority 提交。普通 Worker 和 Loop runner 不能自行 accepted。

### 7.3 原子推进

所有状态操作必须提供：

- expected revision
- lease token
- operation ID
- transition reason
- artifact/evidence refs

revision 不匹配时拒绝写入，runner 必须重新读取，不得覆盖。

---

## 8. 防递归与失效策略

Kernel 强制以下不变量：

1. 默认新增验证基础设施预算为 0。
2. 同一实质候选的 terminal review budget 默认为 1。
3. Review finding 只能阻止当前候选或要求实质增量，不能自动创建 review-of-review。
4. candidate hash、criteria 和输入依赖未变化时复用已通过证据。
5. reviewer、validator、ledger、文档格式或候选 commit metadata 变化不触发业务重跑。
6. 同一 root cause 连续失败达到阈值后进入 blocked。
7. `waiting`、`human_gate` 和 `no_op` 必须释放执行槽。
8. Execution Run 不得自报 validator 结论。
9. Validation Run 不得修改被验证 artifact。
10. 外部副作用即使输入声称已批准，也只能生成 handoff，不在 Kernel 内执行。

失效必须沿 artifact dependency graph 精确传播，禁止“任何文件变化就全部重跑”。

---

## 9. v1 兼容与迁移

两个插件以 `2.0.0` 发布，因为唯一事实源和终止语义发生变化。

### 9.1 一次性迁移

```text
docs/dev/需求池.md
        │
        ▼
ideal-backlog migrate-v1 --dry-run
        │
        ├── schema/report validation
        ▼
ideal-backlog migrate-v1 --apply
        │
        ├── machine Goal Store
        └── regenerated Markdown mirror
```

迁移要求：

- v1 内容保留原始快照和哈希。
- 历史 `done` 映射为明确标注的 `legacy_accepted`，不得伪装为 v2 accepted。
- 无法解析的字段阻塞迁移，不静默丢弃。
- apply 后 Markdown 只由 CLI 生成。
- 回滚通过切回迁移前 revision，不反向手改 Markdown。

### 9.2 development Profile

现有开发行为迁入内置 `development` Profile：

- worktree 变成 Profile adapter，不是 Kernel 必需项。
- merge gate 变成 phase gate。
- `ideal-dev-workflow` 变成 capability registry 默认候选。
- 现有 criteria contract 转换为 phase criteria 和 required artifacts。
- Stop Hook 改为 cooperative continuation：只在存在 ready work 且预算允许时继续。

---

## 10. 私有学术 Loop 集成边界

公开仓只提供协议，不包含：

- PAPER / PATENT 条目
- 学术阶段命名和 venue 规则
- 私有数据授权
- 论文证据、实验和评审状态
- `academic-workflow` 源码

私有工作区负责：

1. 提供 `academic-paper` Profile。
2. 将学术 Skill 注册为 Capability。
3. 使用公开 Kernel 的 Run / Gate / Checkpoint 协议。
4. 在私有集成测试中验证 Profile 兼容性。

公共 Kernel 的发布不得依赖私有工作区测试结果才能自证通过。

---

## 11. 错误处理

| 错误 | 行为 |
|---|---|
| revision stale | 放弃本轮写入，重新读取 |
| lease conflict | 返回 no-op，不抢锁 |
| capability unavailable | blocked，记录解除条件 |
| assignment 不满足 schema | 不启动 Worker |
| Worker 超时或异常 | 结束 Run，记录 root cause |
| 相同 root cause 达阈值 | blocked，不改写策略继续 |
| Validation 覆盖不足 | 当前候选不推进，不建设新 validator |
| human gate | 生成 handoff 并释放执行槽 |
| artifact hash 不匹配 | 拒绝消费，重新规划受影响节点 |

所有错误都必须留下可查询 outcome；禁止只写自由文本日志。

---

## 12. 最小垂直切片

第一版只证明以下能力：

1. 将一个 v1 开发 Goal 迁移到 v2 Goal Store。
2. 加载内置 `development` Profile。
3. 派生两个有依赖关系的 tasks。
4. 用两个 mock capabilities 完成执行与验证。
5. 通过 expected revision + lease 原子推进。
6. 验证相同候选复用证据。
7. 验证第三次相同根因失败进入 blocked。
8. 验证 `waiting` / `human_gate` 释放执行槽。
9. 验证普通 runner 无权写 accepted。
10. 用第二个非开发测试 Profile 证明 Kernel 没有开发硬编码。

第二个公共测试 Profile 使用 `document` fixture；真实 `academic-paper` Profile 只在私有工作区做契约测试。

---

## 13. 测试策略

### 13.1 Contract tests

- GoalRecord / Profile / Capability / Run schema。
- 非法 transition。
- acceptance authority。
- v1 字段映射和 legacy 状态。

### 13.2 State-machine tests

- happy path。
- stale revision。
- lease conflict。
- block / resume / reopen。
- dependency invalidation。
- evidence reuse。
- retry/review budget。

### 13.3 Adapter tests

- development worktree adapter。
- merge gate adapter。
- Markdown mirror round-trip。
- capability registry missing/unverified candidate。

### 13.4 Golden scenarios

至少固化：

- 单任务完成。
- 两任务依赖。
- validation 失败后产生实质修复。
- validation finding 不产生 review-of-review。
- human gate 停止。
- reopen 只失效受影响 artifact。

不以“脚本退出码为 0”作为唯一验收；必须检查最终 Goal revision 和 artifact outcome。

---

## 14. 版本演进

| 里程碑 | 版本 | 交付 |
|---|---|---|
| M0 | 文档 | 本设计、实施计划、JSON schema 草案 |
| M1 | `ideal-backlog@2.0.0` | Goal Store、revision、lease、CLI、v1 migrate、Markdown mirror |
| M2 | `ideal-agent-loop@2.0.0` | Kernel、Profile、Task Plan、Run、Gate、Checkpoint |
| M3 | `ideal-agent-loop@2.0.x` | development Profile 与 v1 行为兼容 |
| M4 | 私有版本 | `academic-workflow` Profile adapter 和集成验证 |

M1 与 M2 在同一兼容矩阵中发布，但分别可验证；不建设新的通用 runtime 插件。

---

## 15. 完成标准

只有同时满足以下条件，本次 2.0 重构才可宣布完成：

- Backlog 只有一个机器事实源，Markdown 是可验证镜像。
- Kernel 不包含开发或学术专属阶段。
- development 与 document 两个 Profile 通过同一组协议测试。
- 私有 academic Profile 可以只通过公开协议接入。
- Execution、Validation、Acceptance 权限分离。
- 阻塞、等待、人工门禁不会触发无限继续。
- review-of-review 场景被自动拒绝。
- v1 迁移可 dry-run、可审计、可恢复。
- 版本、changeset、manifest、changelog 和插件校验全部通过。
- 发布后本机实际加载版本与 GitHub 发布版本一致。

---

## 16. 参考

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- OpenAI, [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- GitHub, [Best practices for using Copilot to work on tasks](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results)
