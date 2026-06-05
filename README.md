# Talaria

> In Greek mythology, the *Talaria* are the winged sandals of Hermes — forged by Hephaestus, they let the messenger god fly as fast as any bird.

Local kanban board for task management. No Docker required.

## Overview

- **Tasks**: Stored as markdown files in `/tasks` directory
- **Projects**: Configured in `data/projects.json` with real filesystem paths
- **Server**: Lightweight Python HTTP server
- **Access**: http://localhost:8080

## Quick Start

```bash
./start.sh
```

This will:
1. Generate `tasks.json` from markdown files in `/tasks`
2. Start Python server on port 8080
3. Open browser automatically

## Project Configuration

Edit `data/projects.json` to add/modify projects:

```json
[
  {
    "id": "project-id",
    "name": "Project Name",
    "path": "/absolute/path/to/project",
    "description": "Project description",
    "language": "gdscript",
    "active": true
  }
]
```

**Note**: Use absolute filesystem paths for the `path` field.

## Task Management

Tasks are markdown files in `/tasks` with frontmatter:

```markdown
---
title: Task Title
status: todo
priority: high
project: project-id
---

Task description here.
```

The `scripts/md_to_talaria.sh` script converts these to `tasks.json` for the web UI.
