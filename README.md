# ideal-lab

**Claude Code 最佳实践插件库** — 覆盖开发流程、PPT 生成、文档写作、知识库构建、深度调研的全链路 Skill 集合

[![License](https://img.shields.io/badge/license-Private-red?style=flat-square)](https://github.com/MTleen/ideal-lab)
[![Plugins](https://img.shields.io/badge/plugins-9-blue?style=flat-square)](./plugins)
[![Skills](https://img.shields.io/badge/skills-42-green?style=flat-square)](./plugins)
[![Version](https://img.shields.io/badge/changeset-managed-orange?style=flat-square)](./.changeset)

[插件清单](#插件清单) · [快速开始](#快速开始) · [使用方式](#使用方式) · [开发](#开发) · [迁移](#迁移说明)

---

## 概览

ideal-lab 通过 Claude Code 官方 Plugin Marketplace 分发，每个插件自包含（skills + references + scripts），支持按需安装单个插件或完整工作流。

目前包含 **9 个插件**、**42 个 Skill**，覆盖从需求到交付的完整链路。

## 插件清单

### 工作流套件

| 插件 | 版本 | 说明 | Skills |
|------|------|------|--------|
| [ideal-dev-workflow](./plugins/ideal-dev-workflow) | 1.1.0 | 15 阶段开发流程：需求 → 方案 → 计划 → 编码 → 测试 → 评审 → 交付 | 14 |
| [ideal-ppt-suite](./plugins/ideal-ppt-suite) | 1.0.0 | PPT 全链路生成：调研 → 策略 → 大纲 → 提示词 → 生成 → 配图 → 导出 | 9 |
| [ideal-document-workflow](./plugins/ideal-document-workflow) | 1.0.0 | 结构化文档写作：需求分析 → 大纲 → 写作 → 配图 → 渲染 | 8 |
| [ideal-knowledge-base](./plugins/ideal-knowledge-base) | 1.0.0 | 知识库构建编排：材料分析 → 文档规划 → 并行生成 → 汇总评审 | 6 |

### 独立工具

| 插件 | 版本 | 说明 |
|------|------|------|
| [baoyu-image-gen](./plugins/baoyu-image-gen) | 1.0.0 | 多 Provider AI 图片生成（OpenAI / Google / DashScope） |
| [ideal-deep-research](./plugins/ideal-deep-research) | 1.0.0 | 企业级深度调研：多源综合、引用追踪、可信度评分 |
| [ideal-dify-generator](./plugins/ideal-dify-generator) | 1.0.0 | Dify 工作流 DSL YAML 端到端生成与校验 |

### 开发工具

| 插件 | 版本 | 说明 |
|------|------|------|
| [ideal-ralph](./plugins/ideal-ralph) | 0.5.0 | Socratic 任务澄清 + 持久化小步迭代验证循环 |
| [ideal-lab-maintainer](./plugins/ideal-lab-maintainer) | 1.1.0 | 仓库维护工具（commit / add-skill / release / validate） |

## 快速开始

### 1. 添加 Marketplace

```bash
claude plugin marketplace add https://github.com/MTleen/ideal-lab
```

### 2. 安装插件

```bash
# 安装开发流程工作流（14 个 Skill）
claude plugin install ideal-dev-workflow@ideal-lab

# 安装 PPT 全链路（9 个 Skill）
claude plugin install ideal-ppt-suite@ideal-lab

# 安装文档写作工作流（8 个 Skill）
claude plugin install ideal-document-workflow@ideal-lab

# 安装单个工具
claude plugin install ideal-deep-research@ideal-lab
```

### 3. 调用 Skill

安装后 Skill 自动加载，通过斜杠命令调用：

```
/ideal-dev-workflow:ideal-requirement    # P1 需求收集
/ideal-ppt-suite:ideal-ppt-generator    # PPT 生成
/ideal-deep-research:deep-research       # 深度调研
```

> [!TIP]
> 每个工作流插件都有一个编排器 Skill（如 `ideal-flow-control`、`ideal-ppt-workflow`），调用编排器即可自动走完整个流程，无需逐阶段手动触发。

## 使用方式

### 开发流程（ideal-dev-workflow）

15 个阶段、严格有序的阶段流水线，支持 YOLO 模式（自动推进）：

```
P1 需求 → P3 技术方案 → P5 编码计划 → P7 测试用例
→ P9 开发执行 → P10 代码评审 → P11 测试执行
→ P13 维基更新 → P15 成果提交
```

核心 Skill：`ideal-init`（项目初始化）、`ideal-flow-control`（阶段流转控制）、`ideal-yolo`（多视角自动评审）

### PPT 生成（ideal-ppt-suite）

13 阶段全链路，支持 17 种预设风格，输出可编辑 PPTX：

```
P1 调研 → P3 策略（八确认） → P5 大纲（金字塔原理） → P7 提示词工程
→ P9 AI 配图 → P11 HTML 执行 → P13 PPTX 导出
```

### 文档写作（ideal-document-workflow）

12 阶段结构化写作，支持 What-Why-How 模式，自动配图：

```
P1 需求分析 → P3 大纲 → P5 任务拆分 → P7 并行写作
→ P9 智能配图 → P11 渲染输出
```

### 深度调研（ideal-deep-research）

4 种深度模式（quick / standard / deep / ultradeep），8 个阶段管道，要求 10+ 信息源、每条结论 3+ 引用：

```
SCOPE → PLAN → RETRIEVE → TRIANGULATE → OUTLINE
→ SYNTHESIZE → CRITIQUE → REFINE → PACKAGE
```

## 开发

### 目录结构

```
ideal-lab/
├── .claude-plugin/
│   └── marketplace.json          # Plugin 市场索引
├── .changeset/                   # Changesets 版本管理
├── plugins/
│   ├── ideal-dev-workflow/       # 每个 plugin 自包含
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   └── ideal-requirement/
│   │   │       └── SKILL.md
│   │   ├── package.json
│   │   └── CHANGELOG.md
│   ├── ideal-ppt-suite/
│   ├── ideal-document-workflow/
│   ├── ideal-knowledge-base/
│   └── ...
└── .github/workflows/            # CI: validate + release
```

### 日常开发

```bash
# 修改现有 Skill
vim plugins/ideal-dev-workflow/skills/ideal-requirement/SKILL.md

# 提交（自动检测改动、生成 changeset、bump 版本）
/ideal-lab-maintainer:maintainer commit

# 新增 Skill
/ideal-lab-maintainer:maintainer add-skill

# 发布
/ideal-lab-maintainer:maintainer release

# 校验所有插件
/ideal-lab-maintainer:maintainer validate
```

### 版本策略

| bump | 标准 |
|------|------|
| patch | 修 typo、补充说明、修脚本 bug |
| minor | 新增 Skill、可选配置、新 Provider |
| major | Skill 改名/删除、阶段编号变化、Schema 不兼容 |

## 迁移说明

从旧版 `best-practices/` 结构迁移的用户：

| 旧路径 | 新 Plugin |
|--------|-----------|
| `best-practices/dev-workflow/` | ideal-dev-workflow |
| `best-practices/content-tools/ideal-ppt-*` | ideal-ppt-suite |
| `best-practices/content-tools/baoyu-image-gen` | baoyu-image-gen |
| `best-practices/ideal-document-workflow/` | ideal-document-workflow |
| `best-practices/build-knowledge-base-workflow/` | ideal-knowledge-base |
| `best-practices/utilities/deep-research` | ideal-deep-research |
| `best-practices/ideal-dify-generator` | ideal-dify-generator |

> [!NOTE]
> 请删除旧的 `~/.claude/skills/` 下手动复制的 Skill，改用 Plugin 安装以获得自动更新。
