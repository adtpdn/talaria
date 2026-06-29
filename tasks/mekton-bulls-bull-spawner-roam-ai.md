---
title: "Mekton Bulls: Big Mekton Bull Spawner + Roam AI"
id: "136"
status: "todo"
blocked_by: ["134", "135"]
priority: 01
sprint: alpha
category: AI
description: "Spawn a large Mekton 'bull' that roams the arena, charges in straight lines, and knocks any player it touches out of the match."
modified: "2026-06-29"
---

# Mekton Bulls: Big Mekton Bull Spawner + Roam AI

## Problem
Mekton Bulls has the static Mekton `Tekton` (delivery target) **and** a
mobile bull — a separate, larger NPC that walks the arena and knocks
players out on contact. Existing `Tekton` nodes (`tekton.tscn`,
`static_tekton.tscn`) are anchored, not roamers. We need a new entity
type for the bull.

## Solution
Add a `MektonBull` scene + behaviour script with a roam AI.

### Concrete Changes
1. **New scene — `scenes/mekton_bull.tscn`**
    - Extends `CharacterBody3D` (or `Node3D` + driver script).
    - Carries a bull mesh (use scaled `static_tekton.tscn` mesh as placeholder).
    - Has a `CollisionShape3D` sized for the bull.
    - Tagged `TILE_BULL` semantically (collision only, not a tile).
2. **Behaviour script — `scripts/npcs/mekton_bull.gd`**
    - `state`: `{ ROAM, CHARGE, COOLDOWN }`.
    - `_roam()`: random walk to a reachable cell inside current arena.
    - `_charge(target_pos)`: straight line toward a player it picked.
    - `_cooldown()`: 1.5 s pause after a charge that hits or misses.
    - `on_body_entered(player)`: knock the player out (eliminate them,
      or set them to `"out"` — see #140 for placement scoring).
3. **Spawner — `MektonBullsManager._spawn_bull()`**
    - Spawn at the centre on `start_game_mode()`.
    - Re-position inside the new boundary on each `#135` shrink.
4. **Roam AI constraints**
    - Must avoid stepping on `TILE_WATER` (boundary of the shrunk arena).
    - Must not occupy the same cell as the static Mekton (delivery target).

## Acceptance Criteria
- One bull spawned on match start.
- Bull roams the arena in a believable path.
- Bull charges a player on line-of-sight.
- Bull touches player → player gets eliminated.
- Bull re-spawns at the centre after `#135` shrink.
- Bull never enters the water ring.

## Migration Checklist
- [ ] Create `scenes/mekton_bull.tscn`.
- [ ] Create `scripts/npcs/mekton_bull.gd` with state machine.
- [ ] Hook `on_body_entered` for player knock.
- [ ] Wire `MektonBullsManager._spawn_bull()`.
- [ ] Reposition on shrink (#135).
- [ ] Constrain roam path to inside `arena_size`.