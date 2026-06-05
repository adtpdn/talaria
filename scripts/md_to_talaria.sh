#!/usr/bin/env bash
# Parse task markdown files into tasks.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/md_to_json.py"
