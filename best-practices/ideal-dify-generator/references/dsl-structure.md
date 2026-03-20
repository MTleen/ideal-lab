# Dify DSL 结构详解（完整版）

本文档说明 Dify 工作流 DSL (YML) 文件的完整结构，适用于版本 0.3.0。

## 文件结构概览

```yaml
app:                    # 应用配置
dependencies:           # 插件依赖
kind: app
version: 0.3.0
workflow:              # 工作流配置
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    edges: []          # 节点连接
    nodes: []          # 节点定义
```

## 1. app 应用配置

```yaml
app:
  name: '工作流名称'
  description: '工作流详细描述'
  icon: '🤖'                    # Emoji 图标
  icon_background: '#FFEAD5'    # 图标背景色（16进制）
  mode: advanced-chat           # 工作流模式
  use_icon_as_answer_icon: false
```

### 工作流模式 (mode)

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `advanced-chat` | 高级对话（Chatflow） | 多轮对话、智能客服、RAG |
| `workflow` | 标准工作流 | 单次任务、数据处理、定时任务 |
| `agent-chat` | AI Agent | 工具调用、复杂自主规划 |

## 2. dependencies 插件依赖

```yaml
dependencies:
  - current_identifier: null
    type: marketplace
    value:
      marketplace_plugin_unique_identifier: '插件唯一标识符'
```

### 常用插件标识符

```yaml
# OpenAI 兼容接口
langgenius/openai_api_compatible:0.0.16@哈希值

# Markdown 导出器
bowenliang123/md_exporter:1.2.0@哈希值

# 数据库插件
plugin_author/database_plugin:版本@哈希值
```

## 3. workflow 工作流配置

### conversation_variables 对话变量

```yaml
conversation_variables: []   # ⚠️ 必须为空数组，不要在此定义任何变量
```

> **重要**：Dify DSL 导入时 `conversation_variables` 必须为空数组 `[]`。如果填入任何变量，会导致导入时报错或工作流节点显示异常。涉及跨节点状态传递时，使用 Code 节点的返回值或 HTTP Response 变量。
### environment_variables 环境变量

```yaml
environment_variables:
  - id: 环境变量ID
    name: 环境变量名
    value: 默认值
    value_type: string   # 必须有 value_type 字段（Dify 0.6.0+）
    description: 变量说明
```

> **⚠️ 关键注意（Dify 0.6.0+ 强制要求）**：
> - `environment_variables` 中每个变量**必须同时包含** `value` 和 `value_type` 字段
> - `conversation_variables` 中每个变量**必须同时包含** `value` 和 `value_type` 字段
> - 如果缺少这两个字段，Dify API 导入时会返回 `VariableError: missing value type`

### features 功能配置

#### 文件上传

```yaml
features:
  file_upload:
    enabled: true
    allowed_file_extensions: ['.jpg', '.png', '.pdf']
    allowed_file_types: ['image', 'document']
    allowed_file_upload_methods: ['local_file', 'remote_url']
    fileUploadConfig:
      file_size_limit: 15          # MB
      image_file_size_limit: 100   # MB
      audio_file_size_limit: 500   # MB
      batch_count_limit: 5
      number_limits: 3
    image:
      enabled: true
      number_limits: 3
      transfer_methods: ['local_file', 'remote_url']
```

#### 语音功能

```yaml
features:
  speech_to_text:
    enabled: true
    language: zh-CN
  text_to_speech:
    enabled: true
    language: zh-CN
    voice: alloy
```

#### 其他功能

```yaml
features:
  opening_statement: '欢迎使用智能助手'
  retriever_resource:
    enabled: true
  suggested_questions:
    - 问题1
    - 问题2
  suggested_questions_after_answer:
    enabled: false
```

## 4. graph 图结构

### nodes 节点

每个节点的通用结构：

```yaml
nodes:
  - data:
      # 节点类型特定配置
    id: '节点唯一ID'
    position:
      x: 100
      y: 300
    positionAbsolute:
      x: 100
      y: 300
    selected: false
    sourcePosition: right
    targetPosition: left
    type: custom
    width: 244
    height: 90
```

### edges 连接

```yaml
edges:
  - data:
      isInIteration: false
      isInLoop: false
      sourceType: start        # 源节点类型
      targetType: llm          # 目标节点类型
    id: '唯一连接ID'            # 格式: 源ID-source-目标ID-target
    source: '源节点ID'
    sourceHandle: source       # source | true | false | success-branch | fail-branch
    target: '目标节点ID'
    targetHandle: target       # 通常为 target
    type: custom
    zIndex: 0
```

## 5. 节点类型详解

### 5.1 Start 节点（根节点）

```yaml
- data:
    desc: ''
    title: 开始
    type: start
    variables:
      - label: 用户输入
        max_length: 1000
        options: []
        required: true
        type: paragraph
        variable: query
  id: 'start'
  position:
    x: 80
    y: 282
  type: custom
```

