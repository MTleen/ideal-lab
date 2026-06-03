# ideal-ppt-suite

## 2.1.0

### Minor Changes

- **refactor(ideal-ppt-strategist)**: 八大确认从"一次性 8 问"改为分阶段路由
  - 阶段 1：a 画幅 + b 页数 + c 受众（一次性）
  - 阶段 2：d 美业方式（**单独询问，作为路由点**）
  - 阶段 3：e 配色 + f 图标 + g 字体（一次性）
  - 阶段 4：h 图片使用（**仅 d=html-mode 时触发，d=image-mode 时跳过**）
- **feat**: 引入 image-mode / html-mode 二选一作为新的 d 项路由开关
  - `image-mode`：每页即一张 AI 大图，无需询问图片形式
  - `html-mode`：每页 HTML 排版，h 正常问（None/User-provided/AI-generated/Placeholders）
- **docs**: 更新 SKILL.md 主入口 + eight-confirmations.md 总则 + strategy-template.md 第 VIII 节（按渲染模式分 8A/8B）

## 2.0.0
- **Breaking**: 归档 `ideal-ppt-generator`（单体版），统一使用 `ideal-ppt-workflow`（14 阶段模块化流水线）
- 删除 `skills/ideal-ppt-generator/` 目录（SKILL.md + 17 references + 2 scripts）

## 1.2.0

### Minor Changes

- Improve ideal PPT image generation skills

## 1.0.0

- Initial release migrated from best-practices/content-tools
