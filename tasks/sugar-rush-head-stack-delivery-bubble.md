---
title: "Sugar Rush: Head-Stack Delivery Bubble"
id: "124"
status: "todo"
priority: 02
sprint: alpha
category: VFX
description: "Re-skin the shipped candy-bubble system as a delivery-triggered VFX/SFX burst that fires when a player delivers head-stack candies to the Mekton."
modified: "2026-06-29"
supersedes_part_of: ["082"]
---

# Sugar Rush: Head-Stack Delivery Bubble

## Problem
`_try_spawn_bubble()` / `_explode_bubble()` periodically spawn a candy
bubble on the arena that explodes into sticky cells. Sugar Rush repurposes
the bubble **only as the delivery VFX** — when a player delivers head-stack
candies to the Mekton (#128), a burst of candy particles plays. The
arena-wide bubble spawner is removed.

## Solution
Reuse the bubble visual for the delivery event only.

### Changes
1. Remove the periodic `_try_spawn_bubble()` timer from Sugar Rush.
2. Add `play_delivery_burst(pid, candy_count)`:
    - Spawns a particle burst at the Mekton node.
    - Color matches the delivered candies.
    - SFX: `candy_delivered.wav`.
3. Keep `_explode_bubble()` and the particle material for the visual only.
4. Hook `play_delivery_burst` from the delivery success path (#128).

## Acceptance Criteria
- Delivery spawns a colored burst on the Mekton.
- Burst VFX is identical to the old bubble explosion.
- No periodic arena-wide bubble spawns in Sugar Rush.
- Legacy Gauntlet still uses `_try_spawn_bubble` (gated by mode flag).

## Migration Checklist
- [ ] Gate `_try_spawn_bubble` behind a "legacy Gauntlet" mode flag.
- [ ] Add `play_delivery_burst`.
- [ ] Wire to delivery success (#128).
- [ ] Add delivery SFX.