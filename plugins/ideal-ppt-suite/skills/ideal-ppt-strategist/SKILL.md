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

### Phase 2: 八大确认 (Eight Confirmations)

**关键原则：八大确认必须一次性打包呈现给用户，等待用户整体确认后再进入生成阶段。**

向用户呈现以下 8 项确认，每项附基于研究成果的推荐值：

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

#### d. 风格目标 (Style Objective)

提供两种选择模式：

**模式 A：17 种预设风格**（参见 `references/dimensions/presets.md`）

| 编号 | 预设名称 | 典型场景 |
|------|----------|----------|
| 1 | 蓝图风格 | 技术架构、系统设计 |
| 2 | 黑板风格 | 教育、概念讲解 |
| 3 | 商务风格 | 企业汇报、商务提案 |
| 4 | 极简风格 | 高端展示、品牌介绍 |
| 5 | 手绘风格 | 创意提案、故事叙述 |
| 6 | 水彩风格 | 艺术、情感表达 |
| 7 | 暗色风格 | 科技、前沿主题 |
| 8 | 块状风格 | 信息密集、数据展示 |
| 9 | 杂志风格 | 品牌、生活方式 |
| 10 | 图表风格 | 数据分析、报告 |
| 11 | 动画风格 | 故事、流程展示 |
| 12 | 架构图风格 | 技术方案、系统设计 |
| 13 | 像素风格 | 游戏、创意 |
| 14 | 论文风格 | 学术、研究 |
| 15 | 插画风格 | 教育、创意 |
| 16 | 复古报纸风 | 怀旧、主题展示 |
| 17 | 高密度信息图 | 综合报告、总结 |

**模式 B：自定义四维组合**（参见 `references/dimensions/` 目录）

| 维度 | 可选项 |
|------|--------|
| Texture (质感) | clean / grid / organic / pixel / paper |
| Mood (氛围) | professional / warm / cool / vibrant / dark / neutral |
| Typography (字体) | geometric / humanist / handwritten / editorial / technical |
| Density (密度) | minimal / balanced / dense |

**风格选择决策树**（基于 ppt-master）：

```
演示目的是什么？
├─ 重图像展示/推广宣传 → General Versatile（通用多能）
├─ 数据分析/进度汇报 → General Consulting（通用咨询）
└─ 战略决策/说服影响 → Top Consulting（顶级咨询）
    ↓
根据决策树结果映射到对应预设：
├─ General Versatile → 商务风格 / 极简风格
├─ General Consulting → 图表风格 / 块状风格
└─ Top Consulting → 商务风格 / 论文风格
```

**推荐逻辑**：结合使用场景 + 受众 + 目的，推荐 1-2 个预设并说明理由。

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

#### h. 图片使用 (Image Usage)

| 选项 | 说明 |
|------|------|
| None | 不使用图片，纯图形设计 |
| User-provided | 用户提供图片，需提供路径 |
| AI-generated | AI 生成配图 |
| Placeholders | 占位图，后续替换 |

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
| `dimensions/presets.md` | 17 种预设风格映射 |
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
| 无法确定推荐值 | 提供所有选项供用户选择，不设默认值 |

---

## 使用示例

```
用户已完成 P1 研究，主题为"2026年Q1销售业绩汇报"
→ 读取 research.md
→ 解读：内部汇报、数据驱动、面向管理层
→ 打包呈现八大确认：
  a. 画幅：推荐 PPT 16:9（内部会议投影）
  b. 页数：8-12页（4个分析维度 + 开结尾）
  c. 受众：管理层 / 数据分析目的
  d. 风格：推荐"图表风格"（数据密集型）
  e. 配色：咨询蓝系（#005587 / #2196F3 / #FF9800）
  f. 图标：Built-in Library
  g. 字体：MiSans + Liter
  h. 图片：None（数据为主）
→ 用户确认
→ 生成 design-spec.md
```
