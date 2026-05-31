---
name: ideal-dev-exec
description: Use when P8 test case review is completed and development execution is needed. Executes coding tasks following TDD principles with Git branch management.
agents: [implement, check, debug]
io:
  inputs:
    - name: dev_plan
      source: ideal-dev-plan.dev_plan
  outputs:
    - name: source_code
      type: code
---

# ideal-dev-exec（P9 开发执行）

## 角色定位

Phase Skill — **执行协调者**。

职责：
1. 加载所需上下文（stories/ + P5 编码计划）
2. 调度子智能体按拓扑顺序执行任务
3. 将代码写入项目文件系统
4. 返回执行摘要

**不负责**：更新 flow state、验证前置条件、协调评审。

---

## 输入

| 来源 | 内容 |
|------|------|
| stories/ | 上下文隔离的故事文件和任务清单 |
| P5-编码计划.md | 任务依赖关系、验证清单 |
| project-config.md | Git 分支配置、测试/构建命令 |

## 输出

| 输出 | 位置 |
|------|------|
| 代码实现 | `src/` |
| 测试代码 | `tests/` |

---

## 子智能体调度

| 调用时机 | 子智能体 | 任务 |
|----------|----------|------|
| 代码实现 | `implement` | 按故事文件执行任务，遵循 TDD |
| 运行时验证 | `check` | 运行测试套件 + 规范合规审查 + 代码质量审查 |
| 调试支援 | `debug` | 根因分析、问题调试（验证失败时调用） |

### TDD 协议

详见 `references/tdd-protocol.md`。

### check 子智能体职责（三阶段审查）

```
Phase 0 — 运行时验证（新增，最高优先级）
  ├─ 执行 make test（或 project-config.md 中的 test_command）
  ├─ 测试全部通过？
  │   ├── 是 → 进入 Phase 1
  │   └── 否 → 记录失败用例 → 返回失败，触发 debug 子智能体
  └─ 执行 make lint（或 lint_command）
      ├── 通过 → 进入 Phase 1
      └── 不通过 → 记录问题 → 返回失败，触发 debug 子智能体

Phase 1 — 规范合规审查
  ├─ 实现了计划中指定的功能？
  ├─ 没有添加计划外的功能？
  └─ 测试覆盖了计划中的验证标准？

Phase 2 — 代码质量审查
  ├─ 代码风格符合项目规范？
  ├─ 无明显性能问题？
  └─ 无安全隐患？

发现问题 → 自我修复 → 重新验证（从 Phase 0 重跑）
```

---

## 执行流程

```
Step 0: 验证前置产物
  ├─ 检查 stories/index.md 存在 → 否则终止
  └─ 检查 P5-编码计划.md 存在 → 否则终止

Step 1: 加载上下文
  ├─ 读取 stories/index.md
  ├─ 确定执行顺序（拓扑排序）
  └─ 读取 project-config.md（获取 test_command, build_command）

Step 2: 环境检查
  ├─ 读取 flow state 中的 worktree.path
  ├─ 验证当前目录是否为 worktree.path
  └─ 若不在正确的 worktree 中，终止并报告错误

Step 3: 验证干净基线
  ├─ 执行 make test（或 test_command）
  └─ 确认基线测试通过

Step 4: 按拓扑层级执行任务
  ├─ 第 1 层（无依赖）→ 并行执行
  ├─ 第 2 层 → 第 1 层完成后并行执行
  └─ 每批次：
      ├─ 读取 story 的 executor 标签，选择对应 agent
      │   ├─ default → 默认 implement agent
      │   ├─ go-agent → Go 技术栈 agent
      │   ├─ react-agent → React/前端 agent
      │   └─ python-agent → Python agent
      ├─ Task(implement:{executor}) → TDD: RED → GREEN → REFACTOR
      ├─ Task(check)
      │   ├─ Phase 0: 执行 story 对应 toolchain 的 test + lint
      │   ├─ Phase 1: 规范合规审查
      │   └─ Phase 2: 代码质量审查
      ├─ check 不通过 → Task(debug) → 修复后重新 Task(check)
      └─ 最多重试 3 次，超过则暂停并报告

Step 5: 最终验证
  ├─ 对每个 toolchain 执行对应 verify 命令
  ├─ 全部通过 → 继续
  └─ 有失败 → Task(debug) 修复 → 重新验证 → 最多 3 轮

Step 6: 返回摘要
```

---

## 质量检查清单

每批次完成后：
- [ ] implement 返回了实现报告
- [ ] check Phase 0 运行时验证通过（对应 toolchain 的 test + lint 全绿）
- [ ] check Phase 1-2 两阶段审查通过
- [ ] 测试套件全部通过

全部完成后：
- [ ] 所有任务已完成
- [ ] 所有 toolchain 的 verify 全部通过
- [ ] 代码已提交

---

## 返回格式

```markdown
## P9 开发执行 — 执行摘要

### 执行统计
- 总故事数：{N}，完成：{N}，跳过：{N}

### 批次执行记录
| 批次 | 故事 | 状态 | 运行时验证 | 耗时 |
|------|------|------|-----------|------|
| 1 | 001, 002 | ✅ 完成 | ✅ 通过 | {X}min |

### 最终验证
- 测试套件：{通过/失败}
- Lint 检查：{通过/失败}
- 构建验证：{通过/失败}

### 产出文件
{列出所有修改/创建的文件}
```
