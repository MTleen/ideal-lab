# idealab 展示站重构 — 实施计划

- **日期**：2026-06-05
- **依据**：`docs/superpowers/specs/2026-06-05-idealab-showcase-redesign-design.md`
- **状态**：待开始
- **目标产物**：`https://MTleen.github.io/ideal-lab` 展示站 v2

---

## 0. 范围与非范围

继承 spec 节 2。本计划只展开 **how**，不重复 **what / why**（在 spec 里）。

**关键约束提醒**：
- 部署目标：GitHub Pages 项目页（**不是** Vercel/Cloudflare）
- Next.js 16 + `output: 'export'` + `basePath: '/ideal-lab'`
- 静态导出禁止 SSR endpoint / API route / cookies() / headers()
- 完整 4 sprint 计划 + commit 节点

---

## 1. 仓库准备

### 1.1 锁定依赖版本

执行前在仓库根跑一次：

```bash
node --version    # 期望 ≥ 20
cd site && npm ls next    # 期望 next@16.2.6
cd site && npm ls tailwindcss    # 期望 tailwindcss@4
```

### 1.2 启用 basePath 验证

**S1 第一步**必须验证 `site/next.config.ts` 的基础配置——读、跑、确认输出。

```bash
cd site
npm run dev    # 跑起来，访问 http://localhost:3000
# 验证：所有资源 URL 是 / 开头（dev mode 不用 /ideal-lab 前缀）
```

**S4 第一步**改 `next.config.ts` 加 `output: 'export'` + `basePath: '/ideal-lab'` 后再跑 dev，必须把所有资源都加前缀。

### 1.3 Git 工作流

