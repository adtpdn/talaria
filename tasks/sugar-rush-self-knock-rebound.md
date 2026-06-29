---
title: "Sugar Rush: Self-Knock Rebound"
id: "131"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: CORE
description: "Knocking a player who carries no head-stack candies rebounds the knock back at the attacker."
modified: "2026-06-29"
---

# Sugar Rush: Self-Knock Rebound

## Problem
Knocking a head-stack-less player is wasted — there's nothing to steal.
Sugar Rush punishes this by **rebinding** the knock onto the attacker.

## Solution
Add a rebound check to `consume_knock_charge` (#116).

### Changes
1. In `consume_knock_charge(attacker_pid, target_pid)`:
    - Check `player_head_stack[target_pid]`.
    - If `target_pid` is ghost-active (#117) → knock fails silently.
    - If `target_pid` has 0 head-stack and is not ghost-active →
      rebound: apply the same shove to `attacker_pid` instead.
    - If `target_pid` has ≥ 1 candy → transfer (#116) and shove normally.
2. Add `candies_stolen` signal — payload now includes
   `rebound: bool`.
3. Add VFX distinction: blue burst on normal knock, red burst on rebound.

## Acceptance Criteria
- Knocking a head-stack-less player → attacker is shoved.
- Knocking a ghost-active player → no effect, no charge consumed (TBD).
- Knocking a stacked player → transfer + shove.
- VFX differentiates rebound from normal knock.

## Migration Checklist
- [ ] Add rebound branch in `consume_knock_charge`.
- [ ] Update `candies_stolen` signal payload.
- [ ] Add rebound VFX.
- [ ] Decide: does ghost-active refund the charge? (TBD).