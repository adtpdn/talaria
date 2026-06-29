---
title: "Sugar Rush: Candy Stack Growth Tick"
id: "113"
status: "halt"
halt_reason: "need confirmation"
priority: 01
sprint: alpha
category: CORE
description: "Replace the shipped _process_growth_tick with a per-second candy-stack tick that grows the player's head stack when standing on a matching tile."
modified: "2026-06-29"
supersedes: ["067"]
---

# Sugar Rush: Candy Stack Growth Tick

## Problem
`gauntlet_manager._process_growth_tick()` selects sticky-cell candidates and
schedules them for telegraph → sticky. Sugar Rush does not grow sticky cells
on a timer — instead, the player **picks up** candy onto their head stack
when they walk over a matching-color tile.

## Solution
Replace the tick implementation. Keep the timer cadence
(`gauntlet_growth_interval = 3 s` default), but redirect its work from
"grow the arena" to "feed the players".

### Changes
1. Rename `_process_growth_tick()` → `_process_candy_tick()`.
2. For each live player, check if their cell tile color matches the active
   blueprint color.
    - Match → increment `player_head_stack[pid]` by 1.
    - No match → no-op (or: increment a `player_off_color_count` for
      [task #129](#) half-point tracking).
3. Blueprint state machine: when a player's blueprint reaches its required
   count, spawn a candy on their head (see #127).
4. Remove `telegraphed_cells` dictionary usage (replaced by #114).
5. Keep the 3 s interval; emit `candy_tick(player_id, color)` signal.

## Acceptance Criteria
- Walking over a matching tile increments the head stack by 1 / 3 s.
- Standing still on a matching tile still increments (it's a tick, not a step).
- Off-color tiles do not increment.
- Blueprint completion spawns a candy on the head.
- Sticky cells still grow at the existing rate (handled by `is_sticky_cell`,
  unchanged from #068).

## Migration Checklist
- [ ] Rename `_process_growth_tick` → `_process_candy_tick`.
- [ ] Add `player_head_stack: Dictionary[int, int]`.
- [ ] Hook blueprint completion → head-stack spawn.
- [ ] Remove `sync_growth_telegraph` callers (replaced by #114).
- [ ] Keep sticky growth unaffected.