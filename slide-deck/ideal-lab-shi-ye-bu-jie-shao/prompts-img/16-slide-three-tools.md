Slide type: Content

Title: "三大独立工具"

Content — three standalone tools:

1. ideal-deep-research (v1.0.0):
   一句话定位: 企业级深度调研
   4 种深度模式:
   - quick: 2-5 分钟快速扫描
   - standard: 5-10 分钟标准调研（默认）
   - deep: 10-20 分钟深度分析
   - ultradeep: 20-45 分钟全面审查
   调研管道: SCOPE → PLAN → RETRIEVE → TRIANGULATE → OUTLINE → SYNTHESIZE → CRITIQUE → REFINE → PACKAGE（8 个阶段）
   质量标准: 覆盖 10+ 信息源，每条结论至少 3 条引用，对信息源做可信度评分
   适用场景: 竞品分析、技术选型、趋势调研
   调用: `/ideal-deep-research:deep-research`

2. baoyu-image-gen (v1.0.0):
   一句话定位: 多 Provider AI 图片生成
   支持: OpenAI (DALL-E)、Google (Imagen)、DashScope (通义万相)、Replicate 等多个 Provider
   适用场景: 文档配图、PPT 插图、营销素材
   调用: `/baoyu-image-gen:baoyu-image-gen`

3. ideal-dify-generator (v1.0.0):
   一句话定位: Dify 工作流 DSL YAML 端到端生成与校验
   功能: 从需求描述生成 Dify DSL 规范的 YAML 配置，自动语法校验和逻辑检查
   适用场景: 快速搭建 Dify 工作流
   调用: `/ideal-dify-generator:ideal-dify-generator`
