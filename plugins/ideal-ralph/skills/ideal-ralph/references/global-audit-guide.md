# Global Audit Guide

When all individual criteria have passed, perform a global audit BEFORE generating `report.md`. This ensures the overall objective is truly met, not just individual checkpoints.

## Audit Steps

### Step 1: Restate the Objective

Read `contract.json` and restate the user's original `description` as a set of concrete deliverables. Each deliverable should be a tangible artifact (file, behavior, test result) rather than an abstract goal.

### Step 2: Build a Prompt-to-Artifact Checklist

For every item in the contract's `output` array and every `criteria` entry, create a checklist row:

```
| Deliverable | Expected | Actual Evidence | Covered? |
|-------------|----------|-----------------|----------|
| OAuth module | New file src/auth/oauth.ts | File exists, exports ... | Yes |
| Login flow | Complete GitHub OAuth flow | Only Google flow implemented | NO |
```

### Step 3: Inspect Real Evidence

For each checklist row:
- Read the actual file, run the actual test, check the actual command output.
- Do NOT rely on memory of earlier work or a plausible narrative.
- Do NOT accept proxy signals:
  - "Tests pass" does NOT mean "requirement is met" — verify coverage.
  - "File exists" does NOT mean "file is correct" — verify content.
  - "No errors" does NOT mean "feature works" — verify behavior.

### Step 4: Identify Gaps

Any deliverable that is:
- Missing entirely
- Only partially implemented
- Verified only by proxy signal (test pass without coverage check)
- Marked as `manual_accept` (acceptable, but note it)

...is a **gap** that must be addressed.

### Step 5: Decision

- **No gaps found** → Proceed to generate `report.md`.
- **Gaps found** → For each gap, create a new criterion in `state.json`:

```json
{
  "id": <next_available_id>,
  "desc": "<gap description>",
  "verify_type": "llm_judgment",
  "command": null,
  "status": "pending",
  "attempts": 0,
  "last_error": null,
  "evidence": null,
  "updated_at": null,
  "affected_files": [],
  "source": "global_audit"
}
```

Then return to LOOP Step 1 to continue working.

### Maximum Audit Rounds

The global audit runs at most **1 round**. If the audit finds gaps and new criteria are added, the LOOP continues normally. A second global audit is NOT performed — the normal criterion-level verification is sufficient for the newly added items.

## Anti-Patterns to Avoid

1. **Wishful verification**: "I remember writing this, so it should be fine." → Go read the file.
2. **Proxy substitution**: "The test suite is green, so the feature works." → Check test coverage of the specific requirement.
3. **Scope creep**: "While I'm auditing, I might as well improve X." → Only check contract deliverables.
4. **Rubber-stamping**: "Everything looks good." → Show specific evidence for each item.
