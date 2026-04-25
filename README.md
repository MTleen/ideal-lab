# ideal-lab

Claude Code 最佳实践插件库。通过 Claude Code 官方 Plugin Marketplace 分发，支持按需安装单个插件或完整工作流。

## 插件清单

| Plugin | 说明 | 类型 |
|--------|------|------|
| ideal-dev-workflow | 15 阶段开发流程工作流：需求→方案→计划→编码→测试→评审→交付 | bundle |
| ideal-ppt-suite | PPT 全链路生成：调研→策略→大纲→提示词→生成→配图→导出 | bundle |
| ideal-document-workflow | 结构化文档写作：需求分析→大纲→写作→配图→渲染 | bundle |
| ideal-knowledge-base | 知识库构建编排：材料分析→文档规划→并行生成→汇总评审 | bundle |
| baoyu-image-gen | 多 Provider AI 图片生成 | 独立 |
| ideal-deep-research | 企业级深度调研：多源综合、引用追踪、可信度评分 | 独立 |
| ideal-dify-generator | Dify 工作流 DSL YAML 端到端生成与校验 | 独立 |
| ideal-lab-maintainer | 仓库维护工具（commit/add-skill/release/validate） | 工具 |

## 安装方式

### 1. 添加 Marketplace

```bash
claude plugin marketplace add https://github.com/MTleen/ideal-lab
```

### 2. 安装插件

```bash
# 安装整个开发流程工作流
claude plugin install ideal-dev-workflow@ideal-lab

# 安装 PPT 全链路
claude plugin install ideal-ppt-suite@ideal-lab

# 安装单个工具
claude plugin install ideal-deep-research@ideal-lab
```

### 3. 在 Claude Code 中使用

安装后，插件的 skill 会自动加载。使用时通过斜杠命令调用：

```
/ideal-dev-workflow:ideal-requirement
/ideal-ppt-suite:ideal-ppt-generator
/ideal-deep-research:deep-research
```

## 开发

### 目录结构

```
ideal-lab/
├── .claude-plugin/
│   └── marketplace.json       # Plugin 市场索引
├── .changeset/                # Changesets 版本管理
├── plugins/
│   ├── ideal-dev-workflow/    # 每个 plugin 自包含
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   ├── package.json       # Changesets 版本追踪
│   │   └── CHANGELOG.md
│   ├── ideal-ppt-suite/
│   ├── ...
│   └── ideal-lab-maintainer/  # 维护工具
└── .github/workflows/         # CI: validate + release
```

### 日常开发流程

```bash
# 修改现有 skill
vim plugins/ideal-dev-workflow/skills/ideal-requirement/SKILL.md

# 提交（自动检测改动、生成 changeset、bump 版本）
/ideal-lab-maintainer:maintainer commit

# 新增 skill
/ideal-lab-maintainer:maintainer add-skill

# 发布
/ideal-lab-maintainer:maintainer release
```

### 版本策略

| bump | 标准 |
|------|------|
| patch | 修 typo、补充说明、修脚本 bug |
| minor | 新增 skill、可选配置、新 provider |
| major | skill 改名/删除、阶段编号变化、schema 不兼容 |

## 迁移说明

从旧版 `best-practices/` 结构迁移的用户：

| 旧路径 | 新 Plugin |
|--------|-----------|
| best-practices/dev-workflow/ | ideal-dev-workflow |
| best-practices/content-tools/ideal-ppt-* | ideal-ppt-suite |
| best-practices/content-tools/baoyu-image-gen | baoyu-image-gen |
| best-practices/ideal-document-workflow/ | ideal-document-workflow |
| best-practices/build-knowledge-base-workflow/ | ideal-knowledge-base |
| best-practices/utilities/deep-research | ideal-deep-research |
| best-practices/ideal-dify-generator | ideal-dify-generator |

请删除旧的 `~/.claude/skills/` 下手动复制的 skill，改用 plugin 安装。

## License

Private
