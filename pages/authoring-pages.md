---
title: "Pages Authoring Guide"
slug: "authoring-pages"
description: "How to write and ship a static Talaria page."
modified: "2026-06-29"
---

# Pages Authoring Guide

Drop a Markdown file in `pages/` and it becomes a public page on the static
site at `/<slug>/`. Slug must be unique, lower-case, kebab-case.

## Frontmatter

```yaml
---
title: "Pages Authoring Guide"
slug: "authoring-pages"
description: "How to write and ship a static Talaria page."
modified: "2026-06-29"
---
```

| Field         | Required | Notes                                  |
| ------------- | -------- | -------------------------------------- |
| `title`       | yes      | Shown in nav dropdown + browser tab.   |
| `slug`        | yes      | URL segment. Becomes `docs/<slug>/`.   |
| `description` | no       | Used for hover tooltips.               |
| `modified`    | no       | ISO date (`YYYY-MM-DD`).               |

## Build

Pages are generated automatically by `scripts/build_pages.sh`. Each one is
rendered to `docs/<slug>/index.html` so the URL is a clean permalink:

```
docs/authoring-pages/index.html  →  https://<host>/talaria/authoring-pages/
```

Markdown is rendered with the same engine as the task modal (`marked` +
`highlight.js` for code blocks).