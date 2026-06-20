# Agent Loop 验证方式详细指南

本文档详细说明三种验证方式的使用场景、执行协议和判定标准。Agent Loop 在 LOOP 阶段执行验证时，必须严格遵循本指南。

---

## 概览

| 验证方式 | 标识 | 适用场景 | 验证器 |
|----------|------|----------|--------|
| 固定脚本验证 | `script: {命令}` | 有客观判定标准的场景 | automated |
| LLM 自主判断 | `llm_judgment` | 需要语义理解或主观评估的场景 | LLM |
| 混合验证 | `hybrid: script={命令} + llm_judgment` | 既有客观标准又有主观要求 | mixed |

---

## 1. 固定脚本验证（script）

### 何时使用

- 有现成的测试命令（`npm test`、`pytest`、`go test`）
- 有构建命令（`npm run build`、`tsc --noEmit`、`cargo build`）
- 有 lint 命令（`eslint`、`ruff check`、`golangci-lint`）
- 有自定义验证脚本
- 验收标准可以用 exit code 0/非0 判定

### 不适用场景

- 需要判断"代码是否易读"、"设计是否合理"
- 需要对比文档和实现的一致性
- 需要理解业务逻辑是否正确

### 执行协议

```
IDENTIFY:
  从合约中提取验证命令：script: `{命令}`
  确认命令在当前环境下可执行

EXECUTE:
  运行命令，捕获完整输出：
  - stdout（标准输出）
  - stderr（标准错误）
  - exit code（退出码）

READ:
  读取命令的完整输出

JUDGE:
  exit code == 0 → 通过
  exit code != 0 → 失败

  通过时记录：
  - 命令：{执行的完整命令}
  - 输出摘要：{stdout 的关键行}

  失败时记录：
  - 命令：{执行的完整命令}
  - exit code：{值}
  - 错误输出：{stderr 或 stdout 中的错误信息}
```

### 判定标准

| 结果 | 条件 |
|------|------|
| 通过 | exit code == 0 |
| 失败 | exit code != 0（附带输出供分析） |

### 注意事项

- 如果命令不存在或环境未配置，标记为 `failed`，在失败原因中说明"命令不可用"
- 不要为了通过验证而修改测试命令
- 命令输出应完整记录，不能截断关键错误信息

---

## 2. LLM 自主判断（llm_judgment）

### 何时使用

- 验收标准涉及语义正确性（"功能是否完整"、"逻辑是否正确"）
- 需要对比文档和实现的一致性
- 需要评估代码质量、可读性
- 没有现成的自动化测试命令
- 标准中有主观因素（"用户体验是否流畅"、"错误处理是否充分"）

### 不适用场景

- 有明确的自动化测试命令（应该用 script 验证）
- 纯客观标准（文件是否存在、行数是否达标）

### 执行协议

```
IDENTIFY:
  从合约中提取该标准的完整描述
  拆解为可逐条检查的子要求

EXECUTE:
  Step 1 — 列出子要求
    将标准拆解为具体的检查点。
    例如："登录功能完整"拆解为：
      a) 有登录表单组件
      b) 有提交逻辑
      c) 有错误处理
      d) 有成功/失败反馈

  Step 2 — 定位相关文件
    根据合约中的输出列表，定位需要检查的文件。

  Step 3 — 逐条检查
    对每个子要求：
    - 读取相关文件内容
    - 寻找满足该要求的证据
    - 找到 → 记录证据（文件路径 + 具体内容/行号）
    - 未找到 → 记录差距（缺少什么）

READ:
  汇总所有子要求的检查结果

JUDGE:
  所有子要求都有证据 → 通过
  有任何子要求缺少证据 → 不通过
```

### 判定标准

| 结果 | 条件 |
|------|------|
| 通过 | 每个子要求都有具体证据（文件路径 + 内容引用） |
| 不通过 | 有子要求缺少证据（列出差距） |

### 证据要求（关键）

LLM 判断的"通过"必须附带新鲜证据，禁止空泛描述：

**合格证据**：
```
✅ src/auth/oauth.ts 第 42-58 行：
   async function handleGitHubCallback(code: string) {
     const token = await exchangeCodeForToken(code);
     const user = await fetchGitHubUser(token);
     return createOrLinkUser(user);
   }
   完整实现了回调处理：code → token → 用户信息 → 创建/关联用户
```

**不合格证据**：
```
❌ "已检查 oauth.ts，GitHub 回调功能看起来是完整的"
❌ "代码逻辑正确"
❌ "应该可以了"
```

### 示例

