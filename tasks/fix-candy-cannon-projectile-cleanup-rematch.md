---
title: "Fix Candy Cannon Projectile Cleanup on Rematch"
id: "146"
status: done
priority: 01
sprint: alpha
category: BUG
description: "Fix orphaned projectiles on candy cannon due to session timeout and rematch."
modified: "2026-06-30"
---

### Goal / Risk

When a game session times out or triggers a rematch, actively spawning projectiles from the candy cannon were orphaned on the scene tree root and persisted across the reload.

### Solution

1. Updated `scripts/controllers/candy_cannon_controller.gd` to parent spawned projectiles to the cannon itself rather than the root window (`get_tree().get_root().add_child`).
2. Enabled `projectile.top_level = true` so the projectile still behaves with independent global transforms but remains part of the cannon's lifecycle hierarchy.
3. This ensures that when the scene is reloaded/cleaned up during a rematch, the cannon and its active projectiles are cleanly destroyed together, preventing orphaned VFX.

### Files Modified

- `scripts/controllers/candy_cannon_controller.gd` - Changed projectile parenting to use `top_level = true` and `add_child(projectile)`.