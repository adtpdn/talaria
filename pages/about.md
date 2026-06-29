---
title: "About Talaria"
slug: "about"
description: "Project overview, goals, and tech stack for the Talaria task board."
modified: "2026-06-29"
---

# About Talaria

Talaria is a self-hosted, single-page Kanban board for game-dev task tracking. The
front end is a static site (vanilla HTML + JS + Markdown) that also runs in
GitHub Pages mode without any backend.

## Goals

- **Zero-config static deploy** — drop the `docs/` folder on any static host.
- **Markdown-first authoring** — every task and page is a `.md` file you can edit
  in any text editor or IDE.
- **Themeable UI** — six built-in color schemes tuned for long sessions.

## Tech Stack

| Layer    | Choice                          |
| -------- | ------------------------------- |
| Frontend | Vanilla JS, no build step       |
| Markup   | Markdown + YAML frontmatter     |
| Backend  | Python 3 `http.server` (local)  |
| Hosting  | GitHub Pages (`/docs`)          |

## Folder Layout

```
talaria/
├── html/        # Source UI (live dev)
├── docs/        # Static build output (GitHub Pages)
├── tasks/       # Kanban task markdown
├── pages/       # Long-form pages (this file lives here)
├── data/        # Generated JSON
└── scripts/     # Build + server utilities
```