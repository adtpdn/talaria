---
title: "Sugar Rush: Polish — Rush Bar + ×N Badge"
id: "120"
status: "halt"
halt_reason: "need confirmation"
priority: 03
sprint: alpha
category: POLISH
description: "Fold the remaining Gauntlet polish work onto Sugar Rush visuals — rush bar (red), ×N multiplier badge on Mekton head, and HUD wiring."
modified: "2026-06-29"
supersedes: ["076"]
---

# Sugar Rush: Polish — Rush Bar + ×N Badge

## Problem
`#076 Gauntlet: Polish` is in progress, scoped to VFX / SFX / HUD / Arena
Scene wiring. Sugar Rush re-scopes that polish to the new visuals: red rush
bar, head-stack multiplier badge, and Mekton face-color beacon.

## Solution
Update the polish pass to cover Sugar Rush surfaces only.

### Changes
1. Replace the existing phase-label animation with a **Rush Bar**:
    - Red horizontal bar at top of HUD.
    - Fills / drains with `current_rush_time / rush_stacking_limit`.
2. Add **×N Badge** next to the Mekton head sprite (#127).
3. Add **Mekton Color Beacon** VFX (#123).
4. Add rush **SFX** cue on `_rotate_mekton_color` and `trigger_sugar_rush`.
5. Update `_setup_hud()` to include the new widgets.
6. Update `_animate_phase_label()` → `_animate_rush_bar()`.

## Acceptance Criteria
- Rush bar appears red when rush is active, drains visibly.
- ×N badge updates whenever the head stack changes.
- Mekton color rotation triggers a face-flash SFX.
- HUD layout fits 1080p and 720p.

## Migration Checklist
- [ ] Replace `_animate_phase_label` → `_animate_rush_bar`.
- [ ] Add ×N badge renderer.
- [ ] Add Mekton face-flash SFX.
- [ ] Verify HUD at 720p / 1080p.
- [ ] Update settings manager defaults if needed.