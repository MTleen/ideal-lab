# Loop Profile contract

A Loop Profile supplies domain differences to the public Kernel. It declares:

- phases, required artifacts, Stage Task definitions, and phase gates;
- Capability requirements as exact inputs, outputs, and permissions;
- retry, terminal review, evidence reuse, permission, and acceptance policies;
- optional adapters that are outside the Kernel.

The Kernel owns no domain phase names and no Worker locator. A Profile may
request an adapter, but missing adapter configuration is not an error unless
that Profile marks it required.

## Adapter resolution

The built-in development Profile exposes:

```json
{
  "adapters": {
    "workspace": "git-worktree-optional",
    "integration_gate": "merge-gate"
  }
}
```

`git-worktree-optional` has no effect unless enabled by project configuration.
`merge-gate` is active only in its configured phase. A Profile without
`adapters` runs through the same Goal, Task Plan, Capability, Run, Gate, and
Checkpoint contracts.

## v1 criteria compatibility

Legacy criterion records are imported as validation-owned required evidence
artifacts. They do not own Goal status. The compatibility verifier may emit
evidence references and a validation conclusion, but it must emit no modified
candidate artifact.
