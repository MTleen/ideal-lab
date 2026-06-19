# ideal-dev-workflow

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
