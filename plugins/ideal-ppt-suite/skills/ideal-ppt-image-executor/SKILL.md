---
name: ideal-ppt-image-executor
description: Use when P8 or P10 review is completed AND rendering_mode=image in flow state. Generates slide images via gpt-image-2-compatible AI image generation. Triggered by ideal-ppt-workflow at P11.
---

# ideal-ppt-image-executor

> 图片执行器 — 根据 prompts 逐页生成 PNG 幻灯片图片，每页由 gpt-image-2 生成完整 PPT 信息图

## 角色

你是图片执行器，负责将 P7 生成的完整页面 prompt 逐页转化为 16:9 PNG 幻灯片图片。P7 prompt 已经包含内容、风格、区块级布局和质量合同；执行器不得把它压缩成简短描述。

## 前置条件（Gate）

执行前必须确认：

```
prompts/*.md           # 各页内容简报（含完整素材）
design-spec.md         # 设计参数规范
流程状态.md            # rendering_mode == "image"
```

并确认 P8（prompt 审阅）或 P10（图像审阅）阶段已完成。

---

## 设计参数确认

从 `design-spec.md` 和 `流程状态.md` 提取以下参数：

| 参数 | 说明 | 来源 |
|------|------|------|
| Canvas 尺寸 | 宽高比 16:9 | design-spec |
| 主色 Primary | HEX 值 | design-spec |
| 辅色 Secondary | HEX 值 | design-spec |
| 强调色 Accent | HEX 值 | design-spec |
| 字体方案 | 标题 / 正文风格 | design-spec |
| style.density | minimal / balanced / dense / ultra-dense | 流程状态.md |
| style_reference.type | none / image / description | 流程状态.md |
| style_reference.path | 参考图片路径（type=image 时） | 流程状态.md |
| style_reference.description | 风格文字描述（type=description 时） | 流程状态.md |

---

## 风格参考处理

根据 `style_reference.type` 决定风格传递方式：

### type=none

仅通过 prompt 文字中的 Style Brief 段落传递风格信息。无参考图片。

### type=image

将参考图片通过 `--ref` 参数传递给图像生成工具。参考图片用于风格、背景、母版或版式锚定，不能复制旧文字、logo、水印、页码。

```
baoyu-image-gen <prompt> --provider openai --model gpt-image-2 --size 1792x1024 --ref <style_reference.path>
```

### freeform layout sketch

当 prompt 指定 `Layout freedom: freeform editorial`，且上一版 judgment 判定“网格残留”不通过时，优先使用或生成一张自由排版布局草图作为参考图：

- 草图只包含抽象区块、平直错位区域、数据飘带、信息簇大小差异和阅读路径。
- 默认草图应使用平直几何自由排版：不等宽/不等高区块、错位色带、数据条、括号分组、阶梯阅读路径和信息簇大小差异。
- 不要默认生成不规则曲线边框、泡泡轮廓、lasso 形状或 contour map；只有用户明确要求生态地图、有机地图或轮廓能力图时才使用。
- 草图不能包含可复制的旧文字、logo、水印、页码或最终数据。
- 最终生成仍以 P7 prompt 的文字和数据为准，参考图只作为 composition reference。
- 生成命令必须传入 `--ref <layout_sketch_path>`，并在 `images_output/judgment.md` 记录参考图角色。

### type=description

将 `style_reference.description` 嵌入每个 prompt 的 Style Brief 段落，作为文字风格指令。

---

## 执行流程

### Step 1: 读取源文件并提取参数

```
1. 读取 流程状态.md → 确认 rendering_mode=image，提取 style_reference 配置
2. 读取 design-spec.md → 提取配色、字体、排版参数
3. 读取 prompts/*.md → 获取所有 prompt 文件列表
```

### Step 2: 发现图像生成工具

检测可用的图像生成 skill：

```
优先：baoyu-image-gen + OpenAI provider + gpt-image-2
备选：其他可用的图像生成工具
```

默认模型策略：
- 首选：`gpt-image-2`
- 必须显式传入模型参数或环境变量，不依赖工具默认值
- 仅当 gpt-image-2 不可用时，才回退到其他支持 16:9 和参考图的模型，并在报告中说明

### Step 3: 逐页生成图片

**关键规则：一次只生成一页，不批量生成。**

每页生成流程：

```
1. 读取当前页 prompt（如 prompts/01-slide-cover.md）
2. 构建 image generation prompt：
   - 原样保留 prompts/NN-slide-*.md 的完整内容
   - 不摘要、不裁剪、不重写为短 Style Brief
   - 在末尾追加 EXECUTION ADDENDUM（见下方）
3. 调用图像生成：
   baoyu-image-gen "<prompt>" --provider openai --model gpt-image-2 --size 1792x1024 [--ref <reference_image>]
4. 保存输出到 images_output/NN-slide-title.png
5. 确认当前页无错误后，继续下一页
```

