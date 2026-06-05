# ideal-lab 展示站全面重构设计

- **日期**：2026-06-05
- **作者**：Claude Code（brainstorming skill）
- **状态**：待评审
- **关联**：`docs/design-system.md`、`site/`（Next.js 16 展示站）、`skills-graph.json`（46 节点 / 183 边 / 5 关系）

---

## 0. 背景与目标

`site/` 是 ideal-lab 的展示站。当前痛点：

1. **风格过于简单**——已有 design-system.md 定义了"Structured · Sharp · Warm"，但仅落实到颜色/字体，未转化为首页/详情页的视觉语言。
2. **Skill 展示不够详细**——Skill 详情页直接渲染 `SKILL.md` 全文，没有"它能做什么 / 解决什么痛点 / 原理 / 上下游"的结构化信息。
3. **缺少知识图谱**——`skills-graph.json` 已存在（46 节点 / 183 边），但站点未利用。访客无法直观看到 skill 间的引用、增强、前置、嵌入、产出关系。

**核心目标**：让访客在 30 秒内知道——
- 仓库里大概总共有哪些 skill
- 它们之间的关系是什么
- 能实现哪些任务
- 每个 skill 都能做什么
- 能解决哪些痛点
- 逻辑 / 原理是什么

---

## 1. 范围与非范围

### 1.1 范围内

| 维度 | 内容 |
|------|------|
| 重写 | 首页、Plugin 详情页、Skill 详情页 |
| 新增 | 任务数据层（`tasks.json`）、痛点数据层（`plugin-pain-points.json`）、交互式知识图谱组件、任务面板组件、Mini Graph 组件、TOC 折叠 |
| 设计 | 全面应用 `design-system.md` 全部 token；首屏以图谱为中心 |
| CI/CD | 仓库 push → GitHub Action 触发 lint + validate + next build + 部署（准实时更新） |
| 验收 | Lighthouse mobile ≥ 90、a11y 0 critical、构建期 skillId 一致性校验 |

### 1.2 范围外（明确不做）

| 项 | 原因 |
|----|------|
| 实时推送（SSE / WebSocket） | ideal-lab 是公开展示站，无多人协作需求；过度工程 |
| 客户端轮询（每 30-60s 拉数据） | 46 节点数据小，build 10s 内，CI/CD 准实时（A 方案）足够 |
| 用户登录、收藏、评论 | 单向展示站，无身份概念 |
| 图谱搜索节点 | 复用现有 `/plugins` 列表的搜索；URL 跳转到 skill 详情 |
| 多任务叠加高亮 | 单任务保持对比；多任务会丧失焦点 |
| 国际化 | 第一版中文；i18n 框架预留但 P2 |
| 移动端拖动图谱 | 支持 pinch-zoom；拖动不实现（小屏物理空间不足） |
| 导出 PNG | 工具栏预留位置，P2 |
| FRP 创作系统（如用户自定义任务） | 数据层静态；P2 之后可考虑 |

---

## 2. 受众与场景

| 受众 | 占比假设 | 关心什么 | 在站点找什么 |
|------|----------|----------|--------------|
| 技术决策者（架构师 / 技术负责人） | 40% | 能不能用、好不好装、解决什么问题 | 首屏价值主张 + 痛点卡 + 安装命令 |
| Claude Code 重度使用者（开发者 / AI 工程师） | 40% | 内部怎么工作、阶段顺序、什么场景触发、参数怎么配 | 知识图谱 + Skill 详情页的原理与上下游 |
| 潜在 Skill 贡献者 / 外部访客 | 20% | 这是个什么、能不能贡献、贡献路径 | Plugin 索引 + Skill 详情页的 references/scripts |

**设计含义**：单一首页必须分层服务三类访客。首屏中段同时呈现"图谱"（重度用户）+ "任务"（决策者）+ "Plugin 索引"（贡献者）。

---

## 3. 核心决策（设计期锁定）

