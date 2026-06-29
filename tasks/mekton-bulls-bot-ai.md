---
title: "Mekton Bulls: Bot AI (Bull Avoidance + Knock Steal Pathing)"
id: "141"
status: "todo"
blocked_by: ["136", "138", "139"]
priority: 02
sprint: alpha
category: AI
description: "Rework bot AI for the Mekton Bulls mode — bot pathfinding avoids the roaming bull, times knock pickups, and accounts for the shrinking arena."
modified: "2026-06-29"
---

# Mekton Bulls: Bot AI (Bull Avoidance + Knock Steal Pathing)

## Problem
Sugar Rush's `BotStrategicPlanner` (`tasks/sugar-rush-bot-ai.md` ->
`#118`) is tuned for head-stack pickups and Mekton delivery timing.
Mekton Bulls has a different shape:

- No head-stack — bots must walk their 3 × 3 blueprint tiles
  (`#138`).
- A roaming bull (`#136`) knocks bots out on contact — bots must
  avoid it.
- The arena shrinks (`#135`) — bots must stay inside or be flooded
  (`#137`).

## Solution
Extend `BotStrategicPlanner` with Mekton-Bulls-specific scoring.

### Concrete Changes
1. Reuse the existing `_calculate_candidate_score` scorer; parameterize
   it for `mode = "MEKTON_BULLS"`.
2. Add new scoring branches:
    - **Bull-distance penalty:** `+cost` when a path passes within
      `2` cells of a `MektonBull`.
    - **Boundary penalty:** `+cost` when a path crosses the current
      `arena_size` boundary (will be eliminated by `#137`).
    - **Blueprint-tile bonus:** `-cost` for cells inside the bot's
      active 3 × 3 (`#138`).
3. Add `_should_use_freeze(bot) -> bool`:
    - Returns true when a bull is within 3 cells of the bot's
      current position. Triggers the Freeze power (`#139`).
4. Add `_should_use_knock(bot) -> Vector2i | null`:
    - Returns a target cell when:
        - Bot has a Knock charge.
        - Target is within 1 cell.
        - Target's cell + 1 cell ahead is into the bull or boundary.
5. A* path-invalidation hook:
    - Re-plan on arena shrink (`#135`).
    - Re-plan on bull state change (ROAM → CHARGE).

## Acceptance Criteria
- Bots consistently walk their 3 × 3 blueprint cells.
- Bots avoid the bull's line of sight.
- Bots use Freeze when within 3 cells of a bull.
- Bots use Knock to shove other players into the bull / boundary.
- Bots stay inside the shrinking arena.

## Migration Checklist
- [ ] Add mode branch to `_calculate_candidate_score`.
- [ ] Add bull-distance + boundary penalties.
- [ ] Add blueprint-tile bonus.
- [ ] Add `_should_use_freeze` / `_should_use_knock`.
- [ ] A* invalidation on shrink / bull state.
- [ ] Smoke-test in an 8-bot Mekton Bulls match.