**变量类型（type）**：
- `paragraph`: 多行文本
- `text-input`: 单行文本
- `select`: 下拉选择
- `number`: 数字
- `file`: 文件上传
- `files`: 多文件上传

### 5.2 LLM 节点

> ⚠️ **必须包含 `variables` 声明**：当 prompt 模板中引用了输入变量（而非直接硬编码）时，必须在 `variables` 节中声明这些输入变量，并在 prompt 中使用变量名（而非 `{{#node_id.field#}}` 形式）。

```yaml
- data:
    context:
      enabled: false
      variable_selector: []
    model:
      completion_params:
        temperature: 0.7
        max_tokens: 2000
        top_p: 0.9
        frequency_penalty: 0
        presence_penalty: 0
      mode: chat
      name: gpt-4
      provider: openai
    prompt_template:
      - id: '提示词块ID'
        role: system
        text: 系统提示词
      - id: '提示词块ID'
        role: user
        text: '用户提示词：合同类型为 {{#contract_type#}}，内容为 {{#contract_text#}}'
    title: LLM节点
    type: llm
    # ⚠️ 如果 prompt 中引用了输入变量，必须声明 variables
    variables:
      - value_selector:
          - 'start'
          - contract_type
        variable: contract_type
      - value_selector:
          - '1740700000002'
          - text
        variable: contract_text
    vision:
      enabled: false
      configs:
        detail: high
        variable_selector: []
  id: '节点ID'
  position:
    x: 380
    y: 282
  type: custom
```

**prompt 中变量引用规则**：
- `{{#contract_type#}}` — 引用本地 `variables` 中 `variable: contract_type` 的值（推荐）
- `{{#start.contract_type#}}` — 直接引用节点 ID（⚠️ 不推荐，可能绕过 variables 链路验证）
- `{{#node_id.text#}}` — 引用上游节点输出（用于 context 等字段）

```yaml
- data:
    context:
      enabled: false
      variable_selector: []
    model:
      completion_params:
        temperature: 0.7
        max_tokens: 2000
        top_p: 0.9
        frequency_penalty: 0
        presence_penalty: 0
      mode: chat
      name: gpt-4
      provider: openai
    prompt_template:
      - id: '提示词块ID'
        role: system
        text: 系统提示词
      - id: '提示词块ID'
        role: user
        text: '用户提示词 {{#变量引用#}}'
    title: LLM节点
    type: llm
    vision:
      enabled: false
      configs:
        detail: high
        variable_selector: []
  id: '节点ID'
  position:
    x: 380
    y: 282
  type: custom
```

**常用 provider**：
- `openai`: OpenAI
- `anthropic`: Claude
- `alibaba`: 通义千问
- `langgenius/openai_api_compatible/openai_api_compatible`: 兼容接口

### 5.3 Code 代码执行节点

```yaml
- data:
    code: |
      def main(arg1: str) -> dict:
          return {"result": arg1, "status": "success"}
    code_language: python3  # python3 | javascript
    outputs:
      result:
        type: string
      status:
        type: string
    title: 代码执行
    type: code
    variables:
      - value_selector:
          - '源节点ID'
          - 输出变量名
        variable: arg1
  id: '节点ID'
  position:
    x: 680
    y: 282
  type: custom
```

### 5.4 HTTP Request 节点

```yaml
- data:
    authorization:
      config:
        api_key: ''
        header: ''
      type: no-auth  # no-auth | api-key | bearer
    body:
      data: '{"key": "{{#变量#}}"}'
      type: json  # none | form-data | x-www-form-urlencoded | json | raw-text
    headers: 'Content-Type: application/json'
    method: post  # get | post | put | patch | delete | head
    timeout:
      max_connect_timeout: 0
      max_read_timeout: 0
      max_write_timeout: 0
    title: HTTP请求
    type: http-request
    url: https://api.example.com/endpoint
    variables:
      - value_selector:
          - '节点ID'
          - 变量名
        variable: 变量名
  id: '节点ID'
  position:
    x: 680
    y: 282
  type: custom
```

### 5.5 If-Else 条件判断节点

```yaml
- data:
    cases:
      - case_id: 'true'    # ⚠️ 必须是字符串 "true"，不能是 "high"/"case1" 等
        conditions:
          - comparison_operator: is  # is | is not | contains | not contains | empty | not empty | > | < | >= | <=
            id: '条件ID'
            value: 'HIGH'
            variable_selector:
              - '节点ID'
              - 变量名
        id: 'true'
        logical_operator: and
      - case_id: 'false'  # ⚠️ 必须是字符串 "false"，不能是 "else"
        conditions:
          - comparison_operator: is
            id: '条件ID2'
            value: 'MEDIUM'
            variable_selector:
              - '节点ID'
              - 变量名
        id: 'false'
        logical_operator: and
    logical_operator: or  # and | or
    title: 条件判断
    type: if-else
  id: '节点ID'
  position:
    x: 380
    y: 300
  type: custom
```

