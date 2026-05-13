---
name: ideal-ppt-workflow
description: Use when user asks to "create slides", "make a presentation", "generate deck", "PPT", "幻灯片", "生成PPT", "制作PPT", "制作演示文稿"
---

> **主智能体（Claude Code 会话）职责：仅编排，不执行。所有阶段内的工作由 Phase Skill 完成，本 skill 只负责读取状态、调度阶段、管理流转。**

# ideal-ppt-workflow（AIPPT 流水线编排器）

## 角色定位

**主智能体 = 编排器（Orchestrator）**，永远不直接执行任何阶段内工作。

### 主智能体只做三件事

1. **读取** `流程状态.md`，确定当前阶段
2. **调用** Phase Skill（通过 Skill 工具调度）
3. **更新** `流程状态.md`，推进到下一阶段

### 主智能体绝对不做

- ❌ 读取源素材或分析内容
- ❌ 生成大纲、提示词或 HTML/图片
- ❌ 做风格推荐或内容策略决策
- ❌ 直接生成图像或导出文件
- ❌ 验证 HTML/图片质量

所有上述工作由各 Phase Skill 内部完成。

---

## 流水线概览

### 13 个阶段（P1-P13）

| 阶段 | 类型 | Phase Skill | 中文名称 | 核心产出 |
|------|------|-------------|---------|---------|
| **P1** | 产物 | `ideal-ppt-research` | 需求研究 | `analysis.md` |
| **P2** | 评审 | *(用户审核)* | 需求确认 | 用户确认的风格/受众/规模 |
| **P3** | 产物 | `ideal-ppt-strategist` | 策略规划 | `strategy.md` |
| **P4** | 评审 | *(用户审核)* | 策略确认 | 用户批准的策略方向 **[BLOCKING]** |
| **P5** | 产物 | `ideal-ppt-outline` | 大纲生成 | `outline.md` |
| **P6** | 评审 | *(用户审核)* | 大纲审核 | 用户确认的幻灯片结构 |
| **P7** | 产物 | `ideal-ppt-prompt` | 提示词工程 | `prompts/*.md` |
| **P8** | 评审 | *(用户审核)* | 提示词审核 | 用户确认的生成指令 |
| **P9** | 产物 | `ideal-ppt-image` | 图像生成 | `images/*.png` |
| **P10** | 评审 | *(用户审核)* | 图像审核 | 用户确认的配图 |
| **P11** | 产物 | `ideal-ppt-executor` / `ideal-ppt-image-executor` | 幻灯片执行 | `html_output/*.html` 或 `images_output/*.png` |
| **P12** | 评审 | *(用户审核)* | 幻灯片审核 | 用户确认的最终幻灯片 |
| **P13** | 产物 | `ideal-ppt-export` | 导出交付 | `.pptx` + `.pdf` |

### 阶段分组

| 分组 | 阶段 | 说明 |
|------|------|------|
| **研究与规划** | P1 → P4 | 理解需求，制定策略 |
| **内容工程** | P5 → P8 | 生成大纲和提示词 |
| **视觉制作** | P9 → P12 | 生成图像和幻灯片（HTML 或图片） |
| **交付** | P13 | 导出最终文件 |

### 条件跳过

| 条件 | 跳过阶段 | 说明 |
|------|---------|------|
| `image_approach != "ai-generated"` | P9, P10 | 非AI生成图像时，跳过图像生成与审核 |
| `review.skip_outline: true` | P6 | 自动通过大纲审核 |
| `review.skip_prompts: true` | P8 | 自动通过提示词审核 |
| `review.skip_images: true` | P10 | 自动通过图像审核 |

### BLOCKING 评审关卡

**P4（策略确认）是唯一的硬性 BLOCKING 评审关卡。**

- P4 未通过前，**禁止进入 P5 及后续阶段**
- 用户必须在 P4 明确批准策略方向（风格、结构、受众）
- YOLO 模式下，P4 仍需用户确认或由 `ideal-yolo` 评审通过
- 其他评审关卡（P2/P6/P8/P10/P12）可根据 review 配置自动通过

---

## 两种执行模式

| 模式 | yolo_mode | 行为 |
|------|-----------|------|
| **手动模式** | `false` | 每次阶段完成后停下来，等待用户确认后再推进 |
| **YOLO 模式** | `true` | 阶段完成后不停止，自动推进直到流程完成（P13）或熔断 |

### 手动模式行为（yolo_mode: false）

```
1. 读取 流程状态.md → current_phase
2. 判断阶段类型
   ┌──────────────────────────────────────┐
   │ 产物阶段（P1/P3/P5/P7/P9/P11/P13）   │
   │   → 调用 Phase Skill                  │
   │   → 等待 Skill 返回                   │
   │   → 验证产出文件存在                  │
   │   → 更新 current_phase                │
   │   → ⏸ 停下来等待用户确认             │
   ├──────────────────────────────────────┤
   │ 评审阶段（P2/P4/P6/P8/P10/P12）      │
   │   → 展示摘要                          │
   │   → 询问是否通过 / 启用 YOLO          │
   │   → 等待用户响应                      │
   └──────────────────────────────────────┘
```

