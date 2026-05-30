---
name: ideal-ppt-image
description: Use when P8 prompt review is completed AND design-spec image_approach is "ai-generated". Generates AI images for slide assets. Triggered by ideal-ppt-workflow at P9 (conditional).
---

# Ideal PPT Image (P9)

图像生成器 — 根据设计规范中的 Image Resource List 生成 AI 图片资源。

## 角色定义

| 属性 | 值 |
|------|-----|
| 角色 | Image Generator |
| 触发条件 | design-spec.md 中 image_approach == "ai-generated" |
| 输入工件 | `design-spec.md`（含 Image Resource List）|
| 输出工件 | `images/*.png` |

## Gate 检查

- `design-spec.md` 存在
- Image Resource List 中有 status == "pending generation" 的条目
- P8 评审已完成（或 P10 如果跳过了 P9/P10）

## 工作流程

### Step 1: 提取待生成图像

从 design-spec.md 的 Image Resource List 中提取所有 status == "pending generation" 的条目。每个条目包含：
- filename（目标文件名）
- dimensions（尺寸）
- aspect_ratio（纵横比）
- type（Background / Photography / Illustration / Diagram / Decorative Pattern）
- purpose（用途说明）
- generation_description（生成描述）

### Step 2: 生成优化的图像提示词

根据图像类型，使用对应的提示词模板（见 `references/image-generation-guide.md`）：
- Background → 抽象渐变，低对比度，预留文字区域
- Photography → 真实场景，专业光影
- Illustration → 扁平矢量，简洁线条
- Diagram → 流程图/架构图风格
- Decorative Pattern → 微妙纹理，辅助装饰

### Step 3: 生成图像

使用可用的 AI 图像生成工具：
- OpenAI `gpt-image-2`（默认推荐）
- Gemini API（仅在参考图或环境约束需要时备选）
- 其他可用工具

生成时注意：
- 匹配 design-spec 中的色彩方案
- 匹配纵横比要求
- 保持风格统一
- 如果提供参考图，仅继承背景/风格/模板节奏，不复制旧文字、logo、水印、页码

### Step 4: 保存到 images/

将生成的图片保存到 `images/` 目录，文件名与 design-spec 中的 filename 一致。

## 图像类型说明

| 类型 | 适用场景 | 提示词要点 |
|------|---------|-----------|
| Background | 封面/章节页全页背景 | 抽象、渐变、低对比度、预留文字区域 |
| Photography | 真实场景、人物、产品 | 专业摄影、合理光影、高分辨率 |
| Illustration | 扁平设计、矢量风格、概念图 | 扁平矢量、简洁线条、配色方案匹配 |
| Diagram | 流程图、架构图、概念关系 | 技术图表、清晰线条、标注 |
| Decorative Pattern | 局部装饰、纹理、边框 | 微妙、含蓄、辅助元素 |

## 跳过条件

当以下任一条件成立时，P9/P10 自动标记为 completed：
- design-spec.md 中 image_approach == "none"
- design-spec.md 中 image_approach == "user-provided"
- design-spec.md 中 image_approach == "placeholders"
- Image Resource List 中没有 "pending generation" 条目

## 完成标记

```markdown
## ✅ P9 图像生成完成
- [x] 所有 pending 图像已生成
- [x] 图片保存至 images/
- [x] 文件名与 design-spec 一致
- [ ] **Next**: 进入 P10 图像评审
```
