# Skill Design Patterns — 设计模式目录

用于 skill-builder absorb 的 Step 1 模式识别。agent 将外部 skill 的结构特征匹配到已知模式，匹配不到的标记为 `novel-pattern`。

每个模式包含：名称、识别特征、适用场景、吸收注意事项。

---

## 1. Gate-in-Workflow

- **识别特征**: 工作流步骤间有显式的"用户确认后才能进入下一步"指令。通常表现为 `Do NOT proceed until user confirms` 或 `Ask user before continuing`。
- **适用场景**: 多阶段 workflow skill、Pipeline skill、不可逆操作的编排器
- **吸收注意**: 过度使用 gate 会增加摩擦。只在不可逆操作前设 gate。如果外部 skill 在每个步骤都设 gate，不吸收——会导致用户疲劳。

## 2. Claim-Checklist Mapping

- **识别特征**: 先从 skill 中显式提取能力声称，再为每条声称生成 yes/no checklist 问题。表现为 `Extract claims → Propose checklist → Verify` 的三段式结构。
- **适用场景**: 任何需要可量化质量评估的 skill
- **吸收注意**: 这是 skill-builder 自己的核心模式。如果外部 skill 的 SM 中也体现了类似模式，说明它经过了类似的质量工程训练。

## 3. Intent Expansion

- **识别特征**: 在写 draft 或生成 checklist 之前，主动向用户提出边界场景问题（如"如果输入是空文件怎么办？如果依赖没安装怎么办？"）。表现为 agent 主动反问的场景列表。
- **适用场景**: 创建型 skill、需求分析型 skill
- **吸收注意**: skill-builder Phase 0 Step A4 的核心设计。如果外部 skill 在创建流程中包含了类似的主动边界扩展，值得吸收具体的边界分类维度。

## 4. CSO-Description-Only

- **识别特征**: Description 仅写触发条件和使用场景，不写 skill 的执行逻辑。高密度触发词，第三人称，每个触发词精确匹配用户可能使用的表述。
- **适用场景**: 有多个 skill 共存的生态（需要准确的 skill dispatch）
- **吸收注意**: 这是 Anthropic 官方 skill 的共性特征。如果外部 skill 的 description 比我们的长 2-3 倍但全是触发词——说明我们在触发密度上有差距。

## 5. Same-Judge Scoring

- **识别特征**: 同一 agent 在同一调用中对两个版本（改前/改后）打分，而非不同实例各自打分。文档中会出现"eliminate judge variance"或"scores both versions in the same call"。
- **适用场景**: 任何需要 A/B 比较质量评估的场景
- **吸收注意**: skill-builder Phase 4 Step 3 的核心设计。此模式要求独立 agent spawn，对基础设施有要求。

## 6. Rationalization Table

- **识别特征**: 用表格形式提供决策理由，而非纯 prose。通常表现为"条件 → 操作 → 理由"的三列表格。如 skill-builder 的 Fix Priority 表、Exception Handling 表。
- **适用场景**: 有多个条件分支的 skill、需要 agent 做上下文决策的场景
- **吸收注意**: 如果外部 skill 用表格做决策树而我们的对应 skill 用 prose——表格通常更 agent-friendly，值得吸收格式但不一定吸收内容。

## 7. Red-Flags List

- **识别特征**: 在指令末尾或关键操作前，列出不可违反的规则列表（反模式/禁令）。通常以 `Anti-Patterns`、`Do NOT`、`Red Flags` 为标题。
- **适用场景**: 有已知常见错误的 skill
- **吸收注意**: 如果外部 skill 的反模式列表中有我们没覆盖的条目——查看是否适用于我们。但注意反模式是生态相关的。

## 8. Iron-Law Enforcement

- **识别特征**: 不仅在文档某处声明了规则，还在每个相关 Phase/Step 中显式引用了该规则。如 skill-builder 的反模式检查在 Phase 2 和 Phase 4 都有落地。
- **适用场景**: 有全局约束需要跨阶段执行的复杂 skill
- **吸收注意**: 如果外部 skill 的某项规则贯彻得比我们好——值得我们检查自己的对应规则是否有多 Phase 落地。

## 9. Progressive Refinement via Changelog

- **识别特征**: 每次修改不仅记录 WHAT，还记录 WHY（为什么有效/为什么失败）。changelog 是知识点积累而非操作日志。
- **适用场景**: 需要长期迭代的 skill
- **吸收注意**: skill-builder 的 Phase 4 Step 5 changelog 设计。如果外部 skill 也在做类似的事，可以吸收它的 changelog 格式或记录维度。

## 10. Fallback Ladder

- **识别特征**: 优先级逐级退化的处理链。如 panel-review 的 `TeamCreate → 子Agent → 主Agent 自行审查` 三级退化。
- **适用场景**: 依赖外部基础设施的 skill（如需要 agent spawn、MCP 服务）
- **吸收注意**: 检查外部 skill 的退化链是否比我们的更完整——如果它有"最终兜底"而我们没有，值得补上。

## 11. Script-Self-Containment

- **识别特征**: 脚本处理自己的异常，返回有意义的错误信息或默认值，而不是抛 raw exception 让 Claude 处理。脚本中有 try-catch、有 fallback 值、所有常量有注释说明。
- **适用场景**: 包含可执行脚本的 skill
- **吸收注意**: Anthropic 官方原则——"Solve, don't punt"。如果外部 skill 的脚本比我们的更自包含，检查改进点。

## 12. Ecosystem-Aware Triggering

- **识别特征**: Description 中包含该生态特有的触发机制——如 Claude Code 的 `/skill-name:command` 格式、Codex 的 `@skill-name` 格式。trigger 关键词覆盖了生态的安装/调用命令。
- **适用场景**: 跨生态分发的 skill
- **吸收注意**: 如果外部 skill 的 trigger 列表中有生态特有的调用方式（如 `npx skills add` 后的使用模式），而我们只在 Claude Code 生态使用，不吸收。

## 13. Structured Output with Schema

- **识别特征**: Phase/Step 之间用结构化数据（JSON/YAML schema）交接，而非自由文本。表现为文档中的 JSON schema 定义、字段映射表。
- **适用场景**: 多 Phase skill、有数据从 agent → agent 流转的场景
- **吸收注意**: panel-review 的 Phase 2→3 和 Phase 3→4 都加了 JSON schema 交接。如果外部 skill 的结构化程度更高——值得吸收 schema 设计。

## 14. Pre-flight Checklist

- **识别特征**: 在核心流程开始前，执行前置条件检查。通常表现为 Step 0 或 Prerequisites 章节，检查 git clean、文件存在、依赖可用等。
- **适用场景**: 有外部依赖或状态前提的 skill
- **吸收注意**: absorb 方案本身需要 Pre-flight（计划中的 Step 0）。如果外部 skill 的前置检查比我们更完整——补上遗漏项。

## 15. Token Budget Guard

- **识别特征**: 对输入/输出大小有硬上限声明。表现为 "> X tokens 时拒绝"、"> N 分段时拒绝"、单次输出限制等。
- **适用场景**: 处理可变大小输入的 skill
- **吸收注意**: 如果外部 skill 有而我们没有的 token guard——检查我们的 skill 是否也需要。但注意不同生态的 tokenization 不同，数字不能直接照搬。