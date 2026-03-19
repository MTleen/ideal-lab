# 边连接类型详解

## sourceHandle 类型

### 标准节点

```
sourceHandle: "source"
```

用于所有标准 EXECUTABLE 节点（llm、code、http-request 等）。

### 分支节点

```
# If-Else
sourceHandle: "true"    # 条件为真
sourceHandle: "false"   # 条件为假

# Question Classifier
sourceHandle: "分类标签1"  # 分类结果 1
sourceHandle: "分类标签2"  # 分类结果 2
sourceHandle: "false"   # 默认兜底
```

### 错误处理

```
# Code / HTTP Request / LLM / Tool 节点
sourceHandle: "success-branch"  # 成功
sourceHandle: "fail-branch"    # 失败
```

### 循环节点

```
sourceHandle: "loop"  # 继续循环
# 注意：循环节点也有普通 source
```

### 迭代节点

```
sourceHandle: "source"  # 迭代完成，继续后续
# 迭代内部的边使用普通 source
```

## 边 ID 命名规范

格式：`{source_id}-{sourceHandle}-{target_id}-target`

示例：
- `start-source-llm-target`
- `ifelse-true-handler-target`
- `code-success-branch-aggregator-target`
- `code-fail-branch-recovery-target`

## 常见连接模式

### 模式 1：线性流程

```
Start(source) → LLM(target)
  LLM(source) → Answer(target)
```

### 模式 2：If-Else 分支

```
Start(source) → IfElse(target)
  IfElse(true) → HandlerA(target)
  IfElse(false) → HandlerB(target)
  HandlerA(source) → Aggregator(target)
  HandlerB(source) → Aggregator(target)
  Aggregator(source) → Answer(target)
```

### 模式 3：错误处理

```
Start(source) → Code(target)
  Code(success-branch) → SuccessHandler(target)
  Code(fail-branch) → FailHandler(target)
  SuccessHandler(source) → Answer(target)
  FailHandler(source) → Answer(target)
```

### 模式 4：迭代

```
Start(source) → Iteration(target)
  Iteration(loop) → ProcessItem(target)
  ProcessItem(source) → Iteration(target)  # 循环回去
  Iteration(source) → EndItem(target)
  EndItem(source) → Answer(target)
```

### 模式 5：多工具 Agent

```
Start(source) → Agent(target)
  Agent(tool_1) → Tool1(target)
  Agent(tool_2) → Tool2(target)
  Agent(tool_3) → Tool3(target)
  Tool1(source) → Agent(target)  # 回流
  Tool2(source) → Agent(target)
  Tool3(source) → Agent(target)
  Agent(source) → Answer(target)
```

## 边验证规则

1. **唯一性**：同一对 source→target 之间不应有多条边（除非是不同的 sourceHandle）
2. **类型匹配**：`data.sourceType` 和 `data.targetType` 必须与实际节点类型一致
3. **无孤立边**：所有边的 source 和 target 都必须在 nodes 数组中存在
4. **handle 匹配**：sourceHandle 必须与源节点支持的 handle 类型匹配
5. **双向性**：如果 A 的 source 指向 B，B 的 source 不能指向 A（无环）
