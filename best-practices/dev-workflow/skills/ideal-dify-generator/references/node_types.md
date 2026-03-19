# 节点类型详解

## 按执行类型分类

| 类型 | 节点 | 说明 |
|------|------|------|
| ROOT | start | 工作流入口，定义输入变量 |
| ROOT | trigger-webhook | Webhook 触发 |
| ROOT | trigger-schedule | 定时触发 |
| ROOT | trigger-plugin | 插件触发 |
| ROOT | datasource | 数据源触发 |
| EXECUTABLE | llm | 大语言模型调用 |
| EXECUTABLE | agent | Agent 模式（工具调用循环） |
| EXECUTABLE | code | 代码执行 |
| EXECUTABLE | http-request | HTTP 请求 |
| EXECUTABLE | knowledge-retrieval | 知识库检索 |
| EXECUTABLE | template-transform | 字符串模板转换 |
| EXECUTABLE | tool | 工具调用 |
| EXECUTABLE | variable-assigner | 修改变量 |
| EXECUTABLE | variable-aggregator | 聚合变量 |
| EXECUTABLE | question-classifier | 意图分类 |
| EXECUTABLE | parameter-extractor | 参数提取 |
| EXECUTABLE | iteration | 列表迭代 |
| EXECUTABLE | loop | 循环执行 |
| EXECUTABLE | document-extractor | 文档提取 |
| EXECUTABLE | list-operator | 列表操作 |
| BRANCH | if-else | 条件分支 |
| RESPONSE | answer | 流式回复 |
| RESPONSE | end | 终止工作流 |

## 节点输出速查

| 节点类型 | 主要输出 | 其他输出 |
|---------|---------|---------|
| start | 定义的输入变量 | - |
| llm | text | usage, reasoning_content |
| agent | text | usage |
| code | outputs 中定义的所有字段 | error_message, error_type |
| http-request | body | status_code, headers, files |
| if-else | condition_result | - |
| knowledge-retrieval | result | - |
| iteration | output | iteration（当前次数） |
| loop | output | loop（当前次数） |
| question-classifier | class_name | usage |
| parameter-extractor | parameters 中定义的字段 | __is_success, __reason, __usage |
| variable-aggregator | output | - |
| template-transform | output | - |
| tool | text, files, json | - |
| document-extractor | - | 提取的内容字段 |

## 节点通用属性

所有节点都有以下内部属性（以 `_` 开头）：

- `_runningStatus`: 运行状态（running/succeeded/failed）
- `_connectedSourceHandleIds`: 已连接的源 handle
- `_connectedTargetHandleIds`: 已连接的目标 handle
- `_isSingleRun`: 单步调试模式
- `_isCandidate`: 拖拽连接中的临时节点
- `_children`: 容器节点的子节点
- `_iterationIndex`: 迭代中的当前索引
- `_loopIndex`: 循环中的当前索引
- `_retryIndex`: 重试次数

**注意**：这些属性是前端 UI 状态，不应写入 DSL 文件。
