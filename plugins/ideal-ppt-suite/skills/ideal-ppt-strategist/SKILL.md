---
name: ideal-ppt-strategist
description: Use when P1 research review is completed and strategy/design specification phase needs to begin. Triggered by ideal-ppt-workflow at P3.
---

# ideal-ppt-strategist

## 角色定义

**策略规划师 (Strategy Planner)**

接收 P1 研究成果，执行八大确认协议，输出完整的设计规格文档。

## 前置门控

| 检查项 | 条件 |
|--------|------|
| P1 产物 | `research.md` 存在且已完成内容填充 |
| P2 评审 | 用户已确认研究内容，评审状态为 `approved` |
| 工作目录 | 当前项目目录下可写入文件 |

若门控未通过，提示用户完成前置阶段后重试。

---

## 工作流程

### Phase 1: 研究成果解读

1. 读取 `research.md`，提取以下关键信息：
   - 主题与核心论点
   - 目标受众描述
   - 使用场景
   - 内容框架
   - 关键数据与论据
   - 用户偏好（如有）
2. 基于研究成果，生成初步策略推荐

### Phase 2: 八大确认 (Eight Confirmations) — 分阶段路由呈现

**关键原则：八大确认按依赖关系分 4 阶段呈现，不可越阶段。** 详细协议见 `references/eight-confirmations.md`。

| 阶段 | 包含项 | 呈现方式 |
|------|--------|----------|
| 阶段 1 | a 画幅 + b 页数 + c 受众与目的 | 一次性呈现 |
| 阶段 2 | **d 美业方式 + 风格** | **单独询问（路由开关）** |
| 阶段 3 | e 配色 + f 图标 + g 字体 | 一次性呈现 |
| 阶段 4 | **h 图片使用** | **仅 d=html-mode 时才问，d=image-mode 时跳过** |

**核心约束**：
- d 不可与 e/f/g 批量问，必须在阶段 2 单独出现
- d=image-mode 时 h 严格不出现（每页即一张图，无"图片形式"概念）
- d=html-mode 时 h 正常出现，按 None/User-provided/AI-generated/Placeholders 四选一

#### a. 画幅格式 (Canvas Format)

| 选项 | 比例 | 适用场景 |
|------|------|----------|
| PPT 16:9 | 1920×1080 | **默认**，会议演示、投影 |
| PPT 4:3 | 1024×768 | 传统投影、兼容旧设备 |
| XHS (小红书) | 1080×1440 | 社交媒体竖版图文 |
| Story (故事) | 1080×1920 | Instagram/微信 Stories |
| Square (方形) | 1080×1080 | 社交媒体方图 |
| WeChat Header (微信头图) | 900×383 | 微信公众号头图 |

**推荐逻辑**：根据 research.md 中的使用场景自动推荐。无明确场景时默认 PPT 16:9。

#### b. 页数范围 (Page Count Range)

基于内容框架估算页数：
- 开场（1-2页）
- 目录/过渡（1页）
- 核心章节（每章节 2-5 页）
- 结尾（1-2页）

呈现推荐范围 `[min, max]`，说明计算依据，询问用户确认或调整。

#### c. 目标受众与目的 (Target Audience & Purpose)

从 research.md 提取并确认：
- **受众画像**：初学者 / 从业者 / 专家 / 高管 / 混合
- **演示目的**：教育传授 / 方案汇报 / 数据分析 / 产品发布 / 战略决策 / 培训 / 说服
- **认知负荷等级**：低（需引导） / 中（可自主） / 高（深度分析）

#### d. 美业方式 + 风格目标 (Render Mode + Style) — ⚠️ 路由点

> **本项单独询问，是阶段 4 (h) 是否触发的开关。**

**第一步：美业方式**

| 模式 | 说明 | 后续 |
|------|------|------|
| `image-mode` | 每页由 AI 生成一张完整大图，图就是页 | **跳过 h** |
| `html-mode` | 每页用 HTML 排版（SVG/占位符/排版），图只是页内元素 | **继续问 h** |

**美业方式推荐**：
- 内容以视觉/图为主（产品发布、品牌宣传、故事叙述）→ `image-mode`
- 内容以数据/方案/结构为主（论文、方案汇报、培训、战略）→ `html-mode`

**第二步：风格目标**

只提供两种长期预设风格（参见 `ideal-ppt-prompt/references/dimensions/presets.md`）：

| 预设 | 中文名 | 典型场景 |
|------|--------|----------|
| scientific | 学术风格 | 论文汇报、课题答辩、研究综述、实验结果、算法/方法报告 |
| china-telecom | 电信高信息密度风格 | 中国电信、央企政企汇报、云网算力、AI、安全、DICT、行业解决方案 |

不再提供任意风格库或自定义维度组合。若用户有电信 PPT 背景图、母版截图或其他参考图片，应写入 `style_reference`，作为背景/母版/版式锚点，而不是新建风格预设。

**风格选择决策树**：

```
内容是否明显是学术/研究/论文/实验？
├─ 是 → scientific
└─ 否 → china-telecom

是否提供电信 PPT 背景图/母版/参考页？
├─ 是 → style_reference.type=image，并说明保留背景质感、红蓝比例、标题栏和空间节奏
└─ 否 → style_reference.type=none 或 description
```

**推荐逻辑**：只推荐一个主预设，并说明为什么不是另一个预设。

#### e. 配色方案 (Color Scheme)

遵循 60-30-10 规则：
- **主色 (Primary, 60%)**：背景、大面积色块
- **辅助色 (Secondary, 30%)**：标题、图形元素
- **强调色 (Accent, 10%)**：按钮、重点标注、数据高亮

