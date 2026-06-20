---
name: ideal-backlog
description: 需求池构建与管理。入队（调 ideal-requirement 澄清落盘→登记 goal）、状态流转、优先级+FIFO 排序。维护 docs/dev/需求池.md 作为 ideal-agent-loop outer loop 出队契约源。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# ideal-backlog（需求池构建与管理）

> **职责边界**：本 skill 只负责需求池的**构建与管理**（入队 / 状态 / 排序 / 格式）。不澄清需求（归 `ideal-requirement`）、不执行 goal（归 `ideal-agent-loop`）。它是 `ideal-requirement`（产出需求）↔ `ideal-agent-loop`（消费需求）之间的队列层。

## 角色定位

**需求池管家** — 维护 `docs/dev/需求池.md`，把 `ideal-requirement` 澄清落盘的需求登记为 goal 条目，按优先级 + FIFO 排序，供 `ideal-agent-loop` 的 outer loop 出队消费。

## 数据流

```
用户"加需求"
  → ideal-requirement 澄清 + 落盘 需求.md
  → ideal-backlog 登记 goal 条目入 需求池.md（ID/优先级/状态/验收标准）
  → （待执行）
  → ideal-agent-loop outer loop 读 需求池.md → 出队 → 跑 → 标 done
```

## 需求池.md 格式（契约）

路径：`docs/dev/需求池.md`（项目级，git 跟踪）。

```markdown
# 需求池

> 由 ideal-backlog 维护；ideal-agent-loop 只读消费（outer loop 出队）。
> 排序：优先级降序（P0 > P1 > P2）+ 同优先级 FIFO（最早创建优先）。

## 待办 / 进行中

### [REQ-001] 标题
- 优先级：P0
- 创建时间：2026-06-20
- 状态：todo  <!-- todo | doing | done | blocked -->
- 需求文档：docs/迭代/2026-06-20-{slug}/需求.md
- 验收标准：
  - [ ] 标准 1
  - [ ] 标准 2
- 备注：
```

### 字段约定

| 字段 | 说明 |
|------|------|
| ID | `REQ-{三位递增}`，全局唯一，不回收 |
| 优先级 | P0（紧急）/ P1（高）/ P2（常规） |
| 创建时间 | YYYY-MM-DD（入队日期，FIFO 依据） |
| 状态 | todo / doing / done / blocked |
| 需求文档 | `ideal-requirement` 落盘的 `需求.md` 路径 |
| 验收标准 | 可判定的完成条件（agent-loop 全 task passed 的目标） |

### 排序规则

需求池.md 中 goal 条目按**优先级降序**排列；同优先级内按**创建时间升序**（FIFO）。入队 / 重排时维持此序。

## 操作

### 入队（enqueue）

```
1. 用户描述需求（一句话或多句）
2. 调 ideal-requirement：澄清（背景/目标/范围/验收标准）→ 落盘 需求.md 到 docs/迭代/{date}-{slug}/
3. 扫描现有最大 REQ 编号，分配 ID（+1）
4. 询问 / 确认优先级（P0/P1/P2）
5. 在 需求池.md 按排序规则插入 goal 条目（状态 todo）
6. 确认登记成功，输出 REQ-ID
```

### 状态流转

| 转换 | 触发 | 执行者 |
|------|------|--------|
| → todo | 入队 | ideal-backlog |
| todo → doing | 出队（agent-loop 取走） | ideal-agent-loop |
| doing → done | goal 全 task passed | ideal-agent-loop |
| doing → blocked | 连续 3 次 verification 失败 | ideal-agent-loop |
| * → 调整 | 用户改优先级 / 取消 | ideal-backlog（用户指令） |

> ideal-backlog 默认只管 todo（入队）+ 用户指令的调整。doing/done/blocked 由 ideal-agent-loop 在执行时更新。状态流转的**事实源是 需求池.md**（agent-loop 直接改文件，backlog 不维护运行时状态）。

### 查询 / 重排

- **列出待办**：按优先级 + FIFO 显示所有 todo goal
- **改优先级**：调整 goal 的优先级字段 + 重排条目顺序
- **取消 / 归档**：状态改 done（备注"已取消"）或移到归档区

## 与其他 skill 的关系

| skill | 关系 |
|-------|------|
| `ideal-requirement` | 上游：backlog 入队时调它澄清 + 落盘 `需求.md` |
| `ideal-agent-loop` | 下游：它只读消费 `需求池.md`（outer loop 出队），并直接更新 goal 状态（doing/done/blocked） |
| `ideal-dev-workflow` | 不直接交互（agent-loop 在 task 粒度调它） |

## 质量检查清单

入队时：
- [ ] 调 `ideal-requirement` 完成澄清并落盘 `需求.md`
- [ ] 分配唯一 REQ-ID（扫描现有最大 +1）
- [ ] 优先级已确认（P0/P1/P2）
- [ ] 验收标准可判定（非"做好"这类模糊表述）
- [ ] `需求池.md` 按优先级 + FIFO 排序
- [ ] 需求文档路径正确指向落盘的 `需求.md`

## 错误处理

| 场景 | 处理 |
|------|------|
| `需求池.md` 不存在 | 创建带头部说明的空池（保留排序规则注释） |
| ID 冲突 | 扫描现有最大编号 +1，不回收已用 ID |
| 需求文档落盘失败 | 不入队，报告 `ideal-requirement` 失败原因 |
| 优先级未指定 | 默认 P2，提示用户确认 |
| 验收标准模糊 | 追问至可判定，或标记 `[待澄清]` 并提示 |
