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
mkdir -p "$DOCS/js" "$DOCS/assets"

# Copy HTML, JS, data
cp "$ROOT/html/index.html" "$DOCS/index.html"
cp "$ROOT/html/js/agent.js" "$DOCS/js/agent.js"
cp "$ROOT/data/tasks.json" "$DOCS/tasks.json"

# Copy assets (logo, favicon, etc.) so pages and the board share them
cp -r "$ROOT/html/assets/." "$DOCS/assets/"

# Render /pages/*.md → docs/<slug>/index.html + docs/pages.json
python3 "$ROOT/scripts/md_pages_to_json.py"

# Mirror docs/pages.json → html/pages.json so the dev server (python http.server
# rooted at html/) can serve the same nav dropdown without needing its own build.
cp "$DOCS/pages.json" "$ROOT/html/pages.json"

# Ensure .nojekyll exists
touch "$DOCS/.nojekyll"

echo ""
echo "Done. Top-level entries in docs/:"
ls -la "$DOCS/" | grep -E "^d|^-" || ls -la "$DOCS/"
echo ""
echo "To deploy: commit docs/ and enable GitHub Pages (source: main, folder: /docs)"