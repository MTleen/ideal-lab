---
name: ideal-ralph
description: 苏格拉底式任务澄清 + 持久小步迭代验证循环。适用于需要保证完成质量的独立任务。
---

> **agents**: 独立编排器 — 不隶属 ideal-dev-workflow，可调用任何 skill（包括 ideal-dev-workflow 的各 phase skill）完成工作。

# ideal-ralph（Ralph 持久任务执行器）

## 角色定位

**任务守护者** — 通过苏格拉底式对话明确任务边界，然后以持久迭代循环确保每个验收标准都被满足。

职责：
1. 澄清任务（输入、输出、验证、实施方式）
2. 生成任务合约（contract.json + contract.md）
3. 持久迭代，小步推进
4. 验证每个标准，记录证据
5. 全部通过后生成完成报告

**不负责**：
- 替用户决定验收标准（只引导，不替代）
- 在验收标准不通过时擅自标记通过
- 跳过任何标准

---

## 核心架构：两阶段执行

```
CLARIFY（澄清）        LOOP（迭代循环）
┌─────────────┐      ┌──────────────────┐
│ 维度1: 输入  │      │ 读取 state.json   │
│ 维度2: 输出  │ ──→  │ 找未通过标准      │
│ 维度3: 验证  │ 确认  │ 执行最小步骤      │
│ 维度4: 实施  │ 合约  │ 运行验证          │
│              │      │ 更新 state.json   │
│ 生成合约文件  │      │ iteration++       │
└─────────────┘      └──────────────────┘
```

---

## Script Directory（硬约束层）

本插件包含三个 Python 脚本，作为 SKILL.md 软约束的硬约束补充。脚本路径均相对于插件根目录 `plugins/ideal-ralph/`。

| 脚本 | 路径 | 用途 |
|------|------|------|
| **ralph_state.py** | `scripts/ralph_state.py` | JSON 状态管理器。管理 `state.json` 和 `contract.json` 的读写、初始化、查询。 |
| **ralph_stop_hook.py** | `scripts/ralph_stop_hook.py` | Claude Code Stop Hook。阻止停止时使用 continuation-template.md 生成结构化 prompt，引导 Agent 继续工作。模板不存在时回退到纯文本。 |
| **ralph_verify.py** | `scripts/ralph_verify.py` | 验证执行器。根据 `verify_type` 执行 script / llm_judgment / hybrid 验证并更新状态。 |

### Hook 注册方式

将 `ralph_stop_hook.py` 注册到项目的 `.claude/settings.json` 或全局 `~/.claude/settings.json` 中：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/plugins/ideal-ralph/scripts/ralph_stop_hook.py"
          }
        ]
      }
    ]
  }
}
```

### 脚本共同约定

- 所有脚本使用 `#!/usr/bin/env python3`
- 所有脚本支持 `--help` 参数
- 状态文件路径使用 `.ralph/{task-name}/` 前缀
- 使用 `pathlib.Path` 处理所有路径
- 命令超时默认 120 秒
- 输出截断默认 500 字符

### mark-modified 子命令（ralph_state.py）

当 LOOP 中修改了文件，需要将受影响的已通过标准重置为 pending：

```bash
python3 scripts/ralph_state.py mark-modified \
    --state .ralph/{task-name}/state.json \
    --files src/auth/oauth.ts src/routes/auth.ts
```

此命令会：
1. 检查每个已通过（passed）标准的 `affected_files` 是否包含被修改的文件
2. 匹配到的标准状态重置为 `pending`，`evidence` 清空
3. 将修改的文件追加到 `modified_files` 列表
4. 保存更新后的 state.json

---

## Phase 0: PREFLIGHT（前置检查）

在开始 CLARIFY 之前，**必须**执行以下检查。如果检查不通过， Ralph LOOP 的铁律"不停止"无法执行。

### Step 1: 检查 Stop Hook 注册

读取项目级 `.claude/settings.json`，检查 `hooks.Stop` 中是否包含 `ralph_stop_hook.py`：

