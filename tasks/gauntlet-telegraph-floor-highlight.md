---
title: "Gauntlet: Telegraph Floor Highlight Before Growth"
id: "081"
status: "in_progress"
priority: 02
sprint: alpha
category: FEATURE
description: "Add temporary floor highlight before growth tick cells become sticky, improving readability of incoming danger."
modified: "2026-06-10"
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
- [ ] Keep `TILE_TELEGRAPH = 18` definition
- [ ] Update telegraph to fire every 3s (growth interval) instead of cannon timing
- [ ] Update RPC: `sync_telegraph` should accept array of 4–10 cells
- [ ] Update VFX sequence for multi-cell telegraph (not single projectile)
- [ ] Sequence: highlight (0.5–1.0s) → telegraph build-up → sticky
