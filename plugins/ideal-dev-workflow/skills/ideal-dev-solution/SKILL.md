---
name: ideal-dev-solution
description: Use when P2 requirement review is completed and technical solution generation is needed. Analyzes requirements and generates comprehensive technical design including architecture, tech stack, data models, and risk analysis.
agents: [general-purpose (x6 parallel)]
---

> **Phase Skill 角色**：Team Lead。主智能体调用本 Skill 后，本 Skill 全权负责：加载上下文 → spawn sub-agent 完成所有工作 → 写入产物文件 → 返回摘要。主智能体只等待本 Skill 返回。

# ideal-dev-solution（P3 技术方案生成）

## 职责边界

| 本 Skill 负责 | 本 Skill 不负责 |
|--------------|----------------|
| 读取 P1 需求文档 | 更新 flow state |
| 读取项目配置 | 验证前置条件 |
| spawn sub-agent 执行调研 | 决定评审结果 |
| spawn sub-agent 写 P3 文档 | 调度其他 Skill |
| 写入 `P3-技术方案.md` | |
| 返回执行摘要 | |

---

## 输入

| 来源 | 内容 |
|------|------|
| `docs/迭代/{需求名}/P1-需求文档.md` | 功能需求、验收标准、约束条件 |
| `CLAUDE.md` | 项目背景、技术栈 |
| `.claude/project-config.md` | 项目配置 |

## 输出

| 文件 | 路径 |
|------|------|
| `P3-技术方案.md` | `docs/迭代/{需求名称}/P3-技术方案.md` |

---

## 执行流程（全部由 sub-agent 完成）

> **强制要求**：阶段内所有工作必须通过 Agent 工具（`subagent_type: general-purpose`）并行调度。**主智能体不读取文件、不分析代码、不写文档**。所有工作由本 Skill 的 sub-agent 执行。

### Step 0: 验证前置产物（必须）

**在开始任何工作前，验证所有输入文件存在**：

| 文件 | 缺失时处理 |
|------|-----------|
| `docs/迭代/{需求名}/P1-需求文档.md` | 终止执行，报告"P1 需求文档不存在，请先完成 P1 阶段" |
| `CLAUDE.md` | 降级：使用 README.md 替代，若都不存在则从对话中提取项目背景 |

任一强制文件不存在 → 终止执行，返回 flow-control 等待前置阶段完成。

> **调研原则**（必须遵守）：
> 1. **必须使用 `ideal-deep-research` 进行详细调研** — 任何技术选型、功能方案必须先调研现有最佳实践，不能凭直觉设计
> 2. **涉及第三方库、框架、SDK 或 API 时必须使用 Context7** — 查询与项目实际版本匹配的当前文档、API、配置方式和代码示例；记录 Context7 library ID、版本、查询问题和关键结论
> 3. **评估公开 GitHub 项目复用或参考其实现时必须使用 DeepWiki** — 先读取仓库文档结构和相关内容，再针对架构、扩展点、关键实现、依赖与限制提问；记录仓库、主题/问题和关键结论
> 4. **必须交叉验证工具结论** — Context7 结论应与目标版本的官方文档一致；DeepWiki 的 AI 回答不能作为唯一依据，必须回查仓库源码、README、发布说明或官方文档
> 5. **必须避免重复造轮子** — 优先调研现有开源项目、SDK、框架是否可复用，引用调研报告作为方案依据
>
> Context7 或 DeepWiki 不可用、目标未收录或目标为无权访问的私有仓库时，允许降级到目标版本官方文档、源码仓库和 Web 调研，但必须在调研报告中记录不可用原因、替代来源和验证结果，禁止伪造工具调用或查询结论。

### Step 1: 加载上下文

Spawn 一个 sub-agent（`context-loader`）读取：

- `docs/迭代/{需求名}/P1-需求文档.md` 完整内容
- `CLAUDE.md` 项目背景和技术栈
- `.claude/project-config.md` 项目配置
- `docs/迭代/{需求名}/research/` 目录下的已有调研报告（如存在）

### Step 2: 详细调研（先于并行调研执行）

**使用 `ideal-deep-research` 进行技术调研**，调研内容包括：

| 调研方向 | 调研目的 |
|---------|---------|
| 竞品实现方案 | 业界如何实现类似功能，参考成熟方案 |
| 最新技术趋势 | 是否有更优的技术方案 |
| 开源项目复用 | 是否有可复用的开源项目/SDK |
| 踩坑记录 | 他人遇到的坑及解决方案 |

#### 工具使用指引