```bash
cat {project_root}/.claude/settings.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
hooks = data.get('hooks', {}).get('Stop', [])
found = any('ralph_stop_hook' in h.get('command','') for group in hooks for h in group.get('hooks', []))
print('registered' if found else 'not_registered')
"
```

如果结果为 `not_registered` → 继续 Step 2。

### Step 2: 添加 Hook 配置

先检测插件安装路径：

```bash
find ~/.claude/plugins -name "ralph_stop_hook.py" -path "*/ideal-ralph/*" 2>/dev/null | head -1
```

然后向用户说明：

> Ralph 需要 Stop Hook 来阻止 Agent 在验收标准未全部通过时停止。检测到项目级 `.claude/settings.json` 中未注册该 Hook，是否添加？

用户确认后，读取现有 `{project_root}/.claude/settings.json`（不存在则创建空对象），合并以下配置（不覆盖已有的其他 hooks）：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 {检测到的脚本绝对路径}"
          }
        ]
      }
    ]
  }
}
```

写入后通知用户配置已添加。

### Step 3: 验证 Hook 可执行

```bash
echo '{"cwd":"{project_root}"}' | python3 {脚本路径}
```

应输出 `{"decision": "block", ...}` 或无输出（取决于是否有活跃 Ralph 任务），不应报错。

验证通过后继续到 Phase 1: CLARIFY。

---

## Phase 1: CLARIFY（苏格拉底式澄清）

通过苏格拉底式询问，逐一明确 4 个维度。一次只问一个维度。

### 维度顺序与内容

| # | 维度 | 核心问题 | 典型追问 |
|---|------|----------|----------|
| 1 | **输入** | 任务的起点是什么？ | 已有哪些文件？需要什么上下文？数据源在哪里？ |
| 2 | **输出** | 完成后应该产生什么？ | 具体文件路径？期望的行为？状态变化？ |
| 3 | **验证方法** | 怎么判断输出是正确的？ | 有现成的测试命令？需要人工评审？客观+主观？ |
| 4 | **实施方式** | 通过什么途径实现？ | 直接写代码？迭代某个 skill？写文档？混合？ |

### 提问策略

```
每个维度的提问流程：

1. 开放式引导
   "让我们先确认一下输入。这个任务的起点是什么？"
   "你手边已经有哪些文件或上下文？"

2. 追问细节（苏格拉底式）
   "你提到了 xxx 文件，这个文件在哪个路径？"
   "除了 xxx，还有其他依赖吗？"
   "能给我一个具体的例子吗？"

3. 提供选项辅助（当用户不确定时）
   "验证方法通常有三种：
    A) 固定脚本验证 — 你提供 test/lint/build 命令
    B) LLM 自主判断 — 我根据标准逐条评估
    C) 混合验证 — 脚本做客观检查 + 我做主观判断
    你倾向哪种？"
