# Loop Kernel + Profile Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade `ideal-backlog` and `ideal-agent-loop` to a domain-neutral 2.0 protocol with one machine Goal truth, profile-driven two-level loops, bounded validation, and v1 migration.

**Architecture:** `ideal-backlog` owns immutable backlog revisions, leases, transitions, and generated Markdown mirrors. `ideal-agent-loop` consumes the backlog only through its CLI contract, loads domain Profiles, derives stage-local Task Plans, routes verified capabilities, and records immutable execution/validation runs. Domain rules live in Profiles and adapters; development remains an included compatibility Profile, while private academic rules remain outside this repository.

**Tech Stack:** Python 3 standard library, JSON/JSON Schema documents, Markdown Skill contracts, `unittest`, Claude plugin manifests, Changesets.

---

## 0. Execution rules

- Work only in a clean worktree based on current `main`.
- Read root `AGENTS.md` before each delivery slice.
- Do not edit installed plugin caches.
- Use TDD: failing focused test, minimal implementation, passing focused test.
- Do not add a daemon, database, Web UI, YAML parser, or third-party Python dependency.
- Do not import private `academic-workflow` code or fixtures.
- Keep execution, validation, and acceptance authorities distinct.
- Commit plugin changes through `ideal-lab-maintainer`; use targeted staging and never `git add .`.
- Push/version/install only after the complete 2.0 contract passes.

Baseline commands:

```bash
git status --short --branch
python3 --version
claude plugin validate plugins/ideal-backlog
claude plugin validate plugins/ideal-agent-loop
```

Expected:

- clean task worktree;
- Python 3 available;
- both current plugin packages validate before modification.

---

### Task 1: Define `ideal-backlog` v2 contract fixtures

**Files:**

- Create: `plugins/ideal-backlog/schemas/goal-v2.schema.json`
- Create: `plugins/ideal-backlog/tests/fixtures/empty-backlog.json`
- Create: `plugins/ideal-backlog/tests/fixtures/one-goal-backlog.json`
- Create: `plugins/ideal-backlog/tests/test_contract.py`

**Step 1: Write the failing schema-shape test**

Create `test_contract.py` with tests that load the schema and fixtures and assert:

```python
REQUIRED_GOAL_KEYS = {
    "id",
    "profile",
    "project_path",
    "source_binding",
    "priority",
    "dependencies",
    "execution",
    "quality",
    "phase",
    "revision",
    "lease",
    "evidence_refs",
    "history_refs",
}
```

Also assert:

```python
self.assertEqual(schema["$id"], "ideal-backlog/goal-v2")
self.assertEqual(fixture["schema"], "ideal-backlog/backlog-v2")
self.assertEqual(fixture["goals"][0]["execution"]["status"], "todo")
self.assertEqual(fixture["goals"][0]["quality"]["status"], "unverified")
```

**Step 2: Run the test and confirm failure**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_contract.py -v
```

Expected: `FileNotFoundError` for the new schema or fixture.

**Step 3: Add the minimal schema and fixtures**

The schema must enumerate, at minimum:

```json
{
  "$id": "ideal-backlog/goal-v2",
  "type": "object",
  "required": [
    "id",
    "profile",
    "project_path",
    "source_binding",
    "priority",
    "dependencies",
    "execution",
    "quality",
    "phase",
    "revision",
    "lease",
    "evidence_refs",
    "history_refs"
  ]
}
```

Use only JSON-compatible scalar/array/object fields. Do not put derived Markdown into the machine record.

**Step 4: Run the focused test**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_contract.py -v
```

Expected: all contract fixture tests pass.

**Step 5: Commit the contract slice**

Use a targeted documentation/test commit. Do not bump the plugin yet; the feature is not usable.

```bash
git add \
  plugins/ideal-backlog/schemas/goal-v2.schema.json \
  plugins/ideal-backlog/tests/fixtures/empty-backlog.json \
  plugins/ideal-backlog/tests/fixtures/one-goal-backlog.json \
  plugins/ideal-backlog/tests/test_contract.py
git commit -m "test(backlog): define v2 goal contract"
```

If root policy requires the maintainer flow even before a release bump, use its manual targeted-staging path and preserve this commit boundary.

---

### Task 2: Implement immutable backlog revisions

**Files:**

- Create: `plugins/ideal-backlog/scripts/ideal_backlog.py`
- Create: `plugins/ideal-backlog/tests/test_store.py`

