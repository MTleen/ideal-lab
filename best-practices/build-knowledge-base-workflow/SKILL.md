---
name: build-knowledge-base-workflow
description: |
  知识库构建编排工作流。当用户需要从项目原始素材中构建结构化知识库时使用。
  触发场景：(1) 用户要求"构建知识库"、"分析项目" (2) 用户提供了项目路径希望生成知识库
---

# Knowledge Base Build Workflow

## 角色定位

本 workflow 是编排器，负责四件事：
1. 分析原始素材，确定要生成哪些文档
2. 确认项目定位和事实基调
3. 为每个文档写初步需求文档（作为 ideal-document-workflow 的输入）
4. 通过 Agent 工具并行调用 ideal-document-workflow（YOLO 模式），等待通知后汇总

文档质量由 `ideal-document-workflow` 的评审机制保障，本 workflow 不重复做文档评审。

---

## 完整执行流程

### Phase 1：初始化（串行，需人工确认）

**Step 1.1 — 项目信息确认**

确认以下信息（若用户未提供则询问）：
- 项目名称
- 原始材料路径（本地路径或 GitHub 仓库）
- 分类（可从材料推断）

验证路径是否存在：
- 本地路径：检查目录是否存在
- GitHub 仓库：用 `mcp__zread__get_repo_structure` 验证

**Step 1.2 — 调用 kb-material-scope（P1）**

扫描原始素材，产出 `P1-材料清单.md`。

**Step 1.3 — 调用 kb-deep-analysis（P2）**

深度分析素材，产出 `P2-分析报告.md`。

**Step 1.4 — 调用 kb-doc-planning（P3）**

规划文档清单，产出 `P3-文档规划.md`（含机器可读文档清单）。

**Step 1.5 — 项目定位确认（关键步骤）**

在展示文档清单之前，先向用户确认项目的**事实基调**。这些问题在 P2 分析完成后最合适提问，因为此时对项目已有基本了解：

使用 `AskUserQuestion` 确认以下关键定位（根据项目情况选择性提问）：

```json
{
  "header": "项目定位确认",
  "question": "在开始生成知识库之前，请确认以下关键定位信息（这些将影响所有文档的写作基调）：",
  "fields": [
    "平台定位：是自研产品还是基于开源项目？如果基于开源项目，对外是否宣称自研？",
    "领域定位：是通用平台还是领域专用？如果素材来自特定领域项目，该领域是平台的定位还是仅是应用场景？",
    "竞品对比：是否需要在文档中与同类产品对比？对比对象的定位是什么？"
  ]
}
```

**为什么要确认：** 这些定位信息一旦写进 9 个文档，事后修正需要逐文档批量修改。在生成前确认，一次沟通到位。

将确认结果记录到 `P3-文档规划.md` 的头部，作为所有文档的写作基调约束。

**Step 1.6 — 人工审核关卡**

使用 `AskUserQuestion` 展示文档清单和定位约束，等待确认：

```json
{
  "header": "Phase 1 完成，请确认文档规划",
  "question": "已完成材料分析，规划生成以下 {N} 个知识库文档：\n\n{文档清单}\n\n写作基调约束：\n{从 Step 1.5 确认的定位信息}\n\n信息缺口：{知识缺口摘要}\n\n确认后将并行启动文档生成（YOLO 模式）。",
  "options": [
    {"label": "确认，开始生成", "description": "并行启动所有文档的生成流程"},
    {"label": "需要调整", "description": "修改文档清单或内容要点"}
  ]
}
```

**Step 1.7 — 建立目录结构**

```
{分类}/知识库/{项目名称}/
├── 流程状态.md         # 本 workflow 状态
├── P1-材料清单.md
├── P2-分析报告.md
├── P3-文档规划.md      # 含写作基调约束
├── 需求文档/           # 各文档的初步需求（ideal-document-workflow 输入）
│   ├── {文档名}/       # ideal-document-workflow 工作目录
│   │   └── 流程状态.md
│   ├── {文档名}-需求.md
│   └── ...
└── {各知识库文档}.md   # ideal-document-workflow 的最终输出
```

**Step 1.8 — 为每个文档创建 ideal-document-workflow 的 流程状态.md**