### YOLO 模式行为（yolo_mode: true）

**主智能体在 YOLO 模式下是"永不停歇的循环器"。** 阶段完成后**立即回到起点**，不等待用户输入，直到流程终止。

```
YOLO 自动循环：

循环（永不停止，除非满足终止条件）：
  1. 读取 流程状态.md → current_phase, status, yolo_mode
  2. 检查终止条件（见下方）→ 满足则输出结果，停止循环
  3. 确定当前阶段 X = 第一个未完成的阶段
     （遍历 P1→P2→...→P13，查找第一个状态不为 completed/approved 的阶段）
     ⚠️ 序列完整性校验：X 序号 <= current_phase → 前置阶段被跳过，输出警告并停住
  4. 检查条件跳过：
     - 如果 X = P9 且 image_approach != "ai-generated" → 标记 P9/P10 为 skipped → 回到循环起点
     - 如果 X = P6 且 review.skip_outline = true → 标记 P6 为 auto_approved → 回到循环起点
     - 如果 X = P8 且 review.skip_prompts = true → 标记 P8 为 auto_approved → 回到循环起点
     - 如果 X = P10 且 review.skip_images = true → 标记 P10 为 auto_approved → 回到循环起点
  5. 如果 X 是产物阶段（P1/P3/P5/P7/P9/P11/P13）：
       → 调用 Phase Skill
	         P11: rendering_mode=html → ideal-ppt-executor, rendering_mode=image → ideal-ppt-image-executor
       → 等待完成
       → 验证产出文件存在且非空
       → 更新 flow state：X > current_phase 时推进 current_phase → X，状态设为 completed
       → 立即回到循环起点（步骤 1）
  6. 如果 X 是评审阶段（P2/P4/P6/P8/P10/P12）：
       → 如果 X = P4（BLOCKING 关卡）：
         → 调用 ideal-yolo 执行评审
         → 通过 → approved，回到循环起点
         → 熔断 → 输出报告，停止循环
       → 其他评审阶段：
         → 检查 review 配置，可自动通过则 auto_approved
         → 否则调用 ideal-yolo 执行评审
         → 通过 → approved，回到循环起点
         → 熔断 → 输出报告，停止循环
  7. 如果 X = P13（交付阶段）：
       → 调用 ideal-ppt-export
       → 等待完成
       → 更新状态为 "已完成"
       → 输出流程完成摘要 → 停止循环
```

**终止条件**（满足任一即停止）：
- `status: 已完成` 或 `status: 已交付`
- P13 阶段已完成（产物文件已生成）
- 评审返回熔断信号 → 停止循环，报告未解决问题

**关键原则**：YOLO 模式下，主智能体在每次阶段完成后**立即回到循环起点**，不输出"等待用户确认"之类的提示，不停下来。循环直到终止条件满足。

---

## 编排协议

### 每次只推进一个阶段

```
1. 读取 flow state → current_phase = X
2. 确定下一阶段 X+1 的 Phase Skill 名称（参见 phase-mapping.md）
3. 检查前置条件（前置阶段的产出文件是否存在）
4. 调用 Phase Skill（通过 Skill 工具）
5. 等待 Skill 返回执行摘要
6. 验证产出文件存在且非空
7. 更新 flow state：current_phase → X+1，status 更新，时间戳更新
8. 如果 yolo_mode → 回到步骤 1，否则停下来等待用户确认
```

### Phase Skill 职责边界

| Phase Skill 负责 | Phase Skill 不负责 |
|------------------|-------------------|
| 读取前置产出文件 | 更新 flow state |
| 执行调研和分析 | 验证前置条件 |
| 生成阶段产出文件 | 决定评审结果 |
| 写入产出文件 | 调度其他 Phase Skill |
| 返回执行摘要 | 修改 flow state |

### 产出验证

每次 Phase Skill 返回后，编排器必须验证：

```
1. 产出文件路径正确（参见 phase-mapping.md 中的 output artifacts）
2. 产出文件存在（使用 Bash test -f）
3. 产出文件非空（使用 Bash test -s）
4. 如果验证失败 → 输出错误报告，停止流程
```

### 状态更新规则

| 当前阶段 | 推进到 | 更新动作 |
|---------|--------|---------|
| 产物阶段完成 | 下一评审阶段 | `current_phase` 推进，前一阶段状态 `completed` |
| 评审阶段通过 | 下一产物阶段 | `current_phase` 推进，评审阶段状态 `approved` |
| 评审阶段不通过 | 退回产物阶段 | `current_phase` 回退，产物阶段状态 `in_progress` |
| 条件跳过 | 跳过阶段 | 被跳过阶段状态 `skipped`，`current_phase` 推进 |
| P13 完成 | 流程结束 | `status: 已完成`，输出摘要 |

