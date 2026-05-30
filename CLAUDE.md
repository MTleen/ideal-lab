# ideal-lab 项目规范

本仓库是 Claude Code Plugin 库，所有改动必须通过 Plugin 架构管理。

详细行为规则见 [AGENTS.md](./AGENTS.md)。

## image-to-svg 复原度验证流程

用 `mcp__zai-mcp-server__ui_diff_check` 对比源图与 SVG 渲染结果，作为 Step 2.5 的独立第三方验证。

```
1. 渲染 SVG → PNG（Playwright MCP screenshot）
2. resize 到与源图同尺寸（Pillow Image.resize）
3. mcp__zai-mcp-server__ui_diff_check(expected=源图, actual=渲染图)
4. 记录差异到 diagnostics/<page>.zai-judgment.md
5. 根据 HIGH 级问题返回 Step 1 修复
```

验证标准：视觉匹配度 ≥ 90% 且无 HIGH 级图标语义错误。

darwin 闭环：ZAI 发现问题 → 修 SKILL.md（加约束） → 用新 SKILL 重新生成 → ZAI 复查。不直接修 SVG。

本项目使用 `mcp__zai-mcp-server__ui_diff_check` 作为 image-to-svg Step 2.5.4 的独立第三方视觉验证工具。
