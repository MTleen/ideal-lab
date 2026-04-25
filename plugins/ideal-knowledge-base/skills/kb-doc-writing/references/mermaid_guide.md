# Mermaid 图表编写指南

本指南为知识库文档中各类 Mermaid 图表提供模板、规范与示例。

---

## 一、系统架构图

### 1.1 模板模式

使用 `graph TB`（从上到下）方向，按层次组织节点。

```mermaid
graph TB
    subgraph 应用层["应用服务层"]
        A1[服务A]
        A2[服务B]
    end

    subgraph 服务层["业务服务层"]
        S1[服务X]
        S2[服务Y]
        S3[服务Z]
    end

    subgraph 数据层["数据存储层"]
        D1[(数据库A)]
        D2[(数据库B)]
        D3[(缓存)]
    end

    A1 --> S1
    A2 --> S2
    S1 --> D1
    S1 --> D3
    S2 --> D2
    S3 --> D1
    S3 --> D2
```

### 1.2 常见布局模式

**三层架构：**

```mermaid
graph TB
    subgraph 展示层["展示层"]
        UI[Web前端 / 移动端]
        GW[API Gateway]
    end

    subgraph 业务层["业务逻辑层"]
        SVC1[用户服务]
        SVC2[数据服务]
        SVC3[通知服务]
    end

    subgraph 数据层["数据层"]
        DB[(MySQL)]
        ES[(Elasticsearch)]
        REDIS[(Redis)]
    end

    UI --> GW
    GW --> SVC1 & SVC2 & SVC3
    SVC1 --> DB & REDIS
    SVC2 --> DB & ES
    SVC3 --> REDIS
```

**四层架构：**

```mermaid
graph TB
    subgraph L4["应用层"]
        APP1[Web 应用]
        APP2[API 服务]
    end

    subgraph L3["服务层"]
        S1[认证服务]
        S2[核心业务服务]
        S3[任务调度服务]
    end

    subgraph L2["数据层"]
        D1[(PostgreSQL)]
        D2[(MongoDB)]
        D3[(Redis)]
    end

    subgraph L1["基础设施层"]
        MQ[Kafka]
        OBJ[MinIO]
        LOG[ELK Stack]
    end

    APP1 & APP2 --> S1 & S2 & S3
    S1 & S2 --> D1 & D3
    S3 --> D2 & MQ
    S2 --> MQ
    S3 --> LOG
```

**微服务架构：**

```mermaid
graph TB
    subgraph 接入层["接入层"]
        NGINX[Nginx]
        GW[API Gateway]
    end

    subgraph 微服务群["微服务集群"]
        MS1[用户微服务]
        MS2[订单微服务]
        MS3[支付微服务]
        MS4[通知微服务]
    end

    subgraph 中间件["中间件"]
        REG[Nacos 注册中心]
        MQ[RocketMQ]
        CACHE[Redis Cluster]
    end

    subgraph 存储["数据存储"]
        DB[(MySQL 主从)]
        MG[(MongoDB)]
    end

    NGINX --> GW
    GW --> MS1 & MS2 & MS3 & MS4
    MS1 & MS2 & MS3 & MS4 -.注册/发现.-> REG
    MS2 --> MQ
    MS4 --> MQ
    MS1 & MS2 & MS3 --> CACHE
    MS1 & MS2 --> DB
    MS3 --> MG
```

### 1.3 节点样式规范

| 节点类型 | 语法 | 用途 |
|---------|------|------|
| 矩形 | `[名称]` | 服务、组件、模块 |
| 圆角矩形 | `(名称)` | 实体、通用组件 |
| 数据库 | `[(名称)]` | 数据库、数据存储 |
| 圆柱体 | `[(名称)]` | 数据库（与圆角矩形同语法，Mermaid 无原生圆柱体） |
| 菱形 | `{名称}` | 决策点、判断节点 |
| 平行四边形 | `[/名称/]` | 输入/输出 |
| 双圆 | `(((名称)))` | 外部系统 |
| 虚线连接 | `-.-` | 可选依赖、异步通信 |
| 粗线连接 | `===` | 核心数据流、主链路 |

**连接线标注：**

```mermaid
graph LR
    A[服务A] -->|同步调用| B[服务B]
    A -.->|异步消息| C[消息队列]
    B -->|HTTP/REST| D[外部API]
    C -->|事件通知| E[通知服务]
```