---

## 流程状态管理

### 位置

```
slide-deck/{topic-slug}/流程状态.md
```

### 详细规格

参见 `references/flow-state-spec.md` 获取完整的 YAML frontmatter 规格和状态表定义。

### 快速参考

```yaml
---
project_name: {项目名称}
source_material: {源素材路径}
canvas_format: "1280x720"
rendering_mode: {html|image}
current_phase: P1
status: in_progress
yolo_mode: false
style:
  preset: {预设名称或 custom}
  texture: {clean|grid|organic|pixel|paper}
  mood: {professional|warm|cool|vibrant|dark|neutral}
  typography: {geometric|humanist|handwritten|editorial|technical}
  density: {minimal|balanced|dense|ultra-dense}
style_reference:
  type: {none|image|description}
  path: null
  description: null
audience: {初学者|一般读者|专家|管理层}
language: {en|zh|ja|...}
slide_count:
  recommended: {N}
  confirmed: {N}
image_approach: {none|user-provided|ai-generated|placeholders}
review:
  skip_outline: false
  skip_prompts: false
  skip_images: false
created_at: {YYYY-MM-DD HH:mm}
updated_at: {YYYY-MM-DD HH:mm}
---
```

---

## Phase 映射速查

参见 `references/phase-mapping.md` 获取完整的阶段映射表，包含输入/输出产物路径和前置条件。

| 阶段 | Phase Skill | 核心产出 | 前置条件 |
|------|-------------|---------|---------|
| P1 | `ideal-ppt-research` | `analysis.md` | source material 存在 |
| P3 | `ideal-ppt-strategist` | `strategy.md` | P1 completed |
| P5 | `ideal-ppt-outline` | `outline.md` | P4 approved |
| P7 | `ideal-ppt-prompt` | `prompts/*.md` | P5 completed |
| P9 | `ideal-ppt-image` | `images/*.png` | P7 completed, image_approach=ai-generated |
| P11 | `ideal-ppt-executor` / `ideal-ppt-image-executor` | `html_output/*.html` 或 `images_output/*.png` | P7 completed, 由 rendering_mode 决定 |
| P13 | `ideal-ppt-export` | `.pptx` + `.pdf` | P11 completed |

---

## 评审阶段处理

### 人工模式（默认，yolo_mode: false）

```
1. 产物阶段完成后 → 停下来，展示产出摘要
2. 评审阶段：
   a) 展示评审摘要
   b) 如果是 P4（BLOCKING）→ 强调必须明确批准
   c) 展示选项：
      - "通过" → 推进下一阶段
      - "通过，启用 YOLO" → 推进并启用 YOLO
      - "启用 YOLO" → 启用 YOLO 模式
      - 其他反馈 → 记录并等待进一步指示
```

**YOLO 模式提示（每次评审阶段必须展示）**：

```
评审摘要已生成。
请选择后续处理方式：
  1. [通过] — 继续下一阶段（保持手动模式）
  2. [通过，启用 YOLO] — 通过并启用 YOLO 模式，后续自动推进
  3. [启用 YOLO] — 不通过评审但启用 YOLO 模式，让 AI 自动迭代
  4. [其他反馈] — 提供具体修改意见
```

### YOLO 模式（yolo_mode: true）

- 评审阶段由 `ideal-yolo` 自动处理
- **P4 BLOCKING 关卡**：即使 YOLO 模式下，P4 仍执行完整评审流程
- 其他评审关卡：根据 `review` 配置可自动通过
- 熔断 → 停止循环，输出报告，等待人工介入

---

## 使用方式

### 命令格式

```bash
# 完整流水线
/ideal-ppt-workflow content.md

# 自动推进模式
/ideal-ppt-workflow content.md --yolo

# 从指定阶段恢复
/ideal-ppt-workflow slide-deck/topic/ --from P5

# 重新生成指定幻灯片
/ideal-ppt-workflow slide-deck/topic/ --regenerate 3

# 仅生成大纲
/ideal-ppt-workflow content.md --outline-only

# 生成大纲+提示词，跳过执行
/ideal-ppt-workflow content.md --prompts-only

# 从现有提示词生成 HTML 幻灯片
/ideal-ppt-workflow slide-deck/topic/ --html-only

# 从现有提示词生成图片幻灯片
/ideal-ppt-workflow slide-deck/topic/ --image-only
```

### 命令行选项

