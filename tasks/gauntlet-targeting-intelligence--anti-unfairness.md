---
title: "Gauntlet: Targeting Intelligence & Anti-Unfairness"
id: "073"
status: "done"
priority: 02
sprint: alpha
category: CORE
description: "Implement advanced targeting logic for the Candy Cannon to ensure the game is challenging but fair."
modified: "2026-06-03"
---

# Gauntlet: Targeting Intelligence & Anti-Unfairness

## Problem
Random targeting can lead to "unfair" outcomes: hitting one player repeatedly, instantly boxing players in, or wasting shots on already sticky areas. The targeting must be weighted to maintain "Controlled Chaos."

## Solution
Implement a weighted targeting system in `CandyCannonController` with strict fairness constraints.

### Targeting Weights
- **60% - Player Proximity:** Target non-sticky cells adjacent to active players.
- **25% - Route Blocking:** Target bottlenecks between players and goals.
- **10% - Random:** Target any random non-sticky cell.
- **5% - Chaos:** Target any cell (including sticky) for visual clutter.

### Anti-Unfairness Rules
- **No Double-Taps:** Cannon cannot target the same player in consecutive volleys.
- **Safe-Spacing:** 2×2 shots must be offset from the player's center.
- **Exit Guarantee:** Use `EnhancedGridMap.initialize_astar()` to ensure at least one path exists from each player to a safe region.
- **Endgame Exception:** Exit guarantees are disabled in the final 30 seconds.

## Benefits
- **Fair Competition:** Reduces frustration from perceived "targeting."
- **Strategic Pressure:** Forces movement and prevents "camping" in corners.
- **Professional Feel:** The NPC feels like an active adversary rather than a random generator.

## Acceptance Criteria
- **Weighting Check:** Verify ~60% of shots land near players over 100 volleys.
- **Unfairness Check:** Confirm no player is hit in two consecutive volleys.
- **Path Validation:** Verify players are not fully boxed in before the final 30s.
- **Endgame Transition:** Confirm aggressive route-blocking becomes possible after 2:30.

## Migration Checklist
- [ ] Implement `_select_targets(count)` with 60/25/10/5 weights.
- [ ] Add `last_targeted_player_id` tracking.
- [ ] Integrate `EnhancedGridMap.initialize_astar()` for path validation.
- [ ] Implement the "Endgame" timer override.
- [ ] Create `_get_route_blocking_target()` based on player-to-goal paths.
