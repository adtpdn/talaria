---
title: "Sugar Rush: Arena Setup 18×18 Grid"
id: "112"
status: "halt"
halt_reason: "need confirmation"
priority: 01
sprint: alpha
category: CORE
description: "Shrink the shipped 20×20 Gauntlet arena to 18×18 for Sugar Rush and recompute NPC center + boundary checks."
modified: "2026-06-29"
supersedes: ["066"]
---

# Sugar Rush: Arena Setup 18×18 Grid

## Problem
`scripts/managers/gauntlet_manager.gd` defines `ARENA_COLUMNS = 20` and
`ARENA_ROWS = 20`. Sugar Rush plays on an **18 × 18** grid.

## Solution
Replace the constants and any hard-coded `20` references with `18`. Recompute
the NPC center for the smaller grid and re-derive spawn points.

### Changes
1. `gauntlet_manager.gd`
    - `const ARENA_COLUMNS: int = 18`
    - `const ARENA_ROWS: int = 18`
    - `const NPC_CENTER: Vector2i = Vector2i(8, 8)` (center of 18², 0-indexed).
2. `_setup_arena()` — boundary loop uses `range(ARENA_COLUMNS)` /
   `range(ARENA_ROWS)` (already driven by constants, but verify).
3. `_is_boundary(pos)` — uses constants; verify with new center.
4. `get_spawn_points(player_count)` — recompute spawn offsets relative to
   the new 18² grid (corners + edges).
5. `_is_npc_zone(pos)` — uses `NPC_CENTER`; verify with new value.

## Acceptance Criteria
- Arena renders as 18 × 18.
- NPC Mekton sits at (8, 8) ± half a 3×3 block.
- Boundary walls still wrap the playable area.
- Spawn points distribute evenly for 1–8 players.
- No leftover `range(20)` literals.

## Migration Checklist
- [ ] Update `ARENA_COLUMNS` / `ARENA_ROWS`.
- [ ] Update `NPC_CENTER`.
- [ ] Recompute `get_spawn_points()` for 18².
- [ ] Grep for `range(20)` / `range(0, 20)` and replace.
- [ ] Smoke-test arena boundary walls and Mekton spawn.