Slide type: Content

Title: "版本管理与质量保障"

Content — how versioning and quality control works:

Version strategy using Changeset + GitHub Actions:

| Version type | Standard | Example |
|-------------|----------|---------|
| patch | 修 typo、补充说明、修脚本 bug | 1.0.0 → 1.0.1 |
| minor | 新增 Skill、可选配置、新 Provider | 1.0.0 → 1.1.0 |
| major | Skill 改名/删除、阶段编号变化、Schema 不兼容 | 1.0.0 → 2.0.0 |

Automated quality assurance:
- CI 流水线在合并前自动校验所有插件的结构完整性和配置合法性
- 每次提交改动时，维护工具自动检测变更范围、生成 Changeset、Bump 版本号
- 确保发布的内容不会因为格式问题导致安装失败

What this means for users:
- 版本可追溯：任何一个 Skill 的任何一次变更都有记录，可以回溯到具体改动内容
- 更新可控：minor 版本保证向后兼容，不会因为升级丢失已有配置；major 版本提前说明不兼容变更，给足迁移时间