**Step 1: Write failing repository tests**

Cover:

1. `init_store(root)` creates:

   ```text
   .ideal/backlog/CURRENT
   .ideal/backlog/revisions/<sha256>/backlog.json
   ```

2. `read_current(root)` verifies that `CURRENT` matches the canonical JSON SHA-256.
3. `write_revision(root, snapshot, expected_revision, operation_id)`:
   - rejects stale `expected_revision`;
   - returns the old revision for a repeated `operation_id`;
   - never modifies an existing revision directory.

Use `tempfile.TemporaryDirectory()` for every test.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_store.py -v
```

Expected: import failure for `ideal_backlog`.

**Step 3: Implement canonical hashing and atomic CURRENT update**

Implement:

```python
def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def revision_hash(snapshot):
    return hashlib.sha256(canonical_json(snapshot)).hexdigest()
```

Write a new revision to a sibling temporary directory, `os.replace` it into `revisions/<sha>`, then update `CURRENT` through `CURRENT.tmp` + `os.replace`.

Do not delete or rewrite old revisions.

**Step 4: Run focused tests**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_store.py -v
```

Expected: all repository tests pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-backlog/scripts/ideal_backlog.py \
  plugins/ideal-backlog/tests/test_store.py
git commit -m "feat(backlog): add immutable revision store"
```

---

### Task 3: Add global lock, lease, and idempotent operations

**Files:**

- Modify: `plugins/ideal-backlog/scripts/ideal_backlog.py`
- Create: `plugins/ideal-backlog/tests/test_concurrency.py`

**Step 1: Write failing lock and lease tests**

Test:

- global lock uses exclusive creation;
- a second writer cannot enter;
- lock has no TTL and cannot be stolen automatically;
- release requires the exact lock token;
- `claim_goal` sets a non-empty lease token;
- transition with the wrong lease fails;
- release with the right lease succeeds;
- the same operation ID returns the same resulting revision.

Expected exception names:

```python
LockConflict
LeaseConflict
StaleRevision
InvalidTransition
```

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_concurrency.py -v
```

Expected: missing exception/operation APIs.

**Step 3: Implement the minimal APIs**

Add:

```python
acquire_lock(root, owner, operation_id) -> token
release_lock(root, token) -> None
claim_goal(root, goal_id, expected_revision, operation_id) -> Result
transition_goal(root, goal_id, expected_revision, lease_token, operation_id, patch) -> Result
release_goal(root, goal_id, expected_revision, lease_token, operation_id) -> Result
```

Persist applied operation IDs in the immutable snapshot metadata for the first release. Do not build a separate event database.

**Step 4: Run store and concurrency tests**

```bash
python3 -m unittest \
  plugins/ideal-backlog/tests/test_store.py \
  plugins/ideal-backlog/tests/test_concurrency.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-backlog/scripts/ideal_backlog.py \
  plugins/ideal-backlog/tests/test_concurrency.py
git commit -m "feat(backlog): add lock and lease operations"
```

---

### Task 4: Implement legal state transitions and acceptance authority

**Files:**

- Modify: `plugins/ideal-backlog/scripts/ideal_backlog.py`
- Create: `plugins/ideal-backlog/tests/test_transitions.py`

**Step 1: Write the transition-table tests**

Test the execution states:

```text
todo, claimed, planning, executing, verifying,
awaiting_acceptance, done, blocked, waiting,
human_gate, cancelled
```

Test quality states:

```text
unverified, implemented, verified,
awaiting_acceptance, accepted, reopened
```

Required negative tests:

- ordinary runner cannot write `accepted`;
- `verified` cannot skip to `accepted`;
- reopening requires `reason`, `missing_test_reason`, and `required_regression`;
- `cancelled` is not represented as `done`;
- blocked/waiting/human gate release the Goal lease.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_transitions.py -v
```

Expected: transition policy failures.

**Step 3: Implement a data-driven transition table**

Keep policy in constants rather than nested conditionals. Acceptance must require:

```python
authority in goal["acceptance"]["allowed_authorities"]
```

and an operation payload with an explicit evidence reference.

**Step 4: Run all backlog state tests**

```bash
python3 -m unittest discover -s plugins/ideal-backlog/tests -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-backlog/scripts/ideal_backlog.py \
  plugins/ideal-backlog/tests/test_transitions.py