### 1.4 示例：典型数据平台架构

```mermaid
graph TB
    subgraph 数据源["数据源层"]
        SRC1[业务数据库 MySQL]
        SRC2[日志系统]
        SRC3[第三方 API]
        SRC4[文件系统 CSV/Excel]
    end

    subgraph 数据接入["数据接入层"]
        CDC[Flink CDC]
        KAFKA[Kafka 集群]
        FTP[SFTP 采集]
    end

    subgraph 数据处理["数据处理层"]
        SPARK[Spark ETL]
        FLINK_JOB[Flink 流处理]
        RULE[Drools 规则引擎]
    end

    subgraph 数据存储["数据存储层"]
        ODS[(ODS 原始层)]
        DWD[(DWD 明细层)]
        DWS[(DWS 汇总层)]
        DIM[(维度表)]
    end

    subgraph 数据服务["数据服务层"]
        API[数据 API]
        DASH[可视化看板]
        EXPORT[数据导出]
    end

    SRC1 --> CDC --> KAFKA
    SRC2 --> KAFKA
    SRC3 --> FTP
    SRC4 --> FTP

    KAFKA --> FLINK_JOB --> DWD
    KAFKA --> SPARK --> ODS --> DWD
    FTP --> SPARK

    DWD --> DWS
    DWD --> DIM

    DWS --> API & DASH & EXPORT
    DIM --> API
```

---

## 二、数据流图

### 2.1 模板模式

使用 `flowchart LR`（从左到右）方向，按数据处理阶段组织。

```mermaid
flowchart LR
    subgraph 输入["数据输入"]
        IN1[数据源A]
        IN2[数据源B]
    end

    subgraph 处理["数据处理"]
        P1[阶段1：采集]
        P2[阶段2：清洗]
        P3[阶段3：转换]
        P4[阶段4：加载]
    end

    subgraph 输出["数据输出"]
        OUT1[目标系统A]
        OUT2[目标系统B]
    end

    subgraph 存储["数据存储"]
        ST1[(临时存储)]
        ST2[(持久存储)]
    end

    IN1 & IN2 --> P1 --> P2 --> P3 --> P4
    P2 --> ST1
    P4 --> ST2
    P4 --> OUT1 & OUT2
```

### 2.2 数据处理管线模式

```mermaid
flowchart LR
    SRC[(源数据)] --> EXTRACT[数据抽取] --> VALIDATE[数据校验]
    VALIDATE -->|通过| TRANSFORM[数据转换]
    VALIDATE -->|失败| DLQ[(死信队列)]

    TRANSFORM --> ENRICH[数据富化]
    ENRICH --> DEDUP[去重处理]
    DEDUP --> QUALITY[质量检测]
    QUALITY -->|合格| LOAD[数据加载] --> TARGET[(目标存储)]
    QUALITY -->|不合格| REJECT[(异常数据)]
    REJECT --> ALERT[告警通知]
```

### 2.3 输入/处理/输出/存储标注规范

- **输入节点**：使用 `[名称]` 或 `[(名称)]`，标注数据类型与频率
- **处理节点**：使用 `[名称]`，标注处理动作
- **存储节点**：使用 `[(名称)]`，标注存储技术与保留策略
- **输出节点**：使用 `[名称]`，标注消费方
- **异常分支**：使用 `|条件|` 标注判断条件

### 2.4 示例：典型数据治理管线

```mermaid
flowchart LR
    subgraph 数据源["数据源"]
        DB1[(MySQL 业务库)]
        DB2[(Oracle 报表库)]
        LOG[应用日志]
    end

    subgraph 采集层["数据采集"]
        CDC[CDC 实时采集]
        BATCH[批量采集]
    end

    subgraph ODS["ODS 层"]
        ODS_RAW[(原始数据表)]
    end

    subgraph 处理层["数据清洗与治理"]
        CLEAN[数据清洗]
        STANDARD[标准化处理]
        MATCH[实体匹配]
        DEDUP[去重合并]
        QUALITY_CHECK[质量检测]
    end

    subgraph DWD["DWD 层"]
        DWD_CLEAN[(明细数据表)]
    end

    subgraph 质量管理["质量管理"]
        QUALITY_RULE[(质量规则库)]
        QUALITY_REPORT[(质量报告)]
        ALERT[异常告警]
    end

    DB1 --> CDC --> ODS_RAW
    DB2 & LOG --> BATCH --> ODS_RAW
    ODS_RAW --> CLEAN --> STANDARD --> MATCH --> DEDUP
    DEDUP --> QUALITY_CHECK -->|合格| DWD_CLEAN
    QUALITY_CHECK -->|不合格| QUALITY_REPORT --> ALERT
    QUALITY_RULE --> QUALITY_CHECK
```

