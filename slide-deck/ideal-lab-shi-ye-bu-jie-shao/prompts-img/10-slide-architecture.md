Slide type: Content

Title: "架构全貌：8 个 Skill 如何协作"

Content — the 8 skills and their data flow:

1 orchestrator (编排器):
- ideal-document-workflow: 主调度器，读取流程状态文件，调用对应阶段 Skill，推进状态。只调度不执行。

6 pipeline skills (阶段 Skill), each with input → output:
- requirement-analysis (P1): 输入 = 原始需求描述或项目材料 → 输出 = P1-需求分析.md
- outline-generation (P3): 输入 = P1-需求分析.md → 输出 = P2-大纲.md
- task-split (P5): 输入 = P2-大纲.md → 输出 = P3-任务拆分.md
- document-writing (P7): 输入 = P3-任务拆分.md + P1 + P2 → 输出 = sections/*.md (各章节)
- illustration (P9): 输入 = sections/*.md → 输出 = 更新后的 sections/*.md + images/
- document-render (P11): 输入 = sections/*.md + images/ → 输出 = 最终交付物 (docx/pptx/md)

1 auxiliary skill:
- writing-skills: 写作规范辅助，提供统一写作风格标准

Data flow chain: 需求描述 → P1需求分析 → P3大纲 → P5任务拆分 → P7并行写作 → P9智能配图 → P11渲染输出 → 交付物

Review phases (interleaved): P2/P4/P6/P8/P10 — 每个产物阶段后有评审阶段，确保质量

Bottom note: "每个下游 Skill 消费上游 Skill 的产出物，形成严格的数据流链条"