git commit -m "feat(backlog): enforce quality transitions"
```

---

### Task 5: Add v1 migration and generated Markdown mirror

**Files:**

- Modify: `plugins/ideal-backlog/scripts/ideal_backlog.py`
- Create: `plugins/ideal-backlog/tests/fixtures/v1-backlog.md`
- Create: `plugins/ideal-backlog/tests/fixtures/v1-backlog-edge-cases.md`
- Create: `plugins/ideal-backlog/tests/test_migration.py`
- Create: `plugins/ideal-backlog/tests/test_render.py`

**Step 1: Write migration failures first**

Test:

- `migrate-v1 --dry-run` does not create `.ideal/backlog`;
- `--apply` records source path and SHA-256;
- priority, FIFO date, dependencies, execution state, quality evidence, and reopen history survive;
- historical `done` becomes visibly marked `legacy_accepted`;
- unknown controlled fields stop apply with a report;
- rendering the current revision is deterministic;
- manually edited controlled Markdown fails `verify-mirror`.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest \
  plugins/ideal-backlog/tests/test_migration.py \
  plugins/ideal-backlog/tests/test_render.py -v
```

Expected: missing migration/render APIs.

**Step 3: Implement migration, render, and mirror verification**

Add CLI commands:

```text
init
inspect
migrate-v1 --source <path> [--dry-run|--apply]
render --output <path>
verify
verify-mirror --path <path>
claim
transition
release
```

All write commands must require `--apply`, expected revision where applicable, and operation ID.

**Step 4: Run all backlog tests**

```bash
python3 -m unittest discover -s plugins/ideal-backlog/tests -v
```

Expected: pass with no network access.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-backlog/scripts/ideal_backlog.py \
  plugins/ideal-backlog/tests
git commit -m "feat(backlog): migrate v1 and render mirrors"
```

---

### Task 6: Update the `ideal-backlog` Skill contract

**Files:**

- Modify: `plugins/ideal-backlog/skills/ideal-backlog/SKILL.md`
- Create: `plugins/ideal-backlog/skills/ideal-backlog/references/goal-store-v2.md`
- Modify: `plugins/ideal-backlog/.claude-plugin/plugin.json`

**Step 1: Write a contract-content test**

Extend `test_contract.py` to assert that `SKILL.md` contains:

```text
single machine source of truth
expected revision
lease token
operation ID
--apply
fixed
dynamic
blocked
waiting
human_gate
reopen
```

Also assert it no longer says the Markdown file is the source of truth.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-backlog/tests/test_contract.py -v
```

Expected: missing v2 contract phrases.

**Step 3: Rewrite the Skill around the CLI contract**

Document:

- Goal ownership;
- fixed/dynamic selection;
- atomic write preconditions;
- generated mirror;
- human acceptance authority;
- blocking and recovery;
- v1 migration.

Update plugin description, but do not manually update its version.

**Step 4: Validate**

```bash
python3 -m unittest discover -s plugins/ideal-backlog/tests -v
claude plugin validate plugins/ideal-backlog
```

Expected: pass.

**Step 5: Create the major changeset and version commit**

Use the maintainer flow with a `major` bump and message:

```text
Add an immutable v2 goal store and migration contract
```

Before commit, verify only `ideal-backlog` files, its changeset/version files, and the intended docs are staged.

Expected final version: `ideal-backlog@2.0.0`.

---

### Task 7: Define Profile, Capability, Task Plan, and Run schemas

**Files:**

- Create: `plugins/ideal-agent-loop/schemas/profile-v1.schema.json`
- Create: `plugins/ideal-agent-loop/schemas/capability-v1.schema.json`
- Create: `plugins/ideal-agent-loop/schemas/task-plan-v1.schema.json`
- Create: `plugins/ideal-agent-loop/schemas/run-v1.schema.json`
- Create: `plugins/ideal-agent-loop/profiles/development.json`
- Create: `plugins/ideal-agent-loop/tests/fixtures/document-profile.json`
- Create: `plugins/ideal-agent-loop/tests/test_contracts.py`

**Step 1: Write failing contract tests**

Assert:

