---
title: "Sugar Rush: Sugar Rush Stacking (Replaces Phase Escalation)"
id: "115"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: CORE
description: "Replace growth phase escalation (cells_per_tick dict) with Sugar Rush stacking — rush duration caps and converts overflow to points."
modified: "2026-06-29"
supersedes: ["070"]
---

# Sugar Rush: Sugar Rush Stacking

## Problem
`_check_phase_transition()` escalates `cells_per_tick` across three phases
(`OPEN_ARENA → ROUTE_PRESSURE → SURVIVAL_ENDGAME`). Sugar Rush removes the
phase-driven escalation and replaces it with a **rush-stacking** mechanic:
rush time is added per candy delivered, capped at a TBD limit, and any
overflow converts to points.

## Solution
Replace the phase escalation with a stack manager.

### Changes
1. Add `rush_stacking_limit: float = 12.0` (TBD) and `rush_points_per_sec: int = 50`.
2. Replace `cells_per_tick` dict with `rush_stack_state[pid]`:
    - `current_rush_time: float`
    - `last_delivery_at: float`
3. `trigger_sugar_rush(pid, candies_fed)`:
    - Adds `candies_fed * 1.2 * 2.0` seconds to `current_rush_time`.
    - If `current_rush_time > rush_stacking_limit` → convert overflow to
      points at `rush_points_per_sec` and clamp.
4. Keep the three-phase enum for backward compatibility, but Sugar Rush
   starts in `OPEN_ARENA` and never transitions.
5. Keep `PHASE_3_START = 120.0` — Survival Endgame still triggers at the
   last 120 s as a global "final push" event.

## Acceptance Criteria
- Delivering 5 candies → 4 s rush (per spec).
- 8+ candies → capped at `rush_stacking_limit`, excess converts to points.
- `current_phase` stays at `Phase.OPEN_ARENA` (no escalation).
- Survival Endgame still fires at 120 s remaining.

## Migration Checklist
- [ ] Add `rush_stacking_limit` config.
- [ ] Add `rush_points_per_sec` config.
- [ ] Implement `trigger_sugar_rush(pid, candies_fed)`.
- [ ] Disable `_check_phase_transition()` for Sugar Rush (keep for legacy).
- [ ] Document final-push Survival Endgame hook.