---

## 三、功能模块关系图

### 3.1 模板模式

使用 `graph LR` 配合 `subgraph` 展示模块分组与依赖关系。

```mermaid
graph LR
    subgraph 核心模块["核心模块"]
        M01[M01 用户管理]
        M02[M02 权限控制]
        M03[M03 数据管理]
    end

    subgraph 扩展模块["扩展模块"]
        M04[M04 报表中心]
        M05[M05 消息通知]
        M06[M06 工作流引擎]
    end

    subgraph 外部依赖["外部依赖"]
        EXT1[((LDAP)))
        EXT2[((SMS 网关)))
    end

    M01 --> M02
    M03 --> M01
    M04 --> M03
    M05 --> M03
    M06 --> M01 & M05
    M01 -.-> EXT1
    M05 -.-> EXT2
```

### 3.2 模块依赖标注规范

| 连线类型 | 语法 | 含义 |
|---------|------|------|
| 实线箭头 | `A --> B` | 强依赖（A 必须依赖 B 才能运行） |
| 虚线箭头 | `A -.-> B` | 弱依赖 / 可选依赖 |
| 双向箭头 | `A <--> B` | 双向依赖 / 相互调用 |
| 带标注 | `A -->|API| B` | 标注依赖方式 |

### 3.3 示例：功能模块关系

```mermaid
graph LR
    subgraph 基础能力["基础能力层"]
        M01[M01 数据源管理]
        M02[M02 元数据采集]
        M03[M03 数据标准管理]
    end

    subgraph 治理能力["治理能力层"]
        M04[M04 数据质量检测]
        M05[M05 数据血缘分析]
        M06[M06 数据资产管理]
        M07[M07 治理工作流]
    end

    subgraph 应用层["应用展示层"]
        M08[M08 数据资产目录]
        M09[M09 质量监控看板]
        M10[M10 血缘可视化]
        M11[M11 治理报告]
    end

    M01 --> M02 & M04
    M02 --> M05 & M06
    M03 --> M04
    M04 --> M07 & M09
    M05 --> M10
    M06 --> M08 & M11
    M07 --> M04 & M05

    M08 --> M06
    M09 --> M04
    M10 --> M05
    M11 --> M04 & M06
```

---

## 四、部署架构图

### 4.1 模板模式

使用 `graph TB` 展示物理部署拓扑，用 subgraph 表示物理节点或集群。

```mermaid
graph TB
    subgraph 用户访问["用户访问层"]
        CLIENT[用户浏览器 / API 调用方]
    end

    subgraph 负载均衡["负载均衡层"]
        LB[Nginx / HAProxy<br/>192.168.1.10]
    end

    subgraph 应用集群["应用服务集群"]
        APP1[应用节点1<br/>4C8G<br/>192.168.1.11]
        APP2[应用节点2<br/>4C8G<br/>192.168.1.12]
        APP3[应用节点3<br/>4C8G<br/>192.168.1.13]
    end

    subgraph 中间件集群["中间件集群"]
        MQ[Kafka Broker<br/>3节点集群]
        CACHE[Redis Sentinel<br/>3节点集群]
    end

    subgraph 数据集群["数据存储集群"]
        DB[(MySQL 主从<br/>1主2从)]
        ES[(Elasticsearch<br/>3节点集群)]
    end

    CLIENT --> LB --> APP1 & APP2 & APP3
    APP1 & APP2 & APP3 --> MQ & CACHE
    APP1 & APP2 & APP3 --> DB & ES
```

### 4.2 物理部署拓扑要点

- 标注节点 IP / 域名（如有）
- 标注硬件规格（CPU / 内存）
- 标注集群规模（节点数量）
- 区分有状态服务与无状态服务
- 标注网络分区（如 DMZ / 内网 / 数据网段）

### 4.3 示例：Docker 部署拓扑

