---
title: "Mekton Bulls: Player Knock (Mutual Knockback)"
id: "142"
status: "todo"
blocked_by: ["139"]
priority: 02
sprint: alpha
category: CORE
description: "Players can knock each other (and bots) just like the bull does — 1 cell shove, with placement-side-effects for boundary or bull-line pushes."
modified: "2026-06-29"
---

# Mekton Bulls: Player Knock (Mutual Knockback)

## Problem
In Sugar Rush the **Knock charge** (#116) transfers head-stack candies.
In Mekton Bulls the **Knock power** (#139) shoves another player into
either the water boundary or the bull's charge path. This task wires
the actual knockback into `MektonBullsManager` and reuses the
shipped `Tekton`/player collision logic.

## Solution
Implement `_use_knock_on_player(attacker_pid, target_pid)` and chain
the side-effect loops.

### Concrete Changes
1. Add `_use_knock_on_player(attacker_pid, target_pid) -> bool`:
    - Returns false if target is out of range (>1 cell) or has no
      knock charge.
    - Shoves `target_pid` 1 cell in the direction the attacker is
      facing.
2. Side-effect loop on shove:
    - If target's new cell is on the arena boundary →
      `_trigger_water_flood_on_player(target_pid)` (delegated to
      `#137`).
    - If target's new cell is on the bull's line of sight →
      register a "trampoline" flag for `#136` to pick up on its
      next charge.
    - Else target stays.
3. Mutual knockback parity: bots use the same handler from `#141`.
4. Networked: `sync_player_knock` RPC.
5. SFX: same knock SFX as `gauntlet_manager.smack_*`.

## Acceptance Criteria
- Using a Knock power shoves the target exactly 1 cell.
- Shove into water → player eliminated by water flood.
- Shove into bull path → bull hits player on next charge.
- Shove into open cell → no side effect.
- Knock SFX plays.

## Migration Checklist
- [ ] Add `_use_knock_on_player`.
- [ ] Add trampoline flag on the bull (`#136`).
- [ ] Wire to `#137` water flood.
- [ ] Networked RPC.
- [ ] Add knock SFX.
- [ ] Verify parity with bot AI (`#141`).