| # | 决策 | 取值 | 锁定理由 |
|---|------|------|----------|
| 1 | 受众 | 三类都要照顾 | 用户已确认 |
| 2 | 首页核心能力 | 知识图谱 + 任务探索并列 | 用户已确认 |
| 3 | 图谱位置 | 首屏正中央 | 用户已确认 |
| 4 | 图谱交互 | 力导向 + 可拖/缩/高亮/点击 | 用户已确认 |
| 5 | 任务粒度 | 13 个高级任务 | 用户已确认 |
| 6 | 信息架构 | 4 层渐进深入 | 用户已确认 |
| 7 | 实现路径 | 全面重写 `site/` 设计，保留 Next.js 16 + Tailwind + 现有 design tokens | 用户已确认 |
| 8 | 不可牺牲 | 视觉冲击力 + 交互质量 + 性能与可访问性 | 用户已确认 |
| 9 | 任务数据源 | 手动定义 13 个任务，**不**自动推断 | 用户授权我用最佳实践 |
| 10 | 独立 `/graph` 路由 | 不新增 | 用户授权我用最佳实践 |
| 11 | 图谱库选型 | **react-force-graph-2d** | 用户授权我用最佳实践 |
| 12 | 实时更新 | **CI/CD 准实时**（GitHub Action 触发部署，1-3 分钟） | 用户已确认选 A |
| 13 | TOC 折叠 | 在 S4 交付，纳入 Skill 详情页改造 | 用户已确认 |

---

## 4. 目录与文件结构

```
site/
├── src/
│   ├── app/
│   │   ├── page.tsx                     # 首页（重写）
│   │   ├── layout.tsx                  # 不动
│   │   ├── globals.css                 # 仅加图谱/Mini Graph 专用 token
│   │   ├── plugins/
│   │   │   ├── page.tsx                # 11 个 Plugin 总览（保留 grid，可优化）
│   │   │   └── [plugin]/
│   │   │       ├── page.tsx            # Plugin 详情（重写：Hero + 痛点 + 数据 + Skill 列表）
│   │   │       └── skills/
│   │   │           └── [skill]/
│   │   │               └── page.tsx    # Skill 详情（重写：原理 + 流程 + 上下游 + TOC）
│   ├── components/
│   │   ├── graph/
│   │   │   ├── GraphCanvas.tsx         # 首屏主图谱（react-force-graph-2d）
│   │   │   ├── GraphLegend.tsx         # 关系类型图例
│   │   │   ├── GraphTooltip.tsx        # 节点 hover 详情
│   │   │   └── GraphControls.tsx       # 重置/全屏/导出
│   │   ├── graph-mini/                 # Skill 详情页用 Mini Graph
│   │   │   ├── MiniGraph.tsx           # 6-12 节点子图
│   │   │   └── MiniGraphLegend.tsx
│   │   ├── tasks/
│   │   │   ├── TaskPanel.tsx           # 首屏右侧任务面板
│   │   │   ├── TaskCard.tsx            # 单张任务卡
│   │   │   └── TaskScriptView.tsx      # 任务详情态（剧本卡）
│   │   ├── plugin/
│   │   │   ├── PluginHero.tsx
│   │   │   ├── PluginPainPoints.tsx    # 痛点卡网格
│   │   │   ├── PluginMetrics.tsx       # 结构指标
│   │   │   └── PluginSkillList.tsx
│   │   ├── skill/
│   │   │   ├── SkillHeader.tsx
│   │   │   ├── SkillCapabilities.tsx   # 它能做什么
│   │   │   ├── SkillPainPoints.tsx     # 它解决什么痛点
│   │   │   ├── SkillRelated.tsx        # 上下游 skill（含 L4 入口）
│   │   │   ├── SkillToc.tsx            # TOC + 折叠
│   │   │   └── SkillMdRenderer.tsx     # 已有 prose，保留
│   │   ├── Nav.tsx                     # 加 "Plugins" "Graph" 入口（Graph 锚到首页）
│   │   └── Footer.tsx                  # 不动
│   ├── lib/
│   │   ├── plugins.ts                  # 已有，不动
│   │   ├── types.ts                    # 加 SkillEdge / Task 类型
│   │   ├── graph.ts                    # 加载 skills-graph.json → 节点/边
│   │   ├── tasks.ts                    # 加载 tasks.json → Task[]
│   │   ├── plugin-pain-points.ts       # 加载 plugin-pain-points.json
│   │   ├── skill-summary.ts            # 从 SKILL.md 抽 H2 列表（用于 TOC + "它能做什么"）
│   │   └── utils.ts                    # 已有
│   └── data/
│       ├── tasks.json                  # 13 个高级任务定义
│       └── plugin-pain-points.json     # 11 plugin × 2-4 条痛点（第一版至少 8 个 plugin 有内容）
├── public/
│   └── graphs/
│       └── skills-graph-fallback.svg  # build-time 用 mermaid 渲染的静态降级图
├── .github/workflows/
│   └── deploy-site.yml                # 新增：GitHub Pages 部署
├── next.config.ts                      # 改：output: 'export' + basePath '/ideal-lab' + trailingSlash
├── package.json                        # 加 react-force-graph-2d, d3-force, @types/d3-force
└── ...
```