```

### 用户快捷命令（随时可用）

| 命令 | 作用 |
|------|------|
| **够了 / 确认** | 跳到下一维度（当前维度按已有信息填充） |
| **直接开干** | 停止追问剩余维度，使用推断值填充，但仍需确认合约 |
| **修改 XX** | 回到某维度重新确认 |
| **取消** | 终止流程 |

### "直接开干"安全性

使用"直接开干"时：
- 停止追问剩余维度，使用推断值填充
- 未澄清的维度使用默认值填充，但在合约中标记为 **"推断值（未确认）"**
- 进入 LOOP 前，**仍需用户确认合约**
- 合约确认环节会展示所有推断值，让用户有机会修正

### 默认值（用户跳过时使用，均标记为推断值）

| 维度 | 默认值 |
|------|--------|
| 输入 | 当前目录下的已有文件 |
| 输出 | 根据任务描述推断 |
| 验证方法 | llm_judgment（LLM 自主判断） |
| 实施方式 | 直接写代码 |

### 合约生成

四个维度澄清完成后：

1. 生成合约文件：
   - `.ralph/{task-name}/contract.json`（机器可读，事实源）
   - `.ralph/{task-name}/contract.md`（人类可读，从 JSON 渲染）
2. 完整展示合约内容给用户
3. 等待用户确认：
   - "确认 / ok" -> 更新 contract.json 中 meta.phase 为 "loop"，进入 LOOP 阶段
   - "修改 XX" -> 返回对应维度重新确认
   - "取消" -> 终止

---

## Phase 2: LOOP（持久迭代循环）

用户确认合约后进入循环。**循环不会自行停止**，直到所有验收标准通过或触发终止条件。

### 单次迭代流程

```
Iteration N:

  Step 1: 读取状态
    ├─ 读取 .ralph/{task-name}/state.json
    ├─ 检查是否有已通过标准因文件修改需重新验证
    └─ 找到第一个状态不为 passed/manual_accept 的验收标准

  Step 2: 确定最小步骤
    ├─ 分析当前标准需要什么变更
    └─ 确定最小操作单元（文件级 / 函数级 / 配置级）

  Step 3: 执行步骤
    ├─ 直接写代码（简单任务）
    ├─ 调用 ideal-dev-workflow 的 skill（复杂编码任务）
    ├─ 调用 ideal-deep-research（调研任务）
    ├─ 调用其他 skill（文档编写等）
    └─ 混合方式

  Step 4: 运行验证
    ├─ IDENTIFY — 确定验证方式（script / llm_judgment / hybrid）
    ├─ EXECUTE — 执行验证（可调用 ralph_verify.py）
    ├─ READ — 读取验证结果
    └─ JUDGE — 判定通过/失败

  Step 5: 更新状态
    ├─ 更新 state.json 中的标准状态
    ├─ 记录证据 / 错误
    ├─ 同步生成 state.md（从 JSON 渲染的人类可读版）
    └─ iteration++

  Step 6: 检查终止条件
    ├─ 所有标准通过 -> 执行全局审计（Step 6.1）
    │   ├─ 审计通过 -> 生成 report.md，结束
    │   └─ 审计发现遗漏 -> 追加新标准到 state.json，回到 Step 1
    ├─ 超过最大迭代次数 -> 报告进度，等用户决策
    ├─ 连续 3 次同标准失败 -> 报告卡点，等用户决策
    └─ 否则 -> 回到 Step 1
```

### 全局审计（Step 6.1）

所有单项验收标准通过后、生成 report.md 之前，必须执行全局审计。详细指南见 `references/global-audit-guide.md`。

```
全局审计流程：

1. 重述目标 — 从 contract.json 读取 description，拆解为具体交付物
2. 构建清单 — 每个交付物对应一行：预期 → 实际证据 → 是否覆盖
3. 检查证据 — 读取实际文件/运行测试/检查命令输出（禁止依赖记忆）
4. 识别遗漏 — 缺失、部分完成、仅靠代理信号验证的都算遗漏
5. 决策：
   ├─ 无遗漏 → 生成 report.md
   └─ 有遗漏 → 为每个遗漏创建新标准（source: "global_audit"），回到 LOOP
```

**约束**：
- 全局审计最多执行 1 轮。追加新标准后不再执行第二次全局审计。
- 新追加的标准使用 `llm_judgment` 验证方式，`affected_files` 为空。
```

### 重新验证机制

当修改已通过标准关联的文件时，该标准状态重置为 `pending`：

- 每个 `CriterionState` 有 `affected_files` 字段，记录该标准涉及的文件
- 当 LOOP 中修改了某个文件时，检查哪些已通过标准的 `affected_files` 包含该文件
- 匹配到的标准状态重置为 `pending`，`evidence` 清空
- 下次迭代时会重新验证这些标准

### 验证流程详解

#### 固定脚本验证（script）

```
IDENTIFY: 标准 #N 的验证方式为 script: `{命令}`
EXECUTE:  运行 `{命令}`，捕获 stdout/stderr/exit code
READ:     读取命令输出
JUDGE:    exit code == 0 -> 通过；否则 -> 失败（附带输出）
```