- Profile declares phases, required artifacts, gates, capabilities, retry/review/permissions policies.
- Capability declares exact inputs, outputs, permissions, locator, version, and verified state.
- Task Plan binds to a Goal revision and current phase.
- Run distinguishes `execution` and `validation`.
- development and document fixtures both satisfy the same Profile shape.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-agent-loop/tests/test_contracts.py -v
```

Expected: missing schemas and profiles.

**Step 3: Add minimal JSON contracts**

Do not add YAML support. Keep Profile files deterministic and dependency-free.

The development Profile must express worktree and merge behavior as adapters:

```json
{
  "adapters": {
    "workspace": "git-worktree-optional",
    "integration_gate": "merge-gate"
  }
}
```

Kernel schemas must not contain paper, patent, venue, experiment, worktree, or merge-specific required fields.

**Step 4: Run focused tests**

```bash
python3 -m unittest plugins/ideal-agent-loop/tests/test_contracts.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/schemas \
  plugins/ideal-agent-loop/profiles \
  plugins/ideal-agent-loop/tests
git commit -m "test(loop): define kernel contracts"
```

---

### Task 8: Implement Profile loading and capability resolution

**Files:**

- Create: `plugins/ideal-agent-loop/scripts/loop_kernel.py`
- Create: `plugins/ideal-agent-loop/tests/test_profile_loader.py`
- Create: `plugins/ideal-agent-loop/tests/test_capability_resolver.py`

**Step 1: Write resolver tests**

Cover:

- exact input/output contract match;
- denied permission exclusion;
- unverified candidate exclusion;
- explicit version/locator retention;
- deterministic preference ordering;
- no candidate returns `capability_unavailable`, not a guessed Skill.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_profile_loader.py \
  plugins/ideal-agent-loop/tests/test_capability_resolver.py -v
```

Expected: missing `loop_kernel`.

**Step 3: Implement minimal loaders and resolver**

Public APIs:

```python
load_profile(path) -> dict
load_capabilities(path) -> list[dict]
resolve_capability(requirement, candidates, allowed_permissions) -> dict
```

Return structured failures:

```python
{
    "outcome": "blocked",
    "reason": "capability_unavailable",
    "required": requirement,
}
```

**Step 4: Run focused tests**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_profile_loader.py \
  plugins/ideal-agent-loop/tests/test_capability_resolver.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/scripts/loop_kernel.py \
  plugins/ideal-agent-loop/tests/test_profile_loader.py \
  plugins/ideal-agent-loop/tests/test_capability_resolver.py
git commit -m "feat(loop): load profiles and resolve capabilities"
```

---

### Task 9: Implement Stage Task Plan and checkpoints

**Files:**

- Modify: `plugins/ideal-agent-loop/scripts/loop_kernel.py`
- Create: `plugins/ideal-agent-loop/tests/test_task_plan.py`
- Create: `plugins/ideal-agent-loop/tests/test_invalidation.py`

**Step 1: Write task selection tests**

Test:

- a plan binds to `goal_revision` and `phase`;
- only dependency-satisfied tasks are ready;
- exactly one task is selected per inner-loop iteration;
- checkpoint is an immutable artifact reference;
- changed business input invalidates downstream artifacts;
- reviewer/ledger/format-only changes do not invalidate business artifacts.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_task_plan.py \
  plugins/ideal-agent-loop/tests/test_invalidation.py -v
```

Expected: missing task/invalidation APIs.

**Step 3: Implement plan APIs**

```python
derive_task_plan(goal, profile, artifacts) -> dict
select_ready_task(plan) -> dict | None
checkpoint(plan, run_ref, artifact_refs) -> dict
invalidate(plan, changed_refs, artifact_graph) -> dict
```

Do not persist a second Goal status in the plan.

**Step 4: Run focused tests**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_task_plan.py \
  plugins/ideal-agent-loop/tests/test_invalidation.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/scripts/loop_kernel.py \
  plugins/ideal-agent-loop/tests/test_task_plan.py \
  plugins/ideal-agent-loop/tests/test_invalidation.py
git commit -m "feat(loop): derive stage task plans"
```

---

### Task 10: Implement immutable Run Envelopes and bounded validation

**Files:**

- Modify: `plugins/ideal-agent-loop/scripts/loop_kernel.py`
- Create: `plugins/ideal-agent-loop/tests/test_runs.py`
- Create: `plugins/ideal-agent-loop/tests/test_review_budget.py`

**Step 1: Write Run tests**

Assert:

- start records assignment hash, Goal revision, phase, task, capability locator, and role;
- finish records terminal outcome and artifact/evidence refs;
- finished Run files cannot be overwritten;
- execution cannot write validator conclusion;
- validation cannot return modified candidate artifacts;
- unchanged candidate/criteria/input hashes reuse passing evidence;
- terminal review budget defaults to one;
- review finding never creates a review task.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_runs.py \
  plugins/ideal-agent-loop/tests/test_review_budget.py -v
```

