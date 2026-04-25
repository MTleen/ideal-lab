# build-knowledge-base-workflow

知识库构建编排工作流。从项目原始素材（源码、文档）到结构化知识库的端到端流程。

## 主 Skill

| Skill | 说明 |
|-------|------|
| [SKILL.md](SKILL.md) | 编排器：P1 材料分析 → P3 文档规划 → Agent 并行生成 → 汇总 |

## 子 Skills

| Skill | 阶段 | 说明 |
|-------|------|------|
| [kb-material-scope](kb-material-scope/) | P1 | 材料收集与范围确认 |
| [kb-deep-analysis](kb-deep-analysis/) | P2 | 深度分析（含分析方法论参考） |
| [kb-doc-planning](kb-doc-planning/) | P3 | 文档规划（含机器可读文档清单） |
| [kb-doc-writing](kb-doc-writing/) | P4 | 文档生成（已退场，由 ideal-document-workflow 替代） |
| [kb-index-review](kb-index-review/) | P5 | 索引更新与质量审查 |

## 依赖

- `ideal-document-workflow` — 各文档的完整生成流程（含评审）
