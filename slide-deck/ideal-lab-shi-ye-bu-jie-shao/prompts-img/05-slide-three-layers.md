Slide type: Content

Title: "Plugin → Skill → References 三层架构"

Content — the three-layer structure of ideal-lab:

Layer 1 — Plugin（插件）: 最大的能力单元。每个 Plugin 对应一个独立工作领域（如 ideal-dev-workflow 覆盖开发流程、ideal-ppt-suite 覆盖 PPT 生成）。Plugin 之间完全解耦，按需安装，不需要全量部署。

Layer 2 — Skill（技能）: Plugin 内的执行单元。每个 Skill 做一件事，通过 SKILL.md 定义"做什么"和"怎么做"。一个 Plugin 下的多个 Skill 按流程编排，形成完整工作流。

Layer 3 — References & Scripts: Skill 的支撑资源。references/ 存放参考文档（写作规范、模板、技术规格），scripts/ 存放执行脚本（格式校验、文件转换、自动化工具）。Skill 执行时读取这些资源，确保输出符合预设标准。

Key benefit: "透明可审计——任何一个 Skill 的行为都可以通过阅读 SKILL.md 完整了解，不需要逆向工程"