```mermaid
graph TB
    subgraph 宿主机["宿主机 192.168.1.100 (64C/256G)"]
        subgraph Docker["Docker Engine"]
            subgraph 网段["docker network: app-net"]
                NGINX[nginx:latest<br/>端口: 80/443]
                APP[app-server:latest<br/>端口: 8080<br/>副本: 3]
                WORKER[worker:latest<br/>端口: 8081<br/>副本: 2]
            end

            subgraph 中间件["docker network: middleware-net"]
                REDIS[redis:7-alpine<br/>端口: 6379]
                KAFKA[confluentinc/cp-kafka<br/>端口: 9092]
                ZOOKEEPER[confluentinc/cp-zookeeper<br/>端口: 2181]
            end

            subgraph 存储["docker network: data-net"]
                MYSQL[mysql:8.0<br/>端口: 3306]
                ES[elasticsearch:8.10<br/>端口: 9200]
                MINIO[minio/minio<br/>端口: 9000]
            end
        end

        VOLUMES[volumes: mysql_data, es_data, minio_data]
    end

    NGINX --> APP
    APP --> WORKER
    APP & WORKER --> REDIS & KAFKA
    WORKER --> MYSQL & ES
    KAFKA --> ZOOKEEPER
    APP --> MINIO
    MYSQL & ES & MINIO --> VOLUMES
```

---

## 五、分类专属图表

### 5.1 模型训练：训练管线图

```mermaid
flowchart TB
    subgraph 数据准备["数据准备阶段"]
        COLLECT[数据采集与汇聚]
        SPLIT[数据集划分<br/>训练集 70% / 验证集 15% / 测试集 15%]
        LABEL[数据标注]
    end

    subgraph 特征工程["特征工程阶段"]
        FE_EXTRACT[特征提取]
        FE_SELECT[特征选择]
        FE_ENCODE[特征编码与归一化]
    end

    subgraph 模型训练["模型训练阶段"]
        TRAIN[模型训练<br/>GPU: A100 x 4<br/>轮次: 50 epochs]
        EVAL[验证集评估]
        TUNE[超参调优<br/>Optuna 贝叶斯优化]
    end

    subgraph 模型评估["模型评估阶段"]
        TEST[测试集评估]
        BIAS[偏差分析]
        COMPARE[基线对比]
    end

    subgraph 部署["模型部署阶段"]
        EXPORT[模型导出 ONNX]
        SERVE[模型服务化 TorchServe]
        MONITOR[线上监控与漂移检测]
    end

    COLLECT --> SPLIT --> LABEL
    LABEL --> FE_EXTRACT --> FE_SELECT --> FE_ENCODE
    FE_ENCODE --> TRAIN --> EVAL
    EVAL -->|未达标| TUNE --> TRAIN
    EVAL -->|达标| TEST --> BIAS --> COMPARE
    COMPARE -->|通过| EXPORT --> SERVE --> MONITOR
    COMPARE -->|未通过| TRAIN
```

### 5.2 知识库：RAG 管线图

```mermaid
flowchart TB
    subgraph 知识入库["知识入库管线"]
        DOC[文档输入<br/>PDF/Word/网页]
        CHUNK[文档切分<br/>滑动窗口 512 tokens<br/>重叠 64 tokens]
        EMBED[向量化<br/>bge-large-zh-v1.5<br/>维度: 1024]
        STORE[向量存储<br/>Milvus 2.3]
        META[元数据索引<br/>Elasticsearch]
    end

    subgraph 检索增强["检索增强生成"]
        QUERY[用户查询]
        REWRITE[查询改写<br/>LLM 展开/缩写]
        RETRIEVE[混合检索<br/>向量检索 + BM25 关键词检索]
        RERANK[重排序<br/>bge-reranker-large]
        ASSEMBLE[上下文组装<br/>Top-K: 5]
    end

    subgraph 生成["大模型生成"]
        PROMPT[Prompt 构建<br/>系统提示 + 检索上下文 + 用户问题]
        LLM[大模型推理<br/>Qwen-72B-Chat]
        RESPONSE[生成回答]
        CITE[引用溯源]
    end

    subgraph 质量保障["质量保障"]
        HALLUC[幻觉检测]
        RELV[相关性校验]
    end

    DOC --> CHUNK --> EMBED --> STORE & META
    QUERY --> REWRITE --> RETRIEVE
    STORE & META --> RETRIEVE
    RETRIEVE --> RERANK --> ASSEMBLE
    ASSEMBLE --> PROMPT --> LLM --> RESPONSE
    RESPONSE --> CITE
    RESPONSE --> HALLUC & RELV
    HALLUC & RELV -->|不通过| RETRIEVE
```

