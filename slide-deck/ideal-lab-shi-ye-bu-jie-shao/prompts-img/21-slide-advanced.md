Slide type: Content

Title: "进阶用法与常见问题"

Advanced usage 1 — YOLO 模式:
启动时附加指令即可全自动推进：
`/ideal-document-workflow:ideal-document-workflow YOLO 模式，帮我写一份...`
自动运行直到完成或触发熔断（发现 P0 级问题才停下来）

Advanced usage 2 — 多插件组合:
先调研再输出是典型组合：
  Step 1: `/ideal-deep-research:deep-research 调研 2025 年主流 LLM 应用开发框架对比`
  Step 2: `/ideal-ppt-suite:ideal-ppt-workflow 基于上面的调研结果，生成一份汇报 PPT`

FAQ:
Q: 安装失败怎么办？
A: 检查 Claude Code 版本是否支持 Plugin，确认网络可访问 GitHub

Q: 如何更新已安装的插件？
A: 重新运行安装命令即可覆盖更新

Q: 可以只安装单个 Skill 吗？
A: 插件是安装的最小单位，但安装后可以只使用其中某个 Skill

Q: 输出格式支持哪些？
A: 文档默认 Markdown，PPT 输出 PPTX，调研输出 Markdown，可按需指定格式

Q: 数据安全如何保障？
A: 所有任务本地执行，代码和文档不上传。插件只含 Markdown 定义和脚本，无数据收集逻辑
