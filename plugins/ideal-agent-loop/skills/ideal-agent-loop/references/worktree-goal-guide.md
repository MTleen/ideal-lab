# development Profile：可选 Worktree Adapter

Worktree 不是 Kernel 原语。只有 Profile 声明
`adapters.workspace=git-worktree-optional` 且项目启用该 adapter 时，才按本
文创建 goal 级 worktree。未配置时继续在调用方提供的 workspace 中运行；
非开发 Profile 不需要理解本协议。

启用时，本 adapter 可复用开发 Worker 的 worktree 规范（路径、命名、创建
和删除），但 Worker locator 由 Capability Registry 决定，Kernel 不硬编码。

## 基本原则

启用 adapter 后，每个出队 goal 在独立 worktree 中执行阶段任务；未启用
时不创建或删除 worktree。无论是否启用，同一 Goal revision 的 lease 和 Run
记录都由公共协议管理。

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

兼容层可以把 worktree 信息记录为 Run artifact；不得写入 Markdown 需求池，
也不得把 `.agent-loop/` 兼容状态提升为第二个 Goal 事实源。

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
