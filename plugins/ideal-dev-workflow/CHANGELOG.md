# ideal-dev-workflow

## 2.1.1

### Patch Changes

- worktree-per-goal + configurable merge gate for ideal-agent-loop outer loop.

  - ideal-agent-loop (minor): each goal runs in an isolated worktree (pulled from base_branch), merged per merge_gate (auto/confirm/pr), then worktree + branch cleaned up. New project-level loop config (loop.yaml, path overridable via AGENTS.md `loop 配置：X`) controls worktree strategy + merge gate. New references: loop-config, worktree-goal-guide, merge-gate.
  - ideal-dev-workflow (patch): ideal-flow-control adds a guard to reuse the existing worktree when already inside one (no orphan task worktree when ideal-agent-loop goal worktree is active).
  - ideal-backlog (patch): note that goal exec env (worktree/merge gate) is owned by ideal-agent-loop; backlog only manages the queue.

## 2.1.0

### Minor Changes

- Remove io frontmatter declarations from phase skills (decouple inter-skill data flow).
- Add real-app end-to-end (core loop) test case type to ideal-test-case and execution section to ideal-test-exec.
- Decouple ideal-requirement to clarification+persist only (drop worktree check, flow-state init, P2 handoff); ideal-flow-control now initializes 流程状态.md before P1.

## 2.0.0

### Major Changes

- Remove sub-iteration mechanism (parent/is_parent/sub_iterations fields, parent-child sync protocol, worktree inheritance). Add story executor field for multi-toolchain support. Add prerequisite file checks to all Phase Skills. Align P7 test cases with P5 stories. Fix flow-state.py YAML parsing. Deduplicate worktree protocol.

## 1.0.0

- Initial release migrated from best-practices/dev-workflow
