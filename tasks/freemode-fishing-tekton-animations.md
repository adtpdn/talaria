---
title: "Freemode Fishing Tekton Animations"
id: "092"
status: done
priority: 01
sprint: beta
category: ASSETS
description: "Animate both meshes (ted_bones body + fishing_acc rod) of the freemode fishing tektons by merging the GLB's two animations into one looped clip."
modified: "2026-06-18"
---

### Goal / Risk

Freemode arena fishing tektons don't animate — all 3 instances of `tekton_fishing_animation.glb` sit static. Static tekton throw in free mode doesn't face direction or play throw animation.

Follow-up: only the `ted_bones` body mesh animated; the separate `fishing_acc` mesh (rod/reel/thread/hook) stayed static.

### Solution

1. Created `tekton_fishing_autoplay.gd` — drives the GLB animations and loops them via AnimationPlayer
2. Attached script to all 3 fishing animation instances in `freemode.tscn`
3. Fixed static tekton throw: player now faces tekton toward throw direction and plays throw animation
4. Fixed AnimationPlayer path in `tekton.gd` for static turrets (`Visuals/tekton/AnimationPlayer`)
5. Fixed animation names from `tekton_throw_tile` to actual GLB name `ted_bones_001|Tekton Throwing Tiles|Anima_Layer`
6. Fixed static_tekton_controller.gd idle resume (no idle anim exists for static mesh — stops instead)

### Both-mesh fix (follow-up)

The GLB contains two independent skeletons, each with its own animation:
- `ted_bones` skin → `ted_bones.002|NEW|Anima_Layer` (character body)
- `fishing_acc` skin → `hook.003|NEW|Anima_Layer` (rod/reel/thread/hook)

A single AnimationPlayer plays only one clip at a time, so the old loop over `get_animation_list()` calling `play()` per clip left only the alphabetically-last (`ted_bones…`) playing — the rod stayed frozen.

Fix: since the two animations target disjoint node sets, `tekton_fishing_autoplay.gd` now **merges all tracks from every source animation into one combined `Animation`** (`LOOP_LINEAR`), registers it in an AnimationLibrary, and plays that single clip — so both meshes animate and loop together.

### Files Modified

- scenes/arena/freemode.tscn — added autoplay script to 3 fishing tekton instances
- scripts/tekton_fishing_autoplay.gd — merges both GLB animations into one looped clip so body + rod animate together
- scenes/player.gd — sync_throw_tekton now faces tekton + plays throw anim, removed duplicate end_world_pos
- scripts/tekton.gd — fixed AnimationPlayer path for static turrets, fixed throw animation name
- scripts/static_tekton_controller.gd — fixed animation name, idle resume stops instead of playing nonexistent idle
