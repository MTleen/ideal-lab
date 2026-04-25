#!/usr/bin/env bash
set -u

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root" || exit 1

failed=0

run_check() {
  local label="$1"
  shift
  echo "==> $label"
  if "$@"; then
    echo "PASS: $label"
  else
    echo "FAIL: $label" >&2
    failed=1
  fi
}

if command -v claude >/dev/null 2>&1; then
  for plugin_dir in plugins/*; do
    [ -d "$plugin_dir" ] || continue
    [ -f "$plugin_dir/.claude-plugin/plugin.json" ] || continue
    run_check "claude plugin validate $plugin_dir" claude plugin validate "$plugin_dir"
  done
  run_check "claude plugin validate ." claude plugin validate .
else
  echo "FAIL: claude command not found" >&2
  failed=1
fi

echo "==> version consistency"
while IFS= read -r manifest; do
  plugin_dir="$(dirname "$(dirname "$manifest")")"
  package_json="$plugin_dir/package.json"
  if [ ! -f "$package_json" ]; then
    echo "FAIL: missing $package_json" >&2
    failed=1
    continue
  fi

  plugin_version="$(node -e "console.log(require('./$manifest').version || '')")"
  package_version="$(node -e "console.log(require('./$package_json').version || '')")"
  if [ "$plugin_version" != "$package_version" ]; then
    echo "FAIL: version mismatch in $plugin_dir ($plugin_version != $package_version)" >&2
    failed=1
  else
    echo "PASS: $plugin_dir version $plugin_version"
  fi
done < <(find plugins -path '*/.claude-plugin/plugin.json' -type f | sort)

echo "==> skill frontmatter"
while IFS= read -r skill_file; do
  if awk '
    NR == 1 && $0 != "---" { exit 1 }
    NR > 1 && $0 == "---" { found_end = 1; exit 0 }
    END { if (!found_end) exit 1 }
  ' "$skill_file" && grep -q '^name:' "$skill_file" && grep -q '^description:' "$skill_file"; then
    echo "PASS: $skill_file"
  else
    echo "FAIL: invalid frontmatter in $skill_file" >&2
    failed=1
  fi
done < <(find plugins -path '*/skills/*/SKILL.md' -type f | sort)

exit "$failed"
