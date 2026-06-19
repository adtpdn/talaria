---
title: "Wire take_powerup VFX on Powerup Pickup"
id: "096"
status: done
priority: 02
sprint: beta
category: VFX
description: "Trigger the take_powerup AnimatedSprite3D when players/bots pick up holo powerup tiles."
modified: "2026-06-19"
---
### Goal / Risk

The take_powerup VFX node existed in player.tscn but was never triggered by any script — no visual feedback on powerup pickup.

### Solution

Added play_skill_vfx("take_powerup") call inside add_powerup_from_item() in special_tiles_manager.gd, using the same auth/RPC guard pattern as the 4 skill VFX.

### Acceptance Criteria

- [x] VFX plays on all peers when any player picks up holo tile (11-14)
- [x] Uses multiplayer auth/RPC guard (player.rpc path)
- [x] Fires from add_powerup_from_item() — all 3 pickup code paths covered
