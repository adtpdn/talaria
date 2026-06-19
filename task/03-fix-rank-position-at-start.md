# Fix Rank Position Label Showing at Game Start

**Status:** Done

## Context
The `Position` Label3D on each player was hardcoded to `"1st"` and visible by default in the scene. Before/at game start, everyone showed a rank (and the default "1st"), even though all players had score 0. Additionally, tied scores were assigned arbitrary 1/2/3/4 by array order.

## Changes

### `scenes/player.tscn`
- Added `visible = false` to the `Position` Label3D node so it never shows "1st" before real ranking

### `scenes/player.gd` (line ~931)
- `update_rank_visuals(rank)` → `update_rank_visuals(rank, score: int = -1)`
- Added guard: if `score == 0`, hide the label and return early

### `scenes/main.gd` (line ~2266)
- Rank assignment now computes standard competition ranking (tied scores share the same rank)
- Passes player score to `update_rank_visuals` so zero-score players stay hidden

## Result
- Match start (all 0 pts) → no Position labels shown
- First player to score → shows rank, others stay hidden until they score
- Tied scores → same rank displayed
