#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <plugin-name> <patch|minor|major> <message>" >&2
}

if [ "$#" -lt 3 ]; then
  usage
  exit 1
fi

plugin_name="$1"
bump_type="$2"
shift 2
message="$*"

case "$bump_type" in
  patch|minor|major) ;;
  *)
    echo "Invalid bump type: $bump_type" >&2
    usage
    exit 1
    ;;
esac

root="$(git rev-parse --show-toplevel)"
cd "$root"

plugin_dir="plugins/$plugin_name"
manifest="$plugin_dir/.claude-plugin/plugin.json"
package_json="$plugin_dir/package.json"

if [ ! -f "$manifest" ] || [ ! -f "$package_json" ]; then
  echo "Plugin not found or incomplete: $plugin_name" >&2
  exit 1
fi

if [ -z "$(git status --short)" ]; then
  echo "No changes to commit."
  exit 0
fi

mkdir -p .changeset
slug="$(printf '%s-%s' "$plugin_name" "$(date +%Y%m%d%H%M%S)" | tr -cd '[:alnum:]-')"
changeset_file=".changeset/$slug.md"

cat > "$changeset_file" <<EOF
---
"$plugin_name": $bump_type
---

$message
EOF

npx changeset version

package_version="$(node -e "console.log(require('./$package_json').version)")"
node - "$manifest" "$package_version" <<'NODE'
const fs = require("fs");
const [manifestPath, version] = process.argv.slice(2);
const data = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
data.version = version;
fs.writeFileSync(manifestPath, JSON.stringify(data, null, 2) + "\n");
NODE

git add .
git commit -m "$message"
