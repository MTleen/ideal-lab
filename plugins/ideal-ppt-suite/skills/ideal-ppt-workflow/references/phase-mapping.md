# 阶段映射表（phase-mapping）

本文档定义 AIPPT 流水线中每个阶段的完整映射关系，包括 Phase Skill 名称、输入/输出产物路径、前置条件和 BLOCKING 标记。

---

## 基础目录

所有路径相对于 `slide-deck/{topic-slug}/` 目录。

```
slide-deck/{topic-slug}/
├── 流程状态.md
├── source-{slug}.{ext}
├── analysis.md
├── strategy.md
├── outline.md
├── prompts/
│   └── NN-slide-{name}.md
├── images/
│   └── NN-{name}.png
├── html_output/
│   └── NN-slide-{name}.html
├── slides_png/
│   └── NN-slide-{name}.png
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

---

## 完整映射表

| 字段 | 说明 |
|------|------|
| **Phase** | 阶段编号和名称 |
| **Skill** | 要调用的 Phase Skill 名称 |
| **Input Artifacts** | 本阶段需要读取的文件（必须存在才能进入） |
| **Output Artifacts** | 本阶段产出的文件（完成后必须存在） |
| **Prerequisites** | 前置条件（哪些阶段必须先完成） |
| **BLOCKING** | 是否为硬性评审关卡 |

---

### P1：需求研究

| 字段 | 值 |
|------|-----|
| **Phase** | P1 需求研究 |
| **Skill** | `ideal-ppt-research` |
| **Input Artifacts** | `source-{slug}.{ext}`（源素材文件） |
| **Output Artifacts** | `analysis.md` |
| **Prerequisites** | 无（流水线起始阶段） |
| **BLOCKING** | 否 |

**说明**：分析源素材内容，识别主题、内容信号、语言、推荐风格和幻灯片数量。产出 `analysis.md` 包含完整的分析结果和建议。

---

### P2：需求确认（评审）

| 字段 | 值 |
|------|-----|
| **Phase** | P2 需求确认 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `analysis.md` |
| **Output Artifacts** | *(用户确认信息写入 `流程状态.md`)* |
| **Prerequisites** | P1 completed |
| **BLOCKING** | 否 |

**说明**：用户审核 P1 分析结果，确认风格、受众、幻灯片数量、图像策略。编排器展示分析摘要，收集用户选择，更新 `流程状态.md` 中的 `style`、`audience`、`slide_count.confirmed`、`image_approach`、`review` 等字段。

---

### P3：策略规划

| 字段 | 值 |
|------|-----|
| **Phase** | P3 策略规划 |
| **Skill** | `ideal-ppt-strategist` |
| **Input Artifacts** | `source-{slug}.{ext}`、`analysis.md` |
| **Output Artifacts** | `strategy.md` |
| **Prerequisites** | P2 approved（用户已确认需求） |
| **BLOCKING** | 否 |

**说明**：基于确认的需求制定详细的内容策略。产出 `strategy.md` 包含叙事结构、每页幻灯片的内容分配策略、视觉风格具体参数、布局建议等。

---

### P4：策略确认（评审）**[BLOCKING]**

| 字段 | 值 |
|------|-----|
| **Phase** | P4 策略确认 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `strategy.md` |
| **Output Artifacts** | *(用户批准信息写入 `流程状态.md`)* |
| **Prerequisites** | P3 completed |
| **BLOCKING** | **是** |

**说明**：**P4 是唯一的硬性 BLOCKING 评审关卡。** 用户必须明确批准策略方向后才能进入 P5。未经 P4 批准，禁止进入 P5-P13 任何阶段。YOLO 模式下 P4 仍需通过 `ideal-yolo` 评审或用户明确批准。

---

### P5：大纲生成

| 字段 | 值 |
|------|-----|
| **Phase** | P5 大纲生成 |
| **Skill** | `ideal-ppt-outline` |
| **Input Artifacts** | `source-{slug}.{ext}`、`analysis.md`、`strategy.md` |
| **Output Artifacts** | `outline.md` |
| **Prerequisites** | P4 approved |
| **BLOCKING** | 否 |

**说明**：根据策略生成详细的幻灯片大纲。产出 `outline.md` 包含每页幻灯片的标题、内容摘要、布局类型、备注等信息。

---

### P6：大纲审核（评审）

| 字段 | 值 |
|------|-----|
| **Phase** | P6 大纲审核 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `outline.md` |
| **Output Artifacts** | *(用户反馈)* |
| **Prerequisites** | P5 completed |
| **BLOCKING** | 否 |

**说明**：用户审核幻灯片大纲结构和内容分配。可通过 `review.skip_outline: true` 跳过此阶段。跳过时状态设为 `auto_approved`。

---

### P7：提示词工程

| 字段 | 值 |
|------|-----|
| **Phase** | P7 提示词工程 |
| **Skill** | `ideal-ppt-prompt` |
| **Input Artifacts** | `source-{slug}.{ext}`、`analysis.md`、`strategy.md`、`outline.md` |
| **Output Artifacts** | `prompts/01-slide-cover.md`、`prompts/02-slide-{name}.md`、... |
| **Prerequisites** | P5 completed（P6 approved 或 auto_approved） |
| **BLOCKING** | 否 |

**说明**：为每页幻灯片生成详细的 SVG 生成提示词。产出 `prompts/*.md` 文件，每个文件包含完整的 SVG 生成指令（风格参数、内容、布局、颜色等）。遵循 prompt 内容深度规则——提示词必须自包含所有细节，禁止抽象标签。

---

### P8：提示词审核（评审）

| 字段 | 值 |
|------|-----|
| **Phase** | P8 提示词审核 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `prompts/*.md` |
| **Output Artifacts** | *(用户反馈)* |
| **Prerequisites** | P7 completed |
| **BLOCKING** | 否 |

**说明**：用户审核 SVG 生成提示词的质量和完整性。可通过 `review.skip_prompts: true` 跳过此阶段。跳过时状态设为 `auto_approved`。

---

### P9：图像生成（条件）

| 字段 | 值 |
|------|-----|
| **Phase** | P9 图像生成 |
| **Skill** | `ideal-ppt-image` |
| **Input Artifacts** | `prompts/*.md`、`outline.md` |
| **Output Artifacts** | `images/01-hero.png`、`images/02-{name}.png`、... |
| **Prerequisites** | P7 completed，`image_approach: ai-generated` |
| **BLOCKING** | 否 |
| **条件** | 仅当 `image_approach == "ai-generated"` 时执行 |

**说明**：使用 AI 图像生成模型为需要的幻灯片生成配图。根据大纲中标记需要配图的页面生成对应图像。`image_approach` 不为 `ai-generated` 时，此阶段和 P10 均被跳过（状态设为 `skipped`）。

---

### P10：图像审核（评审，条件）

| 字段 | 值 |
|------|-----|
| **Phase** | P10 图像审核 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `images/*.png` |
| **Output Artifacts** | *(用户反馈)* |
| **Prerequisites** | P9 completed |
| **BLOCKING** | 否 |
| **条件** | 仅当 `image_approach == "ai-generated"` 时执行 |

**说明**：用户审核 AI 生成的配图质量和相关性。可通过 `review.skip_images: true` 跳过。当 P9 被跳过时，P10 也随之一同跳过。

---

### P11：HTML 执行

| 字段 | 值 |
|------|-----|
| **Phase** | P11 HTML 执行 |
| **Skill** | `ideal-ppt-executor` |
| **Input Artifacts** | `prompts/*.md`、`outline.md`、`images/*.png`（条件） |
| **Output Artifacts** | `html_output/01-slide-cover.html`、`html_output/02-slide-{name}.html`、... |
| **Prerequisites** | P7 completed（P8 approved 或 auto_approved） |
| **BLOCKING** | 否 |

**说明**：根据提示词逐页生成独立 HTML 幻灯片。每页 HTML 包含内联 CSS 和内嵌 SVG，浏览器可直接渲染。如果存在 AI 生成图像（P9），通过 `<img>` 标签引用。

---

### P12：HTML 审核（评审）

| 字段 | 值 |
|------|-----|
| **Phase** | P12 HTML 审核 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `html_output/*.html` |
| **Output Artifacts** | *(用户反馈)* |
| **Prerequisites** | P11 completed |
| **BLOCKING** | 否 |

**说明**：用户审核 HTML 幻灯片的视觉效果。在浏览器中打开 HTML 文件查看实际渲染效果。如有问题可指定 `--regenerate {N}` 重新生成特定页面。

---

### P13：导出交付

| 字段 | 值 |
|------|-----|
| **Phase** | P13 导出交付 |
| **Skill** | `ideal-ppt-export` |
| **Input Artifacts** | `html_output/*.html` |
| **Output Artifacts** | `{topic-slug}.pptx`、`{topic-slug}.pdf` |
| **Prerequisites** | P11 completed（P12 approved 或 auto_approved） |
| **BLOCKING** | 否 |

**说明**：将 HTML 幻灯片通过无头浏览器截图，合并导出为 PowerPoint 和 PDF 文件。

---

## 前置条件依赖图

```
P1 ──→ P2 ──→ P3 ──→ P4 [BLOCKING] ──→ P5 ──→ P6 ──→ P7 ──→ P8
                                                     │        │
                                                     ↓        ↓
                                              P9 (条件) → P10 (条件)
                                                     │
                                                     ↓
                                              P11 → P12 → P13
                                               ↑
                                               │
                                    P7 completed 即可进入 P11
                                    （无需等待 P9/P10）
```

**关键依赖说明**：

| 依赖关系 | 说明 |
|---------|------|
| P4 → P5 | P4 BLOCKING，必须通过才能进入 P5-P13 |
| P7 → P9 | P7 completed 且 `image_approach=ai-generated` 才进入 P9 |
| P7 → P11 | P7 completed 且 P8 通过后即可进入 P11（不依赖 P9/P10） |
| P9 → P10 | P9 完成后才进入 P10，P9 跳过则 P10 也跳过 |
| P11 → P13 | P11 completed 且 P12 通过后才进入 P13 |

**注意**：P9（图像生成）和 P11（SVG 执行）是并行友好的，但在当前流水线中串行执行。P11 可以在 P8 通过后立即开始，无需等待 P9/P10 完成。如果未来需要优化性能，P9 和 P11 可以并行执行。

---

## 产出验证清单

编排器在每次 Phase Skill 返回后，按以下清单验证产出：

| 阶段 | 必须存在的文件 | 验证命令 |
|------|--------------|---------|
| P1 | `analysis.md` | `test -f analysis.md && test -s analysis.md` |
| P3 | `strategy.md` | `test -f strategy.md && test -s strategy.md` |
| P5 | `outline.md` | `test -f outline.md && test -s outline.md` |
| P7 | `prompts/*.md`（至少 1 个） | `test -d prompts && ls prompts/*.md >/dev/null 2>&1` |
| P9 | `images/*.png`（至少 1 个） | `test -d images && ls images/*.png >/dev/null 2>&1` |
| P11 | `html_output/*-slide-*.html`（至少 1 个） | `test -d html_output && ls html_output/*-slide-*.html >/dev/null 2>&1` |
| P13 | `{topic-slug}.pptx` + `{topic-slug}.pdf` | `test -f {topic-slug}.pptx && test -f {topic-slug}.pdf` |
