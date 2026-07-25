---
name: ideal-backlog
description: "管理 ideal-backlog v2 Goal Store：创建和查询 Goal、按 fixed/dynamic 绑定选择、通过 revision/lease 并发控制执行原子流转、迁移 v1 Markdown 并生成只读镜像。"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# ideal-backlog

`ideal-backlog` owns the single machine source of truth for Goal state. The
machine store lives under `.ideal/backlog/`; a Markdown backlog is only a
generated view. `ideal-agent-loop` consumes this contract but never writes raw
Goal files.

## Responsibility

This Skill may:

- initialize and inspect the immutable Goal Store;
- create revisions through guarded CLI operations;
- bind one Goal with `fixed` selection or select ready work with `dynamic`
  ordering;
- claim and release a Goal lease;
- record legal execution, quality, blocking, acceptance, and reopen
  transitions;
- migrate a v1 Markdown backlog and render its generated mirror.

It does not execute Goal work, choose a domain Worker, validate an artifact, or
grant acceptance authority.

## Storage contract

```text
.ideal/backlog/
├── CURRENT
├── LOCK
├── revisions/<sha256>/backlog.json
└── migrations/<source-sha256>/source.md
```

- `CURRENT` names an immutable, content-addressed revision.
- Each Goal mutation creates a new revision; old revisions are never edited.
- A global writer lock prevents concurrent commits and has no automatic TTL.
- An operation ID makes retries idempotent.
- Each Goal claim creates a lease token bound to the current revision.
- `docs/dev/需求池.md` is a generated Markdown mirror and is never a write
  surface.

See [references/goal-store-v2.md](references/goal-store-v2.md) for the record
shape and transition rules.

## Required write preconditions

Every write command must:

1. pass `--apply`;
2. provide a unique operation ID;
3. provide the expected revision when modifying an existing store;
4. provide the current lease token for a leased Goal;
5. state a transition reason and attach evidence when the operation requires
   it.

On stale revision, lock conflict, or lease conflict, stop the write, inspect
again, and decide from the new record. Never overwrite the newer revision.

## Workflow

### 1. Inspect

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" inspect
```

Read the current revision on every scheduling round. Do not retain a long-lived
Goal snapshot.

### 2. Bind the Goal

- `fixed`: operate only on the specified Goal ID. Queue reordering never
  switches the bound Goal.
- `dynamic`: select an unfinished dependency-satisfied Goal by priority,
  deadline, FIFO creation time, then stable ID.

The binding choice is part of the Goal contract; a runner must not silently
change it.

### 3. Claim

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" claim \
  --goal-id REQ-001 \
  --expected-revision "$REVISION" \
  --operation-id "$OPERATION_ID" \
  --apply
```

Record the returned revision and lease token. Only the holder may transition or
release that Goal.

### 4. Transition atomically

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" transition \
  --goal-id REQ-001 \
  --expected-revision "$REVISION" \
  --lease-token "$LEASE_TOKEN" \
  --operation-id "$OPERATION_ID" \
  --reason "focused validation completed" \
  --patch '{"execution":{"status":"verifying"},"quality":{"status":"verified"}}' \
  --evidence evidence://run/validation-001 \
  --apply
```

Execution and quality states are separate. `accepted` requires an authority
listed in the Goal and an explicit acceptance evidence reference. An ordinary
runner cannot accept its own output.

### 5. Release execution capacity

`blocked`, `waiting`, `human_gate`, `cancelled`, and completed terminal states
release the Goal lease. Record the reason and an actionable release condition
for non-terminal states. No ready work is a legitimate no-op; it is not a
reason to retain a slot.

Use explicit release when abandoning an otherwise runnable claim:

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" release \
  --goal-id REQ-001 \
  --expected-revision "$REVISION" \
  --lease-token "$LEASE_TOKEN" \
  --operation-id "$OPERATION_ID" \
  --apply
```

### 6. Reopen

A reopen transition must preserve historical evidence and include:

- `reason`;
- `missing_test_reason`;
- `required_regression`.

Reopen the original Goal. Do not create a review-of-review or a separate Goal
whose only purpose is to validate the validator.

## v1 migration

Preview first:

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" migrate-v1 \
  --source docs/dev/需求池.md \
  --dry-run
```

The dry-run must not create `.ideal/backlog`. Resolve every reported unknown
controlled field before applying.

Apply with an auditable source snapshot:

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" migrate-v1 \
  --source docs/dev/需求池.md \
  --operation-id "$OPERATION_ID" \
  --apply
```

Historical `done` entries without v2 quality evidence are marked
`legacy_accepted`; they are not represented as newly accepted v2 Goals.

## Mirror and integrity verification

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" verify

python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" verify-mirror \
  --path docs/dev/需求池.md
```

If the mirror diverges, regenerate it through `render --apply`. Never reconcile
the machine store by copying edited Markdown back into a revision.

## Failure outcomes

| Failure | Required outcome |
|---|---|
| stale expected revision | reload; do not overwrite |
| global lock held | no-op; do not steal by age |
| wrong lease token | reject the mutation |
| unknown v1 controlled field | block migration with a report |
| `blocked` | release lease and record release condition |
| `waiting` | release lease and record awaited event |
| `human_gate` | produce a handoff and release lease |
| unauthorized `accepted` | reject the transition |
| incomplete reopen metadata | reject the transition |

## Completion evidence

Report the final current revision, Goal execution/quality state, operation IDs,
lease disposition, evidence references, and mirror verification result.
Passing a command alone is not evidence that the intended Goal revision was
created.
