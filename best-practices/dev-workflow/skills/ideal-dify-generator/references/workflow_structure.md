# 工作流图结构详解

## graph 结构

```yaml
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    # 功能配置
  graph:
    viewport:
      x: 0
      y: 0
      zoom: 1.0
    nodes: []
    edges: []
```

## viewport 画布视图

```yaml
viewport:
  x: 0      # 画布 X 偏移（像素）
  y: 0      # 画布 Y 偏移（像素）
  zoom: 1.0 # 缩放级别（0.1 - 2.0）
```

## 执行模型

### 队列-事件驱动架构

```
GraphEngine（调度器）
    │
    ├── WorkerPool（线程池）→ 并行执行独立节点
    ├── VariablePool（变量池）→ 跨节点数据共享
    └── EdgeProcessor（边处理器）→ 条件路由
```

### 执行流程

1. **初始化**：GraphEngine 将根节点（start）放入 ReadyQueue
2. **并行执行**：Worker 线程从 ReadyQueue 取节点执行
3. **事件分发**：节点完成后推送事件到 event_queue
4. **依赖解析**：EdgeProcessor 处理事件，激活下游节点
5. **循环**：重复直到所有路径到达终节点
6. **完成**：End/Answer 节点执行后工作流结束

### 并行执行规则

- **同一层级节点自动并行**：如果 A 和 B 都依赖 Start，且互相无依赖，则并行执行
- **显式顺序**：如需强制顺序，用边连接强制串行
- **容器节点（Iteration/Loop）内部串行**

### 执行状态

| 状态 | 说明 |
|------|------|
| SCHEDULED | 排队中 |
| RUNNING | 执行中 |
| SUCCEEDED | 成功 |
| FAILED | 失败（未处理） |
| PARTIAL_SUCCEEDED | 部分成功（有错误处理） |
| STOPPED | 手动停止 |
| PAUSED | 等待人工输入 |

### 节点执行状态

| 状态 | 说明 |
|------|------|
| NOT_START | 未开始 |
| WAITING | 等待依赖完成 |
| LISTENING | 等待事件（Trigger 节点） |
| RUNNING | 执行中 |
| SUCCEEDED | 成功 |
| FAILED | 失败 |
| EXCEPTION | 失败但已处理（通过 fail-branch） |
| RETRY | 重试中 |
| STOPPED | 被停止 |
