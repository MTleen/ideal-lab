---
name: ideal-ppt-outline
description: Use when P3 strategy review is completed and content outline generation phase begins. Triggered by ideal-ppt-workflow at P5.
---

# Ideal PPT Outline (P5)

内容架构师 — 使用金字塔原理和 Bento Grid 布局方法论构建幻灯片大纲。

## 角色定义

| 属性 | 值 |
|------|-----|
| 角色 | Content Architect |
| 前置阶段 | P4 策略评审完成 |
| 输入工件 | `research.md` + `design-spec.md` |
| 输出工件 | `outline.md` |
| 核心方法论 | 金字塔原理 + Bento Grid 卡片规划 |

## Gate 检查

进入此阶段前必须验证：
- `research.md` 存在且非空
- `design-spec.md` 存在且非空
- P4 评审状态为 `approved`

## 工作流程

### Step 1: 读取输入

读取 `research.md`（需求调研结果）和 `design-spec.md`（设计规范）。

### Step 2: 构建叙事流程

基于 research.md 的核心信息，设计完整的演示叙事结构：

```
开场（1-2 页）
  ├── Hook: 引人入胜的开场
  ├── Context: 背景铺垫
  └── Preview: 预告核心内容

主体（N 页）
  ├── 模式 A: 问题 → 解决方案
  ├── 模式 B: SCR（情境 → 冲突 → 答案）
  ├── 模式 C: What / Why / How
  ├── 模式 D: 时间线叙事
  └── 模式 E: 并列对比

结尾（1-2 页）
  ├── Synthesis: 核心观点总结
  ├── CTA: 行动号召
  └── Close: 令人印象深刻的收尾
```

### Step 3: Bento Grid 卡片分解

为每页幻灯片规划 Bento Grid 卡片布局：

1. 确定每页的核心内容块
2. 将每个内容块映射为一种卡片类型
3. 规划卡片的尺寸和排列方式
4. 确保视觉层级通过卡片大小体现

### Step 4: 生成 STYLE_INSTRUCTIONS

从 `design-spec.md` 提取视觉参数，生成统一的 STYLE_INSTRUCTIONS 块：
- Design Aesthetic
- Background
- Typography
- Color Palette（含 HEX 值）
- Visual Elements
- Density Guidelines
- Style Rules（Do / Don't）

### Step 5: 输出 outline.md

保存为 `outline.md`，遵循 `references/outline-template.md` 格式。

## 大纲结构规范

### Header 元数据

```yaml
topic: {主题}
style: {预设名称或 custom}
dimensions:
  texture: {纹理}
  mood: {色调}
  typography: {字体风格}
  density: {密度}
audience: {受众}
language: {语言}
slide_count: {页数}
date: {日期}
```

### STYLE_INSTRUCTIONS 块

所有视觉决策的唯一来源。每页提示词直接复制此块，不再重新读取风格文件。

### 幻灯片模板

**封面页**：
```
## Slide 1: {标题}
- Type: cover
- Title: {主标题}
- Subtitle: {副标题}
- Visual: {视觉描述}
- Layout: title-hero
```

**内容页**：
```
## Slide N: {标题}
- Type: content
- Narrative Goal: {叙事目标}
- Bento Grid:
  - Card 1 (large, left): {标题} — {具体内容}
  - Card 2 (small, right-top): {标题} — {具体内容}
  - Card 3 (small, right-bottom): {标题} — {具体内容}
- Visual: {视觉描述}
- Layout: {布局名称}
```

**封底页**：
```
## Slide N: {标题}
- Type: back-cover
- Summary Message: {核心总结信息}
- CTA: {行动号召}
- Visual: {视觉描述}
- Layout: title-hero
```

## 文件命名规则

- 格式：`NN-slide-{slug}.svg`
- NN：两位序号（01, 02, ...）
- slug：kebab-case，2-5 个词，唯一标识
- 中文内容可用拼音或英文命名

## 质量检查清单

- [ ] 每页都有明确的叙事目标
- [ ] 内容遵循金字塔原理（结论先行）
- [ ] Bento Grid 卡片规划具体
- [ ] STYLE_INSTRUCTIONS 完整且自包含
- [ ] 封面和封底有意义（非空洞模板）
- [ ] 页数在 design-spec 确认的范围内
- [ ] 所有卡片内容具体（无抽象标签）

## 完成标记

生成 outline.md 后输出：

```markdown
## ✅ P5 大纲生成完成
- [x] 叙事流程构建完成
- [x] Bento Grid 卡片规划完成
- [x] STYLE_INSTRUCTIONS 生成完成
- [x] outline.md 已保存
- [ ] **Next**: 进入 P6 大纲评审
```