> **关键规则**：`case_id` 必须是字符串 `"true"` 或 `"false"`，**不是** `"high"/"medium"/"case1"` 等业务语义值。对应边的 `sourceHandle` 也必须是 `'true'` 或 `'false'`，与 case_id 完全一致。

### 5.6 Tool 工具节点

```yaml
- data:
    provider_id: builtin
    provider_name: 提供者名称
    provider_type: builtin  # builtin | api | plugin
    title: 工具调用
    tool_configurations: {}
    tool_label: 工具标签
    tool_name: 工具名称
    tool_parameters:
      参数名:
        type: mixed
        value: '{{#变量#}}'
    type: tool
  id: '节点ID'
  position:
    x: 680
    y: 282
  type: custom
```

### 5.7 Answer 直接回复节点

```yaml
- data:
    answer: |
      {{#LLM节点ID.text#}}
    title: 直接回复
    type: answer
    variables: []
  id: 'answer'
  position:
    x: 980
    y: 282
  type: custom
```

### 5.8 Parameter Extractor 参数提取器

```yaml
- data:
    instruction: 提取指令说明
    is_array: false
    model:
      completion_params: {}
      mode: chat
      name: gpt-4
      provider: openai
    parameters:
      - description: 参数描述
        name: 参数名
        required: true
        type: string
    query:
      - role: user
        text: '{{#输入变量#}}'
    reasoning_mode: prompt
    title: 参数提取
    type: parameter-extractor
  id: '节点ID'
  position:
    x: 380
    y: 282
  type: custom
```

### 5.9 Variable Aggregator 变量聚合器

```yaml
- data:
    advanced_settings: null
    groups:
      - group_name: 分组1
        output_type: string
        variables:
          - value_selector:
              - '节点ID'
              - 变量名
            variable: 输出变量名
    title: 变量聚合器
    type: variable-aggregator
  id: '节点ID'
  position:
    x: 980
    y: 300
  type: custom
```

### 5.10 Iteration 迭代节点

```yaml
- data:
    iterator_selector:
      - 数组变量所在节点ID
      - 数组变量名
    output_selector:
      - 迭代内最后节点ID
      - 输出变量名
    output_type: string
    startNodeType: code
    start_node_id: 迭代起始节点ID
    title: 列表循环
    type: iteration
  id: '节点ID'
  position:
    x: 380
    y: 282
  type: custom
```

### 5.11 Loop 循环节点

```yaml
- data:
    loop_count: 10
    break_conditions:
      - case_id: break1
        condition:
          comparison_operator: is_not_empty
          id: '条件ID'
          value: ''
          variable_selector:
            - '节点ID'
            - 变量名
        id: break1
    title: 循环执行
    type: loop
  id: '节点ID'
  position:
    x: 380
    y: 282
  type: custom
```

## 6. 坐标系统

### 推荐布局

**水平流程**：
```
Start(80,282) → LLM(380,282) → Code(680,282) → Answer(980,282)
```

**垂直分支**：
```
              → 分支1(680,132)
If-Else(380,300) →
              → 分支2(680,468)
```

### 节点尺寸

| 节点类型 | 宽度 | 高度 |
|----------|------|------|
| Start | 244 | 90-150 |
| LLM | 244 | 90 |
| Code | 244 | 90 |
| If-Else | 244 | 120 |
| Answer | 244 | 90-143 |
| Iteration/Loop | 244 | 200+ |

## 7. 错误处理配置

### 节点级错误策略

```yaml
# abort（默认）- 失败时停止整个工作流
error_strategy: abort

# fail-branch - 失败时走替代路径
error_strategy: fail-branch

# default-value - 失败时返回默认值
error_strategy: default-value
default_value: '默认值'

# retry - 失败时重试
error_strategy: retry
retry_config:
  max_retries: 3
  retry_interval: 100
```

### 边连接（fail-branch 时）

```yaml
# 成功路径
- id: code-success-llm-target
  source: code_node_id
  target: llm_node_id
  sourceHandle: success-branch
  targetHandle: target

# 失败路径
- id: code-fail-handler-target
  source: code_node_id
  target: error_handler_id
  sourceHandle: fail-branch
  targetHandle: target
```

## 8. 版本兼容性

| Dify 版本 | DSL 版本 | 兼容性 |
|-----------|----------|--------|
| 0.8.0+ | 0.6.0 | ✅ 完全支持 |
| 0.6.0-0.7.x | 0.3.0 | ⚠️ 部分兼容 |
| < 0.6.0 | 0.1.0 | ❌ 不兼容 |

> **当前实测**：Dify 1.13.2 使用 DSL 版本 0.6.0 完全兼容。
> `version` 字段写 0.3.0 或 0.6.0 均可，API 会在导入时自动转换为最新版本。
