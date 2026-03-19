# ideal-lab

Ideal Lab 最佳实践沉淀仓库。

## 目录结构

```
ideal-lab/
├── best-practices/
│   ├── dev-workflow/              # Claude Code 开发工作流
│   │   ├── agents/                # Agent 角色定义（analyst/pm/architect/dev/qa 等）
│   │   └── skills/               # 开发阶段 skill（requirement/plan/solution/exec 等）
│   ├── ideal-dify-generator/      # Dify 智能体/工作流生成
│   ├── meta-tools/                # 能力建设工具
│   │   └── mypush/               # Skill 推送工具
│   └── technical-proposal-workflow/ # 技术方案撰写工作流
│       ├── technical-proposal-merge/
│       └── technical-proposal-writing/
└── README.md
```

## 最佳实践清单

| 分类 | 说明 | 主要内容 |
|------|------|----------|
| [dev-workflow/](best-practices/dev-workflow/) | Claude Code 开发工作流 | 15 阶段流程、Agent 角色定义、Skills 规范 |
| [technical-proposal-workflow/](best-practices/technical-proposal-workflow/) | 技术方案撰写工作流 | P1 需求分析 → P6 文档合并，6 阶段带审核关卡 |
| [ideal-dify-generator/](best-practices/ideal-dify-generator/) | Dify 工作流生成 | 从需求到 DSL YAML，端到端生成与校验 |
| [meta-tools/mypush](best-practices/meta-tools/mypush/) | Skill 推送工具 | 将本地 skill 推送到 ideal-lab 仓库沉淀 |

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

## 版本

当前版本：1.0.0
