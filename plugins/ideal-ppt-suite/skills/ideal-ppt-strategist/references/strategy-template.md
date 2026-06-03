# Design Specification Template — design-spec.md 模板

本文件定义 `design-spec.md` 的完整模板结构。生成时根据八大确认结果填充各节内容。

---

## 模板

```markdown
# 设计规格文档 (Design Specification)

> 本文档定义 PPT 生成的完整设计规格，所有后续生成步骤必须严格遵循本文档的约束。

---

## I. 项目信息 (Project Info)

| 字段 | 值 |
|------|-----|
| 项目名称 | {{project_name}} |
| 主题 | {{topic}} |
| 版本 | v1.0 |
| 创建日期 | {{date}} |
| 基于 | research.md v{{version}} |
| 状态 | Draft / Confirmed |

### 项目概述

{{project_overview_from_research}}

### 关键约束

- 受众：{{audience}}
- 目的：{{purpose}}
- 使用场景：{{scenario}}

---

## II. 画幅规格 (Canvas Specification)

| 参数 | 值 |
|------|-----|
| 格式 | {{canvas_format}} |
| 宽度 | {{width}}px |
| 高度 | {{height}}px |
| 比例 | {{aspect_ratio}} |
| 像素密度 | 1x (SVG 矢量) |
| 安全边距 | 上 {{margin_top}}px / 下 {{margin_bottom}}px / 左 {{margin_left}}px / 右 {{margin_right}}px |

### 内容区域

- 有效内容区域：{{content_area_width}} × {{content_area_height}}px
- 页面分割：{{grid_columns}} 列 × {{grid_rows}} 行（Bento Grid）

---

## III. 视觉主题 (Visual Theme)

### 3.1 风格定义

| 维度 | 选择 | 说明 |
|------|------|------|
| 渲染模式 (Render Mode) | {{render_mode}} | image-mode: 每页 AI 大图 / html-mode: 每页 HTML 排版 |
| 预设风格 | {{preset_name}} | {{preset_description}} |
| Texture 质感 | {{texture}} | {{texture_description}} |
| Mood 氛围 | {{mood}} | {{mood_description}} |
| Typography 字体风格 | {{typography_style}} | {{typography_description}} |
| Density 密度 | {{density}} | {{density_description}} |

### 3.2 色彩系统

#### 主配色 (60-30-10 规则)

| 角色 | 颜色名称 | HEX 值 | 用途 | 占比 |
|------|----------|--------|------|------|
| Primary 主色 | {{primary_name}} | `{{primary_hex}}` | 背景、大面积色块 | 60% |
| Secondary 辅助色 | {{secondary_name}} | `{{secondary_hex}}` | 标题、图形元素 | 30% |
| Accent 强调色 | {{accent_name}} | `{{accent_hex}}` | 重点标注、CTA | 10% |

#### 中性色层级

| 角色 | HEX 值 | 用途 |
|------|--------|------|
| 正文文字 | `#212121` | 主要文本内容 |
| 次要文字 | `#757575` | 辅助说明、标签 |
| 弱化文字 | `#9E9E9E` | 时间戳、脚注 |
| 分割线 | `#E0E0E0` | 线条、边框 |
| 背景浅色 | `#F5F7FA` | 卡片背景、色块 |

#### 功能色

| 功能 | HEX 值 | 用途 |
|------|--------|------|
| 正向/增长 | `#4CAF50` | 正面数据、增长指标 |
| 警告/注意 | `#FF9800` | 需关注的数据 |
| 负向/下降 | `#F44336` | 负面数据、下降指标 |
| 信息/中性 | `#2196F3` | 信息标注、链接 |

#### 渐变定义

```css
/* 主渐变 - 用于标题背景、封面等 */
background: linear-gradient(135deg, {{grad_start}} 0%, {{grad_end}} 100%);

/* 辅助渐变 - 用于卡片、装饰元素 */
background: linear-gradient(180deg, {{aux_grad_start}} 0%, {{aux_grad_end}} 100%);
```

