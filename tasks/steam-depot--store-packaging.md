---
title: "Steam Depot & Store Packaging"
id: "046"
status: todo
priority: 02
sprint: alpha
category: DEVOPS
description: "Create SteamPipe VDFs, branch SOP, signing/notarization, platform filters."
---
### Goal / Risk

Create SteamPipe VDFs, branch SOP, signing/notarization, platform filters.

### Files / Areas

tools/steam/, export presets

### Execution Checklist

- [ ] Create tools/steam/app_build_<STEAM_APP_ID>.vdf and per-platform depot templates.
- [ ] Document steamcmd upload command, branch promotion path.
- [ ] Add guidance for Windows signing, macOS notarization, Android package name.
- [ ] Configure store-specific export filters.
### AI Execution Prompt

```plain text
Add Steam and storefront release packaging workflow for Tekton after P0/P1 backend gates are complete. Review export_presets.cfg, docs/STEAMWORKS_SETUP.md, README.md, and current build output conventions. Create tools/steam/app_build_<STEAM_APP_ID>.vdf and per-platform depot VDF templates using placeholders only. Document steamcmd upload command, branch promotion path internal -> beta -> default, and smoke tests required before promotion. Add guidance for Windows signing, macOS bundle/team/notarization, Android final package name/version code, and store-specific export filters so Steam libraries are not shipped in non-Steam builds. Acceptance: no real IDs/secrets committed; SteamPipe templates exist; release checklist blocks default branch promotion until smoke tests pass.
```

### Testing / Auto-Check

AI AUTO-CHECK: Trigger dry-run of SteamPipe VDF. Assert paths resolve to output directory without committing real credentials.

### MS Teams Daily Report

```plain text
**Completed [PRD-P2-1]: Steam Depot & Store Packaging**\n- **Goal:** Create SteamPipe VDFs, branch SOP, signing/notarization, platform filters.\n- **Status:** Integrated & verified. Code changes applied to: tools/steam/, export presets
```