Expected: missing Run APIs.

**Step 3: Implement Run APIs**

```python
begin_run(root, assignment, role) -> dict
finish_run(root, run_id, outcome, artifact_refs, evidence_refs, root_cause=None) -> dict
find_reusable_evidence(root, candidate_hash, criteria_hash, input_hashes) -> dict | None
review_allowed(profile, candidate_hash, prior_runs) -> bool
```

Allowed outcomes:

```text
completed, blocked, waiting, human_gate, no_op, failed, cancelled
```

**Step 4: Run focused tests**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_runs.py \
  plugins/ideal-agent-loop/tests/test_review_budget.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/scripts/loop_kernel.py \
  plugins/ideal-agent-loop/tests/test_runs.py \
  plugins/ideal-agent-loop/tests/test_review_budget.py
git commit -m "feat(loop): record bounded execution runs"
```

---

### Task 11: Implement the outer Goal Loop and cooperative stop policy

**Files:**

- Modify: `plugins/ideal-agent-loop/scripts/loop_kernel.py`
- Modify: `plugins/ideal-agent-loop/scripts/agent_loop_stop_hook.py`
- Create: `plugins/ideal-agent-loop/tests/test_goal_loop.py`
- Create: `plugins/ideal-agent-loop/tests/test_stop_policy.py`

**Step 1: Write fixed/dynamic source tests**

Test:

- fixed binding re-reads only the specified Goal;
- dynamic binding selects dependency-satisfied goals by priority, deadline, then FIFO;
- stale backlog revision causes reload;
- no ready work returns `no_op`;
- waiting/blocked/human gate do not continue;
- ready work continues only when retry/review/permission budgets allow;
- three failures with the same root cause block instead of strategy reset.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_goal_loop.py \
  plugins/ideal-agent-loop/tests/test_stop_policy.py -v
```

Expected: current Stop Hook continues cases that should terminate.

**Step 3: Implement one-iteration controller**

Add a command that performs exactly one bounded iteration:

```text
loop_kernel.py step \
  --backlog-cli <path> \
  --profile <path> \
  --capabilities <path> \
  --source-binding fixed|dynamic \
  [--goal-id <id>] \
  --apply
```

The command may create one execution assignment or one validation assignment, but never both in the same Run.

Change Stop Hook semantics from “never stop before accepted” to:

```python
continue_running = (
    ready_work_exists
    and not blocked
    and not waiting
    and not human_gate
    and retry_budget_available
    and review_budget_available
)
```

**Step 4: Run loop and stop-policy tests**

```bash
python3 -m unittest \
  plugins/ideal-agent-loop/tests/test_goal_loop.py \
  plugins/ideal-agent-loop/tests/test_stop_policy.py -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/scripts/loop_kernel.py \
  plugins/ideal-agent-loop/scripts/agent_loop_stop_hook.py \
  plugins/ideal-agent-loop/tests/test_goal_loop.py \
  plugins/ideal-agent-loop/tests/test_stop_policy.py
git commit -m "feat(loop): add bounded goal loop controller"
```

---

### Task 12: Convert existing development behavior into adapters

**Files:**

- Modify: `plugins/ideal-agent-loop/scripts/agent_loop_state.py`
- Modify: `plugins/ideal-agent-loop/scripts/agent_loop_verify.py`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/worktree-goal-guide.md`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/merge-gate.md`
- Create: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/profile-contract.md`
- Create: `plugins/ideal-agent-loop/tests/test_development_profile.py`

**Step 1: Write compatibility tests**

Use the development Profile to prove:

- worktree is optional and profile-owned;
- merge gate runs only in the configured phase;
- existing criteria import into required artifacts;
- missing worktree configuration does not break a document Profile;
- Kernel code contains no hardcoded `ideal-dev-workflow` locator.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-agent-loop/tests/test_development_profile.py -v
```

Expected: current scripts contain development-specific assumptions.

**Step 3: Move assumptions behind adapters**

Keep existing behavior available through `development.json`; remove it from Kernel defaults. Document how a repository overrides adapter settings without redefining the Kernel.

