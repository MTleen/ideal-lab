# Technical Proposal Workflow

AI-powered technical proposal writing system. 自动化的技术方案撰写工作流，覆盖从需求分析到 Word 交付的全流程。

## 快速开始

### 1. 安装 Skills

将 `skills/` 目录复制到你的 Claude Code 配置目录：

```bash
# macOS
cp -r skills/* ~/.claude/skills/

# Linux
cp -r skills/* ~/.claude/skills/
```

### 2. 开始使用

在 Claude Code 中输入：

```
写一个技术方案：基于知识库的自然语言查询系统
```

或者启动完整工作流：

```
/technical-proposal-workflow
```

## 架构

```
technical-proposal-workflow/
├── skills/
│   ├── technical-proposal-workflow/     # 编排器：协调全流程
│   ├── technical-proposal-analysis/    # P1 需求分析
│   ├── technical-proposal-outline/     # P2 大纲生成
│   ├── technical-proposal-task-split/  # P3 任务拆分
│   ├── technical-proposal-writing/     # P4 并行写作
│   ├── technical-proposal-illustration/ # P5 智能配图
│   ├── technical-proposal-merge/       # P6 文档合并
│   │   └── scripts/
│   │       └── markdown_to_word.sh    # Markdown → Word 转换脚本
│   └── technical-proposal-style/       # 写作风格规范
```

## 工作流程

| 阶段 | Skill | 产出 |
|------|-------|------|
| P1 | `technical-proposal-analysis` | P1-需求分析.md |
| P2 | `technical-proposal-outline` | P2-技术方案大纲.md |
| P3 | `technical-proposal-task-split` | P3-任务拆分计划.md |
| P4 | `technical-proposal-writing` | sections/*.md |
| P5 | `technical-proposal-illustration` | sections/*.md + images/ |
| P6 | `technical-proposal-merge` | 最终方案.docx |

每个阶段完成后需人工审核，通过后进入下一阶段。

## 依赖

### P6 文档转换

- **pandoc**: `brew install pandoc`
- **python-docx**: `pip3 install python-docx`

```bash
# 转换示例
./scripts/markdown_to_word.sh -o 最终方案.docx sections/
```

## License

MIT
