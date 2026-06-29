---
title: "Sugar Rush: Head Stack Multiplier + ×N Badge UI"
id: "127"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: UI
description: "Render the running ×N multiplier next to the Mekton head sprite and update it whenever the player's head-stack changes."
modified: "2026-06-29"
---

# Sugar Rush: Head Stack Multiplier + ×N Badge UI

## Problem
The Mekton head sprite should show a `×N` badge representing the player's
head-stack multiplier. The multiplier scales with stack size (TBD curve;
default: `1 + log2(stack)` or fixed ladder like `1×, 1.5×, 2×, 3×, 5×`).

## Solution
Render the badge and update it on every stack change.

### Changes
1. Add `head_stack_multiplier(stack: int) -> float`:
    - Returns the multiplier for a given stack count.
    - Default curve TBD; document in `mode_config.gd`.
2. Add `×N Badge` UI node as a child of the Mekton head sprite.
3. Add `update_head_stack_badge(pid)`:
    - Reads `player_head_stack[pid]`.
    - Computes multiplier via `head_stack_multiplier`.
    - Updates the badge text.
4. Call from:
    - `#113 _process_candy_tick` on increment.
    - `#116 transfer_head_stack` on steal.
    - `#128 delivery` on removal.

## Acceptance Criteria
- Badge visible next to Mekton head sprite for the active player.
- Updates immediately on stack change.
- Multiplier curve is documented in `mode_config.gd`.
- Badge hides when stack is 0.

## Migration Checklist
- [ ] Define multiplier curve.
- [ ] Add badge UI node.
- [ ] Add `update_head_stack_badge`.
- [ ] Wire to candy tick (#113), knock transfer (#116), delivery (#128).
- [ ] Verify at 720p / 1080p.