| 工具 | 必须使用的场景 | 操作要求 | 调研报告必须记录 |
|------|---------------|---------|------------------|
| Context7 | 方案涉及第三方库、框架、SDK、API、安装或配置 | 先解析并确认正确的 library ID，再按项目锁定版本查询具体问题；优先选择名称、版本和来源信誉匹配的结果 | library ID、版本、查询问题、关键结论、对应方案决策；不适用或降级时记录原因与替代来源 |
| DeepWiki | 评估公开 GitHub 仓库是否可复用，或参考其架构与实现 | 依次使用 `read_wiki_structure` 定位主题、`read_wiki_contents` 阅读相关内容，必要时用 `ask_question` 追问；最终回查仓库源码或官方资料 | 仓库标识、阅读主题、提问、关键结论、源码/官方资料交叉验证位置；不适用或降级时记录原因与替代来源 |

查询必须围绕当前需求提出具体问题，不能只搜索宽泛关键词。Context7 用于确认“目标版本支持什么以及如何正确调用”，DeepWiki 用于理解“候选仓库实际上如何组织和实现”；两者不能替代对当前项目代码、目标仓库源码和官方资料的直接检查。

- Context7 使用参考：<https://context7.com/docs/clients/claude-code>
- DeepWiki MCP 使用参考：<https://docs.devin.ai/work-with-devin/deepwiki-mcp>

**调研报告输出路径**：`docs/迭代/{需求名}/research/P3-技术调研_{timestamp}.md`

> **重要**：技术选型、功能设计必须基于调研报告，禁止凭空设计。

### Step 3: 并行调研（6 个 sub-agent 同步执行）

| sub-agent | 任务 |
|-----------|------|
| `agent-requirements` | 功能分解、依赖关系、优先级排序 |
| `agent-architecture` | 系统架构、组件划分，输出 Mermaid 架构图 |
| `agent-tech-selection` | 候选技术评估（按功能满足度30%/团队熟悉度25%/社区活跃度15%/性能15%/学习成本10%/维护成本5%打分）、推荐方案 |
| `agent-data-model` | 核心数据模型，输出 Mermaid ER 图和数据流 |
| `agent-interface-design` | 内部/外部接口规范定义 |
| `agent-risk-analysis` | 风险矩阵（技术/性能/安全三维）+ 应对策略 |

**所有 6 个 sub-agent 并发执行，互不依赖。调研结果汇总到 Step 4。**

> **禁止重复造轮子检查**：每个 sub-agent 必须先检查 `research/` 目录是否有相关调研报告，复用已有结论。

### Step 4: 汇总与文档生成

Spawn 一个 sub-agent（`doc-writer`）：

- 整合 Step 1 和 Step 2 的所有结果
- 按以下结构填充 `P3-技术方案.md`：

| 章节 | 内容 |
|------|------|
| 一、方案概述 | 设计目标、核心原则 |
| 二、系统架构 | Mermaid 架构图、目录结构 |
| 三、功能模块设计 | 模块总览、详细设计 |
| 四、数据模型 | Mermaid ER 图、数据流 |
| 五、接口设计 | 内部接口、外部接口 |
| 六、风险分析与应对 | 风险项、应对策略 |
| 七、实施计划 | 阶段划分、依赖关系 |
| 八、参考资料 | 相关文档链接 |

- 写入文件到 `docs/迭代/{需求名称}/P3-技术方案.md`

### Step 5: 返回摘要

本 Skill 返回标准格式摘要给主智能体。

---

## 质量检查清单

- [ ] 架构图使用 Mermaid 格式（非 ASCII 图）
- [ ] 所有功能需求都有对应的技术方案
- [ ] 非功能需求（性能、安全等）有解决方案
- [ ] 技术选型有明确的打分和理由
- [ ] 风险分析覆盖技术/性能/安全三个维度
- [ ] 文档路径正确
- [ ] 所有工作由 sub-agent 完成（主智能体零直接操作）
- [ ] **必须使用 `ideal-deep-research` 进行过技术调研**
- [ ] **必须引用调研报告结论，不能凭空设计**
- [ ] **必须说明为何不直接复用现有开源项目/SDK**
- [ ] 涉及第三方库、框架、SDK 或 API 时，已有 Context7 查询证据；不适用或降级时已记录原因和替代来源
- [ ] 评估公开 GitHub 项目复用或实现时，已有 DeepWiki 查询证据；不适用或降级时已记录原因和替代来源
- [ ] DeepWiki 关键结论已回查源码或官方资料，未将 AI 回答作为唯一依据

---

## 返回格式

```markdown
## P3 技术方案 — 执行摘要

### 产物
- 调研报告：docs/迭代/{需求名称}/research/P3-技术调研_{timestamp}.md
- 技术方案：docs/迭代/{需求名称}/P3-技术方案.md

### 调研依据
- 已调研 {N} 个技术方向
- 引用开源项目/SDK：{列表}
- 决定自研的原因：{理由}

### 工具证据
- Context7：{library ID、版本、查询问题与结论；或不适用/降级原因及替代来源}
- DeepWiki：{仓库、主题/问题、结论与交叉验证位置；或不适用/降级原因及替代来源}

### 关键决策
1. {决策1} — {理由}（基于调研结论）
2. {决策2} — {理由}（基于调研结论）

### 风险提示
- {风险1}：{应对措施}
```
