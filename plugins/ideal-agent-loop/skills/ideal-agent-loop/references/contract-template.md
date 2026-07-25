# Bounded assignment contract

The v2 contract binds work to a Goal revision and one Stage task. Goal revision
and quality state remain in `ideal-backlog`; this assignment is an immutable
Run input.

## Assignment

```json
{
  "goal_id": "REQ-001",
  "goal_revision": "sha256:...",
  "phase": "implementation",
  "task_id": "implement",
  "role": "execution",
  "produces": ["implementation-artifact"],
  "lease_token_hash": "sha256:...",
  "capability": {
    "id": "code-implementation",
    "locator": "registry:worker",
    "version": "1.0.0"
  },
  "candidate_hash": "sha256:...",
  "criteria_hash": "sha256:...",
  "input_hashes": [
    "sha256:..."
  ],
  "validation_fingerprint": "sha256:..."
}
```

Required fields:

| Field | Contract |
|---|---|
| Goal revision | Must equal the revision from the latest backlog inspection |
| phase/task | Must exist in the selected Loop Profile Task Plan |
| role | Exactly `execution` or `validation` |
| produces | Exact output refs authorized for this Task and Run role |
| lease digest | Must match the lease token presented when starting the Run |
| capability | Verified registry ID, locator, and version |
| candidate hash | Hash of the substantive candidate |
| criteria hash | Hash of the applicable phase gate criteria |
| input hashes | Hashes of business inputs consumed by this assignment |
| validation fingerprint | Validator ID/locator/version plus Profile/Gate policy digest |

An assignment cannot authorize external side effects or acceptance. Those
authorities remain in the Profile and Goal.

## Legacy criterion import

The v1 `.agent-loop/.../contract.json` format may be imported as validation
evidence requirements. Each criterion becomes `criterion-{id}-evidence`.
Legacy contract/state files never replace the v2 Goal revision or Task Plan.
