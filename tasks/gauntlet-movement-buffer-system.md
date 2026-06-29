---
title: "Gauntlet: Movement Buffer System"
id: "083"
status: "done"
blocked_by: ["073"]
priority: 02
sprint: alpha
category: CORE
description: "Implement the hidden movement buffer system that prevents the arena from becoming movement-broken too early."
modified: "2026-06-26"
---

# Gauntlet: Movement Buffer System

## Problem
Without movement buffers, the ground growth algorithm could seal off all exits too early, making the arena unplayable before the final minute. Players need temporary safe routes to navigate while the candy spreads.

## Solution
Hidden algorithmic safe zones that decay over time:

### What Movement Buffers Are
- **Hidden from players** — not visually marked, not guaranteed safe
- **Not a shield or reward** — they don't protect camping players
- **Temporary** — decay over time and during phase transitions
- **Dynamic** — detected by the algorithm based on current arena shape

### Purpose
- Prevent unfair early traps
- Preserve basic movement flow
- Leave temporary gaps in sticky growth
- Support Cleanser decision-making
- Prevent arena from becoming broken too early

### How the Algorithm Uses Them
The system dynamically detects **safe clusters** (connected groups of SAFE cells). If removing a cluster would break movement flow, its targeting priority is temporarily reduced.

### Buffer Decay
| Event | Effect |
|---|---|
| Created | Full penalty value |
| Every 5 seconds | Reduce penalty by 25% |
| Phase change | Reduce all penalties by 50% |
| Final 30 seconds | Remove most penalties |

### Camping Override
If a player stays in the same area too long, the buffer weakens:
- Player in same 4×4 area >5–7 seconds: increase area's targetability
- Player in same area >8–10 seconds: allow candy bubble near that area

### Implementation Notes
- Movement Buffers are **not placed by level design**
- They are **detected dynamically** based on current sticky cell layout
- The system looks for SAFE cell clusters and reduces their selection chance
- Players experience this as "uneven candy growth" not "protected zones"

### Integration with Candidate Scoring
Movement buffer penalties are part of the `CandidateScore` formula:
- Phase 1: -40 inside buffer, -20 adjacent
- Phase 2: -20 inside buffer, -10 adjacent
- Phase 3: -10 inside buffer, 0 during final 30s

## Acceptance Criteria
- Players never see visual indicators for movement buffers
- Arena doesn't become movement-broken before final minute
- Buffers decay naturally over time
- Camping players lose buffer protection
- Final 30 seconds allows aggressive blocking
- Growth appears "uneven but fair" — not perfectly random, not perfectly predictable

## Migration Checklist
- [x] Add `movement_buffers: Dictionary` state (Vector2i → {penalty})
- [x] Implement `_detect_movement_buffers()` — find SAFE cell corridors (chokepoints)
- [x] Implement `_decay_movement_buffers()` — reduce penalties over time
- [x] Implement buffer integration in growth loop (`_detect_movement_buffers` runs in `_process_growth_tick` before scoring — satisfies #067's `_apply_movement_buffer_check`)
- [x] Add buffer penalty to `_calculate_candidate_score()` (via `_score_movement_buffer`)
- [x] Add camping tracker per player (position, duration) — reused from #073 (`_camp_tracking`)
- [x] Implement camping override (campers don't get fresh buffers near them)
- [x] Add phase-change decay (50% reduction in `_start_phase`)
- [x] Add final-30s removal (`_buffer_penalty_at` returns 0 in the final window)
- [ ] Test that growth appears organic with temporary gaps — deferred: live playtest (mechanics covered by 14/14 unit tests)

## Implementation Notes (2026-06-25)
Implemented in `scripts/managers/gauntlet_manager.gd`:
- **State:** `movement_buffers` (`Vector2i → {penalty}`), `_buffer_decay_timer`,
  and tuning consts — `BUFFER_DECAY_INTERVAL` (5s), `BUFFER_DECAY_FACTOR` (0.75 =
  −25%/step), `BUFFER_PHASE_DECAY` (0.5), `BUFFER_MIN_PENALTY` (4.0, prune floor),
  `BUFFER_BASE_PENALTY` (`[40, 20, 10]` per phase), `BUFFER_CORRIDOR_THRESHOLD` (12).
- **Detection** (`_detect_movement_buffers`, each growth tick before scoring): for
  each active player, examine the 4 passable neighbours; a neighbour is a corridor
  if removing it drops the player's BFS-reachable region below
  `BUFFER_CORRIDOR_THRESHOLD` (a genuine chokepoint, not open floor). Campers
  (`_camp_time_for_region > 5s`) get no fresh buffers near them.
- **Decay:** `_decay_movement_buffers(delta)` runs each server `_process` tick;
  every 5s scales all penalties by 0.75 and prunes faded ones. `_start_phase`
  halves all penalties (`_scale_all_buffers(0.5)`).
- **Scoring:** `_score_movement_buffer` returns the detected-corridor penalty
  (inside = full, adjacent = half via `_buffer_penalty_at`), falling back to the
  #073 player-proximity floor. Lifts entirely in the final 30s so the arena closes.
- Buffers are **never synced to clients** — purely a server-side scoring bias, so
  players experience "uneven candy growth," never visible protected zones.

Tests: `tests/test_gauntlet_movement_buffer.gd` — 14/14 passing (registration,
inside/adjacent/far penalty, final-window lift, time decay, prune, phase halving,
scoring integration). Full gauntlet suite: 130/130.
