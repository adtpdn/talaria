---
title: "Gauntlet: Sticky Cell System"
id: "068"
status: todo
priority: 01
sprint: alpha
category: CORE
description: "Implement the 'sticky candy' logic that blocks movement, traps players, and changes the arena layout."
---

# Gauntlet: Sticky Cell System

## Problem
The Candy Cannon must leave a permanent mark to create escalating pressure. If impacts were temporary, the arena would never reach the intended 80% sticky state by the end of the round, failing to force route adaptation.

## Solution
Use GridMap Layer 2 as a dynamic "Sticky Overlay" to manage cell states without destroying the base floor.

### Technical Implementation
1. **State Mapping:** Maintain a server-side `sticky_cells: Dictionary` (`Vector2i` $\rightarrow$ `true`).
2. **Visuals:** Assign `TILE_STICKY = 17` (Pink mesh) to Layer 2. Sync via `main.rpc("sync_grid_item", x, 2, z, TILE_STICKY)`.
3. **Movement Block:** Modify `PlayerMovementManager.simple_move_to()` to block movement if the destination is sticky (unless `Cleanser` is active).
4. **Trap Logic:**
    - **Step-on:** Player is trapped if their current cell becomes sticky.
    - **Push:** In `try_push()`, stop the player and trap them at the first sticky cell encountered.
5. **Trapped State:** Disable movement and scoring until a `Cleanser` is used.

## Benefits
- **Dynamic Layout:** Evolves the arena into a maze, forcing strategic movement.
- **Emergent PvP:** Enables players to "herd" opponents into sticky zones using Smack.
- **Efficiency:** Layer 2 overlays are more performant than spawning hundreds of static bodies.

## Acceptance Criteria
- **Collision Check:** Confirm players cannot enter sticky cells.
- **Trap Verification:** Verify trapping occurs via direct cannon hit or `try_push()`.
- **Network Sync:** Confirm pink overlay appears on all clients upon host impact.
- **Bypass Check:** Verify that `Cleanser` allows movement through sticky cells.

## Migration Checklist
- [ ] Define `TILE_STICKY = 17` in MeshLibrary.
- [ ] Implement `sticky_cells` tracking in `GauntletManager`.
- [ ] Update `PlayerMovementManager.simple_move_to()` with sticky check.
- [ ] Update `PlayerMovementManager.try_push()` with trap logic.
- [ ] Implement `trap_player(player_id)` and `sync_grid_item` RPC.