#### 对比度合规

| 组合 | 前景色 | 背景色 | 对比度 | WCAG AA |
|------|--------|--------|--------|---------|
| 正文/白底 | #212121 | #FFFFFF | 16.1:1 | ✅ Pass |
| 次要/白底 | #757575 | #FFFFFF | 4.6:1 | ✅ Pass |
| 白字/主色 | #FFFFFF | {{primary_hex}} | {{ratio}}:1 | ✅/❌ |
| 白字/辅助色 | #FFFFFF | {{secondary_hex}} | {{ratio}}:1 | ✅/❌ |

---

## IV. 字体系统 (Typography System)

### 4.1 字体方案

| 级别 | 用途 | 中文字体 | 英文字体 | 字重 |
|------|------|----------|----------|------|
| P1 | 大标题 (Hero) | {{cn_hero_font}} | {{en_hero_font}} | Bold (700) |
| P2 | 章节标题 (H1) | {{cn_h1_font}} | {{en_h1_font}} | SemiBold (600) |
| P3 | 小标题 (H2) | {{cn_h2_font}} | {{en_h2_font}} | Medium (500) |
| P4 | 正文 (Body) | {{cn_body_font}} | {{en_body_font}} | Regular (400) |
| P5 | 辅助文字 (Caption) | {{cn_caption_font}} | {{en_caption_font}} | Light (300) |

### 4.2 字号层级

基于 {{baseline}}px 基准：

| 元素 | 字号 | 行高 | 字间距 | 用途 |
|------|------|------|--------|------|
| Hero | {{hero_size}}px | 1.2 | -0.02em | 封面标题、核心大标题 |
| H1 | {{h1_size}}px | 1.3 | -0.01em | 章节标题 |
| H2 | {{h2_size}}px | 1.4 | 0 | 小标题、卡片标题 |
| Body | {{body_size}}px | 1.6 | 0.01em | 正文内容 |
| Caption | {{caption_size}}px | 1.5 | 0.02em | 注释、来源、时间 |

### 4.3 排版规则

- 标题不换行，超出时精简措辞
- 正文每行不超过 {{max_chars_per_line}} 个中文字符（约 {{max_line_width}}px）
- 段落间距 ≥ 行高 × 1.5
- 中英文之间自动添加半角空格
- 数字使用等宽对齐

---

## V. 排版原则 (Layout Principles)

### 5.1 主要排版范式：Bento Grid

采用 Bento Grid（便当盒网格）作为主要排版范式：

```
┌──────────┬─────┬─────┐
│          │     │     │
│  大卡片   │ B1  │ B2  │
│  (2×2)   ├─────┴─────┤
│          │           │
├────┬─────┤   中卡片   │
│ C1 │ C2  │  (2×1)    │
└────┴─────┴───────────┘
```

- 基础网格：12 列 × {{rows}} 行
- 间距 (Gap)：{{gap_size}}px
- 卡片圆角：{{border_radius}}px
- 卡片背景：{{card_bg}}

### 5.2 六种布局模式

| 模式 | 结构 | 适用内容 | 示例 |
|------|------|----------|------|
| 全幅标题 (Full Hero) | 标题占满整页 | 封面、章节过渡 | `[████████████]` |
| 左文右图 (Text-Image) | 60% 文字 + 40% 图片/图形 | 内容讲解、概念说明 | `[████    ████]` |
| 上下分割 (Split) | 上 40% 标题 + 下 60% 内容 | 数据展示、列表 | `[████████████]` |
| 多卡片 (Multi-card) | 2-4 个等宽卡片 | 对比、并列要点 | `[████][████]` |
| Bento Grid | 混合大小卡片 | 综合信息展示 | `[██][█][███]` |
| 对角线 (Diagonal) | 对角线分割布局 | 对比、转折 | `[███/    /██]` |

### 5.3 布局规则

