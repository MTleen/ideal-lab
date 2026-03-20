---
name: ideal-dev-solution
description: Use when P2 requirement review is completed and technical solution generation is needed. Analyzes requirements and generates comprehensive technical design including architecture, tech stack, data models, and risk analysis.
agents: [architect]
---

# ideal-dev-solution（P3 技术方案生成）

## 角色定位

Phase Skill — **执行协调者**。

职责：
1. 加载所需上下文（P1 + 项目配置）
2. 调度子智能体执行具体设计任务
3. 将产物写入文件系统
4. 返回执行摘要

**不负责**：更新 flow state、验证前置条件，协调评审。

---

## 输入

| 来源 | 内容 |
|------|------|
| P1-需求文档.md | 功能需求、非功能需求、验收标准、约束条件 |
| CLAUDE.md | 项目背景、技术栈、团队规模 |
| project-config.md | Git 配置、执行命令、技术栈详情 |

## 输出

| 文件 | 路径 |
|------|------|
| P3-技术方案.md | `docs/迭代/{需求名称}/P3-技术方案.md` |

---

## 子智能体调度

| 调用时机 | 子智能体 | 任务 |
|----------|----------|------|
| 需求分析 | `architect` | 功能分解、依赖识别、优先级排序 |
| 架构设计 | `architect` | 系统架构、组件划分、架构图（Mermaid） |
| 技术选型 | `architect` | 候选评估、对比分析、推荐方案 |
| 数据设计 | `architect` | 核心实体、关系设计、ER 图（Mermaid） |
| 接口设计 | `architect` | 内部/外部接口、规范定义 |
| 风险分析 | `architect` | 风险识别、影响评估、应对措施 |

---

## 文档结构

| 章节 | 内容 |
|------|------|
| 一、方案概述 | 设计目标、核心原则 |
| 二、系统架构 | 架构图（Mermaid）、目录结构 |
| 三、功能模块设计 | 模块总览、详细设计 |
| 四、数据模型 | 核心数据模型、ER 图（Mermaid）、数据流 |
| 五、接口设计 | 内部接口、外部接口 |
| 六、风险分析与应对 | 风险项、应对策略 |
| 七、实施计划 | 阶段划分、依赖关系 |
| 八、参考资料 | 相关文档链接 |

---

## 执行流程

```
Step 1: 加载上下文
  ├─ 读取 P1-需求文档.md
  └─ 读取 CLAUDE.md + project-config.md

Step 2: 需求分析
  └─ Task(architect) → 功能分解、依赖关系、优先级

Step 3: 系统架构设计
  └─ Task(architect) → 架构图（Mermaid）+ 组件划分

Step 4: 技术选型
  └─ Task(architect) → 评估框架打分、推荐方案

Step 5: 数据模型设计
  └─ Task(architect) → ER 图（Mermaid）+ 数据流

Step 6: 接口设计
  └─ Task(architect) → RESTful 接口规范

Step 7: 风险分析
  └─ Task(architect) → 风险矩阵 + 应对策略

Step 8: 写入产物
  └─ 填充方案模板 → 写入 P3-技术方案.md

Step 9: 返回摘要
```

---

## 技术选型评估框架

| 维度 | 权重 |
|------|------|
| 功能满足度 | 30% |
| 团队熟悉度 | 25% |
| 社区活跃度 | 15% |
| 性能表现 | 15% |
| 学习成本 | 10% |
| 长期维护成本 | 5% |

每个技术选型都应有 ADR 记录。

---

## 质量检查清单

- [ ] 架构图使用 Mermaid 格式（非 ASCII 图）
- [ ] 所有功能需求都有对应的技术方案
- [ ] 非功能需求（性能、安全等）有解决方案
- [ ] 技术选型有明确的打分和理由
- [ ] 风险分析覆盖技术/性能/安全三个维度
- [ ] 文档路径正确

---

## 返回格式

```markdown
## P3 技术方案 — 执行摘要

### 产物
- 文件：docs/迭代/{需求名称}/P3-技术方案.md

### 关键决策
1. {决策1} — {理由}
2. {决策2} — {理由}

### 风险提示
- {风险1}：{应对措施}
```
