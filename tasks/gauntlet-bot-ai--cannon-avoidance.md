---
title: "Gauntlet: Bot AI — Cannon Avoidance"
id: "075"
status: "done"
priority: 02
sprint: alpha
category: AI
description: "Adapt Bot controllers to navigate the grid while avoiding candy cannon telegraphs and sticky cells."
modified: "2026-06-03"
---

# Gauntlet: Bot AI — Cannon Avoidance

## Problem
Standard bots follow the shortest path. In Gauntlet, this leads them directly into telegraphs or sticky traps. Bots need "survival intelligence" to be viable opponents.

## Solution
Adapt `BotController` and `BotStrategicPlanner` to incorporate danger-avoidance into pathfinding.

### AI Logic
1. **Danger-Aware Pathfinding:** Modify A* costs:
    - **Normal Cell:** Cost = 1.
    - **Sticky Cell:** Cost = $\infty$.
    - **Telegraphed Cell:** Cost = 10.
2. **Reactive Dodging:** If a bot is on a telegraphed cell, trigger "evade" to the nearest non-telegraphed neighbor, prioritizing distance from the center NPC.
3. **Strategic Planning:** Prioritize the nearest mission tile that is NOT currently telegraphed.
4. **Smack Interaction:** Bots should attempt to smack other bots if they are in range and near a sticky zone.

## Benefits
- **Realistic Opponents:** Bots that dodge and react create a more living, challenging game.
- **Testing Utility:** Allows for better balance testing of cannon rates and impact sizes.
- **Reduced Frustration:** Prevents bots from simply walking into traps.

## Acceptance Criteria
- **Avoidance Check:** Confirm bots deviate from the shortest path when a target is telegraphed.
- **Reaction Time:** Verify bots move off telegraphed cells within 0.5s.
- **Path Validity:** Confirm bots never enter sticky cells unless they have a Cleanser.
- **Competitive Behavior:** Verify bots use the Smack mechanic against other bots.

## Migration Checklist
- [ ] Update `BotStrategicPlanner` to include `TILE_TELEGRAPH` in cost-map.
- [ ] Implement "Immediate Evade" logic in `BotController`.
- [ ] Add sticky-cell awareness to pathfinding weights.
- [ ] Implement "Smack" logic for bots.
- [ ] Test in 4-bot match to ensure diverse behavior.
