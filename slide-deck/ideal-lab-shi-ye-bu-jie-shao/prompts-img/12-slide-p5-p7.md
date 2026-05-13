Slide type: Content

Title: "P5 任务拆分 → P7 文档写作"

P5 任务拆分 (task-split):
What it does: 将大纲拆分为独立的、可并行执行的写作任务，每个任务约 5000 字
Input: P2-大纲.md + P1-需求分析.md
Output: P3-任务拆分.md — 包含多个任务卡片
Splitting rules:
  - 优先按一级标题拆分（每个一级标题 = 一个任务）
  - 若单节超过 10000 字，按二级标题拆分
  - 每个任务控制在 3000-6000 字
Each task card includes: 目标文件路径、预估字数、章节范围、原始需求上下文、写作要点

P7 文档写作 (document-writing):
What it does: 按任务卡并行写作各章节，使用 What-Why-How 写作模式确保内容完整
Input: P3-任务拆分.md + P1-需求分析.md + P2-大纲.md
Output: sections/*.md — 各章节 Markdown 文件
Writing pattern — What-Why-How:
  - What: 这个功能/技术是什么
  - Why: 为什么选择它（决策依据）
  - How: 怎么实现的（落地路径）
Additional capability: 每个任务可按需调用 ideal-deep-research 做外部调研，或读取源码提取信息
Key point: "多个 sub-agent 并行写作，统一写作规范确保风格一致"