提供以下信息：
1. 基于 research.md 内容类型的推荐配色（参见 `references/color-knowledge-base.md`）
2. 每个颜色的 HEX 值
3. 渐变定义（如适用）
4. 中性色层级（文字色 / 次要文字 / 分割线）

用户可接受推荐或提供自定义 HEX 值。

#### f. 图标使用 (Icon Usage)

| 选项 | 说明 | 适用场景 |
|------|------|----------|
| Emoji | Unicode 表情符号 | 轻松、非正式 |
| AI-Generated | AI 生成图标 | 定制化需求 |
| Built-in Library | 内置 SVG 图标库 | 专业、一致 |
| None | 不使用图标 | 极简、纯文字 |

**推荐**：默认 Built-in Library，除非用户指定。

#### g. 字体方案 (Typography Plan)

根据风格预设推荐字体组合（参见 `references/design-guidelines.md`）：

| 用途 | 中文字体 | 英文字体 |
|------|----------|----------|
| 标题 | 推荐字体 | 推荐字体 |
| 正文 | 推荐字体 | 推荐字体 |
| 强调 | 推荐字体 | 推荐字体 |

附字号层级体系（基于 24px 或 18px 基准）。

#### h. 图片使用 (Image Usage) — 仅 html-mode

> **⚠️ 条件性确认**：仅 d=html-mode 时才询问。d=image-mode 时直接跳过本项（每页即一张图，无"图片形式"概念）。

| 选项 | 说明 |
|------|------|
| None | 不使用图片，纯图形设计 |
| User-provided | 用户提供图片，需提供路径 |
| AI-generated | AI 生成配图 |
| Placeholders | 占位图，后续替换 |

**推荐**：数据密集型 → None；品牌推广型 → User-provided 或 AI-generated；通用型 → Placeholders。

---

### Phase 3: 确认与生成

1. 将八大确认结果整理为摘要表格，供用户最终确认
2. 用户确认后，基于确认结果和 `references/strategy-template.md` 模板生成 `design-spec.md`
3. 生成完成后，进入 P4 评审阶段

---

## 输出产物

| 产物 | 文件名 | 说明 |
|------|--------|------|
| 设计规格文档 | `design-spec.md` | 完整的 12 节设计规格，指导后续 PPT 生成 |

### design-spec.md 结构（12 节）

```
I.    项目信息 (Project Info)
II.   画幅规格 (Canvas Specification)
III.  视觉主题 (Visual Theme)
IV.   字体系统 (Typography System)
V.    排版原则 (Layout Principles)
VI.   图标使用规格 (Icon Usage Spec)
VII.  图表参考列表 (Chart Reference List)
VIII. 图片资源列表 (Image Resource List)
IX.   内容大纲 (Content Outline)
X.    演讲者备注要求 (Speaker Notes Requirements)
XI.   技术约束 (Technical Constraints)
XII.  设计检查清单 (Design Checklist)
```

---

## 参考文档

本技能依赖以下参考文档，位于 `references/` 目录：

| 文档 | 用途 |
|------|------|
| `eight-confirmations.md` | 八大确认详细协议与决策树 |
| `strategy-template.md` | design-spec.md 模板 |
| `color-knowledge-base.md` | 配色参考知识库 |
| `design-guidelines.md` | 设计原则与指南 |
| `content-rules.md` | 内容与风格规则 |
| `dimensions/presets.md` | scientific / china-telecom 两种预设映射 |
| `dimensions/texture.md` | 质感维度选项 |
| `dimensions/mood.md` | 氛围维度选项 |
| `dimensions/typography.md` | 字体维度选项 |
| `dimensions/density.md` | 密度维度选项 |

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| research.md 不存在 | 提示用户先完成 P1 研究阶段 |
| research.md 内容不完整 | 基于已有信息生成推荐，标注缺失项 |
| 用户拒绝全部推荐 | 进入自由讨论模式，逐项确认 |
| 用户中途修改确认 | 允许修改，重新生成受影响的部分 |
| 无法确定推荐值 | 默认使用 `china-telecom`，并说明可切换为 `scientific` |

---

## 使用示例

```
用户已完成 P1 研究，主题为"2026年Q1销售业绩汇报"
→ 读取 research.md
→ 解读：内部汇报、数据驱动、面向管理层

【阶段 1：基础 3 问，一次性】
→ 打包呈现 a 画幅 + b 页数 + c 受众
  a. 画幅：推荐 PPT 16:9（内部会议投影）
  b. 页数：8-12页（4个分析维度 + 开结尾）
  c. 受众：管理层 / 数据分析目的
→ 用户确认

【阶段 2：路由点，单独问】
→ 单独问 d 美业方式
  d. 美业方式 + 风格：推荐 html-mode + china-telecom（数据方案型，排版优于大图）
→ 用户选 html-mode

【阶段 3：风格 3 问，一次性】
→ 打包呈现 e + f + g
  e. 配色：电信红 #C41E24 + 科技蓝 #005BAC + 深灰蓝 #25364D
  f. 图标：Built-in Library
  g. 字体：MiSans + Liter
→ 用户确认

【阶段 4：条件 h，因 d=html-mode 触发】
→ 问 h 图片使用
  h. 图片：None（数据为主）
→ 用户确认

→ 生成 design-spec.md
```

**对比示例 — 选了 image-mode**：

```
【阶段 1】a + b + c（一次性）
【阶段 2】d：用户选 image-mode
【阶段 3】e + f + g（一次性）
【阶段 4】⏭️ 跳过 h（image-mode 下每页即图，无图片形式问题）
→ 直接生成 design-spec.md
```