---

## 5. 4 层信息架构

### 5.1 L1 首页

```
┌────────────────────────────────────────────────────────────┐
│ NAV: Ideal Best Practices    Plugins    Graph    GitHub  ☀│
├────────────────────────────────────────────────────────────┤
│ HERO BAND (h-32)                                            │
│  "46 个 skill · 11 个 plugin · 183 条引用关系"             │
│  一句话价值主张                                              │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────┐    │
│  │   交互式知识图谱         │  │  任务面板（Tasks）    │    │
│  │   （70% 宽，h-[70vh]）   │  │  13 张任务卡          │    │
│  │                          │  │  关系类型过滤器       │    │
│  │  • 力导向 + Plugin 聚类  │  │                      │    │
│  │  • 节点 = skill          │  │                      │    │
│  │  • 边 = 5 种关系         │  │                      │    │
│  │  • 大小 = 入度           │  │                      │    │
│  │  • 颜色 = category       │  │                      │    │
│  │  [↻] [⛶] [↓ PNG]         │  │                      │    │
│  └──────────────────────────┘  └──────────────────────┘    │
│ ── L1 痛点卡（4 张，scroll-triggered reveal） ──           │
│ ── Plugin 索引（11 张卡，grid 3 列） ──                    │
├────────────────────────────────────────────────────────────┤
│ FOOTER                                                     │
└────────────────────────────────────────────────────────────┘
```

**响应式**：
- Desktop ≥1024px：图谱 + 任务面板左右分栏
- Tablet 640-1023px：图谱占满，任务面板折叠为顶部按钮"🎯 13 个任务"
- Mobile <640px：图谱只读 + pinch-zoom，任务面板顶部折叠

### 5.2 L2 Plugin 详情页

```
← 返回首页 / 全部 Plugin

[Category 徽章]   ideal-dev-workflow       v2.0.0
H1: ideal-dev-workflow
副标题: 15 阶段开发流程：需求→方案→计划→编码→测试→评审→交付
[安装命令 复制按钮]

── 痛点（3-4 张卡，scroll reveal） ──
── 结构指标（4 列：skill 数 / 阶段数 / 关系数 / 编排器数） ──
── Skill 列表（按 phase 排序；阶段 / 名称 / 描述 / 引用·脚本数） ──
── CTA: "在图谱中只看本 Plugin" → 跳首页 ?plugin=... ──
```

### 5.3 L3 Skill 详情页

```
← 返回 ideal-dev-workflow

[Phase P1]   ideal-requirement    需求收集
H1: ideal-requirement
副标题: "在 P1 阶段收集、澄清、确认用户需求"

── 它能做什么（3-5 个动词句） ──
  ✓ 解析模糊需求 → 结构化需求文档
  ✓ 区分功能/非功能/约束需求
  ...
── 它解决什么痛点（1-2 段叙事） ──
── 上下游 skill（含 L4 入口） ──
  上游（前序）: ...
  下游（被谁用）: ideal-dev-solution [展开 →]
  增强: panel-review [展开 →]
── SKILL.md 全文（带 TOC + 折叠） ──
  [TOC 浮动在右侧]
  [H2 超过 8 个时折叠最深的 3 个]
── 引用与脚本 ──
  references/: requirements-template.md, ...
  scripts/: validate-requirements.sh, ...
```

### 5.4 L4 Mini Graph（Skill 详情页内联展开）

点"上下游 skill"中的任一项 → 在该 section 内联展开 6-12 节点子图。中心节点 = 当前 skill，1 跳邻居围绕。

```
┌────────────────────────────────────┐
│   [panel-review]                   │
│       ↘                            │
│   [ideal-requirement]  ← 中心      │
│       ↘ ↗                          │
│   [ideal-dev-solution]             │
│       ↓                            │
│   [ideal-dev-plan]                 │
│                                    │
│   [在图谱中查看 → 跳到首页]        │
└────────────────────────────────────┘
```

**实现**：用 SVG + d3-force 一次性算（不复用首屏 GraphCanvas），100ms 内完成，6-12 节点无压力。
> **为什么不用 react-force-graph-2d**：首屏主图谱是固定 46 节点（一次性算完后持续交互），react-force-graph-2d 适合这种规模。Mini Graph 每次展开都要重算，d3-force 直接调底层 API 更轻量、bundle 更小（避免在小节点图上引入完整图谱库的开销）。

