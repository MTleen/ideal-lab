---
name: ideal-dify-generator
description: 完整的 Dify 智能体/工作流 DSL 生成器。从自然语言需求出发，生成可直接导入 Dify 的完整 DSL YAML 文件。支持端到端流程：需求分析 → 节点选型 → DSL 生成 → 自动校验 → 输出交付。融合 dify-dsl-generator 的案例驱动方法与 dify-workflow-skills 的精细化工程规范。
version: 1.0.0
---

# ideal-dify-generator
完整的 Dify 智能体 & 工作流 DSL 生成器，融合案例驱动与工程规范。

## 核心能力

- **需求 → DSL 端到端**：自然语言描述 → 完整可导入 Dify 的 YAML 文件
- **智能节点选型**：基于决策树推荐最合适的节点类型
- **完整应用结构**：生成包含 `app` + `dependencies` + `workflow` 的完整 DSL（版本 0.3.0）
- **自动化校验**：生成后自动跑校验脚本，确保语法、结构和变量链路正确
- **8 个场景模板**：从基础 LLM 到 OCR、Agent、迭代，覆盖常见业务场景

## 整体流程

```
用户自然语言描述需求
         ↓
┌─────────────────────────────────────────┐
│  Step 1: 需求分析                        │
│  - 确定工作流类型（chatflow/workflow/agent）│
│  - 识别输入/输出                          │
│  - 规划处理步骤                           │
│  - 判断是否需要插件依赖                    │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Step 2: 节点选型（参考 node_selection） │
│  - 按决策树匹配节点类型                    │
│  - 从模板库选择最接近的基础模式              │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Step 3: DSL 生成                        │
│  - 填充 app 配置（名称/描述/icon/mode）   │
│  - 填充 dependencies（插件）               │
│  - 填充 workflow.graph（nodes + edges）   │
│  - 生成唯一节点 ID                        │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Step 4: 自动校验（validate_workflow.py）│
│  - 语法校验                              │
│  - 结构校验（节点/边/根节点/终节点）       │
│  - 变量引用链路校验                        │
│  - 错误处理完整性校验                      │
└────────────────┬────────────────────────┘
                 ↓
         输出完整 DSL YAML
    （可直接导入 Dify 平台）
```

## Step 1: 需求分析

向用户收集以下信息（可一次收集也可逐步确认）：

```
1. 工作流类型？
   - chatflow（高级对话，多轮交互）→ mode: advanced-chat
   - workflow（标准工作流，单次任务）→ mode: workflow
   - agent（AI Agent，工具调用）→ mode: agent-chat

2. 输入是什么？
   - 文本（段落/单行）
   - 文件（图片/文档/音频）
   - 参数选择（下拉）

3. 工作流要做什么？（核心业务逻辑）
   - 纯 LLM 对话/生成
   - RAG（知识库检索）
   - 外部 API 调用
   - 代码数据处理
   - 条件分支判断
   - 循环迭代处理
   - 错误自动恢复

4. 输出是什么？
   - 文本回复
   - 结构化数据（JSON）
   - 文件（图片/文档）
   - API 响应

5. 需要哪些外部能力？
   - 知识库检索
   - 搜索引擎
   - 数据库查询
   - 文件处理/导出
   - 第三方 API

6. 是否需要错误处理？
   - 是 → 需要 fail-branch / retry / default-value
   - 否 → 默认 abort 策略
```

## Step 2: 节点选型（决策树）

### 主流程节点

```
输入类型
├── 文本输入
│   ├── 简单问答 → Start → LLM → Answer
│   ├── 带知识库 → Start → Knowledge Retrieval → LLM → Answer
│   ├── 带外部调用 → Start → HTTP Request → LLM → Answer
│   └── 带数据处理 → Start → Code → LLM → Answer
├── 文件输入
│   ├── 图片识别 → Start → LLM(vision) → Answer
│   ├── 文档解析 → Start → Document Extractor → LLM → Answer
│   └── 多文件处理 → Start → Iteration → [Process] → Answer
└── 参数输入
    └── 下拉选择 → Start → If-Else → [分支] → Answer
```

### 控制流节点

| 场景 | 节点类型 | 说明 |
|------|---------|------|
| 条件分支 | `if-else` | 两路分支，支持 and/or 组合条件 |
| 意图分类 | `question-classifier` | 多路分支，按用户意图分类 |
| 列表迭代 | `iteration` | 对数组每个元素执行子流程 |
| 循环执行 | `loop` | 重复执行直到满足退出条件 |

### 数据处理节点

| 节点类型 | 用途 |
|---------|------|
| `code` | Python/JS 代码执行，数据转换 |
| `template-transform` | 字符串模板替换 |
| `variable-assigner` | 修改变量值 |
| `variable-aggregator` | 合并多分支变量 |
| `list-operator` | 列表过滤/排序 |

### LLM 节点

| 节点类型 | 用途 |
|---------|------|
| `llm` | 标准大语言模型调用 |
| `agent` | Agent 模式，支持工具调用循环 |

### 输出节点

| 节点类型 | 用途 |
|---------|------|
| `answer` | 流式输出回复（可出现在流程中途） |
| `end` | 终止工作流 |

## Step 3: DSL 生成规范

### 完整文件结构（版本 0.3.0 → Dify 自动升级到 0.6.0）

```yaml
app:
  name: '工作流名称'
  description: '工作流描述'
  icon: '🤖'
  icon_background: '#FFEAD5'
  mode: advanced-chat  # advanced-chat | workflow | agent-chat
  use_icon_as_answer_icon: false

dependencies:
  # 插件依赖（如需）

kind: app
version: 0.3.0

workflow:
  # ⚠️ 必须包含 value + value_type，否则 Dify API 导入报错 "missing value type"
  conversation_variables: []
  environment_variables:
    - id: 'env_xxx'
      name: 'API_BASE_URL'
      value: 'https://api.example.com'
      value_type: string   # 必须有
      description: 'API地址'
  features:
    # 功能配置
  graph:
    nodes: []
    edges: []
```

