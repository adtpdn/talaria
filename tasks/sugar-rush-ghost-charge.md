---
title: "Sugar Rush: Ghost Charge (4 s)"
id: "117"
status: "todo"
priority: 01
sprint: alpha
category: CORE
description: "Replace the Cleanser Power-Up with a 5-charge, 4-second Ghost Charge that lets the player walk through candies and become immune to knocks."
modified: "2026-06-29"
supersedes: ["072"]
---

# Sugar Rush: Ghost Charge (4 s)

## Problem
`_try_use_cleanser()` and `use_cleanser_cell()` grant 5 cells of sticky-cell
immunity and clear those cells on contact. Sugar Rush removes Cleanser and
adds a **Ghost Charge**: 4 seconds of pass-through candy movement and
knock immunity.

## Solution
Replace Cleanser with Ghost.

### Changes
1. Rename `use_cleanser_cell` → `activate_ghost(pid) -> bool`:
    - Adds 4 s to `ghost_active_until[pid]` (networked time).
    - Returns true if the player had a charge.
2. Add `ghost_charges: Dictionary[int, int]` initialized to **5** per
   player at spawn (see #130 for the "5 knock OR 5 ghost" choice).
3. Add `is_ghost_active(pid) -> bool`:
    - Returns `Time.get_ticks_msec() / 1000.0 < ghost_active_until[pid]`.
4. While ghost is active:
    - Player collides through candy pickups (no head-stack increment).
    - Player is immune to knock (#116).
5. Remove Cleanser per-cell clearing (`mark_cleansed`, `clear_sticky_cell`)
   for Sugar Rush — keep the methods for legacy Gauntlet.

## Acceptance Criteria
- Each player starts with 5 ghost charges (or 5 knock charges; see #116/#130).
- Activation lasts exactly 4 s.
- During ghost: no head-stack gain from tiles.
- During ghost: knock charges bounce off (no transfer).
- Ghost VFX is distinct from knock VFX (translucent / white).

## Migration Checklist
- [ ] Replace `_try_use_cleanser` → `_try_activate_ghost`.
- [ ] Add `ghost_charges` dictionary.
- [ ] Add `ghost_active_until` dictionary.
- [ ] Add `is_ghost_active()` helper.
- [ ] Wire to #118 Bot AI and #116 Knock Charge System.