按 AGENTS.md 规则：
- **plugin 内容改动** → `/ideal-lab-maintainer:maintainer commit`（自动 changeset + bump）
- **site/ 改动**（本计划主体）→ 裸 git commit OK（不影响 plugin 版本号）
- **spec / plan / docs/** 改动 → 裸 git commit OK

**commit 规范**（沿用 spec 已有的 commit 风格）：
```
feat(site): add GraphCanvas with react-force-graph-2d
fix(site): correct basePath for static export
docs(site): document plugin pain points
chore(site): bump next config for static export
refactor(site): extract TaskPanel from HomeClient
```

---

## 2. Sprint 1 — 设计系统迁移（1-2 天）

**目标**：把 `docs/design-system.md` 的所有 token 全部接入 `globals.css`，新增图谱/Mini Graph 专用 token。

### S1.1 起点

- 起点状态：`globals.css` 已有完整 token 系统（见 `site/src/app/globals.css` 第 7-83 行）
- 大部分 design-system.md 已落地，**差距在**：
  1. 没有 graph 专用 token
  2. 没有 mini graph 专用 token
  3. 字体加载（Fontshare CDN）已在，但需要确认 bundle 不重复加载

### S1.2 Todos

- [ ] **读** `docs/design-system.md` 全文 + 当前 `globals.css` + 当前 `tailwind.config.*`（如有）
- [ ] **加** graph 专用 token 到 `:root` 和 `.dark`：
  - `--graph-node-default-fill`
  - `--graph-node-hover-glow` (rgba)
  - `--graph-edge-enhancement` (#a3a3a3)
  - `--graph-edge-prerequisite` (brand)
  - `--graph-edge-embeds` (content)
  - `--graph-edge-produces-for` (research)
  - `--graph-edge-alternative` (tooling)
  - `--graph-plugin-halo` (rgba，虚线圆颜色)
  - `--graph-task-highlight` (rgba)
- [ ] **加** mini graph 专用 token（subset of graph + 简化的色板）
- [ ] **加** TOC 专用 token（sticky 偏移、border、text 层级）
- [ ] **加** task panel 专用 token（卡片背景、选中态、过滤态）
- [ ] **验证** dark mode 下所有新 token 都自动切换（用 `.dark { ... }` 覆盖）
- [ ] **跑** Lighthouse 100/100/100/100 验证（desktop + mobile）
- [ ] **commit** `feat(site): extend design tokens for graph and task panel`

### S1.3 验收

- `site/out/`（s4 之后才有）目录所有 CSS 不超过 **30KB** gzipped
- Lighthouse mobile Performance ≥ 95
- dark mode 切换无闪烁（看 `layout.tsx` 已有 inline script）
- 所有 token 命名一致 `--bp-{scope}-{prop}` 风格

### S1.4 风险

| 风险 | 缓解 |
|------|------|
| 现有 prose 样式被新 token 覆盖 | **不改 `.prose` block**（spec 节 11.4 约束） |
| Fontshare CDN 偶发慢 | 已有降级栈 `system-ui, -apple-system, sans-serif` |

---

## 3. Sprint 2 — 数据层（1-2 天）

**目标**：13 个任务 + 41 条 plugin 痛点 + 41 个 skill edge 全部 build-time 可加载，校验 100% 通过。

### S2.1 起点

- 起点状态：
  - `skills-graph.json` 已存在（41 节点 / 183 边 / 5 关系）—— `cat skills-graph.json | jq '.metadata'`
  - `plugin-pain-points-data.json` **spec 阶段已起草**（41 条，12 plugin）—— `docs/superpowers/specs/plugin-pain-points-data.json`
  - `tasks.json` **未起草**—— 需现在写（13 个任务，参考 spec 节 6.3）

### S2.2 Todos — tasks.json 起草

按 spec 节 6.3 的 13 个任务表，逐个**查 skills-graph.json 验证**：

```bash
# 1. 拿 nodes
jq '.nodes[].id' skills-graph.json | sort > /tmp/nodes.txt

# 2. 写 tasks.json 草稿（13 个），每个 task 的 skillIds 必须是 /tmp/nodes.txt 里的真值
```

**13 个任务的 skillIds 收集指南**（基于 skills-graph.json 实际节点，不是编的）：

| task.id | 涉及的 skill 路径 |
|---------|-------------------|
| `make-ppt` | `ideal-ppt-suite/ideal-ppt-workflow` + 7-8 个子 skill（workflkow 编排） |
| `deep-research-topic` | `ideal-deep-research/deep-research` + `ideal-ppt-suite/ideal-ppt-requirement`（如适用） |
| `full-dev-cycle` | `ideal-dev-workflow` 下全部 14 个 skill |
| `review-solution` | `ideal-dev-workflow/ideal-code-review` + `panel-review/panel-review` + `ideal-dev-workflow/ideal-debugging` |
| `write-solution` | `ideal-dev-workflow/ideal-dev-solution` + `ideal-dev-workflow/ideal-dev-plan` |
| `generate-test-cases` | `ideal-dev-workflow/ideal-test-case` |
| `exec-and-review` | `ideal-dev-workflow/ideal-dev-exec` + `ideal-dev-workflow/ideal-code-review` + `ideal-dev-workflow/ideal-test-exec` |
| `build-knowledge-base` | `ideal-knowledge-base/build-knowledge-base-workflow` + 4 个阶段 skill |
| `write-long-doc` | `ideal-document-workflow/ideal-document-workflow` + 6 个子 skill |
| `generate-images` | `baoyu-image-gen/baoyu-image-gen` + `ideal-ppt-suite/ideal-ppt-image` |
| `generate-dify-dsl` | `ideal-dify-generator/ideal-dify-generator` |
| `maintain-ideal-lab` | `ideal-lab-maintainer/ideal-lab-maintainer` |
| `optimize-skill` | `skill-builder/skill-builder` + `panel-review/panel-review` |

**写时跑**：

```bash
# 边写边验证
while true; do
  vim site/src/data/tasks.json
  node -e "import('./site/src/data/tasks.json', {assert: {type: 'json'}}).then(t => {
    const nodes = new Set(require('./skills-graph.json').nodes.map(n => n.id));
    for (const task of t.default) {
      for (const id of task.skillIds) {
        if (!nodes.has(id)) console.error('MISSING:', task.id, '->', id);
      }
    }
    console.log('OK,', t.default.length, 'tasks');
  })"
done
```

### S2.3 Todos — 复制痛点数据

```bash
cp docs/superpowers/specs/plugin-pain-points-data.json site/src/data/plugin-pain-points.json
```

### S2.4 Todos — 写 4 个 lib

- [ ] `site/src/lib/graph.ts`：
  ```ts
  import graphData from "../../../skills-graph.json";
  export interface GraphNode { id: string; name: string; plugin: string; category: string; arity: string; description: string; }
  export interface GraphEdge { source: string; target: string; relation: "enhancement" | "prerequisite" | "embeds" | "produces_for" | "alternative"; }
  export const graphNodes: GraphNode[] = graphData.nodes;
  export const graphEdges: GraphEdge[] = graphData.edges;
  export function getNodeInDegree(id: string): number {
    return graphEdges.filter(e => e.target === id).length;
  }
  export function getPluginCluster(slug: string): GraphNode[] {
    return graphNodes.filter(n => n.plugin === slug);
  }
  export function getRelated(skillId: string): { upstream: GraphNode[]; downstream: GraphNode[]; enhancement: GraphNode[] } {
    // ... 反查
  }
  ```
- [ ] `site/src/lib/tasks.ts`：
  - `loadTasks()` 读 `site/src/data/tasks.json`
  - `getTask(id)` 拿单个
  - `validateTaskIds()` build-time 校验（节 11.1 规则）
- [ ] `site/src/lib/plugin-pain-points.ts`：
  - `loadPainPoints()` 读 `site/src/data/plugin-pain-points.json`
  - `getPluginPainPoints(slug)` 拿单个
  - `validatePluginSlugs()` build-time 校验（节 11.2 规则）
- [ ] `site/src/lib/skill-summary.ts`：
  - 给定 SKILL.md content，解析 H2 标题 + 第一句描述
  - 用 `remark-parse` + 简单 walk AST（不加新依赖）
  - 返回 `{ capabilities: string[], toc: {level: number, text: string}[] }`

### S2.5 验收

```bash
cd site
npm run build
# 必须无 warning 提到 tasks/pain-points 数据
# build 输出 site/out/ 目录
```

- 13 个 task 全部在 `tasks.json`
- 12 plugin 全部在 `plugin-pain-points.json`（合计 41 条）
- build-time 校验函数 0 抛错
- 每个 task 的 skillIds 100% 在 `skills-graph.json` 中存在

### S2.6 风险

| 风险 | 缓解 |
|------|------|
| 13 个任务的 skillIds 拼写错 | build-time 校验先于 build 跑 |
| `skills-graph.json` 节点名改了但 spec 没改 | build-time 校验报错时同步更新 spec |
| `plugin-pain-points.json` 复制后键名与 plugin slug 不一致 | 复制后跑 `validatePluginSlugs()` |

---

## 4. Sprint 3 — 首屏图谱 + 任务面板（3-5 天）

**目标**：重写首页，左侧 70% 知识图谱，右侧 30% 任务面板，可拖可点可过滤。

### S3.1 起点

- 起点状态：
  - `site/src/app/page.tsx` 已是 Hero + grid 布局（保持作为参考）
  - `site/src/app/HomeClient.tsx` 是"使用 client"组件，含搜索 + 分类 + 时间线
  - 任务面板 / 图谱 / 剧本视图 **完全不存在**——从零写

### S3.2 决策点（实施时定，不需要问用户）

| 决策 | 取值 | 理由 |
|------|------|------|
| `dynamic` 引入 react-force-graph-2d | `dynamic(() => import('@/components/graph/GraphCanvas'), { ssr: false })` | 跳 SSR（spec 节 7.4 约束） |
| d3-force 调参常量 | 写死 `components/graph/forces.ts` 常量文件 | spec 节 7.3 数值 |
| 任务面板状态管理 | React `useState` + URL `useSearchParams` | spec 节 7.6 约束 |
| 关系类型过滤 | 5 个 checkbox，state 写 URL | spec 节 8.1 |
| 单任务聚焦 | 同一时间 1 个任务高亮，URL `?task=xxx` | spec 节 8.1 |
| 静态 fallback | build-time 渲染 SVG 海报到 `public/graphs/skills-graph-fallback.svg` | spec 节 7.8 + 11.3 |
| 节点 Plugin 聚类 halo | 虚线圆，半径 = 同 plugin skill 包围盒 + 20px | spec 节 7.1 |
| 反向联动 | hover 节点 → 任务面板加 brand 边框 | spec 节 7.6 |

### S3.3 Todos

#### S3.3.1 安装依赖

```bash
cd site
npm install react-force-graph-2d
npm install -D @types/d3-force
```

#### S3.3.2 创建组件

- [ ] `components/graph/GraphCanvas.tsx`：
  - props: `{ nodes, edges, highlightedSkillIds, dimOthers, onNodeClick, onNodeHover }`
  - 用 `useRef` + `useEffect` 初始化 `ForceGraph2D`
  - 配置力学参数（spec 节 7.3）
  - 节点渲染：圆 + category 色 + 大小按 inDegree
  - 边渲染：5 种样式（spec 节 7.2 表）
  - Plugin 聚类 halo：用 hidden intra-plugin edges 拉近
  - 高亮 / dim：根据 props 应用 opacity
  - tooltip：自有 DOM 浮层（react-force-graph-2d 不内置）
  - 节点 click：调 `onNodeClick` → 跳 `/plugins/${plugin}/skills/${slug}`
  - 节点 hover：调 `onNodeHover` → 设置 state → 任务面板响应
  - a11y：键盘 Tab + Enter 跳转（spec 节 7.7）
  - **关键**：用 `useMemo` 缓存 `graphData` 对象，避免每次渲染都重算
- [ ] `components/graph/GraphLegend.tsx`：
  - 5 个关系类型小色块 + 文字
  - 固定位置：图谱左下角
- [ ] `components/graph/GraphControls.tsx`：
  - 3 个按钮：重置 / 全屏 / 导出（导出 P2 可留 stub）
  - 固定位置：图谱右下角
- [ ] `components/tasks/TaskPanel.tsx`：
  - props: `{ tasks, onSelect, selected, hoveredSkillId }`
  - 任务列表（13 张卡）
  - 关系类型过滤（5 个 checkbox）
  - [清空过滤] 按钮
  - mobile：折叠为顶部按钮
- [ ] `components/tasks/TaskCard.tsx`：
  - props: `{ task, isSelected, isHighlighted, onClick }`
  - 标题 + skill 数 + Plugin 徽章
  - hover 态 + 选中态样式
- [ ] `components/tasks/TaskScriptView.tsx`：
  - props: `{ task, onClose }`
  - drawer 式展开（不切页）
  - 显示痛点 + 步骤列表（点步骤跳 skill 详情）
- [ ] `components/PluginCard.tsx`（已有）+ `components/SearchBar.tsx`（已有）：保留

#### S3.3.3 重写首页

- [ ] `site/src/app/page.tsx`：
  - 删除现有 Hero（替换为 hero band + 数据徽章）
  - 主体：`<GraphCanvas>` + `<TaskPanel>` 左右分栏
  - 底部：4 张痛点卡 + 11 张 Plugin 索引卡 + 时间线
- [ ] `site/src/app/HomeClient.tsx`（重写）：
  - state: `selectedTaskId`, `selectedRelations`, `hoveredSkillId`
  - 同步 URL: `useSearchParams` + `router.replace`
  - 计算 `highlightedSkillIds`: 从 selected task 的 skillIds 拿
  - 提供给 `GraphCanvas` 和 `TaskPanel`
  - 监听 `GraphCanvas` 的 `onNodeHover` 更新 `hoveredSkillId`

#### S3.3.4 静态 fallback

- [ ] CI 步骤（`deploy-site.yml`）加 mermaid CLI 渲染：
  ```bash
  npx -p @mermaid-js/mermaid-cli mmdc -i docs/skills-graph.mmd -o site/public/graphs/skills-graph-fallback.svg
  ```
- [ ] `GraphCanvas` 加 `if (typeof window === 'undefined' || !canvasRef.current) return <img src="/ideal-lab/graphs/skills-graph-fallback.svg" />`

### S3.4 验收

- **Lighthouse mobile**：Performance ≥ 90，Accessibility ≥ 95
- **a11y**：axe-core 跑首页 0 critical issue
- **键盘**：Tab 焦点节点（按入度降序），Enter 跳转
- **URL 持久化**：`?task=make-ppt&rel=prerequisite,enhancement` 刷新后状态保留
- **拖动帧率**：Chrome devtools 录制 ≥ 55fps
- **静态 fallback**：禁用 JS 时显示 SVG 海报
- **Playwright 截图**：首屏 + 任务聚焦态 + 关系过滤态各一张

### S3.5 风险

| 风险 | 缓解 |
|------|------|
| react-force-graph-2d bundle 大 | 检查 `dist/`：>200KB 报告 |
| d3-force 力学调参需要 5+ 轮迭代 | 留 1 天 buffer；先看效果再调 |
| 任务面板 mobile 折叠交互 | 用 `details/summary` 或 headlessui `Disclosure` |
| 静态 fallback SVG 在 mermaid 渲染失败 | build-time 报错（fail fast），不强降级 |

### S3.6 commit 节点

```
S3-A: feat(site): install react-force-graph-2d
S3-B: feat(site): add GraphCanvas component with force-directed layout
S3-C: feat(site): add GraphLegend and GraphControls
S3-D: feat(site): add TaskPanel and TaskCard
S3-E: feat(site): rewrite homepage with graph + task panel
S3-F: feat(site): add TaskScriptView and reverse-link from graph
S3-G: chore(site): add mermaid CLI fallback SVG generation
S3-H: test(site): Playwright screenshot for 3 states
```

---

## 5. Sprint 4 — Plugin/Skill 详情页 + TOC + Mini Graph + CI（4-6 天）

**目标**：重写详情页 + 加 TOC 折叠 + Mini Graph + GitHub Pages CI/CD。

### S5.1 起点

- 起点状态：
  - `site/src/app/plugins/[plugin]/page.tsx` 已有基础版（重写）
  - `site/src/app/plugins/[plugin]/skills/[skill]/page.tsx` 已有（重写）
  - `site/src/lib/plugins.ts` 已有 `loadPlugin` 和 `loadSkill`（保留）
  - `site/next.config.ts` 已有 `nextConfig`（改静态导出）
  - **没有** `MiniGraph`、`SkillToc`、`SkillRelated`
  - **没有** `static export` 配置
  - **没有** `.github/workflows/deploy-site.yml`

### S5.2 决策点

| 决策 | 取值 | 理由 |
|------|------|------|
| `static export` 改 next.config | `output: 'export'` + `basePath: '/ideal-lab'` + `assetPrefix: '/ideal-lab'` + `images: { unoptimized: true }` + `trailingSlash: true` | spec 节 12.1 |
| Mini Graph 实现 | SVG + d3-force 直接调（**不**用 react-force-graph-2d） | spec 节 5.4 注释 |
| Mini Graph 触发 | 点"上下游 skill"中任一项 → 内联展开（`<details>` 元素） | spec 节 5.4 |
| TOC 提取 | 从已渲染 DOM 读 H2/H3（**不**解析 markdown 两次） | spec 节 10.2 |
| TOC 折叠阈值 | H2 超过 8 个时折叠最深的 3 个 | spec 节 10.2 |
| 部署目标 | GitHub Pages（项目页 `MTleen.github.io/ideal-lab`） | spec 节 12 |
| 仓库 Pages Source | "GitHub Actions" | spec 节 12.3 |
| CI 触发 | push to main，paths filter | spec 节 12.2 |

### S5.3 Todos — 详情页

#### S5.3.1 Plugin 详情页重写

- [ ] `components/plugin/PluginHero.tsx`：Hero 数据 + 安装命令
- [ ] `components/plugin/PluginPainPoints.tsx`：3-4 张卡（scroll reveal）
- [ ] `components/plugin/PluginMetrics.tsx`：4 列结构指标
- [ ] `components/plugin/PluginSkillList.tsx`：按 phase 排序
- [ ] 重写 `site/src/app/plugins/[plugin]/page.tsx`：组合上述 4 个组件 + CTA "在图谱中只看本 Plugin"

#### S5.3.2 Skill 详情页重写

- [ ] `components/skill/SkillHeader.tsx`：Phase + 名称 + 副标题
- [ ] `components/skill/SkillCapabilities.tsx`：3-5 个动词句（**空** = section 不显示）
- [ ] `components/skill/SkillPainPoints.tsx`：1-2 段（**空** = section 不显示）
- [ ] `components/skill/SkillRelated.tsx`：上下游 + L4 入口
  - 调 `graph.ts::getRelated(skillId)` 拿数据
  - 每个邻居 `<button>` 触发 `<details>` 展开 mini graph
- [ ] `components/skill/SkillToc.tsx`：右侧浮动目录 + 折叠
  - 从已渲染 DOM 读 H2/H3
  - sticky `top-24`
  - IntersectionObserver 高亮当前章节
- [ ] `components/skill/SkillMdRenderer.tsx`：保留现有 prose 渲染，**只**加 TOC wrapper
- [ ] 重写 `site/src/app/plugins/[plugin]/skills/[skill]/page.tsx`：组合上述

#### S5.3.3 Mini Graph

- [ ] `components/graph-mini/MiniGraph.tsx`：
  - props: `{ centerNode, neighborNodes, edges }`
  - **不**用 react-force-graph-2d
  - 用 `d3-force` 直接算位置（`forceSimulation`）
  - 渲染：SVG `<circle>` + `<line>`，**不**用 `<canvas>`
  - 6-12 节点，100ms 内算完
  - 中心节点高亮（不同色）
- [ ] `components/graph-mini/MiniGraphLegend.tsx`：简化版（只标 center + 邻居方向）

#### S5.3.4 静态导出配置

- [ ] 改 `site/next.config.ts`：
  ```ts
  const nextConfig: NextConfig = {
    output: 'export',
    basePath: '/ideal-lab',
    assetPrefix: '/ideal-lab',
    images: { unoptimized: true },
    trailingSlash: true,
  };
  ```
- [ ] 跑 `npm run build` 验证 `site/out/` 目录生成
- [ ] 跑 `npx serve site/out` 模拟部署，本地访问 `http://localhost:3000/ideal-lab/`（手动加前缀）
- [ ] **关键检查**：浏览首页 + Plugin 详情 + Skill 详情，所有图片/CSS/JS URL 都含 `/ideal-lab/` 前缀

#### S5.3.5 CI/CD

- [ ] 写 `.github/workflows/deploy-site.yml`（spec 节 12.2 完整 YAML）
- [ ] 仓库 Settings → Pages → Source = "GitHub Actions"
- [ ] 第一次手动 push 触发（让 GitHub 创建 environment）
- [ ] 验证 `https://MTleen.github.io/ideal-lab` 1-3 分钟内可见

### S5.4 验收

- **Lighthouse mobile**：Performance ≥ 90，Accessibility ≥ 95
- **静态导出**：`site/out/` 包含完整 `index.html`、`plugins/[slug]/index.html`、`plugins/[slug]/skills/[skill]/index.html`
- **资源前缀**：所有 `<link>` / `<script>` / `<img>` 都有 `/ideal-lab/` 前缀
- **CI 准实时**：push 到 main 1-3 分钟内 `https://MTleen.github.io/ideal-lab` 可见
- **TOC 折叠**：长 SKILL.md（如 ideal-ppt-strategist）正确显示目录 + 折叠最深的 3 个
- **Mini Graph**：点上下游节点 → 内联展开 6-12 节点子图
- **basePath**：直接访问根域 `https://MTleen.github.io/` 显示 404（不显示 ideal-lab）

### S5.5 风险

| 风险 | 缓解 |
|------|------|
| 静态导出与某现有 feature 冲突（如 SSR endpoint） | 实施时检查 `app/api/` 目录是否已存在 |
| basePath 漏改导致 404 | **S5.3.4 跑 build + serve 验证** 必须做 |
| mermaid CLI CI 超时 | CI step 加 `timeout-minutes: 5` |
| 第一次 GitHub Pages 部署失败 | workflow_dispatch 手动重试；看 `Actions` 日志 |

### S5.6 commit 节点

```
S4-A: feat(site): add PluginHero PluginPainPoints PluginMetrics PluginSkillList
S4-B: feat(site): add SkillHeader SkillCapabilities SkillPainPoints SkillRelated
S4-C: feat(site): add SkillToc with right-side sticky nav and folding
S4-D: feat(site): add MiniGraph using d3-force directly
S4-E: refactor(site): rewrite plugin detail page with new components
S4-F: refactor(site): rewrite skill detail page with TOC and MiniGraph
S4-G: chore(site): configure next.config.ts for static export
S4-H: ci(site): add deploy-site workflow for GitHub Pages
S4-I: test(site): verify 12 plugins × 3 skills render without error
S4-J: docs(site): update README with deployment URL
```

---

## 6. 跨 Sprint 任务

### 6.1 README 更新

- [ ] 替换 `MTleen.github.io/ideal-lab` 链接（README.md 旧 GitHub URL）
- [ ] 加 deploy badge
- [ ] 加 lighthouse badge

### 6.2 文档同步

- [ ] `CLAUDE.md` 加 `site/` 静态导出部署说明
- [ ] `site/README.md` 加 `npm run build` 部署说明

### 6.3 Validation

按 `AGENTS.md` 规则，**每次 commit 后**：

```bash
claude plugin validate    # 验证所有 plugin
```

仅 plugin 内容改动需要跑；site 改动不需要。

---

## 7. 跨 Sprint 风险与升级路径

### 7.1 已知风险

| 风险 | 触发条件 | 升级路径 |
|------|----------|----------|
| react-force-graph-2d 在低端机卡顿 | 实测 < 30fps | 降级为 d3-force 静态布局（无交互） |
| GitHub Pages 部署太慢（>5 分钟） | CI 一直 pending | 检查 Actions 队列；手跑 `workflow_dispatch` |
| 13 个任务的 skillIds 频繁变 | 节点改名 | build-time 校验报错时同步更新 tasks.json |
| `site/out/` build 失败 | next 16 静态导出有 breaking change | 卡住则回退到当前 Vercel 部署 + 不动 |
| Mini Graph 渲染性能 | 12 节点拖动卡 | 减少到 8 节点（只显示直接邻居） |

### 7.2 验收节点（每个 sprint 结束必跑）

```bash
# S1 末尾
cd site && npm run build && npm run start
# 验证：现有 /plugins 列表、Plugin 详情、Skill 详情在 dev 下完全没坏
# 验证：Lighthouse 100/100/100/100

# S2 末尾
cd site && npm run build
# 验证：build-time 校验函数 0 抛错

# S3 末尾
cd site && npm run build
npx serve site/out
# 验证：首页 + 图谱 + 任务面板
# 验证：Playwright 3 张截图

# S4 末尾
cd site && npm run build
npx serve site/out
# 验证：12 plugin × 3 skill 详情页全部加载
# 验证：所有资源 URL 含 /ideal-lab/ 前缀
# 验证：GitHub Pages 1-3 分钟内可见
```

---

## 8. 整体验收（4 sprint 全过）

- **Lighthouse mobile**：首页 / Plugin 详情 / Skill 详情 三页 Performance ≥ 90，Accessibility ≥ 95
- **a11y**：axe-core 0 critical
- **dark mode**：所有页面色彩对比度 ≥ 4.5:1
- **真实内容**：13 任务 skillId 100% 在 graph 中；12/12 plugin 痛点；零编造
- **可访问 fallback**：禁用 JS 时降级为 SVG 海报 + 文字 + /plugins 链接
- **CI 准实时**：push → 1-3 分钟内 `https://MTleen.github.io/ideal-lab` 可见
- **basePath**：所有资源 URL 含 `/ideal-lab/` 前缀

---

## 9. 不在范围（提醒）

| 项 | 原因 |
|----|------|
| 实时推送（SSE/WebSocket） | 公开展示站无多人协作 |
| 客户端轮询 | 46 节点数据小，CI 准实时足够 |
| 用户登录、收藏、评论 | 单向展示 |
| 图谱节点搜索 | 复用 /plugins 搜索 |
| 多任务叠加高亮 | 单任务保持对比 |
| 国际化 | 首版中文 |
| 移动端图谱拖动 | pinch-zoom 已支持 |
| 导出 PNG | 工具栏预留，P2 |
| FRP 创作系统 | 静态数据，P2 |

---

## 10. 升级 / Rollback

每个 sprint 末尾是 **commit boundary**。S1 / S2 / S3 任意一个失败：

```bash
git revert <commit-sha>    # 回滚
# 或
git reset --hard <previous-commit>  # 强制回滚
```

S4 末尾 CI 部署后：

- 站点回滚：仓库 Settings → Pages → 选 "Deploy from a branch" 临时回退到 main branch 的 `site/out/` 旧版
- 或 git revert S4 commits 重新触发 CI

---

**End of plan. Ready to start S1.**
