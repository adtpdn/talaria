---
title: "Tutorial Isolation Contract"
id: "044"
status: todo
priority: 01
sprint: alpha
category: CLIENT
description: "Remove multiplayer-side effects during pause/freeze phases. Isolate tutorial boundaries."
---
### Goal / Risk

Remove multiplayer-side effects during pause/freeze phases. Isolate tutorial boundaries.

### Files / Areas

tutorial_manager.gd

### Execution Checklist

- [ ] Keep onboarding sequence and camera storytelling.
- [ ] Enforce contract: no persistent wallet/profile mutation during tutorial.
- [ ] Ensure no shared lobby state leakage.
- [ ] Ensure clean bot/timer restore on exit, deterministic return-to-lobby handshake.
- [ ] Replace broad pause/freeze side effects with scoped tutorial-state toggles.
### AI Execution Prompt

```plain text
Isolate tutorial runtime from multiplayer/session side effects. Review scripts/managers/tutorial_manager.gd and match lifecycle hooks. Keep onboarding sequence and camera storytelling, but enforce tutorial contract: no persistent wallet/profile mutation, no shared lobby state leakage, clean bot/timer restore on exit, deterministic return-to-lobby handshake. Replace broad pause/freeze side effects with scoped tutorial-state toggles where possible. Acceptance: exiting tutorial leaves no stale bot freeze, no leaked paused systems, and no corrupted room/session flags.
```

### Testing / Auto-Check

AI AUTO-CHECK: Abort tutorial midway. Assert main game tree is fully unpaused, bots are reset, and no 'tutorial_active' flags leak into lobby.

### MS Teams Daily Report

```plain text
**Completed [PRD-GF-P1-1]: Tutorial Isolation Contract**\n- **Goal:** Remove multiplayer-side effects during pause/freeze phases. Isolate tutorial boundaries.\n- **Status:** Integrated & verified. Code changes applied to: tutorial_manager.gd
```
