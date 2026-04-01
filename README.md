# ideal-lab

Claude Code 最佳实践 skill 沉淀仓库。

## 目录结构

```
ideal-lab/
├── best-practices/
│   ├── build-knowledge-base-workflow/  # 知识库构建编排工作流
│   ├── content-tools/                  # 内容生成工具（图片、PPT）
│   ├── dev-workflow/                    # 开发流程工作流（15 阶段）
│   ├── ideal-dify-generator/           # Dify 工作流 DSL 生成器
│   ├── ideal-document-workflow/         # 结构化文档写作工作流（12 阶段）
│   ├── meta-tools/                      # 工具类（mypush）
│   └── utilities/                       # 通用工具（deep-research）
└── README.md
```

## 最佳实践清单

| 分类 | 说明 | 主要内容 |
|------|------|----------|
| [build-knowledge-base-workflow](best-practices/build-knowledge-base-workflow/) | 知识库构建编排 | P1 材料分析 → P3 文档规划 → Agent 并行生成 → 汇总 |
| [content-tools](best-practices/content-tools/) | 内容生成工具 | AI 图片生成、PPT 生成器 |
| [dev-workflow](best-practices/dev-workflow/) | 开发流程工作流 | 需求→方案→计划→编码→评审→测试→交付，15 阶段 |
| [ideal-dify-generator](best-practices/ideal-dify-generator/) | Dify 工作流生成 | 从需求到 DSL YAML，端到端生成与校验 |
| [ideal-document-workflow](best-practices/ideal-document-workflow/) | 结构化文档写作 | 需求分析→大纲→写作→配图→渲染输出，12 阶段 |
| [meta-tools](best-practices/meta-tools/) | 工具类 | mypush — skill 推送工具 |
| [utilities](best-practices/utilities/) | 通用工具 | deep-research — 深度调研 |

## 使用方式

### 推送新最佳实践

使用 `mypush` skill 将本地 skill 推送到仓库：

```bash
# 在 Claude Code 中调用
/mypush
```

### 克隆使用

```bash
git clone https://github.com/MTleen/ideal-lab.git
# 复制需要的 skill 到 ~/.claude/skills/
cp -r ideal-lab/best-practices/dev-workflow/ideal-yolo ~/.claude/skills/
```