---

## 6. 数据模型

### 6.1 SkillEdge（type 扩展）

```ts
// site/src/lib/types.ts
export interface SkillEdge {
  source: string;       // "ideal-ppt-suite/ideal-ppt-research"
  target: string;       // "ideal-ppt-suite/ideal-ppt-outline"
  relation: "enhancement" | "prerequisite" | "embeds" | "produces_for" | "alternative";
}
```

### 6.2 Task

```ts
export interface Task {
  id: string;                       // url 友好: "make-ppt"
  title: string;                    // 用户语言: "做一个市场汇报 PPT"
  problem: string;                  // 1-2 句痛点
  outcome: string;                  // 1 句预期产出
  scope: "lead" | "support" | "infra";
  skillIds: string[];               // 完整路径 plugin/skill
  relatedPluginSlugs: string[];     // 卡片显示
  estimatedSteps: number;           // 5-15
}
```

### 6.3 13 个初始任务（设计期锁定）

| # | id | title | scope | skill 数估算 |
|---|----|-------|-------|--------------|
| 1 | make-ppt | 做一个市场汇报 PPT | lead | 7-9 |
| 2 | deep-research-topic | 把一份主题调研透 | lead | 5-7 |
| 3 | full-dev-cycle | 走一次完整的开发流程 | lead | 12-14 |
| 4 | review-solution | 评审一份技术方案 | support | 4-6 |
| 5 | write-solution | 写一份技术方案 | lead | 3-5 |
| 6 | generate-test-cases | 生成验收用例 | support | 3-4 |
| 7 | exec-and-review | 执行编码 + 自动评审 | support | 5-7 |
| 8 | build-knowledge-base | 建一个结构化知识库 | lead | 4-6 |
| 9 | write-long-doc | 写一份长文档（标书/方案/汇报） | lead | 5-7 |
| 10 | generate-images | 调一个图片生成模型 | infra | 1-2 |
| 11 | generate-dify-dsl | 生成一个 Dify 工作流 DSL | lead | 1-3 |
| 12 | maintain-ideal-lab | 维护 ideal-lab 仓库 | infra | 1-3 |
| 13 | optimize-skill | 优化 / 评审一个 skill 自身 | support | 2-4 |

**硬约束**：每个 task 的 `skillIds` 必须在 `skills-graph.json` 的 `nodes[].id` 中存在。**不存在的 skill 不在任务里出现**。

### 6.4 plugin-pain-points.json

```ts
export interface PluginPainPoint {
  title: string;       // 1 句话痛点
  detail?: string;     // 1 段补充
}
export interface PluginPainPoints {
  [pluginSlug: string]: PluginPainPoint[];  // 2-4 条
}
```

**硬约束**：
- 第一版至少 8/11 plugin 有内容；剩余 3 个可空
- **不**写"用了之后业务提升 X%"——只写**问题本身**
- 内容由 implementation phase 人工撰写；不通过算法生成

---

## 7. 首屏图谱（GraphCanvas）详细设计

### 7.1 节点视觉规则

| 维度 | 规则 |
|------|------|
| 大小 | 半径 = `√(inDegree + 1) × 6px`，范围 8-24px |
| 填充色 | 5 种 category 色（沿用 `--bp-category-*` token） |
| 外环 | 同 plugin 的 skill 共享一个虚线 `plugin halo`（Plugin 聚类视觉） |
| 默认态 | 实心 + 1px 同色边框 |
| 被任务选中 | 填充不变 + 2px 白色描边 + 6px 品牌色发光 |
| hover | 放大 1.4× + tooltip |
| hover 邻居 | 1 跳邻居边框 2px 高亮；其他透明度 0.25 |
| dim（被过滤器筛掉） | 透明度 0.15 |
| 选中（点击进入） | 1.4× 缓动脉动（1.5s 一次） |

### 7.2 边视觉规则

| 关系 | 边数 | 颜色 | 样式 | 标签 |
|------|------|------|------|------|
| enhancement | 146 | `#a3a3a3` | 实线 0.8px | 不显示 |
| prerequisite | 14 | `#7b5cea` | 实线 1.5px + 箭头 | 不显示 |
| embeds | 18 | `#0ea5a0` | 虚线 1px | 不显示 |
| produces_for | 4 | `#d98b0a` | 实线 1.5px + 双箭头 | 不显示 |
| alternative | 1 | `#9b6cea` | 点线 1.5px | 不显示 |

