# Loop 配置（loop.yaml）

ideal-agent-loop outer loop 的执行环境（worktree 策略、合并 gate）由 loop 配置控制。本文件定义配置格式、解析规则与字段。

## 配置定位（项目级，每项目独立一份）

**loop 配置是项目级的**：每个项目在自己的**项目根**放配置，A/B 项目的 loop 配置互不影响。skill 只读项目根的配置文件，**不读全局 `~/.claude/` 或用户级配置**。跨项目复用的是 skill 的 worktree-per-goal **能力**，不是配置本身。

解析顺序复用 `ideal-backlog` 的 AGENTS.md 范式（与「需求池路径」完全一致）：

1. 读项目 `AGENTS.md` 的 `loop 配置：X` 声明（相对项目根）→ 用 X
2. 否则默认 `.ideal/loop.yaml`
3. 文件不存在 → 用全默认值（见下），不报错
4. 父目录不存在 → `mkdir -p` 创建

> 跨项目零改 skill：想覆盖默认，在该项目 `AGENTS.md` 写一行 `loop 配置：path/to/loop.yaml`（相对项目根），或在默认位置放 `.ideal/loop.yaml`。什么都没有就走全默认。

## 字段

| 字段 | 默认值 | 取值 | 说明 |
|------|--------|------|------|
| `worktree` | `per-goal` | `per-goal` / `off` | `per-goal` = 每个 goal 一个独立 worktree；`off` = 不建 worktree，直接在当前分支跑 |
| `merge_gate` | `confirm` | `auto` / `confirm` / `pr` | goal 完成后合并 base_branch 的策略（详见 `merge-gate.md`） |
| `base_branch` | `main` | 分支名 | 合并目标分支；goal worktree 从此分支拉，完成后合回 |
| `branch_prefix` | `feature` | `feature` / `fix` / `refactor` 等 | goal 分支前缀，分支名 = `{prefix}/REQ-{NNN}-{slug}` |
| `worktree_root` | `worktrees` | 目录名（相对 repo toplevel） | goal worktree 存放根目录 |

## AGENTS.md 声明示例

```text
loop 配置：.ideal/loop.yaml
```

## loop.yaml 完整示例

```yaml
worktree: per-goal
merge_gate: confirm
base_branch: main
branch_prefix: feature
worktree_root: worktrees
```

## merge_gate 行为摘要

| gate | 行为 |
|------|------|
| `auto` | goal 完成 → fast-forward 合并 base_branch → 推送 → 清理 worktree。全自动接力，不停 |
| `confirm` | goal 完成 → 暂停，展示 report/trace/task 矩阵/真机证据 → 用户确认后执行 `auto` 的合并清理 |
| `pr` | goal 完成 → 委托 `ideal-dev-workflow/ideal-delivery` 走 PR 流程（`gh pr create` → 等合并 → 清理） |

逐步执行见 `merge-gate.md`。

## 设计原则

- **软约定**：本配置由 ideal-agent-loop（LLM）读 SKILL.md 解析执行，现有脚本（`agent_loop_state.py` / `agent_loop_verify.py` / `agent_loop_stop_hook.py`）不读配置，保持现状。
- **默认安全**：默认 `merge_gate: confirm`——合并主分支是 outward-facing 且会成为后续 goal 的基线，默认留轻量 gate。需要全自动接力时改 `auto`，需要人工 review 时改 `pr`。
- **与需求池路径同范式**：解析规则与 `ideal-backlog` 的 `需求池路径：` 完全一致，项目侧体验统一，跨项目零改 skill。
