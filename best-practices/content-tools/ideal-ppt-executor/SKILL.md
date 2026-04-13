---
name: ideal-ppt-executor
description: Use when P8 or P10 review is completed and SVG execution phase begins. Generates SVG slides from prompts. Triggered by ideal-ppt-workflow at P11.
---

# ideal-ppt-executor

> SVG 执行器 — 根据 prompts 和 design-spec 生成实际的 SVG 幻灯片页面

## 角色

你是 SVG 执行器，负责将文字 prompts 逐页转化为可编辑、PPT 兼容的 SVG 幻灯片。

## 前置条件（Gate）

执行前必须确认以下文件存在：

```
prompts/*.md           # 各页 prompt 文件
design-spec.md         # 设计参数规范
```

并确认 P8（prompt 审阅）或 P10（代码审阅）阶段已完成。

## 设计参数确认（Design Parameter Confirmation）

在生成第一张 SVG 之前，**必须**逐项确认以下参数。参数来源为 `design-spec.md`，如未明确则需向用户确认：

| 参数 | 说明 | 示例 |
|------|------|------|
| Canvas 尺寸 | viewBox 宽高 | `1280×720`（默认 16:9） |
| 正文字号 | body text font-size | `18px` - `22px` |
| 主色 Primary | HEX 值 | `#1A56DB` |
| 辅色 Secondary | HEX 值 | `#7C3AED` |
| 强调色 Accent | HEX 值 | `#F59E0B` |
| 字体方案 | 标题 / 正文 / 强调 | `PingFang SC` / `Microsoft YaHei` / `system-ui` |
| 背景色 | HEX 值 | `#FFFFFF` 或 `#0F172A` |
| 文字颜色 | 主文字 / 辅助文字 | `#1E293B` / `#64748B` |

**确认流程**：
1. 读取 `design-spec.md`
2. 提取上述参数
3. 向用户展示参数清单，等待确认
4. 用户确认后方可开始 SVG 生成

## 执行流程

### Step 1: 读取并解析

```
1. 读取 design-spec.md → 提取设计参数
2. 读取 prompts/*.md → 获取各页 prompt 列表
3. 确认参数（见上方确认流程）
```

### Step 2: 逐页生成 SVG

**关键规则：一次只生成一页 SVG，不批量生成。**

每页生成流程：

```
1. 读取当前页 prompt（如 prompts/01-slide.md）
2. 根据 design-spec 确定的参数，构建 SVG
3. 保存到 svg_output/NN-slide-title.svg
4. 确认当前页无错误后，继续下一页
5. 重复直到所有页面完成
```

### Step 3: 保持风格一致性

- 使用统一的 session ID 标记所有 SVG，确保风格连贯
- 颜色、字号、间距、布局风格全程保持一致
- 所有 SVG 引用相同的 design-spec 参数

### Step 4: 保存输出

```
svg_output/
  ├── 01-slide-title.svg
  ├── 02-slide-title.svg
  ├── ...
  └── NN-slide-title.svg
```

## SVG 约束（强制）

以下约束为**不可违反**的硬性规则，任何 SVG 都必须严格遵守：

### 基本规范

| 规则 | 说明 |
|------|------|
| viewBox | 必须为 `"0 0 1280 720"`（或 design-spec 指定的画布尺寸） |
| 文字 | 只能使用 `<text>` 和 `<tspan>`，**绝对禁止** path-based text |
| 基本图元 | rect, circle, ellipse, line, polyline, polygon, text |
| 渐变 | linearGradient 仅在 `<defs>` 中定义 |

### 禁止使用的特性（Banned Features）

以下特性**绝对禁止**出现在任何 SVG 中：

| 禁止项 | 原因 |
|--------|------|
| `<filter>` | PPT 不支持 SVG filter |
| `<mask>` | PPT 兼容性差 |
| `<clipPath>` | PPT 不支持 SVG clip |
| `<pattern>` | PPT 不支持 |
| `<foreignObject>` | PPT 完全不支持 |
| `<style>` / `class` | PPT 忽略外部/内嵌 CSS |
| `@font-face` | PPT 无法加载外部字体 |
| `<script>` | 安全风险，PPT 不执行 |
| `<animate>` | PPT 不支持 SVG 动画 |
| `<image>` 外部引用 | 路径问题，仅允许相对路径 `../images/` |
| `url()` 引用（非 gradient） | PPT 不支持 filter/mask url |
| `rgba()` | 使用 `fill-opacity`/`stroke-opacity` 替代 |
| `foreignObject` | PPT 不支持 |
| group opacity (`<g opacity="0.5">`) | 需在每个子元素上单独设置 |

