#!/usr/bin/env python3
"""
Convert markdown task files to JSON format.
Reads .md files from tasks/ directory, parses YAML frontmatter,
and outputs JSON array to data/tasks.json.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown content.
    Returns (frontmatter_dict, remaining_content).
    """
    # Match YAML frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = match.group(2)

    # Parse YAML manually (simple key: value pairs)
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # Convert to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.lower() in ('null', 'none', ''):
                value = None
            elif value.isdigit():
                value = int(value)

            frontmatter[key] = value

    return frontmatter, body.strip()


def process_task_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Process a single markdown task file.
    Returns task dict or None if parsing fails.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)

        # Extract fields with defaults
        task = {
            'id': frontmatter.get('id', filepath.stem),
            'title': frontmatter.get('title', ''),
            'status': frontmatter.get('status', 'todo'),
            'priority': frontmatter.get('priority', 'medium'),
            'sprint': frontmatter.get('sprint'),
            'category': frontmatter.get('category'),
            'description': frontmatter.get('description', ''),
            'content': body,
            'halt_reason': frontmatter.get('halt_reason'),
            'modified': frontmatter.get('modified'),
            'file': filepath.name
        }

        return task

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None


def main():
    """Main execution function."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tasks_dir = project_root / 'tasks'
    output_file = project_root / 'data' / 'tasks.json'

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing tasks.json to preserve runtime status changes
    existing_status: Dict[str, str] = {}
    existing_halt_reason: Dict[str, Optional[str]] = {}
    existing_modified: Dict[str, Optional[str]] = {}
    if output_file.exists():
        try:
            with open(output_file, encoding='utf-8') as f:
                for t in json.load(f):
                    tid = str(t.get('id', ''))
                    if tid:
                        existing_status[tid] = t.get('status', 'todo')
                        existing_halt_reason[tid] = t.get('halt_reason')
                        existing_modified[tid] = t.get('modified')
        except Exception:
            pass

    # Process all .md files
    tasks = []
    if tasks_dir.exists():
        for md_file in sorted(tasks_dir.glob('*.md')):
            task = process_task_file(md_file)
            if task:
                tid = str(task.get('id', ''))
                # Preserve status set at runtime (e.g. moved via UI/agent)
                # Only override if we have a previously saved status
                if tid in existing_status:
                    task['status'] = existing_status[tid]
                    # Preserve halt_reason if status is halt
                    if task['status'] == 'halt' and existing_halt_reason.get(tid):
                        task['halt_reason'] = existing_halt_reason[tid]
                    # Preserve modified date set at runtime
                    if existing_modified.get(tid):
                        task['modified'] = existing_modified[tid]
                tasks.append(task)

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(tasks)} tasks -> {output_file}")


if __name__ == '__main__':
    main()
