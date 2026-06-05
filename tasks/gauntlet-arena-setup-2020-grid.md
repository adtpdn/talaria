---
title: "Gauntlet: Arena Setup (20x20 Grid)"
id: "066"
status: todo
priority: 01
sprint: alpha
category: CORE
description: "Implement the 20x20 cell grid layout for the Gauntlet arena, including the central NPC forbidden zone."
assignee: "default"
cron_job: "pending"
---

# Gauntlet: Arena Setup (20x20 Grid)

## Problem
Gauntlet requires a larger, square-grid layout than Stop N Go to allow for movement-based survival and strategic route-blocking. Existing arena setups are too narrow, making the Candy Cannon's area-of-effect attacks either too oppressive or trivial.

## Solution
Implement a custom `_setup_arena()` method within `GauntletManager` using the `EnhancedGridMap` API.

### Implementation Details
1. **Grid Generation:** Initialize a 20×20 walkable floor using `TILE_WALKABLE` (ID 0) with strictly enforced bounds.
2. **NPC Forbidden Zone:** Designate a 3×3 area at center `(9, 9)` as the Candy Cannon footprint using `TILE_OBSTACLE` (ID 4).
3. **Player Spawn Mapping:**
    - 4 players: Outer corners.
    - 6-8 players: Mid-edges and corner-adjacent cells.
4. **Boundary Walls:** Surround the 20x20 perimeter with `TILE_OBSTACLE` to ensure a closed-loop environment.

## Benefits
- **Spatial Balance:** 400 cells provide the right scale for 8 players and 80% sticky coverage.
- **Visual Clarity:** Symmetric layout makes the center-point threat intuitive.
- **Standardization:** Reuses the `StopNGoManager` setup pattern for reliability.

## Acceptance Criteria
- **Layout Verification:** Verify the grid is exactly 20x20 walkable cells.
- **Collision Check:** Confirm the 3x3 center is blocked and players cannot leave the 20x20 boundary.
- **Spawn Logic:** Verify players spawn in corners (4p) or edges (8p) without overlapping.

## Migration Checklist
- [ ] Implement `GauntletManager._setup_arena()` following the `StopNGoManager` pattern.
- [ ] Define `ARENA_SIZE = 20` and `NPC_SIZE = 3` constants.
- [ ] Set the 3x3 center block to `TILE_OBSTACLE` in the `EnhancedGridMap`.
- [ ] Implement spawn position logic for 4, 6, and 8 players.
- [ ] Verify `main.gd` calls `gauntlet_manager._setup_arena()` during host setup.
