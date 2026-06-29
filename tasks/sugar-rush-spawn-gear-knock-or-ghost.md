---
title: "Sugar Rush: Spawn Gear — 5 Knock OR 5 Ghost"
id: "130"
status: "halt"
halt_reason: "need confirmation"
priority: 01
sprint: alpha
category: CORE
description: "Spawn each Sugar Rush player with exactly one of two gears: 5 Knock charges (offense) or 5 Ghost charges (4 s, defense)."
modified: "2026-06-29"
supersedes_part_of: ["080"]
---

# Sugar Rush: Spawn Gear — 5 Knock OR 5 Ghost

## Problem
`#080 Disable Default Powerups Except Smack` keeps Smack as the only power-up.
Sugar Rush replaces Smack with two **mutually exclusive** spawn gears:

- **5 Knock charges** (offense — knock-steal; see #116)
- **5 Ghost charges** (defense — 4 s pass-through; see #117)

Each player picks one at lobby time.

## Solution
Add a lobby gear picker and spawn initialization.

### Changes
1. Add `SpawnGear` enum: `{ KNOCK, GHOST }`.
2. Add `player_spawn_gear: Dictionary[int, SpawnGear]`.
3. Add lobby UI: gear picker per player.
4. On `start_game_mode()`:
    - For each player, set `knock_charges = 5` (if `KNOCK`) or
      `ghost_charges = 5` (if `GHOST`).
    - The other counter stays at 0.
5. Update HUD to show the chosen gear + remaining charges.

## Acceptance Criteria
- Each player has exactly one gear type with 5 charges.
- The other gear type is unavailable (count = 0).
- Gear choice is networked.
- HUD reflects the chosen gear.

## Migration Checklist
- [ ] Add `SpawnGear` enum.
- [ ] Add `player_spawn_gear` dictionary.
- [ ] Add lobby picker UI.
- [ ] Initialize charges in `start_game_mode`.
- [ ] Update HUD to show gear + count.