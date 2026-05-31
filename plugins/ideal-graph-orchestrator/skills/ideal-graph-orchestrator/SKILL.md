---
name: ideal-graph-orchestrator
description: "通用 Skill Graph 编排器。双模式：(1) Generate — 自然语言描述需求，自动匹配 skills-graph.json 中的已有 skill、检测缺口、编译 workflow.yml；(2) Execute — 读取 workflow.yml，沿图路径顺序执行，处理已有 skill 复用和新建 skill scaffold。Use when user wants to compose skills into a new workflow."
io:
  inputs:
    - name: user_intent
      source: user
  outputs:
    - name: workflow_yml
      path: "workflows/{name}/workflow.yml"
      type: yaml
    - name: execution_result
      type: artifacts
---

# ideal-graph-orchestrator（通用 Skill Graph 编排器）

## 核心能力

将用户的自然语言 workflow 需求编译为可执行的 skill 路径，自动处理已有 skill 复用和新建 skill scaffold。

```
用户: "做一个代码转技术文档的流程"
  ↓
Generate 模式: NL → 意图解析 → skills-graph.json 匹配 → Gap 检测 → workflow.yml
  ↓
用户审批 workflow.yml
  ↓
Execute 模式: 读 workflow.yml → 沿路径执行 → 产物
```

---

## Mode 1: Generate（生成 workflow.yml）

### 触发

用户描述一个需要多步骤完成的任务，涉及跨 plugin 的 skill 组合。

### 流程

```
1. 解析意图
   → 将用户的自然语言需求分解为步骤序列
   → 每个步骤标注: 动作 + 期望产出

2. 匹配 skill（查 skills-graph.json）
   → 对每个步骤，在 skills-graph.json 的 nodes[].description 中做语义匹配
   → 读 matched skill 的 io manifest
   → 记录 match_confidence

3. 检测 Gap
   → 前置 skill 的 io.outputs 是否覆盖后置 skill 的 io.inputs？
   → 不覆盖 → Gap
   → Gap 分类:
       - 简单变换（格式转换、字段重命名）→ 内联 adapter
       - 有实质逻辑 → 规划 skill: new

4. 插入评审节点
   → 每个产物步骤后自动插入 panel-review（yolo_mode: true）

5. 编译 workflow.yml
   → 写入 workflows/{name}/workflow.yml
   → 包含: name, generated_at, generated_from, path[]

6. 呈现审批
   → 摘要: N 步骤，M 个已有 skill，K 个新建
   → 展示路径图（文本格式）
   → 用户可增删换步骤、调整参数
   → 确认后进入 Execute 模式
```

### 匹配策略（内部规则）

```
语义匹配:
  - 对步骤描述做关键词提取
  - 在 skills-graph.json 的 description 字段做模糊匹配
  - 取 top-3，选 match_confidence 最高的

I/O 匹配:
  - 读 matched skill 的 io.inputs → 查前置 skill 的 io.outputs
  - name 匹配 → source 字段对应 → 覆盖
  - 不匹配 → Gap

图结构偏好:
  - 优先选择有 prerequisite 边的 skill 对（已在同一 workflow 中验证过）
  - enhancement 边的 skill（如 panel-review）自动追加到产物步骤后
  - alternative 边的 skill（如 deep-research ×2）提示用户选择
```

### 呈现格式

```
我将用 12 个步骤完成「代码转技术文档」：

已有 skill（9 个）:
  1. ideal-requirement     → 需求收集     (match: 94%)
  2. panel-review          → 需求评审     (自动)
  3. ideal-dev-solution    → 技术方案     (match: 91%)
  4. panel-review          → 方案评审     (自动)
  5. outline-generation    → 文档大纲     (match: 88%)
  6. panel-review          → 大纲评审     (自动)
  7. document-writing      → 文档写作     (match: 85%)
  8. panel-review          → 文档评审     (自动)
  9. document-render       → 导出 Word    (match: 95%)

新建 skill（2 个）:
  10. 方案转文档需求       → 技术方案 → 文档需求分析格式
  11. 架构图生成          → 技术方案 → Mermaid 架构图

确认后开始执行。你可以:
  - 删除/替换某个步骤
  - 调整新建 skill 的描述
  - 直接说"开始"执行
```

