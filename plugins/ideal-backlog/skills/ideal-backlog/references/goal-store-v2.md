# Goal Store v2 contract

The Goal Store is the machine authority for the backlog. A generated Markdown mirror
is a deterministic, human-readable projection and is never an
independent state source.

## Goal record

Every v2 Goal contains:

- identity: `id`, `profile`, `project_path`, and `source_binding`;
- ordering: `priority`, optional `deadline`, FIFO creation time, and
  `dependencies`;
- independent `execution.status` and `quality.status`;
- current phase and next gate;
- the observed current store revision and current lease;
- evidence and history references;
- acceptance authorities.

The store revision is the SHA-256 of canonical JSON. `CURRENT` changes through
an atomic replace only after the immutable revision directory exists.

## Atomic mutation

A mutation is valid only when:

1. its expected revision equals `CURRENT`;
2. the global writer lock is held by the operation;
3. a Goal-scoped mutation presents the exact lease token;
4. the operation ID has not already produced another result, or its canonical
   kind, target, parent revision, and payload hash exactly match the retry;
5. the requested state edge is legal.

Old revision files are never modified or deleted.

## State authority

Execution states describe scheduling:

```text
todo → claimed → planning → executing → verifying
     → awaiting_acceptance → done
```

`blocked`, `waiting`, `human_gate`, and `cancelled` are explicit outcomes.
They release the execution lease. `awaiting_acceptance` also releases it.

Quality states describe evidence maturity:

```text
unverified → implemented → verified → awaiting_acceptance → accepted
```

`accepted` uses a separate authority operation with explicit evidence; it
never reuses an execution lease. `reopened` is also a separate authority
operation that preserves prior evidence and records the missed test plus
required regression. `transition` cannot modify identity, revision, lease,
history, or acceptance policy.

## v1 audit trail

Migration records the original path, source SHA-256, previous revision, and a
byte-preserving source snapshot. Unknown controlled fields or a non-empty v2
store block apply. A legacy `done` item without v2 evidence is labeled
`legacy_accepted` and can use the authorized reopen path. Restore writes a new
auditable revision from a verified historical target.
