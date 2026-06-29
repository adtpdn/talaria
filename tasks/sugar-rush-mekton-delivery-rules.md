---
title: "Sugar Rush: Mekton Delivery Rules"
id: "128"
status: "todo"
priority: 01
sprint: alpha
category: CORE
description: "Implement Mekton delivery rules — only matching-color candies deliver; mismatches stay on the head."
modified: "2026-06-29"
---

# Sugar Rush: Mekton Delivery Rules

## Problem
Players carry head-stack candies. When they step onto the Mekton's cell,
matching-color candies must be delivered (points + Sugar Rush trigger) and
non-matching candies must stay on the head. There is no current delivery
logic — `gauntlet_manager` only handles goal scoring.

## Solution
Add a delivery handler invoked when a player steps onto the Mekton.

### Changes
1. Add `attempt_delivery(pid) -> DeliveryResult`:
    - Reads `player_head_stack[pid]`.
    - Splits into `matching` and `non_matching` based on
      `current_mekton_color` (#114).
    - If `matching > 0`:
        - Add points: `matching * delivery_points_per_candy` (TBD).
        - Trigger Sugar Rush (#122): `candies_fed = matching`.
        - Pop the matching candies from the head.
        - Play delivery VFX (#124).
    - Returns `{ delivered: int, kept: int }`.
2. Wire `attempt_delivery` to the player-on-Mekton collision check.
3. Add `delivery_points_per_candy: int = 100` config.
4. Add `current_delivery_multiplier` (uses #127).

## Acceptance Criteria
- Stepping onto Mekton with matching candies → points + rush.
- Stepping onto Mekton with mismatched candies → no delivery, candies stay.
- Mixed stack → partial delivery (matching only).
- Delivery fires once per Mekton visit (no double-counting while standing).

## Migration Checklist
- [ ] Add `attempt_delivery`.
- [ ] Add `delivery_points_per_candy` config.
- [ ] Wire to player-on-Mekton collision.
- [ ] Add `DeliveryResult` struct (or dict).
- [ ] Hook to #122 Sugar Rush trigger.
- [ ] Hook to #124 delivery VFX.