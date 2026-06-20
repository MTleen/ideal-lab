## Agent Loop: iteration {{ iteration }}/{{ max_iterations }}

You are in a persistent task loop. Do NOT stop until all criteria pass.

### Objective

{{ objective }}

### Progress

{{ progress_summary }}

### Completed Work

{{ completed_work }}

### Next Action

Work on criterion **#{{ next_id }}** ({{ next_verify_type }}): {{ next_desc }}

{{ next_hint }}

### Completion Audit Rules

Before deciding this task is done, you MUST:
1. Restate the objective as concrete deliverables.
2. Map every criterion to real evidence (file content, test output, command result).
3. Do NOT accept proxy signals. A passing test alone is not enough — verify it covers the requirement.
4. Treat uncertainty as NOT achieved. Do more verification or keep working.
5. Do NOT mark a criterion passed without fresh, specific evidence.

Do NOT stop. Continue working on the next criterion.