**Step 4: Run all loop tests**

```bash
python3 -m unittest discover -s plugins/ideal-agent-loop/tests -v
```

Expected: pass.

**Step 5: Commit**

```bash
git add \
  plugins/ideal-agent-loop/scripts \
  plugins/ideal-agent-loop/profiles/development.json \
  plugins/ideal-agent-loop/skills/ideal-agent-loop/references \
  plugins/ideal-agent-loop/tests/test_development_profile.py
git commit -m "refactor(loop): move development rules to profile"
```

---

### Task 13: Rewrite the `ideal-agent-loop` Skill contract

**Files:**

- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/SKILL.md`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/contract-template.md`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/continuation-template.md`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/verification-guide.md`
- Modify: `plugins/ideal-agent-loop/skills/ideal-agent-loop/references/loop-config.md`
- Modify: `plugins/ideal-agent-loop/.claude-plugin/plugin.json`
- Create: `plugins/ideal-agent-loop/tests/test_skill_contract.py`

**Step 1: Write failing content tests**

Require:

```text
Goal Loop
Stage / Task Loop
Loop Profile
Capability Registry
Execution Run
Validation Run
fixed
dynamic
waiting
human_gate
no_op
review budget
evidence reuse
```

Reject:

- unconditional “不停止” language;
- direct raw edits to backlog state;
- hardcoded requirement to invoke `ideal-dev-workflow`.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest plugins/ideal-agent-loop/tests/test_skill_contract.py -v
```

Expected: current v1 contract fails new assertions.

**Step 3: Rewrite the Skill and references**

Make the normal workflow:

1. inspect;
2. bind;
3. lease;
4. plan one phase;
5. route one task;
6. execute or validate one Run;
7. checkpoint;
8. transition/block/release.

Update the plugin description, but not its version manually.

**Step 4: Validate**

```bash
python3 -m unittest discover -s plugins/ideal-agent-loop/tests -v
claude plugin validate plugins/ideal-agent-loop
```

Expected: pass.

**Step 5: Create the major changeset and version commit**

Use the maintainer flow with a `major` bump and message:

```text
Add the profile-driven bounded Loop Kernel
```

Expected final version: `ideal-agent-loop@2.0.0`.

---

### Task 14: Add cross-plugin golden scenarios

**Files:**

- Create: `tests/loop-kernel/test_end_to_end.py`
- Create: `tests/loop-kernel/fixtures/development/`
- Create: `tests/loop-kernel/fixtures/document/`
- Create: `tests/loop-kernel/fixtures/v1/需求池.md`

**Step 1: Write failing E2E scenarios**

Scenarios:

1. migrate one v1 Goal;
2. fixed binding completes two dependent development tasks;
3. dynamic binding chooses a ready Goal using priority/deadline/FIFO;
4. execution and validation become separate immutable Runs;
5. unchanged candidate reuses evidence;
6. changed business artifact invalidates only downstream evidence;
7. review finding creates a substantive repair assignment, not review-of-review;
8. repeated root cause blocks on the third failure;
9. human gate releases the lease;
10. document Profile runs without worktree or merge assumptions;
11. ordinary runner cannot accepted;
12. reopen preserves historical evidence and requires regression metadata.

**Step 2: Run and confirm failure**

```bash
python3 -m unittest tests/loop-kernel/test_end_to_end.py -v
```

Expected: one or more integration mismatches.

**Step 3: Make only integration-level fixes**

Do not add new infrastructure. Fix protocol mismatches in existing CLI/kernel code and add focused regression tests beside each fix.

**Step 4: Run complete suites**

```bash
python3 -m unittest discover -s plugins/ideal-backlog/tests -v
python3 -m unittest discover -s plugins/ideal-agent-loop/tests -v
python3 -m unittest tests/loop-kernel/test_end_to_end.py -v
```

Expected: all pass.

**Step 5: Commit**

```bash
git add \
  tests/loop-kernel \
  plugins/ideal-backlog \
  plugins/ideal-agent-loop