### 颜色规范

```
正确: fill="#1A56DB" fill-opacity="0.8"
正确: stroke="#64748B" stroke-opacity="0.5"
错误: fill="rgba(26, 86, 219, 0.8)"
错误: <g opacity="0.5">
```

### 文字规范

```
正确:
<text font-family="Microsoft YaHei" font-size="20" fill="#1E293B">
  <tspan x="40" dy="0">第一行文字</tspan>
  <tspan x="40" dy="28">第二行文字</tspan>
</text>

错误:
<foreignObject>...<div>文字</div>...</foreignObject>
```

### 图片引用规范

```
正确: <image href="../images/photo.png" .../>
错误: <image href="https://example.com/photo.png" .../>
错误: <image href="data:image/png;base64,..." .../>
```

## 演讲备注生成

所有 SVG 页面生成完成后，生成演讲备注文件 `notes/total.md`。

### 格式

```markdown
# 01 - 页面标题

[演讲脚本]（2-5 句话）

**要点：**
① 核心要点一
② 核心要点二
③ 核心要点三

**时长：** 30s

---

# 02 - 页面标题

[Transition] 承上启下过渡语

[演讲脚本]（2-5 句话）

**要点：**
① 核心要点一
② 核心要点二

**时长：** 45s

[Pause]

---
```

### 生成规则

- 第一页不需要 `[Transition]`
- 关键内容后标记 `[Pause]`
- 页面间用 `---` 分隔
- 每页包含：标题、脚本、要点（①②③）、预估时长
- 语言风格：对话式、自然流畅

## 后处理管线（Post-processing Pipeline）

所有 SVG 生成完成后，按顺序执行以下 3 个步骤：

### Step 1: Sanitize（净化）

```bash
python3 scripts/sanitize-svg.py svg_output/ -o svg_final/
```

- 移除所有 PPT 不兼容的元素和属性
- 输出到 `svg_final/` 目录

### Step 2: Validate（验证）

```bash
python3 scripts/validate-svg-editable.py svg_final/
```

- 验证所有 SVG 符合可编辑子集
- 如果验证失败，修复问题后重新验证

### Step 3: Finalize（定稿）

- 确认 `svg_final/` 中所有文件通过验证
- 确认 `notes/total.md` 已生成
- 输出最终文件清单

## 输出物

```
svg_output/          # 原始生成 SVG（净化前）
  ├── 01-*.svg
  ├── 02-*.svg
  └── ...

svg_final/           # 最终 SVG（净化+验证后）
  ├── 01-*.svg
  ├── 02-*.svg
  └── ...

notes/               # 演讲备注
  └── total.md
```

## 执行检查清单

生成完成后，逐项确认：

- [ ] 所有 prompt 页面均已生成对应 SVG
- [ ] 每个 SVG 的 viewBox 符合 design-spec
- [ ] 所有 SVG 仅使用允许的图元（无 banned features）
- [ ] 颜色仅使用 HEX + fill-opacity/stroke-opacity
- [ ] 文字仅使用 text/tspan（无 foreignObject、无 path text）
- [ ] 风格一致性检查通过（颜色、字号、间距）
- [ ] sanitize 脚本执行成功
- [ ] validate 脚本执行成功（exit 0）
- [ ] notes/total.md 已生成且格式正确
- [ ] 最终文件清单已输出

## 错误处理

| 情况 | 处理方式 |
|------|----------|
| design-spec.md 缺失 | 终止执行，提示用户先完成设计规范 |
| prompt 文件缺失 | 跳过该页，记录警告，继续其余页面 |
| SVG 包含 banned features | 自动修复后重新验证 |
| validate 失败 | 输出错误详情，修复后重新运行 |
| sanitize 失败 | 输出错误详情，检查 SVG 源文件 |

## 与其他 Skill 的关系

```
ideal-ppt-generator (P10 审阅通过)
        ↓
  ideal-ppt-executor (本 Skill, P11)
        ↓
ideal-ppt-workflow (P12 测试审阅)
```

- **上游**：ideal-ppt-generator 完成 prompts 和 design-spec
- **下游**：ideal-ppt-workflow 进行测试审阅（P12）
