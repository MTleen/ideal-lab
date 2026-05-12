# 流程状态文件规格（flow-state-spec）

本文档定义 `slide-deck/{topic-slug}/流程状态.md` 的完整格式。

---

## YAML Frontmatter

```yaml
---
# === 基本信息 ===
project_name: {项目名称}                        # 必填，中文或英文
source_material: {源素材路径}                    # 必填，相对路径或绝对路径
canvas_format: "1280x720"                       # 必填，HTML 画布尺寸，固定值

# === 流程状态 ===
current_phase: P1                               # 必填，当前阶段 P1-P13
status: in_progress                             # 必填，见状态枚举
yolo_mode: false                                # 必填，boolean

# === 风格配置 ===
style:
  preset: {预设名称或 custom}                    # 必填，如 蓝图风格 / 商务风格 / custom
  texture: {clean|grid|organic|pixel|paper}     # 条件必填，preset=custom 时必填
  mood: {professional|warm|cool|vibrant|dark|neutral}  # 条件必填
  typography: {geometric|humanist|handwritten|editorial|technical}  # 条件必填
  density: {minimal|balanced|dense}              # 条件必填

# === 受众与语言 ===
audience: {初学者|一般读者|专家|管理层}            # 必填
language: {en|zh|ja|...}                        # 必填

# === 幻灯片规模 ===
slide_count:
  recommended: {N}                              # 必填，P1 推荐数量
  confirmed: {N}                                # P2 后填入，用户确认的数量

# === 图像策略 ===
image_approach: {none|user-provided|ai-generated|placeholders}  # 必填
# none: 不使用配图
# user-provided: 用户提供图片，放在 images/ 目录
# ai-generated: AI 生成配图，触发 P9/P10 阶段
# placeholders: 使用占位符

# === 评审配置 ===
review:
  skip_outline: false                           # 为 true 时跳过 P6 大纲审核
  skip_prompts: false                           # 为 true 时跳过 P8 提示词审核
  skip_images: false                            # 为 true 时跳过 P10 图像审核

# === 时间戳 ===
created_at: {YYYY-MM-DD HH:mm}                  # 必填，流程创建时间
updated_at: {YYYY-MM-DD HH:mm}                  # 必填，最后更新时间
---
```

### 字段详细说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `project_name` | string | 是 | 演示文稿项目名称，用于显示 |
| `source_material` | string | 是 | 源素材文件路径（相对或绝对） |
| `canvas_format` | string | 是 | HTML 画布尺寸，当前固定为 `"1280x720"` |
| `current_phase` | enum | 是 | 当前所处阶段：P1-P13 |
| `status` | enum | 是 | 流程整体状态，见下方枚举 |
| `yolo_mode` | boolean | 是 | 是否启用 YOLO 自动推进模式 |
| `style.preset` | string | 是 | 视觉风格预设名称，自定义时填 `"custom"` |
| `style.texture` | enum | 条件 | 纹理维度，preset=custom 时必填 |
| `style.mood` | enum | 条件 | 色调维度，preset=custom 时必填 |
| `style.typography` | enum | 条件 | 字体维度，preset=custom 时必填 |
| `style.density` | enum | 条件 | 密度维度，preset=custom 时必填 |
| `audience` | enum | 是 | 目标受众 |
| `language` | string | 是 | 输出语言代码 |
| `slide_count.recommended` | integer | 是 | P1 分析后推荐的幻灯片数量 |
| `slide_count.confirmed` | integer | 条件 | P2 用户确认的数量，P2 之前为空 |
| `image_approach` | enum | 是 | 图像生成策略 |
| `review.skip_outline` | boolean | 是 | 是否跳过大纲审核（P6） |
| `review.skip_prompts` | boolean | 是 | 是否跳过提示词审核（P8） |
| `review.skip_images` | boolean | 是 | 是否跳过图像审核（P10） |
| `created_at` | datetime | 是 | 流程创建时间 |
| `updated_at` | datetime | 是 | 每次状态更新时刷新 |

### 状态枚举

| 值 | 含义 |
|----|------|
| `pending` | 未开始 |
| `in_progress` | 进行中 |
| `completed` | 已完成 |
| `approved` | 评审通过 |
| `blocked` | 被阻塞 |
| `skipped` | 条件跳过 |
| `auto_approved` | YOLO 模式或 review 配置自动通过 |

---

## Markdown 状态表

YAML frontmatter 之后，使用 Markdown 表格记录各阶段的详细状态。

### 完整模板