| 选项 | 描述 |
|------|------|
| `--yolo` | 启用 YOLO 模式，自动推进所有阶段 |
| `--from P{N}` | 从指定阶段恢复执行 |
| `--regenerate {N}` | 重新生成指定幻灯片（需已有 prompts） |
| `--style <名称>` | 指定视觉风格预设 |
| `--audience <类型>` | 指定目标受众 |
| `--lang <代码>` | 指定输出语言 |
| `--slides <数量>` | 指定幻灯片数量 |
| `--outline-only` | 仅执行 P1-P5，到大纲为止 |
| `--prompts-only` | 执行到 P7，到提示词为止 |
| `--html-only` | 从 P11 开始，从现有提示词生成 HTML 幻灯片 |
| `--image-only` | 从 P11 开始，从现有提示词生成图片幻灯片 |
| `--rendering-mode <模式>` | 渲染路径：html（默认）或 image |
| `--style-ref <路径>` | 风格参考图片路径（image 模式） |
| `--image-approach <方式>` | 图像策略：none / user-provided / ai-generated / placeholders |

### 典型流程

#### 全新创建

```
/ideal-ppt-workflow content.md
  → P1 需求研究 → P2 确认 → P3 策略规划 → P4 策略确认 [BLOCKING]
  → P5 大纲生成 → P6 大纲审核 → P7 提示词工程 → P8 提示词审核
  → P9 图像生成（条件） → P10 图像审核（条件）
  → P11 幻灯片执行（html/image） → P12 幻灯片审核 → P13 导出交付
```

#### 从中断恢复

```
# 假设在 P7 中断
/ideal-ppt-workflow slide-deck/my-topic/ --from P7
  → 读取 流程状态.md → current_phase = P7
  → 验证 P1-P6 产出存在
  → 从 P7 继续
```

#### 快速迭代

```
# 修改第 3 页提示词后重新生成
/ideal-ppt-workflow slide-deck/my-topic/ --regenerate 3
  → 读取 prompts/03-slide-xxx.md
  → 调用 ideal-ppt-executor（html）或 ideal-ppt-image-executor（image）生成对应文件
  → 调用 ideal-ppt-export 重新导出
```

---

## 目录结构

```
slide-deck/{topic-slug}/
├── 流程状态.md              ← flow state
├── source-{slug}.{ext}      ← 源素材
├── analysis.md              ← P1 产出：需求分析
├── strategy.md              ← P3 产出：策略规划
├── outline.md               ← P5 产出：幻灯片大纲
├── prompts/                 ← P7 产出：生成提示词（html/image 两种模板）
│   ├── 01-slide-cover.md
│   ├── 02-slide-intro.md
│   └── ...
├── images/                  ← P9 产出：AI 生成图像（条件）
│   ├── 01-hero.png
│   └── ...
├── html_output/             ← P11 产出（rendering_mode=html）
│   ├── 01-slide-cover.html
│   └── ...
├── images_output/           ← P11 产出（rendering_mode=image）
│   ├── 01-slide-cover.png
│   └── ...
├── slides_png/              ← HTML 截图（html 模式导出用）
│   └── ...
├── {topic-slug}.pptx        ← P13 产出：PowerPoint
└── {topic-slug}.pdf         ← P13 产出：PDF
```

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 源素材不存在 | 停止，报告错误，提示用户提供 |
| 前置产出缺失 | 停止，报告缺失文件，建议从正确阶段恢复 |
| Phase Skill 返回失败 | 停止，报告错误，保留当前状态 |
| 产出验证失败（文件不存在或为空） | 停止，报告验证失败，不更新状态 |
| YOLO 熔断 | 停止循环，输出熔断报告，等待人工介入 |
| 条件跳过冲突 | P9 被跳过但 `--regenerate` 指向图像相关幻灯片 → 报告冲突 |

---

## 质量检查清单

### 每次阶段推进必须验证

- [ ] flow state 文件格式正确（YAML frontmatter 有效）
- [ ] 阶段序列完整性：下一个阶段序号 <= current_phase + 1
- [ ] 前置条件已满足（前置产出文件存在且非空）
- [ ] Phase Skill 已被正确调用
- [ ] 产出文件已写入正确路径
- [ ] 产出内容非空
- [ ] `current_phase` 已正确推进
- [ ] `updated_at` 已更新为当前时间
- [ ] 条件跳过逻辑已正确执行（P9/P10）

### YOLO 模式额外检查

- [ ] 阶段完成后立即回到循环起点，不停下来
- [ ] 熔断信号被正确识别并处理
- [ ] P4 BLOCKING 关卡已执行完整评审
- [ ] 流程完成时输出完整执行摘要

### 通用质量要求

- [ ] 主智能体未直接执行任何阶段内工作
- [ ] 评审阶段已展示 YOLO 选项提示
- [ ] P4 BLOCKING 关卡未被跳过
- [ ] 产出文件备份规则已执行（同名文件先备份再覆盖）
