---
title: "Gauntlet: Sticky Cell System (v2)"
id: "068"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Implement the 'sticky candy' logic that blocks movement, traps players, and changes the arena layout. Updated for ground growth model."
modified: "2026-06-18"
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
- [ ] Keep `TILE_STICKY = 17` and `TILE_TELEGRAPH = 18` definitions
- [ ] Keep `sticky_cells` tracking dictionary
- [ ] Keep `is_sticky_cell()`, `clear_sticky_cell()`, `_trap_player()` functions
- [ ] Update `_check_all_players_trapped()` to run after each growth tick (not cannon volley)
- [ ] Add `CLEANSED = 6` cell state to grid
- [ ] Add path safety validation before applying growth tick selections
- [ ] Update coverage target from 80% to 70–75%
- [ ] Update all "Candy Cannon" references to "Candy Pump" in comments
