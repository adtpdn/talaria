---
title: "Gauntlet: Candy Bubble System"
id: "082"
status: "done"
blocked_by: ["068", "073"]
priority: 01
sprint: alpha
category: CORE
description: "Implement the candy bubble anti-camping hazard that grows from 1×1 and explodes into 3×3 sticky areas."
modified: "2026-06-26"
---

# Gauntlet: Candy Bubble System

## Problem
Without anti-camping hazards, players can hide in safe corners and avoid the ground growth pressure. Candy bubbles force players out of comfortable positions and create panic moments during the match.

## Solution
Occasional anti-camping hazards that grow and explode:

### Bubble Timing
| Phase | Bubbles |
|---|---|
| Phase 1 (0:00–1:00) | 0 |
| Phase 2 (1:00–2:00) | 2 total |
| Phase 3 (2:00–3:00) | 3 total |
| **Total per round** | **5** |

### Bubble Properties
- **Grow Duration:** 2.5–3 seconds
- **Explosion Size:** 3×3 sticky area
- **Visual Stages:**
  1. Small 1×1 candy bubble appears
  2. Bubble grows larger and becomes brighter
  3. Bubble shakes or pulses
  4. Bubble explodes into 3×3 sticky area

### Bubble Spawn Scoring
Bubbles use a separate scoring system from normal growth:

```
BubbleScore =
    CampingScore
  + UntouchedAreaScore
  + PlayerClusterScore
  + MissionRouteScore
  + RandomNoise
  + DirectHitPenalty
  + RecentBubblePenalty
  + UnfairTrapPenalty
```

| Component | Value |
|---|---|
| CampingScore | +40 if player in same 4×4 >5s, +60 if >8s, +80 if >10s with Cleanser |
| UntouchedAreaScore | +30 if near large untouched cluster |
| PlayerClusterScore | +20 if 2+ players nearby |
| MissionRouteScore | +10 to +20 if important for scoring |
| RandomNoise | -20 to +20 |
| DirectHitPenalty | -60 if directly under player |
| RecentBubblePenalty | -50 if area had recent bubble |
| UnfairTrapPenalty | -100 if creates unavoidable trap |

### Bubble Anti-Unfairness Rules
- Do not spawn with no readable warning
- Do not spawn that instantly traps all nearby players
- Do not stack multiple bubbles in same small area
- Do not spawn repeatedly in exact same region
- Do not use as main map-filling tool

### Visual Telegraph
- 3×3 warning area appears during grow phase
- Pulsing shadow/circular glow around bubble
- Syrup splash preview before explosion
- Final flash before impact

## Acceptance Criteria
- 0 bubbles in Phase 1, 2 in Phase 2, 3 in Phase 3
- Bubble grows visibly for 2.5–3 seconds before exploding
- 3×3 explosion area is visually warned before impact
- Bubbles target camping behavior and large untouched spaces
- No bubble spawns directly on a player without warning
- Bubbles don't stack in the same area

## Migration Checklist
- [x] Add `active_bubbles: Array` state to GauntletManager
- [x] Add `recent_bubble_positions: Array` for anti-stacking
- [x] Add `bubbles_this_phase: int` counter
- [x] Add `MAX_BUBBLES_PER_PHASE: Array = [0, 2, 3]`
- [x] Implement `_try_spawn_bubble()` — called each growth tick
- [x] Implement `_generate_bubble_candidates()` — scored candidate list
- [x] Implement `_calculate_bubble_score()` — bubble-specific scoring
- [x] Implement `_spawn_bubble()` — create growing bubble at position
- [x] Implement `_explode_bubble()` — apply 3×3 sticky, VFX, slow players
- [x] Implement bubble grow timer in `_process()` (`_update_bubbles`)
- [x] Add `sync_bubble_spawn` and `sync_bubble_explode` RPCs
- [x] Add bubble VFX (grow animation, warning area, explosion particles)
- [x] Invalidate bot paths on bubble explosion (`gridmap.initialize_astar()`)

## Implementation Notes (2026-06-25)
Implemented in `scripts/managers/gauntlet_manager.gd`:
- **State:** `active_bubbles` (`{center, timer, cells}`), `bubble_cells` (BUBBLE_GROWING
  overlay), `recent_bubble_positions` (anti-stacking, capped at `BUBBLE_RECENT_MEMORY`
  = 4), `bubbles_this_phase` / `bubbles_total`, `MAX_BUBBLES_PER_PHASE = [0, 2, 3]`,
  `BUBBLE_GROW_DURATION` = 2.75s, `BUBBLE_EXPLOSION_RADIUS` = 1 (3×3).
- **Cell state:** `BUBBLE_GROWING` wired into `cell_state()` so a growing bubble's
  footprint is excluded from normal growth candidates (still passable).
- **Spawn:** `_try_spawn_bubble()` runs after each growth tick, phase-gated by the
  per-phase budget and a ~25% per-eligible-tick chance; rejects centers that score
  negative (penalties veto). Picks via the shared `_select_cells_weighted`.
- **Scoring** (`_calculate_bubble_score`): Camping (+40/+60/+80-w-cleanser) +
  UntouchedArea (+30 large open region via BFS) + PlayerCluster (+20 for 2+ nearby)
  + RandomNoise(±20) + DirectHit (−60 under a player) + Recent (−50 anti-stacking)
  + UnfairTrap (−100 if the 3×3 would strand a player before the final window).
  Each component is its own testable fn.
- **Lifecycle:** `_spawn_bubble` marks the 3×3 BUBBLE_GROWING + starts a grow timer
  + `sync_bubble_spawn` (telegraph overlay + growing candy sphere VFX + audio).
  `_update_bubbles(delta)` in the server `_process` advances timers; on elapse
  `_explode_bubble` converts the 3×3 to sticky, `sync_bubble_explode` (sticky
  overlay + medium shake + splash particles), slows players caught in the blast
  (reuses `apply_sticky_slow` from #068; cleanser-immune), and re-inits A* so bot
  paths re-route.
- Per-phase counter resets in `_start_phase`.

Tests: `tests/test_gauntlet_bubble.gd` — 16/16 passing (phase budgets, 3×3 clip,
all score components, anti-stacking cap, grow→explode lifecycle). A headless
GridMap mock (`tests/helpers/gridmap_mock.gd`) records `set_cell_item` so the
local sync path runs without a real GridMap. Full gauntlet suite: 146/146.

Live-only checks (not headless-testable): visible 2.5–3s grow animation, 60 FPS,
"no spawn directly on a player without warning" feel.
