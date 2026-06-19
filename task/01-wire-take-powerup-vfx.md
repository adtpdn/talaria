# Task: Wire take_powerup VFX on Powerup Pickup

**Status:** Done
**Date:** 2026-06-19

## Problem
The `take_powerup` AnimatedSprite3D node existed in `player.tscn` with sprite frames and animation config, but no script ever called `play_skill_vfx("take_powerup")`. Players/bots picking up holo powerup tiles (IDs 11-14) got no visual feedback.

## Changes

### `scripts/managers/special_tiles_manager.gd`
- Added VFX trigger inside `add_powerup_from_item()` — the single chokepoint all 3 pickup code paths route through
- Follows the same auth/RPC guard pattern used by the 4 skill VFX (`skill_speed`, `skill_freeze`, `skill_wall`, `skill_ghost`):
  ```gdscript
  if player.is_multiplayer_authority() and player.has_method("can_rpc") and player.can_rpc():
      player.rpc("play_skill_vfx", "take_powerup")
  elif player.has_method("play_skill_vfx"):
      player.play_skill_vfx("take_powerup")
  ```
- Fires after the `effect == -1` guard, so only plays on valid powerup tiles (11-14)

## Why this approach
`add_powerup_from_item()` is called from all 3 pickup paths in `playerboard_manager.gd` (lines 91, 191, 305), so one hook covers every case — no need to modify multiple call sites.
