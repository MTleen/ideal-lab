# 节点选型决策树

## 入口判断

```
用户需求
  │
  ├─── 简单对话/问答 ─────────────────→ LLM 类
  │
  ├─── 需要外部能力 ──────────────────→ 工具类
  │       ├── API 调用 ─────────────→ HTTP Request
  │       ├── 知识库检索 ────────────→ Knowledge Retrieval
  │       ├── 代码处理 ──────────────→ Code
  │       └── 工具集调用 ────────────→ Tool / Agent
  │
  ├─── 需要逻辑控制 ──────────────────→ 控制流类
  │       ├── 二元分支 ──────────────→ If-Else
  │       ├── 多元分类 ─────────────→ Question Classifier
  │       ├── 列表遍历 ──────────────→ Iteration
  │       └── 条件循环 ──────────────→ Loop
  │
  ├─── 数据转换/聚合 ────────────────→ 数据处理类
  │       ├── 字符串模板 ───────────→ Template Transform
  │       ├── 修改变量 ──────────────→ Variable Assigner
  │       ├── 合并分支 ─────────────→ Variable Aggregator
  │       └── 列表操作 ──────────────→ List Operator
  │
  └─── 参数提取 ──────────────────────→ Parameter Extractor
```

## 一、按输入类型选型

### 1.1 文本输入

| 输入类型 | 子场景 | 推荐节点组合 |
|---------|--------|------------|
| 单行短文本 | 简单问答 | Start → LLM → Answer |
| 多行长文本 | 内容分析/摘要 | Start → LLM → Answer |
| 多轮对话 | 带上下文对话 | Start → LLM → Answer（advanced-chat） |
| JSON 数据 | 结构化解析 | Start → Parameter Extractor → [后继节点] |

### 1.2 文件输入

| 输入类型 | 子场景 | 推荐节点组合 |
|---------|--------|------------|
| 图片 | OCR 识别 | Start → LLM(vision) → Answer |
| 图片 | 图像描述 | Start → LLM(vision) → Answer |
| PDF/文档 | 内容提取 | Start → Document Extractor → LLM → Answer |
| 多文件 | 批量处理 | Start → Iteration → [处理节点] → Answer |
| 音频 | 语音转文字 | Start → LLM → Answer（speech_to_text） |

### 1.3 参数输入

| 输入类型 | 推荐节点 |
|---------|---------|
| 下拉选择 | Start(select) → [后继节点] |
| 数字输入 | Start(number) → [后继节点] |
| 布尔开关 | Start(checkbox) → [后继节点] |

## 二、按 LLM 角色选型

### 2.1 标准 LLM 调用

**场景**：通用对话、文本生成、翻译、总结

```
Start → LLM → Answer
```

**何时用**：
- 纯对话场景
- 文本生成/改写/翻译
- 简单问答
- 需要控制 temperature/max_tokens 等参数

### 2.2 带工具调用的 Agent

**场景**：复杂任务、自主规划、多工具协同

```
Start → Agent → Answer
        ↑
     [Tool 1]
        ↑
     [Tool 2]
        ↑
     [Tool N]
```

**何时用**：
- 需要自主决定调用哪些工具
- 任务路径不确定
- 需要多轮工具调用循环
- ReAct 模式的 Agent

### 2.3 带上下文的 RAG

**场景**：知识库问答、私域知识检索

```
Start → Knowledge Retrieval → LLM → Answer
```

**何时用**：
- 基于文档/知识库回答
- 需要引用特定来源
- 企业知识管理

## 三、按外部能力选型

### 3.1 HTTP Request

**何时用**：
- 调用第三方 API（天气、股票、翻译等）
- 查询数据库
- 调用内部微服务
- Webhook 触发

**是否需要错误处理**：
- ✅ 必须有：API 不稳定、网络超时
- 建议策略：`fail-branch` + 错误恢复 LLM

### 3.2 Code 节点

**何时用**：
- 数据格式转换（JSON → 字符串）
- 数据过滤/排序
- 字符串拼接/正则提取
- 简单计算逻辑
- 日期/时间处理

**语言选择**：
- `python3`：数据处理首选
- `javascript`：轻量逻辑

### 3.3 Tool 工具节点

**何时用**：
- Dify 内置工具（搜索、计算器、天气）
- 自定义 API 工具
- 插件工具

## 四、按控制流选型

### 4.1 If-Else 二元分支

**何时用**：
- 按条件走不同路径
- 简单是/否判断
- 错误分流

```
Start → If-Else ──True──→ 分支A → Answer
           └──False──→ 分支B → Answer
```

### 4.2 Question Classifier 多元分类

**何时用**：
- 多意图识别（>2 种）
- 用户类型分流
- 场景分类

### 4.3 Iteration 列表迭代

**何时用**：
- 批量处理文件列表
- 对数组每个元素执行相同操作
- 批量生成/批量查询

### 4.4 Loop 循环

**何时用**：
- 固定次数重复
- 直到条件满足退出
- 轮询重试（配合 HTTP Request）

## 五、按数据处理选型

| 需求 | 节点 | 示例 |
|------|------|------|
| 字符串模板替换 | `template-transform` | "您好，{{name}}" |
| 修改变量值 | `variable-assigner` | `counter = counter + 1` |
| 合并多分支变量 | `variable-aggregator` | 聚合 success/fail 两路结果 |
| 列表过滤 | `list-operator` | 过滤出符合条件的元素 |
| 提取参数 | `parameter-extractor` | 从文本中提取结构化参数 |

## 六、输出节点选型

### 6.1 Answer 节点

**何时用**：
- 需要流式输出
- 中途返回结果
- Chatflow 模式（多轮对话）

### 6.2 End 节点

**何时用**：
- Workflow 模式（单次任务）
- 明确终止流程
- 不需要流式输出

## 七、完整场景决策表

| 场景 | 节点链 | 模板文件 |
|------|--------|---------|
| 简单问答 | Start → LLM → Answer | simple_llm_workflow.yml |
| 图片 OCR | Start → LLM(vision) → Answer | ocr_workflow.yml |
| 带知识库问答 | Start → Knowledge → LLM → Answer | simple_llm_workflow.yml |
| API 调用+容错 | Start → HTTP → If-Else → [分支] → Answer | error_handling_workflow.yml |
| 意图分流 | Start → Classifier → [N路] → Answer | conditional_workflow.yml |
| 数据库查询 | Start → LLM → HTTP → Code → LLM → Answer | data_query_workflow.yml |
| 工具型 Agent | Start → Agent → [Tools] → Answer | agent_workflow.yml |
| 批量 OCR | Start → Iteration → LLM(vision) → Answer | iteration_workflow.yml |
| 多步骤数据处理 | Start → Code → If-Else → [分支] → Aggregator → Answer | error_handling_workflow.yml |
| 带参数的复杂任务 | Start → Parameter Extractor → [后继] → Answer | 数据查询/Agent 模板 |

## 八、节点组合经验

1. **HTTP + Code 是黄金搭档**：HTTP 取数 → Code 清洗 → LLM 生成
2. **If-Else 之后必接 Aggregator**：多分支最终需要汇合
3. **Agent 不要滥用**：简单任务不要用 Agent，直接用 LLM
4. **Iteration 慎用**：大数据量场景注意性能
5. **Parameter Extractor 放在 LLM 之前**：用于结构化用户输入
