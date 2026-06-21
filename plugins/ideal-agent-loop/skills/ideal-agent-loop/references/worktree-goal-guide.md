# Goal 级 Worktree 协议

ideal-agent-loop outer loop 在 `worktree: per-goal` 时，为每个 goal 创建独立 worktree。本协议**复用 `ideal-dev-workflow/ideal-flow-control` 的 worktree 规范**（路径/命名/创建/删除，见 `ideal-flow-control/SKILL.md`「Git Worktree 协议」），下沉到 goal 粒度。

## 基本原则

每个出队的 goal 在独立 worktree 中执行完整生命周期（规划 → 各 task 闭环 → 合并），禁止在 `base_branch` 上直接跑 goal。同时只 1 个 active goal worktree（outer loop 串行出队）。

## 路径与命名（复用 flow-control）

- **路径**：`<repo_toplevel>/<worktree_root>/<sanitized-branch>`，`sanitized` = 分支名 `/` → `-`
- **分支**：`{branch_prefix}/REQ-{NNN}-{slug}`，如 `feature/REQ-001-native-agent-team`
- 默认 `worktree_root=worktrees`

示例：repo=`/Users/foo/Wrapday`，分支=`feature/REQ-001-native-agent-team` → `/Users/foo/Wrapday/worktrees/feature-REQ-001-native-agent-team`

> 路径/命名规范与 `ideal-flow-control` 一致，确保 goal worktree 被 flow-control 识别为合法 worktree（分支匹配 `feature/fix/refactor` + pwd 含 `worktrees`）。

## 创建（goal 出队后）

```bash
REPO=$(git rev-parse --show-toplevel)
BRANCH="feature/REQ-001-native-agent-team"
SANITIZED=$(echo "$BRANCH" | sed 's/\//-/g')
WORKTREE="$REPO/worktrees/$SANITIZED"
mkdir -p "$REPO/worktrees"
git worktree add -b "$BRANCH" "$WORKTREE" {base_branch}
cd "$WORKTREE"
# 验证
pwd | grep -q worktrees && git branch --show-current | grep -qE "^${branch_prefix}/"
```

## 切换验证（关键）

创建后必须 `cd` 进 goal worktree 并验证 `pwd` 含 `worktrees` + 分支正确。后续所有 task 在此 worktree 执行，直到 goal 合并后才退出。

## 与 task 级 worktree 的协调（复用，不新建）

goal worktree 内委托 `ideal-dev-workflow` 跑各 task 时，`ideal-flow-control` 检测到当前已在 worktree（`pwd` 含 `worktrees` + 分支匹配 `feature/fix/refactor`）→ **复用 goal worktree，跳过 task worktree 创建**。task 级用 commit 隔离（每 task 一 commit），不再开 task worktree。

> 依赖 `ideal-flow-control` 的「已在 worktree 则复用」guard。若 flow-control 仍试图新建 task worktree，视为 guard 缺失，需补 flow-control guard（本次增强已配套补上）。

## 状态记录

goal worktree 信息记录在 `.agent-loop/{goal}/state.json` 的 `meta.worktree`（`branch` / `path` / `created_at`），**不污染需求池.md**（需求池只管队列状态）。

## 删除（goal 合并后）

```bash
cd {repo_toplevel}
git worktree remove "$WORKTREE"
git branch -d "$BRANCH"   # 合并后删本地分支（pr 模式由 ideal-delivery 处理清理）
```

## 生命周期

```text
出队 goal（todo → doing）
  → 建 goal worktree + cd
  → 规划 + 各 task dev-workflow 闭环（复用 goal worktree，task 级只 commit）
  → goal 全 task passed + 全局审计
  → 按 merge_gate 合并 base_branch（见 merge-gate.md）
  → 删 goal worktree + 分支
  → goal done → 出队下一个（从更新后的 base_branch 拉）
```

## `worktree: off` 模式

不建 worktree，goal 直接在当前分支跑。适用于：无 git 仓库的项目、或明确不想隔离的场景。此模式下不建/删 worktree，但 `merge_gate` 仍适用（auto/confirm 直接合并当前分支到 base_branch；pr 建 PR）。
