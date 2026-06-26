# ideal-agent-loop

## 1.2.0

### Minor Changes

- Add quality closure semantics for backlog-backed loops: verified, awaiting_acceptance, accepted, and reopened states; acceptance-gated termination; quality evidence; and reopen metadata.

## 1.1.0

### Minor Changes

- worktree-per-goal + configurable merge gate for ideal-agent-loop outer loop.

  - ideal-agent-loop (minor): each goal runs in an isolated worktree (pulled from base_branch), merged per merge_gate (auto/confirm/pr), then worktree + branch cleaned up. New project-level loop config (loop.yaml, path overridable via AGENTS.md `loop 配置：X`) controls worktree strategy + merge gate. New references: loop-config, worktree-goal-guide, merge-gate.
  - ideal-dev-workflow (patch): ideal-flow-control adds a guard to reuse the existing worktree when already inside one (no orphan task worktree when ideal-agent-loop goal worktree is active).
  - ideal-backlog (patch): note that goal exec env (worktree/merge gate) is owned by ideal-agent-loop; backlog only manages the queue.

## 1.0.1

### Patch Changes

- outer loop 消费需求池时遵循 ideal-backlog 的路径解析规则（读 AGENTS.md 的「需求池路径」声明 → 默认 docs/dev/需求池.md）。

## 1.0.0

### Major Changes

- Rename from ideal-ralph to ideal-agent-loop; reposition as loop engineering implementation (goal-driven agent loop: plan/act/observe/validate/terminate).
- Add outer loop scenario: consume docs/dev/需求池.md (built by ideal-backlog), dequeue goals by priority+FIFO, run inner loop per task via ideal-dev-workflow, relay to next goal.
- State dir .ralph/ → .agent-loop/; scripts ralph*\*.py → agent_loop*\*.py.

## 0.6.0

### Minor Changes

- Add structured continuation prompt template and global audit step

### Patch Changes

- Add PREFLIGHT phase to auto-register Stop Hook before LOOP

## 0.4.0

### Minor Changes

- Add ideal-agent-loop plugin with Socratic task clarification and persistent iteration loop

## 0.3.0

### Minor Changes

- Add ideal-agent-loop plugin with Socratic task clarification and persistent iteration loop

## 0.1.0

### Patch Changes

- 新增 ideal-agent-loop skill：苏格拉底式任务澄清 + 持久小步迭代验证循环
