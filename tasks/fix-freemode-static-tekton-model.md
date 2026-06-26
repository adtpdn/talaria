---
title: "Fix Freemode Static Tekton Model and Powerup Logic"
id: "101"
status: done
priority: 01
sprint: alpha
category: BUG
description: "Restore correct static Tekton model in Freemode and stop Gauntlet powerup cubes/floor-freeze logic from leaking into Freemode."
modified: "2026-06-22"
---

### Goal / Risk

Freemode static Tekton used the wrong 3D model (`tekton.tscn` / `tekton_mesh.tscn` instead of `tekton_throwing_tiles.glb`).

Gauntlet-specific logic also leaked into Freemode, causing powerup cubes like the pink floating cube to spawn when a Tekton was attacked.

### Solution

1. Restored `scenes/tekton_mesh.tscn` / `tekton.tscn` for roaming Tektons.
2. Added `scenes/static_tekton_mesh.tscn` using `assets/characters/tektons/tekton_throwing_tiles.glb` for static turrets.
3. Added `scenes/static_tekton.tscn` and updated static spawning to use it when `is_static` is true.
4. Updated static Tekton animation targeting for the GLB AnimationPlayer and throw/idle clips.
5. Ensured static Tektons rotate toward the throw direction.
6. Limited Freemode Tekton tile spawning to normal tile IDs 7-10.
7. Disabled floor-freeze powerup logic in Freemode.
8. Fixed `controller` scoping in `on_thrown_landing`.

### Files Modified

- `scenes/tekton_mesh.tscn` - restored roaming Tekton mesh setup
- `scenes/tekton.tscn` - restored roaming Tekton scene setup
- `scenes/static_tekton_mesh.tscn` - new static turret mesh scene
- `scenes/static_tekton.tscn` - new static turret scene
- `scripts/static_tekton_manager.gd` - spawns static Tekton scene for static instances
- `scenes/main.gd` - spawns static Tekton scene for static instances
- `scripts/tekton.gd` - Freemode tile/powerup guard, static animation targeting, controller scoping fix
