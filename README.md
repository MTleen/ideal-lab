# ideal-lab

Ideal Lab 最佳实践集合

## 目录结构

```
ideal-lab/
├── best-practices/
│   └── dev-workflow/        # Claude Code 开发工作流模板
│       ├── version.json     # 版本信息
│       ├── agents/          # Agent 定义
│       ├── skills/          # Skill 定义
│       └── configs/         # 配置模板
└── README.md
```

## 使用方式

通过 `ideal-cli` 工具初始化工作流：

```bash
npm install -g ideal-cli
ideal init
```

## dev-workflow 模板

Claude Code 中心化团队工作流模板，包含：

- **agents/** - 角色定义（PM、架构师、开发、测试等）
- **skills/** - 流程规范（需求、方案、计划、测试等）
- **configs/** - 配置模板

## 版本

当前版本：1.0.0