### 节点 ID 生成规则

使用时间戳确保唯一性：

```bash
# 方式1: 使用脚本
python3 scripts/generate_id.py 5

# 方式2: Python
node_id = str(int(time.time() * 1000))

# 方式3: JavaScript
const nodeId = Date.now().toString()
```

**容器节点特殊规则**：
- Iteration/Loop 的内部起始节点 ID：`${parentNodeId}start`
- 例：父节点 ID 为 `1736668800000`，内部起始节点为 `1736668800000start`

### 变量引用格式

```
{{#节点ID.输出变量#}}
```

**常见输出字段**：
- LLM 节点：`{{#node_id.text#}}`、`{{#node_id.usage#}}`
- HTTP Request：`{{#node_id.body#}}`、`{{#node_id.status_code#}}`
- Code 节点：`{{#node_id.自定义输出名#}}`
- System：`{{#sys.query#}}`、`{{#sys.files#}}`

### 错误处理配置

```yaml
# 节点内配置
error_strategy: fail-branch  # abort | fail-branch | default-value | retry

# 边连接配置（fail-branch 时）
sourceHandle: success-branch  # 或 fail-branch
```

## Step 4: 自动化校验

生成 DSL 后，调用校验脚本：

```bash
python3 scripts/validate_workflow.py output.yml
```

校验维度（新增 Dify 0.6+ 变量字段检查）：

| 检查项 | 说明 |
|-------|------|
| 语法校验 | YAML 格式正确，可正常解析 |
| 结构完整 | 包含 app + kind + version + workflow |
| 节点唯一性 | 所有节点 ID 唯一 |
| 边引用有效 | 所有边的 source/target 指向存在的节点 |
| 根节点 | 存在且仅存在一个 start/datasource/trigger 节点 |
| 终节点 | 存在至少一个 end/answer 节点 |
| 变量引用 | 所有 `{{#xxx#}}` 格式的引用指向有效节点 |
| 错误处理 | fail-branch 节点同时有 success/fail 两条边 |

校验通过后输出：

```
✅ 语法校验: PASS
✅ 结构校验: PASS
✅ 节点 ID: 全部唯一
✅ 边引用: 全部有效
✅ 变量引用: 全部有效
✅ 错误处理: 完整

🎉 DSL 生成成功，可直接导入 Dify！
```

## 场景 → 模板映射

| 用户场景 | 使用模板 |
|---------|---------|
| 简单问答 / 文本生成 | `simple_llm_workflow.yml` |
| API 调用 + 容错 | `error_handling_workflow.yml` |
| 意图分流 / 多路分支 | `conditional_workflow.yml` |
| 图片 OCR 识别 | `ocr_workflow.yml` |
| 数据库查询 + 图表 | `data_query_workflow.yml` |
| 工具调用型 Agent | `agent_workflow.yml` |
| 批量文件处理 | `iteration_workflow.yml` |

## 输出规范

生成的 DSL 文件必须满足：

### 合格标准（必须满足）
- ✅ YAML 格式正确，可被解析
- ✅ 包含完整的 `app` + `kind` + `version` + `workflow` 结构
- ✅ 至少包含 `start` 和 `answer/end` 节点
- ✅ 所有边连接的 source/target 节点 ID 均存在
- ✅ 变量引用格式正确：`{{#node_id.field#}}`
- ✅ 节点 ID 全局唯一
- ✅ 坐标位置合理，无重叠
- ⚠️ **environment_variables 中每个变量必须有 `value` 和 `value_type` 字段**
- ⚠️ **conversation_variables 中每个变量必须有 `value` 和 `value_type` 字段**
- ⚠️ **导入 API 使用 `mode: yaml-content`（不是 overwrite）**

### 优秀标准（建议满足）
- 🌟 提示词设计专业，角色定义清晰
- 🌟 节点布局美观，逻辑流向清晰
- 🌟 关键节点有 fail-branch 错误处理
- 🌟 使用合适的插件依赖
- 🌟 变量命名语义化
- 🌟 Code 节点包含合理的数据转换逻辑
- 🌟 自动化校验全部通过

## 触发关键词

- "生成 Dify 工作流" / "创建 Dify 智能体"
- "Dify DSL" / "Dify YML"
- "帮我搭一个 Dify 应用"
- "Dify workflow 配置"

## 文件索引

| 文件 | 用途 |
|------|------|
| `references/dsl-structure.md` | 完整 DSL 结构规范（含 0.6.0 变量字段要求） |
| `references/node_types.md` | 20+ 节点类型详解 |
| `references/edge_types.md` | 连接类型与验证规则 |
| `references/node_positioning.md` | 节点坐标布局规范 |
| `references/workflow_structure.md` | 工作流图结构详解 |
| `references/node_selection.md` | 节点选型决策树 |
| `scripts/validate_workflow.py` | 自动化校验脚本（含 Dify 0.6 变量字段校验） |
| `scripts/dify_import.py` | Dify API 导入脚本（推荐，比浏览器自动化更可靠） |
| `scripts/generate_id.py` | 节点 ID 生成器 |
| `assets/*.yml` | 7 个场景模板 |
| `CHECKLIST.md` | 验证检查清单（人工核对版） |

## 参考资料

- Dify 官方文档: https://docs.dify.ai
- Dify GitHub: https://github.com/langgenius/dify
- DSL Schema: https://github.com/langgenius/dify/tree/main/api/core/workflow
