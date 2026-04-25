---
name: ideal-lab-maintainer
description: "ideal-lab monorepo 维护工具。用于：提交改动并自动生成 changeset（/maintainer commit）、新增 skill（/maintainer add-skill）、新增 plugin（/maintainer add-plugin）、发布版本（/maintainer release）、全量校验（/maintainer validate）。"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# ideal-lab Maintainer

这个 skill 用于维护 ideal-lab monorepo 中的 Claude Code 插件库。它覆盖日常高频动作：提交改动并生成 changeset、新增 skill、新增 plugin、发布版本、全量校验。

所有命令默认从仓库根目录执行。开始执行前，先确认当前目录包含根 `package.json`、`.claude-plugin/marketplace.json` 和 `plugins/` 目录；如果不在仓库根目录，先切换到仓库根目录。

## 通用约定

- 不要修改与当前任务无关的 plugin。
- 修改前先运行 `git status --short`，识别已有改动，避免覆盖用户未提交内容。
- 涉及 JSON 修改时，保持现有字段风格和缩进。
- plugin manifest 路径固定为 `plugins/<plugin-name>/.claude-plugin/plugin.json`。
- skill 路径固定为 `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`。
- 根 marketplace 路径固定为 `.claude-plugin/marketplace.json`。
- 根 `package.json` 已使用 `workspaces: ["plugins/*"]`，新增 plugin 时通常不需要修改 workspace 配置。
- 可优先使用本插件脚本：
  - `plugins/ideal-lab-maintainer/scripts/commit.sh`
  - `plugins/ideal-lab-maintainer/scripts/add-skill.sh`
  - `plugins/ideal-lab-maintainer/scripts/add-plugin.sh`
  - `plugins/ideal-lab-maintainer/scripts/release.sh`
  - `plugins/ideal-lab-maintainer/scripts/validate.sh`

## /maintainer commit

用于将当前改动整理成 changeset、更新版本并提交。

工作流程：

1. 运行 `git status --short` 检测改动。
2. 如果没有改动，直接汇报无需提交。
3. 分析受影响的 plugin：
   - 文件路径匹配 `plugins/<plugin-name>/...` 的改动归属到对应 plugin。
   - 根目录配置、changeset、文档等改动不自动归属 plugin，需要人工判断是否要包含在提交说明中。
4. 对每个受影响 plugin，询问用户 bump 类型：
   - `patch`：修复、文档、脚本、小改动。
   - `minor`：新增向后兼容能力、新 skill、新命令。
   - `major`：破坏性变更、行为或接口不兼容。
5. 询问或整理 changeset message。message 应简短说明用户可见变化，例如 `Add maintainer automation scripts`。
6. 为每个受影响 plugin 生成 `.changeset/<slug>.md`：

   ```md
   ---
   "plugin-name": patch
   ---

   Change summary.
   ```

7. 运行 `npx changeset version` 更新 workspace package 版本和 changelog。
8. 检查 `plugins/<plugin-name>/.claude-plugin/plugin.json` 的 `version` 是否与 `plugins/<plugin-name>/package.json` 一致。
9. 如果不一致，将 `plugin.json` 的 `version` 同步为 `package.json` 的版本。
10. 运行校验：
    - `plugins/ideal-lab-maintainer/scripts/validate.sh`
    - 如果只影响单个 plugin，也可以先运行 `claude plugin validate plugins/<plugin-name>`。
11. 运行 `git diff --stat` 和必要的 `git diff` 检查最终改动。
12. 执行 `git add` 并提交：

    ```bash
    git add .
    git commit -m "<message>"
    ```

脚本用法：

```bash
plugins/ideal-lab-maintainer/scripts/commit.sh <plugin-name> <patch|minor|major> "<message>"
```

脚本会生成 changeset、运行 `npx changeset version`、同步 `plugin.json` 版本、执行 `git add` 和 `git commit`。

## /maintainer add-skill

用于在已有 plugin 中新增 Claude Code skill 骨架。

工作流程：

1. 列出现有 plugin：

   ```bash
   find plugins -maxdepth 1 -mindepth 1 -type d | sort
   ```

