---
name: ideal-ppt-image-executor
description: Use when P8 or P10 review is completed AND rendering_mode=image in flow state. Generates slide images via AI image generation (baoyu-image-gen). Triggered by ideal-ppt-workflow at P11.
---

# ideal-ppt-image-executor

> 图片执行器 — 根据 prompts 逐页生成 PNG 幻灯片图片，每页由 AI 图像模型自主完成设计与排版

## 角色

你是图片执行器，负责将文字 prompts 逐页转化为 16:9 PNG 幻灯片图片。每页 prompt 包含完整内容素材，图像模型同时承担设计师与排版编辑的角色，自主决定布局。

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

将参考图片通过 `--ref` 参数传递给 baoyu-image-gen。图像模型基于参考图片的视觉风格生成新幻灯片。

```
baoyu-image-gen <prompt> --ar 16:9 --ref <style_reference.path>
```

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
优先：baoyu-image-gen（支持 7 个 provider，支持 --ref 参考图）
备选：其他可用的图像生成工具
```

baoyu-image-gen 支持的 provider：
- Google Gemini（推荐，原生多模态，--ref 效果最佳）
- OpenAI（DALL-E）
- Replicate（支持 --ref）
- OpenRouter（支持 --ref）
- DashScope（通义万相）
- Seedream（支持 --ref）
- Jimeng（即梦）

### Step 3: 逐页生成图片

**关键规则：一次只生成一页，不批量生成。**

每页生成流程：

```
1. 读取当前页 prompt（如 prompts/01-slide-cover.md）
2. 构建 image generation prompt：
   ---
   [Style Brief]
   视觉风格：{从 design-spec 提取}
   配色：Primary #XXXXXX / Secondary #XXXXXX / Accent #XXXXXX
   密度：{style.density}（见下方密度说明）
   {style_reference.description（如 type=description）}

   [Content]
   {完整 prompt 内容，不做裁剪或过滤}
   ---
3. 调用图像生成：
   baoyu-image-gen "<prompt>" --ar 16:9 [--ref <reference_image>]
4. 保存输出到 images_output/NN-slide-title.png
5. 确认当前页无错误后，继续下一页
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

### Step 5: 生成演讲备注

所有图片生成完成后，生成 `notes/total.md`。格式与 ideal-ppt-executor 一致：

```markdown
# 01 - 页面标题

[演讲脚本]（2-5 句话）

**要点：**
① 核心要点一
② 核心要点二

**时长：** 30s

---

# 02 - 页面标题

[Transition] 承上启下过渡语

[演讲脚本]（2-5 句话）

**时长：** 45s

---
```

### Step 6: 验证输出

逐项确认：

- [ ] 每个 prompt 文件均有对应 images_output/*.png
- [ ] 所有 PNG 文件大小 > 0
- [ ] **所有 PNG 宽高比校验通过**（16:9，±2% 以内）
- [ ] 比例异常页面已标记（如有重试失败的页面）
- [ ] 文件名按序号排列完整
- [ ] notes/total.md 已生成

---

## Prompt 结构（发送给图像模型的内容）

每个 prompt 由两部分组成，**Content 部分不做任何裁剪或过滤**，图像模型自行决定如何在画面中呈现：

```
=== Style Brief ===
视觉风格：{mood}，{texture} 质感
配色方案：主色 {Primary} / 辅色 {Secondary} / 强调色 {Accent}
字体风格：{typography}
信息密度：{density}（{density 的具体行为说明}）
{附加风格指令，如 type=description 时的文字描述}

=== Slide Content ===
{prompt 文件中的完整内容，包含标题、正文、数据、视觉描述等全部素材}
```

图像模型根据 Style Brief 的密度指令，自主决定：
- 哪些内容放在画面中
- 如何分区排版
- 文字大小与层级
- 图表/卡片/列表的布局形式

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

notes/                   # 演讲备注
  └── total.md
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
