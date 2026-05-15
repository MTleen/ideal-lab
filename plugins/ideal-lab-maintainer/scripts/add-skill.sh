#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <plugin-name> <skill-name> <description>" >&2
}

if [ "$#" -lt 3 ]; then
  usage
  exit 1
fi

plugin_name="$1"
skill_name="$2"
shift 2
description="$*"

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root"

plugin_dir="plugins/$plugin_name"
skill_dir="$plugin_dir/skills/$skill_name"
skill_file="$skill_dir/SKILL.md"

if [ ! -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
  echo "Plugin not found: $plugin_name" >&2
  exit 1
fi

if [ -e "$skill_file" ]; then
  echo "Skill already exists: $skill_file" >&2
  exit 1
fi

mkdir -p "$skill_dir"
cat > "$skill_file" <<EOF
---
name: $skill_name
description: "$description"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# $skill_name

## Purpose

TODO: describe when to use this skill.

## Workflow

1. TODO
EOF

echo "Created $skill_file"
echo "Edit the skill body, then run: claude plugin validate $plugin_dir"
