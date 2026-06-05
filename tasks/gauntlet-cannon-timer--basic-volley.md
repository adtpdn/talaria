---
title: "Gauntlet: Cannon Timer & Basic Volley"
id: "067"
status: todo
priority: 01
sprint: alpha
category: CORE
description: "Implement the core timing loop and basic projectile firing logic for the Candy Cannon NPC."
assignee: "default"
cron_job: "pending"
---

# Gauntlet: Cannon Timer & Basic Volley

## Problem
The Candy Cannon is the primary driver of tension. Without a precise timing loop, volleys would feel either too random or too predictable. The system must manage a strict 5-second interval and coordinate 5 distinct shots per volley.

## Solution
Implement a server-authoritative timer and volley manager within `GauntletManager` and `CandyCannonController`.

### Technical Approach
1. **Volley Timer:** Use a `cannon_timer` in `_process(delta)`. Trigger `_fire_volley()` and reset when `cannon_timer >= 5.0s`.
2. **Volley Execution:** Fire `volley_size` (5) shots with a small offset (0.1s) for a rhythmic "thump" effect.
3. **Targeting:** Implement basic random non-sticky cell selection for initial development.
4. **Projectile Sync:** Use the `tekton.gd` pattern: Server calculates target $\rightarrow$ `rpc("sync_projectile", start, end)` $\rightarrow$ Client tweens candy mesh.

## Benefits
- **Rhythmic Tension:** Predictable 5s beats create "safe windows" for tactical movement.
- **Server Authority:** Prevents clients from desyncing the "danger zones".
- **Scalability:** Variable interval/size allows for easy lobby-based difficulty tuning.

## Acceptance Criteria
- **Timing Accuracy:** Verify volleys fire exactly every 5 seconds.
- **Volley Count:** Confirm exactly 5 projectiles are spawned per volley.
- **Visual Sync:** Verify all clients see projectiles travel from center to target.
- **Impact Trigger:** Confirm projectiles trigger the sticky cell logic on arrival.

## Migration Checklist
- [ ] Add `cannon_timer`, `cannon_interval`, and `volley_size` to `GauntletManager`.
- [ ] Implement `_process` loop to trigger `_fire_volley()`.
- [ ] Create `CandyCannonController._fire_volley()` for random target selection.
- [ ] Integrate `sync_projectile` RPC for visual travel.
- [ ] Verify loop stability over a 180s match.