**默认不显示边标签**——避免视觉噪声。hover 边时弹 tooltip："X 是 Y 的前置"。

### 7.3 力学参数（d3-force 调优）

```
forceCenter:     strength 0.05
forceLink:       distance 60, strength 0.3
forceManyBody:   strength -120
forceCollide:    radius = nodeRadius + 4
forceX / forceY: 弱（同 plugin 通过 hidden intra-plugin edges 拉近）
```

### 7.4 性能预算

| 指标 | 目标 |
|------|------|
| 初始渲染 | < 500ms |
| 拖动帧率 | ≥ 55fps（桌面）/ ≥ 30fps（移动） |
| 内存 | < 50MB |
| 首屏 LCP | < 2.5s（用 `dynamic(import, { ssr: false })` 跳过 SSR） |

### 7.5 控件（右下角浮工具条）

```
[↻ 重置布局]  [⛶ 全屏]  [↓ 导出 PNG]
```

- **重置**：50ms 动画回到当前中心
- **全屏**：`requestFullscreen`，图谱占满视口
- **导出 PNG**：`canvas.toDataURL()`，文件名 `ideal-lab-graph-YYYYMMDD.png`

### 7.6 与任务面板联动

任务面板 checkbox 状态 → URL `?task=make-ppt&rel=prerequisite,enhancement` → GraphCanvas 过滤。

| 任务面板状态 | 图谱响应 |
|--------------|----------|
| 无任务 | 全图正常 |
| 勾选 1 个任务 | 该任务涉及的 skill 高亮，其他 dim 0.15 |
| 多个任务 | 不支持（单任务模式） |
| 关系类型过滤 | 在已选任务内，只显示选中类型的边 |

**反向**：hover 图谱节点 → 任务面板里"涉及该 skill 的任务卡"加 brand 色边框。

### 7.7 无障碍

| 维度 | 处理 |
|------|------|
| 键盘 | Tab 聚焦下一节点（入度降序），Enter 跳转，Esc 退出全屏 |
| 屏幕阅读器 | 节点 `role="button"` + `aria-label="skill · plugin · phase"`；容器 `role="application"` |
| 减少动画 | `prefers-reduced-motion: reduce` 关闭拖动惯性、关闭 hover 缩放 |
| 替代视图 | 链接到 `/plugins` 列表 |

### 7.8 静态 fallback

禁用 JS 或图谱加载失败时，降级为：
- 半幅高度（h-64）的静态 SVG 海报（CI 渲染 `docs/skills-graph.mmd` 导出，存 `public/graphs/skills-graph-fallback.svg`）
- 标题照常
- 任务面板变成"加载失败 [重试]" + 跳 `/plugins` 链接

---

## 8. 任务面板与剧本视图

### 8.1 任务面板 UI（首屏右侧）

```
┌──────────────────────────────────┐
│  你想做什么？                     │
│  选一个任务，看哪些 skill 参与   │
│                                  │
│  [做一个市场汇报 PPT]            │  ← 卡片
│  7-9 个 skill · PPT 全链路      │
│  [ideal-ppt-suite]              │
│                                  │
│  [走一次完整的开发流程]          │
│  12-14 个 skill · 15 阶段       │
│  [ideal-dev-workflow]           │
│  ... 13 张                       │
│                                  │
│  ── 关系类型过滤 ──              │
│  □ enhancement (146)             │
│  □ prerequisite (14)             │
│  □ embeds (18)                   │
│  □ produces_for (4)              │
│  □ alternative (1)               │
│                                  │
│  [清空过滤]                      │
└──────────────────────────────────┘
```

**交互**：
- 单任务聚焦（避免多选导致图谱全是高亮，丧失对比）
- URL 持久化（`?task=make-ppt&rel=prerequisite,enhancement`），可分享
- 移动端：顶部一行"🎯 13 个任务"按钮 + 全屏抽屉

### 8.2 任务详情态（剧本视图）

点任务卡 → 顶部图谱过滤 + 任务卡展开为"剧本卡"（在首页内联 drawer，不切页）：

```
← 退出剧本

H2: 做一个市场汇报 PPT
痛点：从 0 到 1 做 PPT，要拼模板、想大纲、调风格、出图、改样式...
预期：交付一份 16:9 / 10-30 页 / 可编辑 PPTX

── 它会这样工作（13 步骤） ──
1. ideal-ppt-research      主题调研
2. ideal-ppt-strategist    八大确认
3. ideal-ppt-outline       大纲生成
...

── 涉及的 7 个 skill 在图谱中已高亮 ──

[查看 Plugin 详情]  [查看第一个 skill]
```

