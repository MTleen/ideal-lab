---
name: ideal-agent-loop
description: "运行 profile-driven bounded Loop Kernel：从 ideal-backlog 绑定 Goal，派生 Stage Task Plan，经 Capability Registry 路由独立 Execution/Validation Run，并按预算 checkpoint、阻塞、等待、验收或 reopen。"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# ideal-agent-loop

`ideal-agent-loop` is the domain-neutral control loop that consumes the v2
Goal Store. **ideal-backlog is the only machine Goal source of truth.** This
Skill may interpret Profiles and create Run artifacts, but it never edits a raw
backlog revision or maintains a second Goal status.

## Kernel boundary

The public Kernel owns only these primitives:

- Goal Loop;
- Stage / Task Loop;
- Loop Profile;
- Capability Registry;
- Task Plan and Checkpoint;
- Execution Run and Validation Run;
- Gate, reopen, evidence reuse, and bounded stop decisions.

Domain phases, Worker locators, workspace isolation, integration behavior, and
acceptance authorities come from a Profile or adapter. A Skill is a Worker; it
does not own transition authority.

## Two-level loop

### Goal Loop

Each outer iteration:

1. inspect the current Goal Store revision through the `ideal-backlog` CLI;
2. apply the declared source binding;
3. claim the selected Goal and retain its lease token;
4. call one bounded Stage / Task Loop iteration;
5. request one atomic backlog transition or release the lease.

Source binding:

- `fixed` stays on the named Goal even if queue ordering changes;
- `dynamic` selects dependency-satisfied work by priority, deadline, FIFO, then
  stable ID.

The Goal Loop re-reads before every mutation. A stale revision returns `reload`;
it never overwrites the newer Goal.

### Stage / Task Loop

Each inner iteration:

1. load the current phase from the Goal revision;
2. derive or resume its immutable Task Plan;
3. select exactly one dependency-satisfied task;
4. resolve one verified Capability;
5. create either one Execution Run or one Validation Run;
6. checkpoint produced artifact or evidence references;
7. evaluate the phase gate when all required tasks are complete.

The Task Plan is a revision-bound derived artifact. It carries no independent
Goal execution or quality status.

## Loop Profile

A Profile JSON declares:

- phases, required artifacts, tasks, and gates;
- Capability input/output/permission requirements;
- retry and review budget;
- evidence reuse and invalidation policy;
- permissions and acceptance authorities;
- optional adapters.

Use `profiles/development.json` for the included compatibility behavior. A
second Profile without development adapters must still use exactly the same
Kernel protocol. See
[references/profile-contract.md](references/profile-contract.md).

## Capability Registry

Resolve a Worker only when all conditions hold:

1. inputs exactly match the task requirement;
2. outputs exactly match the task requirement;
3. permissions are a subset of the Profile allowance;
4. locator and version are explicit;
5. the Capability record is verified.

Sort equal candidates by Profile preference, then stable identity. If none
match, return `blocked: capability_unavailable`; do not guess a nearby Skill.

## Run authority

Every Run binds:

- Goal revision, phase, and task ID;
- assignment hash;
- Capability ID, locator, and version;
- input/candidate/criteria hashes;
- Goal lease digest, declared Task outputs, and validator/Profile policy
  fingerprint;
- start/finish time, outcome, artifacts, evidence, and root cause.

### Execution Run

An Execution Run may produce only the candidate artifacts declared by its
Task. It cannot write validation evidence, a validation conclusion, or an
accepted quality state.

### Validation Run

A Validation Run reads the candidate and produces evidence plus a `pass` or
`fail` conclusion. It must not return modified candidate artifacts. The
acceptance authority remains separate from both Run roles.

Finished Runs are immutable. Additional information creates another record
that references the prior Run.

## Standard workflow

### 1. Inspect and bind

```bash
python3 plugins/ideal-backlog/scripts/ideal_backlog.py \
  --root "$PROJECT_ROOT" inspect --goal-id "$GOAL_ID"
```

Use `--goal-id` for `fixed`; inspect the full store for `dynamic`.

### 2. Claim

Claim through `ideal-backlog` with `--apply`, the expected revision, and a
unique operation ID. Preserve the returned Goal revision and lease token.

### 3. Plan one phase

