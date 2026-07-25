# 需求池

## 待办 / 进行中

### [REQ-001] Build the v2 store
- 优先级：P0
- 创建时间：2026-07-01
- 状态：doing
- 质量状态：implemented
- Profile：development
- 项目路径：products/example
- Source Binding：fixed
- 依赖：REQ-000
- 当前阶段：implementation
- 下一门禁：implementation-verified
- 验收标准：
  - [ ] Revision writes are atomic
- 质量证据：
  - 自动验证：tests/store.log
- Reopen 记录：
  - 原因：stale write escaped
  - 漏测原因：concurrent writer was not covered
  - 必补回归：cover stale expected revisions

### [REQ-002] Historical completed goal
- 优先级：P2
- 创建时间：2026-06-01
- 状态：done
- 依赖：无
- 验收标准：
  - [x] Historical behavior existed
- 质量证据：
  - 自动验证：legacy build log
