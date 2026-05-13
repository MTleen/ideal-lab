Slide type: Content

Title: "前置条件与安装"

Prerequisites:
- Claude Code 已安装：终端中运行 `claude --version` 可以输出版本号
- Anthropic API Key 已配置：Claude Code 首次启动时会引导配置

Step 1 — 添加 Marketplace:
Command: `claude plugin marketplace add https://github.com/MTleen/ideal-lab`
Expected: ✓ Marketplace "ideal-lab" added successfully, 9 Plugins available

Step 2 — 安装推荐插件（按需选择）:
- 文档写作: `claude plugin install ideal-document-workflow@ideal-lab`（8 Skills，上手门槛最低）
- 深度调研: `claude plugin install ideal-deep-research@ideal-lab`
- PPT 生成: `claude plugin install ideal-ppt-suite@ideal-lab`（9 Skills）
- 开发流程: `claude plugin install ideal-dev-workflow@ideal-lab`（14 Skills）

Step 3 — 验证安装:
安装完成后 Skill 自动加载，无需额外配置
直接在对话中输入 `/插件名` 即可看到可用 Skill 列表
