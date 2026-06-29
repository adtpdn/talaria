---
title: "Sugar Rush: Bot AI for Candy Survival"
id: "118"
status: "todo"
priority: 02
sprint: alpha
category: AI
description: "Rework bot pathfinding for Sugar Rush — prefer candy-rich tiles, time deliveries to Mekton color, and weigh head-stack theft vs risk."
modified: "2026-06-29"
supersedes: ["073", "075"]
---

# Sugar Rush: Bot AI for Candy Survival

## Problem
`BotStrategicPlanner._calculate_candidate_score()` scores tiles for sticky
growth (priority / camping pressure / cluster growth). Sugar Rush removes
sticky growth and replaces it with **head-stack pickup and Mekton delivery**.
The bot has to be re-taught to:

1. Walk onto matching-color tiles for head-stack gain.
2. Time deliveries to the Mekton's active face color (#114).
3. Steal head-stack from low-charge players (use #116 Knock).
4. Avoid players who have knock charges pending.

## Solution
Replace the growth-candidate scorer with a delivery-cost scorer.

### Changes
1. Replace `_calculate_candidate_score` with
   `_calculate_blueprint_score(pos, player_id)`:
    - +weight for matching-color tiles within reach.
    - −weight for tiles currently held by another player's blueprint.
    - −weight for tiles in a known knock-charge blast radius.
2. Replace `BotController`'s growth-tick handler with a `_tick_blueprint()`
   hook into #113.
3. Add `_should_deliver_now(player_id) -> bool`:
    - Mekton color matches at least one candy on the player's head → true.
    - Path to Mekton is clear → true.
    - No nearby knock-charge holder → true.
4. Add `_consider_knock_steal(player_id) -> Vector2i | null`:
    - Find a target with `head_stack >= 1` in adjacent cells.
    - Returns the target's cell if a knock would succeed.
5. Update `escape_sticky()` → `escape_danger()` since sticky is no longer
   growing (kept as collision only; see #068).

## Acceptance Criteria
- Bots reliably walk onto matching-color tiles within 1 tick.
- Bots time delivery to Mekton color matches.
- Bots attempt knock-steal when a target is adjacent.
- Bots do not enter the Mekton blast radius during rush (visual cue).
- Bot paths update on Mekton color rotation.

## Migration Checklist
- [ ] Replace `_calculate_candidate_score` → `_calculate_blueprint_score`.
- [ ] Add `_should_deliver_now`.
- [ ] Add `_consider_knock_steal`.
- [ ] Rename `escape_sticky` → `escape_danger`.
- [ ] Wire to Mekton color rotation (read `current_mekton_color`).
- [ ] Wire to Ghost Charge immunity checks.