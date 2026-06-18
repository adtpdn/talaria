#!/usr/bin/env bash
# Build static GitHub Pages site into docs/
# Run from repo root: bash scripts/build_pages.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="$ROOT/docs"

echo "Building GitHub Pages site → docs/"

# Regenerate tasks.json from markdown
bash "$ROOT/scripts/md_to_talaria.sh"

# Ensure docs dir exists
mkdir -p "$DOCS/js"

# Copy HTML, JS, data
cp "$ROOT/html/index.html" "$DOCS/index.html"
cp "$ROOT/html/js/agent.js" "$DOCS/js/agent.js"
cp "$ROOT/data/tasks.json" "$DOCS/tasks.json"

# Ensure .nojekyll exists
touch "$DOCS/.nojekyll"

echo "Done. Files in docs/:"
ls -la "$DOCS/"
echo ""
echo "To deploy: commit docs/ and enable GitHub Pages (source: main, folder: /docs)"
