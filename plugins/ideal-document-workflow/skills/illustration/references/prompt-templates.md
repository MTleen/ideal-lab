# AI 图片生成 Prompt 模板

## 调用方式

对于架构图、数据图、原型图等，调用 `baoyu-image-gen`：

```bash
# 确定脚本路径
baseDir="/Users/mathrippermacmini/.claude/skills/baoyu-image-gen"

# 设置 Google Native API（via 老张）
export GOOGLE_API_KEY="sk-xS0aIvt5ESBqgGPu56AcEc4932264a6b8fCcD8A9Aa75DbC3"
export GOOGLE_BASE_URL="https://api.laozhang.ai/v1beta"

cd "{项目目录}/文档产出"

# 生成架构图
npx -y bun $baseDir/scripts/main.ts \
  --promptfiles sections/images/prompts/01-framework-xxx.md \
  --image sections/images/01-framework-xxx.png \
  --ar 16:9 --quality 2k --provider google
```

## Prompt 构造要点（学术白底风格）

- **白色背景**（必须）：`Background: Pure white (#FFFFFF). No dark backgrounds.`
- **中文标签**（必须）：所有文字标签使用中文，仅在其他语言的专有名词时使用英文（如 API、URL 等约定俗成的术语）
- 学术论文风格：简洁、专业、几何化，避免花哨装饰
- 核心组件配图标：用通用图标符号表示（数据库=圆柱、API=↔、用户=👤、服务=⚙）
- 包含具体的技术术语和数值
- 布局清晰，分区明确
- 色彩语义化且克制（蓝色=接入/接口，青色=服务层，紫色=数据层，灰色=基础设施）
- 无渐变、无阴影、无复杂纹理

## Prompt 示例

### 架构图 — 学术白底风格

```
Technical system architecture diagram. Academic paper style.

BACKGROUND: Pure white (#FFFFFF). No gradients, no shadows, no textures.

Layout: Top-down hierarchical, 3 layers.

ZONES:
- Zone 1 (Top): API Gateway / User Interface layer
  → Icon: ↔ (bidirectional arrows) for gateway
  → Label: "接入层" in Chinese
- Zone 2 (Middle): Core Services layer
  → Icon: ⚙ (gear) for each service module
  → 3 service modules with icons: 用户服务 ⚙ / 业务服务 ⚙ / 数据服务 ⚙
  → Label: "服务层" in Chinese
- Zone 3 (Bottom): Data Persistence layer
  → Icon: ⧈ (cylinder) for database
  → 3 data stores: 主数据 ⧈ / 业务数据 ⧈ / 日志数据 ⧈
  → Label: "数据层" in Chinese

CONNECTIONS: Clean straight lines with directional arrows. No curved lines.
Clean geometric containers: rounded rectangles with 1px solid borders. No fill (white/transparent fill).

Colors:
- Gateway: Blue (#2563EB) outline
- Service modules: Teal (#0D9488) outline
- Data stores: Purple (#7C3AED) outline
- All text: Dark gray (#374151) or black
- Borders: 1px solid, matching component color

Style: Academic / technical diagram. Flat design, white background, precise layout, clean lines, minimal decoration. Each component has a clear icon. Text labels in Chinese. Professional and formal.
ASPECT: 16:9
```

### 数据流图 — 学术白底风格

```
Data flow diagram. Academic paper style.

BACKGROUND: Pure white (#FFFFFF). No gradients, no shadows, no textures.

Layout: Left-to-right horizontal flow.

PROCESS NODES:
- Node 1 (Left): Data Input
  → Icon: → (arrow pointing in)
  → Label: "数据采集" in Chinese
- Node 2 (Center): Processing
  → Icon: ⚙ (gear) for processing
  → Label: "数据处理" in Chinese
  → 3 sub-processes with icons
- Node 3 (Right): Output
  → Icon: ⬇ (arrow pointing down)
  → Label: "数据输出" in Chinese

FLOWS:
- Clean arrows showing data direction
- Labels on arrows in Chinese
- Flow 1: "原始数据" → "清洗" → "转换" → "加载"
- Flow 2: "质量报告" from quality check

Colors:
- Input nodes: Blue (#2563EB) outline
- Processing nodes: Teal (#0D9488) outline
- Output nodes: Purple (#7C3AED) outline
- All text: Dark gray (#374151)
- Arrows: Gray (#6B7280)

Style: Academic / technical diagram. Flat design, white background, precise layout, clean lines. Text labels in Chinese. Professional and formal.
ASPECT: 16:9
```

### 技术路线图 — 学术白底风格

```
Technology roadmap diagram. Academic paper style.

BACKGROUND: Pure white (#FFFFFF). No gradients, no shadows, no textures.

Layout: Timeline with phases.

TIMELINE PHASES:
- Phase 1 (Q1): 基础能力建设
  → 4 milestones with icons
- Phase 2 (Q2-Q3): 核心功能开发
  → 6 milestones with icons
- Phase 3 (Q4): 试点与优化
  → 3 milestones with icons

MILESTONE MARKERS:
- Completed: ✓ (check mark)
- In Progress: ● (filled circle)
- Planned: ○ (empty circle)

Colors:
- Phase 1: Blue (#2563EB)
- Phase 2: Teal (#0D9488)
- Phase 3: Purple (#7C3AED)
- All text: Dark gray (#374151)
- Timeline: Gray (#6B7280)

Style: Academic / technical diagram. Flat design, white background, precise layout, clean lines. Text labels in Chinese. Professional and formal.
ASPECT: 16:9
```
