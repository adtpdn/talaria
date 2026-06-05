---
title: "Gauntlet: Tile Spawning & Mission System"
id: "074"
status: todo
priority: 01
sprint: alpha
category: CORE
description: "Implement the spawning of colored tiles and the mission-based scoring system."
---

# Gauntlet: Tile Spawning & Mission System

## Problem
Gauntlet needs a primary objective beyond survival. Players must be driven to move across the arena and risk the candy cannon. A mission system requiring specific color collection provides this drive.

## Solution
Adapt `GoalsCycleManager` and `GoalManager` for Gauntlet-specific missions.

### Implementation Details
1. **Tile Spawning:** Use `StopNGoManager._spawn_mission_tiles()` pattern to distribute colors across the 20x20 grid, excluding the 3x3 NPC zone.
2. **Mission Definition:** Implement cycles (e.g., Cycle 1: Collect 3 Red $\rightarrow$ 3 Blue). Use count-based collection.
3. **Scoring:** Award points on mission completion and a "Survival Bonus" at 180s.
4. **Dynamic Respawning:** Respawn tiles in new random non-sticky locations upon mission completion to maintain movement.

## Benefits
- **Objective-Driven Movement:** Forces players to traverse the arena, increasing hazard encounters.
- **Pacing:** Creates natural peaks (scoring) and troughs (preparation).
- **Infrastructure Reuse:** Leverages existing `GoalsCycleManager` to reduce dev time.

## Acceptance Criteria
- **Spawn Check:** Confirm colored tiles appear randomly outside the center 3x3 zone.
- **Mission Flow:** Verify HUD updates and Mission 2 begins after completing Mission 1.
- **Scoring Accuracy:** Confirm points are correctly added to the user's score.
- **Respawn Check:** Verify new tiles appear after a mission is finished.

## Migration Checklist
- [ ] Implement `_spawn_mission_tiles()` in `GauntletManager`.
- [ ] Configure `GoalsCycleManager` with Gauntlet goal requirements.
- [ ] Integrate scoring callbacks to update HUD and leaderboard.
- [ ] Implement respawn logic for mission tiles.
- [ ] Verify tile collection is blocked on `TILE_STICKY` cells.