#### LLM 自主判断（llm_judgment）

```
IDENTIFY: 标准 #N 的验证方式为 llm_judgment
EXECUTE:  列出该标准的具体要求
READ:     检查相关文件/代码
JUDGE:
  1. 逐条对照标准要求
  2. 满足 -> 记录证据（引用具体内容）
  3. 不满足 -> 记录差距（缺少什么）
  4. 全部满足 -> 通过；有任何不满足 -> 不通过
```

#### 混合验证（hybrid）

```
IDENTIFY: 标准 #N 的验证方式为 hybrid
EXECUTE:
  1. 先运行脚本部分（客观检查）
  2. 脚本通过后，执行 LLM 判断（主观检查）
READ:     读取两部分结果
JUDGE:    两部分都通过 -> 通过；任一失败 -> 失败
```

---

## 铁律（IRON LAW）

| # | 铁律 | 说明 |
|---|------|------|
| 1 | **不停止** | 所有验收标准通过前不允许停止。不输出"完成"或"看起来好了"。 |
| 2 | **不减范围** | 合约中的标准一个不能少。不能因为"太难了"就删标准。 |
| 3 | **不空承诺** | 每个"通过"必须有新鲜证据。禁止"应该可以了"、"理论上没问题"。必须展示具体证据。 |
| 4 | **小步前进** | 每次只做最小可验证步骤。不要一次改 5 个文件然后才验证。 |
| 5 | **卡点上报** | 连续 3 次同标准失败 -> 暂停，报告卡点，等用户决策。不要无限重试。 |
| 6 | **不代理** | 禁止用代理信号替代需求完成验证。"测试通过"≠"需求完成"。必须从目标出发逐项核实。全局审计是最后一道防线。 |

---

## 任务目录结构

以任务名隔离，所有状态文件放在 `.ralph/` 目录下：

```
.ralph/
├── {task-name-1}/
│   ├── contract.json       # 任务合约 - 机器可读（事实源）
│   ├── contract.md         # 任务合约 - 人类可读（从 JSON 渲染）
│   ├── state.json          # 迭代状态 - 机器可读（事实源）
│   ├── state.md            # 迭代状态 - 人类可读（从 JSON 渲染）
│   └── report.md           # 完成报告（全部通过后生成）
├── {task-name-2}/
│   ├── contract.json
│   ├── contract.md
│   ├── state.json
│   ├── state.md
│   └── ...
```

**命名规则**：`task-name` 使用小写英文 + 短横线，从用户任务描述中提取关键词。例如 `add-auth-module`、`fix-login-bug`、`refactor-api-layer`。

**双格式策略**：
- `.json` 文件是事实源，所有工具脚本读写 JSON
- `.md` 文件是人类可读渲染版，从 JSON 生成，仅供阅读
- 当两者不一致时，以 `.json` 为准

---

## 合约文件格式 (contract.json)