**标准**：GitHub OAuth 登录流程完整（重定向 → 回调 → token 获取 → 用户创建）

**检查过程**：

| # | 子要求 | 证据 | 状态 |
|---|--------|------|------|
| a | GitHub 重定向入口 | `src/auth/oauth.ts:15` — `getGitHubAuthURL()` 生成 OAuth URL | 满足 |
| b | 回调处理路由 | `src/routes/auth.ts:23` — `GET /auth/github/callback` | 满足 |
| c | Token 交换 | `src/auth/oauth.ts:42` — `exchangeCodeForToken()` | 满足 |
| d | 用户创建/关联 | `src/auth/oauth.ts:58` — `createOrLinkUser()` | 满足 |

**判定**：通过。所有子要求均有具体证据。

---

## 3. 混合验证（hybrid）

### 何时使用

- 验收标准既有客观部分又有主观部分
- 例如："测试覆盖率 ≥ 80% 且测试用例设计合理"
  - 客观：覆盖率数字（脚本验证）
  - 主观：测试用例设计（LLM 判断）
- 例如："代码编译通过且架构设计合理"
  - 客观：编译是否成功（脚本验证）
  - 主观：架构是否合理（LLM 判断）

### 不适用场景

- 标准完全客观（纯 script）
- 标准完全主观（纯 llm_judgment）

### 执行协议

```
IDENTIFY:
  从合约中提取混合验证的两部分：
  - script 部分：{命令}
  - llm_judgment 部分：{主观标准}

EXECUTE:
  按顺序执行，先客观后主观：

  Step 1 — 脚本验证（客观）
    运行 {命令}
    捕获输出和 exit code

  Step 2 — 判断是否继续
    脚本验证失败 → 直接判定失败（不执行 LLM 判断）
    脚本验证通过 → 继续 Step 3

  Step 3 — LLM 判断（主观）
    按照上述"LLM 自主判断"协议执行
    逐条检查主观标准

READ:
  汇总两部分结果

JUDGE:
  脚本通过 AND LLM 通过 → 通过
  脚本失败 OR LLM 不通过 → 失败
  记录两部分各自的证据
```

### 判定标准

| 结果 | 条件 |
|------|------|
| 通过 | 脚本 exit code == 0 且 LLM 所有子要求有证据 |
| 失败 | 脚本 exit code != 0（附带输出），或 LLM 有子要求缺少证据 |

### 执行顺序说明

**先客观后主观**的原因：
1. 脚本验证通常更快，失败时可以立即返回
2. 如果代码连基本检查都过不了，主观评估没有意义
3. 避免浪费 LLM 判断的 token

### 示例

**标准**：测试覆盖率 ≥ 80% 且测试用例设计合理

**执行过程**：

```
Step 1 — 脚本验证
  命令：npx vitest run --coverage tests/auth/oauth.test.ts
  输出：Coverage: 87.3% (statements)
  exit code: 0
  结果：通过

Step 2 — 继续 LLM 判断

Step 3 — LLM 判断
  检查点：
  a) 正常路径测试 — tests/auth/oauth.test.ts:15-28 — 存在
  b) 异常路径测试 — tests/auth/oauth.test.ts:45-62 — 存在
  c) 边界情况测试 — tests/auth/oauth.test.ts:78-91 — 存在
  d) Mock 使用合理 — 外部 API 调用已 mock — 满足

  结果：通过

综合判定：通过
  - 脚本证据：覆盖率 87.3%，exit code 0
  - LLM 证据：4 个检查点全部满足
```

---

## 验证方式选择指南

在 CLARIFY 阶段帮助用户选择验证方式时，参考以下决策树：

```
该标准是否有现成的自动化命令？
├── 是 → 用 script
└── 否
    └── 该标准是否完全需要人工/语义判断？
        ├── 是 → 用 llm_judgment
        └── 否（两者都有）→ 用 hybrid
```

### 常见标准 → 验证方式映射

| 标准类型 | 推荐验证方式 | 示例命令 |
|----------|-------------|----------|
| 编译通过 | script | `npx tsc --noEmit` |
| 测试通过 | script | `npx vitest run` |
| Lint 通过 | script | `npx eslint src/` |
| 功能完整 | llm_judgment | — |
| 代码质量 | llm_judgment | — |
| 测试覆盖 + 用例质量 | hybrid | `npx vitest run --coverage` + LLM 评审用例 |
| 构建成功 + 架构合理 | hybrid | `npm run build` + LLM 评审架构 |
| 性能达标 | script | `node benchmark.js`（自定义脚本检查阈值） |
| 文档完整 | llm_judgment | — |