OpenAI / gpt-image-2 执行注意：
- 当前工具链中 `--ar 16:9` 可能被映射为 1536x1024，不能满足 16:9 gate。
- 使用 `--size 1792x1024` 作为 gpt-image-2 的默认横版尺寸；该比例为 1.7500，落在 16:9 ±2% 容差内。
- 如果图像工具提示 OpenAI provider 忽略 `--ref`，必须在 judgment 中记录“composition reference 未生效”。这种情况下不要声称已经完成 reference-conditioned freeform 测试。

#### EXECUTION ADDENDUM（每页末尾追加）

```
Generate one finished 16:9 PPT slide image.
Use gpt-image-2 quality: crisp Chinese text, high information density, polished enterprise infographic.
Do not simplify this into a poster, three-card layout, icon collage, or decorative illustration.
Preserve required content, data, labels, and logic from the prompt.
Follow the specified composition archetype and style reference.
If a reference image is provided, use it only for background/template/style rhythm; do not copy old text, logo, watermark, page number, or unrelated charts.
Do not render prompt metadata such as slide_number, slide_type, target_filename, or rendering_mode as visible slide content.
```

### Step 3.5: 宽高比校验（每页必检）

每张图片生成后，**立即**校验宽高比是否符合 16:9（误差 ±2% 以内通过）。

```bash
# 使用 Python + Pillow 读取图片尺寸并校验
python3 -c "
from PIL import Image
import sys
img = Image.open(sys.argv[1])
w, h = img.size
ratio = w / h
expected = 16 / 9  # ≈ 1.7778
tolerance = 0.02   # ±2%
if abs(ratio - expected) / expected > tolerance:
    print(f'FAIL: {sys.argv[1]} ratio={ratio:.4f} expected={expected:.4f} size={w}x{h}')
    sys.exit(1)
else:
    print(f'OK: {sys.argv[1]} ratio={ratio:.4f} size={w}x{h}')
" images_output/NN-slide-title.png
```

**校验失败处理**：

| 情况 | 处理 |
|------|------|
| 比例偏差 > 2% 但 < 10% | 记录警告，继续生成下一页，最终汇总报告 |
| 比例偏差 ≥ 10%（如 1:1 正方形） | 标记该页为失败，尝试重新生成（最多重试 1 次） |
| 重试后仍失败 | 跳过该页，在最终报告中标记为需人工处理 |

**校验规则**：
- 目标比例：16:9（≈1.7778）
- 允许范围：1.7422 ~ 1.8133（±2%）
- 检查时机：每张图片生成后立即校验，不等到最后批量检查
- 校验工具：Python Pillow（`from PIL import Image`），或 `sips -g pixelWidth -g pixelHeight`（macOS）

### Step 4: 渐进式风格锚定（可选）

启用条件：style_reference.type != none 且已生成至少 1 页。

```
第 1 页：使用原始 --ref（如存在）生成
第 2 页起：将上一页生成结果作为额外 --ref，与原始参考图合并传递
  → 逐步锚定风格一致性
```

此策略确保即使参考图与幻灯片场景不完全匹配，后续页面仍保持视觉连贯。

### Step 5: 验证输出

逐项确认：

