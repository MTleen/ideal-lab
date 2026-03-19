---
name: mypush
description: |
  将本地 Claude Code skill 推送到 GitHub ideal-lab 私有仓库进行最佳实践沉淀。
  触发场景：(1) 用户调用 "/mypush" (2) 用户要求"推送skill"、"上传最佳实践"
  核心功能：分析 skill 内容 → 推断分类目录 → 识别依赖 skill → 确认后推送到 GitHub。
---

# MyPush — Best Practice Push Tool

将本地 skill 推送到 `MTleen/ideal-lab/best-practices/` 私有仓库。

## 核心原则

1. **用户指定** — 用户通过对话指定要推送的 skill 名称，不批量操作
2. **内容推断** — 通过 skill 的 `SKILL.md` 内容推断分类，不依赖前缀命名
3. **依赖打包** — 自动识别协作依赖，将相关 skill 一并推送
4. **确认制** — 推送前必须用户确认，显示文件结构和目标路径

## 分类推断规则

通过分析 `SKILL.md` 的 `description` 和内容关键词，自动映射到分类目录：

| 关键词 | 分类目录 |
|--------|---------|
| 工作流、编排、Agent、开发流程 | `dev-workflow/` |
| 技术方案、投标、技术标书、写作 | `technical-proposal-workflow/` |
| 图片生成、配图、图像、illustrator | `content-tools/` |
| 论文、NSFC、文献、研究基金 | `academic-writing/` |
| Dify、工作流生成、DSL | `ideal-dify-generator/` |
| 审批流、研发云、SOP、规章、检查 | `business-workflow/` |
| skill 创建、meta、能力建设 | `meta-tools/` |
| PDF、Word、Excel、文档转换 | `doc-tools/` |

未匹配的 skill 归入 `utilities/`。

## 依赖识别规则

扫描 `SKILL.md` 内容，识别对其他 skill 的引用，纳入打包范围：

- 引用格式：`{skill名}/`（如 `baoyu-image-gen/`）
- 引用格式：`technical-proposal-*` 等通配符模式
- 典型依赖关系：
  - `technical-proposal-illustration` → `baoyu-image-gen`
  - `technical-proposal-merge` → `markdown_to_word.sh` 脚本
  - `ideal-yolo` → 多个 `ideal-*` skill
  - `skill-creator` → 依赖参考的其他 skill

## 执行流程

### Step 1: 获取 skill 名称

通过对话确认用户要推送的 skill：

```
请告诉我你要推送的 skill 名称？
可以直接输入名称（如 baoyu-image-gen）
或描述功能（如"图片生成相关的skill"）
```

### Step 2: 定位 skill

在 `~/.claude/skills/` 下查找：

```bash
SKILL_PATH="$HOME/.claude/skills/{skill_name}"
if [ ! -d "$SKILL_PATH" ]; then
    # 尝试 .skill 后缀
    SKILL_PATH="$HOME/.claude/skills/{skill_name}.skill"
fi
```

未找到时提示用户。

### Step 3: 分析内容

读取 `SKILL.md`，执行以下分析：

```python
# 1. 读取 description
description = re.search(r'description:\s*\|\s*(.*?)(?=---)', content, re.DOTALL)

# 2. 关键词匹配分类
category = infer_category(description)

# 3. 扫描依赖 skill
dependencies = scan_dependencies(content)

# 4. 文件统计
file_count, line_count = count_files(skill_path)
```

### Step 4: 构建打包清单

```
推送清单：
- 主 skill：{skill_name}
  路径：best-practices/{category}/{skill_name}/
  文件：N 个，约 L 行

- 依赖 skill：
  - {dep_name}（{category}）
  - ...

共推送 M 个 skill，N 个文件
```

### Step 5: AskUserQuestion 确认

```json
{
  "header": "推送确认",
  "question": "【确认推送以下 skill 到 GitHub】\n\n目标仓库：MTleen/ideal-lab\n路径：best-practices/{category}/{skill_name}/\n\n文件列表：\n- SKILL.md\n- references/\n- scripts/\n- ...\n\n依赖打包：{dep1}, {dep2}\n\n是否确认推送？",
  "options": [
    {"label": "确认推送", "description": "推送到 GitHub ideal-lab 仓库"},
    {"label": "取消", "description": "取消本次推送"}
  ],
  "multiSelect": false
}
```

### Step 6: 执行推送

```bash
# 克隆仓库
gh repo clone MTleen/ideal-lab /tmp/mypush_repo

# 复制 skill 到目标路径
cp -r "$SKILL_PATH" "/tmp/mypush_repo/best-practices/{category}/{skill_name}/"

# 复制依赖
for dep in dependencies; do
    cp -r "$HOME/.claude/skills/$dep" "/tmp/mypush_repo/best-practices/{dep_category}/"
done

# Git 操作
cd /tmp/mypush_repo
git add best-practices/
git commit -m "feat: add {skill_name}"

# 检查是否已有同名 skill（更新 vs 新增）
if git diff --staged --quiet; then
    echo "无变更，跳过"
else
    git push origin main
fi
```

### Step 7: 输出报告

```
mypush 完成

仓库：MTleen/ideal-lab
推送：
- best-practices/{category}/{skill_name}/（主）
- best-practices/{dep_category}/{dep_name}/（依赖）

commit: {hash}
```

## 依赖关系参考表

| 主 skill | 依赖 skill |
|---------|-----------|
| technical-proposal-workflow | analysis, outline, task-split, writing, illustration, merge, style |
| technical-proposal-illustration | baoyu-image-gen |
| technical-proposal-merge | markdown_to_word.sh 脚本 |
| ideal-yolo | requirement, dev-solution, dev-plan, dev-exec, code-review, test-case, test-exec, wiki, debugging |
| ideal-ccworkflow-executor | ideal-requirement, ideal-dev-solution, ideal-dev-plan, ideal-flow-control |
| skill-creator | （依赖用户提供参考 skill） |

## 常见错误处理

| 错误 | 处理方式 |
|------|---------|
| skill 不存在 | 提示用户检查名称，提供相似名称建议 |
| gh 未认证 | 提示运行 `gh auth login` |
| 仓库无写入权限 | 提示联系仓库管理员 |
| 无变更（已推送过） | 跳过推送，提示用户 |
| Git 冲突 | 提示用户手动解决或强制覆盖 |