---

## Mode 2: Execute（执行 workflow.yml）

### 触发

- Generate 模式用户确认后自动进入
- 用户直接指定 workflow: `--from-workflow code-to-doc`

### 流程

```
1. 读 workflow.yml → 解析 path

2. 初始化 workflow_state:
   state = {
     workflow: { name, current_step: 0, mode: "yolo" },
     artifacts: {},
     reviews: []
   }

3. 遍历 path 中的每个步骤:
   ┌── skill: <existing-graph-id>
   │   step:
   │     a. 读 skills-graph.json → 获取该 skill 的 io manifest
   │     b. 解析 io.inputs → 从 state.artifacts 查找所需 artifact
   │        → 找到 → 传递 artifact 路径给 skill
   │        → 未找到 → 报错：缺少前置产出
   │     c. 调用 Skill(skill_name)
   │        → 传递: artifact paths, yolo_mode, phase context
   │     d. 等待 skill 返回
   │     e. 读 io.outputs → 写回 state.artifacts[name] = path
   │     f. state.current_step += 1
   │
   ├── skill: new
   │   step:
   │     a. 调用 skill-builder（create 模式）
   │        → 输入: name, description, io 声明, workflow context
   │        → 输出: 临时 SKILL.md → 写入 workflows/{name}/skills/{skill-name}/
   │     b. 临时注册到 graph（本次运行）
   │     c. 同上流程执行
   │     d. 保留生成的 SKILL.md 供后续 promote
   │
   └── adapter: <transformation>
       step:
         → 内联数据转换（文件格式、字段映射）
         → 不生成独立 skill
         → 输出写入 state.artifacts

4. panel-review 节点的特殊处理:
   → 调用 panel-review(yolo_mode: true, review_target, product_type)
   → 解析 JSON 判定块
   → verdict=="pass" → 继续下一节点
   → verdict=="fail" 且重试 < 3 → 修复产物 → 重新调用 panel-review
   → 连续 3 次 fail → 熔断，停止整个 workflow

5. 完成:
   → 输出 workflow_state
   → 列出所有产物文件
   → 列出所有新建 skill（供 promote 决策）
```

### artifact 传递协议

```
skill A 的 io.outputs:
  - name: solution_doc
    path: "P3-技术方案.md"
    type: markdown

skill B 的 io.inputs:
  - name: solution_doc
    source: ideal-dev-solution.solution_doc

编排器解析:
  B 需要 solution_doc → source 指向 A.solution_doc
  → 从 state.artifacts["solution_doc"] 取路径
  → 传递给 B 作为输入文件路径
```

---

## 新建 skill 生命周期

```
Scaffold（workflow 运行时自动）
  → skill-builder 根据 name/description/io 声明
  → 生成最小 SKILL.md → workflows/{name}/skills/{skill-name}/

Trial（本次 workflow 运行）
  → 编排器临时注册并执行
  → skill 的产出写入 state.artifacts

Promote（手动确认）
  → 用户确认 skill 合格
  → /ideal-lab-maintainer add-skill
  → 从 workflows/ 迁移到 plugins/
  → 重新 build-graph → skills-graph.json 更新
```

---

## 与现有 workflow 的关系

- **向后兼容**：现有的 ideal-flow-control、ideal-ppt-workflow、ideal-document-workflow 保持不变
- **渐进迁移**：新 workflow 用 graph-orchestrator；已有 workflow 继续用原有 orchestrator
- **共享评审**：graph-orchestrator 和三个 workflow orchestrator 都调用同一个 panel-review

---

## 使用方式

```
# 从自然语言生成并执行
/ideal-graph-orchestrator "做一个代码审查+文档生成的流程"

# 从已有的 workflow.yml 执行
/ideal-graph-orchestrator --from-workflow code-to-doc

# 仅生成 workflow.yml（不执行）
/ideal-graph-orchestrator --generate-only "竞品分析报告流程"
```