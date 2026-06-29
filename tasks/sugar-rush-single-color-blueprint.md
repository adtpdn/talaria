---
title: "Sugar Rush: Single-Color Blueprint Auto-Pickup"
id: "119"
status: "halt"
halt_reason: "need confirmation"
priority: 01
sprint: alpha
category: CORE
description: "Rework mission tiles into single-color blueprints with automatic pickup — walking over a matching tile counts toward the player's blueprint progress."
modified: "2026-06-29"
supersedes: ["074"]
---

# Sugar Rush: Single-Color Blueprint Auto-Pickup

## Problem
`setup_mission_tiles()` distributes colored goal tiles across the 20×20
arena for the **objective** system (multi-color, hand-collected). Sugar Rush
flattens this into a **single-color blueprint** that ticks up automatically
as the player walks over matching tiles.

## Solution
Replace the goal-tile manager with a per-player blueprint tracker.

### Changes
1. Replace `setup_mission_tiles()` with `_assign_initial_blueprints()`:
    - For each player, pick one color (from {R, G, B, Y}) and a target
      count (e.g. 8 tiles).
    - Distribute matching tiles evenly across the 18×18 arena (#112).
2. Add `player_blueprint[pid]: { color: Color, target: int, progress: int }`.
3. On `_process_candy_tick` (#113):
    - If player's tile color matches `player_blueprint.color` → increment
      `progress`.
    - If `progress >= target` → spawn candy on head (#127), reset
      `progress = 0`, re-roll a new color.
4. Half-point rule (#129) for finishing a blueprint via off-color pickup.
5. Remove `goal_manager.gd` calls for Sugar Rush; keep the file for legacy
   modes.

## Acceptance Criteria
- Each player has exactly one active blueprint at a time.
- Walking onto a matching tile increments progress automatically.
- Reaching the target spawns a candy on the head.
- Blueprints are evenly distributed across the arena.
- Bots and humans share the same blueprint logic.

## Migration Checklist
- [ ] Add `player_blueprint` dictionary.
- [ ] Implement `_assign_initial_blueprints`.
- [ ] Hook `_process_candy_tick` → blueprint progress.
- [ ] Hook completion → head-stack spawn (#127).
- [ ] Implement half-point off-color path (#129).
- [ ] Decide which color set is allowed (TBD: 4 or 6 colors).