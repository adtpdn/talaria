---
title: "Gauntlet: Smack Mechanic"
id: "071"
status: "done"
priority: 01
sprint: alpha
category: CORE
description: "Implement the 'Smack' sabotage system allowing players to push opponents into sticky zones."
modified: "2026-06-03"
---

# Gauntlet: Smack Mechanic

## Problem
Without PvP interaction, Gauntlet is a survival race. The Smack mechanic adds a competitive layer, allowing players to actively sabotage opponents and push them into traps.

## Solution
Extend `PlayerMovementManager.try_push()` with a charge/cooldown system and "sticky landing" rules.

### Mechanic Design
1. **State Machine:**
    - **Cooldown (8s):** Auto-refill energy bar.
    - **Charged (3s):** Player model turns pink. Active window for hits.
    - **Consumption:** Energy consumed if window expires without a hit.
2. **Execution:**
    - **The Push:** Target is pushed **3 cells** away.
    - **Sticky Landing:** If the target touches a sticky cell during the push, they stop immediately and become `trapped`.
    - **Stun:** Target is stunned for 1.0s after landing.
3. **Smack Clash:** If two players smack simultaneously in range: both are stunned (1.0s), no push occurs, both bars consumed.

## Benefits
- **Interactive Chaos:** Turns the arena into a tactical battleground.
- **Synergy:** Creates high-skill combos (Lure $\rightarrow$ Smack into Candy).
- **Risk/Reward:** The 3s charge window telegraphs intent and makes the attacker vulnerable.

## Acceptance Criteria
- **State Flow:** Verify 8s refill and 3s pink "charged" state.
- **Push Logic:** Confirm 3-cell push distance and 1.0s stun.
- **Sticky Interaction:** Verify that pushing a player into a sticky cell triggers an immediate `trapped` state.
- **Clash Logic:** Verify simultaneous smacks result in mutual stuns and no movement.

## Migration Checklist
- [ ] Add `smack_cooldown` and `smack_charged` to `GauntletManager`.
- [ ] Implement pink model feedback via `player.rpc("sync_modulate", Color.PINK)`.
- [ ] Extend `PlayerMovementManager.try_push()` with sticky path-checking.
- [ ] Implement "Smack Clash" detection using server timestamps.
- [ ] Add 1.0s stun duration to targets.
