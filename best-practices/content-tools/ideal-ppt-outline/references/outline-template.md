# Outline 模板规范

## outline.md 文件结构

```markdown
# {演示主题}

## 元数据

- 主题：{topic}
- 风格：{preset name 或 custom}
- 维度：{texture} + {mood} + {typography} + {density}
- 受众：{audience}
- 语言：{language}
- 页数：{N} 页
- 日期：{YYYY-MM-DD}

---

## STYLE_INSTRUCTIONS

{以下为 STYLE_INSTRUCTIONS 块，是所有视觉决策的唯一来源}

### Design Aesthetic
{2-3 句话描述整体设计美学}

### Background
- 画布背景色：{HEX}
- 纹理效果：{描述}

### Typography
- 标题字体：{font description}
- 正文字体：{font description}
- 强调字体：{font description}

### Color Palette
| Role | Color Name | HEX | Usage |
|------|-----------|-----|-------|
| Primary | {name} | #{hex} | {usage} |
| Secondary | {name} | #{hex} | {usage} |
| Accent | {name} | #{hex} | {usage} |
| Background | {name} | #{hex} | {usage} |
| Text Primary | {name} | #{hex} | {usage} |
| Text Secondary | {name} | #{hex} | {usage} |

### Visual Elements
- {视觉元素 1}
- {视觉元素 2}
- ...

### Density Guidelines
- 每页要点数：{range}
- 正文字号基准：{18px 或 24px}
- 留白比例：{description}

### Style Rules
**Do：**
- {规则 1}
- {规则 2}

**Don't：**
- {禁止 1}
- {禁止 2}

---

## 幻灯片大纲

### Slide 01: {封面标题}
- **Type**: cover
- **Title**: {主标题}
- **Subtitle**: {副标题}
- **Visual**: {视觉描述}
- **Layout**: title-hero

---

### Slide 02: {页面标题}
- **Type**: content
- **Narrative Goal**: {这页要传达什么信息}
- **Bento Grid**:
  - Card 1 ({size}): {标题} — {具体内容要点}
  - Card 2 ({size}): {标题} — {具体内容要点}
  - Card 3 ({size}): {标题} — {具体内容要点}
- **Visual**: {具体的视觉布局描述}
- **Layout**: {布局名称}

---

### Slide NN: {封底标题}
- **Type**: back-cover
- **Summary Message**: {核心总结信息}
- **CTA**: {行动号召}
- **Visual**: {视觉描述}
- **Layout**: title-hero
```

## 卡片内容编写规则

### 具体性要求

每张卡片的内容必须 **具体且自包含**：

**错误**（抽象标签）：
```
Card 1: 核心优势
Card 2: 技术架构
Card 3: 用户案例
```

**正确**（具体内容）：
```
Card 1 (large, left): 核心优势 — 1. 处理速度提升 300%；2. 支持百万级并发；3. 零代码集成
Card 2 (small, right-top): 技术架构 — 微服务架构，Kubernetes 部署，自动扩缩容
Card 3 (small, right-bottom): 用户案例 — 某头部电商双十一期间零故障运行
```

### 数据卡片格式

```
Card (data): 月活用户 — 1.2亿（↑23% YoY），来源：2025 Q4 财报
```

### 引用卡片格式

```
Card (quote): "未来十年最大的机会在 AI + 行业" — 李开复，2025
```

## 文件命名 slug 规则

- 格式：kebab-case
- 长度：2-5 个词
- 唯一：同一演示中不重复
- 中文：可用拼音或简短英文
- 示例：`ji-qi-xue-xi-jie-shao`, `market-analysis`, `team-intro`
