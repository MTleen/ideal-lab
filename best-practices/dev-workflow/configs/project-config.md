---
projectName: {{projectName}}
gitBranch: {{gitBranch}}
techStack: {{techStack}}
workflow:
  templateRepo: MTleen/ideal-lab
  templateBranch: main
  lastUpdated: {{lastUpdated}}
initializedAt: {{initializedAt}}
---

# 项目配置

此文件存储 ideal-cli 工具的项目配置。

## 配置说明

| 字段 | 说明 |
|------|------|
| projectName | 项目名称 |
| gitBranch | 主要开发分支 |
| techStack | 技术栈 |
| workflow.templateRepo | 模板仓库 |
| workflow.templateBranch | 模板分支 |
| workflow.lastUpdated | 最后更新时间 |
| initializedAt | 初始化时间 |

## 修改配置

使用 `ideal config` 命令修改配置：

```bash
ideal config list           # 查看所有配置
ideal config get <key>      # 获取指定配置
ideal config set <key> <value>  # 设置配置值
```
