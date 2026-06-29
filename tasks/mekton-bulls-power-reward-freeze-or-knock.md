---
title: "Mekton Bulls: Power Reward — Freeze OR Knock"
id: "139"
status: "todo"
blocked_by: ["138"]
priority: 02
sprint: alpha
category: CORE
description: "Award each blueprint completion with a single power of the player's choice: Freeze (slow the nearest bull) or Knock (shove another player)."
modified: "2026-06-29"
---

# Mekton Bulls: Power Reward — Freeze OR Knock

## Problem
Finishing a 3 × 3 blueprint must award the player **1 power**, their
choice between:

- **Freeze** — slow the nearest bull long enough to escape.
- **Knock** — shove another player into the bull's path or out of the
  shrinking arena.

This is Mekton Bulls' only offensive gear — different from Sugar Rush's
5-charge Knock OR 5-charge Ghost; here each power is a **single-use
choice** gated by blueprint completion.

## Solution
Add a power inventory + per-power pickup handlers.

### Concrete Changes
1. Add `player_power: Dictionary[int, Power]` where
   `Power = { FREEZE: int, KNOCK: int }` (counters per type).
2. On blueprint completion (`_on_blueprint_completed(pid)`):
    - Open the power-picker UI for `pid` (`#143` HUD).
    - On pick → increment that counter by 1.
3. **Freeze handler — `_use_freeze(pid)`:**
    - Find nearest `MektonBull`.
    - Apply `bull.slow_time = 3.0` (3 s of ½ speed).
    - Emit SFX + freeze VFX on the bull.
4. **Knock handler — `_use_knock(pid, target_pid)`:**
    - Shove target 1 cell.
    - If target ends up on `TILE_WATER` boundary → eliminated by
      `#137` flood on next tick.
    - Or if target ends up in bull path → bull knocks them on its
      next charge.
5. Networked: `sync_power_pick`, `sync_power_use`.
6. Both powers share cooldown per player (1 s) so spam-clicking
   doesn't bypass the gate.

## Acceptance Criteria
- Each completed blueprint awards exactly 1 power.
- Player can choose Freeze or Knock from the picker UI.
- Freeze slow lasts 3 s on the bull.
- Knock shoves a target 1 cell.
- Counts are networked.
- One-power-per-completion rule is enforced.

## Migration Checklist
- [ ] Add `player_power` dict.
- [ ] Add `_on_blueprint_completed` trigger.
- [ ] Add power-picker UI (in `#143`).
- [ ] Implement `_use_freeze` + `_use_knock`.
- [ ] Wire to `#136` bull and `#137` flood.
- [ ] Networked RPCs.
- [ ] Per-player cooldown.