git commit -m "test(loop): cover cross-profile golden scenarios"
```

Use targeted staging after checking the exact diff.

---

### Task 15: Validate versions, docs, and repository integrity

**Files:**

- Modify: `plugins/ideal-backlog/CHANGELOG.md` through Changesets
- Modify: `plugins/ideal-agent-loop/CHANGELOG.md` through Changesets
- Modify: `plugins/ideal-backlog/package.json` through Changesets
- Modify: `plugins/ideal-agent-loop/package.json` through Changesets
- Modify: both `.claude-plugin/plugin.json` versions through maintainer synchronization
- Modify only if required: `.claude-plugin/marketplace.json`

**Step 1: Verify no private academic content leaked**

```bash
rg -n \
  'PAPER-|PATENT-|academic-workflow|WWW 2027|private data|venue' \
  plugins/ideal-agent-loop \
  plugins/ideal-backlog \
  tests/loop-kernel
```

Expected: no private identifiers or private workflow source; generic documentation references must be reviewed explicitly.

**Step 2: Run all automated checks**

```bash
python3 -m unittest discover -s plugins/ideal-backlog/tests -v
python3 -m unittest discover -s plugins/ideal-agent-loop/tests -v
python3 -m unittest tests/loop-kernel/test_end_to_end.py -v
claude plugin validate plugins/ideal-backlog
claude plugin validate plugins/ideal-agent-loop
plugins/ideal-lab-maintainer/scripts/validate.sh
```

Expected: all pass.

**Step 3: Verify version consistency**

```bash
node -e "
for (const p of ['ideal-backlog', 'ideal-agent-loop']) {
  const a = require('./plugins/' + p + '/package.json').version;
  const b = require('./plugins/' + p + '/.claude-plugin/plugin.json').version;
  if (a !== b) throw new Error(p + ': ' + a + ' != ' + b);
  console.log(p, a);
}"
```

Expected:

```text
ideal-backlog 2.0.0
ideal-agent-loop 2.0.0
```

**Step 4: Inspect exact final diff**

```bash
git status --short
git diff --stat main...HEAD
git diff --check main...HEAD
git log --oneline --decorate main..HEAD
```

Expected:

- no cache, private workspace, generated temporary, or unrelated files;
- no whitespace errors;
- commits match the task slices.

**Step 5: Run bounded terminal review**

Run one terminal review over the substantive 2.0 candidate. Findings may:

- block release;
- require a concrete code/contract fix;
- require a focused regression.

Findings may not create another review framework, full matrix, controller rewrite, or review-of-review. After concrete fixes, rerun only affected checks plus the final complete suite once.

---

### Task 16: Publish and verify the released plugins

**Files:** no new source files expected.

**Step 1: Push the implementation branch**

Use the maintainer release flow. Verify branch upstream and remote commit:

```bash
git push -u origin codex/loop-kernel-profile
git rev-parse HEAD
git rev-parse origin/codex/loop-kernel-profile
```

Expected: hashes match.

**Step 2: Merge through the repository's accepted flow**

Do not merge automatically unless authorized. After merge, verify `origin/main` contains both 2.0 changesets and release commits.

**Step 3: Push release tags**

Use:

```text
/ideal-lab-maintainer:maintainer release
```

Expected: both plugin release tags exist remotely.

**Step 4: Update local plugin installation**

Only after GitHub push succeeds:

- update/reinstall `ideal-backlog`;
- update/reinstall `ideal-agent-loop`;
- restart/reload the host if required.

**Step 5: Verify actual loaded versions and smoke behavior**

Confirm the host loads:

```text
ideal-backlog@2.0.0
ideal-agent-loop@2.0.0
```

Run one disposable development Profile smoke:

- initialize a temporary Goal Store;
- create/claim one Goal;
- execute one no-side-effect mock task;
- produce separate execution/validation Runs;
- stop cleanly at awaiting acceptance.

Do not use a real project backlog for the release smoke.

---

## Delivery checkpoints

| Checkpoint | Required proof | Stop if |
|---|---|---|
| Backlog M1 | immutable revisions, locks, leases, migration, mirror tests | lost fields, stale write accepted, mirror divergence |
| Kernel M2 | two Profiles, task DAG, capability routing, immutable Runs | domain hardcode, second Goal truth |
| Safety M3 | bounded retries/reviews, evidence reuse, human/no-op stop | review recursion, unconditional continuation |
| Compatibility M4 | development behavior preserved through adapters | worktree/merge leaked into Kernel |
| Release | versions, plugin validation, remote/local hash, loaded version | any mismatch or unapproved external action |

The implementation is complete only when the final environment outcome matches the design; passing unit tests alone is insufficient.
