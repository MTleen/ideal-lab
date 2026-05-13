Slide type: Content

Title: "两大开发辅助"

Content — two development utilities:

1. ideal-ralph (v0.6.0):
   一句话定位: 苏格拉底式任务澄清 + 持久小步迭代验证循环
   核心理念: "先想清楚再动手"
   工作方式: 通过对话引导你明确任务的输入、输出、验收标准和实施方式，生成任务合约（contract），然后以持久迭代循环逐步执行，每一步验证是否满足验收标准
   特点: 不隶属于 ideal-dev-workflow，是独立编排器，可以调用任何 Skill 完成工作
   安装: `claude plugin install ideal-ralph@ideal-lab`
   调用: `/ideal-ralph:ideal-ralph`

2. ideal-lab-maintainer (v1.1.0):
   一句话定位: ideal-lab 仓库维护工具
   四个核心能力:
   - commit: 自动检测改动、生成 changeset、bump 版本
   - add-skill: 新增 Skill 模板
   - release: 发布流程
   - validate: 校验所有插件结构
   面向: ideal-lab 的开发者和管理员
   安装: `claude plugin install ideal-lab-maintainer@ideal-lab`
   调用: `/ideal-lab-maintainer:ideal-lab-maintainer`
