---
title: "Sugar Rush: Auto Tile Pickup Pathing"
id: "125"
status: "todo"
priority: 02
sprint: alpha
category: AI
description: "Replace the movement-buffer system with an auto-pickup-aware path cost — bots and players prefer paths that sweep up matching tiles."
modified: "2026-06-29"
supersedes: ["083"]
---

# Sugar Rush: Auto Tile Pickup Pathing

## Problem
`_detect_movement_buffers()` and `_buffer_penalty_at(pos)` penalize cells
where a player is forced to stay. Sugar Rush replaces these with a
**pickup-aware path cost** — paths that collect more matching tiles on the
way to the goal are preferred.

## Solution
Replace buffer penalties with pickup gain.

### Changes
1. Remove `_detect_movement_buffers()` and the buffer dictionary.
2. Add `_pickup_gain_along_path(path: Array, color: Color) -> int`:
    - Walks `path` from start to end.
    - Counts tiles whose color matches `color`.
    - Returns the count.
3. Update `BotStrategicPlanner._calculate_blueprint_score` (#118) to factor
   `_pickup_gain_along_path` into the path cost.
4. Add the same helper to `PlayerMovementManager` for HUD route preview
   (optional).

## Acceptance Criteria
- Bot pathfinding prefers routes that pick up more matching tiles.
- Buffer-penalty code is gone from Sugar Rush code paths.
- Path-cost changes do not break existing movement timing.

## Migration Checklist
- [ ] Remove `_detect_movement_buffers` and `_buffer_penalty_at`.
- [ ] Add `_pickup_gain_along_path`.
- [ ] Update `#118` bot scoring to use it.
- [ ] Verify player movement still feels right.