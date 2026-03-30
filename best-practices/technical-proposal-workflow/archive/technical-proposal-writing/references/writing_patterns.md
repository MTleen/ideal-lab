# 技术提案写作模式库

## 1. What-Why-How 模式

这是技术描述的核心模式，每个技术都必须包含这三个要素。

### 标准模板
```
我们将采用[Technology]。

[Technology]是一种[Definition]。它具有[Feature 1]、[Feature 2]和[Feature 3]的特点。

我们选择[Technology]是因为[Reason 1]、[Reason 2]和[Reason 3]。
首先，[Detailed Reason 1]；其次，[Detailed Reason 2]；第三，[Detailed Reason 3]。

在实现上，我们将[Implementation Details]。具体来说，[Specific Implementation Approach]。

这种方案的优势在于[Advantage 1]和[Advantage 2]。这使得[Benefit 1]，并确保[Benefit 2]。
```

### 示例：MQTT协议
```
我们将采用MQTT协议进行数据传输。

MQTT（Message Queuing Telemetry Transport）是一种专为物联网场景设计的轻量级发布/订阅模式协议，由IBM和Eclipse基金会共同维护。它具有低带宽占用（最小报文仅2字节）、低功耗和高可靠性的特点。

我们选择MQTT是因为其独特的设计理念非常适合大规模传感器网络。首先，其发布/订阅模式实现了数据生产者和消费者的完全解耦，使得系统架构更加灵活可扩展；其次，MQTT支持三种QoS（服务质量）等级，可以根据数据重要性灵活配置可靠性保证；第三，作为IoT领域的事实标准，MQTT拥有广泛的设备支持和成熟的开源实现。

在实现上，我们将部署EMQ X作为MQTT Broker集群，采用3节点高可用部署模式。传感器数据将被封装成JSON格式，包含传感器ID、时间戳、测量值、状态码等标准字段，通过主题"sensors/{type}/{location}"进行发布。每个传感器将保持长连接，采用QoS 1级别确保消息至少传递一次。

这种基于MQTT的分布式采集架构具有显著优势。第一，高可扩展性，通过增加Broker节点即可线性扩展接入能力，理论上可支持百万级传感器；第二，高可靠性，QoS机制和本地缓存策略确保数据不丢失；第三，低延迟，协议开销小，EMQ X高性能确保数据采集延迟低于100毫秒。
```

## 2. 问题-解决方案模式

用于描述技术方案如何解决具体问题。

### 标准模板
```
问题：[Specific Problem Description]
挑战：[Why this problem is challenging to solve]
传统方案的局限性：[Limitations of conventional approaches]

解决方案：[Our Solution Approach]
核心技术：[Key technologies used]
实现策略：[Implementation strategy]

预期效果：[Expected Results with specific metrics]
相比传统方案：[Comparison with traditional approach]
```

### 示例：异常检测系统
```
问题：无线电领域的异常样本稀少且类型多样，传统的监督学习方法难以获得足够的标注数据。
挑战：异常信号可能出现在任何频段，且形态各异，无法预先定义所有异常类型。同时，正常信号的模式也会随时间变化，增加了检测难度。
传统方案的局限性：基于规则的方法需要人工编写大量规则，维护成本高且难以覆盖所有情况；监督学习方法需要大量标注数据，在异常检测场景下难以获得。

解决方案：我们采用基于卷积自编码器的无监督学习策略，让模型通过学习大量正常数据来建立"正常"的基准模式，从而能够识别任何偏离正常模式的异常信号。
核心技术：卷积自编码器（CAE）用于特征提取，时频分析用于信号预处理，动态阈值用于异常判定。
实现策略：首先对信号进行短时傅里叶变换生成频谱图，然后输入CAE进行压缩-重构，计算重构误差作为异常得分。

预期效果：检测准确率达到90%以上，误报率低于5%，能够检测包括未知类型在内的各种异常信号。
相比传统方案：无需人工标注异常样本，可自动适应新的异常类型，维护成本降低80%。
```

## 3. 对比模式

用于证明选择的方案优于替代方案。

### 标准模板
```
传统方法：[Traditional Approach Description]
实现方式：[How traditional method works]
局限性：[Limitations and problems]

本方案：[Our Approach Description]
技术优势：[Technical advantages]
性能指标：[Performance metrics]

对比结果：
- 效率提升：[Quantitative improvement]
- 成本降低：[Cost reduction]
- 可扩展性：[Scalability improvement]
- 维护性：[Maintainability improvement]
```

### 示例：数据处理架构
```
传统方法：采用批处理架构，定时（如每小时）收集数据进行批量处理。
实现方式：数据先暂存在文件系统，达到时间或数量阈值后触发批处理作业。
局限性：实时性差，延迟可达小时级别；资源利用率低，波峰波谷明显；故障恢复慢，需要重新处理整个批次。

本方案：采用流处理架构，实现数据的实时处理和分析。
技术优势：基于Apache Flink的流处理引擎，支持事件时间处理，精确一次语义；窗口操作灵活，支持滚动、滑动、会话窗口；状态管理完善，支持大状态状态快照和恢复。
性能指标：处理延迟低于1秒，吞吐量达到每秒10万条事件，故障恢复时间小于30秒。

对比结果：
- 实时性提升：从小时级别降低到秒级别，提升99.9%
- 资源利用率：弹性伸缩机制下，资源成本降低60%
- 数据新鲜度：从T+1降低到准实时，业务价值显著提升
- 运维复杂度：自动故障恢复，人工干预减少80%
```

