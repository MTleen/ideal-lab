# Absorb Dimensions — 跨 Skill 吸收维度

用于 skill-builder absorb 的 Step 3a 差距分析。每个维度包含定义、测量方法、与 skill-builder 7 维度的映射。

## 维度 1: SKILL.md 效率

- **定义**: SKILL.md 的行数和内容密度。过长的 SKILL.md 浪费 token 且稀释关键指令；过短可能遗漏关键步骤。
- **测量**: 行数 / 内容密度比值（步骤覆盖数 ÷ 总行数）
- **映射**: skill-builder 维度 7 — Overall Architecture
- **目标**: SKILL.md < 500 行（Anthropic 官方建议）。内容密度 > 30%（每 100 行至少 30 行是具体操作指令，非解释性文字）
- **反向标**: 如果外部 skill 的 SKILL.md 更短但覆盖了更多步骤 → 这是一个强烈吸收信号

## 维度 2: Description 触发密度

- **定义**: frontmatter description 的触发词数量和覆盖范围。高密度 description 确保 skill 在相关场景下被正确激活。
- **测量**: 字符数、独立触发词/短语数、中文/英文覆盖度
- **映射**: skill-builder 维度 1 — Frontmatter Quality
- **目标**: >= 10 个触发词/短语，涵盖中英文、正式和口语化表述
- **关键判据**: Anthropic 官方 skill 的 description 通常比社区 skill 长 2-3 倍，这是刻意为之——用高密度触发词换取激活准确性

## 维度 3: Reference 结构

- **定义**: Progressive disclosure 的实现方式——reference 文件的数量、层级深度、加载时机。
- **测量**: reference 文件数、最大层级深度、每个文件是否直接从 SKILL.md 引用
- **映射**: skill-builder 维度 7 — Overall Architecture
- **目标**: 引用深度 ≤ 1 层（SKILL.md → reference，无 reference → reference）。每个文件有明确的加载触发条件。
- **反向标**: 如果外部 skill 用 2-3 个 reference 文件实现了和我们 5-8 个文件相同的知识覆盖 → 可能我们过度拆分了

## 维度 4: Workflow 具体性

- **定义**: 工作流步骤的可执行程度——每步是否有显式输入/输出、agent 能否不依赖外部知识就执行。
- **测量**: 步骤中显式声明 I/O 的比例、步骤中含具体参数/格式/示例的比例
- **映射**: skill-builder 维度 2 — Workflow Clarity
- **目标**: 每个步骤有显式输出 artifact（如"输出到 fields.json"而非"分析字段"）。含至少 1 个具体示例

## 维度 5: Edge Case 覆盖

- **定义**: 对空输入、超大输入、异常路径、依赖缺失等边界场景的处理声明。
- **测量**: 显式边界处理声明的数量（不是 agent 推断的，是 skill 文件中明确写出的）
- **映射**: skill-builder 维度 3 — Edge Case Coverage
- **限制**: 这是 cross-reference mapping，不是 de novo discovery。只对比外部 skill 和 目标 skill 中**显式声明**的边界处理，不尝试发现"未覆盖的边界"
- **已知边界分类**（从 skill-builder Phase 0 A4 Intent Expansion 继承）: 非标准输入、依赖缺失、规模边界、环境差异、模糊指令

## 维度 6: Script 自包含

- **定义**: 脚本是否处理自己的错误而不"甩锅"给 Claude。
- **测量**: 脚本中 try-catch/error handling 的覆盖率
- **映射**: skill-builder 维度 6 — Resource Integrity
- **目标**: 无裸 `open(path).read()`、无未处理的 PermissionError/FileNotFoundError。所有 magic number 有注释说明
- **判据**: Anthropic 官方原则——"Solve, don't punt"

## 维度 7: Gate 设计

- **定义**: 关键操作前是否有显式用户确认点（checkpoint）。
- **测量**: 用户确认点的数量、位置的合理性
- **映射**: skill-builder 维度 4 — Checkpoint Design
- **目标**: 不可逆操作前有确认（如安装依赖、删除文件）。Pipeline 的阶段间有 diamond gate

## 维度 8: 反模式

- **定义**: 是否触发了已知的反模式。
- **测量**: 与反模式库的匹配数（skill-builder 本身的 9 条 + 吸收场景的 3 条）
- **映射**: 跨维度
- **注意**: 反模式是生态相关的——不同平台（Claude Code / Codex / Cursor）的反模式不同。对非 Claude Code 生态的 skill，将反模式识别降级为"疑点标记"而非确定性判定

## 差距评级

| 评级 | 含义 | 吸收优先级 |
|------|------|-----------|
| none | 无差距或外部 skill 在此维度更弱 | 不产生候选 |
| minor | 微小差距（<10%），主要是风格差异 | P3 |
| moderate | 中等差距（10-30%），有实质改进空间 | P2 |
| significant | 显著差距（>30%），外部 skill 明显更优 | P1 |

## 与 skill-builder 7 维度评分的映射

当 Step 5 用 skill-builder 现有评分体系验证吸收效果时，8 个吸收维度的改进应体现在对应的 7 维度评分中：

```
absorb 维度 → skill-builder 评分维度（加权）
─────────────────────────────────────
SKILL.md 效率 → Architecture (wt 15)
Description 密度 → Frontmatter (wt 8)
Reference 结构 → Architecture (wt 15)
Workflow 具体性 → Workflow Clarity (wt 15)
Edge case 覆盖 → Edge Case (wt 10)
Script 自包含 → Resource Integrity (wt 5)
Gate 设计 → Checkpoint (wt 7)
反模式 → 跨维度（根据具体反模式归属）
```