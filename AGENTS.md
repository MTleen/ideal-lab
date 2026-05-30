# ideal-lab 项目规范

本仓库是 Claude Code Plugin 库，所有改动必须通过 Plugin 架构管理。

## 提交规则（强制）

**所有 commit 必须通过 `/ideal-lab-maintainer:maintainer commit` 完成。**

禁止使用裸 `git commit`。原因：
- 直接 commit 不会更新 plugin 版本号
- 不会生成 changeset
- 不会同步 plugin.json 和 package.json 的版本
- 导致用户已安装的 plugin 缓存不会刷新

### 正确流程

```
修改 skill/plugin 文件
    ↓
/ideal-lab-maintainer:maintainer commit
    ↓
（自动：检测改动 → 生成 changeset → bump 版本 → 同步 plugin.json → validate → git commit）
```

### 新增 skill

```
/ideal-lab-maintainer:maintainer add-skill
```

### 新增 plugin

```
/ideal-lab-maintainer:maintainer add-plugin
```

### 发布

```
/ideal-lab-maintainer:maintainer release
```

### 其他规则

- 修改任何 plugin 内容后，必须 `claude plugin validate` 确认通过
- 新增 skill 必须放在对应 plugin 的 `skills/` 目录下
- SKILL.md 必须有合法的 YAML frontmatter（name + description）
- 不要手动修改 `plugin.json` 的 version 字段，由 changeset 自动管理
- `node_modules/`、`__pycache__/`、`.DS_Store` 不要提交

## Skill 迭代硬规则

当任务是在优化某个 skill 的输出质量时，必须采用 skill-first 闭环：

1. 先对比当前输出与目标样例，明确差异。
2. 判断差异背后的系统性 skill 缺陷。
3. **先修改对应 `SKILL.md`、reference、脚本或分析契约。**
4. 再按更新后的 skill 重新生成产物。
5. 渲染/验证新产物，并写明本轮 judgment。
6. 若未达标，回到第 1 步。

禁止把最终产物（例如 SVG、PPT、文档）作为主要手工修补对象来”调到像”。只有当 judgment 明确说明某问题是一次性非系统问题时，才允许做最小直接修补，并必须在诊断文件中记录原因。

对于图片转 SVG / PPT 复刻类任务，还必须保持可编辑分层：

- 文字必须作为可编辑文本重建，不能截图替代。
- 方框、圆、线、箭头、分割线等框图元素必须用原生 SVG/PPT 形状重建。
- 复杂照片、复杂图标、难以原生复刻的装饰性位图，才允许从源图裁片嵌入。
- 禁止整页嵌入源图来冒充复刻通过；除非用户明确要求”只要视觉截图版”。
- 所有裁片都必须在 judgment/accept 的 `downgrades[]` 中逐项说明。
