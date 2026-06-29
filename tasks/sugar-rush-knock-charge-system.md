---
title: "Sugar Rush: Knock Charge System"
id: "116"
status: "todo"
priority: 01
sprint: alpha
category: CORE
description: "Convert the Smack Mechanic into a 5-charge spawn gear that shoves other players and steals their head-stack candies."
modified: "2026-06-29"
supersedes: ["071"]
---

# Sugar Rush: Knock Charge System

## Problem
`gauntlet_manager.has_smack_charged(pid)` and `consume_smack(pid)` define a
single-use Smack ability. Sugar Rush promotes this to a **5-charge spawn
gear** with new semantics — knocking a player **steals their head-stack
candies** (or rebounds; see #131).

## Solution
Replace the boolean Smack charge with an integer counter and add candy
transfer.

### Changes
1. Rename `has_smack_charged` → `has_knock_charge(pid) -> bool`.
2. Rename `consume_smack` → `consume_knock_charge(pid) -> bool` (returns
   false when empty).
3. Add `knock_charges: Dictionary[int, int]` initialized to **5** per
   player at spawn (see #130 for the "5 OR 5 ghost" choice).
4. Add `transfer_head_stack(from_pid, to_pid) -> int`:
    - Reads `player_head_stack[from_pid]`, transfers to `to_pid`.
    - Resets `player_head_stack[from_pid]` to 0.
    - Emits `candies_stolen(from_pid, to_pid, count)` signal.
5. Replace Smack's VFX with the Sugar Rush knock burst.

## Acceptance Criteria
- Each player starts with 5 knock charges (or 5 ghost charges; see #117/#130).
- Consuming a charge shoves the target 1 cell.
- If target carries head-stack candies, all of them transfer to the attacker.
- If target has no head-stack, the knock rebounds (see #131).
- Charge counter is networked (host → clients).

## Migration Checklist
- [ ] Replace `has_smack_charged` / `consume_smack` with knock-charge API.
- [ ] Add `knock_charges` dictionary.
- [ ] Add `transfer_head_stack()` function.
- [ ] Update Smack VFX → Sugar Rush knock VFX.
- [ ] Add `candies_stolen` signal.
- [ ] Wire to #118 Bot AI and #131 Self-Knock Rebound.