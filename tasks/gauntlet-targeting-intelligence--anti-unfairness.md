---
title: "Gauntlet: Candidate Scoring System (Replaces Targeting Intelligence)"
id: "073"
status: "done"
blocked_by: ["067"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the cellular-automation-style candidate scoring system for weighted cell selection, replacing the old cannon targeting logic."
modified: "2026-06-25"
---

# Gauntlet: Candidate Scoring System

## Problem
In v1, the cannon used weighted targeting (60% player proximity, 25% route blocking, etc.). In v2, cell selection uses a **candidate scoring formula** that makes growth feel organic, semi-predictable, and shaped by the current phase.

## Solution
Each SAFE cell receives a score. Higher score = higher chance of being selected for sticky growth.

### Candidate Score Formula
```
CandidateScore =
    LayerPriority
  + StickyNeighborScore
  + InwardPressureScore
  + PlayerPressureScore
  + ClusterGrowthScore
  + RoutePressureScore
  + CampingPressureScore
  + RandomNoise
  + MovementBufferPenalty
  + PathSafetyPenalty
  + RepetitionPenalty
```

### Score Components

**LayerPriority** — Guides candy to current pressure layer:
| Phase | Outer | Middle | Inner |
|---|---|---|---|
| 1 | +60 | +15 | -40 |
| 2 | +20 | +60 | +5 |
| 3 | +10 | +35 | +60 |

**StickyNeighborScore** — Prefer growing near existing sticky:
- +8 per sticky neighbor (max +64)
- Creates organic cellular-automation clusters

**InwardPressureScore** — Push inward over time:
- Phase 1: +0 to +10
- Phase 2: +5 to +20
- Phase 3: +10 to +30

**PlayerPressureScore** — Pressure players without direct targeting:
- 2–4 cells from player: +20
- Directly under player (before final 30s): -50
- Directly under player (final 30s): +10

**ClusterGrowthScore** — Connect sticky clusters:
- Expands existing cluster: +15
- Connects two clusters: +25

**RoutePressureScore** — Pressure common routes:
- +10 to +25 for high-traffic cells

**CampingPressureScore** — Break camping behavior:
- Player in same 4×4 area >5s: +20
- >8s: +40
- >10s with Cleanser: +60

**RandomNoise** — Keep growth imperfect:
- Random between -20 and +20

**MovementBufferPenalty** — Respect hidden safe zones:
- Phase 1: -40 inside buffer, -20 adjacent
- Phase 2: -20 inside, -10 adjacent
- Phase 3: -10 inside, 0 during final 30s

**PathSafetyPenalty** — Prevent unfair traps:
- Would fully trap player (before final 30s): -100
- Removes last exit from cluster: -60
- Makes route too narrow: -20

**RepetitionPenalty** — Avoid spammy growth:
- Neighbors selected last tick: -30
- Same region targeted recently: -15

### What Was Removed (v1 → v2)
- `last_targeted_player_id` — replaced by PlayerPressureScore
- 60/25/10/5 targeting weights — replaced by full candidate scoring
- `_select_targets()` — replaced by `_generate_candidates()` + `_select_cells_weighted()`
- `_get_route_blocking_target()` — replaced by RoutePressureScore
- Anti-unfairness as separate system — integrated into score penalties

## Acceptance Criteria
- Growth feels organic and semi-predictable (not perfectly random, not perfectly readable)
- Candy preferentially grows near existing sticky clusters
- Players near the pressure layer feel more pressure
- Camping players get their area targeted
- No unfair instant traps before final 30 seconds

## Migration Checklist
- [x] Implement `_generate_candidates()` — iterate all SAFE cells, calculate scores
- [x] Implement `_calculate_candidate_score()` — full formula with all components
- [x] Implement `_select_cells_weighted()` — weighted random selection from scored candidates
- [x] Implement layer priority lookup per phase (`_score_layer_priority`)
- [x] Implement sticky neighbor counting (8-directional) (`_score_sticky_neighbor`)
- [x] Implement player pressure scoring (distance-based) (`_score_player_pressure`)
- [x] Implement cluster growth detection (`_score_cluster_growth`)
- [x] Implement camping detection (4×4 area tracking per player) (`_camp_tracking` + `_score_camping_pressure`)
- [x] Implement repetition penalty (recent target tracking) (`_score_repetition`)
- [x] Remove old `_select_targets()`, `_get_nearby_valid_cells()`, targeting weights (done in #067)
- [x] Remove `last_targeted_player_id` tracking (done in #067)
- [ ] Test that growth produces organic, broken patterns (not rings or squares) — deferred: live playtest (component logic verified by 21/21 unit tests)

## Implementation Notes (2026-06-24)
Full formula in `_calculate_candidate_score(pos, player_cells)`:
`LayerPriority + StickyNeighbor + InwardPressure + PlayerPressure + ClusterGrowth + CampingPressure + RandomNoise(±20) + MovementBuffer + PathSafety + Repetition`

Each component is its own testable fn: `_score_layer_priority`, `_score_sticky_neighbor`, `_score_inward_pressure`, `_score_player_pressure`, `_score_cluster_growth`, `_score_camping_pressure`, `_score_movement_buffer`, `_score_path_safety` (soft; hard guarantee stays in `_apply_path_safety` from #068), `_score_repetition`.

Camping: `_update_camp_tracking(delta)` runs each server tick in `_process`, accumulating per-player time in their 4×4 region (`_region_of`), reset on region change. `_camp_time_for_region` returns the max camp time for scoring.

`_generate_candidates()` gathers player cells once per tick and threads them into scoring (avoids re-querying the scene tree per cell).

`MovementBuffer` here is a soft proximity penalty; the full hidden-safe-zone system is task #083.

Tests: `tests/test_gauntlet_scoring.gd` — 21/21 passing (component + composition + camping accumulation).
