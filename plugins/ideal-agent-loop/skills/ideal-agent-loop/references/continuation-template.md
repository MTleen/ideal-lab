## Agent Loop: bounded continuation {{ iteration }}/{{ max_iterations }}

### Objective

{{ objective }}

### Progress

{{ progress_summary }}

### Completed work

{{ completed_work }}

### Ready task

Criterion **#{{ next_id }}** ({{ next_verify_type }}): {{ next_desc }}

{{ next_hint }}

Continue with this one ready task only while retry, review, and permission
budgets remain available. Record fresh artifact or evidence references.

If work is `blocked`, `waiting`, `human_gate`, `no_op`, or awaiting acceptance,
record the structured outcome and release the execution slot. Reuse evidence
when candidate, criteria, and input hashes are unchanged.
