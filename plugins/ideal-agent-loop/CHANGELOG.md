# ideal-agent-loop

## 1.0.0

### Major Changes

- Rename from ideal-ralph to ideal-agent-loop; reposition as loop engineering implementation (goal-driven agent loop: plan/act/observe/validate/terminate).
- Add outer loop scenario: consume docs/dev/需求池.md (built by ideal-backlog), dequeue goals by priority+FIFO, run inner loop per task via ideal-dev-workflow, relay to next goal.
- State dir .ralph/ → .agent-loop/; scripts ralph_*.py → agent_loop_*.py.

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