- 每页最多 {{max_elements}} 个主要元素
- 留白占比 ≥ {{whitespace_ratio}}%
- 视觉焦点位于页面上方 1/3 处（Z-pattern 起点）
- 所有元素对齐到网格线

---

## VI. 图标使用规格 (Icon Usage Spec)

### 6.1 图标来源

| 参数 | 值 |
|------|-----|
| 图标类型 | {{icon_type}} |
| 风格 | {{icon_style}} (outline / filled / duo-tone) |
| 尺寸 | {{icon_size}}px × {{icon_size}}px |
| 颜色 | 跟随 Accent 色或内容语义色 |

### 6.2 使用规则

- 每页图标数量 ≤ {{max_icons_per_page}} 个
- 图标与文字间距 ≥ 8px
- 同一页内图标风格必须统一
- 功能图标（如箭头、勾选）使用纯色线条
- 装饰图标可使用多色

---

## VII. 图表参考列表 (Chart Reference List)

### 预期图表清单

| 序号 | 所在页 | 图表类型 | 数据来源 | 说明 |
|------|--------|----------|----------|------|
| 1 | {{page_num}} | {{chart_type}} | {{data_source}} | {{chart_description}} |
| 2 | ... | ... | ... | ... |

### 图表类型映射

| 数据特征 | 推荐图表 |
|----------|----------|
| 趋势/时间序列 | 折线图、面积图 |
| 对比/排名 | 柱状图、条形图 |
| 占比/构成 | 饼图、环形图、瀑布图 |
| 关系/流程 | 桑基图、流程图 |
| 分布 | 散点图、热力图 |
| 多维对比 | 雷达图 |

### 图表样式约束

- 图表配色使用功能色系统
- 坐标轴线条颜色：#E0E0E0
- 数据标签字号：12-14px
- 图例位置：图表下方或右侧
- 动画：入场动画，不使用持续动画

---

## VIII. 图片资源列表 (Image Resource List)

> **根据 d 美业方式渲染本节**：
> - `image-mode`：每页 = 一张 AI 大图，本节按"逐页 prompt 清单"展开
> - `html-mode`：页内可能含图片元素，本节按"页内图片资源表"展开

### 8A. image-mode：逐页 AI 图像 Prompt 清单

| 序号 | 所在页 | 主题 | 完整 Prompt | 负向约束 |
|------|--------|------|-------------|----------|
| 1 | {{page_num}} | {{page_topic}} | {{full_prompt}} | {{negative_prompt}} |
| 2 | ... | ... | ... | ... |

**image-mode 特殊规则**：
- 每一行 = 一页 PPT
- Prompt 必须包含：画幅、风格、密度、文本留白区、关键视觉元素
- 负向约束必须包含：禁止图标替代内容、禁止占位符、禁止数据图表
- 文本内容（如有）由另一通道注入 prompt，AI 图像仅生成背景与视觉

### 8B. html-mode：页内图片资源表

| 序号 | 所在页 | 尺寸 | 类型 | 来源 | 描述/Prompt |
|------|--------|------|------|------|-------------|
| 1 | {{page_num}} | {{img_size}} | {{img_type}} | {{source}} | {{description}} |
| 2 | ... | ... | ... | ... | ... |

### 图片处理规则（两种模式通用）

- 统一圆角：{{img_border_radius}}px
- 遮罩处理：按风格需要
- 滤镜：按风格预设应用
- 优先使用 SVG 矢量图形（html-mode 下）

---

## IX. 内容大纲 (Content Outline)

### 完整逐页大纲

#### Page 1: 封面

- **布局模式**: Full Hero
- **标题**: {{cover_title}}
- **副标题**: {{cover_subtitle}}
- **视觉元素**: {{cover_visual}}
- **背景处理**: {{cover_bg_treatment}}

#### Page 2: 目录

- **布局模式**: Multi-card / Bento Grid
- **标题**: {{toc_title}}
- **章节列表**: {{chapter_list}}

