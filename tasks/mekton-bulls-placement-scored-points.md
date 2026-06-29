---
title: "Mekton Bulls: Placement-Scored Point System"
id: "140"
status: "todo"
blocked_by: ["134", "137"]
priority: 01
sprint: alpha
category: CORE
description: "Replace per-second trickle scoring with a static placement-scored system — last standing gets max points, first out gets min, middle is linear interpolation."
modified: "2026-06-29"
---

# Mekton Bulls: Placement-Scored Point System

## Problem
Sugar Rush scores per-second (carry multiplier + delivery). Mekton
Bulls scores by **placement** only — no per-second trickle. The
shipped `_on_score_updated` hook in `main.gd` is per-tick and would
give the wrong shape.

## Solution
Add a placement table computed at end-of-match based on elimination
order.

### Concrete Changes
1. Add `player_placement: Dictionary[int, int]`:
    - Maps `peer_id → placement rank` (1 = first eliminated, N = last standing).
    - Updated in `_on_player_eliminated()` triggered by #137 (water
      flood) or #136 (bull contact).
2. Add config on `LobbyManager`:
    - `mekton_bulls_min_points: int = 100`
    - `mekton_bulls_max_points: int = 1000`
3. On match end (`_on_round_ended`):
    - For each `pid` sorted by elimination order:
        - First out → `min_points`.
        - Last standing → `max_points`.
        - Middle → linear interpolation.
    - Push scores via `sync_score_updated()`.
4. **Elimination order matters.** First elimination is recorded before
   any subsequent one; we never overwrite a placement.
5. Tiebreaker: simultaneous eliminations (same tick) → shared placement,
   average points.
6. End-of-match UI overlay: `#143` shows a placement table.

## Acceptance Criteria
- Last surviving player gets `mekton_bulls_max_points`.
- First eliminated player gets `mekton_bulls_min_points`.
- Middle players receive linearly interpolated points.
- Scores push via the existing `sync_score_updated` RPC.
- Ties are handled (shared rank, averaged points).

## Migration Checklist
- [ ] Add `player_placement` dict.
- [ ] Add `mekton_bulls_min_points` / `max_points` config + RPC.
- [ ] Implement linear interpolation helper.
- [ ] Hook `_on_player_eliminated()`.
- [ ] Disable per-second scoring while in `Mekton Bulls` mode.
- [ ] Tiebreaker logic for simultaneous eliminations.
- [ ] Add placement UI overlay (in `#143`).