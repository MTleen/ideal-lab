Slide type: Content

Title: "P1 需求分析 → P3 大纲生成"

P1 需求分析 (requirement-analysis):
What it does: 解析需求文档或分析项目原始材料，提取功能需求、非功能需求和技术约束
Input: 用户提供的原始需求描述（如"帮我写一份后端技术方案"）
Output: P1-需求分析.md — 结构化的需求文档，明确文档类型、目标读者、核心内容范围
Two modes:
  - Mode A: 解析已有需求文档，直接提取场景、目标、输入输出、价值
  - Mode B: 分析项目源材料，识别知识缺口，确定需要补充什么信息
Key point: "这是最后一个'你说啥它写啥'的环节，后续所有工作都以此为锚点"

P3 大纲生成 (outline-generation):
What it does: 基于需求分析生成文档大纲（1-3 级标题），含字数估算
Input: P1-需求分析.md
Output: P2-大纲.md — 结构化大纲文档
Additional capability: 可选调用 ideal-deep-research 进行在线调研（竞品分析、技术趋势），或读取本地源码文档
Template: 提供标准文档模板（概述、现状分析、总体设计、功能设计、技术实现、实施计划、保障措施 7 大章节）
Key point: "大纲一旦确认，后续写作严格围绕它展开"
