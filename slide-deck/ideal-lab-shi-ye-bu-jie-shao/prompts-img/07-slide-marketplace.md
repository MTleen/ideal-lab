Slide type: Content

Title: "Marketplace 三步安装"

Content — three steps to get started:

Step 1 — 添加 Marketplace 源:
Command: `claude plugin marketplace add https://github.com/MTleen/ideal-lab`
Result: 告诉 Claude Code 从哪里获取插件清单和安装包，一次添加永久有效

Step 2 — 按需安装插件:
Examples:
- `claude plugin install ideal-document-workflow@ideal-lab` → 安装文档写作工作流（8 个 Skill）
- `claude plugin install ideal-deep-research@ideal-lab` → 安装深度调研工具
- `claude plugin install ideal-dev-workflow@ideal-lab` → 安装开发流程工作流（14 个 Skill）
- `claude plugin install ideal-ppt-suite@ideal-lab` → 安装 PPT 生成套件（9 个 Skill）

Step 3 — 通过斜杠命令调用:
- `/ideal-document-workflow:ideal-document-workflow` → 启动文档写作全流程
- `/ideal-deep-research:deep-research` → 启动深度调研
- `/ideal-ppt-suite:ideal-ppt-workflow` → 启动 PPT 生成全流程

Key point: "用哪个装哪个，不需要全量安装"
