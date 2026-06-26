---
title: "Gauntlet: Cleanser Power-Up"
id: "072"
status: "done"
blocked_by: ["068", "074"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the Cleanser power-up that allows players to move through and clear sticky candy."
assignee: "default"
cron_job: "pending"
modified: "2026-06-25"
---

# Gauntlet: Cleanser Power-Up

## Problem
As the arena reaches 70–75% sticky, players will inevitably get trapped or boxed in. Without recovery, a single mistake or a well-placed Smack would end a run prematurely.

## Solution
Implement a limited-use power-up providing temporary immunity and the ability to clear sticky cells.

### Technical Details
1. **Unlock Logic:** Every 2 completed missions, grant 1 Cleanser. Inventory limit: 1.
2. **Activation:** Trigger via power-up key (0.3s delay).
3. **Effect:**
    - **Immunity:** For **5 cells** of movement, ignore sticky blocking.
    - **Cleansing:** Every sticky cell crossed is set to `TILE_WALKABLE` (ID 0).
4. **Termination:** Ends after 5 cells or when stopping on a safe cell.
5. **Restriction:** Activation is blocked while stunned.

## Benefits
- **Comeback Potential:** Allows trapped players to return and continue scoring.
- **Arena Modification:** Enables players to strategically carve safe paths.
- **Reward Loop:** Ties recovery to mission completion, rewarding brave play.

## Acceptance Criteria
- **Unlock Check:** Verify 1 Cleanser is granted every 2 missions (max 1).
- **Traversal Check:** Verify player can move through sticky cells when active.
- **Cleansing Check:** Confirm sticky cells become walkable after traversal.
- **Limit Check:** Verify immunity ends exactly after the 5th cell.
- **State Check:** Verify activation is blocked during stuns.

## Migration Checklist
- [x] Add `player_cleansers` dictionary to `GauntletManager`.
- [x] Connect `GoalsCycleManager.goal_count_updated` signal to cleanser grants.
- [x] Implement movement bypass in `PlayerMovementManager.simple_move_to()`.
- [x] Implement `clear_sticky_cell` via `main.rpc("sync_grid_item", x, 2, z, -1)`.
- [x] Add a HUD indicator for cleanser count.

## Implementation Notes (2026-06-25)
Most of the Cleanser system was already in place; this task verified the
acceptance criteria and added the missing **safe-stop early termination**.
- **Grant:** `_on_goal_count_updated` (connected to `goal_count_updated`) tracks
  `player_mission_completions` and grants 1 Cleanser every 2 missions, inventory
  capped at 1. Server-authoritative; HUD synced via `sync_cleanser_count`.
- **Activate:** `_try_use_cleanser()` — 0.3s delay, blocked while
  `is_frozen`/`is_stop_frozen`, grants `CLEANSER_MAX_CELLS = 5` immunity cells.
- **Traverse + cleanse:** `PlayerMovementManager.simple_move_to` (and the push
  path) — while active, stepping onto sticky calls `clear_sticky_cell` (erases
  sticky, clears the Layer-2 overlay to reveal walkable Layer-0 floor, marks the
  cell cleansed for regrowth protection) + `use_cleanser_cell` (decrements; ends
  at 0). Both gated on `gm.is_active` so **only Gauntlet mode is affected**.
- **Terminate (new):** `notify_movement_stopped(pid, pos)` — called from
  `_on_movement_finished` (gauntlet-gated) ends the Cleanser early when the player
  comes to rest on a non-sticky cell, per the spec's "ends when stopping on a safe
  cell". No-op without an active cleanser.
- Decoupled from slow-mo (see [[gauntlet-slowmo-effect]] #078); Cleanser no longer
  triggers the global time-scale effect.

Tests: `tests/test_gauntlet_cleanser.gd` — 10/10 passing (grant cadence, 5-cell
lifecycle, sticky clearing, safe-stop termination, stun-block via inactive guard).
Full gauntlet suite: 156/156. Only the shared `player_movement_manager.gd` was
touched, and every Gauntlet branch is `gm.is_active`-gated — default modes
(Freemode / Stop-n-Go / Doors) are unaffected.