**关键**：剧本态 + 图谱**同时可见**——用户能感知"哪些节点被这个任务激活"。

### 8.3 反向联动

hover 图谱节点 → 任务面板里涉及该 skill 的任务卡加 brand 色边框。

---

## 9. Plugin 详情页

### 9.1 结构

| Section | 数据源 | 备注 |
|---------|--------|------|
| Hero | plugin.json | Category 徽章 + 名称 + 副标题 + 安装命令 |
| 痛点卡（3-4 张） | plugin-pain-points.json | scroll-triggered reveal |
| 结构指标 | skills-graph.json + plugin.json | 4 列：skill 数 / 阶段数 / 关系数 / 编排器数 |
| Skill 列表 | SKILL.md frontmatter | 按 phase 排序 |
| CTA | URL 跳首页 | "?plugin=ideal-dev-workflow" 自动 dim |

### 9.2 痛点卡硬约束

- 只写**仓库现状能解决的**问题
- 允许"这个 Plugin 存在的**原因**"
- **不**写"做了之后业务提升 X%"
- 第一版至少 8/11 plugin 有内容；可空

---

## 10. Skill 详情页

### 10.1 结构

| Section | 数据源 | 备注 |
|---------|--------|------|
| Header | SKILL.md frontmatter | Phase + 名称 + 副标题 |
| 它能做什么 | 解析 SKILL.md H2 + 人工 | 3-5 个动词句；解析失败可空 |
| 它解决什么痛点 | 人工 | 1-2 段；可空 |
| 原理 / 流程 | 解析 SKILL.md H2 | 进入 L4 Mini Graph 入口 |
| 上下游 skill | skills-graph.json 反查 | 折叠式 + L4 入口 |
| SKILL.md 全文 | prose 渲染 | 已有样式保留 |
| TOC + 折叠 | 解析 H2/H3 | S4 交付 |
| 引用与脚本 | filesystem 扫 | 已有 |

### 10.2 TOC 与折叠

- **TOC 提取**：从已渲染的 SKILL.md React 树里读 H2/H3 DOM 节点生成（不引入新依赖；不解析 markdown 两次）
- 右侧浮动目录（sticky，`top-24`）
- H2 超过 8 个时，最深的 3 个默认折叠，`<details>` 元素
- 滚动时高亮当前章节（IntersectionObserver）

### 10.3 "它能做什么"内容策略

- 优先从 SKILL.md body **自动提取**——`skill-summary.ts` 解析 H2 标题 + 第一句描述
- 如果 SKILL.md **没有清晰结构**，允许**空**——不编造
- 第一版不强制每页都有

### 10.4 Mini Graph（L4）

- 触发：点"上下游 skill"中任一项
- 实现：SVG + d3-force 一次性算 100ms；6-12 节点无压力
- 中心节点 = 当前 skill；周围 = 1 跳邻居
- 提供"在图谱中查看 → 跳首页"按钮

---

## 11. 数据校验（build-time）

### 11.1 任务 skillId 一致性

```ts
// site/src/lib/tasks.ts
import graph from "../../../skills-graph.json";
import tasks from "../data/tasks.json";

const allSkillIds = new Set(graph.nodes.map(n => n.id));
for (const task of tasks) {
  for (const id of task.skillIds) {
    if (!allSkillIds.has(id)) {
      throw new Error(`Task ${task.id} references unknown skill ${id}`);
    }
  }
}
```

**S2 末尾**必须通过。

### 11.2 Plugin 痛点 pluginSlug 校验

```ts
// site/src/lib/plugin-pain-points.ts
import plugins from "../data/plugin-pain-points.json";
const known = new Set(getAllPlugins().map(p => p.slug));
for (const slug of Object.keys(plugins)) {
  if (!known.has(slug)) throw new Error(`Unknown plugin ${slug} in pain-points`);
}
```

### 11.3 静态降级图渲染（CI）

```yaml
# .github/workflows/build-site.yml
- name: Render graph fallback
  run: npx -p @mermaid-js/mermaid-cli mmdc -i docs/skills-graph.mmd -o site/public/graphs/skills-graph-fallback.svg
```

---

## 12. CI/CD 与准实时更新（GitHub Pages）

