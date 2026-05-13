Slide type: Content

Title: "四大工作流套件"

Content — four workflow suites, each is "orchestrator + phase skills":

1. ideal-dev-workflow (v1.1.0, 14 Skills):
   一句话定位: 15 阶段开发流程，从需求到交付
   核心阶段: 需求 → 技术方案 → 编码计划 → 测试用例 → 开发执行 → 代码评审 → 测试执行 → 维基更新 → 成果提交
   适用场景: 功能开发、Bug 修复、重构任务
   安装: `claude plugin install ideal-dev-workflow@ideal-lab`

2. ideal-ppt-suite (v1.0.0, 9 Skills):
   一句话定位: PPT 全链路生成，17 种预设风格
   核心阶段: 调研 → 策略 → 大纲 → 提示词工程 → 生成 → AI 配图 → PPTX 导出
   适用场景: 方案汇报、产品路演、培训课件
   安装: `claude plugin install ideal-ppt-suite@ideal-lab`

3. ideal-document-workflow (v1.0.0, 8 Skills):
   一句话定位: 12 阶段结构化文档写作
   核心阶段: 需求分析 → 大纲 → 任务拆分 → 并行写作 → 智能配图 → 渲染输出
   适用场景: 技术文档、方案文档、知识沉淀
   安装: `claude plugin install ideal-document-workflow@ideal-lab`

4. ideal-knowledge-base (v1.0.0, 6 Skills):
   一句话定位: 知识库构建编排
   核心阶段: 材料分析 → 文档规划 → 并行生成 → 汇总评审
   适用场景: 项目知识沉淀、团队 Wiki 构建、技术积累
   安装: `claude plugin install ideal-knowledge-base@ideal-lab`

Common pattern: 手动模式每阶段确认，YOLO 模式自动运行直到完成或熔断
