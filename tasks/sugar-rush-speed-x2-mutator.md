---
title: "Sugar Rush: Speed ×2 Mutator"
id: "122"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: CORE
description: "Replace the slow-mo effect (¼ speed, 4 s) with Sugar Rush — game speed ×2 for 2 s base + 1.2× per candy delivered."
modified: "2026-06-29"
supersedes: ["078"]
---

# Sugar Rush: Speed ×2 Mutator

## Problem
`trigger_slowmo(duration = 4.0)` slows the game to ¼ speed for 4 s on a
trigger. Sugar Rush **inverts** the effect: game speed **×2** for
`candies_fed × 1.2 × 2` seconds.

## Solution
Replace slow-mo with a speed multiplier.

### Changes
1. Rename `trigger_slowmo` → `trigger_sugar_rush`:
    - Signature: `trigger_sugar_rush(pid: int, candies_fed: int) -> void`.
    - Adds `candies_fed * 1.2 * 2.0` seconds of ×2 speed to
      `rush_active_until[pid]` (global, not per-player).
2. Add `global_time_scale: float = 1.0`:
    - When any player is in rush → `global_time_scale = 2.0`.
    - Otherwise `global_time_scale = 1.0`.
3. Replace `_show_slowmo_overlay()` / `_hide_slowmo_overlay()` with
   `_show_rush_overlay()` / `_hide_rush_overlay()` (red bar fill, see
   #120).
4. Wire `Engine.time_scale` to `global_time_scale`.
5. Keep `slowmo_duration` constant for legacy Gauntlet (#078).

## Acceptance Criteria
- Feeding 1 candy → 2 s of ×2 speed.
- Feeding 5 candies → 4 s of ×2 speed.
- Feeding 8+ candies → capped at `rush_stacking_limit` (#115).
- Game-wide: projectiles, dashers, AI, timers all run at ×2 during rush.
- Removing all rush cleanly returns `global_time_scale = 1.0`.

## Migration Checklist
- [ ] Rename `trigger_slowmo` → `trigger_sugar_rush`.
- [ ] Add `global_time_scale`.
- [ ] Replace overlay VFX with red rush bar (#120).
- [ ] Wire `Engine.time_scale`.
- [ ] Document stacking cap (#115).