---
# ⚠️ 已退场：此 skill 已被 ideal-document-workflow 替代。
# 文档生成现由 build-knowledge-base-workflow 通过 Agent 工具并行调用 ideal-document-workflow 完成。
# 本文件保留仅作历史参考。
name: kb-doc-writing
description: |
  知识库构建 P4 文档生成阶段。根据文档规划，并行生成知识库文档。
  触发场景：(1) workflow 调用本 skill (2) 用户要求"生成知识库文档"、"生成文档"
  产出：知识库/项目名称/*.md
---

# KB Doc Writing (P4)

## Overview

根据 P3 文档规划，使用子智能体并行生成各知识库文档。每个文档基于对应的模板和分析数据生成。

## 输入

- P1-材料清单.md
- P2-分析报告.md
- P3-文档规划.md
- 项目名称、分类、原始材料路径

## 输出

`{分类}/知识库/{项目名称}/*.md`（7+ 个知识库文档）

> **可选额外文档**：`核心算法详解.md` — 当项目包含复杂算法实现（如LLM调用、Pipeline编排、数据处理管线等）时，在 P3 文档规划中指定后生成。此文档需要分析阶段（kb-deep-analysis）深入源码提取算法细节才能正确生成。

## 写作规范

### 基本原则

1. **彻底填充**：所有内容基于分析结果填充，禁止占位符（"待填写"、"TODO"）
2. **标注来源**：关键信息标注源文件路径（如"根据 `src/pipeline/core.py`"）
3. **诚实标注**：原始材料不足的章节标注"**[待补充]**"并说明需要什么信息
4. **图表规范**：架构图和数据流图必须使用 Mermaid 语法
5. **客观表述**：使用"系统支持"而非"系统拥有强大的"，避免营销化语言
6. **中文为主**：技术术语保留英文原名，其余使用中文

### 模板使用

每个文档基于对应模板生成。模板位于 `assets/` 目录：
- [core_templates.md](assets/core_templates.md) — 4个核心文档模板
- [datagov_templates.md](assets/datagov_templates.md) — 数据治理专属模板
- [model_training_templates.md](assets/model_training_templates.md) — 模型训练专属模板
- [knowledge_mgmt_templates.md](assets/knowledge_mgmt_templates.md) — 知识库与知识治理专属模板
- [agent_templates.md](assets/agent_templates.md) — 智能体专属模板

### Mermaid 图表

详见 [mermaid_guide.md](references/mermaid_guide.md)

## 执行步骤

### 1. 读取任务计划

从 P3-文档规划.md 获取任务列表、依赖关系、内容要点。

### 2. 准备共享上下文

将以下信息打包为共享上下文，传递给所有写作子智能体：

- 项目基本信息（名称、分类、定位）
- 技术架构概览
- 功能模块清单
- 部署运维信息
- 分类专属分析结果

### 3. 并行启动写作 Agent

使用 `Agent` 工具并行启动写作 Agent：

```python
for task in tasks:
    Agent(
        subagent_type="general-purpose",
        description=f"知识库文档: {task.title}",
        prompt=f"""
你是一个知识库构建专家。请根据分析数据生成知识库文档。

## 任务
- 文档：{task.title}
- 输出路径：{task.output_path}
- 模板：{task.template_ref}

## 项目信息
{shared_context}

## 内容要点
{task.content_points}

## 写作规范
1. 基于分析数据填充，禁止占位符
2. 原始材料不足的章节标注"**[待补充]**"
3. 关键信息标注来源文件路径
4. 架构图/数据流图使用 Mermaid 语法
5. 客观表述，避免营销化语言
6. 技术术语保留英文原名

## 输出
直接写入文件：{task.output_path}
请直接输出完整文档内容。
""",
        run_in_background=True
    )
```

### 4. 并发控制

- **最大并发数**：5 个并行任务
- **优先级**：先启动无依赖的任务（概述、部署与运维），再启动有依赖的任务
- **依赖处理**：有依赖的任务等待上游完成后启动

### 5. 结果收集

各 Agent 完成后：
1. 检查各文档是否生成成功
2. 如有失败，重新执行该任务
3. 统计完成情况

### 6. 生成评审文档

输出执行情况报告：

```markdown
## 文档生成情况

| 文档 | 状态 | 字数 | 图表数 | 备注 |
|------|------|------|--------|------|
| 概述.md | ✅ | 1200 | 0 | |
| 技术架构.md | ✅ | 1800 | 2 | 含架构图、部署图 |
| ... | | | | |

## 统计
- 文档总数：7+
- 总字数：XXXX
- 图表总数：X
- 待补充标记：X 处
```

## 质量自检

生成完成后，对每个文档进行自检：

| 检查项 | 方法 |
|--------|------|
| 占位符 | 搜索"待填写"、"TODO"、"TBD" |
| 待补充标记 | 搜索"\[待补充\]"，确认已标注原因 |
| Mermaid 语法 | 检查代码块语法是否正确 |
| 图文一致 | 架构图组件与文字描述是否匹配 |
| 表格完整 | 所有表格是否填充完整 |
