---
title: "Gauntlet: Movement Buffer System"
id: "083"
status: "in_progress"
priority: 02
sprint: alpha
category: CORE
description: "Implement the hidden movement buffer system that prevents the arena from becoming movement-broken too early."
modified: "2026-06-18"
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
- [ ] Add `movement_buffers: Dictionary` state (Vector2i → {penalty, created_at})
- [ ] Implement `_detect_movement_buffers()` — find SAFE cell clusters
- [ ] Implement `_decay_movement_buffers()` — reduce penalties over time
- [ ] Implement `_apply_movement_buffer_check()` — replace unsafe growth selections
- [ ] Add buffer penalty to `_calculate_candidate_score()`
- [ ] Add camping tracker per player (position, duration)
- [ ] Implement camping override (weaken buffer for campers)
- [ ] Add phase-change decay (50% reduction)
- [ ] Add final-30s removal
- [ ] Test that growth appears organic with temporary gaps
