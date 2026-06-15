---
title: "Gauntlet: Arena Setup (24×24 Grid with Layers)"
id: "066"
status: "done"
priority: 01
sprint: alpha
category: CORE
description: "Implement the 24×24 cell grid layout for the Gauntlet arena, including the central NPC forbidden zone and layer-based pressure logic."
modified: "2026-06-15"
---

# Gauntlet: Arena Setup (24×24 Grid with Layers)

## Problem
Gauntlet v2 requires a larger 24×24 square-grid layout to accommodate the ground growth system, movement buffers, candy bubbles, and 4–8 player movement. The old 20×20 arena is too small for the inward-spreading pressure model.

## Solution
Custom `_setup_arena()` in `GauntletManager` using `EnhancedGridMap`:

### Arena Layout (v2)
1. **24×24 walkable floor** (`TILE_WALKABLE` ID 0) with enforced bounds
2. **3×3 NPC forbidden zone** at center `(11, 11)` using `TILE_OBSTACLE` (ID 4)
3. **Boundary walls** using `TILE_OBSTACLE` around the 24×24 perimeter
4. **Player spawn mapping:**
   - 4 players → outer corners `(2,2)`, `(21,2)`, `(2,21)`, `(21,21)`
   - 6–8 players → side-edge and corner-adjacent spawns

### Layer System (NEW in v2)
The arena is divided into three pressure layers based on edge distance:

```
edgeDistance = min(x, y, width - 1 - x, height - 1 - y)
```

| Layer | edgeDistance | Approximate Size | Purpose |
|---|---|---|---|
| Outer | 0–3 | 320 cells | First to become unsafe, teaches inward pressure |
| Middle | 4–7 | 192 cells | Main route-pressure area |
| Inner | 8+ | 64 cells (55 playable) | Final survival area |

Layer calculation is precomputed in `_build_arena_layers()` and stored in `arena_layers: Dictionary` (Vector2i → String).

### Constants
```
ARENA_SIZE = 24
NPC_SIZE = 3
NPC_CENTER = Vector2i(11, 11)  # Center of 24×24
TOTAL_PLAYABLE = 567  # 576 - 9 NPC cells
```

## Acceptance Criteria
- Grid is exactly 24×24 walkable cells
- 3×3 center blocked, players can't leave boundary
- Players spawn in corners (4p) or edges (8p) without overlapping
- Layer distances are correctly precomputed for all 567 playable cells

## Migration Checklist
- [ ] Change `ARENA_COLUMNS`/`ARENA_ROWS` from 20 to 24
- [ ] Change `NPC_CENTER` from `(9,9)` to `(11,11)`
- [ ] Implement `_build_arena_layers()` to precompute edge distances
- [ ] Update `get_spawn_points()` for 24×24 dimensions
- [ ] Update `_is_npc_zone()` for new center
- [ ] Update `_respawn_mission_tiles()` bounds
- [ ] Verify `main.gd` calls `gauntlet_manager._setup_arena()` during host setup
