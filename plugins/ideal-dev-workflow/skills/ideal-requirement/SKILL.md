---
name: ideal-requirement
description: "Use when: (1) starting a new feature, bug fix, or refactoring task, (2) user mentions '需求', '需求文档', 'PRD', 'requirement', '需求编写', '需求收集', 'bug修复', '重构需求'."
agents: [pm, analyst]
---

# Ideal Requirement

通过交互式对话引导用户完善需求，生成符合正式学术风格的标准化需求文档。复杂需求通过 P5 编码计划阶段的 story 机制拆分。

> **职责边界**：本 skill 只负责「需求澄清 + 需求文档落盘」。不创建/检查 Git Worktree、不维护 `流程状态.md`、不推进阶段评审——这些由调用方（如 `ideal-flow-control`）负责。可独立用于编写需求文档，也可作为开发流程的 P1 被编排器调用；调用方负责 worktree、流程状态与阶段推进。

## Agents

| Agent | 角色 | 用途 |
|-------|------|------|
| pm | 产品经理 | 需求梳理、苏格拉底式对话、文档编写 |
| analyst | 业务分析师 | 竞品分析、市场调研（可选） |

```markdown
Task(
    subagent_type: "pm",
    prompt: "执行需求收集，苏格拉底式对话引导用户",
    model: "opus"
)
```

## Workflow

```
进度：
- [ ] Step 0:   项目背景          ⚠️ REQUIRED
- [ ] Step 0.5: 迭代类型（落盘位置）⚠️ REQUIRED
- [ ] Step 1:   类型识别
- [ ] Step 2:   模板处理
- [ ] Step 3:   需求收集（苏格拉底式对话）
- [ ] Step 4:   确认摘要           ⚠️ REQUIRED
- [ ] Step 5:   生成文档
- [ ] Step 6:   完成
```

---

## The Iron Law

```
NO REQUIREMENT QUESTIONS WITHOUT READING PROJECT CONTEXT FIRST
```

**必须先读取 CLAUDE.md 或 README.md**，了解项目背景后再提问。

---

## 核心原则：需求文档聚焦"做什么"，不包含"怎么做"

**需求文档只回答：**
- 背景：现状是什么？为什么需要改变？
- 目标：重构后要达到什么效果？
- 范围：涉及哪些模块？不涉及哪些？
- 验收标准：怎么算完成？

**需求文档不包含（属于技术方案阶段）：**
- 技术选型、架构设计
- 实施步骤、依赖关系
- 接口变更、数据迁移
- 测试策略、详细设计
- 代码实现细节

---

## 0. 项目背景（必须）

读取优先级：CLAUDE.md → README.md → docs/项目状态.md

提取：项目目标、系统架构、当前阶段、已有模块、技术栈、团队规模。

如果无项目文件，在第一个问题中询问"请简要描述项目背景"。

---

## 0.5 迭代类型（必须）

**询问**：这是个人迭代还是项目迭代？

| 类型 | 说明 | 目录位置 |
|------|------|----------|
| 个人迭代 | 个人开发，不需要团队共享进度 | `docs/迭代/` |
| 项目迭代 | 团队协作，需要共享进度和文档 | `docs/项目迭代/` |

两种迭代目录都不被 Git 跟踪。

---

## 1. 类型识别

用户已指定类型 → 直接使用；未指定 → 通过对话识别：

| 类型 | 触发关键词 | 模板 |
|------|-----------|------|
| 软件功能 | 新功能、开发、实现 | `software-feature.md` |
| Bug修复 | Bug、缺陷、错误、修复 | `bug-fix.md` |
| 重构优化 | 重构、优化、改进 | `refactoring.md` |

---

## 2. 模板处理

1. 读取 `references/templates/{type}.md`
2. 扫描所有 `{placeholder}` 占位符
3. 按优先级排序提问（核心 → 主体 → 细节）

**必填字段**：

| 模板 | 必填字段 |
|------|----------|
| software-feature | title, problem_statement, goal, features, acceptance_functional |
| bug-fix | title, bug_title, preconditions, step_1, expected_behavior, actual_behavior |
| refactoring | title, current_state, problems, goals, acceptance_functional |

---

## 3. 需求收集（苏格拉底式对话）

调用 pm 子代理执行。

### 用户命令（随时可用）

| 命令 | 作用 |
|------|------|
| **跳过** | 跳过当前可选问题 |
| **直接生成** | 跳过剩余问题，进入确认 |
| **回到 XX** | 修改之前某个字段的回答 |
| **取消** | 结束流程（可选保存草稿） |

### 提问策略

- 一次只问一个问题
- 提供 2-4 个选项辅助
- 追问细节
- 记录答案
- 聚焦用户价值（每个功能都要回答"为谁解决什么问题"）

---

## 4. 确认摘要

展示：类型、标题、背景摘要、核心功能、验收标准

用户响应：
- "是"/"确认" → 进入生成
- "修改 XX" → 返回收集阶段
- "继续" → 补充更多信息

---

## 5. 生成文档

### 目录命名

```
docs/迭代/YYYY-MM-DD-{需求名称}/
├── P1-需求文档.md
└── 流程状态.md
```

### 输出文件

| 文件 | 说明 |
|------|------|
| `P1-需求文档.md` | 填充模板 + 学术风格 |

> **不生成 `流程状态.md`**：流程状态、worktree 字段、阶段推进由调用方（`ideal-flow-control`）维护。本 skill 只落盘需求文档。

### 生成流程

1. 读取 `references/templates/{type}.md`
2. 填充占位符，计算风险等级
3. 应用正式学术风格（见 `references/writing-style.md`）
4. 写入文件

---

## 6. 完成

输出需求文档位置。后续阶段（评审/方案等）由调用方编排；独立使用时需求文档已落盘可用，本 skill 不推进任何后续阶段。

---

## 示例

详见 `references/examples.md`。

---

## 错误处理

| 场景 | 处理 |
|------|------|
| 目录已存在 | 覆盖 / 修改 / 新名称 |
| 用户取消 | 保存草稿或直接结束 |
| 必填字段缺失 | 提示后用 `[待补充]` 占位 |

---

## Script Directory

| Script | 用途 |
|--------|------|
| `scripts/validate-requirements.py` | 验证需求文档完整性 |
| `scripts/calculate-risk.py` | 计算风险等级 |
| `scripts/generate-flow-status.py` | ⚠️ 已移交：流程状态文件现由 `ideal-flow-control` 维护（P1 前初始化），本 skill 不再调用 |

---

## References

| 文件 | 用途 |
|------|------|
| `references/templates/software-feature.md` | 软件功能需求模板 |
| `references/templates/bug-fix.md` | Bug 修复需求模板 |
| `references/templates/refactoring.md` | 重构优化需求模板 |
| `references/writing-style.md` | 正式学术风格指南 |
| `references/examples.md` | 示例 |