在 `需求文档/{文档名}/` 目录下创建 `流程状态.md`，预设 P1/P2 为 completed（需求已由本 workflow 提供），并指定输出路径：

```yaml
---
project_dir: {需求文档/{文档名}/}
document_name: {文档名}
document_type: 知识库文档
target_reader: 根据文档类型确定（概述→销售/售前，技术架构→技术团队，等）
output_format: markdown
output_path: "{分类}/知识库/{项目名称}/{文档名}.md"
current_phase: P3
status: in_progress
yolo_mode: true
created_at: {时间}
updated_at: {时间}
---

## 阶段状态

> **阶段跳过**：P1/P2 已由 build-knowledge-base-workflow 完成，从 P3 继续执行。

| 阶段 | 类型 | 状态 | 完成时间 | 产出 |
|------|------|------|----------|------|
| P1 | 产物 | ✅ completed | {时间} | 需求文档/{文档名}-需求.md |
| P2 | 评审 | ✅ completed | {时间} | - |
| P3 | 产物 | ⏳ pending | - | P2-大纲.md |
| P4 | 评审 | ⏳ pending | - | - |
| P5 | 产物 | ⏳ pending | - | P3-任务拆分.md |
| P6 | 评审 | ⏳ pending | - | - |
| P7 | 产物 | ⏳ pending | - | sections/ |
| P8 | 评审 | ⏳ pending | - | - |
| P9 | 产物 | ⏳ pending | - | sections/ + images/ |
| P10 | 评审 | ⏳ pending | - | - |
| P11 | 产物 | ⏳ pending | - | 最终交付物 |
| P12 | 交付 | ⏳ pending | - | - |
```

**Step 1.9 — 生成各文档需求文档**

从 `P3-文档规划.md` 读取文档清单（机器可读部分），为每个文档生成 `需求文档/{文档名}-需求.md`。

需求文档格式：

```markdown
# {文档名} 需求文档

## 基本信息
- **项目名称**：{名称}
- **文档类型**：{类型}
- **知识库分类**：{分类}
- **输出路径**：`{分类}/知识库/{项目名称}/{文档名}.md`

## 写作基调约束
{从 Step 1.5 确认的定位信息，逐条列出}
{示例：
- 平台定位为自研产品，不得提及"基于开源项目"或"基于 xxx 框架"
- 平台是通用的 LLM 训练数据治理平台，非领域专用。飞行域仅为首个应用场景
}

## 文档目标
{从 P3 规划中提取该文档的目标和定位}

## 内容要点
{从 P3 规划中提取该文档的章节和内容要点，含信息充分度标注}

## 信息来源
- P2 分析报告：`{分类}/知识库/{项目名称}/P2-分析报告.md`
- 原始材料：{原始材料路径}

## 质量要求
- 所有内容从原始素材中提取，不得虚构
- 架构图、数据流图使用 Mermaid 语法
- 信息不足时标注 **[待补充]** 并说明缺失内容
```

**Step 1.10 — 更新 流程状态.md**

```yaml
---
project_name: {项目名称}
raw_material_path: {原始材料路径}
category: {分类}
current_phase: Phase2
status: in_progress
created_at: {时间}
updated_at: {时间}
---

## 文档状态

| 文档 | 状态 | 完成时间 |
|------|------|----------|
| 概述.md | ⏳ pending | - |
| 技术架构.md | ⏳ pending | - |
| ... | | |

## Phase 状态

| Phase | 状态 | 完成时间 |
|-------|------|----------|
| Phase1 初始化 | ✅ completed | {时间} |
| Phase2 并行生成 | ⏳ in_progress | - |
| Phase3 汇总 | ⏳ pending | - |
```

---

### Phase 2：并行启动（Agent 工具）

使用 Agent 工具并行启动 ideal-document-workflow。

**启动方式：**

对 `P3-文档规划.md` 机器可读清单中的**每个文档**，使用 Agent 工具并行调用：