## 4. 分层架构模式

用于描述复杂系统的分层设计。

### 标准模板
```
整体架构：本系统采用分层架构设计，从[Bottom/Top]至[Top/Bottom]分为[N]层。

[Layer 1 Name]：负责[Layer 1 Function]。采用[Technology 1]实现，主要特点包括[Feature 1]、[Feature 2]。
[Layer 2 Name]：负责[Layer 2 Function]。采用[Technology 2]实现，通过[Interface]与[Layer 1 Name]交互。
[Layer 3 Name]：负责[Layer 3 Function]。采用[Technology 3]实现，提供[Capability]给上层使用。

层间交互：各层之间通过标准接口进行解耦，[Interaction Protocol 1]确保[Guarantee 1]，[Interaction Protocol 2]确保[Guarantee 2]。

架构优势：这种分层设计实现了[Benefit 1]、[Benefit 2]和[Benefit 3]。
```

### 示例：微服务架构
```
整体架构：本系统采用微服务架构设计，从下至上分为基础设施层、数据服务层、业务服务层、聚合服务层和表现层。

基础设施层：负责系统的基础运行环境。采用Kubernetes容器编排平台，实现服务的自动部署、扩缩容和故障自愈。通过Prometheus进行监控，ELK Stack进行日志聚合。

数据服务层：负责数据的存储和访问。采用PostgreSQL 14存储关系型数据，Redis 6.2作为缓存层，InfluxDB 2.0存储时序数据。各数据服务通过统一的Repository模式对外提供数据访问接口。

业务服务层：负责核心业务逻辑的处理。采用Spring Boot框架开发，包括用户管理服务、订单处理服务、支付服务、库存服务等独立服务。服务间通过gRPC进行同步通信，通过Kafka进行异步消息传递。

聚合服务层：负责组合多个业务服务提供复合功能。采用GraphQL聚合多个后端服务的API，通过BFF（Backend for Frontend）模式为不同前端提供定制化的数据接口。

层间交互：各层之间通过RESTful API和RPC调用进行通信，API网关负责路由、认证和限流。服务网格（Istio）提供服务发现、负载均衡和安全通信。

架构优势：这种分层微服务架构实现了服务独立部署和扩展、技术栈灵活选择、故障隔离能力强、团队并行开发等优势。
```

## 5. 实施路线模式

用于描述项目的实施计划。

### 标准模板
```
**阶段[Number]：[Phase Name]（[Duration]）**
本阶段的主要任务是[Primary Tasks]。预计周期为[Duration]，投入[Resources]资源。

主要工作包括：
1. [Task 1 Description]：[Sub-task details]，交付成果包括[Deliverable 1]
2. [Task 2 Description]：[Sub-task details]，交付成果包括[Deliverable 2]
3. [Task 3 Description]：[Sub-task details]，交付成果包括[Deliverable 3]

关键里程碑：[Key Milestones]
风险控制：[Risk mitigation strategies]
```

### 示例：系统开发阶段
```
**阶段3：系统开发与集成（3个月）**
本阶段的主要任务是将核心算法工程化为可运行的系统，并完成各模块的集成测试。预计周期为3个月，投入8名开发工程师和2名测试工程师资源。

主要工作包括：
1. 后端服务开发：基于Spring Boot框架开发RESTful API服务，实现用户管理、数据处理、算法调用等核心功能，交付成果包括后端服务集群
2. 前端界面开发：基于React框架开发Web管理界面，实现数据可视化、系统监控、用户交互等功能，交付成果包括响应式Web应用
3. 系统集成测试：开发自动化测试套件，包括单元测试、集成测试、性能测试，交付成果包括完整测试报告和测试环境

关键里程碑：第1个月完成后端核心服务，第2个月完成前端主要功能，第3个月完成系统集成和测试
风险控制：采用持续集成/持续部署（CI/CD）流水线确保代码质量，使用Mock服务降低开发依赖，建立每日构建和冒烟测试机制
```

## 6. 量化证据模式

用于提供具体的数据支撑。

### 标准模板
```
性能指标：
- 处理能力：达到[Number] [Unit]/[Time unit]
- 响应延迟：平均[Number]ms，P99达到[Number]ms
- 吞吐量：支持[Number]并发用户/请求
- 可用性：达到[Number]%

对比数据：
- 相比[Baseline]，效率提升[Number]%
- 相比传统方案，成本降低[Number]%
- 处理时间从[Original Time]缩短至[New Time]
- 资源利用率提升[Number]%

业务价值：
- 用户满意度提升至[Number]%
- 运维成本降低[Number]万元/年
- 业务处理能力扩大[Number]倍
- 故障恢复时间从[Original Time]减少至[New Time]
```

### 使用建议
1. **数据来源**：使用实际测试数据、行业报告、类似项目的公开数据
2. **保守估计**：在不确定的情况下使用保守的数字
3. **可验证性**：确保数据可以被验证或通过测试证明
4. **上下文**：说明数据的具体条件和适用场景
5. **对比基准**：明确对比的基准或传统方案