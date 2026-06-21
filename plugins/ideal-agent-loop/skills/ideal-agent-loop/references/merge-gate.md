# 合并 Gate（merge_gate）

goal 全 task passed + 全局审计通过后，按 loop 配置的 `merge_gate` 合并主分支。三种 gate。配置解析见 `loop-config.md`。

## `auto`（全自动接力）

```text
1. cd {repo_toplevel}（退出 goal worktree）
2. git checkout {base_branch}
3. git merge --ff-only {goal_branch}     # 必须 fast-forward；非快进则降级 confirm
4. git push origin {base_branch}         # 有远程则推送；无远程跳过
5. git worktree remove {goal_worktree_path}
6. git branch -d {goal_branch}
7. 标 goal status=done → 出队下一个（不停）
```

**fast-forward 失败**（base_branch 有新提交、非快进）→ 降级 `confirm`，报告冲突让用户决策。**禁止 force push**。

## `confirm`（轻量确认，默认）

```text
1. goal 完成 → 暂停 outer loop，向用户展示：
   - .agent-loop/{goal}/report.md（完成报告 + 验收证据）
   - task-boundary-matrix 全 passed 证据
   - 真机验证证据（截图/录影/playwright 或 chrome-devtools 输出）
   - 即将执行：{goal_branch} → {base_branch}，merge_gate=confirm
2. 等用户确认：
   - "合并" / "确认" → 执行 `auto` 的 step 1-7
   - "再改改" / 拒绝 → 回 goal worktree 继续（goal 仍 doing）
3. 合并完成 → 出队下一个
```

## `pr`（PR review）

委托 `ideal-dev-workflow/ideal-delivery` 的完整 PR 流程（`ideal-delivery/SKILL.md` 第 82-96 行）：

```text
1. 确保 goal worktree 内所有改动已 commit
2. git push origin {goal_branch}
3. gh pr create --title "{type}: {goal 标题}" --body "变更概述/内容/检查清单/真机证据"
4. 暂停，等用户在远程（GitHub/GitLab）合并 PR（合并后告知 agent "已合并"）
5. 合并后：
   - cd {repo_toplevel} && git checkout {base_branch} && git pull
   - git worktree remove {goal_worktree_path}
   - git branch -d {goal_branch}
6. 标 goal status=done → 出队下一个
```

> 无远程仓库 / `gh` 未安装 → `ideal-delivery` 已有降级（提示用户手动去远程创建 PR）。

## 共通约束（三种 gate 都遵守）

- 合并后**必须**清理 goal worktree + 删本地分支，不留孤儿 worktree。
- 合并目标是 `base_branch`（默认 main），**不得**合并到其他 goal 的分支。
- `pr` 模式禁止跳过 PR 直接合并（除非无远程仓库）。
- 任何 gate 失败（fast-forward 冲突 / 推送失败 / PR 被拒）→ **不标 goal done**，报告卡点等用户决策（不无限重试）。
- 合并完成、worktree 清理后，才标 goal `status=done`，再出队下一个 goal（下一个 goal 从更新后的 base_branch 拉新 worktree，保证基线干净）。
