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
├── html_output/                ← rendering_mode=html 时
│   └── NN-slide-{name}.html
├── images_output/              ← rendering_mode=image 时
│   └── NN-slide-{name}.png
├── slides_png/                 ← HTML 截图（供导出用）
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

**说明**：为每页幻灯片生成提示词。根据 `rendering_mode` 走不同分支：
- **html 模式**：生成精确布局指令（CSS Grid、字号、位置），产出基于 `references/base-prompt.md` 的 HTML 生成提示词。
- **image 模式**：生成内容简报 + 风格描述的提示词，包含该页要传达的完整素材（不做裁剪），布局由画图模型自主决定。基于 `references/base-prompt-image.md` 模板。密度由 `style.density` 控制。

两种模式均遵循 prompt 内容深度规则——提示词必须自包含，禁止抽象标签。

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

**说明**：用户审核提示词的质量和完整性。可通过 `review.skip_prompts: true` 跳过此阶段。跳过时状态设为 `auto_approved`。

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

### P11：幻灯片执行

| 字段 | 值 |
|------|-----|
| **Phase** | P11 幻灯片执行 |
| **Skill** | `rendering_mode=html` → `ideal-ppt-executor`；`rendering_mode=image` → `ideal-ppt-image-executor` |
| **Input Artifacts** | `prompts/*.md`、`outline.md`、`images/*.png`（条件） |
| **Output Artifacts** | `html_output/*.html`（html 模式）或 `images_output/*.png`（image 模式） |
| **Prerequisites** | P7 completed（P8 approved 或 auto_approved） |
| **BLOCKING** | 否 |

**说明**：根据 `rendering_mode` 走不同执行路径：
- **html 模式**（`ideal-ppt-executor`）：逐页生成独立 HTML 幻灯片（内联 CSS + 内嵌 SVG），浏览器直接渲染。
- **image 模式**（`ideal-ppt-image-executor`）：逐页调用图片生成服务，将内容简报 + 风格参考传给画图模型，模型自主决定布局。支持 `style_reference`（参考图片或风格描述）保证跨页一致性。

---

### P12：幻灯片审核（评审）

| 字段 | 值 |
|------|-----|
| **Phase** | P12 幻灯片审核 |
| **Skill** | *(无，用户直接审核)* |
| **Input Artifacts** | `html_output/*.html` 或 `images_output/*.png` |
| **Output Artifacts** | *(用户反馈)* |
| **Prerequisites** | P11 completed |
| **BLOCKING** | 否 |

**说明**：用户审核最终幻灯片的视觉效果。html 模式在浏览器中查看 HTML；image 模式查看 PNG 图片。如有问题可指定 `--regenerate {N}` 重新生成特定页面。

---

### P13：导出交付

| 字段 | 值 |
|------|-----|
| **Phase** | P13 导出交付 |
| **Skill** | `ideal-ppt-export` |
| **Input Artifacts** | `html_output/*.html`（html 模式）或 `images_output/*.png`（image 模式） |
| **Output Artifacts** | `{topic-slug}.pptx`、`{topic-slug}.pdf` |
| **Prerequisites** | P11 completed（P12 approved 或 auto_approved） |
| **BLOCKING** | 否 |

**说明**：根据 `rendering_mode` 走不同导出管线：
- **html 模式**：HTML → Playwright 截图 → python-pptx 原生元素（可编辑文本框/形状/表格）→ PPTX + PDF
- **image 模式**：PNG → 直接嵌入 PPTX（每页一张全幅图片 + 演讲备注）→ PPTX + PDF

---

## 前置条件依赖图

```
P1 ──→ P2 ──→ P3 ──→ P4 [BLOCKING] ──→ P5 ──→ P6 ──→ P7 ──→ P8
                                                     │        │
                                                     ↓        ↓
                                              P9 (条件) → P10 (条件)
                                                     │
                                                     ↓
                                    ┌──── P11 ────┐
                                    │  html/image  │
                                    └──────┬───────┘
                                           ↓
                                          P12 → P13 (html/image)
```

**P7 分支说明**：`rendering_mode` 在 P7 决定提示词类型（html 布局指令 vs image 内容简报），P11 决定执行器，P13 决定导出管线。

**关键依赖说明**：

| 依赖关系 | 说明 |
|---------|------|
| P4 → P5 | P4 BLOCKING，必须通过才能进入 P5-P13 |
| P7 → P9 | P7 completed 且 `image_approach=ai-generated` 才进入 P9 |
| P7 → P11 | P7 completed 且 P8 通过后即可进入 P11（不依赖 P9/P10） |
| P9 → P10 | P9 完成后才进入 P10，P9 跳过则 P10 也跳过 |
| P11 → P13 | P11 completed 且 P12 通过后才进入 P13 |

**注意**：P9（图像素材生成）和 P11（幻灯片执行）是并行友好的。P11 可以在 P8 通过后立即开始，无需等待 P9/P10 完成。`rendering_mode` 决定 P11 的执行器和 P13 的导出管线，但 P9/P10（辅助配图）在两种模式下都可用。

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
| P11 | `html_output/*-slide-*.html` 或 `images_output/*-slide-*.png`（至少 1 个） | `test -d html_output && ls html_output/*-slide-*.html >/dev/null 2>&1` 或 `test -d images_output && ls images_output/*-slide-*.png >/dev/null 2>&1` |
| P13 | `{topic-slug}.pptx` + `{topic-slug}.pdf` | `test -f {topic-slug}.pptx && test -f {topic-slug}.pdf` |
