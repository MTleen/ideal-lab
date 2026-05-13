# Ralph 合约：PPT Plugin HTML 化改造

## 任务描述
将 ideal-ppt-workflow 的幻灯片输出从纯 SVG 改为 HTML，提升排版质量、信息密度和可编辑性。

## 输入
- `ideal-ppt-executor/SKILL.md`（SVG 执行器 → 改为 HTML 执行器）
- `ideal-ppt-prompt/SKILL.md` + `references/base-prompt.md`（提示词 → HTML+CSS 导向）
- `ideal-ppt-export/SKILL.md`（导出 → HTML→PPTX/PDF）
- `ideal-ppt-outline/SKILL.md`（大纲 → STYLE_INSTRUCTIONS 适配 HTML+CSS）
- `ideal-ppt-workflow/SKILL.md`（编排器 → 适配 HTML 路径）
- harness 工程介绍素材（测试用）

## 输出
| 文件 | 改动 | 说明 |
|------|------|------|
| `ideal-ppt-executor/SKILL.md` | 重写 | SVG → HTML 执行器 |
| `ideal-ppt-executor/references/` | 新增 | HTML 模板、CSS 规范、混合渲染指南 |
| `ideal-ppt-prompt/SKILL.md` | 大改 | prompt 模板适配 HTML+CSS |
| `ideal-ppt-prompt/references/base-prompt.md` | 大改 | 基础提示词适配 HTML |
| `ideal-ppt-export/SKILL.md` | 大改 | HTML → PPTX/PDF 导出 |
| `ideal-ppt-outline/SKILL.md` | 小改 | STYLE_INSTRUCTIONS 适配 HTML+CSS |
| `ideal-ppt-workflow/SKILL.md` | 小改 | 编排器适配 HTML 路径 |

## 验收标准（9 条）
1. executor 重写为 HTML 执行器：生成独立 HTML，可嵌入 SVG 和 AI 图片
2. executor references 新增 HTML+CSS 规范文档
3. prompt 改为 HTML+CSS 导向，输出 HTML 片段
4. export 支持 HTML → PPTX/PDF 导出
5. outline 的 STYLE_INSTRUCTIONS 改为 HTML+CSS 属性
6. workflow 编排器适配 HTML 输出路径
7. 端到端测试：harness 工程介绍，5 页，P1-P13 完整流程
8. 测试产出：排版正确、高信息密度、风格一致
9. 测试产出具可导出为 PPTX 和 PDF

## 实施方式
直接改代码（SKILL.md + references）→ 端到端测试验证

## 约束
- 最大迭代：20 次
- 测试主题：harness 工程介绍
- 测试页数：5 页
