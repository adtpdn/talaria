---
title: "Versioning & Patch Integrity"
id: "045"
status: todo
priority: 01
sprint: alpha
category: DEVOPS
description: "Single release version source, checksums, compatibility rules, changelog archive."
---
### Goal / Risk

Single release version source, checksums, compatibility rules, changelog archive.

### Files / Areas

tools/, export_presets.cfg, version.json

### Execution Checklist

- [ ] Create one release version source (version.json or python script).
- [ ] Update project version, export versions, Android version deterministically.
- [ ] Update patch manifest and changelog archive.
- [ ] Add patch integrity fields: checksum, size, minimum compatible app version.
### AI Execution Prompt

```plain text
Rebuild Tekton versioning workflow. Review tools/generate_version_json.py, tools/build_patch.gd, export_presets.cfg, project.godot, assets/data/version.json, README.md, and CHANGELOG_DRAFT.md. Create one release version source and update all platform metadata deterministically: project version, export versions, Android version/code, patch manifest, changelog archive, and Git tag instructions. Add patch integrity fields such as checksum, size, minimum compatible app version, and signature placeholder if signing is not available yet. Acceptance: one command or documented flow bumps release version; generated metadata matches across files; patch manifest can reject incompatible or corrupted patch.pck.
```

### Testing / Auto-Check

AI AUTO-CHECK: Run version bump script. Assert export_presets.cfg Android version code increments correctly and patch manifest checksum is updated.

### MS Teams Daily Report

```plain text
**Completed [PRD-P1-4]: Versioning & Patch Integrity**\n- **Goal:** Single release version source, checksums, compatibility rules, changelog archive.\n- **Status:** Integrated & verified. Code changes applied to: tools/, export_presets.cfg, version.json
```
