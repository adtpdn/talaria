---
title: "Gauntlet: Arena Setup (20×20 Grid with Layers)"
id: "066"
status: "done"
blocked_by: []
priority: 01
sprint: alpha
category: CORE
description: "Implement the 20×20 cell grid layout for the Gauntlet arena, including the central NPC forbidden zone and layer-based pressure logic."
modified: "2026-06-25"
---

# Gauntlet: Arena Setup (20×20 Grid with Layers)

## Problem
Gauntlet v2 requires a square-grid layout to accommodate the ground growth system, movement buffers, candy bubbles, and 4–8 player movement. The arena uses a 20×20 grid — large enough for the inward-spreading pressure model while keeping the whole board on one camera view.

## Solution
Custom `_setup_arena()` in `GauntletManager` using `EnhancedGridMap`:

### Arena Layout (v2)
1. **20×20 walkable floor** (`TILE_WALKABLE` ID 0) with enforced bounds
2. **3×3 NPC forbidden zone** at center `(9, 9)` using `TILE_OBSTACLE` (ID 4)
3. **Boundary walls** using `TILE_OBSTACLE` around the 20×20 perimeter
4. **Player spawn mapping:**
   - 4 players → inner corners `(1,1)`, `(18,1)`, `(1,18)`, `(18,18)`
   - 6 players → corners + top/bottom mid-edges `(10,1)`, `(10,18)`
   - 8 players → corners + all four mid-edges (adds `(1,10)`, `(18,10)`)

### Layer System (v2)
The arena is divided into three pressure layers based on edge distance:

```
edgeDistance = min(x, y, width - 1 - x, height - 1 - y)
```

| Layer | edgeDistance | Purpose |
|---|---|---|
| Outer | 0–3 | First to become unsafe, teaches inward pressure |
| Middle | 4–6 | Main route-pressure area |
| Inner | 7+ | Final survival area |

Layer classification is computed in `_layer_of()` (Chebyshev distance from center) and used by the candidate scoring system (#073).

### Constants
```
ARENA_COLUMNS = 20
ARENA_ROWS = 20
NPC_SIZE = 3
NPC_CENTER = Vector2i(9, 9)  # Center of 20×20 (0-indexed)
playable_cell_count() = 315  # interior minus NPC zone
```

## Acceptance Criteria
- Grid is exactly 20×20 walkable cells
- 3×3 center blocked, players can't leave boundary
- Players spawn in corners (4p) or edges (8p) without overlapping
- Layer distances are correctly computed for scoring

## Migration Checklist
- [x] `ARENA_COLUMNS`/`ARENA_ROWS` set to 20
- [x] `NPC_CENTER` set to `(9,9)`
- [x] Layer classification implemented (`_layer_of()` — outer≥7 / middle≥4 / inner Chebyshev from center)
- [x] `get_spawn_points()` for 20×20 dimensions (4p corners, 6p +mid-edges, 8p +all edges)
- [x] `_is_npc_zone()` for center `(9,9)`

- [x] `main.gd` calls `gauntlet_manager._setup_arena()` during host setup

## Implementation Notes (2026-06-25)
Spec corrected from an aspirational 24×24 to the shipped **20×20** layout
(decision: keep code as-is, fix the doc). The 20×20 size is what the camera
framing (`camera_context_manager.gd` gauntlet bounds), all gauntlet tests
(116/116), the layer thresholds, and spawn points are built around. NPC zone is
the center 3×3 at `(9,9)`; `playable_cell_count()` returns 315.
