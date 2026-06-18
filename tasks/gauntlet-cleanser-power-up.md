---
title: "Gauntlet: Cleanser Power-Up"
id: "072"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Implement the Cleanser power-up that allows players to move through and clear sticky candy."
assignee: "default"
cron_job: "pending"
modified: "2026-06-18"
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
- [ ] Add `player_cleansers` dictionary to `GauntletManager`.
- [ ] Connect `GoalsCycleManager.goal_count_updated` signal to cleanser grants.
- [ ] Implement movement bypass in `PlayerMovementManager.simple_move_to()`.
- [ ] Implement `clear_sticky_cell` via `main.rpc("sync_grid_item", x, 2, z, -1)`.
- [ ] Add a HUD indicator for cleanser count.