- [ ] 每个 prompt 文件均有对应 images_output/*.png
- [ ] 所有 PNG 文件大小 > 0
- [ ] **所有 PNG 宽高比校验通过**（16:9，±2% 以内）
- [ ] 比例异常页面已标记（如有重试失败的页面）
- [ ] 每页完成视觉 judgment（见下方）
- [ ] 文件名按序号排列完整

### Step 5.5: 视觉 Judgment（每页必写）

图片模式不能只检查文件存在和宽高比。每页生成后必须写入 `images_output/judgment.md`，逐页判断：

| 维度 | 通过标准 |
|------|----------|
| 信息密度 | dense 页面至少 8 个有效信息单元，ultra-dense 页面至少 10 个；每个单元有真实内容，并至少包含一个微表格/指标矩阵/4+ 行清单/迷你图表 |
| PPT 感 | 像完整企业 PPT 页，不像海报、插画、社媒图或粗糙草稿 |
| 设计感 | 不能像线框图；至少有浅色填充面、色带、数据条、迷你图表或填充型模块作为主要视觉 |
| 反单调 | controlled editorial grid / rectilinear editorial map 页必须有明确主证据块、2-4 个辅助证明块、6-10 个微证据碎片，并混合至少 5 种信息形态；不得让大部分模块都是同尺寸同样式矩形卡片 |
| 标题处理 | 不得让所有模块都使用相同的全宽蓝色标题条；主模块、辅助模块、微证据应混合蓝色标题条、小 tab、inline caption、badge、左侧旗标或 bracket label |
| 构图 | 遵循 prompt 指定的 layout freedom 和 composition archetype；若为 freeform editorial，不能退回等宽列、同尺寸卡片矩阵、固定侧栏模板或“顶部流程 + 中部卡片 + 底部行动条”模板，必须有清晰焦点、信息簇和视觉动线 |
| 网格残留 | freeform editorial 页不能出现 3 个以上同样式 KPI 卡片竖排、4 个以上同样式流程节点横排、大右侧栏、全宽底栏，且不能一眼看出 dashboard 网格 |
| 字体 | 中文标题、正文、标签、数据均可读，无伪文字或乱码 |
| 风格 | scientific 或 china-telecom 风格一致；参考图只影响风格，不复制旧内容 |
| 事实 | 关键数据、维度、步骤、结论与 prompt 一致，无编造 |

若 judgment 判定为不通过，优先修改对应 `prompts/NN-slide-*.md` 或上游 skill/reference 后重新生成；不得把最终 PNG 作为主要手工修补对象。

---

## Prompt 结构（发送给图像模型的内容）

每个 prompt 由完整 P7 页面 prompt + 执行补充组成。执行器只能追加约束，不得降级或摘要：

```
=== Style Brief ===
视觉风格：scientific 或 china-telecom
配色方案：主色 {Primary} / 辅色 {Secondary} / 强调色 {Accent}
字体风格：{typography}
信息密度：{density}（{density 的具体行为说明}）
参考图指令：{style_reference.path / description，如有}

=== Slide Content ===
{prompt 文件中的完整内容，包含标题、正文、数据、layout freedom、composition archetype、信息单元、视觉动线、区块级布局等全部素材}

=== Execution Addendum ===
{gpt-image-2 质量合同与参考图限制}
```

图像模型根据 prompt 中的内容和区块级布局进行视觉细化：
- 不能擅自删除 required 内容
- 不能把复杂页降级成 3 个大卡片
- 可以优化区域比例、对齐、局部文字换行、图表细节和视觉层级
- 可以在不改变事实的前提下压缩冗余措辞

---

## 密度级别与图像模型行为

| density | 图像模型行为 | 适用场景 |
|---------|-------------|---------|
| minimal | 只呈现核心结论和关键数据，大量留白，简洁大标题 | 高管汇报、开篇/结尾页 |
| balanced | 标题 + 2-3 个关键论点，适度留白，信息层次清晰 | 通用内容页、产品介绍 |
| dense | 大部分数据点呈现，紧凑卡片布局，信息密度高 | 数据分析、方案对比 |
| ultra-dense | 所有内容打包呈现，密集排版，类似咨询 one-pager | 详细报告、技术方案 |

---

## 输出产物

```
images_output/           # 生成的幻灯片图片
  ├── 01-slide-cover.png
  ├── 02-slide-intro.png
  └── ...
```

### 文件命名规范

```
images_output/{NN}-slide-{slug}.png
```

- NN：两位数序号（01, 02, ...）
- slug：英文小写，连字符分隔，取自标题关键词
- 与 prompts/ 目录中的 prompt 文件一一对应

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| design-spec.md 缺失 | 终止执行，提示用户先完成设计规范 |
| prompts/ 目录为空 | 终止执行，提示用户先完成 P7 提示词工程 |
| rendering_mode != image | 终止执行，提示应使用 ideal-ppt-executor |
| 单张图片生成失败 | 记录错误，跳过该页，继续其余页面，最终报告失败页 |
| baoyu-image-gen 不可用 | 终止执行，提示安装 baoyu-image-gen skill |
| 参考图片路径无效 | 忽略 --ref，回退到纯文字风格描述 |
| 生成图片宽高比偏差 ≥ 10% | 自动重试 1 次，仍失败则标记跳过 |
| Pillow 未安装 | 提示 `pip install Pillow`，无法执行比例校验 |
| images_output/ 写入失败 | 检查权限，创建目录后重试 |

---

## 与其他 Skill 的关系

```
ideal-ppt-prompt (P7/P8 审阅通过)
        ↓
  ideal-ppt-image-executor (本 Skill, P11, rendering_mode=image)
        ↓
ideal-ppt-export (P13, image pipeline: images_output/*.png → PPTX)
```

| 关系 | Skill | 说明 |
|------|-------|------|
| 上游 | ideal-ppt-prompt | 生成 prompts/*.md（内容简报） |
| 上游 | ideal-ppt-strategist | 生成 design-spec.md（设计规范） |
| 平行 | ideal-ppt-executor | P11 的 HTML 模式对应物（rendering_mode=html） |
| 下游 | ideal-ppt-export | 消费 images_output/*.png 导出 PPTX/PDF |
| 编排 | ideal-ppt-workflow | 负责调度本 Skill，管理流程状态 |
