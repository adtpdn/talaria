---
title: "Gauntlet: Growth Tick System (Replaces Cannon Volley)"
id: "067"
status: "done"
blocked_by: ["066", "068"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the core growth tick timing loop and candidate-based cell selection that replaces the old Candy Cannon projectile system."
modified: "2026-06-26"
---

# Gauntlet: Growth Tick System

## Problem
The old Candy Cannon fired projectiles at target cells. In v2, the Candy Pump NPC injects candy into the ground and sticky cells **grow outward** from existing sticky clusters using a cellular-automation-style system. This replaces the entire cannon/volley/projectile architecture.

## Solution
Server-authoritative growth tick timer with weighted candidate selection:

### Growth Timing
| Property | Value |
|---|---|
| Growth interval | Every 3 seconds |
| Telegraph duration | 1 second |
| Total ticks | 60 (180s ÷ 3s) |
| Ticks per phase | 20 each |

### Cells Per Tick (Phase-Based)
| Phase | Time | Cells per Tick | Distribution |
|---|---|---|---|
| Phase 1 (Outer Pressure) | 0:00–1:00 | 4–6 | 75% Outer, 10% Middle, 10% Near-Player, 5% Random |
| Phase 2 (Middle Pressure) | 1:00–2:00 | 6–8 | 50% Middle, 20% Outer, 15% Near-Player, 10% Sticky-Expansion, 5% Random |
| Phase 3 (Inner Survival) | 2:00–3:00 | 8–10 | 35% Inner, 25% Middle, 15% Near-Player, 15% Sticky-Expansion, 10% Random |

### Growth Tick Process
1. Find all SAFE cells
2. Remove invalid cells (BLOCKED, STICKY, BUBBLE_GROWING, already TELEGRAPHED)
3. Calculate **Candidate Score** for each valid cell
4. Select cells using **weighted randomness** (higher score = higher chance)
5. Apply **path safety check** — reject selections that would trap players before final 30s
6. Apply **movement buffer check** — respect hidden safe zones
7. Telegraph selected cells for 1 second
8. Convert telegraphed cells to STICKY

### Target Coverage
- **70%–75%** of playable cells by end of round (397–425 cells)
- Down from 80% in v1 — the growth system is more organic and less aggressive

### What Was Removed (v1 → v2)
- `cannon_timer`, `cannon_interval`, `volley_size` — replaced by `growth_timer`, `growth_interval`, phase-based cell counts
- `_fire_volley()` — replaced by `_process_growth_tick()`
- `_select_targets()` — replaced by `_generate_candidates()` + `_calculate_candidate_score()`
- `CandyCannonController` projectile system — removed entirely
- Impact shapes (1×1, 1×2, 2×2) — replaced by variable cells-per-tick
- `last_targeted_player_id` — replaced by candidate scoring penalties

## Acceptance Criteria
- Growth ticks fire exactly every 3 seconds
- 4–6 cells in Phase 1, 6–8 in Phase 2, 8–10 in Phase 3
- Telegraph appears for 1 second before cells become sticky
- All clients see telegraph and sticky cells simultaneously
- Coverage reaches 70–75% by end of 3-minute round

## Migration Checklist
- [x] Remove `cannon_timer`, `cannon_interval`, `volley_size` state variables
- [x] Remove `_fire_volley()`, `_select_targets()`, `_get_nearby_valid_cells()`
- [x] Add `growth_timer`, `growth_interval` (3.0s), `telegraph_duration` (1.0s)
- [x] Add `phase_growth_config` array with cells-per-tick ranges and distributions
- [x] Implement `_process_growth_tick()` — the main growth entry point
- [x] Implement `_generate_candidates()` — build scored list of all SAFE cells
- [x] Implement `_calculate_candidate_score()` — baseline (full formula in #073)
- [x] Implement `_select_cells_weighted()` — weighted random selection
- [x] Implement `_apply_path_safety()` — reject trapping selections (from #068)
- [x] Implement `_apply_movement_buffer_check()` — respect hidden safe zones (done in #083: `_detect_movement_buffers()` runs in `_process_growth_tick` before scoring)
- [x] Update `_process()` to use growth timer instead of cannon timer
- [x] Update phase transition logic to change growth config
- [x] Remove `sync_telegraph_highlight`, `sync_telegraph`, `sync_impact` RPCs (replaced with `sync_growth_telegraph`/`sync_growth_apply`)
- [x] Remove cannon_instance/candy_cannon_scene references (renamed to static `pump_instance`/`candy_pump_scene` NPC model)
- [ ] Verify 60 growth ticks over 180s produce ~70-75% coverage (deferred — live-match playtest)

## Status (2026-06-25)
Core growth-tick system is **done** and shipping. The remaining unchecked item
is a live-match playtest only, not a code gap:
- Movement-buffer check is now **wired in** via **#083** — `_detect_movement_buffers()`
  runs in `_process_growth_tick()` before scoring, and the penalty feeds
  `_score_movement_buffer`.
- Coverage verification needs a live 3-minute match (can't be asserted headless;
  the soft target lives in `is_coverage_reached()` / `COVERAGE_TARGET_MIN/MAX`).

## Implementation Notes (2026-06-24)
- `signal cannon_fired` → `signal growth_tick(cells)`, emitted after each apply.
- `_process_growth_tick()`: count = `_cells_this_tick()` (phase range) → `_generate_candidates()` (SAFE only; excludes sticky/telegraphed/cleansed/blocked) → `_select_cells_weighted()` → `_apply_path_safety()` → telegraph (passable 1s) → `sync_growth_apply` converts to sticky.
- Baseline score = LayerPriority (phase ring weights) + StickyNeighbor (+8/neighbor, cap +64) + RandomNoise (±20) + RepetitionPenalty (−30 near last tick). Full formula (player/cluster/camping/route pressure) deferred to #073.
- Helpers: `_layer_of()` (outer≥7 / middle≥4 / inner Chebyshev from center), `_sticky_neighbor_count()` (8-dir), `_chebyshev()`.
- Tests: `tests/test_gauntlet_growth_tick.gd` (renamed from cannon-timer test) — 19/19 passing.