### 5.3 智能体：Agent 决策流程图

```mermaid
flowchart TB
    START([用户输入]) --> PARSE[意图解析<br/>LLM 分类]
    PARSE --> PLAN[任务规划<br/>CoT 推理]

    PLAN --> TOOL_SELECT{需要调用<br/>外部工具?}

    TOOL_SELECT -->|是| EXEC[工具执行]
    TOOL_SELECT -->|否| GENERATE[直接生成回答]

    EXEC --> VALIDATE{工具执行<br/>是否成功?}

    VALIDATE -->|成功| OBSERVE[结果观察<br/>结构化解析]
    VALIDATE -->|失败| RETRY{重试次数<br/>小于 3?}

    RETRY -->|是| EXEC
    RETRY -->|否| FALLBACK[降级处理<br/>返回已有信息 + 错误提示]

    OBSERVE --> REASON[推理判断<br/>信息是否充分?]
    REASON -->|充分| GENERATE
    REASON -->|不充分| TOOL_SELECT

    GENERATE --> REVIEW[回答审查<br/>安全/合规/事实性]
    REVIEW -->|通过| OUTPUT([输出回答])
    REVIEW -->|不通过| REVISE[修正回答] --> REVIEW

    FALLBACK --> OUTPUT
```

---

## 六、语法注意事项

### 6.1 中文节点标签

- **节点 ID 使用英文**，显示文本使用中文：

```mermaid
graph LR
    A[数据采集] --> B[数据清洗]
```

- **避免在节点 ID 中使用中文**，否则可能导致渲染问题：

```mermaid
%% 错误写法 - 节点 ID 含中文
graph LR
    数据采集 --> 数据清洗

%% 正确写法 - 节点 ID 为英文
graph LR
    collect[数据采集] --> clean[数据清洗]
```

### 6.2 Subgraph 命名规范

- Subgraph 标题支持中文，使用双引号包裹：

```mermaid
graph TB
    subgraph layer1["数据接入层"]
        A[组件A]
    end
    subgraph layer2["数据处理层"]
        B[组件B]
    end
```

- Subgraph ID 使用英文，标题使用中文：

```mermaid
%% 正确
subgraph app_layer["应用服务层"]

%% 避免 - 标题不含引号可能导致解析异常
subgraph app_layer[应用服务层]
```

### 6.3 常见语法错误及修正

| 错误类型 | 错误写法 | 正确写法 | 说明 |
|---------|---------|---------|------|
| 箭头方向 | `A -- B` | `A --- B` 或 `A --> B` | 无箭头用 `---`，有箭头用 `-->` |
| 节点形状 | `A[文本]-->B(文本)` | 两种语法本身合法，但建议统一 | 保持风格一致 |
| 特殊字符 | `A[组件A/B]` | `A["组件A/B"]` | 含 `/` 等特殊字符时用引号包裹 |
| 连线标签 | `A --> B标签` | `A -->|标签| B` | 连线标签用 `\|标签\|` 语法 |
| 空格问题 | `A -->B` | `A --> B` | 箭头两侧加空格 |
| 中文括号 | `A（文本）` | `A["（文本）"]` | 中文括号需用引号包裹 |

### 6.4 长标签换行

使用 `<br/>` 在节点内换行：

```mermaid
graph TB
    A["数据采集服务<br/>Kafka Connect<br/>版本: 3.5.0"] --> B["ETL 引擎<br/>Apache Spark<br/>版本: 3.4.1"]
```

**注意事项：**
- `<br/>` 标签仅在双引号包裹的文本中生效
- 换行后的节点宽度会自动适配最长行
- 建议每行不超过 20 个中文字符，保持图表可读性
- 简洁优先，避免在节点中放入过多信息

### 6.5 图表大小控制

- **控制节点数量**：单张图建议不超过 20 个节点
- **拆分复杂架构**：超过 20 个节点时，考虑按层次拆分为多张子图
- **使用子图分组**：通过 subgraph 提升可读性
- **避免过度连线**：如果连线过于密集，考虑简化非核心依赖关系
