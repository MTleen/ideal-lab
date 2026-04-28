# Ralph 合约模板

本文档是 `.ralph/{task-name}/contract.json` 的完整模板。每个字段附有填写说明和示例。

合约以 JSON 为事实源（contract.json），同时生成人类可读的 Markdown 版本（contract.md）。当两者不一致时，以 JSON 为准。

---

## 完整模板（JSON）

```json
{
  "description": "{用户原始任务描述}",
  "input": [
    { "desc": "{已有文件路径或上下文描述}", "inferred": false }
  ],
  "output": [
    { "path": "{文件路径}", "type": "{新建/修改}", "desc": "{交付物描述}" }
  ],
  "criteria": [
    {
      "id": 1,
      "desc": "{标准描述}",
      "verify_type": "{script|llm_judgment|hybrid}",
      "command": "{验证命令，llm_judgment 时为 null}",
      "affected_files": ["{文件路径}"]
    }
  ],
  "implementation": {
    "method": "{写代码/迭代 skill/文档/混合}",
    "step": "small"
  },
  "constraints": {
    "max_iterations": 20
  },
  "meta": {
    "phase": "clarify",
    "created_at": "{YYYY-MM-DD HH:mm}"
  }
}
```

---

## 渲染版模板（contract.md）

contract.md 由 contract.json 自动渲染，格式如下：

```markdown
# Ralph Task Contract

## Task Description
{用户原始任务描述}

## Input
- {已有文件路径或上下文描述} (inferred, unconfirmed)
- {已确认的输入项}

## Output
| # | Deliverable | Type | Description |
|---|-------------|------|-------------|
| 1 | {文件路径} | {新建/修改} | {交付物描述} |

## Acceptance Criteria
| # | Standard | Verify Type | Command |
|---|----------|-------------|---------|
| 1 | {标准描述} | {verify_type} | {command} |

## Implementation
- Method: {实施方式}
- Step size: small

## Constraints
- Max iterations: {N}

## Meta
- Phase: {当前阶段}
- Created: {创建时间}
```

---

## 字段说明

### description

**必填**。抄录用户的原始任务描述，不做改写。

```json
"description": "给登录模块添加 OAuth2.0 支持，支持 GitHub 和 Google 两种第三方登录"
```

---

### input

**必填**。列出任务开始时的已有资源。

每项是一个对象，包含 `desc`（描述）和 `inferred`（是否为推断值）。

```json
"input": [
  { "desc": "src/auth/login.ts（当前登录模块）", "inferred": false },
  { "desc": "src/auth/session.ts（会话管理）", "inferred": false },
  { "desc": "docs/api-spec.yaml（API 规范文档）", "inferred": false },
  { "desc": "已有用户名/密码登录功能，需要在此基础上扩展", "inferred": false }
]
```

**当用户使用"直接开干"跳过此维度时**：使用默认值，标记 `inferred: true`。

```json
"input": [
  { "desc": "当前目录下的已有文件", "inferred": true }
]
```

---

### output

**必填**。以数组形式列出所有预期交付物。

| 字段 | 说明 | 可选值 |
|------|------|--------|
| `path` | 文件路径或产物名称 | 具体路径 |
| `type` | 新建还是修改 | `"新建"` / `"修改"` |
| `desc` | 交付物的简要说明 | 自由文本 |

```json
"output": [
  { "path": "src/auth/oauth.ts", "type": "新建", "desc": "OAuth2.0 核心逻辑" },
  { "path": "src/auth/login.ts", "type": "修改", "desc": "集成 OAuth 登录流程" },
  { "path": "src/config/oauth.ts", "type": "新建", "desc": "OAuth 配置（client_id 等）" },
  { "path": "tests/auth/oauth.test.ts", "type": "新建", "desc": "OAuth 模块单元测试" }
]
```

**注意**：交付物的粒度应与验收标准对应。每个交付物至少对应一条验收标准。

---

### criteria

**必填**。这是合约的核心，LOOP 阶段围绕这些标准迭代。

| 字段 | 说明 | 格式 |
|------|------|------|
| `id` | 标准序号 | 1, 2, 3... |
| `desc` | 可验证的具体描述 | 必须可判定"通过/不通过" |
| `verify_type` | 验证方式 | `"script"` / `"llm_judgment"` / `"hybrid"` |
| `command` | 验证命令 | script/hybrid 时必填；llm_judgment 时为 `null` |
| `affected_files` | 涉及的文件列表 | 文件路径数组（用于重新验证机制） |

```json
"criteria": [
  {
    "id": 1,
    "desc": "OAuth 模块可正常导入，无语法错误",
    "verify_type": "script",
    "command": "npx tsc --noEmit src/auth/oauth.ts",
    "affected_files": ["src/auth/oauth.ts"]
  },
  {
    "id": 2,
    "desc": "GitHub OAuth 登录流程完整（重定向->回调->token 获取->用户创建）",
    "verify_type": "llm_judgment",
    "command": null,
    "affected_files": ["src/auth/oauth.ts", "src/routes/auth.ts"]
  },
  {
    "id": 3,
    "desc": "测试覆盖率 >= 80%",
    "verify_type": "hybrid",
    "command": "npx vitest run --coverage tests/auth/oauth.test.ts",
    "affected_files": ["tests/auth/oauth.test.ts"]
  }
]
```

**编写原则**：
- 每条标准必须可明确判定"通过"或"不通过"
- 避免模糊描述（如"代码质量高"、"性能好"）——应量化（如"响应时间 < 200ms"）
- 标准之间不应有重复覆盖

---

### implementation

**必填**。描述实现途径。

| 字段 | 可选值 | 说明 |
|------|--------|------|
| `method` | `"写代码"` / `"迭代 skill"` / `"文档"` / `"混合"` | 主要实施手段 |
| `step` | 固定为 `"small"` | 每次只做最小可验证步骤 |

```json
"implementation": {
  "method": "写代码",
  "step": "small"
}
```

---

### constraints

**可选**。默认值如下：

```json
"constraints": {
  "max_iterations": 20
}
```

用户可自定义：
- 调大迭代次数（复杂任务）
- 调小迭代次数（简单任务快速失败）

---

### meta

**自动生成**。不需要用户填写。

```json
"meta": {
  "phase": "clarify",
  "created_at": "2026-04-26 14:30"
}
```

`phase` 在合约生成时为 `"clarify"`，用户确认后更新为 `"loop"`。

---

## 合约确认检查

生成合约后，Ralph 应自行检查以下项目：

| 检查项 | 要求 |
|--------|------|
| description | 非空，反映用户原始意图 |
| input | 至少有一项 |
| output | 至少有一个交付物 |
| criteria | 至少有一条标准，每条可判定通过/不通过 |
| verify_type | 每条标准都有明确的验证方式 |
| command | script/hybrid 类型必须有命令 |
| affected_files | 尽可能填写，用于重新验证机制 |
| implementation | 已填写 method 和 step |
| meta | phase 和 created_at 已填 |

以上检查全部通过后，才展示给用户确认。
