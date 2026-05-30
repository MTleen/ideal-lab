# ideal-lab Agent 行为规则

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

## 其他规则

- 修改任何 plugin 内容后，必须 `claude plugin validate` 确认通过
- 新增 skill 必须放在对应 plugin 的 `skills/` 目录下
- SKILL.md 必须有合法的 YAML frontmatter（name + description）
- 不要手动修改 `plugin.json` 的 version 字段，由 changeset 自动管理
- `node_modules/`、`__pycache__/`、`.DS_Store` 不要提交