**目标**：仓库 push → 1-3 分钟内 `https://MTleen.github.io/ideal-lab` 反映新内容。

**当前**：仓库 push → 已有 `validate` workflow（lint）→ 但**没有**自动触发站点部署。

### 12.1 Next.js 静态导出配置

`site/next.config.ts` 必须改为静态导出（GitHub Pages 不支持 server runtime）：

```ts
const nextConfig: NextConfig = {
  output: 'export',           // 纯静态 HTML + assets
  basePath: '/ideal-lab',     // 项目页路径
  assetPrefix: '/ideal-lab',  // 静态资源前缀
  images: { unoptimized: true },  // 静态导出禁用 next/image 优化
  trailingSlash: true,        // GitHub Pages 对 /path/index.html 解析更稳
};
```

**静态导出约束（必须遵守，否则 build 失败）**：
- ❌ 不允许 `dynamic = 'force-dynamic'`
- ❌ 不允许 `revalidate` / `revalidatePath`
- ❌ 不允许 API route (`route.ts`)——`tasks.json` 校验在 build-time 跑，**不**做运行时 endpoint
- ❌ 不允许 `cookies()` / `headers()` / `searchParams` 等 server runtime API
- ✅ 允许 `generateStaticParams` 显式枚举（已在用）
- ✅ 允许 `dynamic = 'force-static'` 或默认值

**当前 spec 兼容性核对**：
- 首页、Plugin 详情、Skill 详情都是 SSG + `generateStaticParams` ✅
- 任务过滤 / 图谱交互全部在客户端（`useState` + URL searchParams via `useSearchParams`） ✅
- 数据层 `fs.readFileSync` 是 build-time IO ✅
- `notFound()` 调用——Next 16 静态导出支持 ✅

### 12.2 CI 工作流

