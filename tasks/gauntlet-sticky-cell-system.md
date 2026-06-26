---
title: "Gauntlet: Sticky Cell System (v2)"
id: "068"
status: "done"
blocked_by: ["066"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the 'sticky candy' logic that blocks movement, traps players, and changes the arena layout. Updated for ground growth model."
modified: "2026-06-25"
---

# Gauntlet: Sticky Cell System (v2)

## Problem
The Candy Pump ground growth system must leave permanent sticky marks to create escalating pressure. In v2, sticky cells grow from existing clusters rather than being hit by projectiles.

## Solution
GridMap Layer 2 as dynamic "Sticky Overlay" (same approach, different trigger):

### Cell States
| State | Description |
|---|---|
| SAFE | Can be entered, crossed, collected |
| TELEGRAPHED | Warned as future sticky, still passable (1s) |
| STICKY | Covered in sticky candy, cannot pass, traps players |
| BUBBLE_GROWING | Candy bubble growing, not yet exploded |
| BLOCKED | NPC or permanent obstacle |
| CLEANSED | Recently cleaned by Cleanser (may have temp protection) |

### State Mapping
- Server-side `sticky_cells: Dictionary` (`Vector2i` → `true`)
- Visual: `TILE_STICKY = 17` (deep magenta) on Layer 2
- Telegraph: `TILE_TELEGRAPH = 18` (amber/syrup glow) on Layer 2
- Sync via `main.rpc("sync_grid_item", x, 2, z, TILE_STICKY)`

### Sticky Rules
- Cannot be passed through
- Cannot be collected from
- Traps players who step onto it
- Traps players pushed into it (via Smack)
- Remains sticky until Cleansed or round ends

### Coverage Target
- **70%–75%** of playable cells (397–425 cells)
- Old v1 target was 80% — reduced because growth is more organic

### Path Safety Rule
Before applying selected sticky cells, check that each active player still has:
- At least one reachable safe region within 6–8 cells
- Exception: Final 30 seconds allows forced traps

## Acceptance Criteria
- Players cannot enter sticky cells (unless Cleanser active)
- Trapping occurs via ground growth or Smack push
- Pink overlay appears on all clients upon growth tick impact
- Cleanser allows movement through sticky cells
- Coverage reaches 70–75% by end of round

## Migration Checklist
- [x] Keep `TILE_STICKY = 17` and `TILE_TELEGRAPH = 18` definitions
- [x] Keep `sticky_cells` tracking dictionary
- [x] Keep `is_sticky_cell()`, `clear_sticky_cell()`, `_trap_player()` functions
- [x] Update `_check_all_players_trapped()` to run after each growth tick (not cannon volley) — runs in `sync_growth_apply`; now SLOWS players on fresh sticky instead of trapping
- [x] Add `CLEANSED = 6` cell state to grid (CellState enum, value 5; 0-indexed)
- [x] Add path safety validation before applying growth tick selections (`_apply_path_safety`, BFS reachability)
- [x] Update coverage target from 80% to 70–75% (`COVERAGE_TARGET_MIN/MAX`, `coverage_ratio`, `is_coverage_reached`)
- [x] Update all "Candy Cannon" references to "Candy Pump" in comments

## Implementation Notes (2026-06-24)
Added to `scripts/managers/gauntlet_manager.gd`:
- `enum CellState { SAFE, TELEGRAPHED, STICKY, BUBBLE_GROWING, BLOCKED, CLEANSED }`
- `cleansed_cells` dict + `CLEANSED_PROTECTION_TIME` (5s), decayed each server tick via `_tick_cleansed_cells()`
- `cell_state(pos)`, `is_cleansed_cell()`, `mark_cleansed()`, `_is_boundary()`
- Coverage: `playable_cell_count()` (315 on 20×20), `coverage_ratio()`, `is_coverage_reached()`
- Path safety: `_is_cell_passable()`, `_reachable_safe_cells()` (BFS), `_player_has_safe_region()`, `_apply_path_safety()` (final-30s forced-trap window)
- `clear_sticky_cell()` now marks the cell CLEANSED for temporary regrowth protection

Tests: `tests/test_gauntlet_sticky_system.gd` — 31/31 passing (headless GUT). The `_apply_path_safety` wiring into the live growth loop lands with #067.

## Sticky Entry Behavior Change (2026-06-25)
Sticky entry now **slows** the player instead of hard-trapping them (decision:
"always slow only", no final-30s freeze). This decouples the slow-feel from the
global `Engine.time_scale` slow-mo, which was unfair in multiplayer (one player's
Cleanser slowed everyone). See [[gauntlet-slowmo-effect]] (#078).
- `apply_sticky_slow(player)` → per-player `player.apply_slow_effect(STICKY_SLOW_DURATION=2.0)`
  (20% move speed via `movement_manager.set_speed_multiplier(0.2)`).
- `player_movement_manager.gd`: stepping into / being pushed into sticky calls
  `apply_sticky_slow` (not `_trap_player`); the `trapped_players` movement-block
  was removed so slowed players can still struggle free.
- Cleanser still **removes** the sticky cell on contact (`clear_sticky_cell`) and
  is immune to the slow. `_trap_player` / `trapped_players` kept as legacy, unused
  for sticky.
