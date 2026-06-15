---
title: Fix Freemode Static Tekton Model and Powerup Logic
status: done
priority: high
tags:
  - bug
  - 3d
  - model
  - logic
---

# Description

Fixed an issue where the static tekton in "Freemode" was using the wrong 3D model (`tekton.tscn` / `tekton_mesh.tscn` instead of the old `tekton_throwing_tiles.glb`). 
Also fixed spilled logic from "gauntlet" that caused powerup cubes (like the pink floating cube) to spawn in Freemode when a tekton is attacked.

# Changes Made

1. **Model Restoration:**
   - Changed `scenes/tekton_mesh.tscn` back to use the original model if it was replaced.
   - Restored `tekton.tscn` to use `tekton_mesh.tscn` as the roaming tekton.
   - Created a new scene `scenes/static_tekton_mesh.tscn` specifically using `assets/characters/tektons/tekton_throwing_tiles.glb` for the static turret.
   - Created a new scene `scenes/static_tekton.tscn` that uses `static_tekton_mesh.tscn`.
   - Updated `StaticTektonManager` and `Main` to spawn `static_tekton.tscn` instead of `tekton.tscn` when `is_static` is true.

2. **Animation and Visuals Fix:**
   - Modified `play_animation` in `tekton.gd` to properly target the built-in AnimationPlayer within the `tekton_throwing_tiles.glb` model for the static turret (`Armature|tekton_throw_tile` and `Armature|tekton_idle`).
   - Ensured static tekton rotates to face the direction it throws tiles.

3. **Freemode Logic Fix:**
   - Updated `spawn_tiles_around` in `tekton.gd` to explicitly check for `GameMode.Mode.FREEMODE`.
   - In Freemode, tektons now only spawn normal tiles (IDs 7-10), preventing powerup cubes from spawning.
   - Disabled the `temporarily_change_floor` (floor freeze effect) in Freemode.
   - Fixed a variable scoping error with the `controller` variable in the `on_thrown_landing` method.
