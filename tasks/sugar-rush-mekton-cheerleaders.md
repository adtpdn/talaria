---
title: "Sugar Rush: Mekton Cheerleaders (TBD)"
id: "126"
status: "todo"
priority: 04
sprint: alpha
category: CORE
description: "Design and implement Mekton Cheerleaders — NPCs outside the board that activate per-cheerleader buffs when the player is low on the leaderboard."
modified: "2026-06-29"
---

# Sugar Rush: Mekton Cheerleaders (TBD)

## Problem
Sugar Rush includes cheerleader NPCs that stand outside the board. Each
player picks one during lobby. They activate when the player drops below a
leaderboard threshold. Per-cheerleader buffs are still **TBD** — this task
is a design + skeleton implementation.

## Solution
Add a cheerleader selection menu, a placeholder buff hook, and an
activation rule. The actual buff list is deferred to a follow-up design
doc.

### Changes
1. Add `Cheerleader` enum: at least 4 candidates (TBD names).
2. Add `player_cheerleader: Dictionary[int, Cheerleader]`.
3. Add lobby UI: cheerleader picker.
4. Add `_check_cheerleader_activation(pid)`:
    - Fires when `player_rank > leaderboard_count * 0.7` (low 30 %).
    - Calls the cheerleader's buff stub.
5. Each cheerleader exposes a single `apply_buff(player_id)` stub.

## Acceptance Criteria
- Lobby UI lets each player pick a cheerleader.
- Cheerleader picks are networked.
- Activation rule fires correctly when player is low-ranked.
- Per-cheerleader buff is a no-op until design lands.

## Migration Checklist
- [ ] Add `Cheerleader` enum.
- [ ] Add `player_cheerleader` dictionary.
- [ ] Add lobby picker UI.
- [ ] Add `_check_cheerleader_activation`.
- [ ] Stub each cheerleader's `apply_buff`.
- [ ] Document buff design (TBD).