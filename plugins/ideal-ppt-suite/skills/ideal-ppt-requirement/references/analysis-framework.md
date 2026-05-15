# Analysis Framework — 内容分析方法论

本文件定义源素材的自动化分析方法，包括语言检测、内容信号提取、风格映射和页数估算。

---

## 分析流程总览

```
源素材文本 → 语言检测 → 内容信号提取 → 风格映射 → 页数估算 → topic slug 生成 → 输出信号
```

---

## 1. 语言检测 (Language Detection)

### 检测方法

基于文本中 CJK 字符占比判断主要语言：

```
total_chars = 文本总字符数（排除空白和标点）
cjk_chars = CJK Unified Ideographs (U+4E00-U+9FFF) 字符数
hiragana_katakana = 日文假名字符数
latin_chars = Latin 字母字符数

if hiragana_katakana / total_chars > 0.1:
    language = "ja"
elif cjk_chars / total_chars > 0.3:
    language = "zh"
elif latin_chars / total_chars > 0.7:
    language = "en"
else:
    language = "zh"  # 默认中文
```

### 混合语言处理

- 中英混合（常见于技术文档）：标记为 `zh`，正文提取时保留英文术语
- 日英混合：标记为 `ja`
- 检测不确定时：默认 `zh`

---

## 2. 内容信号提取 → 风格映射

### 信号关键词检测

从源素材中搜索以下关键词，统计命中次数，确定内容类型：

| 信号类别 | 关键词（中文） | 关键词（英文） | 权重 |
|---------|--------------|--------------|------|
| **数据型** | 数据、百分比、增长、下降、趋势、指标、KPI、同比、环比、占比 | data, percentage, growth, decline, trend, metric, KPI, YoY, ratio | 3 |
| **技术型** | 架构、系统、流程、模块、接口、服务、部署、框架、协议 | architecture, system, process, module, API, service, deploy, framework | 3 |
| **战略型** | 战略、愿景、规划、目标、方向、未来、转型、创新 | strategy, vision, plan, goal, direction, future, transformation | 2 |
| **产品型** | 产品、功能、优势、价格、体验、用户、需求、市场 | product, feature, advantage, price, experience, user, demand | 2 |
| **教育型** | 培训、教程、步骤、操作、方法、实践、入门、指南 | training, tutorial, step, operation, method, guide, how-to | 2 |
| **故事型** | 案例、故事、经历、感悟、挑战、成功、历程、回忆 | case, story, experience, challenge, success, journey | 1 |

### 内容类型判定

```
对每个信号类别计算加权得分：
score = 命中关键词数 × 权重

content_type = 得分最高的信号类别
如果最高分 <= 阈值（2 个命中）：默认为 "方案汇报型"
```

### 自动风格选择表

基于内容类型和受众类型，从 17 种预设中选择推荐风格：

| 内容类型 | 受众: 初学者 | 受众: 从业者 | 受众: 专家 | 受众: 高管 | 受众: 混合 |
|---------|------------|------------|-----------|-----------|-----------|
| 数据分析型 | 图表风格 | 图表风格 | 高密度信息图 | 图表风格 | 块状风格 |
| 技术方案型 | 插画风格 | 蓝图风格 | 架构图风格 | 商务风格 | 蓝图风格 |
| 战略规划型 | 商务风格 | 商务风格 | 论文风格 | 极简风格 | 商务风格 |
| 产品发布型 | 动画风格 | 商务风格 | 极简风格 | 极简风格 | 商务风格 |
| 教育培训型 | 黑板风格 | 手绘风格 | 架构图风格 | 商务风格 | 插画风格 |
| 故事叙述型 | 插画风格 | 动画风格 | 论文风格 | 极简风格 | 动画风格 |

### 备选风格

每种内容类型提供 2 个备选风格，按优先级排序：

| 内容类型 | 首选 | 备选 1 | 备选 2 |
|---------|------|--------|--------|
| 数据分析型 | 图表风格 | 块状风格 | 高密度信息图 |
| 技术方案型 | 蓝图风格 | 架构图风格 | 商务风格 |
| 战略规划型 | 商务风格 | 极简风格 | 论文风格 |
| 产品发布型 | 商务风格 | 极简风格 | 动画风格 |
| 教育培训型 | 黑板风格 | 手绘风格 | 插画风格 |
| 故事叙述型 | 动画风格 | 水彩风格 | 手绘风格 |

---

## 3. 内容长度 → 页数估算

### 算法

```
char_count = 源素材文本字符数（含标点，不含空白）

if char_count < 1000:
    slide_range = [5, 10]
elif char_count <= 3000:
    slide_range = [10, 18]
elif char_count <= 5000:
    slide_range = [15, 25]
else:
    slide_range = [20, 30]

# 微调：基于内容类型
if content_type == "数据分析型":
    slide_range = [range[0] + 2, range[1] + 3]  # 数据页需要更多空间
elif content_type == "故事叙述型":
    slide_range = [range[0], range[1] - 2]  # 故事页可以更精炼
```

### 页数分布预估

```
total_slides = (slide_range[0] + slide_range[1]) / 2

opening = 1~2 页（封面 + 可选引入）
toc = 1 页（目录/导航）
core = total_slides - opening - toc - closing
closing = 1~2 页（总结 + CTA/致谢）
```

### 字符数统计注意事项

- 中文字符：1 字符 = 约 1 字
- 英文单词：1 单词 ≈ 5 字符
- 混合文本：直接统计字符数即可，无需换算
- 排除空白行和纯标点行

---

## 4. Topic Slug 生成

将项目名称或主题转换为 URL 安全的 slug，用于目录命名。

### 生成规则

```
1. 提取源素材的核心主题（标题或第一段的核心短语）
2. 转换规则：
   ├── 中文主题 → 使用拼音首字母 + 关键词
   │   例: "2026年Q1销售业绩汇报" → "2026-q1-sales-report"
   ├── 英文主题 → lowercase + hyphenate
   │   例: "AI Product Launch Strategy" → "ai-product-launch"
   └── 混合主题 → 英文部分 lowercase + hyphenate，中文部分拼音化
3. 长度限制：slug 不超过 60 个字符
4. 合法字符：a-z, 0-9, hyphen (-)
5. 禁止连续 hyphen
```

### 示例

| 原始主题 | 生成的 slug |
|---------|------------|
| 2026年Q1销售业绩汇报 | `2026-q1-sales-report` |
| AI 产品发布策略 | `ai-product-launch` |
| 技术架构评审 | `tech-arch-review` |
| Company Annual Report | `company-annual-report` |
| 培训：新员工入职指南 | `onboarding-guide` |

---

## 5. 自动风格选择汇总表

综合所有分析维度的最终推荐输出：

```yaml
# 分析结果输出格式
language: zh | en | ja
content_type: 数据分析型 | 技术方案型 | 战略规划型 | 产品发布型 | 教育培训型 | 故事叙述型
char_count: {数字}
content_signals:
  - signal: {关键词}
    category: {信号类别}
    count: {命中次数}
recommended_style:
  primary: {预设名称}
  secondary: {预设名称}
  texture: {clean|grid|organic|pixel|paper}
  mood: {professional|warm|cool|vibrant|dark|neutral}
  typography: {geometric|humanist|handwritten|editorial|technical}
  density: {minimal|balanced|dense}
slide_count_range: [min, max]
topic_slug: {slug}
```
