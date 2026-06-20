# ideal-backlog

## 1.0.1

### Patch Changes

- 需求池路径改为可配置：先读项目 AGENTS.md 的「需求池路径：X」声明，否则默认 docs/dev/需求池.md，父目录不存在则 mkdir -p 创建。跨项目零改 skill。

## 1.0.0

### Major Changes

- Initial release: 需求池构建与管理 skill。入队（调 ideal-requirement 澄清落盘→登记 goal）、状态流转（todo/doing/done/blocked）、优先级+FIFO 排序。维护 docs/dev/需求池.md，作为 ideal-agent-loop outer loop 出队契约源。