```markdown
## 阶段状态

### 研究与规划（P1-P4）

| 阶段 | 类型 | 状态 | 完成时间 | 产出 | 备注 |
|------|------|------|----------|------|------|
| P1 需求研究 | 产物 | ⏳ pending | - | analysis.md | - |
| P2 需求确认 | 评审 | ⏳ pending | - | - | 用户确认风格/受众/规模 |
| P3 策略规划 | 产物 | ⏳ pending | - | strategy.md | - |
| P4 策略确认 | 评审 | ⏳ pending | - | - | **[BLOCKING]** |

### 内容工程（P5-P8）

| 阶段 | 类型 | 状态 | 完成时间 | 产出 | 备注 |
|------|------|------|----------|------|------|
| P5 大纲生成 | 产物 | ⏳ pending | - | outline.md | - |
| P6 大纲审核 | 评审 | ⏳ pending | - | - | 可通过 review.skip_outline 跳过 |
| P7 提示词工程 | 产物 | ⏳ pending | - | prompts/*.md | - |
| P8 提示词审核 | 评审 | ⏳ pending | - | - | 可通过 review.skip_prompts 跳过 |

### 视觉制作（P9-P12）

| 阶段 | 类型 | 状态 | 完成时间 | 产出 | 备注 |
|------|------|------|----------|------|------|
| P9 图像生成 | 产物 | ⏳ pending | - | images/*.png | image_approach=ai-generated 时执行 |
| P10 图像审核 | 评审 | ⏳ pending | - | - | 可通过 review.skip_images 跳过 |
| P11 HTML 执行 | 产物 | ⏳ pending | - | html_output/NN-slide-*.html | - |
| P12 HTML 审核 | 评审 | ⏳ pending | - | - | - |

### 交付（P13）

| 阶段 | 类型 | 状态 | 完成时间 | 产出 | 备注 |
|------|------|------|----------|------|------|
| P13 导出交付 | 产物 | ⏳ pending | - | .pptx + .pdf | - |

## 评审历史

| 阶段 | 轮次 | 结果 | 说明 |
|------|------|------|------|
```

### 状态图标

| 图标 | 对应值 |
|------|--------|
| ⏳ | `pending` |
| 🔄 | `in_progress` |
| ✅ | `completed` |
| ✅ | `approved` |
| ⏭️ | `skipped` / `auto_approved` |
| 🚫 | `blocked` |

---

## 状态更新示例

### 初始化时（P1 开始前）

```yaml
---
project_name: "机器学习入门教程"
source_material: "source-ml-intro.md"
canvas_format: "1280x720"
current_phase: P1
status: in_progress
yolo_mode: false
style:
  preset: 蓝图风格
  texture: null
  mood: null
  typography: null
  density: null
audience: null
language: zh
slide_count:
  recommended: null
  confirmed: null
image_approach: null
review:
  skip_outline: false
  skip_prompts: false
  skip_images: false
created_at: "2026-04-12 14:30"
updated_at: "2026-04-12 14:30"
---
```

### P1 完成后

```yaml
---
project_name: "机器学习入门教程"
source_material: "source-ml-intro.md"
canvas_format: "1280x720"
current_phase: P2
status: in_progress
yolo_mode: false
style:
  preset: 手绘风格
  texture: null
  mood: null
  typography: null
  density: null
audience: 初学者
language: zh
slide_count:
  recommended: 12
  confirmed: null
image_approach: ai-generated
review:
  skip_outline: false
  skip_prompts: false
  skip_images: false
created_at: "2026-04-12 14:30"
updated_at: "2026-04-12 14:45"
---
```

### P4 通过后（进入内容工程）

```yaml
---
project_name: "机器学习入门教程"
source_material: "source-ml-intro.md"
canvas_format: "1280x720"
current_phase: P5
status: in_progress
yolo_mode: false
style:
  preset: 手绘风格
  texture: organic
  mood: warm
  typography: handwritten
  density: balanced
audience: 初学者
language: zh
slide_count:
  recommended: 12
  confirmed: 15
image_approach: ai-generated
review:
  skip_outline: false
  skip_prompts: true
  skip_images: true
created_at: "2026-04-12 14:30"
updated_at: "2026-04-12 15:20"
---
```

### 条件跳过场景（image_approach = none）

当 `image_approach` 不为 `ai-generated` 时，P9 和 P10 的状态表应标记为 `skipped`：

```markdown
### 视觉制作（P9-P12）

| 阶段 | 类型 | 状态 | 完成时间 | 产出 | 备注 |
|------|------|------|----------|------|------|
| P9 图像生成 | 产物 | ⏭️ skipped | - | - | image_approach=none，跳过 |
| P10 图像审核 | 评审 | ⏭️ skipped | - | - | 随 P9 跳过 |
| P11 HTML 执行 | 产物 | ⏳ pending | - | html_output/NN-slide-*.html | - |
| P12 HTML 审核 | 评审 | ⏳ pending | - | - | - |
```

---

## 编排器读取规则

编排器在每次循环开始时执行以下读取流程：

```
1. 读取 流程状态.md
2. 解析 YAML frontmatter
3. 提取 current_phase、status、yolo_mode
4. 提取 image_approach（判断 P9/P10 是否跳过）
5. 提取 review 配置（判断 P6/P8/P10 是否自动通过）
6. 解析 Markdown 状态表
7. 确定第一个非 completed/approved/skipped/auto_approved 的阶段
8. 进入该阶段
```

### 异常处理

| 异常 | 处理方式 |
|------|---------|
| YAML 解析失败 | 报告格式错误，停止流程 |
| current_phase 不在 P1-P13 范围 | 报告非法值，停止流程 |
| 状态表与 frontmatter 不一致 | 以 frontmatter 为准，记录警告 |
| 缺少必填字段 | 报告缺失字段，停止流程 |