Load the selected Profile, derive a revision-bound Task Plan, incorporate only
provenance-checked artifact references, and select one ready task. When all
required outputs are satisfied, emit an explicit `gate_passed` transition
intent; do not disguise Gate completion as `no_op`. A non-final Gate emits
one phase-advance intent. The final Gate emits the legal Goal Store transition
sequence `implemented -> verified -> awaiting_acceptance`; apply each patch
against the newly returned revision rather than collapsing the sequence.

### 4. Route one task

Query the Capability Registry using exact I/O and exact task permissions
within the Profile permission ceiling. Missing or unverified capability is a
structured block with an actionable release condition.

### 5. Execute or validate one Run

Do not combine execution and validation in one Run. Start the Run before
dispatch and finish it with a legal terminal outcome:

```text
completed | blocked | waiting | human_gate | no_op | failed | cancelled
```

### 6. Checkpoint

Create an immutable checkpoint referencing the Run and new artifact/evidence
refs. Do not copy Goal status into the checkpoint.

### 7. Transition, block, or release

Request the transition through the backlog CLI with expected revision, lease
token, operation ID, reason, and evidence refs. Never edit the Markdown mirror
or a revision JSON directly.

## Bounded continuation

Continue only when all of these are true:

- ready work exists;
- the Goal is not `blocked`, `waiting`, `human_gate`, `no_op`, cancelled, or
  awaiting acceptance;
- retry budget remains;
- review budget remains;
- permission budget allows the assignment.

`waiting`, `human_gate`, `no_op`, and `blocked` are legitimate outcomes and
release the execution slot. Awaiting acceptance produces a handoff and also
releases the slot.

Three consecutive failures with the same root cause transition the Goal to
`blocked`. A different phrasing of the same failure is not a strategy reset.

## Evidence and review policy

- terminal review budget defaults to one per substantive candidate;
- if candidate, criteria, business input, resolved validator
  ID/locator/version, and Profile/Gate policy fingerprints are unchanged, use
  evidence reuse;
- reviewer, ledger, formatting, or commit-metadata changes do not invalidate
  business artifacts;
- changed business inputs invalidate only downstream nodes in the artifact
  dependency graph;
- default validation-infrastructure budget is zero;
- a finding may create one substantive repair assignment and focused
  regression, never a review-of-review task.

A passing command is evidence about that command, not automatic proof that the
Goal is complete. Phase gates must inspect required artifacts and relevant
outcomes.

## Acceptance and reopen

Only an authority allowed by the Goal/Profile may submit `accepted`, and it
must attach explicit acceptance evidence. A runner cannot accept its own work.

Counterevidence reopens the original Goal and records:

- reason;
- missing test reason;
- required regression.

Historical evidence remains queryable. Reopen invalidates only affected
artifacts.

## Compatibility adapters

The development Profile may enable:

- optional workspace isolation;
- a phase-scoped integration gate;
- legacy criterion import as validation-owned required evidence.

These adapters are absent from Kernel defaults. See
[references/worktree-goal-guide.md](references/worktree-goal-guide.md) and
[references/merge-gate.md](references/merge-gate.md).

The legacy `agent_loop_state.py`, `agent_loop_verify.py`, and cooperative Stop
Hook remain compatibility surfaces. Their `.agent-loop/` files are artifacts,
not Goal truth.

## Kernel CLI

One bounded assignment step:

```bash
python3 plugins/ideal-agent-loop/scripts/loop_kernel.py step \
  --backlog-cli plugins/ideal-backlog/scripts/ideal_backlog.py \
  --project-root "$PROJECT_ROOT" \
  --profile plugins/ideal-agent-loop/profiles/development.json \
  --capabilities "$CAPABILITY_REGISTRY" \
  --source-binding fixed \
  --goal-id "$GOAL_ID" \
  --apply
```

The command reads backlog state only through its CLI contract and emits at most
one assignment.

## Completion evidence

Report separately:

- implemented: candidate artifacts and concrete changes;
- verified: Execution/Validation Run IDs, hashes, checkpoints, tests, gates;
- accepted: authority and evidence reference;
- released/published: version, remote revision, and loaded version when
  applicable.

Do not collapse ordinary tests, final acceptance, release, or runtime loading
into one success claim.

## References

- [contract-template.md](references/contract-template.md)
- [verification-guide.md](references/verification-guide.md)
- [continuation-template.md](references/continuation-template.md)
- [profile-contract.md](references/profile-contract.md)
- [global-audit-guide.md](references/global-audit-guide.md)
- [worktree-goal-guide.md](references/worktree-goal-guide.md)
- [merge-gate.md](references/merge-gate.md)
- [loop-config.md](references/loop-config.md)
