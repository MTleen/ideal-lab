# Validation Run guide

Validation is a separate bounded Run. It may read candidate artifacts and emit
evidence plus a conclusion; it must not modify the candidate.

## Roles

| Role | May produce | Must not produce |
|---|---|---|
| Execution Run | declared candidate artifacts | validation evidence, validator conclusion, acceptance |
| Validation Run | validation evidence, `pass`/`fail` | modified candidate artifact, acceptance |
| acceptance authority | acceptance evidence and transition | execution or validation work |

## Validation methods

### Script

Record the exact command, exit status, relevant stdout/stderr, and coverage of
the criterion. Exit zero proves the command passed; it does not by itself prove
the full Goal.

### Structured judgment

Break the criterion into checks. For each check, cite an artifact location and
specific observed content. Missing evidence is a failure, not a reason to infer
success.

### Hybrid

Run the objective script portion first, then structured judgment. Both must
pass. Keep their evidence distinct in the Validation Run.

## Evidence reuse

Reuse a passing Validation Run only when all are identical:

- candidate hash;
- criteria hash;
- business input hashes.
- resolved validator ID, locator, and version;
- Profile/Gate policy fingerprint.

Changes to a reviewer implementation, run ledger, formatting, or commit
metadata do not invalidate passing business evidence. Changed business inputs
invalidate their downstream dependency nodes.

## Review budget

The terminal review budget defaults to one per substantive candidate. A
finding can block release or create a substantive repair assignment and
focused regression. It cannot create another review task, controller, full
matrix, or validation platform. Default new validation-infrastructure budget
is zero.

## Outcomes

Use a structured terminal outcome:

```text
completed | blocked | waiting | human_gate | no_op | failed | cancelled
```

Three consecutive failures with the same root cause become `blocked`.
`waiting`, `human_gate`, and `no_op` release the execution slot.
