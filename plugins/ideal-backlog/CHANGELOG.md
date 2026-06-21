# ideal-backlog

## 1.0.2

### Patch Changes

- worktree-per-goal + configurable merge gate for ideal-agent-loop outer loop.

  - ideal-agent-loop (minor): each goal runs in an isolated worktree (pulled from base_branch), merged per merge_gate (auto/confirm/pr), then worktree + branch cleaned up. New project-level loop config (loop.yaml, path overridable via AGENTS.md `loop 配置：X`) controls worktree strategy + merge gate. New references: loop-config, worktree-goal-guide, merge-gate.
  - ideal-dev-workflow (patch): ideal-flow-control adds a guard to reuse the existing worktree when already inside one (no orphan task worktree when ideal-agent-loop goal worktree is active).
  - ideal-backlog (patch): note that goal exec env (worktree/merge gate) is owned by ideal-agent-loop; backlog only manages the queue.

## 1.0.1

### Patch Changes

- 需求池路径改为可配置：先读项目 AGENTS.md 的「需求池路径：X」声明，否则默认 docs/dev/需求池.md，父目录不存在则 mkdir -p 创建。跨项目零改 skill。

## 1.0.0

### Major Changes

- Initial release: 需求池构建与管理 skill。入队（调 ideal-requirement 澄清落盘 → 登记 goal）、状态流转（todo/doing/done/blocked）、优先级+FIFO 排序。维护 docs/dev/需求池.md，作为 ideal-agent-loop outer loop 出队契约源。
