# Dify DSL 验证检查清单

此清单用于在生成 DSL 后进行人工核对，确保质量达标。

---

## 一、文件结构（必须项）

- [ ] YAML 格式正确，无语法错误
- [ ] 包含 `app` 配置块
- [ ] 包含 `kind: app`
- [ ] 包含 `version: 0.3.0`
- [ ] 包含 `workflow.graph.nodes` 数组
- [ ] 包含 `workflow.graph.edges` 数组

---

## 二、节点检查

### 根节点
- [ ] 存在唯一的根节点（start / datasource / trigger）
- [ ] 根节点 ID 正确（start 节点 ID 必须为 `start`）
- [ ] 根节点定义了必要的输入变量

### 终节点
- [ ] 存在至少一个 end 或 answer 节点
- [ ] 终节点不被任何边作为 source

### LLM 节点
- [ ] 配置了有效的 `provider`（openai / anthropic / alibaba 等）
- [ ] 配置了有效的 `model` 名称
- [ ] 配置了 `prompt_template`（至少包含 system 或 user 角色）
- [ ] 变量引用格式正确：`{{#node_id.field#}}`
- [ ] Vision 节点正确配置了 `variable_selector`

### Code 节点
- [ ] 配置了 `code_language`（python3 / javascript）
- [ ] 定义了 `outputs`，且与函数返回值匹配
- [ ] 定义了 `variables`，引用了前置节点的输出
- [ ] 如需错误处理，配置了 `error_strategy`

### HTTP Request 节点
- [ ] 配置了有效的 URL
- [ ] 配置了正确的 HTTP method
- [ ] 配置了正确的认证类型（no-auth / api-key / bearer）
- [ ] 定义了 `variables` 引用前置节点输出

### If-Else 节点
- [ ] 配置了 `cases`（至少一个 case）
- [ ] 每个 case 配置了 `comparison_operator` 和 `variable_selector`
- [ ] 分支两边都有边连接到后续节点

### 其他节点
- [ ] `variable-aggregator` 正确配置了 `groups` 和 `variables`
- [ ] `parameter-extractor` 配置了 `parameters` 和 `instruction`
- [ ] `iteration` / `loop` 配置了容器边界

---

## 三、边连接检查

- [ ] 所有边的 `source` 和 `target` 指向存在的节点 ID
- [ ] Start 节点无入边
- [ ] 终节点（end/answer）无边作为 source
- [ ] `if-else` 节点的每条分支都有边连接
- [ ] `fail-branch` 节点同时有 `success-branch` 和 `fail-branch` 两条边
- [ ] `sourceHandle` 类型与源节点类型匹配
- [ ] `targetHandle` 通常为 `target`
- [ ] `data.sourceType` 与源节点 `type` 一致
- [ ] `data.targetType` 与目标节点 `type` 一致
- [ ] 边 ID 命名规范：`{source}-{handle}-{target}-target`

---

## 四、变量引用检查

- [ ] 变量引用格式正确：`{{#节点ID.字段#}}`
- [ ] 所有 `{{#...#}}` 格式的引用都指向存在的节点
- [ ] 引用的字段在该节点的实际输出中存在
- [ ] System 变量引用正确：`{{#sys.query#}}`、`{{#sys.files#}}`
- [ ] 变量引用链路无断裂（前置节点 → 后继节点）

---

## 五、坐标布局检查

- [ ] Start 节点位于最左侧（x ≈ 80）
- [ ] 节点水平间距 ≥ 300px
- [ ] 分支节点 Y 坐标合理（±150px 偏移）
- [ ] 同级节点 Y 坐标一致
- [ ] 多分支汇合节点（Aggregator）Y 坐标居中
- [ ] 无节点坐标重叠
- [ ] Iteration/Loop 容器足够容纳内部节点

---

## 六、错误处理检查

- [ ] HTTP Request / Code / LLM 节点有合理的错误策略
- [ ] `fail-branch` 配置：同时有 success 和 fail 两条出边
- [ ] `retry` 配置：`max_retries` 和 `retry_interval` 合理
- [ ] 错误分支有降级处理（回复错误提示或默认值）
- [ ] 错误分支最终汇入主流程（通过 Aggregator）

---

## 七、功能配置检查

- [ ] 文件上传：已启用时配置了 `allowed_file_types` 和 `allowed_file_extensions`
- [ ] 语音功能：已启用时配置了 `language` 和 `voice`
- [ ] 知识库检索：已启用时正确配置了 `retriever_resource`
- [ ] 开场白：`opening_statement` 配置了欢迎语

---

## 八、插件依赖检查

- [ ] 如使用市场插件，在 `dependencies` 中声明
- [ ] 插件标识符格式正确：`author/repo:version@hash`
- [ ] 不使用插件时，`dependencies` 为空数组 `[]`

---

## 九、提示词质量检查

- [ ] System prompt 定义了清晰的 AI 角色
- [ ] Prompt 包含具体的输出格式要求
- [ ] Prompt 中无占位符未填充
- [ ] Prompt 长度适中（不过长也不过简）
- [ ] 敏感信息不在 prompt 中硬编码（使用环境变量）

---

## 十、测试验证

- [ ] 在 Dify 中成功导入 DSL
- [ ] 运行简单测试用例验证流程正确
- [ ] 测试边界条件（空输入、异常输入）
- [ ] 测试错误处理路径（触发 fail-branch）

---

## 快速检查项（生成后必查）

> 完成 DSL 生成后，至少检查以下 3 项：

1. **YAML 能被解析**：`python3 -c "import yaml; yaml.safe_load(open('output.yml'))"`
2. **节点链路完整**：根节点 → 终节点之间不断链
3. **变量引用格式**：所有 `{{#...#}}` 格式正确，无野引用

---

## 常见错误对照表

| 错误 | 原因 | 修复 |
|------|------|------|
| 导入 Dify 失败 | YAML 语法错误 | 用 `python3 -c "import yaml"` 校验 |
| 变量显示为空 | 变量引用节点 ID 错误 | 检查 `{{#node_id.field#}}` |
| 分支不执行 | If-Else 条件始终为假 | 检查 `comparison_operator` |
| Agent 死循环 | 工具调用未正确配置 | 检查 Agent prompt 和工具配置 |
| 图片无法识别 | Vision 未启用 | 检查 `vision.enabled: true` |
| API 调用失败 | 认证配置错误 | 检查 `authorization.type` |
