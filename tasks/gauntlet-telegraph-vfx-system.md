---
title: "Gauntlet: Telegraph VFX System (v2)"
id: "069"
status: "done"
blocked_by: ["067"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the 1-second visual and auditory warning system before growth tick cells become sticky."
modified: "2026-06-25"
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
- [x] Keep `TILE_TELEGRAPH = 18` definition
- [x] Update `sync_telegraph` RPC to accept array of Vector2i (4–10 cells) — `sync_growth_telegraph(cells)` batch RPC from #067
- [x] Update VFX logic for batch telegraph (not single cell)
- [x] Batch particle effects and audio for simultaneous cells (single RPC per tick)
- [x] Remove old cannon-specific telegraph logic (removed in #067; no `sync_telegraph`/`sync_impact` left)
- [x] Add light screen shake on growth tick impact (not medium like cannon) — `shake(0.15, 0.4)` in `sync_growth_apply`

## Implementation Notes (2026-06-25)
Most of the telegraph pipeline shipped with the #067 growth loop; this task added
the **two-stage VFX** the spec calls for:
- `_spawn_telegraph_highlight()` now runs an **amber** build-up (0–0.8s, alpha
  ramps 0→0.55) then a **flash** (0.8–1.0s, emission energy 1.5→4.0 + alpha→0.9)
  right before impact, instead of the old single pink pulse. Amber `(1.0, 0.65,
  0.1)` is deliberately distinct from the pink/magenta sticky overlay (`TILE_STICKY
  = 17`) so the two never read alike.
- Flow per growth tick (server → all clients via `sync_growth_telegraph`):
  `TILE_TELEGRAPH = 18` placed on Layer 2 (still passable) + amber highlight +
  warning audio (`generate_tile`) → after `telegraph_duration` (1.0s) →
  `sync_growth_apply` swaps to `TILE_STICKY`, light screen shake, splash particles,
  `tile_scatter` audio.
- 4–10 cells telegraph simultaneously (the growth-tick batch), single RPC each,
  no per-cell staggering.

Live-only check (not headless-testable): 60 FPS with 10 simultaneous telegraphs.
