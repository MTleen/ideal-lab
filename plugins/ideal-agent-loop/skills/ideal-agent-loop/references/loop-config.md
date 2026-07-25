# Profile and adapter configuration

The v2 Kernel reads deterministic Profile JSON. It does not parse YAML and does
not load user-global configuration.

## Profile JSON

```json
{
  "schema": "ideal-agent-loop/profile-v1",
  "id": "example",
  "phases": [],
  "capabilities": {},
  "policies": {
    "retry": {
      "max_same_root_cause": 3
    },
    "review": {
      "terminal_budget": 1,
      "reuse_unchanged_candidate": true,
      "validation_infrastructure_budget": 0
    },
    "permissions": {
      "allowed": [
        "workspace-read"
      ],
      "external_side_effects": "human_only"
    }
  }
}
```

The included development Profile is
`plugins/ideal-agent-loop/profiles/development.json`.

## Optional adapters

Adapters are Profile-owned:

```json
{
  "adapters": {
    "workspace": "git-worktree-optional",
    "integration_gate": "merge-gate"
  },
  "adapter_settings": {
    "git-worktree-optional": {
      "optional": true
    },
    "merge-gate": {
      "phase": "implementation"
    }
  }
}
```

A Profile without adapters remains valid. The integration adapter activates
only in its configured phase. Worker locators come from the Capability
Registry, never from this configuration.
