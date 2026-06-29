---
title: "Sugar Rush: Half-Point Penalty for Off-Color Finish"
id: "129"
status: "halt"
halt_reason: "need confirmation"
priority: 03
sprint: alpha
category: CORE
description: "Award ½ points when a player finishes a blueprint using a non-matching color tile."
modified: "2026-06-29"
---

# Sugar Rush: Half-Point Penalty for Off-Color Finish

## Problem
If the player's blueprint color runs out, they can finish the blueprint by
walking on any other color. Per the design spec, this earns **½ points**
instead of full points. The current candy tick (#113) does not distinguish
between "matching pickup" and "off-color pickup".

## Solution
Track off-color pickups and halve the awarded points on completion.

### Changes
1. Add `player_blueprint[pid].off_color_pickups: int`:
    - Increments when a non-matching tile is picked up.
    - Resets on completion.
2. In `#113 _process_candy_tick`, increment `off_color_pickups` instead
   of `progress` for mismatched tiles.
3. On blueprint completion:
    - If `off_color_pickups > 0` → award `delivery_points * 0.5`.
    - Otherwise full points.
4. Update HUD badge to indicate "off-color finish" VFX (TBD).

## Acceptance Criteria
- Finishing a blueprint with 0 off-color pickups → full points.
- Finishing with any off-color pickups → ½ points.
- Off-color counter resets after delivery.
- Bots respect the rule (no special-casing; same code path).

## Migration Checklist
- [ ] Add `off_color_pickups` to blueprint state.
- [ ] Update `#113` tick to increment correctly.
- [ ] Apply ½ multiplier on completion.
- [ ] Add HUD indicator (TBD).