```yaml
# .github/workflows/deploy-site.yml
name: Deploy Site to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'site/**'
      - 'plugins/**'              # SKILL.md 改了也要触发
      - 'skills-graph.json'
      - '.github/workflows/deploy-site.yml'
  workflow_dispatch:               # 允许手动触发

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
          cache-dependency-path: site/package-lock.json

      - name: Install dependencies
        run: npm ci --prefix site

      - name: Render graph fallback SVG
        run: |
          npm install -g @mermaid-js/mermaid-cli
          mmdc -i docs/skills-graph.mmd -o site/public/graphs/skills-graph-fallback.svg

      - name: Build static site
        run: npm run build --prefix site
        env:
          NEXT_PUBLIC_BASE_PATH: /ideal-lab

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/out

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 12.3 仓库配置

- 仓库 **Settings → Pages → Source** 选 "GitHub Actions"（不是 "Deploy from a branch"）
- 首次部署前需把 main 分支保护规则允许 bot push
- 自定义域名（可选）：放 `site/out/CNAME` 或 `site/public/CNAME`，build 时复制到 `out/`

### 12.4 注意

- `plugins/**` 改动也要触发站点 build——因为 `site/src/lib/plugins.ts` 是 build-time IO
- 不做客户端轮询；不做 SSE
- 部署目标：**GitHub Pages（项目页 `MTleen.github.io/ideal-lab`）**
- basePath 必须在 `next.config.ts` 里 hardcode，**不**读 `process.env.NEXT_PUBLIC_BASE_PATH`（避免 build 飘）

---

## 13. 实施阶段（4 个 sprint）

| Sprint | 内容 | 验收 |
|--------|------|------|
| **S1 设计系统迁移** | `globals.css` 应用 design-system.md 全部 token；字体加载（已有）；dark mode（已有）；新增图谱/Mini Graph 专用 token | Lighthouse 100/100/100/100；dark mode 切换通过 |
| **S2 数据层** | `lib/graph.ts`、`lib/tasks.ts`、`lib/plugin-pain-points.ts`、`lib/skill-summary.ts`、`data/tasks.json`（13 个）、`data/plugin-pain-points.json`（≥8/11） | build-time 校验全部通过：所有 task 的 skillId 在 graph 中存在；所有 plugin-pain-points 的 slug 是真实 plugin |
| **S3 首屏图谱 + 任务面板** | `GraphCanvas.tsx` + `GraphLegend.tsx` + `GraphControls.tsx` + `TaskPanel.tsx` + `TaskCard.tsx` + `TaskScriptView.tsx` + 首页重写 | Playwright 截图首屏；Lighthouse mobile 性能 ≥ 90；键盘导航通过 axe-core；URL 持久化通过 |
| **S4 Plugin/Skill 详情页 + TOC + Mini Graph + CI** | `PluginHero` / `PluginPainPoints` / `PluginMetrics` / `PluginSkillList` + `SkillCapabilities` / `SkillPainPoints` / `SkillRelated` / `SkillToc` / `MiniGraph` + 详情页重写 + `next.config.ts` 改 `output: 'export'` + `basePath: '/ideal-lab'` + `.github/workflows/deploy-site.yml` + `public/graphs/skills-graph-fallback.svg` | 跑通 11 plugin × 3 skill 详情页无报错；TOC 折叠在长 SKILL.md 上正确工作；`next build` 成功生成 `site/out/`；CI 部署一次验证 `https://MTleen.github.io/ideal-lab` 1-3 分钟可见；所有静态资源 URL 包含 `/ideal-lab/` 前缀 |

---

## 14. 风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 46 节点力导向在低端机卡顿 | 中 | 高 | react-force-graph-2d 用 worker；不行降级为 d3-force 静态布局 |
| tasks.json 中 13 个任务 skillId 拼错 | 中 | 中 | S2 末尾 build-time check |
| 痛点卡内容"看起来像编的" | 高 | 中 | 留空比编造好；S4 至少 8/11 plugin 有真实内容 |
| SKILL.md 渲染破坏现有 prose 样式 | 低 | 中 | 不改 `.prose`；只改外层 wrapper |
| **Next.js 16 静态导出与某未来需求冲突**（如想加 SSR 端 endpoint） | 中 | 高 | 节 12.1 列出禁止项；如未来需要 server runtime，必须迁出 GitHub Pages |
| 13 个任务的 skillId 在 skills-graph.json 中已变 | 低 | 中 | build-time check 兜底 |
| 移动端图谱 pinch-zoom 兼容性 | 低 | 低 | react-force-graph-2d 内置支持；不行则禁用移动端图谱 |
| basePath / assetPrefix 漏改导致资源 404 | 中 | 高 | next.config.ts 改动在 S1 末尾 + S4 部署前再核对 |
| mermaid CLI 渲染 fallback SVG 在 CI 超时 | 低 | 中 | CI 加 60s 超时；fallback 不是关键路径 |

---

## 15. 验收标准

- **首页加载**：LCP < 2.5s，CLS < 0.1，TBT < 300ms（Lighthouse mobile）
- **图谱交互**：拖动/缩放/hover/点击 100 次操作 0 报错
- **a11y**：axe-core 0 critical issue
- **dark mode**：所有页面色彩对比度 ≥ 4.5:1
- **真实内容**：13 任务 skillId 100% 在 graph 中存在；plugin 痛点 0 编造
- **可访问 fallback**：禁用 JS 时降级为 SVG 海报 + 文字 + /plugins 链接
- **CI 准实时**：push 后 1-3 分钟线上反映

---

## 16. 反风格声明（不要做的事）

- ❌ 不用 AI 生成大渐变 Hero 背景
- ❌ 不用浮在图谱上的大块玻璃态浮动卡
- ❌ 不用 3D 旋转、粒子背景、shader 特效
- ❌ 不用侧栏 drawer 折叠做任务过滤（图谱旁固定列更直接）
- ❌ 不引入 framer-motion（CSS animation + react state 足够；少 30KB）
- ❌ 不在 Plugin 痛点卡里写百分比（"提升 X%"）
- ❌ 不在 Skill 详情页"它能做什么"section 里编造内容
- ❌ 不做多任务叠加高亮
- ❌ 不做实时 SSE / WebSocket
- ❌ 不做客户端数据轮询

---

## 17. 开放问题（implementation phase 决定）

| 问题 | 决策 | 备注 |
|------|------|------|
| 部署目标平台 | ✅ **GitHub Pages 项目页** `MTleen.github.io/ideal-lab` | 节 12 完整定义 |
| Next.js 输出模式 | ✅ **`output: 'export'`**（静态导出） | GitHub Pages 强制 |
| Base path | ✅ **`/ideal-lab`** | hardcode in `next.config.ts` |
| 痛点卡第一版完整度 | 8/11 plugin 有内容 | 用户确认是否接受留空 |
| 字体加载 | 保留 Satoshi（Fontshare CDN） | 已有 |
| 导出 PNG | 工具栏预留位置，逻辑 P2 | 实施时定 |
| i18n | 首版中文；预留 P2 | 实施时定 |

---

**End of spec. Ready for review.**
