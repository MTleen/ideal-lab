---
name: ideal-ppt-generator
description: Use when user asks to "create slides", "make a presentation", "generate deck", "PPT", "幻灯片", "生成PPT", or "制作PPT"
---

# Ideal PPT Generator

将内容转换为专业的幻灯片演示文稿图片。

## 使用方法

```bash
/ideal-ppt-generator path/to/content.md
/ideal-ppt-generator path/to/content.md --style 蓝图风格
/ideal-ppt-generator path/to/content.md --audience 管理层
/ideal-ppt-generator path/to/content.md --lang zh
/ideal-ppt-generator path/to/content.md --slides 10
/ideal-ppt-generator path/to/content.md --outline-only
/ideal-ppt-generator  # 然后粘贴内容
```

## 脚本目录

**Agent 执行指令**:
1. 确定此 SKILL.md 文件的目录路径作为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`

| 脚本 | 用途 |
|------|------|
| `scripts/merge-to-pptx.ts` | 合并幻灯片为 PowerPoint |
| `scripts/merge-to-pdf.ts` | 合并幻灯片为 PDF |

## 选项

| 选项 | 描述 |
|------|------|
| `--style <名称>` | 视觉风格：预设名称、`custom`、或自定义风格名称 |
| `--audience <类型>` | 目标受众：初学者、一般读者、专家、管理层 |
| `--lang <代码>` | 输出语言 (en, zh, ja, 等) |
| `--slides <数量>` | 目标幻灯片数量 (推荐 8-25，最大 30) |
| `--outline-only` | 仅生成大纲，跳过图片生成 |
| `--prompts-only` | 生成大纲+提示词，跳过图片 |
| `--images-only` | 从现有提示词目录生成图片 |
| `--regenerate <N>` | 重新生成指定幻灯片 |

**按内容长度确定幻灯片数量**:
| 内容 | 幻灯片数 |
|------|---------|
| < 1000 字 | 5-10 |
| 1000-3000 字 | 10-18 |
| 3000-5000 字 | 15-25 |
| > 5000 字 | 20-30 (考虑拆分) |

## 风格系统

### 预设风格

| 预设 | 维度 | 适用场景 |
|------|------|---------|
| `蓝图风格` (默认) | grid + cool + technical + balanced | 网格背景，工程图纸感，架构系统设计 |
| `黑板风格` | organic + warm + handwritten + balanced | 粉笔手写，教育感，培训教程 |
| `商务风格` | clean + professional + geometric + balanced | 简洁商务，专业感，投资者演示 |
| `极简风格` | clean + neutral + geometric + minimal | 大量留白，少即是多，管理层汇报 |
| `手绘风格` | organic + warm + handwritten + balanced | 马克笔温暖感，教育教程，学习笔记 |
| `水彩风格` | organic + warm + humanist + minimal | 柔和渐变，艺术感，生活健康 |
| `暗色风格` | clean + dark + editorial + balanced | 深色背景，沉浸感，娱乐游戏 |
| `块状风格` | clean + neutral + geometric + dense | 卡片堆叠，模块化，产品演示SaaS |
| `杂志风格` | clean + vibrant + editorial + balanced | 杂志排版，大标题，产品发布演讲 |
| `图表风格` | clean + cool + editorial + dense | 数据可视化，技术解读，新闻 |
| `动画风格` | organic + vibrant + handwritten + minimal | 插画卡通，教育故事，童话魔法 |
| `架构图风格` | clean + cool + technical + dense | 流程图架构连线，技术文档，学术 |
| `像素风格` | pixel + vibrant + technical + balanced | 8-bit像素，游戏复古，开发者 |
| `论文风格` | clean + cool + technical + dense | 学术严谨，生物化学医学研究 |
| `插画风格` | clean + vibrant + humanist + balanced | 扁平矢量，简洁图形，创意儿童 |
| `复古报纸风` | paper + warm + editorial + balanced | 旧报纸质感，历史遗产，传统 |
| `高密度信息图` | clean + cool + technical + dense | 最小留白，信息密集，技术销售产品介绍 |

### 风格维度

| 维度 | 选项 | 描述 |
|------|------|------|
| **纹理 (Texture)** | clean, grid, organic, pixel, paper | 视觉纹理和背景处理 |
| **色调 (Mood)** | professional, warm, cool, vibrant, dark, neutral | 色彩温度和调色板风格 |
| **字体 (Typography)** | geometric, humanist, handwritten, editorial, technical | 标题和正文字体样式 |
| **密度 (Density)** | minimal, balanced, dense | 每页幻灯片的信息密度 |

详细规格：见 `references/dimensions/*.md`

### 自动风格选择

| 内容信号 | 预设 |
|---------|------|
| 教程、学习、教育、指南、入门 | `手绘风格` |
| 课堂、教学、学校 | `黑板风格` |
| 架构、系统、数据、分析、技术 | `蓝图风格` |
| 创意、儿童、可爱 | `插画风格` |
| 汇报、学术、研究、双语、架构图 | `架构图风格` |
| 管理层、简洁、干净、简单 | `极简风格` |
| SaaS、产品、仪表盘、指标 | `块状风格` |
| 投资者、季度、业务、企业 | `商务风格` |
| 发布、营销、演讲、杂志 | `杂志风格` |
| 娱乐、音乐、游戏、氛围 | `暗色风格` |
| 解读、新闻、科学传播 | `图表风格` |
| 故事、童话、动画、魔法 | `动画风格` |
| 游戏、复古、像素、开发者 | `像素风格` |
| 生物、化学、医学、科学 | `论文风格` |
| 历史、遗产、复古、探险 | `复古报纸风` |
| 生活、健康、旅行、艺术 | `水彩风格` |
| 技术销售、企业产品、高密度信息 | `高密度信息图` |
| 默认 | `蓝图风格` |

## 设计理念

幻灯片为**阅读和分享**而设计，非现场演示：
- 每页幻灯片无需口头说明即可理解
- 滚动时逻辑流畅
- 所有必要上下文都在幻灯片内
- 优化为社交媒体分享

详见 `references/design-guidelines.md`：
- 受众特定原则
- 视觉层次
- 内容密度指南
- 色彩和字体选择
- 字体推荐

详见 `references/layouts.md` 布局选项。

## 文件管理

### 输出目录

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/
│   └── 01-slide-cover.md, 02-slide-{slug}.md, ...
├── 01-slide-cover.png, 02-slide-{slug}.png, ...
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug**: 从主题提取 (2-4 个词，kebab-case)。示例："机器学习介绍" → `ji-qi-xue-xi-jie-shao`

## 语言处理

**检测优先级**:
1. `--lang` 标志 (明确指定)
2. EXTEND.md `language` 设置
3. 用户对话语言 (输入语言)
4. 源内容语言

**规则**: 所有响应使用用户首选语言：
- 问题和确认
- 进度报告
- 错误消息
- 完成摘要

技术术语 (风格名称、文件路径、代码) 保持英文。

## 工作流程

```
幻灯片进度:
- [ ] 步骤 1: 设置与分析
  - [ ] 1.1 加载偏好设置
  - [ ] 1.2 分析内容
  - [ ] 1.3 检查现有内容 ⚠️ 必须执行
- [ ] 步骤 2: 确认 ⚠️ 必须执行 (第1轮，第2轮仅自定义维度)
- [ ] 步骤 3: 生成大纲
- [ ] 步骤 4: 审核大纲 (条件触发)
- [ ] 步骤 5: 生成提示词
- [ ] 步骤 6: 审核提示词 (条件触发)
- [ ] 步骤 7: 生成图片
- [ ] 步骤 8: 合并为 PPTX/PDF
- [ ] 步骤 9: 输出摘要
```

### 流程图

```
输入 → 偏好设置 → 分析 → [检查现有?] → 确认 (1-2轮) → 大纲 → [审核大纲?] → 提示词 → [审核提示词?] → 图片 → 合并 → 完成
```

### 步骤 1: 设置与分析

**1.1 加载偏好设置 (EXTEND.md)**

使用 Bash 检查 EXTEND.md 是否存在 (优先级顺序):

```bash
# 首先检查项目级
test -f .ideal-skills/ideal-ppt-generator/EXTEND.md && echo "project"

# 然后检查用户级 (跨平台: $HOME 在 macOS/Linux/WSL 都可用)
test -f "$HOME/.ideal-skills/ideal-ppt-generator/EXTEND.md" && echo "user"
```

| 路径 | 位置 |
|------|------|
| .ideal-skills/ideal-ppt-generator/EXTEND.md | 项目目录 |
| $HOME/.ideal-skills/ideal-ppt-generator/EXTEND.md | 用户主目录 |

**找到 EXTEND.md 时** → 读取，解析，**输出摘要给用户**:

```
📋 已加载偏好设置 from [完整路径]
├─ 风格: [预设/自定义名称]
├─ 受众: [受众或"自动检测"]
├─ 语言: [语言或"自动检测"]
└─ 审核: [启用/禁用]
```

**未找到 EXTEND.md 时** → 首次设置使用 AskUserQuestion 或使用默认值。

**EXTEND.md 支持**: 首选风格 | 自定义维度 | 默认受众 | 语言偏好 | 审核偏好

Schema: `references/config/preferences-schema.md`

**1.2 分析内容**

1. 保存源内容 (如果粘贴，保存为 `source.md`)
   - **备份规则**: 如果 `source.md` 存在，重命名为 `source-backup-YYYYMMDD-HHMMSS.md`
2. 按照 `references/analysis-framework.md` 进行内容分析
3. 分析内容信号以推荐风格
4. 检测源语言
5. 确定推荐幻灯片数量
6. 从内容生成 topic slug

**1.3 检查现有内容** ⚠️ 必须执行

**必须在上一步之前执行。**

使用 Bash 检查输出目录是否存在:

```bash
test -d "slide-deck/{topic-slug}" && echo "exists"
```

**如果目录存在**，使用 AskUserQuestion:

```
header: "Existing"
question: "发现现有内容，如何处理?"
options:
  - label: "重新生成大纲"
    description: "保留图片，仅重新生成大纲"
  - label: "重新生成图片"
    description: "保留大纲，仅重新生成图片"
  - label: "备份后重新生成"
    description: "备份到 {slug}-backup-{timestamp}，然后重新生成全部"
  - label: "退出"
    description: "取消，保持现有内容不变"
```

**保存到 `analysis.md`**:
- 主题、受众、内容信号
- 推荐风格 (基于自动风格选择)
- 推荐幻灯片数量
- 语言检测

### 步骤 2: 确认 ⚠️ 必须执行

**两轮确认**: 第1轮必须，第2轮仅当选择"自定义维度"时。

**语言**: 使用用户输入语言或保存的语言偏好。

**显示摘要**:
- 识别到的内容类型 + 主题
- 语言: [来自 EXTEND.md 或检测]
- **推荐风格**: [预设] (基于内容信号)
- **推荐幻灯片数**: [N] (基于内容长度)

#### 第1轮 (始终)

**使用 AskUserQuestion** 回答所有 5 个问题:

**问题 1: 风格**
```
header: "风格"
question: "这个演示文稿使用哪种视觉风格?"
options:
  - label: "{推荐预设} (推荐)"
    description: "基于内容分析的最佳匹配"
  - label: "{备选预设}"
    description: "[备选风格描述]"
  - label: "自定义维度"
    description: "单独选择纹理、色调、字体、密度"
```

**问题 2: 受众**
```
header: "受众"
question: "主要受众是谁?"
options:
  - label: "一般读者 (推荐)"
    description: "广泛适用，内容易懂"
  - label: "初学者/学习者"
    description: "教育为主，解释清晰"
  - label: "专家/专业人员"
    description: "技术深度，专业知识"
  - label: "管理层"
    description: "高层洞察，少即是多"
```

**问题 3: 幻灯片数量**
```
header: "幻灯片"
question: "需要多少页幻灯片?"
options:
  - label: "{N} 页 (推荐)"
    description: "基于内容长度"
  - label: "少一些 ({N-3} 页)"
    description: "更精简，更少细节"
  - label: "多一些 ({N+3} 页)"
    description: "更详细分解"
```

**问题 4: 审核大纲**
```
header: "大纲"
question: "生成提示词前审核大纲?"
options:
  - label: "是，审核大纲 (推荐)"
    description: "审核幻灯片标题和结构"
  - label: "否，跳过审核"
    description: "直接进入提示词生成"
```

**问题 5: 审核提示词**
```
header: "提示词"
question: "生成图片前审核提示词?"
options:
  - label: "是，审核提示词 (推荐)"
    description: "审核图片生成提示词"
  - label: "否，跳过审核"
    description: "直接进入图片生成"
```

#### 第2轮 (仅当选择"自定义维度")

**使用 AskUserQuestion** 回答所有 4 个维度问题:

**问题 1: 纹理**
```
header: "纹理"
question: "哪种视觉纹理?"
options:
  - label: "clean"
    description: "纯色，无纹理"
  - label: "grid"
    description: "网格叠加，技术感"
  - label: "organic"
    description: "柔和纹理，手绘感"
  - label: "pixel"
    description: "像素块，8-bit 美学"
```

**问题 2: 色调**
```
header: "色调"
question: "哪种色彩风格?"
options:
  - label: "professional"
    description: "冷中性，深蓝/金色"
  - label: "warm"
    description: "大地色调，友好"
  - label: "cool"
    description: "蓝色/灰色，分析感"
  - label: "vibrant"
    description: "高饱和度，醒目"
```

**问题 3: 字体**
```
header: "字体"
question: "哪种字体风格?"
options:
  - label: "geometric"
    description: "现代无衬线，干净"
  - label: "humanist"
    description: "友好，易读"
  - label: "handwritten"
    description: "马克笔/刷子，手绘感"
  - label: "editorial"
    description: "杂志风格，戏剧感"
```

**问题 4: 密度**
```
header: "密度"
question: "信息密度?"
options:
  - label: "balanced (推荐)"
    description: "每页 2-3 个要点"
  - label: "minimal"
    description: "单一焦点，最大留白"
  - label: "dense"
    description: "多数据点，紧凑"
```

**第2轮后**: 将自定义维度存储为风格配置。

**确认后**:
1. 更新 `analysis.md` 的确认偏好设置
2. 存储 `skip_outline_review` 标志 (来自问题4)
3. 存储 `skip_prompt_review` 标志 (来自问题5)
4. → 步骤 3

### 步骤 3: 生成大纲

使用从步骤2确认的风格创建大纲。

**风格解析**:
- 如果选择了预设 → 读取 `references/styles/{预设}.md`
- 如果自定义维度 → 从 `references/dimensions/` 读取维度文件并组合

**生成**:
1. 按照 `references/outline-template.md` 的结构
2. 从风格或维度构建 STYLE_INSTRUCTIONS
3. 应用确认的受众、语言、幻灯片数量
4. 保存为 `outline.md`

**生成后**:
- 如果 `--outline-only`，在此停止
- 如果 `skip_outline_review` 为 true → 跳到步骤5
- 如果 `skip_outline_review` 为 false → 继续步骤4

### 步骤 4: 审核大纲 (条件触发)

**当用户在步骤2选择"否，跳过审核"时跳过此步骤。**

**目的**: 在生成提示词前审核大纲结构。

**语言**: 使用用户输入语言或保存的语言偏好。

**显示**:
- 总幻灯片数: N
- 风格: [预设名称或 "custom: texture+mood+typography+density"]
- 逐页摘要表:

```
| # | 标题 | 类型 | 布局 |
|---|------|------|------|
| 1 | [标题] | 封面 | title-hero |
| 2 | [标题] | 内容 | [布局] |
| 3 | [标题] | 内容 | [布局] |
| ... | ... | ... | ... |
```

**使用 AskUserQuestion**:
```
header: "Confirm"
question: "准备生成提示词了吗?"
options:
  - label: "是，继续 (推荐)"
    description: "生成图片提示词"
  - label: "先编辑大纲"
    description: "我将修改 outline.md 后再继续"
  - label: "重新生成大纲"
    description: "用不同方法创建新大纲"
```

**响应后**:
1. 如果"先编辑大纲" → 通知用户编辑，完成后再次询问
2. 如果"重新生成大纲" → 返回步骤3
3. 如果"是，继续" → 继续步骤5

### 步骤 5: 生成提示词

1. 读取 `references/base-prompt.md`
2. 对于大纲中的每页幻灯片:
   - 从大纲提取 STYLE_INSTRUCTIONS (不再从风格文件读取)
   - 添加幻灯片特定内容
   - 如果指定了 `布局:`，包含来自 `references/layouts.md` 的布局指导
3. 保存到 `prompts/` 目录
   - **备份规则**: 如果提示词文件存在，重命名为 `prompts/NN-slide-{slug}-backup-YYYYMMDD-HHMMSS.md`

**生成后**:
- 如果 `--prompts-only`，在此停止并输出提示词摘要
- 如果 `skip_prompt_review` 为 true → 跳到步骤7
- 如果 `skip_prompt_review` 为 false → 继续步骤6

### 步骤 6: 审核提示词 (条件触发)

**当用户在步骤2选择"否，跳过审核"时跳过此步骤。**

**目的**: 在图片生成前审核提示词。

**语言**: 使用用户输入语言或保存的语言偏好。

**显示**:
- 总提示词数: N
- 风格: [预设名称或自定义维度]
- 提示词列表:

```
| # | 文件名 | 幻灯片标题 |
|---|--------|-------------|
| 1 | 01-slide-cover.md | [标题] |
| 2 | 02-slide-xxx.md | [标题] |
| ... | ... | ... |
```

- 提示词目录路径: `prompts/`

**使用 AskUserQuestion**:
```
header: "Confirm"
question: "准备生成幻灯片图片了吗?"
options:
  - label: "是，继续 (推荐)"
    description: "生成所有幻灯片图片"
  - label: "先编辑提示词"
    description: "我将修改提示词后再继续"
  - label: "重新生成提示词"
    description: "用不同方法创建新提示词"
```

**响应后**:
1. 如果"先编辑提示词" → 通知用户编辑，完成后再次询问
2. 如果"重新生成提示词" → 返回步骤5
3. 如果"是，继续" → 继续步骤7

### 步骤 7: 生成图片

**对于 `--images-only`**: 从现有提示词开始。

**对于 `--regenerate N`**: 仅重新生成指定幻灯片。

**标准流程**:
1. 选择可用的图片生成 skill (baoyu-image-gen)
2. 生成会话 ID: `slides-{topic-slug}-{timestamp}`
3. 对于每页幻灯片:
   - **备份规则**: 如果图片文件存在，重命名为 `NN-slide-{slug}-backup-YYYYMMDD-HHMMSS.png`
   - 使用相同会话 ID 顺序生成图片
4. 报告进度: "已生成 X/N" (使用用户语言)
5. 失败时自动重试一次后再报告错误

### 步骤 8: 合并为 PPTX 和 PDF

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pptx.ts <slide-deck-dir>
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### 步骤 9: 输出摘要

**语言**: 使用用户输入语言或保存的语言偏好。

```
幻灯片演示文稿完成！

主题: [主题]
风格: [预设名称或自定义维度]
位置: [目录路径]
幻灯片: 共 N 页

- 01-slide-cover.png - 封面
- 02-slide-intro.png - 内容
- ...
- {NN}-slide-back-cover.png - 封底

大纲: outline.md
PPTX: {topic-slug}.pptx
PDF: {topic-slug}.pdf
```

## 部分工作流程

| 选项 | 工作流程 |
|------|---------|
| `--outline-only` | 仅步骤 1-3 (大纲后停止) |
| `--prompts-only` | 步骤 1-5 (生成提示词，跳过图片) |
| `--images-only` | 跳到步骤 7 (需要现有 prompts/) |
| `--regenerate N` | 仅重新生成指定幻灯片 |

### 使用 `--prompts-only`

生成大纲和提示词，不生成图片:

```bash
/ideal-ppt-generator content.md --prompts-only
```

输出: `outline.md` + `prompts/*.md` 准备好审核/编辑。

### 使用 `--images-only`

从现有提示词生成图片 (从步骤 7 开始):

```bash
/ideal-ppt-generator slide-deck/topic-slug/ --images-only
```

前提条件:
- `prompts/` 目录包含幻灯片提示词文件
- `outline.md` 包含风格信息

### 使用 `--regenerate`

重新生成指定幻灯片:

```bash
# 单页
/ideal-ppt-generator slide-deck/topic-slug/ --regenerate 3

# 多页
/ideal-ppt-generator slide-deck/topic-slug/ --regenerate 2,5,8
```

流程:
1. 读取指定幻灯片的现有提示词
2. 仅重新生成那些幻灯片的图片
3. 重新生成 PPTX/PDF

## 幻灯片修改

### 快速参考

| 操作 | 命令 | 手动步骤 |
|------|------|---------|
| **编辑** | `--regenerate N` | **首先更新提示词文件** → 重新生成图片 → 重新生成 PDF |
| **添加** | 手动 | 创建提示词 → 生成图片 → 重新编号后续 → 更新大纲 → 重新生成 PDF |
| **删除** | 手动 | 删除文件 → 重新编号后续 → 更新大纲 → 重新生成 PDF |

### 编辑单页幻灯片

1. **首先更新提示词文件** 在 `prompts/NN-slide-{slug}.md`
2. 运行: `/ideal-ppt-generator <dir> --regenerate N`
3. 或手动重新生成图片 + PDF

**重要**: 更新幻灯片时，**始终先更新提示词文件** (`prompts/NN-slide-{slug}.md`)，然后再重新生成。这确保更改被记录且可重现。

### 添加新幻灯片

1. 在位置创建提示词: `prompts/NN-slide-{new-slug}.md`
2. 使用相同会话 ID 生成图片
3. **重新编号**: 后续文件 NN+1 (slug 不变)
4. 更新 `outline.md`
5. 重新生成 PPTX/PDF

### 删除幻灯片

1. 删除 `NN-slide-{slug}.png` 和 `prompts/NN-slide-{slug}.md`
2. **重新编号**: 后续文件 NN-1 (slug 不变)
3. 更新 `outline.md`
4. 重新生成 PPTX/PDF

### 文件命名

格式: `NN-slide-[slug].png`
- `NN`: 两位序号 (01, 02, ...)
- `slug`: 来自内容的 kebab-case (2-5 个词，唯一)

**重新编号规则**: 仅 NN 变化，slug 保持不变。

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/analysis-framework.md` | 演示文稿内容分析 |
| `references/outline-template.md` | 大纲结构和格式 |
| `references/modification-guide.md` | 编辑、添加、删除幻灯片工作流程 |
| `references/content-rules.md` | 内容和风格指南 |
| `references/design-guidelines.md` | 受众、字体、色彩、视觉元素 |
| `references/layouts.md` | 布局选项和选择提示 |
| `references/base-prompt.md` | 图片生成基础提示词 |
| `references/dimensions/*.md` | 维度规格 (纹理、色调、字体、密度) |
| `references/dimensions/presets.md` | 预设 → 维度映射 |
| `references/styles/<style>.md` | 完整风格规格 |
| `references/config/preferences-schema.md` | EXTEND.md 结构 |

## 注意事项

- 图片生成: 每页 10-30 秒
- 生成失败时自动重试一次
- 使用风格化替代方案处理敏感公众人物
- 通过会话 ID 保持风格一致性
- **步骤 2 确认必须** - 不要跳过 (风格、受众、幻灯片数、大纲审核、提示词审核)
- **步骤 4 条件触发** - 仅当用户在步骤 2 请求大纲审核时
- **步骤 6 条件触发** - 仅当用户在步骤 2 请求提示词审核时

## 扩展支持

通过 EXTEND.md 自定义配置。见**步骤 1.1** 的路径和支持选项。
