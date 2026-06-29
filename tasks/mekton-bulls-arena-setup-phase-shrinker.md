---
title: "Mekton Bulls: Arena Setup & Phase Shrinker"
id: "135"
status: "todo"
blocked_by: ["134"]
priority: 01
sprint: alpha
category: CORE
description: "Set up the Mekton Bulls arena as a 20×20 starting grid with a phase shrinker that walks it through 20 → 19 → 18 → 17 each phase."
modified: "2026-06-29"
---

# Mekton Bulls: Arena Setup & Phase Shrinker

## Problem
Mekton Bulls plays on an arena that **shrinks every phase**:

| Phase | Board     |
| ----- | --------- |
| 1     | 20 × 20   |
| 2     | 19 × 19   |
| 3     | 18 × 18   |
| 4     | 17 × 17   |
| 5     | END       |

Unlike Sugar Rush (fixed 18 × 18) or legacy Gauntlet (fixed 20 × 20),
Mekton Bulls needs a runtime-shrinking grid plus NPC re-positioning.

## Solution
Implement an arena phase manager on `MektonBullsManager`.

### Concrete Changes
1. Add arena state to `MektonBullsManager`:
    - `current_phase: int = 1`
    - `arena_size_for_phase(p: int) -> Vector2i` (lookup: 1=20, 2=19, 3=18, 4=17).
    - `arena_cells: Dictionary[Vector2i, CellState]`.
2. Implement `_setup_arena()`:
    - Initialize `arena_size = (20, 20)`, build boundary walls, place
      spawn points analogous to `gauntlet_manager.get_spawn_points()`.
    - NPC Mekton (the bull — see #136) sits at the centre.
3. Implement `_shrink_arena()`:
    - Recompute `arena_size = arena_size_for_phase(current_phase + 1)`.
    - Mark the newly outer ring as `TILE_WATER` (used by #137 water-flood).
    - Spawn the visual shrinking effect (camera dolly-in optional).
    - Reposition Mekton (bull) inside the new boundary.
4. Wire `_shrink_arena()` to `#145` phase timer.
5. Boundary checks (`_is_boundary(pos)`) must read the **current**
   `arena_size`, not a constant — unlike Sugar Rush where the board
   is fixed.

## Acceptance Criteria
- Arena visibly starts at 20 × 20.
- Each phase shrinks by one ring around the edge.
- Water ring is impassable instantly.
- Player outside the new boundary is eliminated (delegated to #137).
- Final phase (17 × 17) eliminates any remaining on the outer ring.

## Migration Checklist
- [ ] Add `current_phase` state.
- [ ] Add `arena_size_for_phase()` lookup.
- [ ] Implement `_setup_arena()` (reuse gauntlet boundary logic with
      current-size reads).
- [ ] Implement `_shrink_arena()`.
- [ ] Mark water tiles via new `TILE_WATER` constant.
- [ ] Reposition bull on each shrink.
- [ ] Verify boundary reads use `arena_size.x` / `arena_size.y`.