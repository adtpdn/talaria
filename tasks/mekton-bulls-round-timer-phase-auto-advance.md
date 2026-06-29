---
title: "Mekton Bulls: Round Timer & Phase Auto-Advance"
id: "145"
status: "todo"
blocked_by: ["134", "135"]
priority: 02
sprint: alpha
category: CORE
description: "Run the Mekton Bulls round timer, auto-advance phases, and end the round at the configured duration (default ≤ 2 min) or when one player remains."
modified: "2026-06-29"
---

# Mekton Bulls: Round Timer & Phase Auto-Advance

## Problem
Mekton Bulls must finish in **2 minutes or less** (per the design spec).
The shipped `gauntlet_round_duration = 180` (`lobby_manager.gd`) is the
default for Gauntlet. Mekton Bulls needs its own timer
(`mekton_bulls_round_duration = 120`) and **automatic phase advance**
that doesn't depend on a player picking up candies.

## Solution
Add a per-mode round timer + phase scheduler on `MektonBullsManager`.

### Concrete Changes
1. Add `MektonBullsManager.round_duration: float = 120.0`.
2. Add `MektonBullsManager._round_tick(delta)`:
    - Decrements remaining time.
    - Emits `time_remaining_changed` for HUD.
3. Add `MektonBullsManager.phase_interval: float = 30.0`:
    - `_shrink_arena()` fires every `phase_interval` seconds (TBD;
      design says 4 phases in 120 s → ~30 s each).
4. Add `_on_round_time_expired()`:
    - Calls placement scoring (`#140`) with all survivors as last
      standing.
5. Add `_on_one_player_remaining(player_id)`:
    - Early end — survivors split max points.
6. Add to `LobbyManager`:
    - `mekton_bulls_round_duration: int = 120`
    - `mekton_bulls_phase_interval: int = 30`
    - RPCs `set_` / `sync_` for both.
7. Emit `round_ended(placements)` once, never twice.

## Acceptance Criteria
- Round ends at exactly `mekton_bulls_round_duration` seconds.
- Phase shrinks every `mekton_bulls_phase_interval` seconds.
- Round ends early when only one player is left.
- All RPCs are networked.
- HUD shows remaining time and current phase.

## Migration Checklist
- [ ] Add `round_duration` + `phase_interval` config.
- [ ] Add `_round_tick` + `_on_round_time_expired`.
- [ ] Add `_on_one_player_remaining`.
- [ ] RPCs for `round_duration` and `phase_interval`.
- [ ] Wire to HUD time/phase widgets (`#143`).
- [ ] Disable `gauntlet_round_duration` use while `mode == MEKTON_BULLS`.