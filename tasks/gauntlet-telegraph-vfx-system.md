---
title: "Gauntlet: Telegraph VFX System (v2)"
id: "069"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Implement the 1-second visual and auditory warning system before growth tick cells become sticky."
modified: "2026-06-18"
---

# Gauntlet: Telegraph VFX System (v2)

## Problem
Without a telegraph, growth ticks feel random and unfair. Players need a readable signal to react (move or cleanse), which is the core "dodge or die" loop of the game mode.

## Solution
Multi-stage warning sequence synced across all clients — now fires every 3s for growth ticks instead of on cannon volleys.

### Sequence Design
1. **Telegraph Sync:** Server sends `rpc("sync_telegraph", cells_array)` — array of 4–10 cells (growth tick batch).
2. **VFX Sequence (1.0s):**
    - **Build-up (0–0.8s):** Place `TILE_TELEGRAPH = 18` (amber/syrup glow) on Layer 2. Tween alpha 0→1. Play rising pitch sound.
    - **Flash (0.8–1.0s):** Flicker brightness/color to bright amber. Play final "pop" sound.
3. **Transition:** Replace `TILE_TELEGRAPH` with `TILE_STICKY` (ID 17) and trigger `screen_shake_manager` ("light").
4. **Polish:** Add "syrup splash" particles at each affected cell.

### What Changed from v1
- Old: Telegraph on cannon projectile landing (1–4 cells every 8–15s)
- New: Telegraph on growth tick cells (4–10 cells every 3s)
- Old: Single target zone telegraph
- New: Multiple scattered cells telegraphed simultaneously
- Audio: Lighter impact sound (growth is gentler than cannon)

### Performance Consideration
With 4–10 cells telegraphing simultaneously, optimize:
- Batch RPC calls (single RPC per tick, not per cell)
- Use instanced particle effects
- Limit simultaneous telegraph count

## Benefits
- **Fairness:** Shifts failure from "bad luck" to "slow reaction".
- **Anticipation:** Rising audio/visuals create psychological pressure.
- **Readability:** Clear color-coding (Amber → Sticky) defines safe zones.

## Acceptance Criteria
- Telegraph lasts exactly 1.0s from glow to impact
- All 4–10 cells appear simultaneously (not staggered)
- `TILE_TELEGRAPH` is clearly different from `TILE_STICKY`
- Audio syncs with alpha fade-in
- All clients see telegraphs simultaneously
- Performance stays above 60 FPS with 10 simultaneous telegraphs

## Migration Checklist
- [ ] Keep `TILE_TELEGRAPH = 18` definition
- [ ] Update `sync_telegraph` RPC to accept array of Vector2i (4–10 cells)
- [ ] Update VFX logic for batch telegraph (not single cell)
- [ ] Batch particle effects and audio for simultaneous cells
- [ ] Remove old cannon-specific telegraph logic
- [ ] Add light screen shake on growth tick impact (not medium like cannon)
