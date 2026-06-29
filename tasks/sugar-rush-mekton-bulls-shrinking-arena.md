---
title: "Sugar Rush: Mekton Bulls — Shrinking Arena + Water Flood"
id: "133"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: CORE
description: "Implement Mekton Bulls shrinking arena (20 → 19 → 18 → 17) and outer-ring water elimination when a bull stands on the boundary."
modified: "2026-06-29"
---

# Sugar Rush: Mekton Bulls — Shrinking Arena + Water Flood

## Problem
Mekton Bulls plays on a shrinking arena: phase 1 = 20×20, phase 2 = 19×19,
phase 3 = 18×18, phase 4 = 17×17. A bull standing on the boundary floods the
outermost ring with water — instant elimination. There is no current
shrinking-arena code.

## Solution
Add phase-driven board shrinks and a water-flood mechanic.

### Changes
1. Add `_arena_phase: int = 1` state.
2. Add `_arena_size_for_phase(phase: int) -> Vector2i`:
    - 1 → 20, 2 → 19, 3 → 18, 4 → 17.
3. Add `_shrink_arena()`:
    - Recompute `ARENA_COLUMNS` / `ARENA_ROWS` for the new phase.
    - Mark the newly outer cells as `TILE_WATER` (a new tile type).
    - Respawn Mekton (bull) inside the new boundary.
4. Add `_spawn_bull_mekton()` — roam the arena, knock players on contact.
5. Add `_check_water_flood()`:
    - If a bull is on a boundary cell → eliminate any player on the new
      outer ring.
6. Phase advance: every 30 s (TBD) or on player count.

## Acceptance Criteria
- Arena visibly shrinks every phase.
- Water ring is impassable (instant elimination).
- Bull mekton roams and knocks players.
- Players can be eliminated by water.
- Phase timer is host-configurable.

## Migration Checklist
- [ ] Add `TILE_WATER` tile type.
- [ ] Add `_shrink_arena`.
- [ ] Add `_spawn_bull_mekton`.
- [ ] Add `_check_water_flood`.
- [ ] Hook phase advance timer.
- [ ] Wire to Mekton Bulls flag (#132).