Slide type: Content

Title: "一个 Plugin 里面有什么"

Content — the internal structure of a Plugin:

Every Plugin contains:
- plugin.json: 插件元数据（名称、版本、描述、包含的 Skill 列表）
- skills/ 目录: 包含该 Plugin 的所有 Skill
  - Each Skill has:
    - SKILL.md: 定义这个 Skill 做什么、怎么做（核心定义文件）
    - references/: 参考文档（写作规范、模板、技术规格等）
    - scripts/: 执行脚本（格式校验、文件转换、自动化工具等）

Example — ideal-document-workflow Plugin:
- plugin.json: 声明 8 个 Skill
- skills/ideal-document-workflow/SKILL.md (编排器)
- skills/requirement-analysis/SKILL.md (P1 需求分析)
- skills/outline-generation/SKILL.md (P3 大纲生成)
- skills/task-split/SKILL.md (P5 任务拆分)
- skills/document-writing/SKILL.md (P7 文档写作)
- skills/illustration/SKILL.md (P9 智能配图)
- skills/document-render/SKILL.md (P11 文档渲染)
- skills/writing-skills/SKILL.md (写作规范辅助)