2. 让用户选择目标 plugin。
3. 询问 skill 名称。名称应使用小写 kebab-case，例如 `ideal-dev-plan`。
4. 创建目录：

   ```text
   plugins/<plugin-name>/skills/<skill-name>/
   ```

5. 创建 `SKILL.md` 骨架，包含 frontmatter：

   ```md
   ---
   name: <skill-name>
   description: "<一句话说明触发场景和能力>"
   allowed-tools: Read, Write, Edit, Bash, Grep, Glob
   ---

   # <skill-name>

   ## Purpose

   TODO: describe when to use this skill.

   ## Workflow

   1. TODO
   ```

6. 提示用户编辑 `SKILL.md` 正文，补充触发条件、输入、输出、步骤、边界条件。
7. 运行 `claude plugin validate plugins/<plugin-name>` 验证目标 plugin。

脚本用法：

```bash
plugins/ideal-lab-maintainer/scripts/add-skill.sh <plugin-name> <skill-name> "<description>"
```

## /maintainer add-plugin

用于新增一个 ideal-lab plugin 目录并注册到 marketplace。

工作流程：

1. 询问 plugin 名称，使用小写 kebab-case，例如 `ideal-example-plugin`。
2. 询问 plugin 描述。
3. 创建目录结构：

   ```text
   plugins/<plugin-name>/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── skills/
   ├── package.json
   └── CHANGELOG.md
   ```

4. 写入 `.claude-plugin/plugin.json`：

   ```json
   {
     "name": "<plugin-name>",
     "version": "1.0.0",
     "description": "<description>",
     "author": { "name": "MTleen" },
     "skills": "./skills",
     "keywords": []
   }
   ```

5. 写入 `package.json`：

   ```json
   {
     "name": "<plugin-name>",
     "version": "1.0.0",
     "private": true
   }
   ```

6. 写入 `CHANGELOG.md` 初始内容。
7. 更新 `.claude-plugin/marketplace.json`，向 `plugins[]` 追加：

   ```json
   {
     "name": "<plugin-name>",
     "source": "./plugins/<plugin-name>",
     "description": "<description>",
     "category": "development",
     "keywords": []
   }
   ```

8. 根 `package.json` 已使用 `workspaces: ["plugins/*"]`，无需修改。
9. 运行：

   ```bash
   claude plugin validate plugins/<plugin-name>
   claude plugin validate .
   ```

脚本用法：

```bash
plugins/ideal-lab-maintainer/scripts/add-plugin.sh <plugin-name> "<description>"
```

## /maintainer release

用于发布已经完成 version/tag 的改动。

工作流程：

1. 检查本地是否有未推送 tag：

   ```bash
   git tag --sort=-creatordate | head
   git log --decorate --oneline --max-count=10
   ```

2. 检查当前分支与远端关系：

   ```bash
   git status --short --branch
   ```

3. 如果存在待发布 tag，执行：

   ```bash
   git push --follow-tags
   ```

4. 汇报推送结果。若没有 upstream 或推送失败，说明需要用户先配置远端分支。

脚本用法：

```bash
plugins/ideal-lab-maintainer/scripts/release.sh
```

## /maintainer validate

用于对 ideal-lab 插件库做全量校验。

工作流程：

1. 遍历 `plugins/*/`，逐个运行：

   ```bash
   claude plugin validate plugins/<plugin-name>
   ```

2. 运行 marketplace 校验：

   ```bash
   claude plugin validate .
   ```

3. 检查所有 plugin 的版本一致性：
   - `plugins/<plugin-name>/.claude-plugin/plugin.json`
   - `plugins/<plugin-name>/package.json`
   - 两者 `version` 必须一致。
4. 检查所有 `SKILL.md` frontmatter：
   - 文件以 `---` 开始。
   - frontmatter 以第二个 `---` 结束。
   - 至少包含 `name:` 和 `description:`。
5. 汇总结果：
   - 每个 plugin 的 validate 结果。
   - marketplace validate 结果。
   - version mismatch 列表。
   - frontmatter 错误列表。
6. 退出码：
   - `0`：全部通过。
   - `1`：任一校验失败。

脚本用法：

```bash
plugins/ideal-lab-maintainer/scripts/validate.sh
```
