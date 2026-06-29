---
title: "Mekton Bulls: 3 × 3 Blueprint Auto-Pickup"
id: "138"
status: "todo"
blocked_by: ["134", "135"]
priority: 01
sprint: alpha
category: CORE
description: "Distribute small 3×3 blueprints across the arena with automatic pickup — walking over a matching tile counts toward the player's blueprint progress."
modified: "2026-06-29"
---

# Mekton Bulls: 3 × 3 Blueprint Auto-Pickup

## Problem
Sugar Rush's blueprints are single-color, full-arena. Mekton Bulls
blueprints are **3 × 3** — a tight neighbourhood that constrains
play and rewards reading local tile clusters. We need a smaller
blueprint shape on the same auto-pickup foundation
(`tasks/sugar-rush-single-color-blueprint.md` -> `#119`).

## Solution
Reuse the Sugar Rush blueprint machinery (single-color,
auto-pickup, networked) but switch the **shape** from full-arena to
**3 × 3 local clusters** that re-randomise on completion.

### Concrete Changes
1. Add `_assign_initial_blueprints()` to `MektonBullsManager` (mirror of
   `#119 _assign_initial_blueprints` on `GauntletManager`).
2. Blueprint shape: for each player, pick a random 3 × 3 anchor cell
   inside the current arena + a random target color
   (R / G / B / Y, 4 colors).
3. Cell positions in the 3 × 3 are pre-computed from the anchor:
    - `cells = [anchor + offset for offset in offsets_3x3]`.
    - Offsets: `[(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]`.
4. On `_process_candy_tick`:
    - If player's cell is in their blueprint's 3 × 3 AND matches the
      target color → progress += 1.
    - If `progress >= 9` → grant a power (`#139`) and re-roll a new 3 × 3.
5. The Mekton Bulls arena shrinks (`#135`) — re-validate 3 × 3 anchors
   that fall outside the new boundary on shrink, re-roll them.
6. No off-color penalty (Meekton Bulls uses no color-matching
   delivery — placement scoring only).

## Acceptance Criteria
- Each player has one 3 × 3 anchor at a time.
- Walking over a matching tile inside the 3 × 3 ticks progress.
- Reaching 9 progress grants one power (Freeze OR Knock).
- New 3 × 3 anchor is randomized on completion.
- Shrink re-rolls anchors that fall outside the new boundary.

## Migration Checklist
- [ ] Add `Blueprint3x3` data class (anchor, color, cells, progress).
- [ ] Implement `_assign_initial_blueprints`.
- [ ] Add `_validate_blueprint_after_shrink`.
- [ ] Hook into candy-tick / shrink.
- [ ] Grant 1 power on completion (`#139`).