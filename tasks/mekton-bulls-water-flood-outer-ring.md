---
title: "Mekton Bulls: Water Flood Outer Ring"
id: "137"
status: "todo"
blocked_by: ["135"]
priority: 01
sprint: alpha
category: CORE
description: "When a bull stands on the arena boundary, flood the outermost ring with water and instantly eliminate any player on that ring."
modified: "2026-06-29"
---

# Mekton Bulls: Water Flood Outer Ring

## Problem
A bull standing on the outer boundary of the arena **floods the
outermost ring with water** — instant elimination for any player on
that ring. This is the kicker mechanic that makes shrinking the arena
dangerous: standing at the edge invites a bull flood.

## Solution
Add a tick that watches for a bull on the boundary and floods the
outermost ring.

### Concrete Changes
1. Add `TILE_WATER` cell type (used by `#135` shrinker).
2. In `MektonBullsManager._process_tick()`:
    - If any `MektonBull` occupies an `_is_boundary(pos)` cell →
      `_trigger_water_flood()`.
3. `_trigger_water_flood()`:
    - For every player whose current cell is on the **outermost ring**
      of `arena_size` → eliminate them.
    - Play a water VFX (rising tide + splash SFX).
    - Set those cells to `TILE_WATER` for the duration of the match
      (no recovery).
4. Cooldown: 3 s minimum between floods (so a bull standing on the
   boundary doesn't instantly re-trigger).
5. Tie `_on_player_eliminated()` into `#140` placement scoring.

## Acceptance Criteria
- A bull on the boundary floods the outer ring.
- Any player on the outer ring is eliminated instantly.
- Flood VFX plays + SFX.
- 3 s cooldown between floods.
- Flooded cells remain water for the rest of the match.

## Migration Checklist
- [ ] Add `TILE_WATER` tile enum.
- [ ] Add `MektonBullsManager._trigger_water_flood`.
- [ ] Hook into `_process_tick()`.
- [ ] Add flood VFX + SFX.
- [ ] Wire elimination → `#140` placement scoring.
- [ ] Confirm bull cannot stand on water itself.