```json
{
  "description": "用户的原始任务描述",
  "input": [
    { "desc": "src/auth/login.ts（当前登录模块）", "inferred": false },
    { "desc": "当前目录下的已有文件", "inferred": true }
  ],
  "output": [
    { "path": "src/auth/oauth.ts", "type": "新建", "desc": "OAuth2.0 核心逻辑" }
  ],
  "criteria": [
    {
      "id": 1,
      "desc": "OAuth 模块可正常导入，无语法错误",
      "verify_type": "script",
      "command": "npx tsc --noEmit src/auth/oauth.ts"
    },
    {
      "id": 2,
      "desc": "GitHub OAuth 登录流程完整",
      "verify_type": "llm_judgment",
      "command": null,
      "affected_files": ["src/auth/oauth.ts", "src/routes/auth.ts"]
    }
  ],
  "implementation": {
    "method": "写代码",
    "step": "small"
  },
  "constraints": {
    "max_iterations": 20
  },
  "meta": {
    "phase": "clarify",
    "created_at": "2026-04-26 14:30"
  }
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `description` | 用户原始任务描述（不改写） |
| `input[].desc` | 输入项描述 |
| `input[].inferred` | 是否为推断值（未确认）。"直接开干"时跳过的维度标记为 true |
| `output[].path` | 交付物文件路径 |
| `output[].type` | `新建` 或 `修改` |
| `criteria[].id` | 标准序号 |
| `criteria[].desc` | 标准描述（必须可判定通过/不通过） |
| `criteria[].verify_type` | `script` / `llm_judgment` / `hybrid` |
| `criteria[].command` | script/hybrid 时的验证命令 |
| `criteria[].affected_files` | 该标准涉及的文件列表（用于重新验证机制） |
| `implementation.method` | 实施方式 |
| `constraints.max_iterations` | 最大迭代次数（默认 20） |
| `meta.phase` | `clarify` -> `loop`（用户确认后更新） |

详细字段说明见 `references/contract-template.md`。

---

## 状态文件格式 (state.json)

```json
{
  "task": "add-oauth",
  "iteration": 3,
  "max_iterations": 20,
  "started_at": "2026-04-26T14:30:00",
  "status": "active",
  "criteria": [
    {
      "id": 1,
      "desc": "OAuth 模块可正常导入",
      "verify_type": "script",
      "command": "npx tsc --noEmit src/auth/oauth.ts",
      "status": "passed",
      "attempts": 2,
      "last_error": null,
      "evidence": "Command exited with code 0",
      "updated_at": "2026-04-26T14:35:00",
      "affected_files": ["src/auth/oauth.ts"]
    },
    {
      "id": 2,
      "desc": "GitHub OAuth 登录流程完整",
      "verify_type": "llm_judgment",
      "command": null,
      "status": "pending",
      "attempts": 0,
      "last_error": null,
      "evidence": null,
      "updated_at": null,
      "affected_files": ["src/auth/oauth.ts", "src/routes/auth.ts"]
    }
  ],
  "modified_files": ["src/auth/oauth.ts"]
}
```

### 状态枚举

| 值 | 含义 |
|----|------|
| `pending` | 未开始验证 |
| `in_progress` | 正在验证 |
| `passed` | 验证通过（附带证据） |
| `failed` | 验证失败（附带差距） |
| `blocked` | 卡点（连续 3 次失败，等用户决策） |
| `manual_accept` | 人工验收通过（用户选择标记） |

### 增强字段

| 字段 | 说明 |
|------|------|
| `attempts` | 该标准的验证尝试次数 |
| `last_error` | 最后一次失败原因 |
| `evidence` | 通过证据（必须引用具体文件/内容） |
| `updated_at` | 最后更新时间（ISO 格式） |
| `affected_files` | 该标准涉及的文件列表（用于重新验证机制） |

---

## LLM 判断验证协议

当验证方式为 `llm_judgment` 时，严格按以下协议执行：

```
1. 列出该标准的具体要求（从合约中提取）
2. 检查相关文件/代码
3. 逐条对照：
   - 满足 -> 记录证据（引用文件路径 + 具体内容/行号）
   - 不满足 -> 记录差距（描述缺少什么）
4. 综合判定：
   - 全部满足 -> 通过，记录每条证据
   - 有任何不满足 -> 不通过，列出所有差距
```

**证据要求**：
- 必须引用具体文件路径
- 必须引用具体内容（不能只说"已检查"）
- 禁止模糊描述（"看起来对"、"应该可以"）

---

## 终止条件

| 条件 | 处理 |
|------|------|
| 所有标准通过 | 生成 `report.md`，展示完成报告 |
| 迭代超过上限（默认 20） | 报告当前进度和未完成标准，等用户决策 |
| 连续 3 次同标准失败 | 标记为 `blocked`，报告卡点原因，等用户决策 |
| 用户取消 | 清理状态（可选保留 contract.json 供参考） |

### 用户决策选项（卡点时）

```
卡点报告：
  标准 #N 已连续 3 次验证失败。
  失败原因：{具体差距}

  请选择后续处理方式：
    1. [调整标准] — 修改该标准的验证方式或内容
    2. [手动修复] — 你自己修复后让我重新验证
    3. [标记为人工验收] — 标记为 "manual_accept"（在最终报告中区分）
    4. [终止任务] — 生成当前进度报告并结束
