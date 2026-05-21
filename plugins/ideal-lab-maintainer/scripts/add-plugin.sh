#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <plugin-name> <description>" >&2
}

if [ "$#" -lt 2 ]; then
  usage
  exit 1
fi

plugin_name="$1"
shift
description="$*"

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$root"

plugin_dir="plugins/$plugin_name"
manifest_dir="$plugin_dir/.claude-plugin"
marketplace=".claude-plugin/marketplace.json"

if [ -e "$plugin_dir" ]; then
  echo "Plugin already exists: $plugin_dir" >&2
  exit 1
fi

mkdir -p "$manifest_dir" "$plugin_dir/skills"

node - "$manifest_dir/plugin.json" "$plugin_name" "$description" <<'NODE'
const fs = require("fs");
const [manifestPath, name, description] = process.argv.slice(2);
const manifest = {
  name,
  version: "1.0.0",
  description,
  author: { name: "MTleen" },
  skills: "./skills",
  keywords: []
};
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
NODE

cat > "$plugin_dir/package.json" <<EOF
{
  "name": "$plugin_name",
  "version": "1.0.0",
  "private": true
}
EOF

cat > "$plugin_dir/CHANGELOG.md" <<EOF
# $plugin_name

## 1.0.0

- Initial release.
EOF

node - "$marketplace" "$plugin_name" "$description" <<'NODE'
const fs = require("fs");
const [marketplacePath, name, description] = process.argv.slice(2);
const data = JSON.parse(fs.readFileSync(marketplacePath, "utf8"));
data.plugins ||= [];
if (!data.plugins.some((plugin) => plugin.name === name)) {
  data.plugins.push({
    name,
    source: `./plugins/${name}`,
    description,
    category: "development",
    keywords: []
  });
}
fs.writeFileSync(marketplacePath, JSON.stringify(data, null, 2) + "\n");
NODE

echo "Created $plugin_dir"
echo "Run: claude plugin validate $plugin_dir && claude plugin validate ."
