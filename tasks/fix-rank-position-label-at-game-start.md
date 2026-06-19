---
title: "Fix Rank Position Label Showing at Game Start"
id: "098"
status: done
priority: 02
sprint: beta
category: UI
description: "Hide Position Label3D until player actually scores, fix tied rank ordering."
modified: "2026-06-19"
---
### Goal / Risk

The Position Label3D was hardcoded to "1st" and visible at game start, showing all players in 1st place before any scoring. Tied scores also got arbitrary ranks.

### Solution

- Set visible = false in player.tscn Position node
- Added score parameter to update_rank_visuals() — hides when score == 0
- Main.gd rank loop now computes standard competition ranking (tied scores share rank)

### Acceptance Criteria

- [x] No Position labels at game start (all score 0)
- [x] Label appears only after first score
- [x] Tied scores show same rank (standard competition ranking)
- [x] Colors: gold, silver, bronze, grey still apply correctly
