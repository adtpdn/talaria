---
title: "Gauntlet: Telegraph Floor Highlight Before Growth"
id: "081"
status: "done"
blocked_by: ["069"]
priority: 02
sprint: alpha
category: FEATURE
description: "Add temporary floor highlight before growth tick cells become sticky, improving readability of incoming danger."
modified: "2026-06-26"
---

# Gauntlet: Telegraph Floor Highlight Before Growth

## Problem
In v2, cells are telegraphed 1 second before becoming sticky (replacing the old cannon projectile warning). Without a floor highlight, players can't tell which cells are about to become sticky.

## Solution
Add a temporary highlighter on the floor during the 1-second telegraph window:

### Technical Details
1. When a growth tick selects cells, place `TILE_TELEGRAPH = 18` on Layer 2.
2. Highlight appears for exactly **1 second** (the telegraph duration).
3. Sync highlight across all clients via RPC.
4. After 1 second, transition to `TILE_STICKY = 17`.

### Visual Design
- **Build-up (0–0.8s):** Tile fades in with amber/syrup glow. Rising pitch sound.
- **Flash (0.8–1.0s):** Flicker brightness. Final "pop" sound.
- **Transition:** Replace telegraph with sticky. Trigger `screen_shake_manager` ("light").

### What Changed from v1
- Old: Telegraph warned of cannon projectile landing zones
- New: Telegraph warns of growth tick cells becoming sticky
- Timing: Still 1 second, but now fires every 3s (growth interval) instead of every 8–15s (cannon)
- Volume: 4–10 cells telegraphed simultaneously (vs. 1–4 cells from cannon)

## Acceptance Criteria
- Telegraph appears 1 second before cells become sticky
- All clients see telegraphs simultaneously
- Telegraph is clearly distinct from sticky cells
- Smooth transition from highlight to sticky
- Works for 4–10 cells simultaneously (growth tick burst)

## Migration Checklist
- [x] Keep `TILE_TELEGRAPH = 18` definition
- [x] Update telegraph to fire every 3s (growth interval) instead of cannon timing
- [x] Update RPC: `sync_telegraph` should accept array of 4–10 cells (`sync_growth_telegraph(cells)`)
- [x] Update VFX sequence for multi-cell telegraph (not single projectile)
- [x] Sequence: highlight (0.5–1.0s) → telegraph build-up → sticky

## Implementation Notes (2026-06-25)
Fully covered by the #067 growth loop + the #069 two-stage VFX — this task is the
floor-highlight slice of the same pipeline:
- `_spawn_telegraph_highlight()` draws a per-cell amber floor quad under each
  telegraphed cell, fading in over the 0.8s build-up then flashing brighter in the
  final 0.2s before sticky lands. Auto-removed at the end of the 1s window.
- Driven by `sync_growth_telegraph(cells)` (batch, 4–10 cells, all clients), every
  growth interval (3s). `TILE_TELEGRAPH = 18` on Layer 2 is the passable warning;
  `sync_growth_apply` swaps it to `TILE_STICKY = 17` with a light shake.
- Amber highlight is deliberately distinct from the pink sticky overlay.

See [[gauntlet-telegraph-vfx-system]] (#069). Live-only: 60 FPS with 10 highlights.