```

**注意**：选项 3 "标记为人工验收" 不等于"跳过标准"。该标准在最终报告中被明确标记为"人工验收通过"，而非"Ralph 验证通过"。

---

## 完成报告格式 (report.md)

```markdown
# Ralph 完成报告

## 任务
{任务描述}

## 执行统计
- 总迭代：{N}
- 验收结果：{Ralph通过数} Ralph 通过 / {人工验收数} 人工验收 / 0 失败
- 耗时：从 {开始时间} 到 {结束时间}

## 验收结果
| # | 标准 | 验证方式 | 结果 | 证据 |
|---|------|----------|------|------|
| 1 | {标准描述} | script | Ralph 通过 | {命令输出摘要} |
| 2 | {标准描述} | llm_judgment | Ralph 通过 | {证据摘要} |
| 3 | {标准描述} | llm_judgment | 人工验收 | 用户确认 |

## 变更文件
- {文件路径} — {新建/修改} — {简要说明}
- ...

## 迭代历程
- 总共 {N} 次迭代
- 无卡点 / 卡点在第 {X} 次迭代（已解决）
```

---

## 与其他 skill 的关系

ideal-ralph 是上层编排器，可委托执行：

| 场景 | 委托目标 | 说明 |
|------|----------|------|
| 复杂编码任务 | `ideal-dev-workflow` 的 phase skill | 需求->方案->编码->测试全流程 |
| 调研任务 | `ideal-deep-research` | 技术调研、竞品分析 |
| 文档编写 | 直接写 / `ideal-wiki` | 根据复杂度选择 |
| 简单任务 | 直接写代码 | 不需要调度其他 skill |

**调用方式**：在 LOOP 的 Step 3（执行步骤）中，根据合约中约定的实施方式决定是否委托。

---

## 参考文件

| 文件 | 用途 |
|------|------|
| `references/contract-template.md` | 合约完整模板 + 字段填写说明 |
| `references/verification-guide.md` | 三种验证方式的详细指南 |
| `references/continuation-template.md` | Stop Hook continuation prompt 模板 |
| `references/global-audit-guide.md` | 全局审计详细指南 |
| `../../scripts/ralph_state.py` | JSON 状态管理器（硬约束） |
| `../../scripts/ralph_stop_hook.py` | Stop Hook 脚本（硬约束） |
| `../../scripts/ralph_verify.py` | 验证执行器（硬约束） |

---

## 质量检查清单

### PREFLIGHT 阶段
- [ ] 检查了项目级 `.claude/settings.json` 的 Stop Hook 注册
- [ ] 如未注册，已向用户确认并添加
- [ ] Hook 脚本可执行性已验证

### CLARIFY 阶段
- [ ] 4 个维度逐一确认（输入、输出、验证、实施）
- [ ] 合约文件已写入 `.ralph/{task-name}/contract.json` + `.ralph/{task-name}/contract.md`
- [ ] 未确认的维度标记为 `inferred: true`
- [ ] 合约内容已完整展示给用户
- [ ] 用户已确认合约

### LOOP 阶段
- [ ] 状态文件已写入 `.ralph/{task-name}/state.json` + `.ralph/{task-name}/state.md`
- [ ] 每次迭代只做一个最小可验证步骤
- [ ] 每个标准通过时有新鲜证据（非空承诺）
- [ ] 修改已通过标准相关文件时，标准状态重置为 pending
- [ ] 连续 3 次同标准失败已上报
- [ ] 所有标准通过后执行了全局审计（非代理信号）
- [ ] 全局审计通过后生成了 `report.md`
- [ ] 合约中的标准一个不少
