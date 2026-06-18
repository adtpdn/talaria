---
title: "Gauntlet: Candy Bubble System"
id: "082"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Implement the candy bubble anti-camping hazard that grows from 1×1 and explodes into 3×3 sticky areas."
modified: "2026-06-18"
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
- [ ] Add `active_bubbles: Array` state to GauntletManager
- [ ] Add `recent_bubble_positions: Array` for anti-stacking
- [ ] Add `bubbles_this_phase: int` counter
- [ ] Add `max_bubbles_per_phase: Array = [0, 2, 3]`
- [ ] Implement `_try_spawn_bubble()` — called each growth tick
- [ ] Implement `_generate_bubble_candidates()` — scored candidate list
- [ ] Implement `_calculate_bubble_score()` — bubble-specific scoring
- [ ] Implement `_spawn_bubble()` — create growing bubble at position
- [ ] Implement `_explode_bubble()` — apply 3×3 sticky, VFX, trap players
- [ ] Implement bubble grow timer in `_process()`
- [ ] Add `sync_bubble_spawn` and `sync_bubble_explode` RPCs
- [ ] Add bubble VFX (grow animation, warning area, explosion particles)
- [ ] Invalidate bot paths on bubble explosion