```
Agent:
  description: "ideal-document-workflow 生成{文档名}.md"
  subagent_type: general-purpose
  prompt: |
    你是一个文档写作专家，请执行 ideal-document-workflow 工作流来生成文档。

    ## 关键信息

    - **技能文件**：~/.claude/skills/ideal-document-workflow/SKILL.md
    - **项目工作目录**：{分类}/知识库/{项目名称}/需求文档/{文档名}/
    - **流程状态文件**：上述目录下的 流程状态.md（P1/P2 已 completed，从 P3 开始）
    - **需求文档**：{分类}/知识库/{项目名称}/需求文档/{文档名}-需求.md
    - **最终输出路径**：{分类}/知识库/{项目名称}/{文档名}.md

    ## 执行要求

    1. 阅读 ideal-document-workflow 技能文件
    2. 阅读 流程状态.md 确认当前阶段（从 P3 开始）
    3. 阅读需求文档理解目标和写作基调约束
    4. 从 P3 逐阶段执行到 P12（YOLO 模式，评审自动通过）
    5. 每阶段更新 流程状态.md
    6. P11 将最终文档写入指定输出路径
    7. 所有中间产物放在项目工作目录下
```

**注意事项：**
- **并行度控制**：单次最多启动 6 个 Agent，超出部分等第一批完成后再启动（避免 429 速率限制）
- **速率限制处理**：如果 Agent 返回 429 错误，等待 1-2 分钟后单独重跑失败的文档
- Agent 工具的 task notification 机制会自动通知完成状态，无需手动轮询

---

### Phase 3：汇总（所有 Agent 完成后）

所有文档的 Agent 完成后（通过 task notification 逐一确认），执行汇总。

**Step 3.1 — 合并索引片段**

每个文档的 `ideal-document-workflow` 完成后，局部收口会写入 `.status/{文档名}-index.md`（索引片段）。

将所有片段合并，更新：
- `{分类}/索引.md` — 分类索引
- `项目索引.md` — 主索引

索引条目格式（见 CLAUDE.md）。

**Step 3.2 — 质量摘要**

扫描所有已生成文档：
- 检查是否有 `[待补充]` 标记，汇总缺口
- 检查 Mermaid 图表是否存在（技术架构、数据流等要求有图）
- 统计文档完成情况

**Step 3.3 — 输出完成报告**

```
✅ 知识库构建完成

项目：{项目名称}
分类：{分类}
知识库路径：{分类}/知识库/{项目名称}/

已生成文档（{N} 个）：
  ✅ 概述.md
  ✅ 技术架构.md
  ...

信息缺口（需补充）：
  - 概述.md：竞品对比信息不足
  - 应用成效.md：缺少量化数据

索引已更新：
  - {分类}/索引.md
  - 项目索引.md
```

---

## 局部收口（由各文档 ideal-document-workflow 完成后执行）

每个 Agent 在完成文档后（Phase 4 之前），需执行局部收口：

写入 `.status/{文档名}-index.md`（索引片段）：

```markdown
### {文档名}
- **完成时间**：{时间}
- **输出路径**：`{路径}`
- **[待补充] 项**：{数量}，详见文档内标注
- **图表**：{有/无}
```

此步骤由 ideal-document-workflow 的 prompt 中明确要求执行。

---

## 经验教训

### 1. tmux 方案不可行

`claude --dangerously-skip-permissions` 在 tmux 中会弹出交互式安全确认界面（"Yes, I accept"），无法通过 tmux send-keys 可靠地自动化。Agent 工具是更可靠的并行执行方式。

### 2. "太快完成"是红旗信号

如果 ideal-document-workflow（12 阶段）的每篇文档在几分钟内就完成，说明工作流没有真正执行。正确的 12 阶段流程每篇需要 10-20 分钟。可以通过检查中间产物（P2-大纲.md、P3-任务拆分.md、sections/ 目录）来验证工作流是否真正执行。

### 3. 项目定位必须提前确认

平台是否自研、是否通用等定位信息，一旦写入所有文档后修正成本极高（逐文档批量修改）。必须在 Phase 1 的 Step 1.5 确认，并将确认结果写入需求文档的"写作基调约束"章节。

### 4. 并行度控制

超过 6 个并发 Agent 会触发 API 速率限制（429）。失败后等待 1-2 分钟单独重跑即可。

---

## 相关 Skills

- `kb-material-scope` — P1 材料收集与范围确认
- `kb-deep-analysis` — P2 深度分析
- `kb-doc-planning` — P3 文档规划（含机器可读文档清单）
- `ideal-document-workflow` — 各文档的完整生成流程（含评审）