#### Page 3-N: 章节过渡页（如适用）

- **布局模式**: Full Hero
- **标题**: {{chapter_title}}
- **章节编号**: {{chapter_number}}

#### Page X: 内容页（逐页详细）

- **布局模式**: {{layout_mode}}
- **标题**: {{slide_title}}
- **内容要点**:
  1. {{point_1}}
  2. {{point_2}}
  3. {{point_3}}
- **图表**: {{chart_ref}}（关联 VII 节）
- **图片**: {{image_ref}}（关联 VIII 节）
- **图标**: {{icon_ref}}

#### Page Last: 结尾页

- **布局模式**: Full Hero / Split
- **标题**: {{closing_title}}
- **内容**: {{closing_content}}
- **视觉元素**: {{closing_visual}}

---

## X. 演讲者备注要求 (Speaker Notes Requirements)

### 备注规则

| 参数 | 值 |
|------|-----|
| 是否生成备注 | {{enable_speaker_notes}} |
| 备注详细程度 | {{notes_detail_level}} (brief / standard / detailed) |
| 语言 | {{notes_language}} |

### 备注内容要求

每页备注应包含：
1. **关键要点**：本页核心传达的信息（1-2 句）
2. **展开说明**：可补充讲述的细节（2-3 句）
3. **数据来源**：引用数据的出处
4. **过渡语**：到下一页的衔接话术

---

## XI. 技术约束 (Technical Constraints)

### SVG 规则

1. 所有图形必须使用 SVG 格式
2. 文字必须使用 `<text>` 元素，不可转为路径
3. 图标使用 `<symbol>` + `<use>` 复用
4. 渐变使用 `<linearGradient>` 定义
5. 动画使用 CSS animation，不使用 SMIL
6. SVG 中嵌入的图片使用 `<image>` 标签
7. viewBox 必须设置为 `0 0 {{width}} {{height}}`
8. 字体使用 `font-family` 属性引用外部字体
9. 颜色统一使用 HEX 格式 `#RRGGBB`
10. 所有 SVG 必须通过 W3C Validator 校验

### 兼容性

- 目标渲染环境：Chrome 90+、Safari 14+、Edge 90+
- 不使用 CSS Grid，使用 Flexbox 或绝对定位
- 不使用 CSS variables（内联样式优先）
- 图片格式：SVG > WebP > PNG > JPG

---

## XII. 设计检查清单 (Design Checklist)

### 生成后逐项检查

#### 全局一致性

- [ ] 所有页面使用统一的配色方案
- [ ] 字体方案在各页面一致
- [ ] 字号层级符合 IV 节定义
- [ ] 间距和留白符合 V 节定义
- [ ] 图标风格统一

#### 内容质量

- [ ] 标题均为叙述性标题（非标签）
- [ ] 无 AI 常见套话（"综上所述""总而言之"）
- [ ] 数据标注来源
- [ ] 无占位符内容
- [ ] 每页内容自洽

#### 视觉质量

- [ ] 对比度满足 WCAG 2.1 AA
- [ ] 无视觉溢出或重叠
- [ ] 文字可读性良好
- [ ] 视觉焦点明确
- [ ] 整体视觉语言统一

#### 技术质量

- [ ] SVG 格式正确
- [ ] viewBox 设置正确
- [ ] 无孤立元素
- [ ] 动画流畅不卡顿
- [ ] 文件大小合理

#### 封底检查

- [ ] 封底有意义（非空洞"谢谢"）
- [ ] 包含后续行动或联系方式
- [ ] 与封面风格呼应
```

---

## 使用说明

1. 模板中 `{{variable}}` 格式的占位符需根据八大确认结果替换
2. 某些节（如 VII 图表、VIII 图片）的项目数量根据内容大纲动态增减
3. IX 内容大纲逐页展开，页数等于确认的页数范围中值
4. XII 检查清单为最终质量门控，不可省略
