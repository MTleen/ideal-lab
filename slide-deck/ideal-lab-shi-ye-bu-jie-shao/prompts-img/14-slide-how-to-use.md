Slide type: Content

Title: "怎么用：整体跑 or 拆开用"

Two execution modes:

Mode 1 — 手动模式 (yolo_mode: false):
- 每个产物阶段完成后停下来等确认
- 每个评审阶段展示评审摘要后等确认
- 适合：首次使用、重要文档、对质量要求极高的场景
- 人工参与：6-12 次确认

Mode 2 — YOLO 模式 (yolo_mode: true):
- 全自动推进，直到流程完成或触发熔断
- 评审团队的修改工作仍然正常执行，只是不需要逐个确认
- 适合：对流程已熟悉、时间紧迫、对 AI 输出有信心的场景
- 人工参与：0-1 次（仅熔断时介入）

Each Skill can be used independently:
- 只想分析需求？→ 直接调用 `/ideal-document-workflow:requirement-analysis`
- 只想生成大纲？→ 直接调用 `/ideal-document-workflow:outline-generation`
- 只想做配图？→ 直接调用 `/ideal-document-workflow:illustration`
- 只想格式转换？→ 直接调用 `/ideal-document-workflow:document-render`

Example — standalone usage:
"帮我分析这个需求文档的结构" → 只用 P1，输出需求分析
"帮我给这份 Markdown 配图" → 只用 P9，输出带图的文档
