# 布局库

## 基础布局（9 种）

### 1. title-hero
- **描述**：全幅英雄区域，大标题居中
- **适用**：封面、结论页、关键转折点
- **位置**：opening / closing

### 2. quote-callout
- **描述**：大号引用文本，突出显示
- **适用**：名人名言、客户评价、核心洞察
- **位置**：middle

### 3. key-stat
- **描述**：1-3 个大号数字/指标居中展示
- **适用**：KPI 展示、关键数据
- **位置**：middle

### 4. split-screen
- **描述**：左右等分，一侧图片一侧文字
- **适用**：图文对照、功能展示
- **位置**：middle

### 5. icon-grid
- **描述**：2x2 或 2x3 图标网格，每格含标题+描述
- **适用**：特性列表、能力展示、分类说明
- **位置**：middle

### 6. two-columns
- **描述**：两栏文字，可对称或非对称
- **适用**：对比分析、并列论点
- **位置**：middle

### 7. three-columns
- **描述**：三栏等宽文字
- **适用**：三方比较、三步流程、三种方案
- **位置**：middle

### 8. image-caption
- **描述**：大幅图片 + 底部说明文字
- **适用**：产品展示、场景展示
- **位置**：middle

### 9. agenda
- **描述**：编号列表或卡片列表
- **适用**：目录、议程、步骤清单
- **位置**：opening

---

## 信息图布局（14 种）

### 10. linear-progression
- **描述**：线性流程，箭头连接各阶段
- **适用**：流程步骤、时间线
- **内容匹配**：process, timeline
- **位置**：middle

### 11. binary-comparison
- **描述**：左右对比，中间分隔线
- **适用**：优缺点对比、方案选择
- **内容匹配**：comparison, pros-cons
- **位置**：middle

### 12. comparison-matrix
- **描述**：表格/矩阵，行列对比
- **适用**：多维度比较、功能对比表
- **内容匹配**：comparison, features
- **位置**：middle

### 13. hierarchical-layers
- **描述**：堆叠层级，从底到顶
- **适用**：架构层次、组织结构、技术栈
- **内容匹配**：hierarchy, architecture
- **位置**：middle

### 14. hub-spoke
- **描述**：中心主题向外辐射
- **适用**：生态系统、核心能力、影响因素
- **内容匹配**：relationships, ecosystem
- **位置**：middle

### 15. bento-grid
- **描述**：灵活卡片网格（**推荐默认布局**）
- **适用**：几乎所有内容类型
- **内容匹配**：universal
- **位置**：any

### 16. funnel
- **描述**：漏斗形，从宽到窄
- **适用**：转化流程、筛选过程、销售漏斗
- **内容匹配**：conversion, process
- **位置**：middle

### 17. dashboard
- **描述**：多个指标卡片 + 图表组合
- **适用**：数据报告、运营看板
- **内容匹配**：statistics, KPIs
- **位置**：middle

### 18. venn-diagram
- **描述**：交叉圆环，展示重叠关系
- **适用**：共同点与差异、交集概念
- **内容匹配**：relationships, overlap
- **位置**：middle

### 19. circular-flow
- **描述**：环形循环流程
- **适用**：循环过程、迭代模型
- **内容匹配**：process, cycle
- **位置**：middle

### 20. winding-roadmap
- **描述**：蜿蜒路线图，节点沿途分布
- **适用**：里程碑、实施计划
- **内容匹配**：timeline, milestones
- **位置**：middle

### 21. tree-branching
- **描述**：树形结构，根到叶展开
- **适用**：决策树、分类体系
- **内容匹配**：hierarchy, decisions
- **位置**：middle

### 22. iceberg
- **描述**：冰山模型，表层与深层
- **适用**：隐性/显性分析、风险分析
- **内容匹配**：layers, depth
- **位置**：middle

### 23. bridge
- **描述**：桥形，从现状到目标
- **适用**：变革路径、差距分析
- **内容匹配**：transformation, gap-analysis
- **位置**：middle

---

## 布局选择指南

### 按内容类型

| 内容类型 | 推荐布局 |
|---------|---------|
| 流程/步骤 | linear-progression, funnel |
| 对比/比较 | binary-comparison, comparison-matrix, two-columns |
| 层次/架构 | hierarchical-layers, tree-branching |
| 关系/网络 | hub-spoke, venn-diagram |
| 数据/指标 | dashboard, key-stat, bento-grid |
| 时间线 | winding-roadmap, linear-progression |
| 通用内容 | **bento-grid**（默认） |

### 按页面位置

| 位置 | 推荐布局 |
|------|---------|
| Opening (1-2 页) | title-hero, agenda |
| Middle (主体) | bento-grid, icon-grid, two-columns, three-columns |
| Closing (最后 1-2 页) | title-hero, key-stat, quote-callout |
