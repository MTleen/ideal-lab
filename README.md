# ideal-lab

Ideal Lab 最佳实践沉淀仓库。

## 目录结构

```
ideal-lab/
├── best-practices/
│   ├── dev-workflow/              # Claude Code 开发工作流
│   ├── technical-proposal-workflow/ # 技术方案撰写工作流
│   ├── ideal-dify-generator/      # Dify 智能体/工作流生成
│   ├── content-tools/              # 内容生成工具（配图等）
│   ├── academic-writing/           # 学术写作（NSFC 等）
│   ├── business-workflow/          # 业务工作流（研发云 SOP 等）
│   ├── meta-tools/                # 能力建设工具（skill 管理等）
│   ├── doc-tools/                 # 文档工具（PDF/Word/Excel）
│   └── utilities/                  # 未分类工具
└── README.md
```

## 最佳实践清单

| 分类 | 说明 | 主要内容 |
|------|------|----------|
| [dev-workflow/](best-practices/dev-workflow/) | Claude Code 开发工作流 | 15 阶段流程、Agent 角色定义、Skills 规范 |
| [technical-proposal-workflow/](best-practices/technical-proposal-workflow/) | 技术方案撰写工作流 | P1 需求分析 → P6 文档合并，6 阶段带审核关卡 |
| [ideal-dify-generator/](best-practices/ideal-dify-generator/) | Dify 工作流生成 | 从需求到 DSL YAML，端到端生成与校验 |
| [meta-tools/mypush](best-practices/meta-tools/mypush/) | Skill 推送工具 | 将本地 skill 推送到 ideal-lab 仓库沉淀 |

## Commit Message 规范

本仓库使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

<body>
```

**Type 前缀：**

| Type | 使用场景 |
|------|---------|
| `feat` | 新增最佳实践 |
| `fix` | 修复已有最佳实践中的问题 |
| `docs` | 文档更新（README、注释） |
| `refactor` | 重构（不改变功能） |
| `chore` | 维护性变更（依赖、配置） |

**Scope 范围：**

| Scope | 对应分类 |
|-------|---------|
| `dev-workflow` | dev-workflow/ |
| `technical-proposal` | technical-proposal-workflow/ |
| `dify` | ideal-dify-generator/ |
| `content-tools` | content-tools/ |
| `academic` | academic-writing/ |
| `business-workflow` | business-workflow/ |
| `meta-tools` | meta-tools/ |
| `doc-tools` | doc-tools/ |
| `repo` | 仓库级别（README、配置等） |

**示例：**

```bash
# 新增技术方案 skill
git commit -m "feat(technical-proposal): add technical-proposal-merge

# 修复公式渲染问题
git commit -m "fix(technical-proposal): 修复 markdown 转 word 公式渲染失败

# 更新 README
git commit -m "docs(repo): 更新目录结构，补充 technical-proposal-workflow"
```

## 使用方式

### 推送新最佳实践

使用 `mypush` skill 将本地 skill 推送到仓库：

```bash
# 在 Claude Code 中调用
/mypush
```

### 克隆使用

```bash
git clone https://github.com/MTleen/ideal-lab.git
```

### ideal-cli 初始化（dev-workflow）

```bash
npm install -g ideal-cli
ideal init
```

## 版本

当前版本：1.0.0
