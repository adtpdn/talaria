---
title: "Gauntlet: Bot AI — Sticky Avoidance & Pathfinding"
id: "075"
status: "todo"
blocked_by: ["068", "082"]
priority: 02
sprint: alpha
category: AI
description: "Adapt Bot controllers to navigate the grid while avoiding sticky cells, candy bubbles, and telegraphed growth zones."
modified: "2026-06-23"
---

# Gauntlet: Bot AI — Sticky Avoidance & Pathfinding

## Problem
Standard bots follow shortest path, leading directly into sticky cells or candy bubble explosion zones. In v2, bots need "survival intelligence" for the ground growth system — avoiding growing candy, navigating through shrinking safe routes, and using Cleanser when trapped.

## Solution
Adapt `BotController` and `BotStrategicPlanner` for the growth-based hazard system:

### AI Logic (v2)
1. **Danger-Aware Pathfinding:** A* cost modification:
   - Normal Cell: Cost = 1
   - Sticky Cell: Cost = ∞ (blocked)
   - Telegraphed Cell: Cost = 10 (high cost, avoid if possible)
   - Bubble Warning Area: Cost = 8 (avoid 3×3 explosion zones)
2. **Reactive Dodging:** If on telegraphed cell → "evade" to nearest non-telegraphed neighbor
3. **Strategic Planning:** Prioritize nearest mission tile NOT currently telegraphed or in bubble warning
4. **Stuck Recovery:** If no A* path exists to any mission → `escapeSticky()` — move away from nearest sticky cell
5. **Cleanser Auto-Use:** If trapped and has Cleanser → automatically activate
6. **Smack Interaction:** Bots smack other bots if in range and near sticky zone

### Path Invalidation
Bot paths must be invalidated when:
- Sticky cells appear (growth tick)
- Candy bubbles explode
- A bot gets trapped

### What Changed from v1
- Old: "Cannon Avoidance" — avoid projectile landing zones
- New: "Sticky Avoidance" — avoid growing ground candy and bubble zones
- Old: Pathfinding only considered telegraphed cells
- New: Pathfinding considers sticky, telegraphed, AND bubble warning areas
- Added: Stuck recovery fallback when no path exists
- Added: Auto-cleanser usage when trapped

## Acceptance Criteria
- Bots deviate from shortest path when target is telegraphed
- Bots move off telegraphed cells within 0.5s
- Bots never enter sticky cells unless they have a Cleanser
- Bots auto-use Cleanser when trapped
- Bots recover when no path exists (move away from sticky)
- Bots use Smack mechanic against other bots
- Bot paths are invalidated when grid changes

## Migration Checklist
- [ ] Update `BotStrategicPlanner` to include `TILE_TELEGRAPH` and bubble zones in cost-map
- [ ] Implement "Immediate Evade" logic in `BotController`
- [ ] Add sticky-cell and bubble awareness to pathfinding weights
- [ ] Implement `escapeSticky()` fallback for stuck bots
- [ ] Add path invalidation hooks on growth tick and bubble explosion
- [ ] Implement auto-cleanser usage in `trap_player()` for bots
- [ ] Implement "Smack" logic for bots
- [ ] Test in 4-bot match to ensure diverse behavior
